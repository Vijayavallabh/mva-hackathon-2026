#!/usr/bin/env python3
"""Second-release sensitivity using frozen phase-I genetic queries, on eight H100s."""
import argparse
from datetime import datetime,timezone
import gzip
import json
import os
from pathlib import Path
import time
from track2_transcriptome import digest,write_json,require,ranked,normalize,quality

P='GSE70138_Broad_LINCS_'


def prepare(root):
    import shutil
    import h5py
    import numpy as np
    import pandas as pd
    directory=root/'inputs/phase2'
    out=root/'outputs/phase2-prepared';out.mkdir(exist_ok=False)
    plan=json.loads((root/'inputs/phase2-plan.json').read_text())
    hashes={}
    with gzip.open(directory/'GSE70138_SHA512SUMS.txt.gz','rt') as f:
        for line in f:
            h,name=line.strip().split();hashes[name.lstrip('*')]=h
    records=[]
    for path in sorted(directory.glob('*.gz')):
        if path.name=='GSE70138_SHA512SUMS.txt.gz':continue
        require(path.name in hashes,'Missing upstream checksum: '+path.name)
        require(digest(path,'sha512')==hashes[path.name],'Checksum mismatch: '+path.name)
        records.append(dict(name=path.name,sha512=hashes[path.name],sha256=digest(path),bytes=path.stat().st_size))
    matrix=directory/plan['matrix'];raw=matrix.with_suffix('')
    with gzip.open(matrix,'rb') as a,raw.open('xb') as b:shutil.copyfileobj(a,b,8*1024*1024)
    meta=pd.read_csv(directory/(P+'sig_info_2017-03-06.txt.gz'),sep='\t',dtype=str,keep_default_na=False)
    metrics=pd.read_csv(directory/(P+'sig_metrics_2017-03-06.txt.gz'),sep='\t')
    require(meta.sig_id.is_unique and metrics.sig_id.is_unique,'Duplicate phase-II IDs')
    for key in ['distil_nsample','distil_cc_q75','tas']:
        meta[key]=meta.sig_id.map(metrics.set_index('sig_id')[key])
    require(meta[['distil_nsample','distil_cc_q75','tas']].notna().all().all(),'Missing phase-II QC')
    meta=meta.set_index('sig_id')
    lm=pd.read_csv(root/'outputs/prepared/landmarks.tsv',sep='\t',dtype=str)
    own_genes=pd.read_csv(directory/(P+'gene_info_2017-03-06.txt.gz'),sep='\t',dtype=str)
    require(own_genes.pr_gene_id.is_unique and
            set(own_genes.loc[own_genes.pr_is_lm.eq('1'),'pr_gene_id'])==set(lm.pr_gene_id),
            'The two releases do not have the same measured landmarks')
    with h5py.File(raw,'r') as f:
        dec=lambda a:[x.decode() if isinstance(x,bytes) else str(x) for x in a]
        rows=dec(f['0/META/ROW/id'][:]);cols=dec(f['0/META/COL/id'][:]);d=f['0/DATA/0/matrix']
        require(len(set(rows))==len(rows) and len(set(cols))==len(cols),'Duplicate matrix identifiers')
        require(set(cols)==set(meta.index) and d.shape==(118050,12328),'Phase-II matrix/metadata mismatch')
        positions=[rows.index(x) for x in lm.pr_gene_id]
        x=np.lib.format.open_memmap(out/'landmarks.npy',mode='w+',dtype='float32',shape=(118050,978))
        for i in range(0,len(cols),1024):
            block=d[i:i+1024,:][:,positions]
            require(np.isfinite(block).all(),'Nonfinite phase-II values');x[i:i+len(block)]=block
        x.flush();meta=meta.loc[cols].reset_index()
    require(meta.pert_type.eq('trt_cp').sum()==107404,'Phase-II compound count drift')
    meta.to_csv(out/'signatures.tsv.gz',sep='\t',index=False)
    write_json(out/'manifest.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),plan_sha256=digest(root/'inputs/phase2-plan.json'),source_inputs=records,
        matrix_sha256=digest(out/'landmarks.npy'),metadata_sha256=digest(out/'signatures.tsv.gz'),
        landmark_ids_sha256=digest(root/'outputs/prepared/landmarks.tsv'),script_sha256=digest(__file__)))


