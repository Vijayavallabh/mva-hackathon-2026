#!/usr/bin/env python3
"""Public single-cell BUB1B model challenge: preparation and CUDA split-half audit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import time

CELLS = ['rpe1', 'K562_essential']
ENV = Path('/home/prachh/v/mva-track2-transcriptome-20260927')


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')


def column(group, name):
    """Read the deposited AnnData 0.1 categorical encoding without pickle."""
    import numpy as np
    d = group[name]
    x = d[:]
    if '__categories' in group and name in group['__categories']:
        categories = group['__categories'][name][:]
        require((x >= 0).all() and (x < len(categories)).all(), 'Missing/invalid category')
        x = categories[x]
    if x.dtype.kind in 'SO':
        x = np.asarray([v.decode() if isinstance(v, bytes) else str(v) for v in x])
    return x


def stratified_half(strata, rng):
    """Random halves; singleton strata rotate rather than always enter the first half."""
    import numpy as np
    _, inv, count = np.unique(strata, return_inverse=True, return_counts=True)
    order = np.lexsort((rng.random(len(strata)), inv))
    within = np.arange(len(strata)) - np.repeat(np.r_[0, count.cumsum()[:-1]], count)
    side = np.empty(len(strata), dtype=np.int64)
    side[order] = (within + rng.integers(0, 2, len(count))[inv[order]]) % 2
    return side


def prepare(root):
    import h5py
    import numpy as np
    import pandas as pd
    planpath = root / 'inputs/plan.json'
    plan = json.loads(planpath.read_text())
    out = root / 'outputs/prepared'
    out.mkdir(exist_ok=False)
    receipt = json.loads((root / 'outputs/download-complete.json').read_text())
    for row in receipt['files']:
        require(digest(root/'inputs'/row['name']) == row['sha256'], 'Input digest mismatch')
    records = {}
    control_means = {}
    for cell in CELLS:
        with h5py.File(root/'inputs'/f'{cell}_raw_bulk_01.h5ad', 'r') as bulk:
            names = column(bulk['obs'], 'gene_transcript')
            cores = set(names[column(bulk['obs'], 'core_control')])
            provider = {str(n): {k: (float(bulk['obs'][k][i]) if np.isfinite(bulk['obs'][k][i]) else None) for k in
                ['num_cells_filtered','num_cells_unfiltered','fold_expr','control_expr','cnv_score_z']}
                for i,n in enumerate(names) if any('_'+q+'_' in n for q in plan['queries'])}
        with h5py.File(root/'inputs'/f'{cell}_raw_singlecell_01.h5ad', 'r') as f:
            obs = pd.DataFrame({k: column(f['obs'], k) for k in f['obs'] if not k.startswith('__')})
            var = pd.DataFrame({k: column(f['var'], k) for k in f['var'] if not k.startswith('__')})
            require(len(set(var.gene_id)) == len(var), 'Duplicate source gene ID')
            obs['core_control'] = obs.gene_transcript.isin(cores)
            obs['all_control'] = obs.gene.eq('non-targeting')
            require((~obs.core_control | obs.all_control).all(), 'Core control annotation conflict')
            # Full library UMI count is the denominator, not the truncated exported gene sum.
            require((obs.UMI_count > 0).all(), 'Invalid library denominator')
            raw = f['X'][:]
            require(np.isfinite(raw).all() and (raw >= 0).all() and (raw == np.floor(raw)).all(), 'Non-count input')
            require((raw.sum(1) <= obs.UMI_count.to_numpy()+1).all(), 'Exported count sum exceeds library')
            control_means[cell] = dict(zip(var.gene_id, raw[obs.core_control].mean(0, dtype=np.float64)))
            obs.to_csv(out/f'{cell}-obs.tsv.gz', sep='\t', index=False)
            var.to_csv(out/f'{cell}-var.tsv.gz', sep='\t', index=False)
            queries = []
            for q in plan['queries']:
                qo = obs[obs.gene.eq(q)]
                query = dict(gene=q, cells=len(qo), constructs=sorted(qo.gene_transcript.unique()),
                    guide_pairs=sorted(qo.sgID_AB.unique()), gemgroups=int(qo.gem_group.nunique()),
                    provider_summaries={k:v for k,v in provider.items() if '_'+q+'_' in k})
                positions=np.flatnonzero(var.gene_name.eq(q))
                query['measured_gene_ids'] = var.iloc[positions].gene_id.tolist()
                if len(positions)==1 and len(qo):
                    target=raw[:, positions[0]].astype(np.float64)
                    cp=target/obs.UMI_count.to_numpy()*1e4
                    baseline=[];baseline_raw=[]
                    for b in qo.gem_group:
                        cm=obs.core_control & obs.gem_group.eq(b)
                        baseline.append(float(cp[cm].mean()));baseline_raw.append(float(target[cm].mean()))
                    ref=float(np.mean(baseline));rr=float(np.mean(baseline_raw))
                    query.update(mean_target_cp10k=float(cp[qo.index].mean()), matched_control_cp10k=ref,
                        cp10k_ratio=float(cp[qo.index].mean()/ref) if ref>0 else None,
                        raw_umi_ratio=float(target[qo.index].mean()/rr) if rr>0 else None)
                queries.append(query)
            records[cell]=dict(cells=len(obs), features=len(var), batches=int(obs.gem_group.nunique()),
                core_control_cells=int(obs.core_control.sum()), all_control_cells=int(obs.all_control.sum()),
                query_metadata=queries, minimum_adjusted_umi=float(obs.core_adjusted_UMI_count.min()),
                maximum_mito_fraction=float(obs.mitopercent.max()), source_integer_counts=True,
                source_already_selected=True, selection_warning='Only deposited retained cells; excluded/dead cells unavailable.')
            del raw
    ids=sorted(g for g,v in control_means[CELLS[0]].items() if v>=.25 and control_means[CELLS[1]].get(g,0)>=.25)
    require(len(ids)>500, 'Insufficient control-selected features')
    for cell in CELLS:
        obs=pd.read_csv(out/f'{cell}-obs.tsv.gz',sep='\t',keep_default_na=False)
        var=pd.read_csv(out/f'{cell}-var.tsv.gz',sep='\t',keep_default_na=False)
        lookup={g:i for i,g in enumerate(var.gene_id)}
        positions=np.asarray([lookup[g] for g in ids]);order=np.argsort(positions)
        # h5py sorted-index requirement; restore the common ID order after reading.
        with h5py.File(root/'inputs'/f'{cell}_raw_singlecell_01.h5ad','r') as f:
            x=np.asarray(f['X'][:],dtype=np.float32)[:,positions]
        np.divide(x,obs.UMI_count.to_numpy(dtype=np.float32)[:,None],out=x)
        x*=1e4;np.log1p(x,out=x)
        require(np.isfinite(x).all(),'Nonfinite normalized data')
        np.save(out/f'{cell}-logcp10k.npy',x)
        var.iloc[positions].to_csv(out/f'{cell}-features.tsv',sep='\t',index=False)
        del x
    files={p.name:digest(p) for p in out.iterdir()}
    save(out/'manifest.json',dict(plan_sha256=digest(planpath),script_sha256=digest(__file__),
        source_receipt_sha256=digest(root/'outputs/download-complete.json'),cells=records,
        selected_common_features=len(ids),feature_ids=ids,files=files))
    print(json.dumps(dict(prepared=True,features=len(ids),cells={c:r['cells'] for c,r in records.items()})),flush=True)


def worker(root, shard, iterations=256):
    import numpy as np
    import pandas as pd
    import torch
    require(os.environ.get('CUDA_VISIBLE_DEVICES')==str(shard) and torch.cuda.device_count()==1,'GPU assignment')
    torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False
    torch.set_float32_matmul_precision('highest')
    planpath=root/'inputs/plan.json';plan=json.loads(planpath.read_text());prep=root/'outputs/prepared'
    amendment=json.loads((root/'inputs/amendment.json').read_text())
    require(amendment['original_plan_sha256']==digest(planpath),'Amendment/plan mismatch')
    tasks=[(c,'core_control',b) for c in CELLS for b in range(4)]
    cell,view,block=tasks[shard];rng=np.random.default_rng(310000+shard)
    out=root/'outputs'/f'worker-{shard}';out.mkdir(exist_ok=False)
    started=time.monotonic();manifest=json.loads((prep/'manifest.json').read_text())
    obs=pd.read_csv(prep/f'{cell}-obs.tsv.gz',sep='\t',keep_default_na=False)
    var=pd.read_csv(prep/f'{cell}-features.tsv',sep='\t',keep_default_na=False)
    x=np.load(prep/f'{cell}-logcp10k.npy',mmap_mode='r')
    require(digest(prep/f'{cell}-logcp10k.npy')==manifest['files'][f'{cell}-logcp10k.npy'],'Prepared matrix changed')
    cc=set((root/'inputs/cell-cycle.txt').read_text().split())
    masks={'all_features':np.ones(len(var),dtype=bool),
           'no_queries':~var.gene_name.isin(plan['queries']).to_numpy(),
           'no_queries_or_cycle':~var.gene_name.isin(set(plan['queries'])|cc).to_numpy()}
    batch_names,batch=np.unique(obs.gem_group,return_inverse=True);nb=len(batch_names)
    controls=obs[view].to_numpy(dtype=bool)
    nctrl=np.bincount(batch[controls],minlength=nb)
    valid_batch=nctrl>=20
    eligible=~obs.all_control.to_numpy(dtype=bool)&valid_batch[batch]
    counts=obs.loc[eligible,'gene_transcript'].value_counts()
    names=sorted(counts[counts>=30].index)
    require(len(names)>100,'Insufficient reference constructs')
    ni={g:i for i,g in enumerate(names)}
    index=np.asarray([ni.get(g,-1) for g in obs.gene_transcript])
    eligible&=index>=0
    target_rows=np.flatnonzero(eligible);control_rows=np.flatnonzero(controls&valid_batch[batch])
    index=index[target_rows];tb=batch[target_rows];cb=batch[control_rows]
    n=len(names);N=len(target_rows)
    tv=torch.as_tensor(np.asarray(x[target_rows]),device='cuda')
    cv=torch.as_tensor(np.asarray(x[control_rows]),device='cuda')
    ti=torch.as_tensor(index,device='cuda');tbatch=torch.as_tensor(tb,device='cuda')
    cbatch=torch.as_tensor(cb,device='cuda')
    sums=torch.zeros((n,len(var)),device='cuda');sums.index_add_(0,ti,tv)
    control_sum=torch.zeros((nb,len(var)),device='cuda');control_sum.index_add_(0,cbatch,cv)
    cn=torch.as_tensor(np.bincount(cb,minlength=nb),device='cuda',dtype=torch.float32)
    mean=control_sum/cn.clamp_min(1)[:,None]
    batch_counts=np.zeros((n,nb),dtype=np.float64);np.add.at(batch_counts,(index,tb),1)
    bct=torch.as_tensor(batch_counts,device='cuda',dtype=torch.float32)
    total=bct.sum(1);profiles=(sums-bct@mean)/total[:,None]
    require(torch.isfinite(profiles).all().item(),'Invalid full profile')
    np.save(out/'full-profiles.npy',profiles.cpu().numpy())
    save(out/'registration.json',dict(cell=cell,control_view=view,seed_block=block,seed=310000+shard,
        plan_sha256=digest(planpath),amendment_sha256=digest(root/'inputs/amendment.json'),
        script_sha256=digest(__file__),prepared_manifest_sha256=digest(prep/'manifest.json'),
        device=torch.cuda.get_device_name(),torch=torch.__version__,iterations=iterations,
        reference_constructs=n,target_cells=N,control_cells=len(control_rows),
        excluded_batches=batch_names[~valid_batch].tolist(),names=names,
        feature_counts={k:int(v.sum()) for k,v in masks.items()},
        null_definition='Matched non-targeting subsamples versus disjoint remaining controls; conditional resampling, not calibrated biological FDR.'))
    query_indices={q:[i for i,g in enumerate(names) if '_'+q+'_' in g] for q in plan['queries']}
    require(all(len(v)<=1 for v in query_indices.values()),'Multiple query constructs need explicit extension')
    save(out/'missing-queries.json',[q for q,v in query_indices.items() if not v])
    comparisons=0;max_error=0.;cuda_seconds=0.;rows=[]
    # Track full-panel per-construct retrieval distributions, including failures.
    rank_sums={k:np.zeros((n,4),dtype=np.float64) for k in masks}
    tmask={k:torch.as_tensor(np.flatnonzero(v),device='cuda') for k,v in masks.items()}
    qflat=[i for v in query_indices.values() for i in v]
    qgene={i:q for q,v in query_indices.items() for i in v}
    strata=index*nb+tb
    def norm(z):
        z=z-z.mean(1,keepdim=True)
        length=torch.linalg.vector_norm(z,dim=1,keepdim=True)
        require((length>1e-10).all().item(),'Degenerate profile')
        return z/length
    def product(a,b):
        nonlocal comparisons,max_error,cuda_seconds
        before,after=torch.cuda.Event(enable_timing=True),torch.cuda.Event(enable_timing=True)
        before.record();z=a@b.T;after.record();torch.cuda.synchronize()
        cuda_seconds+=before.elapsed_time(after)/1000;comparisons+=z.numel()
        # FP64 original-coordinate dot product, not an unrelated synthetic comparison.
        if comparisons < 20_000_000 or len(rows)%96==0:
            for i,j in [(0,0),(len(a)//2,len(b)//2),(len(a)-1,len(b)-1)]:
                ref=float(np.dot(a[i].cpu().numpy().astype(np.float64),b[j].cpu().numpy().astype(np.float64)))
                max_error=max(max_error,abs(ref-float(z[i,j])))
        require(max_error<=2e-5 and torch.isfinite(z).all().item(),'Numerical control failed')
        return z
    # Cross-profile panels retained once per worker, with no top-hit filtering.
    for key,mask in tmask.items():
        p=norm(profiles[:,mask]);np.save(out/(key+'-full-correlations.npy'),product(p,p).cpu().numpy())
    for rep in range(iterations):
        side=stratified_half(strata,rng)
        cside=stratified_half(cb,rng)
        aidx=np.flatnonzero(side==0);cidx=np.flatnonzero(cside==0)
        ac=np.bincount(index[aidx],minlength=n);bc=total.cpu().numpy()-ac
        require((ac>0).all() and (bc>0).all(),'Empty construct half')
        asums=torch.zeros_like(sums);asums.index_add_(0,ti[aidx],tv[aidx])
        acontrol=torch.zeros_like(control_sum);acontrol.index_add_(0,cbatch[cidx],cv[cidx])
        nac=np.bincount(cb[cidx],minlength=nb);nbc=cn.cpu().numpy()-nac
        require((nac[valid_batch]>=10).all() and (nbc[valid_batch]>=10).all(),'Undercovered independent control half')
        amean=acontrol/torch.as_tensor(nac,device='cuda',dtype=torch.float32).clamp_min(1)[:,None]
        bmean=(control_sum-acontrol)/torch.as_tensor(nbc,device='cuda',dtype=torch.float32).clamp_min(1)[:,None]
        ab=np.zeros((n,nb),dtype=np.float32);np.add.at(ab,(index[aidx],tb[aidx]),1)
        ab=torch.as_tensor(ab,device='cuda')
        ap=(asums-ab@amean)/torch.as_tensor(ac,device='cuda',dtype=torch.float32)[:,None]
        bp=(sums-asums-(bct-ab)@bmean)/torch.as_tensor(bc,device='cuda',dtype=torch.float32)[:,None]
        for key,mask in tmask.items():
            a,b=norm(ap[:,mask]),norm(bp[:,mask]);sc=product(a,b);diag=sc.diag()
            forward=1+(sc>diag[:,None]+1e-6).sum(1)
            reverse=1+(sc>diag[None,:]+1e-6).sum(0)
            f=forward.cpu().numpy();r=reverse.cpu().numpy()
            rank_sums[key]+=np.column_stack([f,r,f==1,r==1])
            for i in qflat:
                rows.append(dict(repeat=rep,representation=key,gene=qgene[i],construct=names[i],
                    correlation=float(diag[i]),forward_rank=int(f[i]),reverse_rank=int(r[i]),
                    cells_a=int(ac[i]),cells_b=int(bc[i]),reference_constructs=n))
        if rep%16==0:
            print(json.dumps(dict(shard=shard,repeat=rep,iterations=iterations,elapsed=time.monotonic()-started)),flush=True)
    pd.DataFrame(rows).to_csv(out/'split-query-records.tsv.gz',sep='\t',index=False)
    for key,value in rank_sums.items():
        frame=pd.DataFrame(value,columns=['sum_forward_rank','sum_reverse_rank','forward_top1','reverse_top1'])
        frame.insert(0,'construct',names);frame.to_csv(out/(key+'-all-construct-retrieval.tsv.gz'),sep='\t',index=False)
    # Distinct controls for pseudo-query and its reference; finite conditional null.
    nullrows=[]
    for i in qflat:
        batch_n=batch_counts[i].astype(int)
        possible=all(nctrl[b]-c>=20 for b,c in enumerate(batch_n) if c)
        if not possible:
            nullrows.append(dict(gene=qgene[i],evaluable=False,reason='insufficient_disjoint_controls'))
            continue
        pools={b:np.flatnonzero(cb==b) for b in np.flatnonzero(batch_n)}
        norms={k:[] for k in masks}
        for rep in range(iterations):
            pick=np.concatenate([rng.choice(pools[b],batch_n[b],replace=False) for b in pools])
            # CP10k profiles remain additive means; pseudo-cells never enter reference.
            chosen=torch.zeros_like(control_sum);chosen.index_add_(0,cbatch[pick],cv[pick])
            counts_t=torch.as_tensor(batch_n,device='cuda',dtype=torch.float32)
            ref=(control_sum-chosen)/(cn-counts_t).clamp_min(1)[:,None]
            pseudo=(chosen.sum(0)-counts_t@ref)/int(batch_n.sum())
            for key,mask in tmask.items():
                v=pseudo[mask];norms[key].append(float(torch.linalg.vector_norm(v-v.mean())))
        for key,mask in tmask.items():
            v=profiles[i,mask];observed=float(torch.linalg.vector_norm(v-v.mean()))
            nullrows.append(dict(gene=qgene[i],representation=key,evaluable=True,observed_norm=observed,
                null_norms=norms[key],greater_equal=sum(v>=observed for v in norms[key]),draws=iterations,
                descriptive_tail=(1+sum(v>=observed for v in norms[key]))/(1+iterations)))
    save(out/'matched-control-null.json',nullrows)
    # Excluding a sequencing partition is a sampling sensitivity, never a biological replicate.
    logo=[]
    for i in qflat:
        for b in np.flatnonzero(batch_counts[i]):
            keep=target_rows[(index==i)&(tb!=b)]
            if len(keep)<30:continue
            vals=torch.as_tensor(np.asarray(x[keep]),device='cuda')-mean[torch.as_tensor(batch[keep],device='cuda')]
            m=vals.mean(0,keepdim=True)
            for key,mask in tmask.items():
                score=product(norm(m[:,mask]),norm(profiles[:,mask]))[0]
                logo.append(dict(gene=qgene[i],excluded_gemgroup=int(batch_names[b]),remaining_cells=len(keep),
                    representation=key,correlation=float(score[i]),rank=1+int((score>score[i]+1e-6).sum()),
                    denominator=n,reference_includes_retained_cells=True))
    save(out/'leave-partition-out.json',logo)
    save(out/'completion.json',dict(shard=shard,complete=True,iterations=iterations,cell=cell,control_view=view,
        comparisons=comparisons,cuda_product_seconds=cuda_seconds,max_cpu_error=max_error,
        elapsed_seconds=time.monotonic()-started,maximum_cuda_allocated_bytes=torch.cuda.max_memory_allocated(),
        biology_validated=False,drug_ranking_changed=False))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['prepare','worker']);p.add_argument('root',type=Path)
    p.add_argument('--shard',type=int);p.add_argument('--iterations',type=int,default=256)
    a=p.parse_args()
    if a.mode=='prepare':prepare(a.root)
    else:worker(a.root,a.shard,a.iterations)
