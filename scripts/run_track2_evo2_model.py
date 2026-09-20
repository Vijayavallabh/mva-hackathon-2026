#!/usr/bin/env python3
"""Run one fixed Evo2 comparison on checked idle devices, retaining exit status."""
import argparse
from datetime import datetime,timezone
import os
from pathlib import Path
import subprocess
import time
from track2_esm_pilot import write_json

ROOT=Path('/home/prachh/v/mva-track2-expanded-20260920')
UV='/home/prachh/v/bin/uv'


def run(model,attempt):
    if model not in ['evo2_7b','evo2_40b'] or not attempt.isalnum():raise ValueError('Invalid run identity')
    devices=[5] if model=='evo2_7b' else [2,4]
    for gpu in devices:
        fields=subprocess.check_output(['nvidia-smi','-i',str(gpu),
            '--query-gpu=memory.used,utilization.gpu','--format=csv,noheader,nounits'],text=True).strip().split(',')
        if int(fields[0])>1000 or int(fields[1])>5:raise RuntimeError(f'GPU {gpu} is busy')
    name=f'{model}-run-{attempt}';project='evo2-env' if model=='evo2_7b' else 'evo2-fp8-env'
    command=[UV,'run','--frozen','--project',str(ROOT/project),'python',
             str(ROOT/'scripts/track2_evo2_comparison.py'),model,str(ROOT/'outputs'/name)]
    env=dict(os.environ,CUDA_VISIBLE_DEVICES=','.join(map(str,devices)),
             HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',PYTHONUNBUFFERED='1')
    if model=='evo2_40b':
        cudnn=ROOT/'evo2-fp8-env/.venv/lib/python3.11/site-packages/nvidia/cudnn/lib'
        env['LD_LIBRARY_PATH']=str(cudnn)+(':'+env['LD_LIBRARY_PATH'] if env.get('LD_LIBRARY_PATH') else '')
    started=time.monotonic();timestamp=datetime.now(timezone.utc).isoformat()
    with (ROOT/'logs'/f'{name}.log').open('x') as log:
        result=subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT,cwd=ROOT)
    write_json(ROOT/'outputs'/f'{name}-status.json',dict(command=command,devices=devices,
        created_utc=timestamp,exit=result.returncode,elapsed_seconds=time.monotonic()-started))
    raise SystemExit(result.returncode)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('model');p.add_argument('attempt')
    a=p.parse_args();run(a.model,a.attempt)
