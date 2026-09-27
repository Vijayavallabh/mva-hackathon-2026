#!/usr/bin/env python3
"""Verify the v23 evidence archive without extraction or executable dependencies."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile


def require(ok,message):
    if not ok:raise ValueError(message)


def digest_stream(stream):
    h=hashlib.sha256()
    for part in iter(lambda:stream.read(8*1024*1024),b''):h.update(part)
    return h.hexdigest()


def verify(path,expected):
    path=Path(path)
    require(path.stat().st_size==expected['bytes'],'Archive byte count mismatch')
    with path.open('rb') as f:require(digest_stream(f)==expected['sha256'],'Archive checksum mismatch')
    with tarfile.open(path,'r:gz') as tar:
        members=tar.getmembers();names=[m.name for m in members]
        require(len(names)==len(set(names))==expected['files'],'Duplicate/missing archive members')
        for m in members:
            p=PurePosixPath(m.name)
            require(m.isfile() and not p.is_absolute() and '..' not in p.parts,'Unsafe archive member')
            require(m.size<=200*1024**2,'Unexpected member size')
        require(sum(m.size for m in members)<1024**3,'Unexpected total expanded size')
        inventory=json.load(tar.extractfile('outputs/inventory.json'))
        selected={r['path']:r for r in inventory['archived_files']}
        require(set(names)==set(selected)|{'outputs/inventory.json'},'Archive inventory membership mismatch')
        require(len(inventory['files'])==expected['full_inventory_files'],'Full inventory drift')
        for name,r in selected.items():
            m=tar.getmember(name);require(m.size==r['bytes'],'Member byte count mismatch: '+name)
            require(digest_stream(tar.extractfile(m))==r['sha256'],'Member hash mismatch: '+name)
    return dict(passed=True,files=len(names),checked_members=len(selected),bytes=path.stat().st_size,sha256=expected['sha256'],
        extracted=False,code_executed=False,biological_validation=False)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('archive',type=Path);p.add_argument('--metadata',type=Path,required=True);a=p.parse_args()
    print(json.dumps(verify(a.archive,json.loads(a.metadata.read_text())),indent=2))
