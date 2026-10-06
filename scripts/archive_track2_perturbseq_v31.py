#!/usr/bin/env python3
"""Archive a completed v31 campaign; omit downloadable counts and rebuilt cell matrices."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile
from track2_perturbseq_v31 import digest, require, save


def build(root):
    for rel in ['outputs/campaign-complete.txt','outputs/analysis/summary.json',
                'outputs/pilot-0/cpu-original-counts-audit.json','outputs/worker-4/cpu-original-counts-audit.json']:
        require((root/rel).is_file(),'Missing completion/audit: '+rel)
    files={};omitted=[]
    for directory in ['inputs','outputs','scripts','logs','sources']:
        for p in sorted((root/directory).rglob('*')):
            require(not p.is_symlink(),'Symlink forbidden')
            if not p.is_file():continue
            rel=str(p.relative_to(root))
            if p.suffix=='.h5ad' or (p.parent.name=='prepared' and p.suffix=='.npy'):
                omitted.append(dict(file=rel,bytes=p.stat().st_size,sha256=digest(p)))
                continue
            if '__pycache__' in p.parts:continue
            files[rel]=digest(p)
    save(root/'archive-manifest.json',dict(version=31,files=files,omitted_reproducible_inputs=omitted))
    archive=root/'perturbseq-v31-audit.tar.gz'
    with tarfile.open(archive,'x:gz') as tar:
        for name in [*files,'archive-manifest.json']:tar.add(root/name,arcname=name,recursive=False)
    result=dict(files=len(files)+1,bytes=archive.stat().st_size,sha256=digest(archive),omitted=len(omitted))
    save(root/'archive-receipt.json',result);print(json.dumps(result))


def verify(archive,destination):
    with tarfile.open(archive,'r:gz') as tar:
        members=tar.getmembers();names=[m.name for m in members]
        require(len(names)==len(set(names)),'Duplicate archive entry')
        require(sum(m.size for m in members)<=5_000_000_000 and len(names)<=10000,'Oversized archive')
        for m in members:
            p=PurePosixPath(m.name)
            require(m.isfile() and not p.is_absolute() and '..' not in p.parts and '\\' not in m.name,'Unsafe archive member')
            require(p.parts[0] in {'inputs','outputs','scripts','logs','sources','archive-manifest.json'},'Unapproved path')
        manifest=json.load(tar.extractfile('archive-manifest.json'))
        require(manifest['version']==31 and set(names)==set(manifest['files'])|{'archive-manifest.json'},'Archive membership mismatch')
        for name,expected in manifest['files'].items():
            require(hashlib.sha256(tar.extractfile(name).read()).hexdigest()==expected,'Archive digest mismatch')
        destination.mkdir(exist_ok=False)
        for m in members:
            p=destination/m.name;p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb') as f:f.write(tar.extractfile(m).read())
    return dict(passed=True,files=len(names),bytes=archive.stat().st_size,sha256=digest(archive))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['build','verify'])
    p.add_argument('source',type=Path);p.add_argument('destination',type=Path,nargs='?');a=p.parse_args()
    if a.action=='build':build(a.source)
    else:print(json.dumps(verify(a.source,a.destination),indent=2))
