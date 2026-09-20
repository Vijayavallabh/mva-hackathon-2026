#!/usr/bin/env python3
"""Fixed all-eight-H100 continuation after 40B long-context OOM; retain earlier run."""
import json
import math
import os
from pathlib import Path
import subprocess
import time
from track2_esm_pilot import digest,write_json
from track2_evo2_comparison import ROOT,rc,validate_inputs,functional_gate


def run():
    import numpy as np
    import torch
    from evo2 import Evo2
    from evo2.test.test_evo2 import read_prompts,test_forward_pass
    if os.environ.get('CUDA_VISIBLE_DEVICES')!='0,1,2,3,4,5,6,7':raise ValueError('Require registered eight-device placement')
    for gpu in range(8):
        f=subprocess.check_output(['nvidia-smi','-i',str(gpu),'--query-gpu=memory.used,utilization.gpu','--format=csv,noheader,nounits'],text=True).strip().split(',')
        if int(f[0])>1000 or int(f[1])>5:raise RuntimeError('Device is busy')
    prior=ROOT/'outputs/evo2_40b-run-cublas128v2';out=ROOT/'outputs/evo2_40b-8gpu-long-v1';out.mkdir(exist_ok=False)
    plan=json.loads((ROOT/'inputs/evo2-plan.json').read_text());doc=json.loads((ROOT/'inputs/evo2-inputs.json').read_text())
    benchmark,candidates=validate_inputs(doc,plan)
    original=json.loads((prior/'benchmark.json').read_text());oldrows=[json.loads(x) for x in (prior/'rows.jsonl').read_text().splitlines()]
    if len(oldrows)!=97 or len(original['rows'])!=96:raise ValueError('Unexpected original result extent')
    weights=json.loads((ROOT/'outputs/evo2_40b-weights.json').read_text())
    if digest(weights['merged']['path'])!=weights['merged']['sha256']:raise ValueError('Weight drift')
    bound=['inputs/evo2-plan.json','inputs/evo2-inputs.json','inputs/evo2-memory-amendment.json',
        'scripts/track2_evo2_long_context.py','scripts/track2_evo2_comparison.py',
        'evo2-fp8-env/pyproject.toml','evo2-fp8-env/uv.lock',
        'outputs/evo2_40b-runtime-cublas128v2.json']
    write_json(out/'preregistration.json',dict(files={p:digest(ROOT/p) for p in bound},
        benchmark_sha256=digest(prior/'benchmark.json'),original_rows_sha256=digest(prior/'rows.jsonl'),
        visible_devices=os.environ['CUDA_VISIBLE_DEVICES'],checkpoint=weights['merged'],
        explicit_library_preload=os.environ['LD_PRELOAD']))
    torch.manual_seed(1);torch.cuda.manual_seed_all(1);np.random.seed(1);torch.set_num_threads(4)
    start=time.monotonic();model=Evo2('evo2_40b',local_path=weights['merged']['path'],use_kernels=False)
    accuracies,losses=test_forward_pass(model=model,sequences=read_prompts('prompts.csv'))
    numerical=dict(mean_loss=float(np.mean(losses)),expected_loss=0.2159424,tolerance=0.001,mean_accuracy=float(np.mean(accuracies)))
    numerical['pass']=math.isfinite(numerical['mean_loss']) and abs(numerical['mean_loss']-0.2159424)<0.001
    write_json(out/'upstream-self-test.json',numerical)
    if not numerical['pass']:raise ValueError('Official numerical test failed; stop')
    def score(seq):
        x=float(model.score_sequences([seq],batch_size=1,prepend_bos=False,reduce_method='mean')[0])
        if not math.isfinite(x):raise ValueError('Nonfinite score')
        return x
    value=score(benchmark[0]['ref_sequence']);repeat=score(benchmark[0]['ref_sequence'])
    numerical['reference_repeat_abs_difference']=abs(value-repeat)
    numerical['prior_reference_abs_difference']=abs(value-original['rows'][0]['reference_forward'])
    numerical['pass']=max(numerical['reference_repeat_abs_difference'],numerical['prior_reference_abs_difference'])<=1e-6
    write_json(out/'numerical-repeat.json',numerical)
    if not numerical['pass']:raise ValueError('Placement/repeat comparison failed; stop')
    rows=[]
    for row in candidates:
        r={k:v for k,v in row.items() if k not in ['ref_sequence','alt_sequence']}
        rf,af=score(row['ref_sequence']),score(row['alt_sequence'])
        rr,ar=score(rc(row['ref_sequence'])),score(rc(row['alt_sequence']))
        r.update(reference_forward=rf,alternate_forward=af,reference_reverse_complement=rr,
            alternate_reverse_complement=ar,delta_forward=af-rf,delta_reverse_complement=ar-rr,
            delta_mean_strands=((af-rf)+(ar-rr))/2)
        with (out/'rows.jsonl').open('a') as f:f.write(json.dumps(r,allow_nan=False)+'\n')
        rows.append(r)
        if len(rows)==1:
            differences={k:abs(r[k]-oldrows[-1][k]) for k in ['reference_forward','alternate_forward','reference_reverse_complement','alternate_reverse_complement']}
            write_json(out/'placement-comparison.json',dict(differences=differences,pass_gate=max(differences.values())<=1e-6))
            if max(differences.values())>1e-6:raise ValueError('Completed candidate differs across placement; stop')
    write_json(out/'summary.json',dict(model='evo2_40b',numerical_gate=numerical,
        benchmark_gate=functional_gate(original['rows']),benchmark=original['rows'],candidate_scores=rows,
        candidate_inference_performed=True,elapsed_seconds=time.monotonic()-start,
        peak_allocated_gib_per_visible_device=[torch.cuda.max_memory_allocated(i)/1024**3 for i in range(8)],
        precision='upstream required FP8; no opt-in inference kernels; isolated cuBLAS 12.8.4.1 preload',
        clinical_classification=False,drug_ranking_changed=False,phase_resolved=False,
        integration='96 benchmark rows from the numerically qualified two-GPU run; all four candidate rows from this eight-GPU continuation. Original OOM and duplicate short-window row preserved; placement checks <=1e-6.',
        interpretation='BRCA1 qualification is not BUB1B validation or clinical/drug-response evidence.'))


if __name__=='__main__':run()
