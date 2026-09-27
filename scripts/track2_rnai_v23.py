#!/usr/bin/env python3
"""Public GSE106127 seed/batch falsification and orthogonal reference analysis."""
import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import shutil
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with Path(path).open('rb') as f:
        for part in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()


def save(path, data):
    with Path(path).open('x') as f:
        json.dump(data, f, indent=2, allow_nan=False)
        f.write('\n')


def ranknorm(x):
    import numpy as np
    from scipy.stats import rankdata
    x = np.asarray(x, dtype=np.float64)
    require(np.isfinite(x).all(), 'Nonfinite rank input')
    r = rankdata(x, axis=-1, method='average')
    r -= r.mean(axis=-1, keepdims=True)
    norm = np.linalg.norm(r, axis=-1, keepdims=True)
    require((norm > 1e-12).all(), 'Constant rank input')
    return r / norm


def bh(p):
    import numpy as np
    p = np.asarray(p, dtype=float)
    require(np.isfinite(p).all() and ((p >= 0) & (p <= 1)).all(), 'Invalid p')
    order = np.argsort(p)
    q = np.minimum.accumulate((p[order] * len(p) / np.arange(1, len(p)+1))[::-1])[::-1]
    out = np.empty_like(q); out[order] = np.minimum(q, 1)
    return out.tolist()


def valid_seed(s, length):
    return len(s) == length and set(s) <= set('ACGT')


def valid_draws(draw, genes, seeds=None):
    import numpy as np
    good = np.ones(len(draw), dtype=bool)
    for a, b in itertools.combinations(range(draw.shape[1]), 2):
        good &= genes[draw[:, a]] != genes[draw[:, b]]
        if seeds is not None:
            good &= seeds[draw[:, a]] != seeds[draw[:, b]]
    return good


def pair_mean(matrix, indices):
    import numpy as np
    a, b = np.triu_indices(indices.shape[-1], 1)
    return matrix[indices[..., a], indices[..., b]].mean(axis=-1)


