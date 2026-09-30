#!/usr/bin/env python3
"""Public LINCS cross-modal specificity stress test, with target-excluded projection."""
import argparse
import json
import os
from pathlib import Path
import time
from track2_saturation_v27 import digest, require, save

PREP = Path('/home/prachh/v/mva-track2-crispr-20261001-v25/outputs/prepared')


def unit(x):
    import numpy as np
    n=np.linalg.norm(x,axis=-1,keepdims=True)
    require(np.isfinite(x).all() and (n>1e-12).all(), 'Degenerate residual')
    return x/n


def ranks(x):
    from scipy.stats import rankdata
    z=rankdata(x,axis=-1,method='average')
    return unit(z-z.mean(axis=-1,keepdims=True))


def means(frame,matrix,column):
    import numpy as np
    names=sorted(frame[column].unique())
    return names,np.asarray([np.asarray(matrix[frame.index[frame[column].eq(g)]],dtype=np.float64).mean(0)
                             for g in names])


def worker(root, shard, gpu):
    import numpy as np
    import pandas as pd
    import torch
    from scipy.stats import spearmanr
    start=time.monotonic()
    require(os.environ.get('CUDA_VISIBLE_DEVICES')==str(gpu) and torch.cuda.device_count()==1,
            'GPU assignment mismatch')
    torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False
    torch.set_float32_matmul_precision('highest')
    planpath=root/'inputs/specificity-plan.json'
    plan=json.loads(planpath.read_text())
    out=root/f'outputs/specificity-{shard}';out.mkdir(exist_ok=False)
    save(out/'registration.json',dict(plan_sha256=digest(planpath),script_sha256=digest(__file__),
        device=torch.cuda.get_device_name(),gpu=gpu,shard=shard,torch=torch.__version__,
        source_manifest_sha256=digest(PREP/'manifest.json')))
    lm=pd.read_csv(PREP/'landmarks.tsv',sep='\t',dtype=str)
    symbol='gene_symbol' if 'gene_symbol' in lm else 'pr_gene_symbol'
    keep=~lm[symbol].isin(plan['cycle_stress_features']).to_numpy()
    save(out/'feature-removal.json',dict(removed=lm.loc[~keep,symbol].tolist(),
         absent=sorted(set(plan['cycle_stress_features'])-set(lm[symbol])),kept=int(keep.sum())))
    xm=pd.read_csv(PREP/'xpr-metadata.tsv.gz',sep='\t',dtype=str,keep_default_na=False)
    rm=pd.read_csv(PREP/'rnai-metadata.tsv.gz',sep='\t',dtype=str,keep_default_na=False)
    cm=pd.read_csv(PREP/'cp-metadata.tsv.gz',sep='\t',dtype=str,keep_default_na=False)
    xx=np.load(PREP/'xpr.npy',mmap_mode='r');cx=np.load(PREP/'cp.npy',mmap_mode='r')
    tasks=[(cell,space) for cell in plan['cells'] for space in plan['spaces']]
    counts=0;cuda_seconds=0.;max_error=0.;summaries=[]

    def product(a,b):
        nonlocal counts,cuda_seconds,max_error
        aa=torch.as_tensor(a,dtype=torch.float32,device='cuda')
        bb=torch.as_tensor(b,dtype=torch.float32,device='cuda')
        before,after=torch.cuda.Event(enable_timing=True),torch.cuda.Event(enable_timing=True)
        before.record();c=aa@bb.T;after.record();torch.cuda.synchronize()
        cuda_seconds+=before.elapsed_time(after)/1000;counts+=c.numel()
        c=c.cpu().numpy()
        for i,j in zip(np.linspace(0,len(a)-1,13,dtype=int),np.linspace(len(b)-1,0,13,dtype=int)):
            max_error=max(max_error,abs(float(a[i]@b[j])-float(c[i,j])))
        require(np.isfinite(c).all() and max_error<=plan['numerical_tolerance'],'CUDA/CPU mismatch')
        return c

    for task in range(shard,len(tasks),8):
        cell,space=tasks[task]
        xf=xm[xm.cell_iname.eq(cell)&xm.pert_type.eq('trt_xpr')&xm.pert_time.eq('96')]
        rf=rm[rm.cell_id.eq(cell)&rm.pert_type.eq('trt_sh')]
        df=cm[cm.cell_iname.eq(cell)&cm.pert_type.eq('trt_cp')&cm.pert_id.eq('BRD-K13514097')]
        xn,xv=means(xf,xx,'cmap_name')
        rn,rv=means(rf,np.load(PREP/f'rnai-{space}.npy',mmap_mode='r'),'pert_iname')
        dv=np.asarray(cx[df.index],dtype=np.float64)
        xr,rr,dr=ranks(xv),ranks(rv),ranks(dv)
        train=np.vstack([xr[[g not in plan['excluded_training_targets'] for g in xn]],
                         rr[[g not in plan['excluded_training_targets'] for g in rn]]])
        mean=unit(train.mean(0))
        centered=train-(train@mean)[:,None]*mean[None,:]
        # GPU FP64 covariance eigendecomposition equals right singular directions.
        gt=torch.as_tensor(centered,dtype=torch.float64,device='cuda')
        eigenvalues,eigenvectors=torch.linalg.eigh(gt.T@gt)
        basis=eigenvectors[:,-10:].flip(1).cpu().numpy()
        orth_error=float(np.max(np.abs(basis.T@basis-np.eye(10))))
        require(orth_error<=1e-8 and np.max(np.abs(mean@basis))<=1e-8,'Invalid projection basis')
        np.savez(out/f'{cell}-{space}-basis.npz',mean=mean,basis=basis,
                 eigenvalues=eigenvalues.cpu().numpy())
        projections={}
        for name in plan['representations']:
            if name=='all978': a,b,d=xr,rr,dr
            elif name=='without_selected_cycle_stress_features':
                a,b,d=ranks(xv[:,keep]),ranks(rv[:,keep]),ranks(dv[:,keep])
            else:
                k=int(name.removeprefix('residual_pc'));q=np.column_stack([mean,basis[:,:k]])
                def residual(z):
                    v=unit(z-(z@q)@q.T)
                    require(np.max(np.abs(v@q))<1e-8,'Residual not orthogonal')
                    return v
                a,b,d=map(residual,[xr,rr,dr])
            sc=product(a,b)
            panel=[];queries=[]
            ri={g:i for i,g in enumerate(rn)}
            for i,g in enumerate(xn):
                if g not in ri: continue
                j=ri[g];v=float(sc[i,j])
                row=dict(gene=g,correlation=v,rnai_rank=1+int((sc[i]>v+1e-6).sum()),
                         crispr_rank=1+int((sc[:,j]>v+1e-6).sum()))
                panel.append(row)
                if g in plan['query_genes']:
                    cpu=float(a[i]@b[j]);error=abs(cpu-v)
                    require(error<=plan['numerical_tolerance'],'Query CPU mismatch')
                    row=dict(row,cpu=cpu,cpu_error=error,
                        rnai_top20=[dict(gene=rn[t],correlation=float(sc[i,t])) for t in np.argsort(-sc[i],kind='stable')[:20]],
                        crispr_top20=[dict(gene=xn[t],correlation=float(sc[t,j])) for t in np.argsort(-sc[:,j],kind='stable')[:20]],
                        crispr_profiles=int(xf.cmap_name.eq(g).sum()),
                        crispr_qc_pass=int((xf.cmap_name.eq(g)&xf.quality_pass.eq('True')).sum()))
                    queries.append(row)
            pd.DataFrame(panel).to_csv(out/f'{cell}-{space}-{name}-panel.tsv.gz',sep='\t',index=False)
            ds=product(a,d);drugs=[]
            for j,(_,meta) in enumerate(df.iterrows()):
                for g in plan['query_genes']:
                    i=xn.index(g);v=float(ds[i,j])
                    drugs.append(dict(gene=g,signature_id=meta.sig_id,dose=meta.pert_dose,
                        dose_unit=meta.pert_dose_unit,time_hours=meta.pert_time,drug_qc=meta.quality_pass=='True',
                        query_qc_pass=int((xf.cmap_name.eq(g)&xf.quality_pass.eq('True')).sum()),
                        correlation=v,reversal_rank=1+int((ds[:,j]<v-1e-6).sum()),
                        mimic_rank=1+int((ds[:,j]>v+1e-6).sum()),reference_genes=len(xn)))
            projections[name]=dict(queries=queries,drug_rows=drugs,shared_gene_records=len(panel),
                rnai_top1=sum(r['rnai_rank']==1 for r in panel),crispr_top1=sum(r['crispr_rank']==1 for r in panel))
        record=dict(cell=cell,space=space,rnai_genes=len(rn),crispr_genes=len(xn),
            training_rows=len(train),orthogonality_error=orth_error,representations=projections)
        save(out/f'{cell}-{space}.json',record);summaries.append(record)
        print(json.dumps(dict(cell=cell,space=space,done=True)),flush=True)
    save(out/'summary.json',dict(tasks=len(summaries),comparisons=counts,cuda_product_seconds=cuda_seconds,
        max_cpu_error=max_error,elapsed_seconds=time.monotonic()-start,drug_ranking_changed=False,
        biological_validation=False,wet_lab_performed=False))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    p.add_argument('--shard',type=int,required=True);p.add_argument('--gpu',type=int,required=True)
    a=p.parse_args();worker(a.root,a.shard,a.gpu)
