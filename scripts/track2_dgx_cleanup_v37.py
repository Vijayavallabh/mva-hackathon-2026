#!/usr/bin/env python3
"""Owner-authorized removal of reproducible uv installer caches from completed MVA jobs.

Never touches inputs, outputs, models, checkpoints, logs, Python interpreters,
environments, shared caches or other projects. Run with the owner's uv on the DGX.
"""
import argparse
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import subprocess

BASE=Path('/home/prachh/v')
PROJECTS=['mva-track2-pilot-20260920','mva-track2-expanded-20260920',
          'mva-track2-orthogonal-20261006-v29','mva-track2-optical-20261019-v33']


def disk_bytes(path):
    return int(subprocess.check_output(['du','-s','-B1',str(path)],text=True).split()[0]) if path.exists() else 0


def inventory():
    if Path.home()!=Path('/home/prachh') or BASE.resolve()!=BASE:
        raise ValueError('Run only in the authorized DGX account/root')
    targets=[BASE/p/'cache/uv' for p in PROJECTS]
    for t in targets:
        if not t.is_dir() or any(p.is_symlink() for p in [BASE,t.parent.parent,t.parent,t]):
            raise ValueError('Missing or symlinked cache')
    # Refuse deletion if a retained symbolic link depends on an installer cache.
    dependencies=[]
    for project in PROJECTS:
        for root,dirs,files in os.walk(BASE/project,followlinks=False):
            dirs[:]=[d for d in dirs if Path(root)/d not in targets]
            for name in dirs+files:
                path=Path(root)/name
                if path.is_symlink():
                    resolved=path.resolve()
                    if any(resolved.is_relative_to(t) for t in targets):dependencies.append(str(path))
    if dependencies:raise ValueError('Retained symlink depends on installer cache: '+str(dependencies[:5]))
    # Check open files and mapped shared libraries without printing process arguments.
    users=[]
    for p in Path('/proc').iterdir():
        if not p.name.isdigit() or int(p.name)==os.getpid():continue
        try:
            if p.stat().st_uid!=os.getuid():continue
            refs=[]
            for fd in (p/'fd').iterdir():
                try:refs.append(str(fd.resolve()))
                except OSError:pass
            refs.extend((p/'maps').read_text().splitlines())
            if any(str(t) in r for r in refs for t in targets):users.append(int(p.name))
        except (FileNotFoundError,ProcessLookupError,PermissionError):continue
    if users:raise ValueError('Caches still in use by processes: '+str(users))
    return targets


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    targets=inventory();record=dict(time_utc=datetime.now(timezone.utc).isoformat(),applied=args.apply,
        authorization='Owner requested deletion of unwanted DGX files during Track 2 work.',
        scope='Four completed MVA project uv installer caches only',targets=[])
    for t in targets:
        row=dict(path=str(t),before_allocated_bytes=disk_bytes(t))
        if args.apply:
            run=subprocess.run([str(BASE/'bin/uv'),'cache','clean','--cache-dir',str(t)],text=True,capture_output=True)
            row.update(exit_code=run.returncode,message=run.stderr.strip())
            if run.returncode:raise RuntimeError('Cache cleanup failed: '+str(t))
        row['after_allocated_bytes']=disk_bytes(t)
        record['targets'].append(row)
    record['allocated_bytes_removed']=sum(r['before_allocated_bytes']-r['after_allocated_bytes'] for r in record['targets'])
    record['limits']='Allocated cache bytes removed are not a measurement of filesystem space gained; hard links and other concurrent work affect that.'
    print(json.dumps(record,indent=2))


if __name__=='__main__':main()
