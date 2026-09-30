#!/usr/bin/env python3
"""Separate CPU audit from original source coordinates; no GPU or inference.

This is a separately implemented numerical check, not an independent reviewer.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import h5py
from scipy.stats import spearmanr


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        while b:=f.read(8*1024**2):h.update(b)
    return h.hexdigest()


def run(root):
    prep=root/'outputs/prepared'
    lm=pd.read_csv(prep/'landmarks.tsv',sep='\t',dtype=str)
    audit=[];bub_original={}
    decode=lambda a:[v.decode() if isinstance(v,bytes) else str(v) for v in a]
    for arm,name in [('xpr','level5_beta_trt_xpr_n142901x12328.gctx'),('cp','level5_beta_trt_cp_n720216x12328.gctx')]:
        meta=pd.read_csv(prep/f'{arm}-metadata.tsv.gz',sep='\t',dtype=str,keep_default_na=False)
        extracted=np.load(prep/(arm+'.npy'),mmap_mode='r')
        with h5py.File(root/'inputs'/name,'r') as f:
            rows=decode(f['0/META/ROW/id'][:]);cols=decode(f['0/META/COL/id'][:])
            assert cols==meta.sig_id.tolist()
            positions=[rows.index(g) for g in lm.gene_id]
            selected=set(np.linspace(0,len(cols)-1,24,dtype=int).tolist())
            if arm=='xpr':selected.update(meta.index[meta.cmap_name.eq('BUB1B')].tolist())
            if arm=='cp':selected.update(meta.index[meta.cmap_name.str.lower().eq('everolimus')][::10].tolist())
            maximum=0.
            for i in sorted(selected):
                source=f['0/DATA/0/matrix'][i][positions]
                maximum=max(maximum,float(np.max(np.abs(source-extracted[i]))))
                if arm=='xpr' and meta.iloc[i].cmap_name=='BUB1B':bub_original[cols[i]]=np.asarray(source,dtype=np.float64)
            assert maximum==0
            audit.append(dict(arm=arm,rows_checked=len(selected),features_checked=978,maximum_error=maximum,all_column_ids_equal=True))
    named=pd.read_csv(root/'outputs/named-drugs.tsv.gz',sep='\t')
    cpmeta=pd.read_csv(prep/'cp-metadata.tsv.gz',sep='\t',dtype=str,keep_default_na=False)
    xm=pd.read_csv(prep/'xpr-metadata.tsv.gz',sep='\t',dtype=str,keep_default_na=False)
    cpos={v:i for i,v in enumerate(cpmeta.sig_id)}
    direct=[]
    with h5py.File(root/'inputs/level5_beta_trt_cp_n720216x12328.gctx','r') as f:
        rows=decode(f['0/META/ROW/id'][:]);positions=[rows.index(g) for g in lm.gene_id]
        for r in named[named.gene.eq('BUB1B')&named.compound.str.lower().eq('everolimus')].itertuples():
            ids=xm[xm.cell_iname.eq(r.cell)&xm.cmap_name.eq('BUB1B')&xm.pert_time.eq('96')].sig_id
            query=np.mean([bub_original[s] for s in ids],axis=0)
            drug=f['0/DATA/0/matrix'][cpos[r.signature_id]][positions]
            score=float(spearmanr(query,drug).statistic)
            error=abs(score-r.correlation)
            assert error<=2e-5
            direct.append(dict(cell=r.cell,signature_id=r.signature_id,source_cpu=score,gpu=r.correlation,error=error))
    manifest=[]
    for path in sorted((root/'outputs').rglob('*')):
        if path.is_file() and path.name not in ['audit.json','output-inventory.json']:
            manifest.append(dict(path=str(path.relative_to(root)),bytes=path.stat().st_size,sha256=sha(path)))
    inventory=root/'outputs/output-inventory.json'
    with inventory.open('x') as f:json.dump(manifest,f,indent=2)
    result=dict(passed=True,source_coordinates=audit,direct_everolimus_checks=direct,
                direct_everolimus_count=len(direct),maximum_error=max(r['error'] for r in direct),
                tolerance=2e-5,inventory_sha256=sha(inventory),inventory_files=len(manifest),
                method='CPU SciPy Spearman from original GCTX values and exact IDs; no GPU score reuse as reference',
                independent_reviewer=False)
    with (root/'outputs/audit.json').open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='direct_everolimus_checks'},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);run(p.parse_args().root)
