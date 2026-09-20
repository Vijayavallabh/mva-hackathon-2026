#!/usr/bin/env python3
"""Evo2 20B comparison using the unchanged public benchmark, with pinned current source."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import statistics
import time
from track2_esm_pilot import digest, write_json

ROOT=Path('/home/prachh/v/mva-track2-expanded-latest-20260921')


def rc(sequence):
    if set(sequence)-set('ACGT'):raise ValueError('Expected unambiguous public-reference DNA')
    return sequence.translate(str.maketrans('ACGT','TGCA'))[::-1]


def functional_gate(rows):
    if len(rows)!=96 or len({r['id'] for r in rows})!=96:
        raise ValueError('Require the full fixed 96-site benchmark')
    loss=[r['delta_mean_strands'] for r in rows if r['group']=='LOF']
    retained=[r['delta_mean_strands'] for r in rows if r['group']=='FUNC']
    if len(loss)!=48 or len(retained)!=48 or not all(map(math.isfinite,loss+retained)):
        raise ValueError('Incomplete/nonfinite functional benchmark')
    auc=sum((a<b)+0.5*(a==b) for a in loss for b in retained)/(len(loss)*len(retained))
    medians={'LOF':statistics.median(loss),'FUNC':statistics.median(retained)}
    return dict(auroc_negative_delta=auc,median_delta=medians,
                pass_gate=auc>=0.70 and medians['LOF']<medians['FUNC'])


def validate_inputs(document, plan):
    rows=document['rows'];benchmark=[r for r in rows if r['group']!='candidate']
    candidate=[r for r in rows if r['group']=='candidate']
    if len(benchmark)!=96 or len({r['pos'] for r in benchmark})!=96 or len(candidate)!=4:
        raise ValueError('Incomplete/duplicated fixed design')
    if (sum(r['group']=='FUNC' for r in benchmark)!=48 or sum(r['group']=='LOF' for r in benchmark)!=48
        or any(r['window']!=8192 for r in benchmark)):
        raise ValueError('Unregistered benchmark class/window')
    expected={(c['id'],c['pos'],c['ref'],c['alt'],w) for c in plan['candidates'] for w in plan['candidate_windows']}
    observed={(r['id'],r['pos'],r['ref'],r['alt'],r['window']) for r in candidate}
    if observed!=expected:raise ValueError('Unregistered candidate')
    for r in rows:
        ref,alt=r['ref_sequence'],r['alt_sequence'];i=r['window']//2
        if len(ref)!=r['window'] or len(alt)!=len(ref) or set(ref+alt)-set('ACGT'):
            raise ValueError('Unexpected sequence/window')
        if ref[i]!=r['ref'] or alt[i]!=r['alt'] or ref[:i]!=alt[:i] or ref[i+1:]!=alt[i+1:] or ref[i]==alt[i]:
            raise ValueError('Reference/alternate must differ only at the prescribed center')
        if r['assembly']!=('GRCh38' if r['group']=='candidate' else 'GRCh37'):
            raise ValueError('Assembly mismatch')
    return benchmark,candidate


def run(name,out):
    import os
    import importlib.metadata
    import numpy as np
    import torch
    import sys
    sys.path.insert(0, str(ROOT/'source/evo2'))
    from evo2 import Evo2
    from evo2.test.test_evo2 import read_prompts, test_forward_pass
    if name not in ['evo2_20b']:raise ValueError('Unregistered model')
    plan_path=ROOT/'inputs/evo2-plan.json';input_path=ROOT/'inputs/evo2-inputs.json'
    plan=json.loads(plan_path.read_text());document=json.loads(input_path.read_text())
    if document['plan_sha256']!=digest(plan_path):raise ValueError('Plan/input binding mismatch')
    benchmark,candidates=validate_inputs(document,plan)
    weights=json.loads((ROOT/f'outputs/{name}-weights.json').read_text())
    path=Path(weights['merged']['path'])
    if digest(path)!=weights['merged']['sha256']:raise ValueError('Checkpoint integrity mismatch')
    out=Path(out);out.mkdir(exist_ok=False,parents=True)
    packages={p:importlib.metadata.version(p) for p in ['evo2','vtx','torch','flash-attn','numpy']}
    if name=='evo2_20b':
        packages.update({p:importlib.metadata.version(p) for p in ['transformer-engine','transformer-engine-torch']})
    env=ROOT.parent/'mva-track2-expanded-20260920/evo2-fp8-env'
    write_json(out/'preregistration.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),
        plan_sha256=digest(plan_path),inputs_sha256=digest(input_path),script_sha256=digest(__file__),
        checkpoint=weights['merged'],checkpoint_repository_revision=weights['revision'],packages=packages,
        environment_hashes={p:digest(env/p) for p in ['pyproject.toml','uv.lock']},
        cuda=torch.version.cuda,cudnn=torch.backends.cudnn.version(),
        visible_devices=os.environ.get('CUDA_VISIBLE_DEVICES'),generation_requested=False,
        current_evo_source_revision='53f195997257c56c00e5ef8d33a54f5baad143a6',
        previous_environment_reused_without_mutation=True))
    torch.manual_seed(1);torch.cuda.manual_seed_all(1);np.random.seed(1)
    torch.set_num_threads(4)
    started=time.monotonic()
    model=Evo2(name,local_path=str(path),use_kernels=False)
    accuracies,losses=test_forward_pass(model=model,sequences=read_prompts('prompts.csv'))
    mean_loss=float(np.mean(losses));expected={'evo2_20b':0.2166748046875}[name]
    numerical={'mean_loss':mean_loss,'expected_loss':expected,'tolerance':0.001,
        'mean_accuracy':float(np.mean(accuracies)),'pass':math.isfinite(mean_loss) and abs(mean_loss-expected)<0.001}
    write_json(out/'upstream-self-test.json',numerical)
    if not numerical['pass']:
        write_json(out/'summary.json',{'model':name,'decision':'stop_numerical_test_failed','numerical_gate':numerical,
                                      'candidate_inference_performed':False})
        return
    cache={}
    def score(seq):
        if seq not in cache:
            value=float(model.score_sequences([seq],batch_size=1,prepend_bos=False,reduce_method='mean')[0])
            if not math.isfinite(value):raise ValueError('Nonfinite sequence likelihood')
            cache[seq]=value
        return cache[seq]
    reference=benchmark[0]['ref_sequence']
    value=score(reference)
    repeat=float(model.score_sequences([reference],batch_size=1,prepend_bos=False,reduce_method='mean')[0])
    numerical['reference_repeat_abs_difference']=abs(value-repeat)
    numerical['pass']=math.isfinite(repeat) and abs(value-repeat)<=1e-6
    write_json(out/'numerical-repeat.json',numerical)
    if not numerical['pass']:
        write_json(out/'summary.json',{'model':name,'decision':'stop_repeat_test_failed','numerical_gate':numerical,
                                      'candidate_inference_performed':False})
        return
    def score_row(row):
        reference,alternate=row['ref_sequence'],row['alt_sequence']
        rf,af=score(reference),score(alternate);rr,ar=score(rc(reference)),score(rc(alternate))
        result={k:v for k,v in row.items() if k not in ['ref_sequence','alt_sequence']}
        result.update(reference_forward=rf,alternate_forward=af,reference_reverse_complement=rr,
            alternate_reverse_complement=ar,delta_forward=af-rf,delta_reverse_complement=ar-rr,
            delta_mean_strands=((af-rf)+(ar-rr))/2)
        with (out/'rows.jsonl').open('a') as f:f.write(json.dumps(result,allow_nan=False)+'\n')
        return result
    rows=[score_row(r) for r in benchmark]
    gate=functional_gate(rows)
    write_json(out/'benchmark.json',dict(rows=rows,gate=gate))
    candidate_rows=[score_row(r) for r in candidates]
    write_json(out/'summary.json',dict(model=name,numerical_gate=numerical,benchmark_gate=gate,
        benchmark=rows,candidate_scores=candidate_rows,candidate_inference_performed=True,
        elapsed_seconds=time.monotonic()-started,
        peak_allocated_gib_per_visible_device=[torch.cuda.max_memory_allocated(i)/1024**3 for i in range(torch.cuda.device_count())],
        precision='upstream configured BF16/required FP8; no opt-in inference kernels',
        clinical_classification=False,drug_ranking_changed=False,phase_resolved=False,
        interpretation='BRCA1 assay qualification is not validation in BUB1B; failed controls and all strands/windows/models remain visible. Scores are not clinical probabilities or drug-response measurements.'))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('model');p.add_argument('out');a=p.parse_args();run(a.model,a.out)
