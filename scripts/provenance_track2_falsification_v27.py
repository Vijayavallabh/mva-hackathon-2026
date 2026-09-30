#!/usr/bin/env python3
"""Bind reused public source matrices and pinned model environments to v27."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
from track2_saturation_v27 import OLD, digest, require, save
from track2_specificity_v27 import PREP


def collect(root):
    manifest=json.loads((PREP/'manifest.json').read_text())
    for item in manifest['matrices']:
        require(digest(PREP/(item['arm']+'.npy'))==item['sha256'],'Changed v25 expression matrix')
        require(digest(PREP/(item['arm']+'-metadata.tsv.gz'))==item['metadata_sha256'],'Changed v25 metadata')
    source={str(p):digest(p) for p in sorted(PREP.iterdir()) if p.is_file()}
    plan=json.loads((root/'inputs/plan.json').read_text())
    for item in plan['models']:
        name=item['repository'].replace('/','_')+'-weights.json'
        shutil.copyfile(OLD/'outputs'/name,root/'inputs'/name)
    revision=subprocess.check_output(['git','-C',str(OLD/'source/esm'),'rev-parse','HEAD'],text=True).strip()
    require(revision=='43b4548b86762edfa747b07d5f440aad3c33acee','Changed ESM source revision')
    status=subprocess.check_output(['git','-C',str(OLD/'source/esm'),'status','--porcelain','--untracked-files=no'],text=True)
    require(not status.strip(),'Modified tracked ESM source')
    second=Path('/home/prachh/v/mva-track2-transcriptome-20260927/uv.lock')
    shutil.copyfile(second,root/'inputs/transcriptome.uv.lock')
    save(root/'outputs/reused-source-provenance.json',dict(source_sha256=source,
        source_revision=revision,tracked_source_unchanged=True,
        esm_environment_lock_sha256=digest(OLD/'envs/esm/uv.lock'),
        transcriptome_environment_lock_sha256=digest(second),
        subject_inputs_transferred=False,public_resources_reused=True,new_provider=False))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    collect(p.parse_args().root)
