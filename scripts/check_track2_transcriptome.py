#!/usr/bin/env python3
"""Offline consistency checks for the v19 public perturbation addendum.

No network, GPU, raw dataset or subject files are needed. Passing does not validate biology.
"""
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def require(value,message):
    if not value:raise ValueError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def bh(values):
    require(all(math.isfinite(p) and 0<p<=1 for p in values),'Invalid empirical tail')
    order=sorted(range(len(values)),key=values.__getitem__)
    out=[0.]*len(values);last=1.
    for k in range(len(values)-1,-1,-1):
        i=order[k];last=min(last,values[i]*len(values)/(k+1));out[i]=last
    return out


def validate(first,second,identity):
    require(first['rescue_priority'] is None and first['clinical_exposure_margin'] is None and
            first['phase']=='unconfirmed' and first['drug_ranking_changed'] is False and
            first['wet_lab_performed_by_this_project'] is False,'Unsupported clinical or priority promotion')
    require(second['clinical_validation'] is False and second['drug_ranking_changed'] is False,'Unsupported secondary promotion')
    require(identity['eligible_identity_id']=='BRD-K13514097' and
            identity['reference_inchi_key']=='HKVAMNSJSFKALM-GKUWKFKPSA-N','Chemical identity drift')
    require(identity['phase2_profile_counts_by_id']=={'BRD-A25736793':132,'BRD-K13514097':6,'BRD-K13154216':42},'Compound-label count drift')
    require(set(identity['unresolved_ids'])=={'BRD-A25736793','BRD-K13154216'},'Unresolved chemistry silently cleared')
    for result in [first,second]:
        qs=result['queries']
        require([q['query_index'] for q in qs]==list(range(14)),'Incomplete/duplicate query matrix')
        require(len({q['cell_id'] for q in qs})==11,'Missing cell context')
        require([r['shard'] for r in result['gpu_runs']]==list(range(8)),'Missing GPU shard')
        require(all(r['complete'] and math.isfinite(r['elapsed_seconds']) and r['elapsed_seconds']>0 and
                    math.isfinite(r['peak_allocated_gib']) and r['peak_allocated_gib']>0 for r in result['gpu_runs']),
                'Missing/invalid GPU completion evidence')
        ids=[qid for run in result['gpu_runs'] for qid in run['query_ids']]
        require(sorted(ids)==sorted(q['query_id'] for q in qs),'GPU/query coverage mismatch')
        for q in qs:
            names=[s['name'] for s in q['spaces']]
            require(names in [['raw','shared_pc1_removed'],['raw','shared_pc1_removed','growth_span_removed']],
                    'Missing or unknown sensitivity space')
            for space in q['spaces']:
                require(0<=space['max_cpu_gpu_abs_difference']<=2e-5,'Numerical audit failed')
                ids=[r['signature_id'] for r in space['named_compounds']]
                require(len(ids)==len(set(ids)),'Duplicate named profile')
                for r in space['named_compounds']:
                    require(math.isfinite(r['correlation']) and abs(r['correlation'])<=1.00001,'Invalid correlation')
                    require(0<=r['negative_tail_fraction']<=1 and r['ranking_denominator']>0,'Invalid descriptive rank')
                    qc=r['metadata_quality']
                    require(r['quality_pass']==(qc['distil_nsample']>=3 and qc['distil_cc_q75']>=.2 and qc['tas']>=.2),
                            'QC threshold drift')
    require([q['query_id'] for q in first['queries']]==[q['query_id'] for q in second['queries']], 'Different genetic queries')
    tails=[q['split_null_tail'] for q in first['queries']]
    require(all(math.isfinite(p) and 0<p<=1 for p in tails),'Invalid resampling tail')
    adjusted=bh(tails)
    for q,expected in zip(first['queries'],adjusted):
        require(all(math.isfinite(q[k]) for k in ['median_target_z','pairwise_median','split_median']),
                'Nonfinite genetic-query statistic')
        require(q['null_draws']==10000 and q['null_cpu_gpu_max_difference']<=2e-5,'Resampling incomplete or numerical mismatch')
        require(abs(q['split_null_BH_q']-expected)<1e-12,'Multiple-testing calculation drift')
        gate=(q['n_reagents']>=6 and q['median_target_z']<0 and q['pairwise_median']>0 and q['split_median']>0 and expected<=.05)
        require(q['operational_query_gate']==gate,'Query gate changed or miscomputed')
    return dict(passed=True,genetic_contexts=14,cell_types=11,gpus=8,
        resampled_reagent_sets=sum(q['null_draws'] for q in first['queries']),
        operational_query_gates_passed=sum(q['operational_query_gate'] for q in first['queries']),
        clinical_validation=False,drug_ranking_changed=False)


