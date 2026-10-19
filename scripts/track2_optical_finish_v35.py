#!/usr/bin/env python3
"""Continue the existing public download into corrected, bounded validation.

Never restarts the downloader, accepts partial coverage, overwrites a completed
wave or stops another GPU process. All outputs remain under the authorized v root.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from track2_optical_fetch_v33 import hashes, write_json, MIN_FREE_BYTES

SCRIPTS=['track2_optical_prepare_v35.py','track2_optical_model_v35.py','track2_optical_run_v35.py',
         'track2_optical_audit_v35.py','track2_optical_independent_v35.py',
         'track2_optical_plate_v35.py','track2_optical_plate_run_v35.py']


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    p.add_argument('--downloader-pid',type=int,required=True);a=p.parse_args();root=a.root.resolve()
    if not root.is_relative_to('/home/prachh/v'):
        raise ValueError('All work must remain under v')
    out=root/'outputs/interphase-v35-pipeline';out.mkdir(exist_ok=False)
    bound={n:hashes(root/'scripts'/n)[1] for n in SCRIPTS}
    registration=dict(pid=os.getpid(),downloader_pid=a.downloader_pid,
        pipeline_script_sha256=hashes(Path(__file__))[1],
        started_utc=datetime.now(timezone.utc).isoformat(),script_hashes=bound,
        amendment_sha256=hashes(root/'inputs/amendment-v35.json')[1],
        maximum_new_storage_bytes=450000000000,minimum_free_bytes=MIN_FREE_BYTES,
        overwrites_allowed=False,stops_other_processes=False)
    write_json(out/'registration.json',registration)
    state=dict(stage='await_existing_download',started_utc=registration['started_utc'])
    def status(stage):
        state.update(stage=stage,updated_utc=datetime.now(timezone.utc).isoformat())
        write_json(out/'status.json',state)
    def disk_guard():
        used=sum(p.stat().st_size for p in root.rglob('*') if p.is_file() and not p.is_symlink())
        free=shutil.disk_usage(root).free
        state.update(campaign_bytes=used,free_bytes=free)
        if used>450000000000 or free<MIN_FREE_BYTES:
            raise RuntimeError('Registered storage limit reached; artifacts preserved')
    def idle_gpus():
        rows=subprocess.check_output(['nvidia-smi','--query-gpu=memory.used,utilization.gpu',
                                      '--format=csv,noheader,nounits'],text=True).strip().splitlines()
        return len(rows)==8 and all(int(v.split(',')[0])<=100 and int(v.split(',')[1])==0 for v in rows)
    def run(script,extra,logname,gpu=False):
        if gpu:
            deadline=time.monotonic()+1800
            while not idle_gpus():
                status('await_idle_gpus_for_'+script)
                if time.monotonic()>deadline:
                    raise RuntimeError('GPUs remained occupied; no process stopped')
                time.sleep(30)
        for n,digest in bound.items():
            if hashes(root/'scripts'/n)[1]!=digest:
                raise ValueError('Registered script changed: '+n)
        disk_guard();status(script)
        env=dict(os.environ,OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4',
                 TMPDIR=str(root/'cache/tmp'))
        cmd=[sys.executable,str(root/'scripts'/script),str(root),*extra]
        with (root/'logs'/logname).open('x') as log:
            subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,
                           stdin=subprocess.DEVNULL,check=True)
        disk_guard()
    try:
        deadline=time.monotonic()+6*3600
        complete=root/'outputs/download-interphase-complete.json'
        while not complete.is_file():
            progress=json.loads((root/'outputs/download-interphase-status.json').read_text())
            if progress['errors']:
                raise RuntimeError('Downloader reported errors; partial coverage prohibited')
            proc=Path('/proc')/str(a.downloader_pid)
            if not proc.exists() or not (proc/'cwd').resolve()==root:
                if complete.is_file():
                    break
                raise RuntimeError('Original downloader disappeared before completion')
            command=(proc/'cmdline').read_bytes().replace(b'\0',b' ').decode()
            if 'track2_optical_fetch_v33.py' not in command or '--arm interphase' not in command:
                raise RuntimeError('Downloader PID identity mismatch')
            if time.monotonic()>deadline:
                raise RuntimeError('Download wait deadline reached; no downloader restart')
            state['download_completed_files']=progress['completed'];status('await_existing_download')
            time.sleep(30)
        finished=json.loads(complete.read_text())
        if (finished['errors'] or finished['completed']!=3029 or
                finished['completed_bytes']!=321585666869):
            raise ValueError('Incomplete interphase source manifest')
        run('track2_optical_prepare_v35.py',['--arm','interphase','--workers','8'],'prepare-v35-interphase.log')
        run('track2_optical_independent_v35.py',['--arm','interphase'],'independent-v35-interphase.log')
        run('track2_optical_run_v35.py',['--arm','interphase'],'wave-v35-interphase.log',gpu=True)
        run('track2_optical_audit_v35.py',['summarize','--arm','interphase'],'audit-v35-interphase.log')
        run('track2_optical_plate_run_v35.py',['--arm','interphase'],'wave-plates-v35-interphase.log',gpu=True)
        status('finished_computation_pending_integrated_review')
        write_json(out/'finished.json',dict(**state,successful=True,biological_validation=False))
    except Exception as exc:
        status('failed_preserved_for_review')
        write_json(out/'failed.json',dict(**state,error_type=type(exc).__name__,error=str(exc)))
        raise


if __name__=='__main__':
    main()
