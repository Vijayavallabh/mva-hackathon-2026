#!/usr/bin/env python3
"""Recompute CUDA full query profiles from original raw counts on CPU FP64."""
import argparse
import json
from pathlib import Path


def audit(root, worker):
    import h5py
    import numpy as np
    import pandas as pd
    out=root/'outputs'/worker
    reg=json.loads((out/'registration.json').read_text())
    cell=reg['cell'];prep=root/'outputs/prepared'
    obs=pd.read_csv(prep/f'{cell}-obs.tsv.gz',sep='\t',keep_default_na=False)
    features=pd.read_csv(prep/f'{cell}-features.tsv',sep='\t')
    original_var=pd.read_csv(prep/f'{cell}-var.tsv.gz',sep='\t')
    pos={g:i for i,g in enumerate(original_var.gene_id)}
    cols=[pos[g] for g in features.gene_id]
    controls=obs[reg['control_view']].to_numpy(dtype=bool,copy=True)
    excluded=set(reg['excluded_batches']);controls&=~obs.gem_group.isin(excluded).to_numpy()
    ids=np.flatnonzero(controls)
    total=obs.UMI_count.to_numpy(dtype=np.float64)
    with h5py.File(root/'inputs'/f'{cell}_raw_singlecell_01.h5ad','r') as source:
        # Read row chunks from the original deposited count matrix, independent of prepared floats.
        blocks=[np.asarray(source['X'][ids[j:j+512]],dtype=np.float64)[:,cols] for j in range(0,len(ids),512)]
        control_data=np.concatenate(blocks)
        control_data=np.log1p(control_data/total[ids,None]*1e4)
        reference={b:control_data[obs.gem_group.to_numpy()[ids]==b].mean(0) for b in set(obs.gem_group[controls])}
        observed=np.load(out/'full-profiles.npy',mmap_mode='r');rows=[]
        plan=json.loads((root/'inputs/plan.json').read_text())
        for gene in plan['queries']:
            labels=[g for g in reg['names'] if '_'+gene+'_' in g]
            for label in labels:
                selected=np.flatnonzero(obs.gene_transcript.eq(label)&~obs.gem_group.isin(excluded))
                count=np.asarray(source['X'][selected],dtype=np.float64)[:,cols]
                values=np.log1p(count/total[selected,None]*1e4)
                for k,idx in enumerate(selected):values[k]-=reference[obs.gem_group.iloc[idx]]
                expected=values.mean(0)
                error=float(np.max(np.abs(expected-observed[reg['names'].index(label)])))
                if error>2e-5:raise ValueError(f'Original-coordinate CPU check failed for {gene}: {error}')
                rows.append(dict(gene=gene,construct=label,cells=len(selected),max_absolute_error=error))
    result=dict(passed=True,scope='Original raw counts and library totals to independent CPU FP64 full query mean profiles',
                worker=worker,queries=rows,tolerance=2e-5,biological_validation=False)
    (out/'cpu-original-counts-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    p.add_argument('--worker',default='worker-0');a=p.parse_args();audit(a.root,a.worker)
