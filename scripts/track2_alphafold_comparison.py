#!/usr/bin/env python3
"""AlphaFold2/ColabFold fixed cross-model comparison; all outputs retained."""
import argparse
import concurrent.futures
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from track2_esm_pilot import digest, write_json

ROOT=Path('/home/prachh/v/mva-track2-expanded-20260920')
UV='/home/prachh/v/bin/uv'


def download():
    from colabfold.download import download_alphafold_params
    dest=ROOT/'cache/alphafold'
    download_alphafold_params('alphafold2_ptm', dest)
    files=sorted(dest.glob('params/params_model_*_ptm.npz'))
    if len(files)!=5:raise ValueError('Expected all five AlphaFold2 pTM parameter files')
    write_json(ROOT/'outputs/alphafold-weights.json',{
        'model':'AlphaFold2 pTM; all five parameter sets',
        'files':{str(p.relative_to(dest)):dict(bytes=p.stat().st_size,sha256=digest(p)) for p in files}})


def prepare():
    plan=json.loads((ROOT/'inputs/alphafold-plan.json').read_text())
    inputs=ROOT/'inputs/alphafold';inputs.mkdir(exist_ok=False)
    variants=plan['variants']
    for i in range(2):
        dest=inputs/f'batch{i}';dest.mkdir()
        for variant in variants[i::2]:
            shutil.copyfile(ROOT/f'msa-arm/inputs/msa/{variant}.a3m',dest/f'{variant}.a3m')
    write_json(ROOT/'outputs/alphafold-preregistration.json',{
        'created_utc':datetime.now(timezone.utc).isoformat(),
        'plan_sha256':digest(ROOT/'inputs/alphafold-plan.json'),'script_sha256':digest(__file__),
        'lock_sha256':digest(ROOT/'alphafold-env/uv.lock'),
        'inputs':{str(p.relative_to(ROOT)):digest(p) for p in sorted(inputs.glob('*/*.a3m'))}})


def run():
    def worker(batch,gpu):
        fields=subprocess.check_output(['nvidia-smi','-i',str(gpu),
            '--query-gpu=memory.used,utilization.gpu','--format=csv,noheader,nounits'],text=True).strip().split(',')
        if int(fields[0])>1000 or int(fields[1])>5:raise RuntimeError('Selected GPU is busy')
        command=[UV,'run','--frozen','--project',str(ROOT/'alphafold-env'),'colabfold_batch',
            str(ROOT/f'inputs/alphafold/batch{batch}'),str(ROOT/f'outputs/alphafold/batch{batch}'),
            '--model-type','alphafold2_ptm','--num-models','5','--num-seeds','3','--random-seed','11',
            '--num-recycle','3','--recycle-early-stop-tolerance','0.0',
            '--data',str(ROOT/'cache/alphafold'),'--disable-unified-memory']
        env=dict(os.environ,CUDA_VISIBLE_DEVICES=str(gpu),
            XLA_PYTHON_CLIENT_PREALLOCATE='false',JAX_COMPILATION_CACHE_DIR=str(ROOT/f'cache/jax-gpu{gpu}'))
        started=time.monotonic()
        with (ROOT/f'logs/alphafold-batch{batch}.log').open('x') as log:
            r=subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT)
        status=dict(batch=batch,gpu=gpu,command=command,exit=r.returncode,elapsed_seconds=time.monotonic()-started)
        write_json(ROOT/f'outputs/alphafold-status-batch{batch}.json',status)
        return status
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(worker,i,gpu) for i,gpu in enumerate([6,7])]
        results=[f.result() for f in futures]
    write_json(ROOT/'outputs/alphafold-worker-status.json',results)
    if any(r['exit'] for r in results):raise RuntimeError('AlphaFold comparison incomplete')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['download','prepare','run']);a=p.parse_args()
    {'download':download,'prepare':prepare,'run':run}[a.command]()
