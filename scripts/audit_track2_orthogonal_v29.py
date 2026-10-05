#!/usr/bin/env python3
"""Bind v29 public findings to original outputs and local aggregate recomputation."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from track2_orthogonal_v29 import digest, require, save


def compare(a,b,path='',differences=None):
    if differences is None:differences=[]
    if isinstance(a,dict):
        require(isinstance(b,dict) and set(a)==set(b),'Reanalysis keys: '+path)
        for k in a:compare(a[k],b[k],path+'/'+k,differences)
    elif isinstance(a,list):
        require(isinstance(b,list) and len(a)==len(b),'Reanalysis length: '+path)
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+f'/{i}',differences)
    elif type(a) in (int,float) and type(b) in (int,float):
        differences.append(abs(a-b));require(abs(a-b)<=2e-5,'Reanalysis value: '+path)
    else:require(type(a) is type(b) and a==b,'Reanalysis field: '+path)
    return differences


def audit(repo,archive,extracted,reanalysis):
    require(digest(archive)=='373d78784dabc003335813736f907348f7c90aaac510e242b0c917eff8e5280e','Original archive differs')
    manifest=json.loads((extracted/'archive-manifest.json').read_text())
    for name,expected in manifest['files'].items():require(digest(extracted/name)==expected,'Extracted bytes changed: '+name)
    original_scripts=['track2_orthogonal_v29.py','track2_crossfit_v29.py','setup_track2_orthogonal_v29.sh',
        'run_track2_orthogonal_v29.sh','run_track2_crossfit_v29.sh','analyze_track2_orthogonal_v29.py','archive_track2_orthogonal_v29.py']
    for name in original_scripts:require(digest(repo/'scripts'/name)==digest(extracted/'scripts'/name),'Published executed source differs: '+name)
    for name,original in [('track2-structural-plan-v29.json','structural-plan.json'),('track2-crossfit-plan-v29.json','crossfit-plan.json')]:
        require(digest(repo/'notes'/name)==digest(extracted/'inputs'/original),'Executed plan differs')
    comparisons={}
    for name in ['track2-structural-results-v29.json','track2-crossfit-results-v29.json','track2-orthogonal-summary-v29.json']:
        a=json.loads((repo/'notes'/name).read_text());b=json.loads((reanalysis/name).read_text())
        diffs=compare(a,b);comparisons[name]=dict(max_abs_difference=max(diffs,default=0),numeric_fields=len(diffs),
            exact_bytes=digest(repo/'notes'/name)==digest(reanalysis/name))
    name='track2-structural-probabilities-v29.tsv'
    with (repo/'notes'/name).open() as f:a=list(csv.DictReader(f,delimiter='\t'))
    with (reanalysis/name).open() as f:b=list(csv.DictReader(f,delimiter='\t'))
    require(len(a)==len(b),'Probability row count differs')
    maxdiff=0.
    for i,(x,y) in enumerate(zip(a,b)):
        require(set(x)==set(y),'Probability fields differ')
        for k in x:
            try:d=abs(float(x[k])-float(y[k]))
            except ValueError:require(x[k]==y[k],'Probability identity differs');continue
            require(d<=2e-5,f'Probability value differs: {i}/{k}');maxdiff=max(maxdiff,d)
    comparisons[name]=dict(rows=len(a),max_abs_difference=maxdiff,exact_bytes=digest(repo/'notes'/name)==digest(reanalysis/name))
    compute=reanalysis/'track2-orthogonal-compute-v29.json'
    target=repo/'notes'/compute.name
    require(not target.exists(),'Compute record already exists')
    target.write_bytes(compute.read_bytes())
    old=json.loads((repo/'results/feat009/jvv7_track2_research_v28/manifest.json').read_text())
    for name,expected in old['input_hashes'].items():require(digest(repo/name)==expected,'Older bound input changed: '+name)
    public={}
    for folder in ['notes','scripts']:
        for p in sorted((repo/folder).glob('*v29*')):
            if p.is_file():public[str(p.relative_to(repo))]=digest(p)
    result=dict(version=29,passed=True,created_utc=datetime.now(timezone.utc).isoformat(),
        original_archive=dict(path=str(archive.relative_to(repo)),sha256=digest(archive),bytes=archive.stat().st_size,
            files=len(manifest['files'])+1,extracted_digests_verified=True),
        executed_scripts_match_public=True,executed_plans_match_public=True,
        local_aggregate_reanalysis=comparisons,public_input_sha256=public,
        v28_preservation=dict(passed=True,inputs=len(old['input_hashes']),changed=[]),
        scope='Complete-output consistency, aggregate recomputation and source binding; not biological validation or independent specialist review.')
    save(repo/'notes/track2-orthogonal-audit-v29.json',result)
    print(json.dumps(dict(passed=True,archive_files=len(manifest['files'])+1,public_files=len(public),reanalysis=comparisons),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('repo',type=Path);p.add_argument('archive',type=Path)
    p.add_argument('extracted',type=Path);p.add_argument('reanalysis',type=Path);a=p.parse_args()
    audit(a.repo.resolve(),a.archive.resolve(),a.extracted.resolve(),a.reanalysis.resolve())
