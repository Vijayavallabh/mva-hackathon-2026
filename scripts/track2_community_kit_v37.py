#!/usr/bin/env python3
"""Build a minimal offline teaching kit without patient or third-party model outputs."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import track2_demo_v37 as demo
import build_track2_demo_v37 as builder

ROOT=demo.ROOT
DEST=ROOT/'results/feat009/jvv7_track2_community_kit_v37.zip'
FILES=['notes/track2-demo-v37.html','notes/track2-demo-cases-v37.json',
       'notes/track2-decision-contract-v21.json','notes/track2-community-kit-v37.md',
       'scripts/track2_demo_v37.py','scripts/track2_falsification_v21.py']

def digest(b):return hashlib.sha256(b).hexdigest()

def contents():
    if builder.rendered()!=(ROOT/FILES[0]).read_text():raise ValueError('Demo source drift')
    result=demo.run()
    values={p:(ROOT/p).read_bytes() for p in FILES}
    values['README.md']=b'# Every enrolled cell\n\nOpen notes/track2-demo-v37.html, or run:\n\n```bash\nuv run --offline --no-project python scripts/track2_demo_v37.py\n```\n\nRequires uv and an available Python 3.12+ interpreter; no third-party Python dependencies.\nRead notes/track2-community-kit-v37.md for scope, limitations, attribution and the full acknowledgement.\nThese cases demonstrate research-policy implementation, not clinical validity.\n'
    values['LICENSE.txt']=b'Original project code and synthetic examples: CC BY 4.0.\nAttribution: jvv7, https://github.com/Vijayavallabh/mva-hackathon-2026\nLicense: https://creativecommons.org/licenses/by/4.0/legalcode\nNo patient data or third-party model outputs are included.\n'
    manifest=dict(version=37,files={p:digest(v) for p,v in values.items()},cases=result['cases'],
                  clinical_validation=False,patient_data_included=False,scope='Offline research teaching kit')
    values['SHA256SUMS.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    return values

def verify():
    expected=contents()
    with zipfile.ZipFile(DEST) as z:
        if z.testzip() is not None or len(z.namelist())!=len(expected) or set(z.namelist())!=set(expected):raise ValueError('Kit members differ')
        if any(z.read(p)!=b for p,b in expected.items()):raise ValueError('Kit bytes differ')
    return dict(verified=True,files=len(expected),bytes=DEST.stat().st_size,sha256=digest(DEST.read_bytes()),
                path=str(DEST.relative_to(ROOT)),clinical_validation=False)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['build','verify']);a=p.parse_args()
    if a.command=='build':
        with zipfile.ZipFile(DEST,'x',compression=zipfile.ZIP_DEFLATED) as z:
            for name,b in contents().items():z.writestr(name,b)
    print(json.dumps(verify(),indent=2))
