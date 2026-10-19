#!/usr/bin/env python3
"""Bind local demo checks, browser receipts and an isolated, minimal-kit replay."""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
import audit_track2_public_v37 as isolation
import track2_community_kit_v37 as kit
import test_track2_demo_v37 as tests

ROOT=kit.ROOT
SOURCES=kit.FILES+[
    'notes/track2-demo-template-v37.html','notes/track2-teleprompter-v37.html',
    'notes/track2-pitch-v37.md','scripts/track2_demo_v37.js',
    'scripts/build_track2_demo_v37.py','scripts/build_track2_recording_v37.py',
    'scripts/review_track2_interactive_v37.mjs','scripts/test_track2_demo_v37.py',
    'scripts/track2_community_kit_v37.py','scripts/audit_track2_demo_v37.py',
    'scripts/audit_track2_public_v37.py']

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def isolated_kit():
    receipt=kit.verify()
    # Use the same tested dependency guard, with only the nine kit files present.
    prefix=isolation.BOOTSTRAP.split('captured = io.StringIO()')[0]
    bootstrap=prefix+'''
captured=io.StringIO()
started=time.perf_counter()
with contextlib.redirect_stdout(captured):
    runpy.run_path(str(root/'scripts/track2_demo_v37.py'),run_name='__main__')
result=json.loads(captured.getvalue())
assert result['cases']==18 and result['synthetic_cases']==17 and result['current_decision']=='HOLD'
assert sys.prefix==sys.base_prefix
print(json.dumps(dict(passed=True,review=result,seconds=time.perf_counter()-started,
    blocked_probes=blocked,network_forbidden_by_audit_hook=True,
    protected_paths_forbidden_by_audit_hook=True,project_environment_used=False,
    source_checkout_or_history_used=False)))
'''
    with tempfile.TemporaryDirectory(prefix='track2-small-kit-') as temporary:
        target=Path(temporary)
        with zipfile.ZipFile(kit.DEST) as z:
            for name in z.namelist():
                path=Path(name)
                if path.is_absolute() or '..' in path.parts:raise ValueError('Unsafe kit member')
                out=target/path;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(z.read(name))
        manifest=json.loads((target/'SHA256SUMS.json').read_text())
        if any(digest(target/p)!=sha for p,sha in manifest['files'].items()):raise ValueError('Extracted kit hash mismatch')
        (target/'bootstrap.py').write_text(bootstrap)
        python=str(Path(sys._base_executable).resolve())
        child=subprocess.run([python,'-I','-B',str(target/'bootstrap.py')],cwd=target,
            env={'PATH':str(Path(python).parent),'LANG':'C.UTF-8','LC_ALL':'C.UTF-8'},
            text=True,capture_output=True,timeout=30,check=True)
        result=json.loads(child.stdout)
    return dict(receipt=receipt,isolated_replay=result)

def main():
    destination=ROOT/'notes/track2-demo-audit-v37.json'
    if destination.exists():raise ValueError('Existing audit protected')
    suite=unittest.defaultTestLoader.loadTestsFromModule(tests)
    output=io.StringIO();result=unittest.TextTestRunner(stream=output,verbosity=1).run(suite)
    if not result.wasSuccessful() or result.testsRun!=6:raise ValueError(output.getvalue())
    browsers={}
    for kind,folder in [('demo','v37-demo-final-20261019'),('prompter','v37-prompter-final-20261019')]:
        base=ROOT/'results/feat009'/folder;r=json.loads((base/'audit.json').read_text())
        source=ROOT/f"notes/track2-{'demo' if kind=='demo' else 'teleprompter'}-v37.html"
        if not r['passed'] or r['source_sha256']!=digest(source):raise ValueError('Browser source drift')
        if r['renderer_sha256']!=digest(ROOT/'scripts/review_track2_interactive_v37.mjs'):raise ValueError('Browser reviewer drift')
        if any(digest(base/p)!=sha for p,sha in r['files'].items()):raise ValueError('Screenshot drift')
        browsers[kind]=r
    audit=dict(schema_version=37,passed=True,
        public_input_sha256={p:digest(ROOT/p) for p in sorted(set(SOURCES))},
        implementation_tests=dict(passed=True,tests=6,valid_python_javascript_agreements=83,
                                  invalid_records_rejected_by_both=12),
        browser_checks=browsers,community_kit=isolated_kit(),
        case_selection='Author-designed teaching cases, not representative or held-out clinical validation',
        independent_review=False,clinical_validation=False,external_adoption_measured=False,
        policy_validity_established=False,recording_created=False)
    with destination.open('x') as f:f.write(json.dumps(audit,indent=2)+'\n')
    print(json.dumps(dict(passed=True,tests=6,kit=audit['community_kit']['receipt'],output=str(destination.relative_to(ROOT))),indent=2))

if __name__=='__main__':main()
