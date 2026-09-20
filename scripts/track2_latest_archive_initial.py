#!/usr/bin/env python3
"""Archive completed public-reference outputs, scripts, logs and provenance, not weights."""
from datetime import datetime,timezone
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
from track2_esm_pilot import digest,write_json

ROOT=Path('/home/prachh/v/mva-track2-expanded-latest-20260921')


def archive():
    required=['ESMC-300M-score','ESMC-600M-score','ESMC-6B-score','ESM3-score','ESM3-fold',
              'ESMFold2-single_sequence-retry','ESMFold2-shared_msa','Evo2-20B']
    for label in required:
        if not (ROOT/'outputs'/label/'summary.json').exists():raise ValueError(f'Incomplete {label}')
    status=json.loads((ROOT/'outputs/AlphaFold3-run-status.json').read_text())
    if status['exit']!=0:raise ValueError('Incomplete AlphaFold3')
    dest=ROOT/'archives';dest.mkdir(exist_ok=True)
    runtime=ROOT/'inputs/runtime';runtime.mkdir(exist_ok=False)
    for env in ['esm','af3']:
        for file in ['pyproject.toml','uv.lock']:
            shutil.copyfile(ROOT/'envs'/env/file,runtime/(env+'-'+file))
    sources={}
    for name in ['esm','alphafold3','evo2']:
        path=ROOT/'source'/name
        revision=subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()
        dirty=subprocess.check_output(['git','-C',str(path),'status','--porcelain'],text=True)
        sources[name]=dict(revision=revision,pristine=not bool(dirty))
        if dirty:raise ValueError('Upstream source checkout was changed')
    write_json(runtime/'source-revisions.json',sources)
    files=sorted(p for parent in ['inputs','outputs','scripts','logs'] for p in (ROOT/parent).rglob('*') if p.is_file())
    manifest=dict(created_utc=datetime.now(timezone.utc).isoformat(),files={str(p.relative_to(ROOT)):dict(bytes=p.stat().st_size,sha256=digest(p)) for p in files},
        disclosure='Public references, synthetic alternates, derived predictions and code only. No raw subject data, credentials, environment directories or weights.',
        af3_output_terms='https://github.com/google-deepmind/alphafold3/blob/main/OUTPUT_TERMS_OF_USE.md')
    write_json(ROOT/'archive-manifest.json',manifest)
    target=dest/'latest-model-comparison-v1.tar.gz'
    with tarfile.open(target,'x:gz',compresslevel=1) as out:
        for p in files+[ROOT/'archive-manifest.json']:
            out.add(p,arcname=str(p.relative_to(ROOT)),recursive=False)
    write_json(dest/'latest-model-comparison-v1.json',dict(archive=target.name,bytes=target.stat().st_size,sha256=digest(target),files=len(files)+1))
    print((dest/'latest-model-comparison-v1.json').read_text())


if __name__=='__main__':archive()
