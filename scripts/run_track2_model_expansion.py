#!/usr/bin/env python3
"""Owner-authorized, bounded concurrent jobs; all work stays under ~/v."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
from datetime import datetime, timezone

ROOT = Path('/home/prachh/v/mva-track2-expanded-20260920')
PILOT = Path('/home/prachh/v/mva-track2-pilot-20260920')
UV = '/home/prachh/v/bin/uv'
MODELS = [f'esm1v_t33_650M_UR90S_{i}' for i in range(1, 6)]
ASSIGNMENTS = {2: MODELS[:2], 4: ['esm2_t36_3B_UR50D'],
               5: ['esm2_t48_15B_UR50D'], 6: MODELS[2:4], 7: MODELS[4:]}


def worker(gpu, models):
    statuses = []
    base = [UV, 'run', '--frozen', '--project', str(PILOT),
            'python', str(ROOT / 'scripts/track2_model_expansion.py')]
    for model in models:
        with (ROOT / f'logs/{model}.log').open('x') as log:
            fetch = subprocess.run(base + ['fetch', model, str(ROOT / 'cache/weights')],
                                   stdout=log, stderr=subprocess.STDOUT)
            if fetch.returncode:
                statuses.append({'model': model, 'stage': 'fetch', 'exit': fetch.returncode})
                continue
            fields = subprocess.check_output(['nvidia-smi', '-i', str(gpu),
                '--query-gpu=memory.used,utilization.gpu', '--format=csv,noheader,nounits'], text=True).strip().split(',')
            if int(fields[0]) > 1000 or int(fields[1]) > 5:
                statuses.append({'model': model, 'stage': 'gpu_busy', 'snapshot': fields})
                continue
            env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(gpu), HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1')
            command = base + ['run', model, '--plan', str(ROOT / 'inputs/plan.json'),
                '--fasta', str(ROOT / 'inputs/uniprot-O60566.fasta'), '--weights', str(ROOT / 'cache/weights'),
                '--out', str(ROOT / f'outputs/{model}')]
            run = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, env=env)
            statuses.append({'model': model, 'stage': 'inference', 'exit': run.returncode, 'gpu': gpu})
        print(json.dumps(statuses[-1]), flush=True)
    return statuses


if __name__ == '__main__':
    if Path.cwd() != ROOT:
        raise SystemExit('Enter isolated expansion root')
    paths = ['inputs/plan.json', 'inputs/uniprot-O60566.fasta',
        'scripts/track2_model_expansion.py', 'scripts/track2_esm_pilot.py',
        'scripts/run_track2_model_expansion.py', 'scripts/track2_expansion_env.sh']
    with (ROOT / 'outputs/preregistration.json').open('x') as f:
        json.dump({'created_utc': datetime.now(timezone.utc).isoformat(), 'assignments': ASSIGNMENTS,
            'sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
            'environment_lock_sha256': hashlib.sha256((PILOT/'uv.lock').read_bytes()).hexdigest()}, f, indent=2)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(worker, gpu, models) for gpu, models in ASSIGNMENTS.items()]
        statuses = [item for future in futures for item in future.result()]
    with (ROOT/'outputs/worker-status.json').open('x') as f:
        json.dump(statuses, f, indent=2)
    raise SystemExit(0 if all(x.get('exit') == 0 and x['stage'] == 'inference' for x in statuses) else 1)
