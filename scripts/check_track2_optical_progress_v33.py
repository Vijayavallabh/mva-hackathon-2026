#!/usr/bin/env python3
"""Check a frozen progress snapshot; never interpret launched jobs as model gains."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(s):
    require(s['research_status'] == 'in_progress' and s['model_results_validated'] is False
            and s['full_model_gain'] is None, 'Unvalidated model gain or completion')
    require(s['drug_ranking_changed'] is False and s['biological_validation'] is False,
            'Unsupported biological promotion')
    require(s['smoke_excluded'] is True, 'Smoke results are not scientific results')
    require((s['source_doi'], s['source_version'], s['source_license']) ==
            ('10.7910/DVN/VYKTI5', '2.0', 'CC BY 4.0'), 'Source identity changed')
    p = s['mitotic_preparation']
    counts = [r['cells'] for r in p['query_coverage']['BUB1B']]
    require(counts == [11, 15, 11, 25] and sum(n >= 20 for n in counts) == 1,
            'BUB1B coverage changed; review original counts')
    require(all(r['meets_20_cell_minimum'] is (r['cells'] >= 20)
                for r in p['query_coverage']['BUB1B']), 'Coverage threshold changed')
    require((p['cells'], p['sampled_cells'], p['guides'], p['features']) ==
            (838224, 832846, 20404, 1068), 'Preparation count drift')
    workers = s['mitotic_worker_registration']['workers']
    require([w['gpu'] for w in workers] == list(range(8)), 'Incomplete launched wave')
    require([w['seed'] for w in workers] == [3301,3302,3303,3304]*2 and
            [w['shuffled'] for w in workers] == [False]*4+[True]*4, 'Worker control design drift')
    return dict(passed=True, research_status='in_progress', launched_workers=8,
                model_results_validated=False, full_model_gain=None,
                bub1b_mitotic_counts=counts, bub1b_mitotic_retrieval='insufficient_guide_coverage',
                drug_ranking_changed=False, biological_validation=False)


def check(root=ROOT):
    s = json.loads((root/'notes/track2-optical-status-v33.json').read_text())
    result = validate(s)
    bindings = dict(s['scripts']) | s['environment'] | {
        'notes/track2-optical-plan-v33.json':s['plan_sha256'],
        'notes/track2-optical-amendment-v33.json':s['amendment_sha256'],
    }
    for relative, expected in bindings.items():
        p = Path(relative)
        require(not p.is_absolute() and '..' not in p.parts and p.parts[0] in {'notes','scripts'},
                'Unsafe progress input path')
        require(not any((root/Path(*p.parts[:i])).is_symlink() for i in range(1,len(p.parts)+1)),
                'Symlinked progress input')
        require(hashlib.sha256((root/p).read_bytes()).hexdigest() == expected,
                'Progress input changed: '+relative)
    amendment = json.loads((root/'notes/track2-optical-amendment-v33.json').read_text())
    require(amendment['implementation_details_fixed_before_fitting']['guide_minimum_unchanged'] == 20,
            'Coverage minimum relaxed')
    require(amendment['changes'][0]['value'] == '2026-11-23', 'Deletion amendment drift')
    return result


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