def check(root=ROOT):
    names=['track2-transcriptome-results-v19.json','track2-transcriptome-phase2-results-v19.json','track2-transcriptome-identity-v19.json']
    first,second,identity=[json.loads((root/'notes'/n).read_text()) for n in names]
    result=validate(first,second,identity)
    followup=json.loads((root/'notes/track2-transcriptome-followup-results-v19.json').read_text())
    validate_followup(followup,first)
    audit=json.loads((root/'notes/track2-transcriptome-audit-v19.json').read_text())
    for path,expected in audit['public_input_sha256'].items():
        require(not Path(path).is_absolute() and '..' not in Path(path).parts,'Unsafe audit path')
        require((root/path).is_file() and not (root/path).is_symlink(),'Missing or unsafe public input')
        require(digest(root/path)==expected,'Changed campaign input: '+path)
    require(first['plan_sha256']==digest(root/'notes/track2-transcriptome-plan-v19.json'),'Primary plan drift')
    require(second['plan_sha256']==digest(root/'notes/track2-transcriptome-phase2-plan-v19.json'),'Secondary plan drift')
    require(followup['plan_sha256']==digest(root/'notes/track2-transcriptome-followup-plan-v19.json'),'Follow-up plan drift')
    require(audit['data_origin']=='public_NIH_GEO_only' and audit['subject_inputs_transferred'] is False,'Data boundary drift')
    require(audit['inference_complete'] is True,'Incomplete campaign')
    state=json.loads((root/'notes/track2-current.json').read_text())
    require(state['research_addendum']['version']==19 and state['research_addendum']['check']=='scripts/check_track2_transcriptome.py',
            'Stale research addendum route')
    require(state['research_addendum']['status']=='complete' and
            state['research_addendum']['report']=='notes/track2-transcriptome-v19.md',
            'Incomplete or missing research addendum')
    result['post_hoc_resampled_reagent_sets']=sum(r['null_draws'] for r in followup['rows'])
    return result


def validate_followup(followup,first):
    require(followup['post_hoc'] is True and followup['primary_gate_replaced'] is False and
            followup['drug_ranking_changed'] is False,'Post-hoc analysis promoted or original gate erased')
    arms={'all_reagents_shared_pc1_removed','provider_members_raw','provider_members_shared_pc1_removed'}
    rows=followup['rows']
    require(len(rows)==42 and {(r['query_index'],r['arm']) for r in rows}=={(i,a) for i in range(14) for a in arms},
            'Incomplete post-hoc comparisons')
    qs=bh([r['split_null_tail'] for r in rows])
    for r,q in zip(rows,qs):
        require(all(math.isfinite(r[k]) for k in ['median_target_z','pairwise_median','split_median']),
                'Nonfinite post-hoc statistic')
        require(r['query_id']==first['queries'][r['query_index']]['query_id'],'Different post-hoc query')
        require(r['null_draws']==10000 and 0<r['split_null_tail']<=1 and r['null_cpu_gpu_max_difference']<=2e-5,
                'Incomplete or inaccurate post-hoc resampling')
        require(abs(r['split_null_BH_q']-q)<1e-12,'Post-hoc multiplicity calculation drift')
        gate=r['n_reagents']>=6 and r['median_target_z']<0 and r['pairwise_median']>0 and r['split_median']>0 and q<=.05
        require(r['same_operational_filter']==gate,'Post-hoc filter drift')
    require([r['shard'] for r in followup['gpu_runs']]==list(range(8)) and
            all(r['complete'] for r in followup['gpu_runs']),'Missing follow-up GPU completion')
    return True


if __name__=='__main__':print(json.dumps(check(),indent=2))
