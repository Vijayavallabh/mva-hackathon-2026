#!/usr/bin/env python3
"""Complete-guide GPU medians, with CPU controls and cross-file conservation."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import warnings

import numpy as np
import pyarrow.parquet as pq

from track2_optical_fetch_v33 import hashes,selected_files,write_json,MIN_FREE_BYTES
from track2_optical_prepare_v35 import phenotype_columns,QUERIES

PLAN_SHA='533e75e8e8f3e122d102e8ef9b3628ecbb169d777a8f083e129196a1305f83b9'


def assignments(files,workers=8):
    parent=list(range(len(files)))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    owner={}
    for i,f in enumerate(files):
        for g in f['guides']:
            if g in owner:parent[find(i)]=find(owner[g])
            else:owner[g]=i
    components={}
    for i in range(len(files)):components.setdefault(find(i),[]).append(i)
    parts=sorted(components.values(),key=lambda ix:(-sum(files[i]['bytes'] for i in ix),min(ix)))
    jobs=[[] for _ in range(workers)];load=[0]*workers
    for ix in parts:
        worker=min(range(workers),key=lambda j:(load[j],j))
        jobs[worker].extend(ix);load[worker]+=sum(files[i]['bytes'] for i in ix)
    return [sorted(ix) for ix in jobs]


def gpu_median(values,device):
    import torch
    x=torch.as_tensor(values,dtype=torch.float32,device=device)
    finite=torch.isfinite(x);count=finite.sum(0)
    ordered=torch.sort(torch.where(finite,x,float('inf')),dim=0,stable=True).values
    low=((count-1)//2).clamp_min(0)[None,:];high=(count//2)[None,:]
    median=(ordered.gather(0,low)+ordered.gather(0,high))[0]*.5
    median=torch.where(count>0,median,float('nan'))
    return median.cpu().numpy(),count.cpu().numpy()


def index_one(job):
    root,arm,row=job
    table=pq.read_table(root/'inputs'/arm/row['label'],columns=['sgRNA_0','gene_symbol_0','group_0'],use_threads=False)
    frame=table.to_pandas(ignore_metadata=True);guides={}
    for guide,ix in frame.groupby('sgRNA_0',sort=True,dropna=False).indices.items():
        genes=frame.iloc[ix]['gene_symbol_0'].fillna('').unique().tolist()
        groups=frame.iloc[ix]['group_0'].fillna('').unique().tolist()
        if not isinstance(guide,str) or len(genes)!=1 or len(groups)!=1:
            raise ValueError('Invalid source guide attribution')
        guides[guide]=dict(gene=genes[0],group=groups[0],cells=len(ix))
    return dict(label=row['label'],source_id=row['dataFile']['id'],bytes=row['dataFile']['filesize'],
                md5=row['dataFile']['checksum']['value'],guides=guides,cells=len(frame))


def worker(root,arm,number):
    import torch
    if not torch.cuda.is_available() or torch.cuda.device_count()!=1:raise ValueError('One idle GPU required')
    torch.use_deterministic_algorithms(True);torch.backends.cuda.matmul.allow_tf32=False
    base=root/'median-v35'/arm;reg=json.loads((base/'registration.json').read_text())
    if reg['worker_script_sha256']!=hashes(Path(__file__))[1]:raise ValueError('Registered median script changed')
    files=json.loads((base/'source-index.json').read_text());features=json.loads((base/'features.json').read_text())
    selected=[files[i] for i in reg['assignments'][number]]
    out=base/'workers'/str(number);out.mkdir(parents=True,exist_ok=False)
    remaining=Counter(g for f in selected for g in f['guides'])
    attribution={};buffer={};profiles={};counts={};records={};audit=[];sources=[];start=time.monotonic()
    for f in selected:
        source=root/'inputs'/arm/f['label'];md5,sha=hashes(source)
        if source.stat().st_size!=f['bytes'] or md5!=f['md5']:raise ValueError('Source digest mismatch')
        sources.append(dict(file=f['label'],sha256=sha,md5=md5))
        table=pq.read_table(source,columns=['sgRNA_0']+features,use_threads=False)
        labels=table.select(['sgRNA_0']).to_pandas(ignore_metadata=True)
        x=np.column_stack([table.column(n).to_numpy(zero_copy_only=False) for n in features]).astype(np.float32)
        x[~np.isfinite(x)]=np.nan;np.clip(x,-10,10,out=x)
        group=labels.groupby('sgRNA_0',sort=True).indices
        if set(group)!=set(f['guides']):raise ValueError('Source/index guide mismatch')
        for g,ix in group.items():
            info=f['guides'][g]
            if len(ix)!=info['cells']:raise ValueError('Source/index count mismatch')
            pair=(info['gene'],info['group'])
            if g in attribution and attribution[g]!=pair:raise ValueError('Cross-file attribution mismatch')
            attribution[g]=pair;buffer.setdefault(g,[]).append(x[ix].copy());remaining[g]-=1
            if remaining[g]:continue
            values=np.concatenate(buffer.pop(g));median,finite=gpu_median(values,'cuda')
            if info['gene'] in QUERIES:
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore',RuntimeWarning)
                    cpu=np.nanmedian(values.astype(np.float64),axis=0)
                if not np.array_equal(np.isnan(cpu),np.isnan(median)):raise ValueError('Median missingness differs')
                error=float(np.max(np.abs(cpu[np.isfinite(cpu)]-median[np.isfinite(cpu)])))
                if error>2e-5:raise ValueError('CPU/GPU median mismatch')
                audit.append(dict(guide=g,gene=info['gene'],cells=len(values),maximum_absolute_error=error))
            profiles[g]=median;counts[g]=finite
            records[g]=dict(guide=g,gene=info['gene'],group=info['group'],cells=len(values))
    if buffer or any(remaining.values()):raise ValueError('Incomplete guide aggregation')
    names=sorted(profiles)
    np.savez(out/'profiles.npz',medians=np.asarray([profiles[g] for g in names],dtype=np.float32).reshape(len(names),len(features)),
             finite_counts=np.asarray([counts[g] for g in names],dtype=np.int64).reshape(len(names),len(features)))
    write_json(out/'guides.json',[records[g] for g in names]);write_json(out/'cpu_audit.json',audit)
    write_json(out/'sources.json',sources)
    receipt=dict(worker=number,source_files=len(selected),guides=len(names),cells=sum(r['cells'] for r in records.values()),
        elapsed_seconds=time.monotonic()-start,peak_gpu_bytes=torch.cuda.max_memory_allocated(),
        script_sha256=hashes(Path(__file__))[1],plan_sha256=PLAN_SHA,
        outputs={p.name:hashes(p)[1] for p in out.iterdir() if p.is_file()})
    write_json(out/'complete.json',receipt);print(json.dumps(receipt),flush=True)


def merge(root,arm):
    base=root/'median-v35'/arm;features=json.loads((base/'features.json').read_text());rows=[];med=[];finite=[];audit=[]
    receipts=[]
    for i in range(8):
        folder=base/'workers'/str(i);r=json.loads((folder/'complete.json').read_text())
        for name,digest in r['outputs'].items():
            if hashes(folder/name)[1]!=digest:raise ValueError('Worker artifact changed')
        receipts.append(r);rows.extend(json.loads((folder/'guides.json').read_text()))
        audit.extend(json.loads((folder/'cpu_audit.json').read_text()))
        with np.load(folder/'profiles.npz') as v:med.append(v['medians']);finite.append(v['finite_counts'])
    order=np.argsort([r['guide'] for r in rows],kind='stable');rows=[rows[i] for i in order]
    if len({r['guide'] for r in rows})!=len(rows):raise ValueError('Cross-worker guide duplication')
    indexed={}
    for f in json.loads((base/'source-index.json').read_text()):
        for g,r in f['guides'].items():
            if g not in indexed:indexed[g]=dict(guide=g,**r)
            else:
                if (indexed[g]['gene'],indexed[g]['group'])!=(r['gene'],r['group']):raise ValueError('Attribution mismatch')
                indexed[g]['cells']+=r['cells']
    if rows!=[indexed[g] for g in sorted(indexed)]:raise ValueError('Source/worker guide conservation failed')
    if {r['guide'] for r in audit}!={r['guide'] for r in rows if r['gene'] in QUERIES}:
        raise ValueError('Query numerical audit omitted')
    np.savez(base/'profiles.npz',medians=np.concatenate(med)[order],finite_counts=np.concatenate(finite)[order])
    write_json(base/'guides.json',rows);write_json(base/'cpu_audit.json',audit)
    write_json(base/'complete.json',dict(arm=arm,guides=len(rows),cells=sum(r['cells'] for r in rows),features=len(features),
        workers=receipts,plan_sha256=PLAN_SHA,biological_validation=False,
        outputs={n:hashes(base/n)[1] for n in ['profiles.npz','guides.json','cpu_audit.json','features.json','source-index.json','registration.json']}))


def run(root,arm):
    if not root.is_relative_to('/home/prachh/v'):raise ValueError('All campaign work must stay under v')
    if not (root/'outputs'/f'download-{arm}-complete.json').is_file():raise ValueError('Partial source coverage prohibited')
    if hashes(root/'inputs/median-plan-v35.json')[1]!=PLAN_SHA:raise ValueError('Median plan changed')
    command=['nvidia-smi','--query-gpu=index,uuid,memory.used,utilization.gpu','--format=csv,noheader,nounits']
    devices=[r.split(',') for r in subprocess.check_output(command,text=True).strip().splitlines()]
    if len(devices)!=8 or any(int(d[2])>100 or int(d[3])!=0 for d in devices):raise ValueError('Eight idle GPUs required')
    base=root/'median-v35'/arm;base.mkdir(parents=True,exist_ok=False)
    source=[r for r in selected_files(root/'inputs/dataverse-metadata.json',arm) if r['label'].startswith('part.')]
    with ThreadPoolExecutor(max_workers=8) as pool:files=list(pool.map(index_one,[(root,arm,r) for r in source]))
    features=phenotype_columns(pq.read_schema(root/'inputs'/arm/'_common_metadata'))
    if len(features)!=1064:raise ValueError('Corrected feature count changed')
    write_json(base/'source-index.json',files);write_json(base/'features.json',features)
    output_bound=len({g for f in files for g in f['guides']})*len(features)*12*2+1024**3
    used=sum(p.stat().st_size for p in root.rglob('*') if p.is_file() and not p.is_symlink())
    if used+output_bound>450000000000 or shutil.disk_usage(root).free<MIN_FREE_BYTES+output_bound:
        raise RuntimeError('Registered storage budget would be exceeded; index preserved')
    current=[r.split(',') for r in subprocess.check_output(command,text=True).strip().splitlines()]
    if len(current)!=8 or any(int(d[2])>100 or int(d[3])!=0 for d in current):
        raise RuntimeError('GPUs became occupied during indexing; no workers launched')
    reg=dict(started_utc=datetime.now(timezone.utc).isoformat(),assignments=assignments(files),
        worker_script_sha256=hashes(Path(__file__))[1],plan_sha256=PLAN_SHA)
    write_json(base/'registration.json',reg)
    processes=[];handles=[]
    for i in range(8):
        env=dict(os.environ,CUDA_VISIBLE_DEVICES=str(i),OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4',
                 CUBLAS_WORKSPACE_CONFIG=':4096:8',TMPDIR=str(root/'cache/tmp'))
        log=(root/'logs'/f'median-v35-{arm}-{i}.log').open('x');handles.append(log)
        cmd=[sys.executable,str(Path(__file__).resolve()),str(root),'worker','--arm',arm,'--worker',str(i)]
        proc=subprocess.Popen(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL)
        processes.append((proc,dict(gpu=i,uuid=devices[i][1].strip(),pid=proc.pid,command=cmd)))
    with (base/'gpu-monitor.jsonl').open('x') as monitor:
        while True:
            state=dict(utc=datetime.now(timezone.utc).isoformat(),workers=[dict(r,returncode=p.poll()) for p,r in processes])
            write_json(base/'status.json',state)
            monitor.write(json.dumps(dict(utc=state['utc'],gpu=subprocess.check_output(command,text=True).strip().splitlines()))+'\n');monitor.flush()
            if all(p.poll() is not None for p,_ in processes):break
            time.sleep(5)
    for h in handles:h.close()
    state['successful']=all(p.returncode==0 for p,_ in processes);write_json(base/'finished.json',state)
    if not state['successful']:raise RuntimeError('Median worker failed; outputs preserved')
    merge(root,arm)
    print(json.dumps(dict(arm=arm,successful=True)),flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    p.add_argument('action',choices=['run','worker']);p.add_argument('--arm',choices=['mitotic','interphase'],required=True)
    p.add_argument('--worker',type=int,choices=range(8));a=p.parse_args();root=a.root.resolve()
    if a.action=='worker':
        if a.worker is None:raise ValueError('Worker index required')
        worker(root,a.arm,a.worker)
    else:run(root,a.arm)


if __name__=='__main__':main()
