#!/usr/bin/env python3
"""Bind the v40 rehearsal-browser receipt; a rehearsal tool is not a recording."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCES=['notes/track2-pitch-v46.md','notes/track2-transcript-v46.txt',
    'notes/track2-teleprompter-v46.html','scripts/build_track2_recording_v46.py',
    'scripts/review_track2_interactive_v46.mjs','scripts/audit_track2_recording_v46.py',
    'scripts/track2_narration_v46.py','notes/track2-recording-guide-v46.md','notes/track2-narration-v46.json']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    target=ROOT/'notes/track2-prompter-audit-v46.json'
    if target.exists():raise ValueError('Existing audit protected')
    folder=ROOT/'results/feat009/v46-prompter-final-20261020-6'
    browser=json.loads((folder/'audit.json').read_text())
    for name,sha in browser['files'].items():
        if Path(name).name!=name or (folder/name).is_symlink() or digest(folder/name)!=sha:
            raise ValueError('Browser export drift')
    record=dict(schema_version=40,passed=True,public_input_sha256={s:digest(ROOT/s) for s in SOURCES},
        browser_checks=browser,recording_created=False,runtime_measured=False,independent_review=False)
    import track2_release_v43 as release
    release.recording_checks(record)
    with target.open('x') as f:f.write(json.dumps(record,indent=2)+'\n')
    print(json.dumps(dict(passed=True,output=str(target.relative_to(ROOT)))))
if __name__=='__main__':main()
