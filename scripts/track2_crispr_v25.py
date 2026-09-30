#!/usr/bin/env python3
"""Fixed-plan public LINCS2020 falsification, on eight owner-host H100s.

CUDA products are descriptive expression comparisons, never efficacy estimates.
All outputs use new paths. Dependencies: frozen track2_transcriptome environment.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import itertools
import json
import os
from pathlib import Path
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        while block := f.read(8 * 1024**2):
            h.update(block)
    return h.hexdigest()


def save(path, value):
    with Path(path).open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')


def normalize(x):
    import numpy as np
    x = np.asarray(x, dtype=np.float64)
    require(np.isfinite(x).all(), 'Nonfinite input')
    x = x - x.mean(axis=-1, keepdims=True)
    n = np.linalg.norm(x, axis=-1, keepdims=True)
    require((n > 1e-12).all(), 'Constant expression vector')
    return x / n


def ranknorm(x):
    import numpy as np
    from scipy.stats import rankdata
    require(np.isfinite(x).all(), 'Nonfinite expression before ranking')
    return normalize(rankdata(x, axis=-1, method='average'))


def quality(frame):
    import pandas as pd
    return (pd.to_numeric(frame.qc_pass, errors='coerce').eq(1) &
            pd.to_numeric(frame.nsample, errors='coerce').ge(3) &
            pd.to_numeric(frame.cc_q75, errors='coerce').ge(.2) &
            pd.to_numeric(frame.tas, errors='coerce').ge(.2))


def aggregate(frame, matrix, keys):
    import numpy as np
    import pandas as pd
    records, values = [], []
    for key, group in frame.groupby(keys, sort=True):
        key = key if isinstance(key, tuple) else (key,)
        record = dict(zip(keys, key))
        record.update(profile_count=len(group), signature_ids=group.sig_id.tolist(),
                      guide_ids=sorted(set(group.pert_id)),
                      distil_ids=sorted(set('|'.join(group.distil_ids).split('|'))),
                      cell_mfc_names=sorted(set(group.cell_mfc_name)),
                      quality_passes=int(quality(group).sum()))
        records.append(record)
        values.append(np.asarray(matrix[group.index], dtype=np.float64).mean(axis=0))
    require(len(records) > 0, 'Empty aggregation')
    return pd.DataFrame(records), np.asarray(values)


def prepare(root):
    import h5py
    import numpy as np
    import pandas as pd
    start = time.monotonic()
    out = root / 'outputs/prepared'
    out.mkdir(exist_ok=False)
    plan = json.loads((root / 'inputs/plan.json').read_text())
    source = json.loads((root / 'outputs/source-manifest.json').read_text())
    for item in source['files']:
        require(digest(root / 'inputs' / item['name']) == item['sha256'], 'Changed source')
    meta = pd.read_csv(root / 'inputs/siginfo_beta.txt', sep='\t', dtype=str, keep_default_na=False)
    require(meta.sig_id.is_unique, 'Duplicate signature metadata')
    genes = pd.read_csv(root / 'inputs/geneinfo_beta.txt', sep='\t', dtype=str, keep_default_na=False)
    lm = genes[genes.feature_space.eq('landmark')].sort_values('gene_id')
    require(len(lm) == 978 and lm.gene_id.is_unique, 'Landmark definition mismatch')
    lm.to_csv(out / 'landmarks.tsv', sep='\t', index=False)
    matrices = []
    for arm, name, expected in [
        ('xpr', 'level5_beta_trt_xpr_n142901x12328.gctx', 142901),
        ('cp', 'level5_beta_trt_cp_n720216x12328.gctx', 720216),
    ]:
        with h5py.File(root / 'inputs' / name, 'r') as f:
            decode = lambda a: [v.decode() if isinstance(v, bytes) else str(v) for v in a]
            rows = decode(f['0/META/ROW/id'][:])
            columns = decode(f['0/META/COL/id'][:])
            require(len(columns) == len(set(columns)) == expected, 'Column count/uniqueness mismatch')
            require(len(rows) == len(set(rows)) == 12328, 'Row count/uniqueness mismatch')
            d = f['0/DATA/0/matrix']
            require(d.shape == (expected, 12328), 'Wrong GCTX orientation')
            index = {g: i for i, g in enumerate(rows)}
            positions = np.array([index[g] for g in lm.gene_id])
            x = np.lib.format.open_memmap(out / (arm + '.npy'), mode='w+', dtype='float32', shape=(expected, 978))
            # Sequential blocks avoid pathological HDF5 fancy-row reads.
            for begin in range(0, expected, 2048):
                block = d[begin:begin+2048][:, positions]
                require(np.isfinite(block).all(), 'Nonfinite expression values')
                x[begin:begin+len(block)] = block
            x.flush()
        m = meta.set_index('sig_id').reindex(columns).reset_index()
        missing = m.pert_type.isna()
        m[missing][['sig_id']].to_csv(out / f'{arm}-unannotated.tsv', sep='\t', index=False)
        m = m.fillna('')
        m['batch'] = m.sig_id.str.split('_').str[0]
        m['quality_pass'] = quality(m)
        m.to_csv(out / f'{arm}-metadata.tsv.gz', sep='\t', index=False)
        matrices.append(dict(arm=arm, profiles=expected, annotated=int((~missing).sum()),
                             unannotated=int(missing.sum()), sha256=digest(out / (arm+'.npy')),
                             metadata_sha256=digest(out / f'{arm}-metadata.tsv.gz')))
    xp = pd.read_csv(out/'xpr-metadata.tsv.gz', sep='\t', dtype=str, keep_default_na=False)
    b = xp[xp.cmap_name.eq('BUB1B') & xp.pert_type.eq('trt_xpr')]
    require(len(b) == 31 and b.pert_id.nunique() == 1 and b.cell_iname.nunique() == 19, 'BUB1B coverage changed')
    require(set(b.cell_iname) == set(plan['cells']), 'Cell plan mismatch')
    require(b.pert_time.eq('96').all(), 'BUB1B time mismatch')
    require(xp.pert_type.eq('trt_xpr').sum() == 140945, 'Annotated CRISPR count changed')
    b.to_csv(out/'bub1b-metadata.tsv', sep='\t', index=False)
    replicate_sets = [set(s.split('|')) for s in b.distil_ids]
    overlaps = [dict(a=b.iloc[i].sig_id, b=b.iloc[j].sig_id, shared=len(replicate_sets[i]&replicate_sets[j]))
                for i,j in itertools.combinations(range(len(b)),2) if replicate_sets[i]&replicate_sets[j]]
    old = Path('/home/prachh/v/mva-track2-rnai-20260927-v23/outputs/prepared')
    om = pd.read_csv(old/'signatures.tsv.gz', sep='\t', dtype=str, keep_default_na=False)
    og = pd.read_csv(old/'genes.tsv', sep='\t', dtype=str)
    old_gene_col = 'pr_gene_id' if 'pr_gene_id' in og else 'gene_id'
    op = {v:i for i,v in enumerate(og[old_gene_col])}
    order = [op[v] for v in lm.gene_id]
    om.to_csv(out/'rnai-metadata.tsv.gz', sep='\t', index=False)
    for space in ['raw', 'prime']:
        oldx = np.load(old/(space+'.npy'), mmap_mode='r')
        np.save(out/f'rnai-{space}.npy', np.asarray(oldx[:,order], dtype=np.float32))
    old_distils = set('|'.join(om.distil_id).split('|'))
    cp = pd.read_csv(out/'cp-metadata.tsv.gz', sep='\t', dtype=str, keep_default_na=False)
    ev = cp[cp.cmap_name.str.lower().eq('everolimus')]
    compounds = pd.read_csv(root/'inputs/compoundinfo_beta.txt', sep='\t', dtype=str, keep_default_na=False)
    compounds[compounds.pert_id.isin(ev.pert_id)].to_csv(out/'everolimus-identity.tsv', sep='\t', index=False)
    ev.to_csv(out/'everolimus-metadata.tsv', sep='\t', index=False)
    cells = pd.read_csv(root/'inputs/cellinfo_beta.txt', sep='\t', dtype=str, keep_default_na=False)
    cells[cells.cell_iname.isin(plan['cells'])][['cell_iname','cell_type','primary_disease','cell_lineage']].to_csv(out/'cell-contexts.tsv',sep='\t',index=False)
    # Exact signatures and underlying wells, not equality of gene names, define reuse.
    v19 = Path('/home/prachh/v/mva-track2-transcriptome-20260927/outputs')
    reuse = []
    for rel, file in [('GSE92742',v19/'prepared/signatures.tsv.gz'),('GSE70138',v19/'phase2-prepared/signatures.tsv.gz')]:
        older = pd.read_csv(file,sep='\t',dtype=str,keep_default_na=False)
        col = 'distil_id' if 'distil_id' in older else 'distil_ids'
        oldids = set(older.sig_id)
        wells = set('|'.join(older[col]).split('|')) if col in older else set()
        reuse.append(dict(release=rel,exact_signature_overlap=int(cp.sig_id.isin(oldids).sum()),
                          everolimus_signature_overlap=int(ev.sig_id.isin(oldids).sum()),
                          everolimus_profiles_with_shared_wells=sum(bool(set(s.split('|'))&wells) for s in ev.distil_ids)))
    save(out/'manifest.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),
         plan_sha256=digest(root/'inputs/plan.json'), script_sha256=digest(__file__),
         source_manifest_sha256=digest(root/'outputs/source-manifest.json'), matrices=matrices,
         old_rnai_manifest_sha256=digest(old/'manifest.json'), bub1b_profiles=31,bub1b_guides=1,bub1b_cells=19,
         bub1b_with_old_shared_wells=sum(bool(s&old_distils) for s in replicate_sets),
         bub1b_shared_replicate_pairs=overlaps,compound_reuse=reuse,
         everolimus_profiles=len(ev),everolimus_quality_passes=int(quality(ev).sum()),
         seconds=time.monotonic()-start))
    print((out/'manifest.json').read_text(),flush=True)


def worker(root, shard):
    import numpy as np
    import pandas as pd
    import torch
    from scipy.stats import spearmanr
    started = time.monotonic()
    out = root/f'outputs/worker-{shard}'
    out.mkdir(exist_ok=False)
    require(os.environ.get('CUDA_VISIBLE_DEVICES') == str(shard) and torch.cuda.device_count() == 1, 'GPU assignment mismatch')
    require('H100' in torch.cuda.get_device_name(0), 'Expected H100')
    torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.set_float32_matmul_precision('highest')
    plan = json.loads((root/'inputs/plan.json').read_text())
    prep = root/'outputs/prepared'
    manifest = json.loads((prep/'manifest.json').read_text())
    require(manifest['plan_sha256']==digest(root/'inputs/plan.json') and manifest['script_sha256']==digest(__file__), 'Prepared code/plan changed')
    registration = dict(shard=shard, created_utc=datetime.now(timezone.utc).isoformat(),
                        plan_sha256=digest(root/'inputs/plan.json'),script_sha256=digest(__file__),
                        manifest_sha256=digest(prep/'manifest.json'),lock_sha256=digest(root/'uv.lock'),
                        device=torch.cuda.get_device_name(0),uuid=str(torch.cuda.get_device_properties(0).uuid),
                        torch=torch.__version__,numpy=np.__version__,cuda=torch.version.cuda,tf32=False)
    save(out/'registration.json',registration)
    xm = pd.read_csv(prep/'xpr-metadata.tsv.gz',sep='\t',dtype=str,keep_default_na=False)
    cm = pd.read_csv(prep/'cp-metadata.tsv.gz',sep='\t',dtype=str,keep_default_na=False)
    rm = pd.read_csv(prep/'rnai-metadata.tsv.gz',sep='\t',dtype=str,keep_default_na=False)
    xx = np.load(prep/'xpr.npy',mmap_mode='r')
    cx = np.load(prep/'cp.npy',mmap_mode='r')
    lm = pd.read_csv(prep/'landmarks.tsv',sep='\t',dtype=str)
    keep = lm.gene_id.ne('701').to_numpy()
    require(keep.sum()==977,'BUB1B not a unique measured feature')
    counts = dict(cross_batch=0,orthogonal=0,drug=0)
    gpu_seconds = 0.
    error = 0.
    validations = []

    def product(a,b):
        nonlocal gpu_seconds,error
        ga=torch.as_tensor(np.asarray(a,dtype=np.float32),device='cuda')
        gb=torch.as_tensor(np.asarray(b,dtype=np.float32),device='cuda')
        begin=torch.cuda.Event(enable_timing=True);end=torch.cuda.Event(enable_timing=True)
        begin.record();gc=ga@gb.T;end.record();torch.cuda.synchronize()
        gpu_seconds+=begin.elapsed_time(end)/1000
        c=gc.cpu().numpy()
        require(np.isfinite(c).all(),'Nonfinite GPU matrix')
        ii=np.linspace(0,len(a)-1,min(12,len(a)),dtype=int)
        jj=np.linspace(len(b)-1,0,min(12,len(b)),dtype=int)
        e=max(abs(float(np.dot(a[i],b[j]))-float(c[i,j])) for i,j in zip(ii,jj))
        error=max(error,e);require(e<=2e-5,'GPU/CPU mismatch')
        return c

    summaries=[]
    for cell_index in range(shard,len(plan['cells']),8):
        cell=plan['cells'][cell_index]
        print('cell',cell,flush=True)
        m=xm[xm.cell_iname.eq(cell)&xm.pert_type.eq('trt_xpr')&xm.pert_time.eq('96')]
        gm,gx=aggregate(m,xx,['cmap_name'])
        gr=ranknorm(gx);gr_no=ranknorm(gx[:,keep])
        names=gm.cmap_name.tolist();bpos=names.index('BUB1B')
        gm.to_json(out/f'{cell}-gene-means.json',orient='records',indent=2)
        pm,px=aggregate(m,xx,['cmap_name','pert_id','batch'])
        pr=ranknorm(px)
        rows=[]
        batches=sorted(pm.batch.unique())
        for ba,bb in itertools.combinations(batches,2):
            ai=np.flatnonzero(pm.batch.eq(ba));bi=np.flatnonzero(pm.batch.eq(bb))
            scores=product(pr[ai],pr[bi]);counts['cross_batch']+=scores.size
            for direction,qs,rs,sc in [('forward',ai,bi,scores),('reverse',bi,ai,scores.T)]:
                reference_guides={}
                reference_wells={}
                for j,k in enumerate(rs):
                    reference_guides.setdefault(pm.iloc[k].pert_id,[]).append(j)
                    for well in pm.iloc[k].distil_ids:
                        reference_wells.setdefault(well,[]).append(j)
                for qi,q in enumerate(qs):
                    exact=reference_guides.get(pm.iloc[q].pert_id,[])
                    if len(exact)!=1:continue
                    j=int(exact[0]);ref=int(rs[j])
                    # Use a per-query eligibility mask, excluding every shared well.
                    qids=set(pm.iloc[q].distil_ids)
                    eligible=np.ones(len(rs),dtype=bool)
                    for well in qids:
                        eligible[reference_wells.get(well,[])]=False
                    if not eligible[j]:continue
                    value=float(sc[qi,j]);n=int(eligible.sum())
                    rank=1+int((sc[qi,eligible]>value+1e-6).sum())
                    rows.append(dict(cell=cell,gene=pm.iloc[q].cmap_name,guide=pm.iloc[q].pert_id,
                                     query_batch=pm.iloc[q].batch,reference_batch=pm.iloc[ref].batch,
                                     correlation=value,rank=rank,candidates=n,
                                     top_one=rank==1,top_five_percent=rank/n<=.05,
                                     query_qc_passes=int(pm.iloc[q].quality_passes),
                                     reference_qc_passes=int(pm.iloc[ref].quality_passes)))
                    if pm.iloc[q].cmap_name=='BUB1B':
                        cpu=float(spearmanr(px[q],px[ref]).statistic)
                        e=abs(value-cpu);error=max(error,e)
                        require(e<=2e-5,'BUB1B original-value Spearman mismatch')
                        validations.append(dict(cell=cell,arm='cross_batch',gpu=value,cpu=cpu,error=e))
        pd.DataFrame(rows).to_csv(out/f'{cell}-cross-batch.tsv.gz',sep='\t',index=False)
        orth=[]
        if cell in plan['rnai_parent_cells']:
            rr=rm[rm.cell_id.eq(cell)&rm.pert_type.eq('trt_sh')]
            rnames=sorted(rr.pert_iname.unique())
            nlookup={g:i for i,g in enumerate(names)}
            rlookup={g:i for i,g in enumerate(rnames)}
            indices=[rr[rr.pert_iname.eq(g)].index.to_numpy() for g in rnames]
            for space in ['raw','prime']:
                rx=np.load(prep/f'rnai-{space}.npy',mmap_mode='r')
                rv=np.asarray([np.asarray(rx[ix],dtype=np.float64).mean(axis=0) for ix in indices])
                for features,cr,ar in [('all978',gr,ranknorm(rv)),('exclude_BUB1B977',gr_no,ranknorm(rv[:,keep]))]:
                    sc=product(cr,ar);counts['orthogonal']+=sc.size
                    for gene in sorted(set(names)&set(rnames)):
                        i=nlookup[gene];j=rlookup[gene];v=float(sc[i,j])
                        row=dict(cell=cell,gene=gene,space=space,features=features,correlation=v,
                                 rnai_rank=1+int((sc[i]>v+1e-6).sum()),rnai_candidates=len(rnames),
                                 crispr_rank=1+int((sc[:,j]>v+1e-6).sum()),crispr_candidates=len(names))
                        orth.append(row)
                        if gene in ['BUB1B','MTOR']:
                            a=gx[i] if features=='all978' else gx[i,keep]
                            b=rv[j] if features=='all978' else rv[j,keep]
                            cpu=float(spearmanr(a,b).statistic);e=abs(v-cpu);error=max(error,e)
                            require(e<=2e-5,'Orthogonal original-value mismatch')
                            validations.append(dict(cell=cell,arm='orthogonal',gene=gene,space=space,features=features,gpu=v,cpu=cpu,error=e))
                    np.save(out/f'{cell}-orthogonal-{space}-{features}.npy',sc)
            pd.DataFrame(orth).to_csv(out/f'{cell}-orthogonal.tsv.gz',sep='\t',index=False)
        dm=cm[cm.cell_iname.eq(cell)&cm.pert_type.eq('trt_cp')]
        dr=ranknorm(np.asarray(cx[dm.index],dtype=np.float64))
        dp=np.flatnonzero(dm.cmap_name.str.lower().isin([s.lower() for s in plan['named_drugs']]))
        panel=[g for g in plan['mechanism_genes'] if g in names]
        panelidx=[names.index(g) for g in panel]
        named=[];bub_vectors=[]
        target=out/f'{cell}-crispr-drug-all.npy'
        allscores=np.lib.format.open_memmap(target,mode='w+',dtype='float32',shape=(len(names),len(dm)))
        common=gr[np.arange(len(gr))!=bpos].mean(axis=0)
        drug_quality=quality(dm).to_numpy()
        for begin in range(0,len(dm),8192):
            end=min(begin+8192,len(dm));sc=product(gr,dr[begin:end]);counts['drug']+=sc.size
            allscores[:,begin:end]=sc
            bub_vectors.extend(sc[bpos].tolist())
            selected=dp[(dp>=begin)&(dp<end)]
            for k in selected:
                row=dm.iloc[k];column=k-begin
                for gene,i in zip(panel,panelidx):
                    v=float(sc[i,column])
                    v_no=float(np.dot(gr_no[i],ranknorm(cx[int(dm.index[k]),keep])))
                    v_res=float(np.dot(normalize(gr[i]-common),normalize(dr[k]-common)))
                    named.append(dict(cell=cell,gene=gene,signature_id=row.sig_id,compound_id=row.pert_id,
                         compound=row.cmap_name,dose=row.pert_dose,dose_unit=row.pert_dose_unit,time_hours=row.pert_time,
                         quality_pass=bool(drug_quality[k]),nsample=row.nsample,cc_q75=row.cc_q75,tas=row.tas,
                         qc_pass=row.qc_pass,is_hiq=row.is_hiq,correlation=v,
                         exclude_BUB1B_correlation=v_no,common_response_removed_correlation=v_res,
                         reversal_rank=1+int((sc[:,column]<v-1e-6).sum()),mimic_rank=1+int((sc[:,column]>v+1e-6).sum()),
                         gene_reference_count=len(names),query_guide_count=len(gm.iloc[i].guide_ids),
                         query_profile_count=int(gm.iloc[i].profile_count),query_quality_passes=int(gm.iloc[i].quality_passes)))
                    if gene=='BUB1B' and row.cmap_name.lower()=='everolimus':
                        cpu=float(spearmanr(gx[i],cx[int(dm.index[k])]).statistic);e=abs(v-cpu);error=max(error,e)
                        require(e<=2e-5,'Drug original-value Spearman mismatch')
                        validations.append(dict(cell=cell,arm='drug',signature_id=row.sig_id,gpu=v,cpu=cpu,error=e))
        allscores.flush()
        named_frame=pd.DataFrame(named)
        named_frame.to_csv(out/f'{cell}-named-drugs.tsv.gz',sep='\t',index=False)
        columns=['sig_id','pert_id','cmap_name','pert_dose','pert_dose_unit','pert_time','quality_pass']
        bv=dm[columns].copy();bv['bub1b_correlation']=bub_vectors
        bv.to_csv(out/f'{cell}-bub1b-all-drugs.tsv.gz',sep='\t',index=False)
        summary=dict(cell=cell,crispr_profiles=len(m),crispr_genes=len(names),compound_profiles=len(dm),
                     cross_batch_queries=len(rows),cross_batch_bub1b=[r for r in rows if r['gene']=='BUB1B'],
                     benchmark_top_one=sum(r['top_one'] for r in rows),benchmark_top_five_percent=sum(r['top_five_percent'] for r in rows),
                     orthogonal_rows=len(orth),orthogonal_panel=[r for r in orth if r['gene'] in plan['mechanism_genes']],
                     bub1b_guide_count=len(gm.iloc[bpos].guide_ids),bub1b_profile_count=int(gm.iloc[bpos].profile_count),
                     bub1b_target_mean_z=float(gx[bpos,np.flatnonzero(~keep)[0]]),
                     bub1b_quality_passes=int(gm.iloc[bpos].quality_passes),
                     independent_guide_qualification=False,
                     full_drug_matrix_sha256=digest(target))
        summaries.append(summary)
        save(out/f'{cell}-summary.json',summary)
    save(out/'numeric-validation.json',dict(tolerance=2e-5,maximum_error=error,checks=validations,passed=True))
    save(out/'results.json',dict(complete=True,registration=registration,cells=summaries,comparisons=counts,
         wall_seconds=time.monotonic()-started,timed_gpu_product_seconds=gpu_seconds,
         maximum_numeric_error=error,peak_allocated_bytes=torch.cuda.max_memory_allocated(),
         peak_reserved_bytes=torch.cuda.max_memory_reserved(),drug_ranking_changed=False,
         biological_validation=False,new_neural_inference=False))
    print(json.dumps(dict(complete=True,shard=shard,comparisons=counts)),flush=True)


def combine(root):
    import pandas as pd
    prep=root/'outputs/prepared'
    runs=[json.loads((root/f'outputs/worker-{i}/results.json').read_text()) for i in range(8)]
    require(all(r['complete'] for r in runs),'Incomplete worker')
    plan=json.loads((root/'inputs/plan.json').read_text())
    cells=[c for r in runs for c in r['cells']]
    require(sorted(c['cell'] for c in cells)==sorted(plan['cells']),'Missing/duplicate cells')
    tables={}
    for label in ['cross-batch','orthogonal','named-drugs','bub1b-all-drugs']:
        paths=sorted((root/'outputs').glob(f'worker-*/*-{label}.tsv.gz'))
        frames=[]
        for p in paths:
            try:frames.append(pd.read_csv(p,sep='\t'))
            except pd.errors.EmptyDataError:continue
        table=pd.concat(frames,ignore_index=True)
        table.to_csv(root/f'outputs/{label}.tsv.gz',sep='\t',index=False)
        tables[label]=dict(rows=len(table),sha256=digest(root/f'outputs/{label}.tsv.gz'))
    save(root/'outputs/results.json',dict(version=25,complete=True,
         plan_sha256=digest(root/'inputs/plan.json'),script_sha256=digest(__file__),
         prepared=json.loads((prep/'manifest.json').read_text()),gpu_runs=runs,
         comparisons={k:sum(r['comparisons'][k] for r in runs) for k in runs[0]['comparisons']},
         tables=tables,drug_ranking_changed=False,independent_guide_qualified_contexts=0,
         new_neural_inference=False,wet_lab_performed=False))
    print(json.dumps(dict(complete=True,tables=tables)),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['prepare','worker','combine'])
    p.add_argument('root',type=Path)
    p.add_argument('--shard',type=int)
    a=p.parse_args()
    if a.command=='prepare':prepare(a.root)
    elif a.command=='worker':worker(a.root,a.shard)
    else:combine(a.root)
