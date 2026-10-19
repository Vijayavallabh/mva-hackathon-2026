#!/usr/bin/env python3
"""Separate query/reference acquisition plates; never claim unseen-plate training."""
import argparse
import json
from pathlib import Path
import time

import numpy as np
import torch
from torch.nn import functional as F

from track2_optical_fetch_v33 import hashes, write_json
from track2_optical_model_v35 import BASIC, eligible_groups
from track2_optical_prepare_v35 import QUERIES


@torch.no_grad()
def separate_retrieval(qvectors,rvectors,qgroups,rgroups,distance='cosine'):
    names=sorted(set(qgroups)&set(rgroups))
    if len(names)<2:
        return dict(status='insufficient_reference_genes',genes=len(names),rows=[],macro_mrr=None)
    qix=[];truth=[];own=[];refs=[]
    for i,g in enumerate(names):
        refs.append(rvectors[rgroups[g]].mean(0))
        for guide in qgroups[g]:
            other=[k for k in rgroups[g] if k!=guide]
            if not other:
                continue
            qix.append(guide);truth.append(i);own.append(rvectors[other].mean(0))
    q=qvectors[qix];r=torch.stack(refs);own=torch.stack(own)
    if distance=='cosine':
        scores=F.normalize(q,dim=1)@F.normalize(r,dim=1).T
        own_scores=(F.normalize(q,dim=1)*F.normalize(own,dim=1)).sum(1)
    elif distance=='absolute':
        scores=-(q[:,None,:]-r[None,:,:]).abs().mean(2)
        own_scores=-(q-own).abs().mean(1)
    else:
        raise ValueError('Unknown distance')
    scores[torch.arange(len(q),device=q.device),torch.tensor(truth,device=q.device)]=own_scores
    if not torch.isfinite(scores).all():
        raise ValueError('Nonfinite separate-plate scores')
    ranks=(1+(scores>own_scores[:,None]).sum(1)+((scores==own_scores[:,None]).sum(1)-1)*.5).cpu().numpy()
    own_scores=own_scores.cpu().numpy();best=scores.argmax(1).cpu().numpy()
    rows=[dict(gene=names[t],guide_index=g,rank=float(rank),own_score=float(s),
               best_gene=names[int(b)],reference_genes=len(names))
          for t,g,rank,s,b in zip(truth,qix,ranks,own_scores,best)]
    by_gene={}
    for r in rows:
        by_gene.setdefault(r['gene'],[]).append(1/r['rank'])
    mrr={g:float(np.mean(v)) for g,v in by_gene.items()}
    return dict(status='evaluated',genes=len(mrr),guide_queries=len(rows),rows=rows,
                by_gene_mrr=mrr,macro_mrr=float(np.mean(list(mrr.values()))))


