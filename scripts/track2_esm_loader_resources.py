#!/usr/bin/env python3
"""Fetch small official ESM2 loader companions; contact prediction remains disabled."""
import json
from pathlib import Path
import urllib.request
from track2_esm_pilot import digest, write_json

ROOT=Path('/home/prachh/v/mva-track2-expanded-20260920')
manifest={}
for name in ['esm2_t36_3B_UR50D','esm2_t48_15B_UR50D']:
    filename=name+'-contact-regression.pt'
    url='https://dl.fbaipublicfiles.com/fair-esm/regression/'+filename
    with urllib.request.urlopen(url,timeout=60) as r:
        payload=r.read(1_000_001)
    if not 100<len(payload)<1_000_000:
        raise ValueError('Unexpected companion size')
    path=ROOT/'cache/weights'/name/filename
    with path.open('xb') as f:f.write(payload)
    manifest[name]={'url':url,'bytes':len(payload),'sha256':digest(path)}
write_json(ROOT/'outputs/esm2-loader-resources.json',manifest)
print(json.dumps(manifest),flush=True)
