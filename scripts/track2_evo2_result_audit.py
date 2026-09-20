#!/usr/bin/env python3
"""Recompute Evo2 score arithmetic and verify the complete fixed design/provenance."""
import argparse
import json
import math
from pathlib import Path
from track2_evo2_comparison import functional_gate,validate_inputs
from track2_esm_pilot import digest,write_json
from track2_model_result_audit import same


def check_summary(result,document,plan):
    benchmark,candidates=validate_inputs(document,plan)
    rows=result['benchmark']+result['candidate_scores']
    if len(rows)!=100:raise ValueError('Incomplete comparison')
    expected={(r['id'],r['window']):r for r in benchmark+candidates}
    if len({(r['id'],r['window']) for r in rows})!=100:raise ValueError('Duplicate result')
    for r in rows:
        source=expected[(r['id'],r['window'])]
        for key in ['pos','ref','alt','group','assembly','window']:
            if r[key]!=source[key]:raise ValueError('Result/input identity mismatch')
        for key in ['reference_forward','alternate_forward','reference_reverse_complement','alternate_reverse_complement']:
            if not math.isfinite(r[key]):raise ValueError('Nonfinite likelihood')
        f=r['alternate_forward']-r['reference_forward']
        b=r['alternate_reverse_complement']-r['reference_reverse_complement']
        same([f,b,(f+b)/2],[r['delta_forward'],r['delta_reverse_complement'],r['delta_mean_strands']])
    same(functional_gate(result['benchmark']),result['benchmark_gate'])
    numerical=result['numerical_gate'];expected_loss={'evo2_7b':0.3476563,'evo2_40b':0.2159424}[result['model']]
    if (numerical['pass'] is not True or not math.isfinite(numerical['mean_loss']) or
        abs(numerical['mean_loss']-expected_loss)>=0.001 or
        not 0<=numerical['reference_repeat_abs_difference']<=1e-6 or
        result['candidate_inference_performed'] is not True):
        raise ValueError('Numerical qualification failed')
    for key in ['clinical_classification','drug_ranking_changed','phase_resolved']:
        if result[key] is not False:raise ValueError('Unjustified scientific promotion')
    return dict(model=result['model'],rows=100,benchmark_gate=result['benchmark_gate'],arithmetic_checked=True)


def audit(archive,output):
    root=Path(archive);repo=Path(__file__).resolve().parents[1]
    plan=json.loads((repo/'notes/track2-evo2-plan.json').read_text())
    doc=json.loads((root/'inputs/evo2-inputs.json').read_text())
    if doc['plan_sha256']!=digest(repo/'notes/track2-evo2-plan.json'):raise ValueError('Input/plan mismatch')
    if doc['script_sha256']!=digest(repo/'scripts/track2_evo2_resources.py'):raise ValueError('Resource script drift')
    checks=[]
    for model,attempt,env in [('evo2_7b','v1','track2_evo2'),('evo2_40b','cublas128v2','track2_evo2_fp8')]:
        base=root/f'outputs/{model}-run-{attempt}'
        if model=='evo2_40b':base=root/'outputs/evo2_40b-8gpu-long-v1'
        result=json.loads((base/'summary.json').read_text())
        same(result,json.loads((repo/f'notes/track2-evo2-{model.split("_")[1]}-results.json').read_text()))
        r=json.loads((base/'preregistration.json').read_text())
        if model=='evo2_40b':
            for path,sha in r['files'].items():
                actual=root/path
                if digest(actual)!=sha:raise ValueError('Continuation input/provenance drift')
                if path.startswith('scripts/') and digest(repo/path)!=sha:
                    raise ValueError('Published continuation script drift')
            if digest(repo/'notes/track2-evo2-memory-amendment.json')!=r['files']['inputs/evo2-memory-amendment.json']:
                raise ValueError('Memory amendment drift')
            prior=root/'outputs/evo2_40b-run-cublas128v2'
            if digest(prior/'benchmark.json')!=r['benchmark_sha256'] or digest(prior/'rows.jsonl')!=r['original_rows_sha256']:
                raise ValueError('Original partial run drift')
            same(result['benchmark'],json.loads((prior/'benchmark.json').read_text())['rows'])
            placement=json.loads((base/'placement-comparison.json').read_text())
            if placement['pass_gate'] is not True or max(placement['differences'].values())>1e-6:
                raise ValueError('Placement check failed')
            if not 0<=result['numerical_gate']['prior_reference_abs_difference']<=1e-6:
                raise ValueError('Reference changed with placement')
            r=json.loads((prior/'preregistration.json').read_text())
        for expected,path in [(r['plan_sha256'],repo/'notes/track2-evo2-plan.json'),
                              (r['inputs_sha256'],root/'inputs/evo2-inputs.json'),
                              (r['script_sha256'],repo/'scripts/track2_evo2_comparison.py'),
                              (r['environment_hashes']['pyproject.toml'],repo/f'scripts/{env}_environment.toml'),
                              (r['environment_hashes']['uv.lock'],repo/f'scripts/{env}.uv.lock')]:
            if expected!=digest(path):raise ValueError(f'Provenance mismatch: {path}')
        weights=json.loads((root/f'outputs/{model}-weights.json').read_text())
        same(r['checkpoint'],weights['merged'])
        same(result['numerical_gate'],json.loads((base/'numerical-repeat.json').read_text()))
        checks.append(check_summary(result,doc,plan))
    write_json(output,dict(passed=True,models=checks,protected_subject_inputs_used=False,
        limitation='Verifies provenance, design completeness and arithmetic; no new inference or clinical validation.'))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('archive');p.add_argument('output')
    a=p.parse_args();audit(a.archive,a.output)
