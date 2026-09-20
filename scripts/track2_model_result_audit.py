#!/usr/bin/env python3
"""Audit archived public protein-model inputs and locally recomputed outputs."""
import argparse
import json
import math
from pathlib import Path
from track2_esm_pilot import digest, write_json
from track2_model_expansion import aggregate


def same(a,b):
    if isinstance(a,float) or isinstance(b,float):
        if not (isinstance(a,(int,float)) and isinstance(b,(int,float)) and
                math.isfinite(a) and math.isfinite(b) and math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10)):
            raise ValueError('Numerical reanalysis mismatch')
    elif isinstance(a,dict):
        if not isinstance(b,dict) or set(a)!=set(b):raise ValueError('Object shape mismatch')
        for k in a:same(a[k],b[k])
    elif isinstance(a,list):
        if not isinstance(b,list) or len(a)!=len(b):raise ValueError('List shape mismatch')
        for x,y in zip(a,b):same(x,y)
    elif a!=b:raise ValueError('Reanalysis mismatch')


def audit(archive,output):
    root=Path(archive);repo=Path(__file__).resolve().parents[1];checks=[]
    def bound(path,expected):
        if digest(path)!=expected:raise ValueError(f'Hash mismatch: {path}')
        checks.append(str(path))
    files=sorted((root/'outputs').glob('esm*/summary.json'))
    same(aggregate(files),json.loads((repo/'notes/track2-esm-expanded-results.json').read_text()))
    for path in files:
        r=json.loads(path.read_text())
        for file,key in [('notes/track2-model-expansion-plan.json','plan_sha256'),
                         ('scripts/track2_model_expansion.py','script_sha256'),
                         ('scripts/track2_esm_pilot.py','pilot_helpers_sha256')]:
            bound(repo/file,r[key])
        bound(root/'inputs/uniprot-O60566.fasta',r['fasta_sha256'])
    for arm in ['', 'msa-arm']:
        base=root/arm;r=json.loads((base/'outputs/boltz-preregistration.json').read_text())
        bound(repo/'notes/track2-model-expansion-plan.json',r['plan_sha256'])
        bound(repo/('scripts/track2_boltz_msa.py' if arm else 'scripts/track2_boltz_comparison.py'),r['script_sha256'])
        bound(repo/'scripts/track2_boltz.uv.lock',r['uv_lock_sha256'])
        for name,sha in r['inputs'].items():
            bound(base/name if arm else base/'inputs/boltz'/name,sha)
        if arm:
            bound(repo/'notes/track2-structure-msa-plan.json',r['amendment_sha256'])
            bound(root/'outputs/public-wt-domain.a3m',r['msa_raw_sha256'])
    r=json.loads((root/'outputs/alphafold-preregistration.json').read_text())
    bound(repo/'notes/track2-alphafold-plan.json',r['plan_sha256'])
    bound(repo/'scripts/track2_alphafold_comparison.py',r['script_sha256'])
    bound(repo/'scripts/track2_alphafold.uv.lock',r['lock_sha256'])
    for name,sha in r['inputs'].items():bound(root/name,sha)
    for name in ['boltz-single','boltz-msa','alphafold']:
        published=f'track2-{name}-'+('results' if name=='alphafold' else 'summary')+'.json'
        same(json.loads((root/f'{name}-local-reanalysis.json').read_text()),
             json.loads((repo/'notes'/published).read_text()))
    write_json(output,dict(passed=True,bound_file_checks=len(checks),esm_checkpoints=7,
        boltz_structures=48,alphafold_structures=120,full_local_reanalysis_matched=True,
        float_comparison_tolerance=1e-10,
        scope='Input/provenance and arithmetic/coordinate checks, not independent biological validation.',
        archived_inputs_and_scripts=checks))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('archive');p.add_argument('output')
    a=p.parse_args();audit(a.archive,a.output)
