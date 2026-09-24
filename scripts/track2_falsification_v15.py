#!/usr/bin/env python3
"""Offline adversarial reanalysis and preclinical claim gates; no clinical decisions."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WINDOWS = ('n_terminal_1022', 'c_terminal_1022', 'published_domain_721_1044')
GROUPS = {'V793R':'primary_impaired', 'K795R':'primary_impaired', 'D911N':'primary_impaired',
          'D882N':'primary_retained', 'K795A':'secondary_impaired',
          'D882A':'secondary_retained', 'N1002K':'candidate'}
MODELS = {'ESMC-300M-score','ESMC-600M-score','ESMC-6B-score','ESM3-score'}
GATES = {'model_qualification','hypothesis_lock','functional_benefit','division_capacity',
         'normal_tissue_safety','replication','exposure_match','source_integrity'}
BIOLOGICAL = {'model_qualification','functional_benefit','division_capacity','normal_tissue_safety','replication'}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def sequence_sensitivity(data):
    """Post-hoc all-control sensitivity, retaining the original primary gate."""
    models = data['models']
    require(set(models) == MODELS, 'Incomplete/unknown model set')
    rows = []
    negative_retained = positive_impaired = 0
    for model, result in sorted(models.items()):
        seen = set()
        for row in result['rows']:
            key = (row['window'],row['variant'])
            require(key not in seen, 'Duplicate score')
            seen.add(key)
            require(row['variant'] in GROUPS and row['group'] == GROUPS[row['variant']], 'Control label drift')
            require(type(row['score']) in (int,float) and math.isfinite(row['score']), 'Nonfinite score')
        require(seen == {(w,v) for w in WINDOWS for v in GROUPS}, 'Missing/extra window or variant')
        for window in WINDOWS:
            s = {r['variant']:r['score'] for r in result['rows'] if r['window'] == window}
            impaired = [s[v] for v,g in GROUPS.items() if 'impaired' in g]
            retained = [s['D882N'], s['D882A']]
            primary = max(s[v] for v in ('V793R','K795R','D911N')) < s['D882N']
            all_controls = max(impaired) < min(retained)
            negative_retained += sum(x < 0 for x in retained)
            positive_impaired += sum(x > 0 for x in impaired)
            rows.append(dict(model=model, window=window, scores=s, primary_ordering=primary,
                             all_control_separation=all_controls,
                             smallest_retained_minus_largest_impaired=min(retained)-max(impaired)))
    return dict(analysis='Post-hoc sensitivity; does not replace the prespecified primary gate',
                model_window_comparisons=len(rows), primary_pass=sum(r['primary_ordering'] for r in rows),
                all_control_pass=sum(r['all_control_separation'] for r in rows),
                all_control_fail=sum(not r['all_control_separation'] for r in rows),
                negative_retained_scores=negative_retained, retained_scores=24,
                positive_impaired_scores=positive_impaired, impaired_scores=48,
                candidate_negative_scores=sum(r['scores']['N1002K']<0 for r in rows),
                rows=rows, independent_biological_replications=0,
                limitations=['One published engineered-control study; endpoint-specific labels.',
                            'D882A secondary label is reported in main text; supplement not independently verified.',
                            'Windows, related substitutions and models are dependent; no pooled p-value or accuracy estimate.',
                            'Negative score is not a pathogenicity or loss-of-function threshold.'])

def success_bounds(enrolled, success, lost):
    """Worst-case identification bounds, not confidence intervals or missing-at-random inference."""
    require(all(type(n) is int and n >= 0 for n in (enrolled,success,lost)), 'Invalid counts')
    require(enrolled > 0 and success + lost <= enrolled, 'Invalid denominator')
    return [success/enrolled, (success+lost)/enrolled]

def difference_bounds(control, treated):
    c = success_bounds(**control)
    t = success_bounds(**treated)
    return [t[0]-c[1], t[1]-c[0]]

def synthetic_examples():
    # Deliberately synthetic counterexamples, never an experiment or effect estimate.
    return dict(synthetic=True, biological_data=False,
        selection=dict(control=dict(enrolled=100,accurate_viable=60,error=20,death=10,arrest=5,lost=5),
                       treated=dict(enrolled=100,accurate_viable=40,error=5,death=20,arrest=25,lost=10),
                       error_among_completed=[20/80,5/45],
                       all_enrolled_success=[0.60,0.40],
                       difference_bounds=difference_bounds(dict(enrolled=100,success=60,lost=5),
                                                           dict(enrolled=100,success=40,lost=10))),
        missingness=dict(difference_bounds=difference_bounds(dict(enrolled=100,success=50,lost=10),
                                                            dict(enrolled=100,success=60,lost=25)),
                         interpretation='Bounds include no improvement; neither significance nor power follows.'))

def evaluate_advancement(gates):
    """Check adjudicated evidence completeness. Does not establish evidence truth or patient suitability."""
    require(set(gates) == GATES, 'Missing/unknown prerequisite')
    failed, missing = [], []
    for name, gate in sorted(gates.items()):
        require(set(gate) == {'status','evidence_kind','evidence_refs','rule_fixed_before_results'}, 'Gate schema drift')
        require(gate['status'] in {'met','failed','unknown'}, 'Unrecognized gate state')
        require(type(gate['rule_fixed_before_results']) is bool, 'Invalid lock state')
        require(isinstance(gate['evidence_refs'],list) and all(isinstance(x,str) and x.strip() for x in gate['evidence_refs']), 'Invalid evidence refs')
        if gate['status'] != 'unknown':
            require(bool(gate['evidence_refs']), 'An adjudicated result requires evidence')
            require(gate['evidence_kind'] in {'observed_relevant_context','justified_exposure_bounds','locked_protocol','source_audit'}, 'Model, proxy or planned evidence cannot satisfy a gate')
            if name in BIOLOGICAL:
                require(gate['evidence_kind']=='observed_relevant_context', 'Direct relevant biological evidence required')
            elif name == 'exposure_match':
                require(gate['evidence_kind'] in {'observed_relevant_context','justified_exposure_bounds'}, 'Exposure evidence required')
            elif name == 'hypothesis_lock':
                require(gate['evidence_kind']=='locked_protocol', 'Locked protocol required')
            elif name == 'source_integrity':
                require(gate['evidence_kind']=='source_audit', 'Source adjudication required')
        if gate['status'] == 'failed':
            failed.append(name)
        elif gate['status'] == 'unknown' or not gate['rule_fixed_before_results']:
            missing.append(name)
    decision = 'stop_tested_context' if failed else ('hold_unresolved' if missing else 'eligible_for_preclinical_review')
    return dict(decision=decision, failed=failed, unresolved=missing, clinical_recommendation=False)

def check_register(register):
    require(register['schema_version']==15 and register['clinical_recommendation'] is False, 'Register scope drift')
    claims = register['claims']
    ids = {c['id'] for c in claims}
    require(len(ids)==len(claims) and len(ids)>=16, 'Incomplete/duplicate claims')
    require({c['layer'] for c in claims} >= {'genetics','models','mechanism','measurement','exposure','safety','statistics','alternatives','delivery'}, 'Missing causal-chain layer')
    required = {'id','layer','claim','support','challenge','falsifier','stop_rule','reopen_rule','next_action','state','depends_on','evidence_refs'}
    for c in claims:
        require(set(c)==required, 'Claim schema drift')
        require(all(isinstance(c[k],str) and c[k].strip() for k in required-{'depends_on','evidence_refs'}), 'Empty claim adjudication')
        require(c['state'] in {'unresolved','inference_rejected','bounded_observation'}, 'Unsupported claim promotion')
        require(isinstance(c['depends_on'],list) and set(c['depends_on']) <= ids and c['id'] not in c['depends_on'], 'Invalid claim dependencies')
        require(isinstance(c['evidence_refs'],list) and bool(c['evidence_refs']), 'Unreferenced adjudication')
    by_id = {c['id']:c for c in claims}
    def visit(ident, trail):
        require(ident not in trail, 'Cyclic claim dependency')
        for dep in by_id[ident]['depends_on']:
            visit(dep,trail|{ident})
    for ident in ids:
        visit(ident,set())
    return evaluate_advancement(register['advancement_gates'])

def analyze():
    protein = ROOT/'notes/track2-latest-protein-results.json'
    register = ROOT/'notes/track2-falsification-register-v15.json'
    return dict(schema_version=15, input_hashes={str(p.relative_to(ROOT)):sha(p) for p in (protein,register,Path(__file__))},
                sequence=sequence_sensitivity(json.loads(protein.read_text())),
                synthetic_examples=synthetic_examples(),
                advancement=check_register(json.loads(register.read_text())),
                new_inference_performed=False, wet_lab_performed=False, clinical_exposure_margin=None)

def check():
    result=analyze()
    recorded=json.loads((ROOT/'notes/track2-falsification-analysis-v15.json').read_text())
    require(result==recorded, 'Falsification reanalysis drift')
    return dict(passed=True, claims=len(json.loads((ROOT/'notes/track2-falsification-register-v15.json').read_text())['claims']),
                primary_pass=result['sequence']['primary_pass'], sensitivity_fail=result['sequence']['all_control_fail'],
                advancement=result['advancement'], scope='Evidence consistency, not biological validation')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['analyze','check']);a=p.parse_args()
    print(json.dumps(analyze() if a.command=='analyze' else check(),indent=2,allow_nan=False))
