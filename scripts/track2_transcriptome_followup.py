#!/usr/bin/env python3
"""Post-hoc challenge to the failed raw reproducibility gate; preserve original outputs."""
import argparse
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import time
from track2_transcriptome import digest,write_json,require,ranked,half_splits,gpu_ranked,gpu_median,bh,normalize


def worker(root,shard):
    import numpy as np
    import pandas as pd
    import torch
    require(os.environ.get('CUDA_VISIBLE_DEVICES')==str(shard) and torch.cuda.device_count()==1,'Wrong GPU shard')
    torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    start=time.monotonic();out=root/f'outputs/followup-shard-{shard}';out.mkdir(exist_ok=False)
    plan=json.loads((root/'inputs/followup-plan.json').read_text())
    prep=root/'outputs/prepared';m=pd.read_csv(prep/'signatures.tsv.gz',sep='\t',keep_default_na=False,low_memory=False)
    x=np.load(prep/'landmarks.npy',mmap_mode='r');ids={v:i for i,v in enumerate(m.sig_id)}
    queries=json.loads((prep/'manifest.json').read_text())['query_ids']
    genes=pd.read_csv(prep/'landmarks.tsv',sep='\t');target=genes.index[genes.pr_gene_symbol.eq('BUB1B')].item()
    write_json(out/'registration.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),shard=shard,
        plan_sha256=digest(root/'inputs/followup-plan.json'),script_sha256=digest(__file__),helper_sha256=digest(Path(__file__).with_name('track2_transcriptome.py')),
        primary_results_sha256=digest(root/'outputs/transcriptome-results.json'),lock_sha256=digest(root/'uv.lock'),
        device=torch.cuda.get_device_name(0),precision='float64 GPU resampling; float32 basis as in original run'))
    results=[]
    for qi in range(shard,14,8):
        q=m.iloc[ids[queries[qi]]];context=m.cell_id.eq(q.cell_id)&m.pert_itime.eq(q.pert_itime)
        members=q.distil_id.split('|')
        require(len(members)==len(set(members)) and all(i in ids for i in members),'Missing/duplicate provider member')
        member_rows=m.iloc[[ids[i] for i in members]]
        require(member_rows.pert_type.eq('trt_sh').all() and member_rows.pert_iname.eq('BUB1B').all() and
                member_rows.cell_id.eq(q.cell_id).all() and member_rows.pert_itime.eq(q.pert_itime).all(),'Provider member mismatch')
        non=m[context&m.pert_type.eq('trt_sh')&m.pert_iname.ne('BUB1B')]
        rawbank=np.array([np.median(x[g.index],axis=0) for _,g in non.groupby('pert_id',sort=True)],dtype=np.float64)
        n=torch.tensor(ranked(x[non.index]).astype(np.float32),device='cuda')
        _,v=torch.linalg.eigh(n.T@n);basis=v[:,-1:].double();basis_cpu=basis.cpu().numpy()
        bank=torch.tensor(rawbank,device='cuda')
        all_rows=m[context&m.pert_type.eq('trt_sh')&m.pert_iname.eq('BUB1B')]
        for ai,arm in enumerate(plan['arms']):
            group=all_rows if arm.startswith('all_reagents') else member_rows
            reagents=sorted(group.pert_id.unique().tolist())
            values=np.array([np.median(x[group.index[group.pert_id.eq(r)]],axis=0) for r in reagents],dtype=np.float64)
            splits=half_splits(len(values));project=arm.endswith('shared_pc1_removed')
            def cpu_transform(a):
                a=ranked(a)
                return normalize(a-(a@basis_cpu)@basis_cpu.T) if project else a
            obs=[float(cpu_transform(values[a].mean(0)[None,:])[0]@cpu_transform(values[b].mean(0)[None,:])[0]) for a,b in splits]
            statistic=float(np.median(obs));rng=np.random.default_rng(plan['seed']+qi*10+ai)
            left=torch.tensor([a for a,b in splits],device='cuda');right=torch.tensor([b for a,b in splits],device='cuda')
            def gpu_transform(a):
                a=gpu_ranked(a)
                if project:
                    a=a-(a@basis)@basis.T
                    norm=torch.linalg.vector_norm(a,dim=-1,keepdim=True);require(bool((norm>1e-8).all()),'Degenerate residual')
                    a=a/norm
                return a
            null=[];error=0.
            for k in range(0,plan['resamples'],64):
                count=min(64,plan['resamples']-k)
                draw=np.array([rng.choice(len(rawbank),len(values),replace=False) for _ in range(count)])
                sampled=bank[torch.from_numpy(draw).cuda()]
                a=gpu_transform(sampled[:,left].mean(2));b=gpu_transform(sampled[:,right].mean(2))
                scores=gpu_median((a*b).sum(-1),1).cpu().numpy()
                if k==0:
                    raw=rawbank[draw[:3]]
                    cpu=np.median([np.einsum('ij,ij->i',cpu_transform(raw[:,a].mean(1)),cpu_transform(raw[:,b].mean(1))) for a,b in splits],axis=0)
                    error=float(np.max(np.abs(cpu-scores[:3])));require(error<=2e-5,'Follow-up GPU/CPU mismatch')
                null.extend(scores.tolist())
            np.savez_compressed(out/f'query-{qi}-{arm}-null.npz',null_statistics=null,observed_splits=obs)
            pair=cpu_transform(values)@cpu_transform(values).T
            result=dict(query_index=qi,query_id=q.sig_id,cell_id=q.cell_id,time=q.pert_itime,arm=arm,n_reagents=len(values),
                reagent_ids=reagents,provider_member_ids=members,provider_member_count=len(members),
                median_target_z=float(np.median(values[:,target])),pairwise_median=float(np.median(pair[np.triu_indices(len(values),1)])),
                split_median=statistic,split_null_tail=(1+sum(v>=statistic for v in null))/(1+len(null)),
                null_draws=len(null),null_cpu_gpu_max_difference=error)
            write_json(out/f'query-{qi}-{arm}.json',result);results.append(result)
        print(json.dumps(dict(query=q.sig_id,post_hoc=True,done=True)),flush=True)
    torch.cuda.synchronize()
    write_json(out/'summary.json',dict(shard=shard,complete=True,arms=len(results),query_ids=queries[shard::8],
        elapsed_seconds=time.monotonic()-start,peak_allocated_gib=torch.cuda.max_memory_allocated()/1024**3))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['worker','aggregate']);p.add_argument('root',type=Path);p.add_argument('--shard',type=int);a=p.parse_args()
    if a.command=='worker':worker(a.root,a.shard)
    else:
        rows=[];runs=[]
        for s in range(8):
            folder=a.root/f'outputs/followup-shard-{s}'
            run=json.loads((folder/'summary.json').read_text());require(run['complete'],'Incomplete follow-up shard');runs.append(run)
            rows.extend(json.loads(p.read_text()) for p in folder.glob('query-*.json'))
        rows.sort(key=lambda r:(r['query_index'],r['arm']));require(len(rows)==42,'Incomplete follow-up')
        for r,q in zip(rows,bh([r['split_null_tail'] for r in rows])):
            r['split_null_BH_q']=q
            r['same_operational_filter']=bool(r['n_reagents']>=6 and r['median_target_z']<0 and r['pairwise_median']>0 and r['split_median']>0 and q<=.05)
        write_json(a.root/'outputs/followup-results.json',dict(post_hoc=True,primary_gate_replaced=False,drug_ranking_changed=False,
            plan_sha256=digest(a.root/'inputs/followup-plan.json'),rows=rows,gpu_runs=runs))