def prepare(root):
    import h5py
    import numpy as np
    import pandas as pd
    start = time.monotonic(); out = root/'outputs/prepared'; out.mkdir(exist_ok=False)
    plan = json.loads((root/'inputs/plan.json').read_text())
    checks = {}
    with gzip.open(root/'inputs/GSE106127_SHA512SUMS.txt.gz', 'rt') as f:
        for line in f:
            checksum, name = line.split(); checks[name.lstrip('*')] = checksum
    source = []
    for name in sorted(checks):
        path = root/'inputs'/name
        if path.exists():
            require(digest(path, 'sha512') == checks[name], 'Upstream checksum mismatch: '+name)
            source.append(dict(path='inputs/'+name, bytes=path.stat().st_size, sha256=digest(path), sha512=checks[name]))
    metadata = pd.read_csv(root/'inputs/GSE106127_sig_info.txt.gz', sep='\t', dtype=str, keep_default_na=False)
    require(len(metadata)==plan['expected_signatures'] and metadata.sig_id.is_unique, 'Signature metadata mismatch')
    require(metadata.pert_type.eq('trt_sh').sum()==plan['expected_rnai_signatures'], 'RNAi count mismatch')
    require(metadata.pert_iname.eq('BUB1B').sum()==plan['expected_bub1b_signatures'], 'BUB1B count mismatch')
    genes = pd.read_csv(root/'inputs/GSE106127_gene_info.txt.gz', sep='\t', dtype=str, keep_default_na=False)
    previous = None; matrix_records = []
    for space, name in plan['matrices'].items():
        require(any(v['path']=='inputs/'+name for v in source), 'Unchecked matrix')
        packed = root/'inputs'/name; raw = packed.with_suffix('')
        with gzip.open(packed,'rb') as f, raw.open('xb') as dst:
            shutil.copyfileobj(f, dst, 8*1024*1024)
        with h5py.File(raw, 'r') as f:
            decode = lambda values: [v.decode() if isinstance(v, bytes) else str(v) for v in values]
            rid = decode(f['0/META/ROW/id'][:]); cid = decode(f['0/META/COL/id'][:])
            require(len(set(rid))==len(rid)==978 and len(set(cid))==len(cid)==len(metadata), 'Matrix IDs not unique')
            require(set(cid)==set(metadata.sig_id), 'Matrix metadata join mismatch')
            require(previous is None or previous==(rid,cid), 'Raw/PRIME ordering mismatch')
            previous = rid,cid
            d = f['0/DATA/0/matrix']; require(d.shape==(len(cid),len(rid)), 'GCTX orientation mismatch')
            x = np.lib.format.open_memmap(out/f'{space}.npy', mode='w+', dtype='float32', shape=d.shape)
            for i in range(0,len(cid),2048):
                block=d[i:i+2048]; require(np.isfinite(block).all(),'Nonfinite matrix'); x[i:i+len(block)]=block
            x.flush()
        matrix_records.append(dict(space=space, shape=list(x.shape), sha256=digest(out/f'{space}.npy')))
    metadata = metadata.set_index('sig_id').loc[cid].reset_index()
    metadata['batch'] = metadata.sig_id.str.split('_').str[0]
    metadata['replicate_id_count'] = metadata.distil_id.str.split('|').map(len)
    metadata['replicate_bin'] = metadata.replicate_id_count.clip(upper=3)
    for cell in plan['cells']:
        m = metadata[metadata.cell_id.eq(cell)&metadata.pert_type.eq('trt_sh')]
        require(m.pert_id.is_unique and m.pert_itime.nunique()==1, 'Repeated reagent or mixed time')
    metadata.to_csv(out/'signatures.tsv.gz',sep='\t',index=False)
    require(genes.pr_gene_id.is_unique and set(rid)==set(genes.pr_gene_id), 'Gene ID mismatch')
    genes.set_index('pr_gene_id').loc[rid].reset_index().to_csv(out/'genes.tsv',sep='\t',index=False)
    old = pd.read_csv(root/'inputs/v19-signatures.tsv.gz',sep='\t',dtype=str,keep_default_na=False).set_index('sig_id')
    overlap = metadata[metadata.sig_id.isin(old.index)]
    same_members = sum(set(r.distil_id.split('|'))==set(old.loc[r.sig_id,'distil_id'].split('|')) for r in overlap.itertuples())
    save(out/'manifest.json',dict(created_utc=datetime.now(timezone.utc).isoformat(), plan_sha256=digest(root/'inputs/plan.json'),
        script_sha256=digest(__file__),source=source,matrices=matrix_records,metadata_sha256=digest(out/'signatures.tsv.gz'),
        genes_sha256=digest(out/'genes.tsv'),v19_metadata_sha256=digest(root/'inputs/v19-signatures.tsv.gz'),
        v19_exact_signature_overlap=len(overlap),v19_same_distil_id_sets=same_members,
        v19_bub1b_overlap=int(overlap.pert_iname.eq('BUB1B').sum()),elapsed_seconds=time.monotonic()-start))
    print(json.dumps(dict(prepared=True,overlap=len(overlap),same_distil_sets=same_members)),flush=True)


def describe(values):
    import numpy as np
    values=np.asarray(values)
    if not len(values): return dict(n=0,mean=None,median=None,quantiles=None)
    return dict(n=int(values.size),mean=float(values.mean(dtype=np.float64)),median=float(np.median(values)),
                quantiles=[float(v) for v in np.quantile(values,[0,.05,.25,.5,.75,.95,1])])


