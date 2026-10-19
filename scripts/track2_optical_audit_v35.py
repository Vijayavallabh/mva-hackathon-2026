#!/usr/bin/env python3
"""Audit corrected public optical inputs and paired held-out-gene comparisons.

No clinical inference. The original centroid-contaminated fits are preserved and
excluded. Bootstrap units are genes, not cells, guides or model seeds.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from track2_optical_fetch_v33 import hashes, write_json

REMOVED = ['nucleus_centroid_r','nucleus_centroid_c','cell_centroid_r','cell_centroid_c']


def verify_files(folder, manifest, field='outputs'):
    for name, expected in manifest[field].items():
        p=Path(name)
        if p.is_absolute() or '..' in p.parts or hashes(folder/p)[1] != expected:
            raise ValueError('Bound output changed: '+name)


def equivalence(root):
    old=root/'prepared/mitotic';new=root/'prepared-v35/mitotic'
    for folder in [old,new]:
        verify_files(folder,json.loads((folder/'complete.json').read_text()))
    f1=json.loads((old/'features.json').read_text());f2=json.loads((new/'features.json').read_text())
    if [f for f in f1 if f not in REMOVED] != f2 or set(f1)-set(f2) != set(REMOVED):
        raise ValueError('Unexpected feature correction')
    keep=[f1.index(f) for f in f2]
    if json.loads((old/'guides.json').read_text()) != json.loads((new/'guides.json').read_text()):
        raise ValueError('Guide counts, attribution or splitting changed')
    m1=pq.read_table(old/'sample_meta.parquet').to_pandas()
    m2=pq.read_table(new/'sample_meta.parquet').to_pandas()
    pd.testing.assert_frame_equal(m1,m2)
    a=np.load(old/'sample_x.npy',mmap_mode='r');b=np.load(new/'sample_x.npy',mmap_mode='r')
    for start in range(0,len(a),4096):
        np.testing.assert_array_equal(a[start:start+4096,keep],b[start:start+4096])
    with np.load(old/'full_profiles.npz') as a, np.load(new/'full_profiles.npz') as b:
        for name in ['sums','finite_counts','means']:
            np.testing.assert_array_equal(a[name][:,keep],b[name])
    return dict(passed=True,original_features=len(f1),corrected_features=len(f2),
                removed=REMOVED,sampled_cells=len(m1),exact_cells_counts_sampling_and_values=True,
                old_complete_sha256=hashes(old/'complete.json')[1],
                new_complete_sha256=hashes(new/'complete.json')[1],biological_validation=False)


def paired_gain(baselines, learned, repetitions=20000, seed=3501):
    """Recompute the strongest baseline inside each paired gene bootstrap."""
    baselines=np.asarray(baselines,dtype=np.float64);learned=np.asarray(learned,dtype=np.float64)
    if (baselines.ndim!=2 or learned.ndim!=2 or baselines.shape[1]!=learned.shape[1]
            or learned.shape[0]!=4 or not np.isfinite(baselines).all()
            or not np.isfinite(learned).all()):
        raise ValueError('Invalid paired gene matrices')
    n=learned.shape[1]
    if n<2:
        raise ValueError('At least two genes required')
    rng=np.random.default_rng(seed);draws=[]
    for start in range(0,repetitions,256):
        ix=rng.integers(n,size=(min(256,repetitions-start),n))
        strongest=baselines[:,ix].mean(2).max(0)
        draws.append(learned[:,ix].mean(2)-strongest)
    boot=np.concatenate(draws,axis=1)
    point=learned.mean(1)-baselines.mean(1).max()
    interval=np.quantile(boot,[.025,.975],axis=1).T
    joint=np.quantile(boot.min(0),[.025,.975])
    return dict(seed=seed,repetitions=repetitions,unit='held-out genes',
        point_difference=point.tolist(),paired_95_percent_intervals=interval.tolist(),
        joint_minimum_seed_95_percent_interval=joint.tolist(),
        all_seeds_exceed_002=bool((point>=.02).all()),
        all_paired_lower_bounds_positive=bool((interval[:,0]>0).all()),
        joint_lower_bound_positive=bool(joint[0]>0),
        practical_gain_gate_passed=bool((point>=.02).all() and (interval[:,0]>0).all() and joint[0]>0))


def metric_summary(result):
    by_gene={}
    for row in result['rows']:
        by_gene.setdefault(row['gene'],[]).append(row['rank'])
    return dict(macro_mrr=result['macro_mrr'],genes=result['genes'],guide_queries=result['guide_queries'],
        macro_top1=float(np.mean([np.mean(np.asarray(v)<=1) for v in by_gene.values()])),
        macro_top10=float(np.mean([np.mean(np.asarray(v)<=10) for v in by_gene.values()])),
        fractional_average_rank_count=sum(float(r['rank'])%1!=0 for r in result['rows']),
        topk_policy='Average ranks for exact score ties; rank thresholds. Fractional-rank count misses ties with integer average rank.')


def summarize(root,arm):
    results=[];bindings={}
    for shuffled in [False,True]:
        for seed in [3301,3302,3303,3304]:
            folder=root/'models-v35'/f"{arm}-{seed}-{'shuffled' if shuffled else 'real'}"
            complete=json.loads((folder/'complete.json').read_text())
            if complete['smoke']:
                raise ValueError('Smoke runs cannot enter analysis')
            verify_files(folder,complete,'files')
            r=json.loads((folder/'results.json').read_text())
            if r['seed']!=seed or r['shuffled']!=shuffled or r['arm']!=arm or r['smoke']:
                raise ValueError('Worker identity mismatch')
            results.append(r);bindings[str(folder.relative_to(root)/'complete.json')]=hashes(folder/'complete.json')[1]
    genes=sorted(results[0]['learned']['by_gene_mrr'])
    names=sorted(results[0]['baseline_results'])
    expected={'full_profile','full_correlation','basic_morphology','size_only','guide_abundance',
              'pca_whiten_64','pca_whiten_128','pca_whiten_256'}
    if set(names)!=expected:
        raise ValueError('Missing declared baseline')
    baseline=[]
    for name in names:
        values=results[0]['baseline_results'][name]['by_gene_mrr']
        if sorted(values)!=genes:
            raise ValueError('Unpaired baseline gene sets')
        a=np.asarray([values[g] for g in genes]);baseline.append(a)
        for r in results[1:]:
            other=r['baseline_results'][name]['by_gene_mrr']
            if sorted(other)!=genes or not np.array_equal(a,[other[g] for g in genes]):
                raise ValueError('Baselines differ across seeds; investigate before averaging')
    learned=[]
    for r in results:
        if sorted(r['learned']['by_gene_mrr'])!=genes:
            raise ValueError('Unpaired learned gene sets')
        learned.append([r['learned']['by_gene_mrr'][g] for g in genes])
    strongest=max(names,key=lambda n:results[0]['baseline_results'][n]['macro_mrr'])
    return dict(arm=arm,bindings=bindings,genes=len(genes),seeds=[3301,3302,3303,3304],
        baselines={n:metric_summary(results[0]['baseline_results'][n]) for n in names},
        strongest_baseline=strongest,
        learned=[dict(seed=r['seed'],**metric_summary(r['learned'])) for r in results[:4]],
        shuffled=[dict(seed=r['seed'],**metric_summary(r['learned'])) for r in results[4:]],
        real_gain=paired_gain(baseline,learned[:4]),shuffled_gain=paired_gain(baseline,learned[4:]),
        query_status=results[0]['query_status'],
        queries=[dict(seed=r['seed'],shuffled=r['shuffled'],
            methods={name:[x for x in obj['rows'] if x['gene'] in r['query_status']]
                     for name,obj in dict(r['baseline_results'],learned=r['learned']).items()}) for r in results],
        original_v33_fits_excluded=True,mitotic_fraction_baseline_pending=True,
        biological_validation=False,drug_ranking_changed=False,
        limitation='Corrected pooled acquisition comparison; separate-plate, independent-summary and cross-arm audits remain separate requirements.')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    p.add_argument('action',choices=['equivalence','summarize']);p.add_argument('--arm',choices=['mitotic','interphase'])
    args=p.parse_args();root=args.root.resolve()
    target=root/'outputs'/('audit-v35-equivalence.json' if args.action=='equivalence' else f'audit-v35-{args.arm}.json')
    if target.exists():
        raise ValueError('Preserve existing audit; use an explicitly versioned follow-up')
    if args.action=='summarize' and not args.arm:
        raise ValueError('Arm required')
    result=equivalence(root) if args.action=='equivalence' else summarize(root,args.arm)
    result['audit_script_sha256']=hashes(Path(__file__))[1]
    write_json(target,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['queries','bindings']},indent=2))


if __name__=='__main__':
    main()
