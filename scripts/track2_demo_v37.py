#!/usr/bin/env python3
"""Replay author-designed teaching cases using the unchanged v21 decision policy.

Standard library only. No network, patient data, model weights or GPU needed.
The cases test implementation behavior, not clinical utility or policy validity.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import time
from track2_falsification_v21 import decide, numeric

ROOT = Path(__file__).resolve().parents[1]


def materialize(definition, current):
    rows = []
    for case in definition['cases']:
        record = copy.deepcopy(current if case['evidence'] == 'current' else definition['base_synthetic_record'])
        for path, value in case['patch'].items():
            keys = path.split('.')
            target = record
            for key in keys[:-1]:
                target = target[key]
            if keys[-1] not in target:
                raise ValueError('Unknown teaching-case field')
            target[keys[-1]] = copy.deepcopy(value)
        rows.append(dict(case=case, record=record))
    return rows


def shortcut(record, include_viability=False):
    """Deliberately incomplete comparator, not a medical decision algorithm."""
    b = record['benefit']
    if b['interval'] is None or b['margin'] is None:
        return False
    enough = b['interval'][0] > b['margin']
    if include_viability:
        h = record['harms']['viability']
        enough = enough and h['interval'] is not None and h['margin'] is not None and h['interval'][1] < h['margin']
    return bool(enough)


def denominator(arm):
    names = {'accurate_viable','erroneous_division','death','arrest','slippage','missing'}
    if set(arm) != names or any(type(v) is not int or v < 0 for v in arm.values()):
        raise ValueError('Nonnegative integer outcome counts required')
    enrolled = sum(arm.values())
    if not enrolled:
        raise ValueError('At least one enrolled cell required')
    divided = arm['accurate_viable'] + arm['erroneous_division']
    return dict(enrolled=enrolled, completed_divisions=divided,
        error_fraction=None if not divided else arm['erroneous_division']/divided,
        observed_useful_fraction=arm['accurate_viable']/enrolled,
        missingness_bounds=[arm['accurate_viable']/enrolled,(arm['accurate_viable']+arm['missing'])/enrolled],
        confidence_interval=False)


def run(case_path=None, current_path=None):
    case_path = case_path or ROOT/'notes/track2-demo-cases-v37.json'
    current_path = current_path or ROOT/'notes/track2-decision-contract-v21.json'
    definition = json.loads(case_path.read_text())
    current = json.loads(current_path.read_text())
    started = time.perf_counter()
    rows = []
    for item in materialize(definition,current):
        case, record = item['case'], item['record']
        decision = decide(record)
        if decision['decision'] != case['expected'] or decision['clinical_recommendation'] is not False:
            raise ValueError('Teaching case mismatch: '+case['id'])
        rows.append(dict(id=case['id'],expected=case['expected'],decision=decision['decision'],
            reason=decision['reason'],evidence_kind=record['evidence_kind'],
            benefit_only_advance=shortcut(record),benefit_and_viability_advance=shortcut(record,True),
            full_policy_advance=decision['decision']=='PRECLINICAL_REVIEW_ONLY'))
    demo=definition['denominator_example']
    outcomes={arm:denominator(demo[arm]) for arm in ['vehicle','drug']}
    baseline,drug=outcomes['vehicle'],outcomes['drug']
    effect_bounds=[drug['missingness_bounds'][0]-baseline['missingness_bounds'][1],
                   drug['missingness_bounds'][1]-baseline['missingness_bounds'][0]]
    return dict(passed=True,version=37,cases=len(rows),synthetic_cases=sum(r['evidence_kind']=='synthetic' for r in rows),
        current_decision=rows[0]['decision'],rows=rows,outcomes=outcomes,
        observed_useful_difference=drug['observed_useful_fraction']-baseline['observed_useful_fraction'],
        missingness_difference_bounds=effect_bounds,missingness_bounds_are_confidence_intervals=False,
        shortcut_advances_rejected_by_policy={key:sum(r[key] and not r['full_policy_advance'] for r in rows)
            for key in ['benefit_only_advance','benefit_and_viability_advance']},
        case_sha256=hashlib.sha256(case_path.read_bytes()).hexdigest(),
        current_sha256=hashlib.sha256(current_path.read_bytes()).hexdigest(),
        seconds=time.perf_counter()-started,clinical_validation=False,external_validation=False,
        community_adoption_measured=False,
        scope='Implementation checks on author-selected teaching cases; no diagnostic or therapeutic performance claim')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases',type=Path)
    parser.add_argument('--current',type=Path)
    args=parser.parse_args()
    print(json.dumps(run(args.cases,args.current),indent=2,allow_nan=False))
