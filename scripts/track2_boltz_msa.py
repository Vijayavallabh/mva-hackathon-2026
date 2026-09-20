#!/usr/bin/env python3
"""Public-WT-only homolog retrieval and fixed shared-MSA Boltz sensitivity arm."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from track2_esm_pilot import digest, write_json
from track2_boltz_comparison import ROOT, run


def fetch():
    from boltz.data.msa.mmseqs2 import run_mmseqs2
    seq=''.join((ROOT/'inputs/uniprot-O60566.fasta').read_text().splitlines()[1:])[720:1044]
    if hashlib.sha256((ROOT/'inputs/uniprot-O60566.fasta').read_bytes()).hexdigest() != '4ac6895daf90501d8398d17ded42f46d78b9db777f5084facc875c2926496d1b':
        raise ValueError('Public reference changed')
    a3ms=run_mmseqs2(seq,prefix=str(ROOT/'cache/public-wt-msa'),use_env=True,use_filter=True,
                    use_pairing=False,host_url='https://api.colabfold.com')
    if len(a3ms)!=1:raise ValueError('Expected one public reference query')
    with (ROOT/'outputs/public-wt-domain.a3m').open('x') as f:f.write(a3ms[0])


def prepare():
    arm=ROOT/'msa-arm';(arm/'inputs/boltz').mkdir(parents=True,exist_ok=False)
    (arm/'outputs').mkdir();(arm/'logs').mkdir();(arm/'inputs/msa').mkdir()
    for name,target in [('boltz-env',ROOT/'boltz-env'),('cache',ROOT/'cache')]:
        (arm/name).symlink_to(target,target_is_directory=True)
    for filename in ['plan.json','uniprot-O60566.fasta']:
        (arm/'inputs'/filename).symlink_to(ROOT/'inputs'/filename)
    raw=(ROOT/'outputs/public-wt-domain.a3m').read_text()
    lines=raw.splitlines(keepends=True)
    if len(lines)<3 or not lines[0].startswith('>'):
        raise ValueError('Malformed or query-only MSA')
    stop=next((i for i,x in enumerate(lines[1:],1) if x.startswith('>')),None)
    if stop is None:raise ValueError('MSA contains no homolog')
    query=''.join(x.strip() for x in lines[1:stop])
    wt=json.loads((ROOT/'inputs/boltz/WT.yaml').read_text())['sequences'][0]['protein']['sequence']
    if query!=wt:raise ValueError('First MSA record is not exact public WT query')
    records=sum(x.startswith('>') for x in lines)
    for path in sorted((ROOT/'inputs/boltz').glob('*.yaml')):
        data=json.loads(path.read_text());seq=data['sequences'][0]['protein']['sequence']
        msa=arm/'inputs/msa'/(path.stem+'.a3m')
        msa.write_text('>public_query\n'+seq+'\n'+''.join(lines[stop:]))
        data['sequences'][0]['protein']['msa']=str(msa)
        write_json(arm/'inputs/boltz'/path.name,data)
    prereg=json.loads((ROOT/'outputs/boltz-preregistration.json').read_text())
    prereg.update(arm='shared WT-derived MSA',created_utc=datetime.now(timezone.utc).isoformat(),
        amendment_sha256=digest(ROOT/'inputs/msa-plan.json'),msa_raw_sha256=digest(ROOT/'outputs/public-wt-domain.a3m'),
        msa_records=records,script_sha256=digest(__file__),
        inputs={str(p.relative_to(arm)):digest(p) for p in sorted((arm/'inputs').glob('*/*'))})
    write_json(arm/'outputs/boltz-preregistration.json',prereg)
    print(json.dumps({'MSA_records':records,'query_only_public_reference':True}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['fetch','prepare','run']);
    p.add_argument('--gpus',type=int,nargs='+',default=[2,4,6,7]);a=p.parse_args()
    if a.command=='fetch':fetch()
    elif a.command=='prepare':prepare()
    else:run(ROOT/'msa-arm',a.gpus)
