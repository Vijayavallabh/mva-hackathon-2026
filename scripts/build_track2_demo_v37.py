#!/usr/bin/env python3
"""Build or verify the self-contained public teaching demo. No remote assets."""
import argparse
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def rendered():
    template=(ROOT/'notes/track2-demo-template-v37.html').read_text()
    ack=' '.join((ROOT/'notes/track2-report-v36.md').read_text().split('## Acknowledgement\n')[1].split())
    values={'ACK':ack,'CASES':json.dumps(json.loads((ROOT/'notes/track2-demo-cases-v37.json').read_text()),ensure_ascii=False).replace('<','\\u003c'),
        'CURRENT':json.dumps(json.loads((ROOT/'notes/track2-decision-contract-v21.json').read_text())),
        'SCRIPT':(ROOT/'scripts/track2_demo_v37.js').read_text()}
    for key,value in values.items():template=template.replace('__'+key+'__',value)
    return template

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    path=ROOT/'notes/track2-demo-v37.html';text=rendered()
    if args.check:
        if path.read_text()!=text:raise ValueError('Generated demo differs from its sources')
    else:path.write_text(text)
    print(json.dumps(dict(generated_demo_verified=True,bytes=len(text.encode()),network_required=False)))
