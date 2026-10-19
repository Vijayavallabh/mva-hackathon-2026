#!/usr/bin/env python3
"""Fail closed on promotion of the corrected mitotic result or historical fits."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BINDINGS={
    'notes/track2-optical-amendment-v35.json':'4231bcb4055c5aaa9899a5d9a0503e140fadafe99dd42240b9693f3cd8116946',
    'notes/track2-optical-mitotic-results-v35.json':'84cdcfca25de1c49210e79948d3747ff7d627cdf03e9b2778d1e2bec25fb967e',
    'notes/track2-optical-equivalence-v35.json':'845b0edc5a5403e2e37e34facbbea26877a1361e4d512b30ee12480a66f70f64',
    'notes/track2-optical-independent-mitotic-v35.json':'08a401ea43318ccb6dd5b522fa87b8d0c06a8aa7f81b7ac12506d931cb245ddd',
    'notes/track2-optical-local-replay-v35.json':'68f2fabc302d7a9f621ff4f7c7d32912a465b7911b64ab376b0fcee994a1e6f0',
    'notes/track2-optical-plates-mitotic-v35.json':'c52fd31d3c4a9e8c78340443cfdd134bb71280d9a3ab87209db41c74e53a768c',
}


def require(condition,message):
    if not condition:
        raise ValueError(message)


def validate(r):
    require(r['arm']=='mitotic' and r['genes']==950,'Wrong evaluated cohort')
    require(r['original_v33_fits_excluded'] is True and r['biological_validation'] is False
            and r['drug_ranking_changed'] is False,'Unsupported promotion')
    best=max(v['macro_mrr'] for v in r['baselines'].values())
    expected=[x['macro_mrr']-best for x in r['learned']]
    require(len(expected)==4 and all(abs(a-b)<1e-12 for a,b in
            zip(expected,r['real_gain']['point_difference'])),'Incorrect paired differences')
    require(all(v<.02 for v in expected) and r['real_gain']['practical_gain_gate_passed'] is False,
            'Failed practical gain gate promoted')
    require(r['real_gain']['joint_minimum_seed_95_percent_interval'][0]<0
            and r['real_gain']['joint_lower_bound_positive'] is False,'Uncertainty omitted')
    require(r['query_status']['BUB1B']==dict(eligible_guides=1,status='insufficient_guide_coverage',rank_is_missing=True),
            'Missing BUB1B evidence promoted')
    require(r['mitotic_fraction_baseline_pending'] is True,'Pending cross-arm analysis falsely completed')
    require(r['seeds']==[3301,3302,3303,3304] and len(r['shuffled'])==4,'Seed/control omitted')
    return dict(passed=True,corrected_mitotic_gain_gate_passed=False,genes=950,
                corrected_features=1064,bub1b_mitotic_retrieval='insufficient_guide_coverage',
                interphase_review_pending=True,biological_validation=False,drug_ranking_changed=False)


def check(root=ROOT):
    for relative,digest in BINDINGS.items():
        p=root/relative
        require(not p.is_symlink() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,
                'Bound optical correction input changed: '+relative)
    r=json.loads((root/'notes/track2-optical-mitotic-results-v35.json').read_text())
    replay=json.loads((root/'notes/track2-optical-equivalence-v35.json').read_text())
    independent=json.loads((root/'notes/track2-optical-independent-mitotic-v35.json').read_text())
    local=json.loads((root/'notes/track2-optical-local-replay-v35.json').read_text())
    plates=json.loads((root/'notes/track2-optical-plates-mitotic-v35.json').read_text())
    require(replay['passed'] and replay['exact_cells_counts_sampling_and_values'] and
            replay['corrected_features']==1064,'Preservation audit failed')
    require(independent['passed'] and len(independent['guides'])==40 and
            max(g['maximum_sum_error'] for g in independent['guides'])<=1e-7,'Independent arithmetic audit failed')
    require(local['passed'] and local['paired_intervals_recomputed'] and local['models']==8
            and local['practical_gain_gate_passed'] is False,'Local rank/interval replay failed')
    require(len(plates['workers'])==8 and all(len(w['plates'])==8 for w in plates['workers']),
            'Plate workers omitted')
    require(all(p['methods']['learned']['genes']<=2 and all(q['status']=='insufficient_guide_coverage'
            for q in p['methods']['learned']['queries'].values()) for w in plates['workers'] for p in w['plates']),
            'Missing plate evidence promoted')
    for record,script in [(r,'track2_optical_audit_v35.py'),(replay,'track2_optical_audit_v35.py'),
                           (independent,'track2_optical_independent_v35.py'),
                           (local,'track2_optical_archive_review_v35.py'),
                           (plates,'track2_optical_plate_summary_v35.py')]:
        key='audit_script_sha256' if 'audit_script_sha256' in record else 'script_sha256'
        require(hashlib.sha256((root/'scripts'/script).read_bytes()).hexdigest()==record[key],
                'Executed audit script changed')
    return validate(r)


if __name__=='__main__':
    print(json.dumps(check(),indent=2))
