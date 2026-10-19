#!/usr/bin/env python3
"""Condense every plate/seed result without pooling changing reference cohorts."""
import argparse
import json
from pathlib import Path
from track2_optical_fetch_v33 import hashes, write_json
from track2_optical_prepare_v35 import QUERIES


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    p.add_argument('--arm',choices=['mitotic','interphase'],required=True);a=p.parse_args();root=a.root.resolve()
    out=root/'outputs'/f'plate-summary-v35-{a.arm}.json'
    if out.exists():raise ValueError('Preserve prior summary')
    results=[];bindings={}
    for shuffled in [False,True]:
        for seed in [3301,3302,3303,3304]:
            folder=root/'plate-v35'/f"{a.arm}-{seed}-{'shuffled' if shuffled else 'real'}"
            complete=json.loads((folder/'complete.json').read_text())
            digest=hashes(folder/'results.json')[1]
            if digest!=complete['files']['results.json']:raise ValueError('Changed plate result')
            r=json.loads((folder/'results.json').read_text())
            if (r['arm'],r['seed'],r['shuffled'],r['unseen_acquisition_training'])!=(a.arm,seed,shuffled,False):
                raise ValueError('Plate worker identity or scope mismatch')
            bindings[str((folder/'results.json').relative_to(root))]=digest
            plates=[]
            for v in r['plate_results']:
                methods={}
                for name,m in v['methods'].items():
                    methods[name]={k:m[k] for k in ['status','genes','macro_mrr']}
                    methods[name]['queries']={g:dict(status='evaluated' if g in m.get('by_gene_mrr',{}) else 'insufficient_guide_coverage',
                        mrr=m.get('by_gene_mrr',{}).get(g),rows=[x for x in m['rows'] if x['gene']==g]) for g in QUERIES}
                plates.append(dict(plate=v['plate'],methods=methods,query_counts=v['queries']))
            results.append(dict(seed=seed,shuffled=shuffled,plates=plates,
                pooled_plate_mean_max_absolute_error=r['pooled_plate_mean_max_absolute_error'],
                elapsed_seconds=r['elapsed_seconds']))
    plate_names=[p['plate'] for p in results[0]['plates']]
    if len(plate_names)!=8 or any([p['plate'] for p in r['plates']]!=plate_names for r in results):
        raise ValueError('Plate coverage differs between workers')
    record=dict(arm=a.arm,bindings=bindings,workers=results,unseen_acquisition_training=False,
        biological_validation=False,drug_ranking_changed=False,script_sha256=hashes(Path(__file__))[1],
        interpretation='Each plate has its own eligible test/reference genes. Do not compare raw MRR across plates or with the pooled 950-gene mitotic cohort as a gain. Missing queries are not negative effects.')
    write_json(out,record)
    for v in results[0]['plates']:
        m=v['methods']['learned']
        print(json.dumps(dict(plate=v['plate'],genes=m['genes'],
            evaluated_queries=[g for g,x in m['queries'].items() if x['status']=='evaluated'])),flush=True)


if __name__=='__main__':main()
