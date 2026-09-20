#!/usr/bin/env python3
"""Prespecified Boltz-2 single-sequence control comparison on public BUBR1."""
from __future__ import annotations
import argparse
import concurrent.futures
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import random
import subprocess
import time
from track2_esm_pilot import digest, parse_variant, write_json

ROOT = Path('/home/prachh/v/mva-track2-expanded-20260920')
UV = '/home/prachh/v/bin/uv'


def prepare(root):
    root = Path(root)
    plan_path = root/'inputs/plan.json'
    plan = json.loads(plan_path.read_text())
    fasta = root/'inputs/uniprot-O60566.fasta'
    if digest(fasta) != plan['reference_fasta_sha256']:
        raise ValueError('Public reference integrity mismatch')
    sequence = ''.join(fasta.read_text().splitlines()[1:])
    input_dir = root/'inputs/boltz'; input_dir.mkdir(exist_ok=False)
    variants = plan['structural_comparison']['variants']
    for variant in variants:
        altered = sequence
        if variant != 'WT':
            ref, pos, alt = parse_variant(variant, sequence)
            altered = sequence[:pos-1]+alt+sequence[pos:]
        # JSON is also YAML; avoids extra serializer dependency in the preparation step.
        write_json(input_dir/f'{variant}.yaml', {'version': 1, 'sequences': [
            {'protein': {'id': 'A', 'sequence': altered[720:1044], 'msa': 'empty'}}]})
    schedule = []
    for seed in plan['structural_comparison']['seeds']:
        order = list(variants); random.Random(seed).shuffle(order)
        schedule.extend({'variant': v, 'seed': seed} for v in order)
    write_json(root/'outputs/boltz-preregistration.json', {
        'created_utc': datetime.now(timezone.utc).isoformat(), 'schedule': schedule,
        'plan_sha256': digest(plan_path), 'script_sha256': digest(__file__),
        'inputs': {p.name: digest(p) for p in sorted(input_dir.glob('*.yaml'))},
        'uv_lock_sha256': digest(root/'boltz-env/uv.lock'),
        'interpretation': plan['structural_comparison']['interpretation']})


def fetch(root):
    import tarfile
    import urllib.request
    from boltz.main import MOL_URL, BOLTZ2_URL_WITH_FALLBACK, BOLTZ2_AFFINITY_URL_WITH_FALLBACK
    cache = root/'cache/boltz'; cache.mkdir(exist_ok=True, parents=True)
    sources = {'mols.tar': MOL_URL, 'boltz2_conf.ckpt': BOLTZ2_URL_WITH_FALLBACK[0],
               'boltz2_aff.ckpt': BOLTZ2_AFFINITY_URL_WITH_FALLBACK[0]}
    manifest = {}
    for name, url in sources.items():
        target = cache/name
        if target.exists():
            raise FileExistsError(target)
        started, size = time.monotonic(), 0
        with urllib.request.urlopen(url, timeout=120) as r, target.with_suffix('.part').open('xb') as f:
            expected = int(r.headers.get('Content-Length', 0))
            while chunk := r.read(8*1024*1024):
                size += len(chunk)
                if size > 12_000_000_000 or time.monotonic()-started > 3600:
                    raise ValueError('Resource retrieval exceeded fixed size/time bound')
                f.write(chunk)
        if expected and size != expected:
            raise ValueError('Incomplete resource download')
        target.with_suffix('.part').rename(target)
        manifest[name] = dict(url=url, bytes=size, sha256=digest(target))
        print(json.dumps({'downloaded': name, 'bytes': size}), flush=True)
    with tarfile.open(cache/'mols.tar') as tar:
        tar.extractall(cache, filter='data')
    write_json(root/'outputs/boltz-resources.json', manifest)


def run(root, gpus):
    schedule = json.loads((root/'outputs/boltz-preregistration.json').read_text())['schedule']
    # Each job has its own output directory and seed; no best-seed selection.
    def worker(gpu, jobs):
        statuses = []
        for job in jobs:
            variant, seed = job['variant'], job['seed']
            name = f'{variant}-seed{seed}'
            fields = subprocess.check_output(['nvidia-smi','-i',str(gpu),
                '--query-gpu=memory.used,utilization.gpu','--format=csv,noheader,nounits'],text=True).strip().split(',')
            if int(fields[0]) > 1000 or int(fields[1]) > 5:
                statuses.append(dict(**job,gpu=gpu,status='gpu_busy',snapshot=fields)); continue
            command = [UV,'run','--frozen','--project',str(root/'boltz-env'),'boltz','predict',
                str(root/f'inputs/boltz/{variant}.yaml'),'--out_dir',str(root/f'outputs/boltz/{name}'),
                '--cache',str(root/'cache/boltz'),'--devices','1','--accelerator','gpu',
                '--model','boltz2','--no_kernels','--seed',str(seed),'--recycling_steps','3',
                '--sampling_steps','200','--diffusion_samples','1','--num_workers','0',
                '--output_format','mmcif']
            started = time.monotonic()
            with (root/f'logs/boltz-{name}.log').open('x') as log:
                outcome = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                    env=dict(os.environ,CUDA_VISIBLE_DEVICES=str(gpu)))
            status = dict(**job,gpu=gpu,status='completed' if outcome.returncode == 0 else 'failed',
                          exit=outcome.returncode,elapsed_seconds=time.monotonic()-started,command=command)
            write_json(root/f'outputs/boltz-status-{name}.json',status)
            statuses.append(status); print(json.dumps(status),flush=True)
        return statuses
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(gpus)) as pool:
        futures = [pool.submit(worker,gpu,schedule[i::len(gpus)]) for i,gpu in enumerate(gpus)]
        statuses = [s for f in futures for s in f.result()]
    write_json(root/'outputs/boltz-worker-status.json',statuses)
    if any(s['status'] != 'completed' for s in statuses):
        raise RuntimeError('Incomplete structural comparison; retain all failures')


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('command',choices=['prepare','fetch','run'])
    p.add_argument('--root',type=Path,default=ROOT); p.add_argument('--gpus',type=int,nargs='+',default=[4,6,7])
    a=p.parse_args()
    if not str(a.root.resolve()).startswith('/home/prachh/v/mva-track2-expanded-'):
        raise ValueError('Unexpected remote root')
    if a.command=='prepare': prepare(a.root)
    elif a.command=='fetch': fetch(a.root)
    else: run(a.root,a.gpus)


if __name__=='__main__': main()