def sample_null(corr, pools, genes, seeds, exact, total, rng, outpath, draws):
    """One slot per query reagent; distinct target genes, optional distinct seeds."""
    import numpy as np
    import torch
    if any(len(p)==0 for p in pools):
        return dict(status='unknown_empty_pool',pool_sizes=[len(p) for p in pools],tail=None)
    n=len(pools); a,b=np.triu_indices(n,1)
    aa=torch.tensor(a,device='cuda'); bb=torch.tensor(b,device='cuda')
    values=[]; accepted=0; proposed=0; cpu_error=0.
    iterator=iter(itertools.product(*pools)) if exact else None
    while (exact or accepted<draws):
        if exact:
            batch=list(itertools.islice(iterator,16384))
            if not batch: break
            d=np.asarray(batch,dtype=np.int64)
        else:
            size=min(16384,max(1024,(draws-accepted)*2))
            d=np.column_stack([rng.choice(p,size=size,replace=True) for p in pools])
        proposed+=len(d); d=d[valid_draws(d,genes,seeds)]
        if not exact: d=d[:draws-accepted]
        if len(d):
            ix=torch.as_tensor(d,device='cuda')
            v=corr[ix[:,aa],ix[:,bb]].double().mean(dim=1).cpu().numpy()
            if not values:
                cpu=corr[d[:3]].cpu().numpy()
                reference=np.array([float(np.mean([cpu[k,a0,d[k,b0]] for a0,b0 in zip(a,b)],dtype=np.float64)) for k in range(min(3,len(d)))])
                cpu_error=float(np.max(np.abs(reference-v[:3])))
                require(cpu_error<=2e-5,'Null CPU/GPU mismatch')
            values.append(v); accepted+=len(v)
        if not exact and proposed>max(draws*100,1000000):
            raise ValueError('Null rejection sampler could not fill requested draws')
    if not values:
        return dict(status='unknown_no_valid_sets',pool_sizes=[len(p) for p in pools],tail=None,proposed=proposed)
    values=np.concatenate(values)
    np.save(outpath,values)
    return dict(status='complete',kind='exact_enumeration' if exact else 'monte_carlo',pool_sizes=[len(p) for p in pools],
        cartesian_combinations=total if exact else None,draws=len(values),proposed=proposed,accepted_set_fraction=len(values)/proposed,
        summary=describe(values),null_file=outpath.name,null_sha256=digest(outpath),numeric_error=cpu_error)


