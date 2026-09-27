#!/usr/bin/env python3
"""Independent CPU spotchecks of original public GCTX coordinates and GPU results."""
import argparse
import csv
import gzip
import itertools
import json
from pathlib import Path
import tarfile
from track2_rnai_v23 import digest, save, require


def audit(root):
    import h5py
    import numpy as np
    import pandas as pd
    from scipy.stats import spearmanr
    result=json.loads((root/'outputs/results.json').read_text())
    meta=pd.read_csv(root/'outputs/prepared/signatures.tsv.gz',sep='\t',keep_default_na=False)
    genes=pd.read_csv(root/'outputs/prepared/genes.tsv',sep='\t',dtype=str)
    plan=json.loads((root/'inputs/plan.json').read_text())
    records=[];null_total=0;max_error=0.
    for space, packed in plan['matrices'].items():
        with h5py.File(root/'inputs'/packed.removesuffix('.gz'),'r') as f:
            matrix=f['0/DATA/0/matrix']
            for ci,cell in enumerate(plan['cells']):
                d=next(x for x in result['rows'] if x['cell']==cell and x['space']==space)
                out=root/f'outputs/worker-{ci%8}';stamp=f'{cell}-{space}'
                ids=meta.index[meta.cell_id.eq(cell)&meta.pert_type.eq('trt_sh')].to_numpy()
                local=meta.iloc[ids].reset_index(drop=True);b=np.flatnonzero(local.pert_iname.eq('BUB1B'))
                pair=np.load(out/f'{stamp}-all-pairs.npy',mmap_mode='r')
                require(pair.shape==(len(ids),len(ids)) and digest(out/f'{stamp}-all-pairs.npy')==d['pair_matrix_sha256'],'Matrix digest/shape mismatch')
                for start in range(0,len(pair),1024):require(np.isfinite(pair[start:start+1024]).all(),'Nonfinite retained matrix')
                direct=np.asarray(matrix[ids[b]],dtype=float)
                correlations=[float(spearmanr(direct[i],direct[j]).statistic) for i,j in itertools.combinations(range(len(b)),2)]
                error=abs(float(np.mean(correlations))-d['bub1b']['mean_pair']);require(error<2e-5,'Original GCTX BUB1B mismatch');max_error=max(max_error,error)
                target=genes.index[genes.pr_gene_symbol.eq('BUB1B')].item()
                for i,r in enumerate(d['bub1b']['reagents']):
                    require(r['signature_id']==local.iloc[b[i]].sig_id and r['target_z']==float(direct[i,target]),'Reagent identity/target mismatch')
                nulls=[]
                by_id={v:i for i,v in enumerate(local.pert_id)}
                for r in d['bub1b']['nulls']:
                    if r['status']!='complete':
                        require(r['tail'] is None and any(v==0 for v in r['pool_sizes']),'Unknown silently treated as complete');continue
                    vals=np.load(out/r['null_file']);require(digest(out/r['null_file'])==r['null_sha256'],'Null checksum mismatch')
                    require(np.isfinite(vals).all() and len(vals)==r['draws'],'Bad retained null')
                    count=int((vals>=r['observed_mean_pair']).sum())
                    expected=count/len(vals) if r['kind']=='exact_enumeration' else (count+1)/(len(vals)+1)
                    require(count==r['at_or_above'] and expected==r['tail'],'Null tail mismatch')
                    # Independently enumerate the first valid seed control sets and use original coordinates.
                    sample_error=None
                    if r['kind']=='exact_enumeration':
                        pools=[[by_id[v] for v in p] for p in r['pool_reagent_ids']]
                        got=[]
                        for draw in itertools.product(*pools):
                            names=local.iloc[list(draw)].pert_iname.tolist()
                            if len(set(names))!=len(names):continue
                            order=np.argsort(ids[list(draw)]);ordered_ids=ids[list(draw)][order]
                            vectors=np.asarray(matrix[ordered_ids],dtype=float)[np.argsort(order)]
                            got.append(np.mean([spearmanr(vectors[a],vectors[b0]).statistic for a,b0 in itertools.combinations(range(len(draw)),2)]))
                            if len(got)==3:break
                        sample_error=float(np.max(np.abs(np.asarray(got)-vals[:len(got)])))
                        require(sample_error<2e-5,'Original-coordinate null mismatch');max_error=max(max_error,sample_error)
                    null_total+=len(vals);nulls.append(dict(arm=r['arm'],retained=len(vals),original_coordinate_sample_error=sample_error))
                records.append(dict(cell=cell,space=space,bub1b_pair_comparisons=len(correlations),original_coordinate_mean_error=error,nulls=nulls))
    require(null_total==result['summary']['null_sets'],'Null count mismatch')
    monitor=list(csv.DictReader((root/'logs/gpu-monitor.csv').open()))
    utilization={}
    for gpu in range(8):
        rows=[r for r in monitor if r[' index'].strip()==str(gpu)]
        use=[float(r[' utilization.gpu [%]'].split()[0]) for r in rows]
        mem=[float(r[' memory.used [MiB]'].split()[0]) for r in rows]
        utilization[str(gpu)]=dict(samples=len(rows),max_percent=max(use),mean_percent=sum(use)/len(use),peak_used_mib=max(mem))
    save(root/'outputs/numerical-audit.json',dict(passed=True,source='Original GCTX read with h5py; independent scipy.stats.spearmanr',
        independent_reviewer=False,biological_validation=False,cells=records,retained_null_statistics=null_total,
        maximum_original_coordinate_error=max_error,gpu_monitor=utilization))
    inventory=[]
    for directory in ['inputs','outputs','scripts','logs']:
        for path in sorted((root/directory).rglob('*')):
            if path.is_file() and path.name != 'audit.log' and not path.name.endswith('.partial'):
                inventory.append(dict(path=str(path.relative_to(root)),bytes=path.stat().st_size,sha256=digest(path)))
    for name in ['pyproject.toml','uv.lock']:
        p=root/name;inventory.append(dict(path=name,bytes=p.stat().st_size,sha256=digest(p)))
    # Complete large matrices stay on the owner host; archive all smaller evidence and null arrays.
    selected=[v for v in inventory if not v['path'].endswith(('.gctx','.gctx.gz','-all-pairs.npy')) and
              not v['path'] in ['outputs/prepared/raw.npy','outputs/prepared/prime.npy']]
    save(root/'outputs/inventory.json',dict(files=inventory,archived_files=selected,excluded_reason='Downloadable original matrices and complete pair arrays retained on owner host, hash-inventoried'))
    archive=root/'rnai-v23-audit.tar.gz'
    with tarfile.open(archive,'x:gz') as tar:
        for record in selected:tar.add(root/record['path'],arcname=record['path'],recursive=False)
        tar.add(root/'outputs/inventory.json',arcname='outputs/inventory.json',recursive=False)
    save(root/'archive.json',dict(path=archive.name,bytes=archive.stat().st_size,sha256=digest(archive),files=len(selected)+1,
        full_inventory_files=len(inventory),omitted_files=len(inventory)-len(selected)))
    print(json.dumps(json.loads((root/'archive.json').read_text()),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);a=p.parse_args();audit(a.root)
