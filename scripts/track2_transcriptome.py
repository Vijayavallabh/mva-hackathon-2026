#!/usr/bin/env python3
"""Public LINCS landmark reanalysis; never reads gated subject files.

Run prepare on the owner host after the public download, then worker 0..7.
All write destinations must be new. Fixed scientific design is in the JSON plan.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import time

PREFIX = 'GSE92742_Broad_LINCS_'


def digest(path, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    with Path(path).open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalize(values):
    import numpy as np
    x = np.asarray(values, dtype=np.float64)
    require(np.isfinite(x).all(), 'Nonfinite values')
    x = x - x.mean(axis=-1, keepdims=True)
    norm = np.linalg.norm(x, axis=-1, keepdims=True)
    require((norm > 1e-12).all(), 'Constant or degenerate vector')
    return x / norm


def ranked(values):
    import numpy as np
    from scipy.stats import rankdata
    require(np.isfinite(values).all(), 'Nonfinite values before ranking')
    return normalize(rankdata(values, axis=-1, method='average'))


def bh(values):
    import numpy as np
    p = np.asarray(values, float)
    require(np.isfinite(p).all() and ((p >= 0) & (p <= 1)).all(), 'Invalid p-values')
    order = np.argsort(p)
    q = np.minimum.accumulate((p[order] * len(p) / np.arange(1, len(p)+1))[::-1])[::-1]
    result = np.empty_like(p)
    result[order] = np.minimum(q, 1)
    return result.tolist()


def quality(row):
    return bool(float(row['distil_nsample']) >= 3 and
                float(row['distil_cc_q75']) >= .2 and float(row['tas']) >= .2)


def half_splits(n):
    # All unique partitions when equal halves; first 1000 otherwise. No random selection.
    left = list(itertools.islice(itertools.combinations(range(n), n//2), 1000))
    if n % 2 == 0:
        left = [x for x in left if 0 in x]
    return [(list(a), [i for i in range(n) if i not in a]) for a in left]


def gpu_ranked(x):
    """Average tied ranks, centered and unit normalized, on the last axis."""
    import torch
    require(bool(torch.isfinite(x).all()), 'Nonfinite GPU rank input')
    s, order = torch.sort(x, dim=-1)
    pos = torch.arange(x.shape[-1],device=x.device).expand_as(order)
    first = torch.ones_like(s,dtype=torch.bool)
    first[...,1:] = s[...,1:] != s[...,:-1]
    last = torch.ones_like(first)
    last[...,:-1] = s[...,:-1] != s[...,1:]
    lo = torch.where(first,pos,0).cummax(dim=-1).values
    hi = torch.flip(torch.flip(torch.where(last,pos,x.shape[-1]-1),[-1]).cummin(dim=-1).values,[-1])
    ranks = torch.empty_like(x)
    ranks.scatter_(-1,order,(lo.to(x.dtype)+hi.to(x.dtype))/2)
    ranks -= ranks.mean(dim=-1,keepdim=True)
    norm = torch.linalg.vector_norm(ranks,dim=-1,keepdim=True)
    require(bool(torch.all(norm > 1e-12)), 'Constant GPU rank vector')
    return ranks/norm


def gpu_median(x, dim):
    import torch
    sorted_x=torch.sort(x,dim=dim).values
    n=x.shape[dim]
    return (sorted_x.select(dim,(n-1)//2)+sorted_x.select(dim,n//2))/2


def metadata(root):
    import pandas as pd
    directory = root/'inputs'
    meta = pd.read_csv(directory/(PREFIX+'sig_info.txt.gz'), sep='\t', dtype=str, keep_default_na=False)
    metrics = pd.read_csv(directory/(PREFIX+'sig_metrics.txt.gz'), sep='\t', keep_default_na=False)
    require(meta.sig_id.is_unique and metrics.sig_id.is_unique, 'Duplicate metadata ID')
    metrics = metrics.set_index('sig_id')
    for col in ['distil_nsample', 'distil_cc_q75', 'tas']:
        meta[col] = meta.sig_id.map(metrics[col]).astype(float)
    require(meta[['distil_nsample','distil_cc_q75','tas']].notna().all().all(), 'Missing QC metadata')
    return meta


def prepare(root):
    import gzip
    import shutil
    import h5py
    import numpy as np
    import pandas as pd
    started = time.monotonic()
    out = root/'outputs/prepared'
    out.mkdir(exist_ok=False)
    plan_path = root/'inputs/plan.json'
    plan = json.loads(plan_path.read_text())
    checksums = {}
    with gzip.open(root/'inputs/GSE92742_SHA512SUMS.txt.gz', 'rt') as f:
        for line in f:
            value, name = line.strip().split()
            checksums[name.lstrip('*')] = value
    inputs = []
    for name in sorted(checksums):
        path = root/'inputs'/name
        if not path.exists():
            continue
        measured = digest(path, 'sha512')
        require(measured == checksums[name], 'Upstream SHA512 mismatch: '+name)
        inputs.append(dict(name=name, bytes=path.stat().st_size, sha512=measured, sha256=digest(path)))
    matrix = root/'inputs'/plan['matrix']
    require(any(i['name'] == matrix.name for i in inputs), 'Matrix not checked against upstream')
    raw = matrix.with_suffix('')
    with gzip.open(matrix, 'rb') as source, raw.open('xb') as target:
        shutil.copyfileobj(source, target, 8*1024*1024)
    meta = metadata(root).set_index('sig_id')
    genes = pd.read_csv(root/'inputs'/(PREFIX+'gene_info.txt.gz'), sep='\t', dtype=str)
    require(genes.pr_gene_id.is_unique, 'Duplicate gene ID')
    lm = set(genes.loc[genes.pr_is_lm == '1', 'pr_gene_id'])
    with h5py.File(raw, 'r') as f:
        decode = lambda xs: [x.decode() if isinstance(x, bytes) else str(x) for x in xs]
        row_ids = decode(f['0/META/ROW/id'][:])
        col_ids = decode(f['0/META/COL/id'][:])
        require(len(set(col_ids)) == len(col_ids) and set(col_ids) == set(meta.index), 'Matrix/signature mismatch')
        require(len(set(row_ids)) == len(row_ids), 'Duplicate matrix gene')
        positions = np.array([i for i, x in enumerate(row_ids) if x in lm])
        require(len(positions) == len(lm) == 978, 'Expected 978 measured landmarks')
        d = f['0/DATA/0/matrix']
        require(d.shape == (len(col_ids), len(row_ids)), 'Unexpected GCTX orientation')
        x = np.lib.format.open_memmap(out/'landmarks.npy', mode='w+', dtype='float32', shape=(len(col_ids),978))
        for start in range(0, len(col_ids), 1024):
            block = d[start:start+1024, :][:,positions]
            require(np.isfinite(block).all(), 'Nonfinite matrix values')
            x[start:start+len(block)] = block
        x.flush()
        meta = meta.loc[col_ids].reset_index()
        meta.to_csv(out/'signatures.tsv.gz', sep='\t', index=False)
        genes.set_index('pr_gene_id').loc[[row_ids[i] for i in positions]].reset_index().to_csv(out/'landmarks.tsv', sep='\t', index=False)
    require(len(meta) == 473647, 'Unexpected signature count')
    require((meta.pert_type == 'trt_cp').sum() == plan['compound_universe']['expected_profiles'], 'Compound count mismatch')
    query = meta[(meta.pert_type == 'trt_sh.cgs') & (meta.pert_iname == 'BUB1B')]
    require(len(query) == 14 and query.cell_id.nunique() == 11, 'Query context mismatch')
    write_json(out/'manifest.json', dict(created_utc=datetime.now(timezone.utc).isoformat(),
        source_inputs=inputs, plan_sha256=digest(plan_path), script_sha256=digest(__file__),
        matrix_shape=[473647,978], landmark_matrix_sha256=digest(out/'landmarks.npy'),
        metadata_sha256=digest(out/'signatures.tsv.gz'), genes_sha256=digest(out/'landmarks.tsv'),
        query_ids=sorted(query.sig_id.tolist()), elapsed_seconds=time.monotonic()-started))
    print(json.dumps(dict(prepared=True,queries=len(query),elapsed_seconds=time.monotonic()-started)), flush=True)


def worker(root, shard):
    import importlib.metadata
    import numpy as np
    import pandas as pd
    import torch
    from scipy.stats import rankdata
    require(0 <= shard < 8, 'Shard must be 0..7')
    require(os.environ.get('CUDA_VISIBLE_DEVICES') == str(shard) and torch.cuda.device_count() == 1,
            'Expose exactly the assigned H100')
    require('H100' in torch.cuda.get_device_name(0), 'Expected H100')
    torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.set_float32_matmul_precision('highest')
    start = time.monotonic()
    out = root/f'outputs/shard-{shard}'
    out.mkdir(exist_ok=False)
    prep = root/'outputs/prepared'
    plan_path = root/'inputs/plan.json'
    plan = json.loads(plan_path.read_text())
    manifest = json.loads((prep/'manifest.json').read_text())
    require(manifest['plan_sha256'] == digest(plan_path), 'Plan changed after preparation')
    meta = pd.read_csv(prep/'signatures.tsv.gz', sep='\t', keep_default_na=False)
    genes = pd.read_csv(prep/'landmarks.tsv', sep='\t', dtype=str)
    values = np.load(prep/'landmarks.npy', mmap_mode='r')
    cp_idx = np.flatnonzero(meta.pert_type.eq('trt_cp'))
    cp_meta = meta.iloc[cp_idx].reset_index(drop=True)
    target_gene = genes.index[genes.pr_gene_symbol.eq('BUB1B')].item()
    # One shared GPU matrix for all chemical profiles, rank normalized within profile.
    cp_cpu = ranked(np.asarray(values[cp_idx])).astype(np.float32)
    cp = torch.from_numpy(cp_cpu).cuda()
    write_json(out/'registration.json', dict(created_utc=datetime.now(timezone.utc).isoformat(), shard=shard,
        plan_sha256=digest(plan_path), script_sha256=digest(__file__), prepared_manifest_sha256=digest(prep/'manifest.json'),
        lock_sha256=digest(root/'uv.lock'), packages={p:importlib.metadata.version(p) for p in ['torch','numpy','scipy','pandas','h5py']},
        device=torch.cuda.get_device_name(0), cuda=torch.version.cuda, tf32=False,
        precision='float32 GPU connectivity; float64 GPU matched-statistic resampling and CPU audit'))
    summaries = []
    for qi in range(shard, len(manifest['query_ids']), 8):
        qid = manifest['query_ids'][qi]
        qrow = meta[meta.sig_id.eq(qid)].iloc[0]
        context = meta.cell_id.eq(qrow.cell_id) & meta.pert_itime.eq(qrow.pert_itime)
        q = ranked(values[meta.index[meta.sig_id.eq(qid)].item()][None,:])[0]
        qgpu = torch.tensor(q, dtype=torch.float32, device='cuda')
        sh_idx = np.flatnonzero(context & meta.pert_type.eq('trt_sh'))
        non_idx = sh_idx[meta.iloc[sh_idx].pert_iname.ne('BUB1B').to_numpy()]
        require(len(non_idx) >= 50, 'Insufficient same-context shRNA reference')
        nr_cpu = ranked(values[non_idx]).astype(np.float32)
        nr = torch.from_numpy(nr_cpu).cuda()
        # Principal axis of rank-normalized profiles (uncentered across profiles).
        # This is shared-pattern removal, not a causal growth correction.
        cov = nr.T @ nr
        _, eig = torch.linalg.eigh(cov)
        pc1 = eig[:,-1:]
        cgs_idx = np.flatnonzero(context & meta.pert_type.eq('trt_sh.cgs'))
        gmeta = meta.iloc[cgs_idx].reset_index(drop=True)
        grank = ranked(values[cgs_idx]).astype(np.float32)
        growth_pos = np.flatnonzero(gmeta.pert_iname.isin(plan['growth_sensitivity_genes']))
        spaces = [('raw', None), ('shared_pc1_removed', pc1)]
        growth_genes = gmeta.iloc[growth_pos].pert_iname.tolist()
        if len(growth_pos) >= 3:
            _, s, vh = torch.linalg.svd(torch.tensor(grank[growth_pos], device='cuda'), full_matrices=False)
            basis = vh[s > s.max()*1e-6].T
            spaces.append(('growth_span_removed', basis))

        def unit(x):
            length = torch.linalg.vector_norm(x, dim=-1, keepdim=True)
            require(bool(torch.all(length > 1e-8)), 'Degenerate projected signature')
            return x / length

        # Unique reagents, independent of the provider CGS membership.
        bub = meta[context & meta.pert_type.eq('trt_sh') & meta.pert_iname.eq('BUB1B')]
        reagent_ids = sorted(bub.pert_id.unique().tolist())
        reagent_values = np.array([np.median(values[bub.index[bub.pert_id.eq(r)].to_numpy()],axis=0) for r in reagent_ids],dtype=np.float64)
        rr = ranked(reagent_values)
        pair = rr @ rr.T
        pair_values = pair[np.triu_indices(len(rr),1)]
        splits = half_splits(len(rr))
        split_scores = [float(ranked(reagent_values[a].mean(0)[None,:])[0] @
                              ranked(reagent_values[b].mean(0)[None,:])[0]) for a,b in splits]
        split_median = float(np.median(split_scores))
        # Null draws whole non-BUB1B reagent vectors, distinct within each resample.
        non_meta = meta.iloc[non_idx]
        null_ids = sorted(non_meta.pert_id.unique().tolist())
        null_values = np.array([np.median(values[non_meta.index[non_meta.pert_id.eq(r)].to_numpy()],axis=0) for r in null_ids],dtype=np.float32)
        rng = np.random.default_rng(plan['seed'] + qi)
        null_statistic = []
        ngpu=torch.tensor(null_values,dtype=torch.float64,device='cuda')
        left=torch.tensor([a for a,b in splits],device='cuda')
        right=torch.tensor([b for a,b in splits],device='cuda')
        null_discrepancy=0.
        for offset in range(0, plan['resamples'], 64):
            count = min(64,plan['resamples']-offset)
            draws = np.array([rng.choice(len(null_values),len(rr),replace=False) for _ in range(count)])
            selected=ngpu[torch.from_numpy(draws).cuda()]
            ra=gpu_ranked(selected[:,left].mean(2))
            rb=gpu_ranked(selected[:,right].mean(2))
            stat=gpu_median((ra*rb).sum(-1),1).cpu().numpy()
            if offset==0:
                # Independent CPU audit uses exactly the same full statistic and draws.
                sample=null_values[draws[:3]].astype(float)
                cpu=np.median([np.einsum('ij,ij->i',ranked(sample[:,a].mean(1)),ranked(sample[:,b].mean(1))) for a,b in splits],axis=0)
                null_discrepancy=float(np.max(np.abs(stat[:3]-cpu)))
                require(null_discrepancy<=2e-5,'GPU null statistic audit failed')
            null_statistic.extend(stat.tolist())
        tail = (1+sum(x >= split_median for x in null_statistic))/(1+len(null_statistic))
        np.savez_compressed(out/f'query-{qi}-reagent-checks.npz', pairwise=pair, split_scores=split_scores,
                            null_median_split_scores=null_statistic)
        matched = np.flatnonzero(cp_meta.cell_id.eq(qrow.cell_id))
        named = np.flatnonzero(cp_meta.cell_id.eq(qrow.cell_id) & cp_meta.pert_iname.isin(plan['named_compounds']))
        qsummary = dict(query_id=qid, query_index=qi, cell_id=qrow.cell_id, knockdown_time=qrow.pert_itime,
            unique_reagents=reagent_ids, n_reagents=len(rr), median_target_z=float(np.median(reagent_values[:,target_gene])),
            published_vs_reconstructed_correlation=float(q @ ranked(reagent_values.mean(0)[None,:])[0]),
            pairwise_median=float(np.median(pair_values)), split_median=split_median, splits=len(splits),
            split_null_tail=tail, null_draws=len(null_statistic), null_cpu_gpu_max_difference=null_discrepancy, growth_genes=growth_genes,
            n_matched_compound_profiles=len(matched), n_genetic_references=len(cgs_idx), spaces=[],
            caveat='CGS membership and independent seeds unverified; knockdown is not selected alleles; no joint drug/knockdown treatment')
        loo = np.array([ranked(np.delete(reagent_values,i,axis=0).mean(0)[None,:])[0] for i in range(len(rr))])
        for name,basis in spaces:
            c = cp if basis is None else unit(cp - (cp @ basis) @ basis.T)
            query = qgpu if basis is None else unit(qgpu - (qgpu @ basis) @ basis.T)
            scores = (c @ query).cpu().numpy()
            require(np.isfinite(scores).all(), 'Nonfinite correlations')
            # Independent CPU implementation, including projection with GPU basis.
            check_ids = np.unique(np.r_[np.linspace(0,len(cp)-1,97,dtype=int),named])
            check_cpu = cp_cpu[check_ids].astype(float)
            qcpu = q.copy()
            if basis is not None:
                bcpu = basis.cpu().numpy().astype(float)
                check_cpu = normalize(check_cpu-(check_cpu@bcpu)@bcpu.T)
                qcpu = normalize(qcpu-(qcpu@bcpu)@bcpu.T)
            discrepancy = float(np.max(np.abs(check_cpu@qcpu - scores[check_ids])))
            require(discrepancy <= 2e-5, 'GPU/CPU tolerance failed')
            np.save(out/f'query-{qi}-{name}-all-compounds.npy', scores)
            refs = torch.tensor(grank,device='cuda')
            if basis is not None:
                refs=refs-(refs@basis)@basis.T
            # Projected-out controls have undefined residual correlation. Exclude
            # them explicitly from the reference denominator instead of amplifying
            # float roundoff into an apparent biological signal.
            valid_refs=(torch.linalg.vector_norm(refs,dim=-1)>1e-5).cpu().numpy()
            if name=='growth_span_removed':
                valid_refs[growth_pos]=False
            refs=unit(refs[valid_refs])
            space_gmeta=gmeta.loc[valid_refs].reset_index(drop=True)
            # Full same-context genetic x chemical reference matrix; compressed floats.
            connectivity = np.lib.format.open_memmap(out/f'query-{qi}-{name}-genetic-compound.npy',
                mode='w+',dtype='float32',shape=(len(space_gmeta),len(matched)))
            for k in range(0,len(matched),2048):
                connectivity[:,k:k+2048] = (refs @ c[matched[k:k+2048]].T).cpu().numpy()
            connectivity.flush()
            ld = torch.tensor(loo,dtype=torch.float32,device='cuda')
            ld = ld if basis is None else unit(ld-(ld@basis)@basis.T)
            loo_scores = (ld @ c[named].T).cpu().numpy()
            rows=[]
            for j,idx in enumerate(named):
                r=cp_meta.iloc[idx]
                comp=matched[cp_meta.iloc[matched].pert_itime.eq(r.pert_itime).to_numpy()]
                local_index=np.flatnonzero(matched==idx).item()
                ref_scores=np.asarray(connectivity[:,local_index])
                controls={gene:float(np.median(ref_scores[space_gmeta.pert_iname.eq(gene)]))
                          for gene in plan['mechanism_controls'] if space_gmeta.pert_iname.eq(gene).any()}
                rows.append(dict(signature_id=r.sig_id, compound=r.pert_iname, dose=str(r.pert_idose),time=str(r.pert_itime),
                    correlation=float(scores[idx]), quality_pass=quality(r),
                    metadata_quality={k:float(r[k]) for k in ['distil_nsample','distil_cc_q75','tas']},
                    negative_tail_fraction=float(np.mean(scores[comp] <= scores[idx])),ranking_denominator=len(comp),
                    gene_reference_negative_tail_fraction=float(np.mean(ref_scores <= scores[idx])),
                    mechanism_control_correlations=controls,loo_min=float(loo_scores[:,j].min()),loo_max=float(loo_scores[:,j].max())))
            # Keep every matched profile score and its metadata; no best-dose selection.
            table=cp_meta.iloc[matched][['sig_id','pert_id','pert_iname','cell_id','pert_idose','pert_itime']].copy()
            table['correlation']=scores[matched]
            table.to_csv(out/f'query-{qi}-{name}-matched.tsv.gz',sep='\t',index=False)
            space_gmeta[['sig_id','pert_iname']].to_csv(out/f'query-{qi}-{name}-genetic-ids.tsv',sep='\t',index=False)
            qsummary['spaces'].append(dict(name=name,max_cpu_gpu_abs_difference=discrepancy,
                genetic_reference_count=len(space_gmeta),excluded_genetic_references=gmeta.loc[~valid_refs,'sig_id'].tolist(),
                named_compounds=rows))
            del connectivity
            if basis is not None:
                del c
        write_json(out/f'query-{qi}.json',qsummary)
        summaries.append(qsummary)
        print(json.dumps(dict(query=qid,shard=shard,done=True,elapsed_seconds=time.monotonic()-start)),flush=True)
    torch.cuda.synchronize()
    write_json(out/'summary.json',dict(shard=shard,query_ids=[q['query_id'] for q in summaries],
        elapsed_seconds=time.monotonic()-start,peak_allocated_gib=torch.cuda.max_memory_allocated()/1024**3,
        complete=True,clinical_validation=False))


def aggregate(root, output):
    rows=[]
    for shard in range(8):
        folder=root/f'outputs/shard-{shard}'
        require(json.loads((folder/'summary.json').read_text())['complete'], 'Incomplete shard')
        rows.extend(json.loads(p.read_text()) for p in folder.glob('query-*.json'))
    rows.sort(key=lambda r:r['query_index'])
    require([r['query_index'] for r in rows] == list(range(14)), 'Missing or duplicate context')
    qvals=bh([r['split_null_tail'] for r in rows])
    for r,q in zip(rows,qvals):
        r['split_null_BH_q']=q
        r['operational_query_gate']=bool(r['n_reagents']>=6 and r['median_target_z']<0 and
                                        r['pairwise_median']>0 and r['split_median']>0 and q<=.05)
    result=dict(schema_version=1,plan_sha256=digest(root/'inputs/plan.json'),
        created_utc=datetime.now(timezone.utc).isoformat(),queries=rows,
        gpu_runs=[json.loads((root/f'outputs/shard-{s}/summary.json').read_text()) for s in range(8)],
        rescue_priority=None,phase='unconfirmed',clinical_exposure_margin=None,
        wet_lab_performed_by_this_project=False,drug_ranking_changed=False,
        interpretation='Public perturbation reanalysis; no patient expression, selected-genotype function, joint treatment or clinical validation')
    write_json(output,result)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['prepare','worker','aggregate'])
    p.add_argument('root',type=Path)
    p.add_argument('--shard',type=int)
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    if a.command=='prepare': prepare(a.root)
    elif a.command=='worker': worker(a.root,a.shard)
    else: aggregate(a.root,a.output)