def worker(root, shard):
    import importlib.metadata
    import numpy as np
    import pandas as pd
    import torch
    from scipy.stats import spearmanr, rankdata
    start=time.monotonic(); out=root/f'outputs/worker-{shard}';out.mkdir(exist_ok=False)
    require(os.environ.get('CUDA_VISIBLE_DEVICES')==str(shard) and torch.cuda.device_count()==1,'GPU assignment mismatch')
    require('H100' in torch.cuda.get_device_name(0),'Expected H100')
    torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    torch.set_float32_matmul_precision('highest')
    plan=json.loads((root/'inputs/plan.json').read_text());prep=root/'outputs/prepared'
    manifest=json.loads((prep/'manifest.json').read_text())
    require(manifest['plan_sha256']==digest(root/'inputs/plan.json') and manifest['script_sha256']==digest(__file__),'Changed plan/code after preparation')
    save(out/'registration.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),shard=shard,
        plan_sha256=digest(root/'inputs/plan.json'),script_sha256=digest(__file__),manifest_sha256=digest(prep/'manifest.json'),
        lock_sha256=digest(root/'uv.lock'),device=torch.cuda.get_device_name(0),device_uuid=str(torch.cuda.get_device_properties(0).uuid),
        torch=torch.__version__,numpy=np.__version__,cuda=torch.version.cuda,tf32=False))
    meta=pd.read_csv(prep/'signatures.tsv.gz',sep='\t',keep_default_na=False)
    genes_meta=pd.read_csv(prep/'genes.tsv',sep='\t',dtype=str)
    gene_pos={v:i for i,v in enumerate(genes_meta.pr_gene_symbol)}
    completed=[]; total_pairs=0; total_null=0; maximum_error=0.; kernel_seconds=0.
    for ci in range(shard,len(plan['cells']),8):
        cell=plan['cells'][ci];m=meta[meta.cell_id.eq(cell)&meta.pert_type.eq('trt_sh')].copy()
        positions=m.index.to_numpy();m=m.reset_index(drop=True);n=len(m)
        symbols=m.pert_iname.to_numpy();seeds6=m.seed_seq_6mer.to_numpy();seeds7=m.seed_seq_7mer.to_numpy()
        s6=np.array([valid_seed(v,6) for v in seeds6]);s7=np.array([valid_seed(v,7) for v in seeds7]);bidx=np.flatnonzero(symbols=='BUB1B')
        require(len(bidx)>=2 and len(set(seeds6[bidx]))==len(bidx),'BUB1B seeds missing/shared; revise method before inference')
        m.to_csv(out/f'{cell}-reagents.tsv.gz',sep='\t',index=False)
        for si,space in enumerate(plan['spaces']):
            stamp=f'{cell}-{space}';x=np.load(prep/f'{space}.npy',mmap_mode='r')
            raw=np.asarray(x[positions],dtype=np.float64);rank=ranknorm(raw)
            t=torch.as_tensor(rank.astype(np.float32),device='cuda')
            begin=torch.cuda.Event(enable_timing=True);end=torch.cuda.Event(enable_timing=True)
            begin.record();c=t@t.T;end.record();torch.cuda.synchronize();matrix_seconds=begin.elapsed_time(end)/1000;kernel_seconds+=matrix_seconds
            require(bool(torch.isfinite(c).all()),'Nonfinite correlations')
            cm=c.cpu().numpy();np.save(out/f'{stamp}-all-pairs.npy',cm)
            verify_pairs=[(int(a),int(b)) for a,b in zip(np.linspace(0,n-2,32,dtype=int),np.linspace(n-1,1,32,dtype=int))]
            verify_pairs+=list(itertools.combinations(bidx.tolist(),2))
            errors=[abs(float(spearmanr(raw[a],raw[b]).statistic)-float(cm[a,b])) for a,b in verify_pairs]
            err=max(errors);require(err<=2e-5,'Matrix CPU/GPU mismatch');maximum_error=max(maximum_error,err)
            special={k:[] for k in ['same_gene_different_seed6','different_gene_same_seed6','different_gene_same_seed7']}
            hist=np.zeros(2000,dtype=np.int64);bgcount=0;bgsum=0.;all_pairs=0
            bins=np.linspace(-1.000001,1.000001,2001)
            for i in range(n-1):
                v=cm[i,i+1:];jg=symbols[i+1:]==symbols[i]
                six=s6[i]&s6[i+1:];seven=s7[i]&s7[i+1:]
                js6=seeds6[i+1:]==seeds6[i];js7=seeds7[i+1:]==seeds7[i]
                for label,mask in [('same_gene_different_seed6',jg&six&~js6),('different_gene_same_seed6',~jg&six&js6),('different_gene_same_seed7',~jg&seven&js7)]:
                    if mask.any():special[label].append(v[mask])
                bv=v[~jg&six&~js6];hist+=np.histogram(bv,bins)[0];bgcount+=len(bv);bgsum+=float(bv.sum(dtype=np.float64));all_pairs+=len(v)
            stats={k:describe(np.concatenate(v) if v else []) for k,v in special.items()}
            stats['different_gene_different_seed6']=dict(n=bgcount,mean=bgsum/bgcount if bgcount else None,histogram_counts=hist.tolist(),histogram_edges=bins.tolist())
            np.savez_compressed(out/f'{stamp}-selected-pairs.npz',**{k:np.concatenate(v) if v else np.array([]) for k,v in special.items()})
            observed=float(pair_mean(cm.astype(np.float64,copy=False),bidx[None,:])[0])
            details=[]
            for i in bidx:
                samegene=(symbols==symbols[i])&(np.arange(n)!=i)&s6&(seeds6!=seeds6[i])
                sameseed=(symbols!=symbols[i])&s6&(seeds6==seeds6[i])
                target=gene_pos['BUB1B']
                details.append(dict(reagent_id=m.iloc[i].pert_id,signature_id=m.iloc[i].sig_id,seed6=seeds6[i],seed7=seeds7[i],
                    batch=m.iloc[i].batch,replicate_bin=int(m.iloc[i].replicate_bin),target_z=float(raw[i,target]),
                    target_rank=int(rankdata(raw[i],method='min')[target]),gene_peers=describe(cm[i,samegene]),seed_peers=describe(cm[i,sameseed])))
            nulls=[]
            for ai,arm in enumerate(['seed6','batch_replicates']):
                pools=[]
                for i in bidx:
                    if arm=='seed6':mask=(symbols!='BUB1B')&s6&(seeds6==seeds6[i])
                    else:mask=(symbols!='BUB1B')&s6&m.batch.eq(m.iloc[i].batch).to_numpy()&m.replicate_bin.eq(m.iloc[i].replicate_bin).to_numpy()
                    pools.append(np.flatnonzero(mask))
                total=math.prod(len(p) for p in pools);exact=arm=='seed6' and total<=plan['max_exact_seed_combinations']
                record=sample_null(c,pools,symbols,seeds6 if arm=='batch_replicates' else None,exact,total,
                    np.random.default_rng(plan['seed']+ci*100+si*10+ai),out/f'{stamp}-{arm}-null.npy',plan['null_draws'])
                record.update(arm=arm,pool_reagent_ids=[[m.iloc[j].pert_id for j in p] for p in pools],observed_mean_pair=observed)
                if record['status']=='complete':
                    vals=np.load(out/record['null_file']);k=int((vals>=observed).sum())
                    record['tail']=(k/len(vals)) if exact else (k+1)/(len(vals)+1)
                    record['at_or_above']=k;total_null+=len(vals)
                nulls.append(record)
            ortho=[];ortho_count=0
            if cell in plan['crispr_pairs']:
                xp=meta[meta.cell_id.eq(plan['crispr_pairs'][cell])&meta.pert_type.eq('trt_xpr')]
                rnagroups=m.groupby('pert_iname',sort=True).indices;ordered=sorted(rnagroups)
                rnacons=np.stack([raw[rnagroups[g]].mean(axis=0) for g in ordered]);rt=torch.as_tensor(ranknorm(rnacons).astype(np.float32),device='cuda')
                xpgenes=sorted(xp.pert_iname.unique());xpcons=np.stack([np.asarray(x[xp.index[xp.pert_iname.eq(g)]]).mean(0) for g in xpgenes])
                xt=torch.as_tensor(ranknorm(xpcons).astype(np.float32),device='cuda');oc=(xt@rt.T).cpu().numpy()
                np.save(out/f'{stamp}-orthogonal.npy',oc);save(out/f'{stamp}-orthogonal-ids.json',dict(crispr=xpgenes,rnai=ordered))
                ortho_count=oc.size
                for j,g in enumerate(xpgenes):
                    if g not in rnagroups:
                        ortho.append(dict(gene=g,status='missing_rnai'));continue
                    ri=ordered.index(g);score=float(oc[j,ri]);strict=int((oc[j]>score).sum())+1;ties=int((oc[j]==score).sum())
                    target=gene_pos.get(g)
                    ortho.append(dict(gene=g,status='complete',rnai_reagents=len(rnagroups[g]),crispr_reagents=int(xp.pert_iname.eq(g).sum()),
                        correlation=score,rank_best=strict,rank_worst=strict+ties-1,reference_genes=len(ordered),
                        rnai_target_z=None if target is None else float(rnacons[ri,target]),crispr_target_z=None if target is None else float(xpcons[j,target]),
                        top_gene=ordered[int(np.argmax(oc[j]))]))
                idxpairs=[(j,ordered.index(g)) for j,g in enumerate(xpgenes) if g in rnagroups]
                oe=max(abs(float(spearmanr(xpcons[j],rnacons[k]).statistic)-float(oc[j,k])) for j,k in idxpairs)
                maximum_error=max(maximum_error,oe);require(oe<=2e-5,'Orthogonal CPU/GPU mismatch')
            result=dict(cell=cell,time=m.pert_itime.iloc[0],space=space,rnai_reagents=n,unordered_pairs=all_pairs,
                pair_matrix_sha256=digest(out/f'{stamp}-all-pairs.npy'),matrix_kernel_seconds=matrix_seconds,numeric_error=err,
                classes=stats,bub1b=dict(n_reagents=len(bidx),unique_seed6=len(set(seeds6[bidx])),mean_pair=observed,reagents=details,nulls=nulls),
                orthogonal=ortho,orthogonal_comparisons=ortho_count,crispr_bub1b_present=any(r['gene']=='BUB1B' for r in ortho))
            save(out/f'{stamp}-result.json',result);completed.append(stamp);total_pairs+=all_pairs
            print(json.dumps(dict(completed=stamp,pairs=all_pairs,observed=observed,tail_areas=[r.get('tail') for r in nulls])),flush=True)
            del c,t,cm,raw,rank;torch.cuda.empty_cache()
    save(out/'summary.json',dict(shard=shard,complete=True,completed=completed,unordered_pairs=total_pairs,null_sets=total_null,
        cpu_gpu_max_difference=maximum_error,elapsed_seconds=time.monotonic()-start,matrix_kernel_seconds=kernel_seconds,
        peak_allocated_gib=torch.cuda.max_memory_allocated()/1024**3))