def transform(values,keep,center,scale):
    x=np.asarray(values[:,keep],dtype=np.float32).copy()
    x=(x-center)/scale;x[~np.isfinite(x)]=0
    return np.clip(x,-10,10).astype(np.float32)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    p.add_argument('--arm',choices=['mitotic','interphase'],required=True)
    p.add_argument('--seed',type=int,choices=[3301,3302,3303,3304],required=True)
    p.add_argument('--shuffled',action='store_true');a=p.parse_args();root=a.root.resolve()
    if not torch.cuda.is_available() or torch.cuda.device_count()!=1:
        raise ValueError('Expose one idle GPU')
    torch.backends.cuda.matmul.allow_tf32=False;torch.use_deterministic_algorithms(True)
    label=f"{a.arm}-{a.seed}-{'shuffled' if a.shuffled else 'real'}"
    model=root/'models-v35'/label;source=root/'prepared-v35'/a.arm
    prepared=json.loads((source/'complete.json').read_text())
    for name in ['guides.json','features.json','full_profiles.npz','guide_plates.json','plate_profiles.npz']:
        if hashes(source/name)[1]!=prepared['outputs'][name]:
            raise ValueError('Changed prepared artifact')
    complete=json.loads((model/'complete.json').read_text())
    if complete['smoke']:
        raise ValueError('Smoke model excluded')
    for name in ['learned_plate_profiles.npy','learned_plate_rows.json','preprocessing.npz','results.json']:
        if hashes(model/name)[1]!=complete['files'][name]:
            raise ValueError('Changed model artifact')
    out=root/'plate-v35'/label;out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    rows=json.loads((source/'guides.json').read_text());lookup={r['guide']:i for i,r in enumerate(rows)}
    features=json.loads((source/'features.json').read_text())
    with np.load(model/'preprocessing.npz') as pre:
        keep,center,scale=pre['keep'],pre['center'],pre['scale']
    names=[n for n,k in zip(features,keep) if k]
    basic=[i for i,n in enumerate(names) if n in BASIC]
    size=[i for i,n in enumerate(names) if n in ['nucleus_area','cell_area']]
    with np.load(source/'full_profiles.npz') as data:
        sums,finite=data['sums'],data['finite_counts']
    counts=np.asarray([r['cells'] for r in rows])
    plate_rows=json.loads((source/'guide_plates.json').read_text())
    with np.load(source/'plate_profiles.npz') as data:
        ps,pf=data['sums'],data['finite_counts']
    lr=json.loads((model/'learned_plate_rows.json').read_text())
    lv=np.load(model/'learned_plate_profiles.npy',allow_pickle=False)
    ls=np.zeros((len(rows),lv.shape[1]),dtype=np.float64);lc=np.zeros(len(rows),dtype=np.int64)
    for r,v in zip(lr,lv):
        g=r['guide_index'];ls[g]+=v.astype(np.float64)*r['sampled_cells'];lc[g]+=r['sampled_cells']
    pooled=np.divide(ls,lc[:,None],out=np.zeros_like(ls),where=lc[:,None]>0)
    model_pooled=np.load(model/'learned_profiles.npy',allow_pickle=False)
    error=float(np.max(np.abs(pooled-model_pooled)))
    if error>2e-5:
        raise ValueError('Sample-weighted plate profiles disagree with pooled inference')
    results=[]
    for plate in sorted({r['plate'] for r in plate_rows}):
        qsum=np.zeros_like(sums);qfinite=np.zeros_like(finite);qc=np.zeros_like(counts)
        for i,r in enumerate(plate_rows):
            if r['plate']==plate:
                g=lookup[r['guide']];qsum[g]=ps[i];qfinite[g]=pf[i];qc[g]=r['cells']
        qlearned=np.zeros_like(ls);qsample=np.zeros_like(lc)
        for r,v in zip(lr,lv):
            if r['plate']==plate:
                qlearned[r['guide_index']]=v;qsample[r['guide_index']]=r['sampled_cells']
        outside=counts-qc;rsample=lc-qsample
        qrows=[dict(r,cells=int(qc[i]) if qsample[i]>0 else 0) for i,r in enumerate(rows)]
        rrows=[dict(r,cells=int(outside[i]) if rsample[i]>0 else 0) for i,r in enumerate(rows)]
        qgroups=eligible_groups(qrows,'test');rgroups=eligible_groups(rrows,'test')
        qm=np.divide(qsum,qfinite,out=np.full(qsum.shape,np.nan),where=qfinite>0)
        rm=np.divide(sums-qsum,finite-qfinite,out=np.full(qsum.shape,np.nan),where=(finite-qfinite)>0)
        qp=torch.tensor(transform(qm,keep,center,scale),device='cuda')
        rp=torch.tensor(transform(rm,keep,center,scale),device='cuda')
        rlearned=np.divide(ls-qlearned*qsample[:,None],rsample[:,None],out=np.zeros_like(ls),where=rsample[:,None]>0)
        matrices={'full_profile':(qp,rp),'full_correlation':(qp-qp.mean(1,keepdim=True),rp-rp.mean(1,keepdim=True)),
            'basic_morphology':(qp[:,basic],rp[:,basic]),'size_only':(qp[:,size],rp[:,size]),
            'learned':(torch.tensor(qlearned,dtype=torch.float32,device='cuda'),torch.tensor(rlearned,dtype=torch.float32,device='cuda')),
            'guide_abundance':(torch.tensor(np.log1p(qc)[:,None],dtype=torch.float32,device='cuda'),
                               torch.tensor(np.log1p(outside)[:,None],dtype=torch.float32,device='cuda'))}
        methods={n:separate_retrieval(q,r,qgroups,rgroups,'absolute' if n=='guide_abundance' else 'cosine') for n,(q,r) in matrices.items()}
        query_counts={g:[dict(guide_index=i,plate_cells=int(qc[i]),other_plate_cells=int(outside[i]),
                            sampled_plate_cells=int(qsample[i]),sampled_other_plate_cells=int(rsample[i]))
                        for i,r in enumerate(rows) if r['gene']==g] for g in QUERIES}
        results.append(dict(plate=plate,methods=methods,queries=query_counts))
    result=dict(arm=a.arm,seed=a.seed,shuffled=a.shuffled,plate_results=results,
        model_complete_sha256=hashes(model/'complete.json')[1],prepared_complete_sha256=hashes(source/'complete.json')[1],
        script_sha256=hashes(Path(__file__))[1],elapsed_seconds=time.monotonic()-start,
        pooled_plate_mean_max_absolute_error=error,pooled_plate_mean_tolerance=2e-5,
        original_v33_fits_excluded=True,unseen_acquisition_training=False,
        biological_validation=False,drug_ranking_changed=False,
        interpretation='Query and references use separate plates and distinct own-gene guides; encoder training used other genes from all plates. Repeated wells/seeds are not biological replicates.')
    write_json(out/'results.json',result)
    write_json(out/'complete.json',dict(files={'results.json':hashes(out/'results.json')[1]},smoke=False))
    print(json.dumps(dict(label=label,plates=len(results),elapsed_seconds=result['elapsed_seconds'])),flush=True)


if __name__=='__main__':
    main()
