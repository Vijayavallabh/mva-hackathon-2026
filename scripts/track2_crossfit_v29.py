#!/usr/bin/env python3
"""Symmetric held-out-gene evaluation of public expression signatures on CUDA."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import time
from track2_orthogonal_v29 import PREP, digest, require, save


def fold_for(gene, seed, folds=5):
    return int(hashlib.sha256(f'{seed}:{gene}'.encode()).hexdigest(),16)%folds


def split_genes(names, seed, fold, queries):
    train=[i for i,g in enumerate(names) if g not in queries and fold_for(g,seed)!=fold]
    evaluate=[i for i,g in enumerate(names) if g in queries or fold_for(g,seed)==fold]
    require(not set(train)&set(evaluate) and len(train)+len(evaluate)==len(names),'Split leakage')
    return train,evaluate


def unit(x):
    import numpy as np
    n=np.linalg.norm(x,axis=-1,keepdims=True)
    require(np.isfinite(x).all() and (n>1e-12).all(),'Degenerate vector')
    return x/n


def ranks(x):
    from scipy.stats import rankdata
    z=rankdata(x,axis=-1,method='average')
    return unit(z-z.mean(axis=-1,keepdims=True))


def means(frame,matrix,column):
    import numpy as np
    names=sorted(frame[column].unique())
    return names,np.asarray([np.asarray(matrix[frame.index[frame[column].eq(g)]],dtype=np.float64).mean(0) for g in names])


def worker(root,shard):
    import numpy as np
    import pandas as pd
    import torch
    require(os.environ.get('CUDA_VISIBLE_DEVICES')==str(shard) and torch.cuda.device_count()==1,'Device assignment')
    torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False;torch.set_float32_matmul_precision('highest')
    start=time.monotonic();planpath=root/'inputs/crossfit-plan.json';plan=json.loads(planpath.read_text())
    out=root/'outputs'/f'crossfit-{shard}';out.mkdir(exist_ok=False)
    save(out/'registration.json',dict(shard=shard,plan_sha256=digest(planpath),script_sha256=digest(__file__),
        torch=torch.__version__,device=torch.cuda.get_device_name(),source_manifest_sha256=digest(PREP/'manifest.json')))
    xm=pd.read_csv(PREP/'xpr-metadata.tsv.gz',sep='\t',dtype=str,keep_default_na=False)
    rm=pd.read_csv(PREP/'rnai-metadata.tsv.gz',sep='\t',dtype=str,keep_default_na=False)
    cm=pd.read_csv(PREP/'cp-metadata.tsv.gz',sep='\t',dtype=str,keep_default_na=False)
    xx=np.load(PREP/'xpr.npy',mmap_mode='r');cx=np.load(PREP/'cp.npy',mmap_mode='r')
    tasks=[(cell,space,qc,seed) for cell in plan['cells'] for space in plan['spaces'] for qc in plan['quality_views'] for seed in plan['partition_seeds']]
    comparisons=0;cuda_seconds=0.;max_error=0.;fit_seconds=0.;records=[]

    def product(a,b):
        nonlocal comparisons,cuda_seconds,max_error
        aa=torch.as_tensor(a,dtype=torch.float32,device='cuda');bb=torch.as_tensor(b,dtype=torch.float32,device='cuda')
        before,after=torch.cuda.Event(enable_timing=True),torch.cuda.Event(enable_timing=True)
        before.record();sc=aa@bb.T;after.record();torch.cuda.synchronize()
        cuda_seconds+=before.elapsed_time(after)/1000;comparisons+=sc.numel();sc=sc.cpu().numpy()
        for i,j in zip(np.linspace(0,len(a)-1,13,dtype=int),np.linspace(len(b)-1,0,13,dtype=int)):
            max_error=max(max_error,abs(float(a[i]@b[j])-float(sc[i,j])))
        require(np.isfinite(sc).all() and max_error<=plan['numerical_tolerance'],'GPU/CPU numerical failure')
        return sc

    for task in range(shard,len(tasks),8):
        cell,space,qc,seed=tasks[task]
        xf=xm[xm.cell_iname.eq(cell)&xm.pert_type.eq('trt_xpr')&xm.pert_time.eq('96')]
        if qc=='crispr_quality_pass_only':xf=xf[xf.quality_pass.eq('True')]
        rf=rm[rm.cell_id.eq(cell)&rm.pert_type.eq('trt_sh')]
        df=cm[cm.cell_iname.eq(cell)&cm.pert_type.eq('trt_cp')&cm.pert_id.eq('BRD-K13514097')]
        xn,xv=means(xf,xx,'cmap_name');rn,rv=means(rf,np.load(PREP/f'rnai-{space}.npy',mmap_mode='r'),'pert_iname')
        xr,rr,dr=ranks(xv),ranks(rv),ranks(np.asarray(cx[df.index],dtype=np.float64))
        full_control=[]
        if qc=='all_profiles' and seed==plan['partition_seeds'][0]:
            for g in ['BUB1B','MTOR']:
                require(g in xn and g in rn,'Missing original control')
                i,j=xn.index(g),rn.index(g);value=float(xr[i]@rr[j])
                full_control.append(dict(gene=g,correlation=value,
                    rnai_rank=1+int((rr@xr[i]>value+1e-6).sum()),
                    crispr_rank=1+int((xr@rr[j]>value+1e-6).sum())))
        fold_results=[];ordinary_evaluated_x=[];ordinary_evaluated_r=[]
        for fold in range(plan['folds']):
            xt,xe=split_genes(xn,seed,fold,plan['query_genes']);rt,re=split_genes(rn,seed,fold,plan['query_genes'])
            xnames=[xn[i] for i in xe];rnames=[rn[i] for i in re]
            ordinary_evaluated_x.extend(g for g in xnames if g not in plan['query_genes'])
            ordinary_evaluated_r.extend(g for g in rnames if g not in plan['query_genes'])
            train=np.vstack([xr[xt],rr[rt]]);require(len(train)>20,'Insufficient training rows')
            mean=unit(train.mean(0));centered=train-(train@mean)[:,None]*mean[None,:]
            before=time.monotonic();gt=torch.as_tensor(centered,dtype=torch.float64,device='cuda')
            eig,vec=torch.linalg.eigh(gt.T@gt);basis=vec[:,-10:].flip(1).cpu().numpy()
            fit_seconds+=time.monotonic()-before
            orth_error=float(max(np.max(np.abs(basis.T@basis-np.eye(10))),np.max(np.abs(mean@basis))))
            require(orth_error<=1e-8,'Projection not orthonormal')
            # Full fitted bases are retained for deterministic coordinate-space replay.
            prefix=f'{cell}-{space}-{qc}-s{seed}-f{fold}'
            np.savez_compressed(out/(prefix+'-basis.npz'),mean=mean,basis=basis)
            views={}
            for name in plan['representations']:
                if name=='all978':a,b,d=xr[xe],rr[re],dr
                else:
                    k=int(name.removeprefix('residual_pc'));q=np.column_stack([mean,basis[:,:k]])
                    def residual(z):
                        value=unit(z-(z@q)@q.T)
                        require(np.max(np.abs(value@q))<=1e-8,'Projection orthogonality failure')
                        return value
                    a,b,d=map(residual,[xr[xe],rr[re],dr])
                sc=product(a,b);rindex={g:i for i,g in enumerate(rnames)};panel=[];queries=[]
                for i,g in enumerate(xnames):
                    if g not in rindex:continue
                    j=rindex[g];v=float(sc[i,j])
                    row=dict(gene=g,correlation=v,rnai_rank=1+int((sc[i]>v+1e-6).sum()),
                        crispr_rank=1+int((sc[:,j]>v+1e-6).sum()))
                    panel.append(row)
                    if g in plan['query_genes']:
                        count=int(xf.cmap_name.eq(g).sum());passing=int((xf.cmap_name.eq(g)&xf.quality_pass.eq('True')).sum())
                        queries.append(row|dict(crispr_profiles=count,crispr_quality_pass=passing))
                missing=[dict(gene=g,reason='absent_from_'+('crispr' if g not in xnames else 'rnai')) for g in plan['query_genes'] if g not in xnames or g not in rnames]
                pd.DataFrame(panel).to_csv(out/(prefix+'-'+name+'-panel.tsv.gz'),sep='\t',index=False)
                ds=product(a,d);drugs=[]
                for j,(_,meta) in enumerate(df.iterrows()):
                    for g in ['BUB1B','MTOR']:
                        if g not in xnames:continue
                        i=xnames.index(g);v=float(ds[i,j])
                        drugs.append(dict(gene=g,signature_id=meta.sig_id,dose=meta.pert_dose,dose_unit=meta.pert_dose_unit,
                            time_hours=meta.pert_time,drug_qc=meta.quality_pass=='True',
                            query_qc_pass=int((xf.cmap_name.eq(g)&xf.quality_pass.eq('True')).sum()),
                            correlation=v,reversal_rank=1+int((ds[:,j]<v-1e-6).sum()),
                            mimic_rank=1+int((ds[:,j]>v+1e-6).sum()),reference_genes=len(xnames)))
                ordinary=[row for row in panel if row['gene'] not in plan['query_genes']]
                views[name]=dict(queries=queries,missing=missing,drugs=drugs,rnai_reference_genes=len(rnames),
                    crispr_reference_genes=len(xnames),heldout_shared_genes=len(ordinary),
                    heldout_rnai_top1=sum(r['rnai_rank']==1 for r in ordinary),
                    heldout_crispr_top1=sum(r['crispr_rank']==1 for r in ordinary),
                    heldout_rnai_top10=sum(r['rnai_rank']<=10 for r in ordinary),
                    heldout_crispr_top10=sum(r['crispr_rank']<=10 for r in ordinary))
            fold_results.append(dict(fold=fold,training_rows=len(train),train_test_disjoint=True,
                orthogonality_error=orth_error,representations=views))
        require(sorted(ordinary_evaluated_x)==sorted(g for g in xn if g not in plan['query_genes']),'CRISPR fold coverage')
        require(sorted(ordinary_evaluated_r)==sorted(g for g in rn if g not in plan['query_genes']),'RNAi fold coverage')
        record=dict(task=task,cell=cell,space=space,quality=qc,partition_seed=seed,rnai_genes=len(rn),crispr_genes=len(xn),
                    full_unadjusted_control=full_control,folds=fold_results,each_reference_evaluated_once=True)
        save(out/f'task-{task}.json',record);records.append(record)
        print(json.dumps(dict(task=task,cell=cell,space=space,quality=qc,seed=seed,complete=True)),flush=True)
    save(out/'completion.json',dict(shard=shard,complete=True,tasks=[r['task'] for r in records],fits=sum(len(r['folds']) for r in records),
        comparisons=comparisons,cuda_product_seconds=cuda_seconds,covariance_eigen_wall_seconds=fit_seconds,
        max_cpu_error=max_error,elapsed_seconds=time.monotonic()-start,biological_validation=False))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--shard',type=int,required=True)
    a=p.parse_args();worker(a.root,a.shard)
