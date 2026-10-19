#!/usr/bin/env python3
"""Finish post-hoc plate controls and package the completed public optical study."""
import argparse
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from track2_optical_fetch_v33 import hashes,write_json,MIN_FREE_BYTES


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    a=p.parse_args();root=a.root.resolve()
    if not root.is_relative_to('/home/prachh/v'):raise ValueError('All work stays under v')
    out=root/'outputs/finalize-v36-pipeline';out.mkdir(exist_ok=False)
    scripts=['track2_optical_plate_control_v36.py','track2_optical_package_v36.py',
             'track2_optical_model_v35.py','track2_optical_plate_v35.py','track2_optical_audit_v35.py',
             'track2_optical_prepare_v35.py','track2_optical_fetch_v33.py']
    bound={n:hashes(root/'scripts'/n)[1] for n in scripts}
    state=dict(pid=os.getpid(),started_utc=datetime.now(timezone.utc).isoformat())
    write_json(out/'registration.json',dict(**state,scripts=bound,script_sha256=hashes(Path(__file__))[1],
        plan_sha256=hashes(root/'inputs/plate-control-plan-v36.json')[1]))
    def status(stage):
        state.update(stage=stage,updated_utc=datetime.now(timezone.utc).isoformat());write_json(out/'status.json',state)
    def run(script,extra,logname):
        for n,digest in bound.items():
            if hashes(root/'scripts'/n)[1]!=digest:raise ValueError('Bound script changed: '+n)
        if shutil.disk_usage(root).free<MIN_FREE_BYTES:raise RuntimeError('Storage floor reached')
        status(script+' '+' '.join(extra))
        env=dict(os.environ,CUDA_VISIBLE_DEVICES='0',OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4',
                 CUBLAS_WORKSPACE_CONFIG=':4096:8',TMPDIR=str(root/'cache/tmp'))
        with (root/'logs'/logname).open('x') as log:
            subprocess.run([sys.executable,str(root/'scripts'/script),str(root),*extra],cwd=root,env=env,
                stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,check=True)
    try:
        previous=root/'outputs/secondary-v35-pipeline';deadline=time.monotonic()+6*3600
        while not (previous/'finished.json').is_file():
            if (previous/'failed.json').is_file():raise RuntimeError('Prior pipeline failed; no bypass')
            registration=json.loads((previous/'registration.json').read_text())
            proc=Path('/proc')/str(registration['pid'])
            if not proc.exists():
                if (previous/'finished.json').is_file():break
                raise RuntimeError('Prior pipeline disappeared before completion')
            if (proc/'cwd').resolve()!=root or b'track2_optical_finish_secondary_v35.py' not in (proc/'cmdline').read_bytes():
                raise RuntimeError('Prior pipeline PID identity changed')
            if time.monotonic()>deadline:raise RuntimeError('Wait deadline; no process stopped')
            status('await_registered_secondary_controls');time.sleep(30)
        if not json.loads((previous/'finished.json').read_text())['successful']:raise ValueError('Prior pipeline incomplete')
        deadline=time.monotonic()+1800
        while True:
            rows=subprocess.check_output(['nvidia-smi','--query-gpu=memory.used,utilization.gpu',
                '--format=csv,noheader,nounits'],text=True).strip().splitlines()
            if len(rows)==8 and all(int(r.split(',')[0])<=100 and int(r.split(',')[1])==0 for r in rows):break
            if time.monotonic()>deadline:raise RuntimeError('GPUs occupied; no process stopped')
            status('await_idle_gpus');time.sleep(30)
        for arm in ['mitotic','interphase']:
            run('track2_optical_plate_control_v36.py',['--arm',arm],'plate-control-v36-'+arm+'.log')
        run('track2_optical_package_v36.py',[],'package-optical-v36.log')
        status('finished_pending_local_replay_and_review')
        write_json(out/'finished.json',dict(**state,successful=True,biological_validation=False))
    except Exception as exc:
        status('failed_preserved_for_review')
        write_json(out/'failed.json',dict(**state,error_type=type(exc).__name__,error=str(exc)));raise


if __name__=='__main__':main()
