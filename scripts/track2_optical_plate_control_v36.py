#!/usr/bin/env python3
"""Post-hoc plate-only and within-plate controls for favorable public morphology.

This does not refit models, replace the registered gain test or claim unseen-batch
validation. The plan was fixed after favorable interphase query ranks were seen.
"""
import argparse
import json
from pathlib import Path
import time
import numpy as np
from track2_optical_fetch_v33 import hashes,write_json

PLAN_SHA='d37fd603963b676eab0ddebb431367a962f33faeaa0d3dc4bd44311d73e7420e'


def plate_vectors(rows,plate_rows):
    lookup={r['guide']:i for i,r in enumerate(rows)}
    if len(lookup)!=len(rows):raise ValueError('Duplicate guide')
    plates=sorted({r['plate'] for r in plate_rows});column={p:i for i,p in enumerate(plates)}
    counts=np.zeros((len(rows),len(plates)),dtype=np.int64);seen=set()
    for row in plate_rows:
        key=(row['guide'],row['plate'])
        if key in seen or row['guide'] not in lookup or row['cells']<=0:
            raise ValueError('Invalid or duplicate guide-plate count')
        seen.add(key);counts[lookup[row['guide']],column[row['plate']]]=row['cells']
    total=np.asarray([r['cells'] for r in rows])
    if not np.array_equal(counts.sum(1),total):raise ValueError('Guide-plate counts do not conserve complete cells')
    single=[plates[int(np.argmax(r))] if np.count_nonzero(r)==1 else None for r in counts]
    return (counts/total[:,None]).astype(np.float32),single,plates


def main():
    import torch
    from track2_optical_model_v35 import eligible_groups,retrieve
    from track2_optical_plate_v35 import transform
    from track2_optical_prepare_v35 import QUERIES
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    p.add_argument('--arm',choices=['mitotic','interphase'],required=True);a=p.parse_args();root=a.root.resolve()
    if not root.is_relative_to('/home/prachh/v'):raise ValueError('All work stays under v')
    if not torch.cuda.is_available() or torch.cuda.device_count()!=1:raise ValueError('Expose one idle GPU')
    if hashes(root/'inputs/plate-control-plan-v36.json')[1]!=PLAN_SHA:raise ValueError('Plan changed')
    torch.backends.cuda.matmul.allow_tf32=False;torch.use_deterministic_algorithms(True)
    source=root/'prepared-v35'/a.arm;model=root/'models-v35'/f'{a.arm}-3301-real'
    prepared=json.loads((source/'complete.json').read_text());complete=json.loads((model/'complete.json').read_text())
    for name in ['guides.json','guide_plates.json','full_profiles.npz']:
        if hashes(source/name)[1]!=prepared['outputs'][name]:raise ValueError('Prepared input changed')
    for name in ['preprocessing.npz','results.json']:
        if hashes(model/name)[1]!=complete['files'][name]:raise ValueError('Model baseline changed')
    out=root/'plate-control-v36'/a.arm;out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    rows=json.loads((source/'guides.json').read_text());plate_rows=json.loads((source/'guide_plates.json').read_text())
    vectors,single,plates=plate_vectors(rows,plate_rows)
    groups=eligible_groups(rows,'test')
    with np.load(model/'preprocessing.npz') as pre,np.load(source/'full_profiles.npz') as data:
        profile=torch.tensor(transform(data['means'],pre['keep'],pre['center'],pre['scale']),device='cuda')
    replay=retrieve(profile,groups)
    original=json.loads((model/'results.json').read_text())['baseline_results']['full_profile']
    if [(r['gene'],r['guide_index'],r['rank']) for r in replay['rows']]!=[
        (r['gene'],r['guide_index'],r['rank']) for r in original['rows']]:
        raise ValueError('Full-profile reconstruction changed guide ranks')
    if abs(replay['macro_mrr']-original['macro_mrr'])>1e-12:raise ValueError('Full-profile MRR replay differs')
    plate_only=retrieve(torch.tensor(vectors,device='cuda'),groups)
    within=[]
    for plate in plates:
        subset={g:[i for i in ix if single[i]==plate] for g,ix in groups.items()}
        subset={g:ix for g,ix in subset.items() if len(ix)>=2}
        metric=retrieve(profile,subset) if len(subset)>=2 else None
        within.append(dict(plate=plate,genes=len(subset),status='evaluated' if metric else 'insufficient_reference_coverage',
            full_profile=metric,query_status={g:'evaluated' if g in subset and metric else 'insufficient_guide_coverage' for g in QUERIES}))
    result=dict(arm=a.arm,plan_sha256=PLAN_SHA,post_hoc=True,plate_only=plate_only,within_plate=within,
        prepared_sha256=hashes(source/'complete.json')[1],original_model_sha256=hashes(model/'complete.json')[1],
        full_profile_rank_replay=True,complete_count_conservation=True,
        query_plates={g:[dict(guide=r['guide'],cells=r['cells'],single_plate=single[i],
                            plate_fractions=vectors[i].tolist()) for i,r in enumerate(rows) if r['gene']==g] for g in QUERIES},
        plates=plates,elapsed_seconds=time.monotonic()-start,script_sha256=hashes(Path(__file__))[1],
        original_gates_changed=False,unseen_acquisition_validation=False,
        biological_validation=False,drug_ranking_changed=False)
    write_json(out/'results.json',result)
    write_json(out/'complete.json',dict(files={'results.json':hashes(out/'results.json')[1]}))
    print(json.dumps(dict(arm=a.arm,plate_only_mrr=plate_only['macro_mrr'],
        bub1b_plate_only=[r['rank'] for r in plate_only['rows'] if r['gene']=='BUB1B'],
        bub1b_within_plate=[dict(plate=v['plate'],genes=v['genes'],ranks=[r['rank'] for r in v['full_profile']['rows'] if r['gene']=='BUB1B'])
            for v in within if v['full_profile'] and 'BUB1B' in v['full_profile']['by_gene_mrr']])),flush=True)


if __name__=='__main__':main()
