#!/usr/bin/env python3
"""Replay all public optical ranks and registered/exploratory paired comparisons.

Rank-to-MRR arithmetic uses math.fsum. Interval replay deliberately uses the
registered bootstrap routine; it is not an independent statistical implementation.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import tarfile
import numpy as np
from track2_optical_audit_v35 import paired_gain


def rank_metrics(result):
    by_gene={}
    for row in result['rows']:
        rank=float(row['rank'])
        if not 1<=rank<=result['genes']:
            raise ValueError('Rank outside candidate cohort')
        by_gene.setdefault(row['gene'],[]).append(1/rank)
    means={g:math.fsum(v)/len(v) for g,v in by_gene.items()}
    if set(means)!=set(result['by_gene_mrr']) or len(means)!=result['genes']:
        raise ValueError('Gene coverage differs')
    if sum(map(len,by_gene.values()))!=result['guide_queries']:
        raise ValueError('Guide-query count differs')
    for g,m in means.items():
        if abs(m-result['by_gene_mrr'][g])>1e-12:
            raise ValueError('Gene reciprocal rank mismatch')
    macro=math.fsum(means.values())/len(means)
    if abs(macro-result['macro_mrr'])>1e-12:
        raise ValueError('Macro reciprocal rank mismatch')
    return means


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive',type=Path);p.add_argument('manifest',type=Path)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise ValueError('Existing replay protected')
    manifest=json.loads(a.manifest.read_text());raw=a.archive.read_bytes()
    if len(raw)!=manifest['bytes'] or hashlib.sha256(raw).hexdigest()!=manifest['sha256']:
        raise ValueError('Archive hash mismatch')
    arms={}
    with tarfile.open(a.archive) as tar:
        members=tar.getmembers()
        if len(members)!=manifest['files'] or len({m.name for m in members})!=len(members):
            raise ValueError('Archive file count/duplicates')
        if set(m.name for m in members)!=set(manifest['content_sha256']):
            raise ValueError('Manifest/archive file mismatch')
        for m in members:
            if not m.isfile() or Path(m.name).is_absolute() or '..' in Path(m.name).parts:
                raise ValueError('Unsafe archive member')
            if hashlib.sha256(tar.extractfile(m).read()).hexdigest()!=manifest['content_sha256'][m.name]:
                raise ValueError('Archived file hash mismatch')
        def read(name):return json.load(tar.extractfile(name))
        summary=read('outputs/final-review-v36/results.json')
        for arm in ['mitotic','interphase']:
            first=read(f'models-v35/{arm}-3301-real/results.json')
            secondary=read(f'secondary-v35/{arm}/results.json')
            original=read('outputs/audit-v35-'+arm+'.json')
            genes=sorted(first['learned']['by_gene_mrr'])
            def vector(obj):
                means=rank_metrics(obj)
                return [means[g] for g in genes]
            base=[]
            for name,obj in sorted(first['baseline_results'].items()):
                means=rank_metrics(obj);base.append([means[g] for g in genes])
            registered=base+[vector(secondary['secondary_results']['mitotic_fraction'])]
            exploratory=registered+[vector(secondary['secondary_results'][name])
                for name in ['matched_sample_mean','full_median_shared_preprocessing','full_median_training_preprocessing']]
            values=[]
            for label in ['real','shuffled']:
                for seed in [3301,3302,3303,3304]:
                    r=read(f'models-v35/{arm}-{seed}-{label}/results.json')
                    if r['smoke'] or not r['no_query_training'] or r['clinical_validation']:
                        raise ValueError('Invalid model scope')
                    for name,obj in r['baseline_results'].items():
                        rank_metrics(obj)
                        if obj!=first['baseline_results'][name]:raise ValueError('Baseline changed across seed')
                    means=rank_metrics(r['learned']);values.append([means[g] for g in genes])
            comparisons=[(base,values[:4],original['real_gain']),
                (base,values[4:],original['shuffled_gain']),
                (registered,values[:4],secondary['registered_gain_with_cross_arm']),
                (registered,values[4:],secondary['registered_shuffled_with_cross_arm']),
                (exploratory,values[:4],secondary['exploratory_gain_with_all_baselines']),
                (exploratory,values[4:],secondary['exploratory_shuffled_with_all_baselines'])]
            for baselines,learned,recorded in comparisons:
                replay=paired_gain(baselines,learned)
                for field in ['point_difference','paired_95_percent_intervals','joint_minimum_seed_95_percent_interval']:
                    np.testing.assert_allclose(replay[field],recorded[field],rtol=0,atol=1e-12)
                if replay['practical_gain_gate_passed']!=recorded['practical_gain_gate_passed']:
                    raise ValueError('Gain decision differs')
            if summary['arms'][arm]['registered_nine_baseline_gain']!=secondary['registered_gain_with_cross_arm']:
                raise ValueError('Final summary differs from recorded comparison')
            for name,obj in secondary['secondary_results'].items():
                rank_metrics(obj)
                if abs(obj['macro_mrr']-summary['arms'][arm]['baselines'][name]['macro_mrr'])>1e-12:
                    raise ValueError('Secondary summary differs')
            control=read(f'plate-control-v36/{arm}/results.json')
            if control!=summary['arms'][arm]['plate_control'] or not control['post_hoc']:
                raise ValueError('Post-hoc plate-control provenance differs')
            if (not control['full_profile_rank_replay'] or not control['complete_count_conservation']
                    or control['original_gates_changed'] or control['unseen_acquisition_validation']
                    or control['biological_validation'] or control['drug_ranking_changed']):
                raise ValueError('Plate-control scope changed')
            plate_means=rank_metrics(control['plate_only'])
            if set(plate_means)!=set(genes):raise ValueError('Plate-only comparison cohort differs')
            evaluated=0
            for plate in control['within_plate']:
                metric=plate['full_profile']
                if metric is None:
                    if plate['status']!='insufficient_reference_coverage':
                        raise ValueError('Missing within-plate result given a score')
                    continue
                means=rank_metrics(metric);evaluated+=1
                if len(means)!=plate['genes'] or not set(means)<=set(genes):
                    raise ValueError('Within-plate comparison cohort differs')
                for gene,status in plate['query_status'].items():
                    if (gene in means)!=(status=='evaluated'):
                        raise ValueError('Within-plate query coverage differs')
            cross_plate_metrics=0
            for worker in summary['arms'][arm]['plates']:
                label='shuffled' if worker['shuffled'] else 'real'
                raw_plate=read(f"plate-v35/{arm}-{worker['seed']}-{label}/results.json")
                if len(raw_plate['plate_results'])!=8 or len(worker['plates'])!=8:
                    raise ValueError('Cross-plate coverage differs')
                for raw,condensed in zip(raw_plate['plate_results'],worker['plates']):
                    if raw['plate']!=condensed['plate']:raise ValueError('Plate order differs')
                    for name,metric in raw['methods'].items():
                        if metric['status']=='evaluated':
                            rank_metrics(metric);cross_plate_metrics+=1
                        elif metric['rows'] or metric['macro_mrr'] is not None:
                            raise ValueError('Insufficient cross-plate comparison given a score')
                        small=condensed['methods'][name]
                        if any(small[k]!=metric[k] for k in ['status','genes','macro_mrr']):
                            raise ValueError('Cross-plate summary differs')
                        for gene,query in small['queries'].items():
                            if (query['rows']!=[r for r in metric['rows'] if r['gene']==gene]
                                    or query['mrr']!=metric.get('by_gene_mrr',{}).get(gene)):
                                raise ValueError('Cross-plate query summary differs')
            arms[arm]=dict(models=8,test_genes=len(genes),baseline_methods=12,
                paired_comparisons_replayed=6,
                cross_plate_metrics_recomputed=cross_plate_metrics,
                post_hoc_plate_only_rank_metrics_recomputed=True,
                within_plate_rank_metrics_recomputed=evaluated,
                registered_gate=secondary['registered_gain_with_cross_arm']['practical_gain_gate_passed'],
                exploratory_gate=secondary['exploratory_gain_with_all_baselines']['practical_gain_gate_passed'])
    result=dict(passed=True,archive_sha256=manifest['sha256'],files=manifest['files'],arms=arms,
        rank_to_mrr_recomputed=True,all_archive_hashes_verified=True,paired_intervals_recomputed=True,
        bootstrap_repetitions=20000,bootstrap_implementation='Reused registered function; no independent statistical algorithm claimed',
        tolerance=1e-12,biological_validation=False,drug_ranking_changed=False,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
