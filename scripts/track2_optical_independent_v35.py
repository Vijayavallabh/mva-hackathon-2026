#!/usr/bin/env python3
"""Independently count/reduce the ten public query genes with CPU math.fsum."""
import argparse
import json
import math
from pathlib import Path
import time

import numpy as np
import pyarrow.parquet as pq

from track2_optical_fetch_v33 import hashes, selected_files, write_json
from track2_optical_prepare_v35 import QUERIES


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    p.add_argument('--arm',choices=['mitotic','interphase'],required=True);a=p.parse_args()
    root=a.root.resolve();out=root/'outputs'/f'audit-independent-v35-{a.arm}.json'
    if out.exists():
        raise ValueError('Preserve prior audit')
    if not (root/'outputs'/f'download-{a.arm}-complete.json').is_file():
        raise ValueError('Complete export required')
    source=root/'prepared-v35'/a.arm
    guides=json.loads((source/'guides.json').read_text())
    features=json.loads((source/'features.json').read_text())
    lookup={r['guide']:i for i,r in enumerate(guides) if r['gene'] in QUERIES}
    accumulated={};files=[];start=time.monotonic()
    for entry in selected_files(root/'inputs/dataverse-metadata.json',a.arm):
        if not entry['label'].startswith('part.'):
            continue
        path=root/'inputs'/a.arm/entry['label']
        labels=pq.read_table(path,columns=['sgRNA_0','gene_symbol_0'],use_threads=False).to_pandas(ignore_metadata=True)
        mask=labels['gene_symbol_0'].isin(QUERIES).to_numpy()
        if not mask.any():
            continue
        md5,sha=hashes(path)
        if md5!=entry['dataFile']['checksum']['value'] or path.stat().st_size!=entry['dataFile']['filesize']:
            raise ValueError('Independent source checksum failure')
        files.append(dict(source=entry['label'],sha256=sha,provider_md5=md5))
        # Separate read and reduction from preparation; no cached profile arithmetic.
        table=pq.read_table(path,columns=features,use_threads=False)
        for guide in sorted(set(labels.loc[mask,'sgRNA_0'])):
            if guide not in lookup:
                raise ValueError('Prepared query guide omitted')
            ix=np.flatnonzero(labels['sgRNA_0'].to_numpy()==guide)
            if set(labels.iloc[ix]['gene_symbol_0'])!={guides[lookup[guide]]['gene']}:
                raise ValueError('Independent guide attribution mismatch')
            item=accumulated.setdefault(guide,dict(cells=0,sums=np.zeros(len(features)),finite=np.zeros(len(features),dtype=np.int64)))
            item['cells']+=len(ix)
            for j,name in enumerate(features):
                values=np.asarray(table.column(name).to_numpy(zero_copy_only=False)[ix],dtype=np.float32)
                finite=values[np.isfinite(values)]
                clipped=[min(10.,max(-10.,float(v))) for v in finite]
                item['sums'][j]+=math.fsum(clipped);item['finite'][j]+=len(clipped)
    if set(accumulated)!=set(lookup):
        raise ValueError('Prepared/source query guide sets differ')
    with np.load(source/'full_profiles.npz') as data:
        sums,counts=data['sums'],data['finite_counts']
    records=[]
    for guide,item in accumulated.items():
        i=lookup[guide]
        if item['cells']!=guides[i]['cells'] or not np.array_equal(item['finite'],counts[i]):
            raise ValueError('Independent query cell/finite counts differ')
        error=float(np.max(np.abs(item['sums']-sums[i])))
        if error>1e-7:
            raise ValueError('Independent query sums differ')
        records.append(dict(gene=guides[i]['gene'],guide=guide,cells=item['cells'],maximum_sum_error=error))
    result=dict(passed=True,arm=a.arm,features=len(features),guides=records,source_files=files,
        sum_absolute_tolerance=1e-7,elapsed_seconds=time.monotonic()-start,
        prepared_complete_sha256=hashes(source/'complete.json')[1],script_sha256=hashes(Path(__file__))[1],
        arithmetic='Separate source reads; CPU math.fsum over finite source-float32 values clipped to [-10,10]',
        biological_validation=False,drug_ranking_changed=False)
    write_json(out,result)
    print(json.dumps(dict(passed=True,arm=a.arm,guides=len(records),elapsed_seconds=result['elapsed_seconds'])),flush=True)


if __name__=='__main__':
    main()