def aggregate(root):
    import numpy as np
    plan=json.loads((root/'inputs/plan.json').read_text());rows=[];runs=[];records=[]
    for s in range(8):
        directory=root/f'outputs/worker-{s}';run=json.loads((directory/'summary.json').read_text());require(run['complete'],'Incomplete GPU worker');runs.append(run)
        for path in sorted(directory.glob('*-result.json')):
            d=json.loads(path.read_text());rows.append(d)
            for r in d['bub1b']['nulls']:records.append((d,r))
    rows.sort(key=lambda x:(x['cell'],x['space']));require(len(rows)==18 and len(records)==36,'Incomplete analysis family')
    for (_,r),q in zip(records,bh([r['tail'] if r.get('tail') is not None else 1 for _,r in records])):
        r['BH_q']=q;r['excess_coherence_under_null']=r.get('tail') is not None and q<=.05 and r['observed_mean_pair']>0
    overlap=json.loads((root/'outputs/prepared/manifest.json').read_text())
    summary=dict(cells=9,spaces=2,gpus=8,rnai_signatures=116782,bub1b_signatures=55,
        unordered_pair_comparisons=sum(r['unordered_pairs'] for r in rows),null_sets=sum(r['null_sets'] for r in runs),
        orthogonal_comparisons=sum(r['orthogonal_comparisons'] for r in rows),bub1b_conditional_tests=36,
        unknown_conditional_tests=sum(r.get('tail') is None for _,r in records),
        conditional_excess_coherence=sum(r['excess_coherence_under_null'] for _,r in records),
        v19_exact_signature_overlap=overlap['v19_exact_signature_overlap'],v19_same_distil_id_sets=overlap['v19_same_distil_id_sets'],
        cpu_gpu_max_difference=max(r['cpu_gpu_max_difference'] for r in runs))
    save(root/'outputs/results.json',dict(version=23,complete=True,summary=summary,plan_sha256=digest(root/'inputs/plan.json'),
        gpu_runs=runs,rows=rows,drug_ranking_changed=False,biological_validation=False,independent_experiments_added=0,
        status=dict(rescue_priority=None,everolimus='mechanistic_probe_only',hcq='reserve',clinical_exposure_margin=None,phase='unconfirmed',wet_lab_performed=False)))
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['prepare','worker','aggregate']);p.add_argument('root',type=Path);p.add_argument('--shard',type=int);a=p.parse_args()
    require(a.root.is_absolute(),'Use absolute campaign path')
    if a.command=='prepare':prepare(a.root)
    elif a.command=='worker':worker(a.root,a.shard)
    else:aggregate(a.root)
