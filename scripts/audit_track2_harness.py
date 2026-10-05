#!/usr/bin/env python3
"""Run the combined review in a temporary public-only copy with Python audit guards.

This checks runtime dependencies, not biology or operating-system sandbox security.
The original repository is read only. No network or protected input is needed.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = r'''
import contextlib, io, json, os, pathlib, runpy, socket, subprocess, sys, time
root = pathlib.Path(__file__).resolve().parent
stdlib = pathlib.Path(sys.base_prefix).resolve()
sys.path.insert(0, str(root / 'scripts'))
def guard(event, args):
    if event.startswith('socket.') or event in {'subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn', 'os.fork'}:
        raise PermissionError('audit: network/process launch denied')
    if event in {'open', 'os.listdir', 'os.scandir'} and args and not isinstance(args[0], int):
        p = pathlib.Path(os.fsdecode(args[0])).resolve()
        if any(x in {'data', 'results', 'logs', '.git', '.env'} for x in p.parts):
            raise PermissionError('audit: protected path denied')
        if not (p.is_relative_to(root) or p.is_relative_to(stdlib)):
            raise PermissionError('audit: external path denied')
        if event == 'open' and len(args) > 2 and isinstance(args[2], int):
            if args[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC):
                raise PermissionError('audit: write denied')
sys.addaudithook(guard)
blocked = []
probes = {
    'network': lambda: socket.socket(),
    'process': lambda: subprocess.run([sys.executable, '-c', 'pass'], check=True),
    'protected_path': lambda: (root / 'data' / 'blocked-probe').read_bytes(),
    'credentials': lambda: (root / '.env').read_bytes(),
    'external_path': lambda: pathlib.Path('/etc/hosts').read_bytes(),
    'write': lambda: (root / 'blocked-write').write_text('blocked'),
}
for name, probe in probes.items():
    try:
        probe()
    except PermissionError:
        blocked.append(name)
    else:
        raise RuntimeError('Guard probe did not fail: ' + name)
captured = io.StringIO()
started = time.perf_counter()
with contextlib.redirect_stdout(captured):
    runpy.run_path(str(root / 'scripts/check_track2_harness.py'), run_name='__main__')
result = json.loads(captured.getvalue())
assert result['passed'] and result['research_addendum']['version'] == 19
assert result['presentation_version'] == 28 and result['harness_version'] == 29
assert result['rnai_addendum']['version'] == 23 and result['rnai_addendum']['passed']
assert result['crispr_addendum']['version'] == 25 and result['crispr_addendum']['passed']
assert result['falsification_addendum']['version'] == 27 and result['falsification_addendum']['passed']
assert result['orthogonal_addendum']['version'] == 29 and result['orthogonal_addendum']['passed']
assert sys.prefix == sys.base_prefix, 'Project environment unexpectedly active'
print(json.dumps(dict(passed=True, review=result, seconds=time.perf_counter()-started,
    blocked_probes=blocked, network_forbidden_by_audit_hook=True,
    data_results_logs_env_forbidden_by_audit_hook=True, writes_forbidden_by_audit_hook=True,
    process_launch_forbidden_by_audit_hook=True, project_environment_used=False,
    source_checkout_or_history_used=False), indent=2))
'''


def audit(root=ROOT):
    names = subprocess.check_output([
        'git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z', '--',
        'AGENTS.md', 'README.md', 'feature_list.json', 'session-handoff.md', 'notes', 'scripts',
    ], cwd=root).decode().split('\0')
    files = sorted(set(n for n in names if n))
    with tempfile.TemporaryDirectory(prefix='track2-public-harness-') as temporary:
        target = Path(temporary)
        for relative in files:
            p = Path(relative)
            if p.is_absolute() or '..' in p.parts or any((root/Path(*p.parts[:i])).is_symlink() for i in range(1,len(p.parts)+1)):
                raise ValueError('Unsafe public copy path: ' + relative)
            source = root / p
            if not source.is_file():
                raise ValueError('Missing public source: ' + relative)
            destination = target / p
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        (target / 'bootstrap.py').write_text(BOOTSTRAP)
        # The parent runs through uv; use its base interpreter to omit the project venv.
        python = str(Path(sys._base_executable).resolve())
        env = {'PATH': str(Path(python).parent), 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8'}
        started = time.perf_counter()
        child = subprocess.run([python, '-I', '-B', str(target/'bootstrap.py')],
                               cwd=target, env=env, text=True, capture_output=True, timeout=60)
        if child.returncode:
            raise RuntimeError('Isolated review failed:\n' + child.stderr)
        result = json.loads(child.stdout)
        result.update(copied_public_files=len(files), total_seconds=time.perf_counter()-started,
                      python_version=sys.version.split()[0], source_copy_created_without_git_history=True,
                      reviewer_sha256=hashlib.sha256((root/'scripts/check_track2_harness.py').read_bytes()).hexdigest())
        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        parser.error('Use a new output path')
    result = audit()
    content = json.dumps(result, indent=2) + '\n'
    if args.output:
        with args.output.open('x') as f:
            f.write(content)
    print(content, end='')
