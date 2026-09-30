#!/usr/bin/env python3
"""Archive completed derived findings, excluding source data and large matrices."""
import argparse
import hashlib
import json
from pathlib import Path
import tarfile


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        while b:=f.read(8*1024**2):h.update(b)
    return h.hexdigest()


def archive(root):
    if not (root/'outputs/complete.txt').exists() or not (root/'outputs/audit.json').exists():
        raise ValueError('Campaign or CPU validation incomplete')
    paths=[root/'pyproject.toml',root/'uv.lock',root/'inputs/plan.json']
    paths += [p for p in sorted((root/'scripts').glob('*')) if p.is_file() or p.is_symlink()]
    paths += [p for p in sorted((root/'logs').glob('*')) if (p.is_file() or p.is_symlink()) and p.name!='archive-final.log']
    paths += [p for p in (root/'outputs').rglob('*') if p.is_file() and 'prepared' not in p.parts
              and p.suffix not in ['.npy','.npz'] and p.name not in ['inventory.json','archive.json']]
    paths += [root/'outputs/prepared/manifest.json',root/'outputs/prepared/cell-contexts.tsv',
              root/'outputs/prepared/everolimus-identity.tsv']
    selected=[]
    for p in sorted(set(paths)):
        if not p.is_file() or p.is_symlink():raise ValueError('Unsafe archive input')
        selected.append(dict(path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=sha(p)))
    full=json.loads((root/'outputs/output-inventory.json').read_text())
    inventory=dict(archived_files=selected,files=full,
        omissions='Original Broad source files, prepared expression/metadata tables, and complete dense score matrices stay hash-inventoried on the owner host. The archive retains complete derived benchmark/drug tables, registrations, source manifests, code, validation and utilization logs. It is a local research archive, not a public source-data redistribution.')
    ip=root/'outputs/inventory.json'
    with ip.open('x') as f:json.dump(inventory,f,indent=2)
    destination=root/'crispr-v25-audit.tar.gz'
    with tarfile.open(destination,'x:gz') as tar:
        for record in selected:tar.add(root/record['path'],arcname=record['path'],recursive=False)
        tar.add(ip,arcname='outputs/inventory.json',recursive=False)
    result=dict(path=destination.name,files=len(selected)+1,bytes=destination.stat().st_size,
                sha256=sha(destination),full_inventory_files=len(full),source_files_redistributed=False)
    with (root/'outputs/archive.json').open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);archive(p.parse_args().root)
