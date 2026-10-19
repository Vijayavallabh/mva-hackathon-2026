#!/usr/bin/env python3
"""Supervise the eight registered public-data workers; record exits and GPU use."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('root', type=Path)
    p.add_argument('--arm', choices=['mitotic', 'interphase'], required=True)
    a = p.parse_args()
    root = a.root.resolve()
    if not root.is_relative_to('/home/prachh/v'):
        raise ValueError('All campaign work must stay under the authorized v directory')
    if not (root/'models-v35'/f'{a.arm}-3301-real'/'complete.json').is_file():
        raise ValueError('Model fitting must be complete before launch')
    command = ['nvidia-smi', '--query-gpu=index,uuid,memory.used,utilization.gpu',
               '--format=csv,noheader,nounits']
    initial = subprocess.check_output(command, text=True).strip().splitlines()
    devices = [line.split(',') for line in initial]
    if len(devices) != 8 or any(int(d[2]) > 100 or int(d[3]) != 0 for d in devices):
        raise ValueError('Eight idle GPUs required; no existing process will be stopped')
    out = root/'outputs'/('wave-plates-v35-'+a.arm)
    out.mkdir(exist_ok=False)
    script = root/'scripts/track2_optical_plate_v35.py'
    workers, handles = [], []
    for gpu in range(8):
        seed = 3301 + gpu % 4
        shuffled = gpu >= 4
        label = f'{a.arm}-{seed}-' + ('shuffled' if shuffled else 'real')
        cmd = [sys.executable, str(script), str(root), '--arm', a.arm, '--seed', str(seed)]
        if shuffled:
            cmd.append('--shuffled')
        env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(gpu),
                   CUBLAS_WORKSPACE_CONFIG=':4096:8', OMP_NUM_THREADS='4',
                   OPENBLAS_NUM_THREADS='4', TORCHINDUCTOR_CACHE_DIR=str(root/'cache/torch'),
                   TRITON_CACHE_DIR=str(root/'cache/triton'))
        log = open(root/'logs'/('plate-v35-'+label+'.log'), 'x')
        handles.append(log)
        proc = subprocess.Popen(cmd, cwd=root, env=env, stdout=log,
                                stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        workers.append((proc, dict(gpu=gpu, uuid=devices[gpu][1].strip(), seed=seed,
                                  shuffled=shuffled, label=label, pid=proc.pid, command=cmd)))
    registration = dict(started_utc=datetime.now(timezone.utc).isoformat(),
                        model_script_sha256=hashlib.sha256(script.read_bytes()).hexdigest(),
                        workers=[record for _, record in workers])
    (out/'registration.json').write_text(json.dumps(registration, indent=2)+'\n')
    with (out/'gpu-monitor.jsonl').open('x') as monitor:
        while True:
            status = dict(utc=datetime.now(timezone.utc).isoformat(),
                          workers=[dict(record, returncode=proc.poll()) for proc, record in workers])
            (out/'status.json').write_text(json.dumps(status, indent=2)+'\n')
            monitor.write(json.dumps(dict(utc=status['utc'],
                gpu=subprocess.check_output(command, text=True).strip().splitlines()))+'\n')
            monitor.flush()
            if all(proc.poll() is not None for proc, _ in workers):
                break
            time.sleep(10)
    for handle in handles:
        handle.close()
    status['successful'] = all(proc.returncode == 0 and
        (root/'plate-v35'/record['label']/'complete.json').is_file() for proc, record in workers)
    (out/'finished.json').write_text(json.dumps(status, indent=2)+'\n')
    print(json.dumps(status), flush=True)
    if not status['successful']:
        raise SystemExit('At least one worker failed; retained outputs require review')


if __name__ == '__main__':
    main()