def worker(root,shard):
    import numpy as np
    import pandas as pd
    import torch
    require(os.environ.get('CUDA_VISIBLE_DEVICES')==str(shard) and torch.cuda.device_count()==1,'Wrong assigned GPU')
    require('H100' in torch.cuda.get_device_name(0),'Expected H100')
    torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False;torch.set_float32_matmul_precision('highest')
    start=time.monotonic();out=root/f'outputs/phase2-shard-{shard}';out.mkdir(exist_ok=False)
    plan=json.loads((root/'inputs/plan.json').read_text())
    pp=root/'outputs/prepared';sp=root/'outputs/phase2-prepared'
    manifest=json.loads((pp/'manifest.json').read_text())
    meta=pd.read_csv(pp/'signatures.tsv.gz',sep='\t',keep_default_na=False)
    m2=pd.read_csv(sp/'signatures.tsv.gz',sep='\t',keep_default_na=False)
    require(json.loads((sp/'manifest.json').read_text())['plan_sha256']==digest(root/'inputs/phase2-plan.json'),'Secondary plan drift')
    values=np.load(pp/'landmarks.npy',mmap_mode='r');v2=np.load(sp/'landmarks.npy',mmap_mode='r')
    overlap=m2.pert_type.eq('trt_cp')&m2.sig_id.isin(meta.sig_id)
    indices=np.flatnonzero(m2.pert_type.eq('trt_cp')&~overlap)
    chemicals=m2.iloc[indices].reset_index(drop=True)
    ccpu=ranked(v2[indices]).astype(np.float32);cp=torch.tensor(ccpu,device='cuda')
    write_json(out/'registration.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),shard=shard,
        plan_sha256=digest(root/'inputs/phase2-plan.json'),script_sha256=digest(__file__),
        helper_sha256=digest(Path(__file__).with_name('track2_transcriptome.py')),lock_sha256=digest(root/'uv.lock'),
        phase1_manifest_sha256=digest(pp/'manifest.json'),phase2_manifest_sha256=digest(sp/'manifest.json'),
        excluded_overlap_ids=m2.loc[overlap,'sig_id'].tolist(),compound_profiles=len(chemicals),device=torch.cuda.get_device_name(0)))
    def unit(x):
        n=torch.linalg.vector_norm(x,dim=-1,keepdim=True)
        require(bool((n>1e-8).all()),'Degenerate projected signature')
        return x/n
    done=[]
    for qi in range(shard,14,8):
        qid=manifest['query_ids'][qi];row=meta[meta.sig_id.eq(qid)].iloc[0]
        mask=meta.cell_id.eq(row.cell_id)&meta.pert_itime.eq(row.pert_itime)
        q=ranked(values[meta.index[meta.sig_id.eq(qid)].item()][None,:])[0]
        qgpu=torch.tensor(q,dtype=torch.float32,device='cuda')
        non=np.flatnonzero(mask&meta.pert_type.eq('trt_sh')&meta.pert_iname.ne('BUB1B'))
        n=torch.tensor(ranked(values[non]).astype(np.float32),device='cuda')
        _,v=torch.linalg.eigh(n.T@n);spaces=[('raw',None),('shared_pc1_removed',v[:,-1:])]
        gi=np.flatnonzero(mask&meta.pert_type.eq('trt_sh.cgs')&meta.pert_iname.isin(plan['growth_sensitivity_genes']))
        if len(gi)>=3:
            g=torch.tensor(ranked(values[gi]).astype(np.float32),device='cuda')
            _,s,vh=torch.linalg.svd(g,full_matrices=False);spaces.append(('growth_span_removed',vh[s>s.max()*1e-6].T))
        matched=np.flatnonzero(chemicals.cell_id.eq(row.cell_id))
        named=np.flatnonzero(chemicals.cell_id.eq(row.cell_id)&chemicals.pert_iname.isin(plan['named_compounds']))
        summary=dict(query_id=qid,query_index=qi,cell_id=row.cell_id,knockdown_time=row.pert_itime,spaces=[],
                     n_matched_compound_profiles=len(matched),compound_profiles=len(chemicals))
        for name,basis in spaces:
            c=cp if basis is None else unit(cp-(cp@basis)@basis.T)
            query=qgpu if basis is None else unit(qgpu-(qgpu@basis)@basis.T)
            scores=(c@query).cpu().numpy();require(np.isfinite(scores).all(),'Nonfinite secondary scores')
            ids=np.unique(np.r_[np.linspace(0,len(cp)-1,97,dtype=int),named])
            audit=ccpu[ids].astype(float);qc=q.copy()
            if basis is not None:
                b=basis.cpu().numpy().astype(float);audit=normalize(audit-(audit@b)@b.T);qc=normalize(qc-(qc@b)@b.T)
            error=float(np.max(np.abs(audit@qc-scores[ids])));require(error<=2e-5,'Secondary CPU/GPU mismatch')
            np.save(out/f'query-{qi}-{name}-all-compounds.npy',scores)
            rows=[]
            for idx in named:
                r=chemicals.iloc[idx];comp=matched[chemicals.iloc[matched].pert_itime.eq(r.pert_itime).to_numpy()]
                rows.append(dict(signature_id=r.sig_id,compound_id=r.pert_id,compound=r.pert_iname,
                    dose=str(r.pert_idose),time=str(r.pert_itime),correlation=float(scores[idx]),quality_pass=quality(r),
                    negative_tail_fraction=float(np.mean(scores[comp]<=scores[idx])),ranking_denominator=len(comp),
                    metadata_quality={k:float(r[k]) for k in ['distil_nsample','distil_cc_q75','tas']}))
            table=chemicals.iloc[matched][['sig_id','pert_id','pert_iname','cell_id','pert_idose','pert_itime']].copy()
            table['correlation']=scores[matched];table.to_csv(out/f'query-{qi}-{name}-matched.tsv.gz',sep='\t',index=False)
            summary['spaces'].append(dict(name=name,max_cpu_gpu_abs_difference=error,named_compounds=rows))
        write_json(out/f'query-{qi}.json',summary);done.append(qid)
        print(json.dumps(dict(query=qid,shard=shard,done=True)),flush=True)
    torch.cuda.synchronize()
    write_json(out/'summary.json',dict(shard=shard,query_ids=done,complete=True,
        elapsed_seconds=time.monotonic()-start,peak_allocated_gib=torch.cuda.max_memory_allocated()/1024**3))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['prepare','worker','aggregate']);p.add_argument('root',type=Path);p.add_argument('--shard',type=int)
    a=p.parse_args()
    if a.command=='prepare':prepare(a.root)
    elif a.command=='worker':worker(a.root,a.shard)
    else:
        rows=[];runs=[]
        for s in range(8):
            folder=a.root/f'outputs/phase2-shard-{s}'
            run=json.loads((folder/'summary.json').read_text());require(run['complete'],'Incomplete secondary shard');runs.append(run)
            rows.extend(json.loads(p.read_text()) for p in folder.glob('query-*.json'))
        rows.sort(key=lambda r:r['query_index']);require([r['query_index'] for r in rows]==list(range(14)),'Missing secondary query')
        write_json(a.root/'outputs/phase2-results.json',dict(queries=rows,gpu_runs=runs,
            plan_sha256=digest(a.root/'inputs/phase2-plan.json'),clinical_validation=False,drug_ranking_changed=False))
