#!/usr/bin/env python3
"""Archive completed v27 public-only jobs; verify/extract without trusting tar paths."""
import argparse
import json
from pathlib import Path, PurePosixPath
import tarfile
from track2_saturation_v27 import digest, require, save


def build(root):
    for marker in ['protein-complete.txt','specificity-complete.txt']:
        require((root/'outputs'/marker).is_file(),'Campaign incomplete')
    files={}
    for directory in ['inputs','outputs','scripts','logs']:
        for p in sorted((root/directory).rglob('*')):
            require(not p.is_symlink(),'Archive symlink forbidden')
            if p.is_file():files[str(p.relative_to(root))]=digest(p)
    save(root/'archive-manifest.json',dict(version=27,files=files))
    archive=root/'falsification-v27-audit.tar.gz'
    with tarfile.open(archive,'x:gz') as tar:
        for name in [*files,'archive-manifest.json']:
            tar.add(root/name,arcname=name,recursive=False)
    print(json.dumps(dict(files=len(files)+1,bytes=archive.stat().st_size,sha256=digest(archive))))


def verify(archive,destination):
    import hashlib
    with tarfile.open(archive,'r:gz') as tar:
        members=tar.getmembers();names=[m.name for m in members]
        require(len(names)==len(set(names)),'Duplicate archive entry')
        require(sum(m.size for m in members)<=200_000_000,'Oversized archive')
        for m in members:
            path=PurePosixPath(m.name)
            require(m.isfile() and not path.is_absolute() and '..' not in path.parts
                    and '\\' not in m.name,'Unsafe archive path/type')
        manifest=json.load(tar.extractfile('archive-manifest.json'))
        require(set(names)==set(manifest['files'])|{'archive-manifest.json'},'Archive membership drift')
        for name,expected in manifest['files'].items():
            require(hashlib.sha256(tar.extractfile(name).read()).hexdigest()==expected,'Archive digest mismatch')
        destination.mkdir(exist_ok=False)
        for m in members:
            p=destination/m.name;p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb') as f:f.write(tar.extractfile(m).read())
    return dict(passed=True,files=len(names),archive_sha256=digest(archive),bytes=archive.stat().st_size)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['build','verify'])
    p.add_argument('source',type=Path);p.add_argument('destination',type=Path,nargs='?');a=p.parse_args()
    if a.command=='build':build(a.source)
    else:print(json.dumps(verify(a.source,a.destination),indent=2))
