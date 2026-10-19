#!/usr/bin/env python3
"""Finish registered optical controls after the existing pipeline releases its GPUs."""
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

SCRIPTS = ['track2_optical_median_v35.py', 'track2_optical_secondary_v35.py',
           'track2_optical_plate_summary_v35.py', 'track2_optical_model_v35.py',
           'track2_optical_audit_v35.py', 'track2_optical_prepare_v35.py',
           'track2_optical_fetch_v33.py']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--pipeline-pid', type=int, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_relative_to('/home/prachh/v'):
        raise ValueError('All work must stay under v')
    parent = root/'outputs/interphase-v36-pipeline'
    registration = json.loads((parent/'registration.json').read_text())
    if registration['pid'] != args.pipeline_pid:
        raise ValueError('Pipeline PID differs from original receipt')
    out = root/'outputs/secondary-v35-pipeline'
    out.mkdir(exist_ok=False)
    bound = {n: hashes(root/'scripts'/n)[1] for n in SCRIPTS}
    plans = {n: hashes(root/'inputs'/n)[1] for n in
             ['median-plan-v35.json', 'secondary-plan-v35.json']}
    state = dict(pid=os.getpid(), pipeline_pid=args.pipeline_pid,
                 started_utc=datetime.now(timezone.utc).isoformat())
    write_json(out/'registration.json', dict(**state, script_hashes=bound,
               plan_hashes=plans, supervisor_sha256=hashes(Path(__file__))[1],
               original_pipeline_registration_sha256=hashes(parent/'registration.json')[1]))

    def status(stage):
        state.update(stage=stage, updated_utc=datetime.now(timezone.utc).isoformat())
        write_json(out/'status.json', state)

    def guard():
        for n, digest in bound.items():
            if hashes(root/'scripts'/n)[1] != digest:
                raise ValueError('Registered script changed: '+n)
        for n, digest in plans.items():
            if hashes(root/'inputs'/n)[1] != digest:
                raise ValueError('Registered plan changed: '+n)
        used = sum(p.stat().st_size for p in root.rglob('*') if p.is_file() and not p.is_symlink())
        if used > 450000000000 or shutil.disk_usage(root).free < MIN_FREE_BYTES:
            raise RuntimeError('Storage limit reached; all outputs retained')

    def idle():
        rows = subprocess.check_output(['nvidia-smi', '--query-gpu=memory.used,utilization.gpu',
                                        '--format=csv,noheader,nounits'], text=True).strip().splitlines()
        return len(rows) == 8 and all(int(r.split(',')[0]) <= 100 and int(r.split(',')[1]) == 0 for r in rows)

    def run(script, extra, logname, gpu=False):
        if gpu:
            deadline = time.monotonic()+1800
            while not idle():
                status('await_idle_gpus_for_'+script)
                if time.monotonic() > deadline:
                    raise RuntimeError('GPUs occupied; no other process stopped')
                time.sleep(30)
        guard()
        status(script+' '+' '.join(extra))
        env = dict(os.environ, OMP_NUM_THREADS='4', OPENBLAS_NUM_THREADS='4',
                   CUBLAS_WORKSPACE_CONFIG=':4096:8', TMPDIR=str(root/'cache/tmp'))
        if script == 'track2_optical_secondary_v35.py':
            env['CUDA_VISIBLE_DEVICES'] = '0'
        with (root/'logs'/logname).open('x') as log:
            subprocess.run([sys.executable, str(root/'scripts'/script), str(root), *extra],
                           cwd=root, env=env, stdin=subprocess.DEVNULL,
                           stdout=log, stderr=subprocess.STDOUT, check=True)
        guard()

    try:
        deadline = time.monotonic()+6*3600
        while not (parent/'finished.json').is_file():
            if (parent/'failed.json').is_file():
                raise RuntimeError('Original pipeline failed; no restart or bypass')
            proc = Path('/proc')/str(args.pipeline_pid)
            if not proc.exists() or (proc/'cwd').resolve() != root:
                if (parent/'finished.json').is_file():
                    break
                raise RuntimeError('Original pipeline disappeared before completion')
            if 'track2_optical_finish_v36.py' not in (proc/'cmdline').read_bytes().decode():
                raise RuntimeError('Original pipeline PID identity mismatch')
            if time.monotonic() > deadline:
                raise RuntimeError('Wait deadline reached; no jobs stopped')
            status('await_existing_pipeline')
            time.sleep(30)
        if json.loads((parent/'finished.json').read_text())['successful'] is not True:
            raise ValueError('Pipeline did not succeed')
        run('track2_optical_plate_summary_v35.py', ['--arm', 'interphase'], 'plate-summary-v35-interphase.log')
        run('track2_optical_median_v35.py', ['run', '--arm', 'interphase'], 'median-v35-interphase.log', gpu=True)
        for arm in ['mitotic', 'interphase']:
            run('track2_optical_secondary_v35.py', ['--arm', arm], 'secondary-v35-'+arm+'.log', gpu=True)
        status('finished_controls_pending_integrated_review')
        write_json(out/'finished.json', dict(**state, successful=True, biological_validation=False))
    except Exception as exc:
        status('failed_preserved_for_review')
        write_json(out/'failed.json', dict(**state, error_type=type(exc).__name__, error=str(exc)))
        raise


if __name__ == '__main__':
    main()
