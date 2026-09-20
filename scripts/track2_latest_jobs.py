#!/usr/bin/env python3
"""Launch fixed current-model jobs on checked idle devices, retaining command and exit."""
import argparse
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import subprocess
import time
from track2_esm_pilot import digest,write_json

ROOT=Path('/home/prachh/v/mva-track2-expanded-latest-20260921')
OLD=ROOT.parent/'mva-track2-expanded-20260920'
UV='/home/prachh/v/bin/uv'


def launch(label,devices,command,extra=None):
    for gpu in devices:
        for attempt in range(7):
            values=subprocess.check_output(['nvidia-smi','-i',str(gpu),'--query-gpu=memory.used,utilization.gpu','--format=csv,noheader,nounits'],text=True).strip().split(',')
            if int(values[0])<=1000 and int(values[1])<=5:
                break
            if attempt<6:
                time.sleep(5)  # GPU-utilization sampling can lag a completed owned job.
        else:
            raise RuntimeError(f'Required GPU {gpu} is busy; do not disturb its job')
    env=dict(os.environ,CUDA_VISIBLE_DEVICES=','.join(map(str,devices)),HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',PYTHONUNBUFFERED='1')
    env.update(extra or {})
    record=dict(label=label,devices=devices,command=command,created_utc=datetime.now(timezone.utc).isoformat(),
        launcher_sha256=digest(__file__),plan_sha256=digest(ROOT/'inputs/latest-plan.json'))
    write_json(ROOT/'outputs'/(label+'-launch.json'),record)
    start=time.monotonic()
    with (ROOT/'logs'/(label+'.log')).open('x') as out:
        result=subprocess.run(command,cwd=ROOT,env=env,stdout=out,stderr=subprocess.STDOUT)
    write_json(ROOT/'outputs'/(label+'-status.json'),dict(record,exit=result.returncode,elapsed_seconds=time.monotonic()-start))
    if result.returncode:
        raise RuntimeError(f'{label} failed; see retained log')


def af3():
    launch('AlphaFold3-run',[7],[UV,'run','--frozen','--project',str(ROOT/'envs/af3'),'python',str(ROOT/'source/alphafold3/run_alphafold.py'),
        '--input_dir='+str(ROOT/'inputs/af3'),'--output_dir='+str(ROOT/'outputs/AlphaFold3'),
        '--model_dir='+str(ROOT/'cache/alphafold3'),'--run_data_pipeline=false',
        '--num_recycles=10','--num_diffusion_samples=5','--buckets=384',
        '--jax_compilation_cache_dir='+str(ROOT/'cache/jax-af3')],{'XLA_PYTHON_CLIENT_PREALLOCATE':'false'})


def protein():
    jobs=[('score','biohub/'+m,m+'-score',None) for m in ['ESMC-300M','ESMC-600M','ESMC-6B']]
    jobs += [('score','EvolutionaryScale/esm3-sm-open-v1','ESM3-score',None),
             ('fold','EvolutionaryScale/esm3-sm-open-v1','ESM3-fold',None),
             ('fold','biohub/ESMFold2','ESMFold2-single_sequence','single_sequence'),
             ('fold','biohub/ESMFold2','ESMFold2-shared_msa','shared_msa')]
    for cmd,repo,label,arm in jobs:
        if (ROOT/'outputs'/label/'summary.json').exists():
            print('Preserved completed '+label,flush=True)
            continue
        command=[UV,'run','--frozen','--project',str(ROOT/'envs/esm'),'python',str(ROOT/'scripts/track2_latest_protein.py'),cmd,repo,label]
        if arm:command+=['--arm',arm]
        launch(label+'-run',[6],command)


def evo():
    plan=json.loads((ROOT/'inputs/latest-plan.json').read_text())['evo2']
    write_json(ROOT/'inputs/evo2-plan.json',plan)
    document=json.loads((ROOT/'inputs/evo2-inputs-v1.json').read_text())
    document['previous_plan_sha256']=document['plan_sha256']
    document['plan_sha256']=digest(ROOT/'inputs/evo2-plan.json')
    write_json(ROOT/'inputs/evo2-inputs.json',document)
    weights=json.loads((ROOT/'outputs/arcinstitute_evo2_20b-weights.json').read_text())
    row=next(r for r in weights['files'] if r['name']=='evo2_20b.pt')
    weights['merged']=dict(path=str(ROOT/'cache/models/arcinstitute_evo2_20b/evo2_20b.pt'),bytes=row['bytes'],sha256=row['sha256'])
    write_json(ROOT/'outputs/evo2_20b-weights.json',weights)
    launch('Evo2-20B-run',[2,3],[UV,'run','--frozen','--project',str(OLD/'evo2-fp8-env'),'python',str(ROOT/'scripts/track2_evo2_20b_comparison.py'),
        'evo2_20b',str(ROOT/'outputs/Evo2-20B')],
        {'LD_LIBRARY_PATH':str(OLD/'evo2-fp8-env/.venv/lib/python3.11/site-packages/nvidia/cudnn/lib'),
         'LD_PRELOAD':':'.join(str(OLD/'cublas-compat-env/.venv/lib/python3.11/site-packages/nvidia/cublas/lib'/name) for name in ['libcublasLt.so.12','libcublas.so.12'])})


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['af3','protein','evo']);a=p.parse_args()
    {'af3':af3,'protein':protein,'evo':evo}[a.command]()
