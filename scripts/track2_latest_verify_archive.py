#!/usr/bin/env python3
"""Verify and safely extract the completed, fixed newer-model research archive."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile

EXPECTED_SHA256 = '084c764b8beb33ae831c5070e702173611c5ba8d8b88e5e61ee75ec9d715baa6'


def verify(archive, output):
    archive, output = Path(archive), Path(output)
    actual = hashlib.sha256(archive.read_bytes()).hexdigest()
    if actual != EXPECTED_SHA256:
        raise ValueError('Archive differs from the completed remote snapshot')
    with tarfile.open(archive, 'r:gz') as source:
        members = source.getmembers()
        names = [m.name for m in members]
        if len(names) != len(set(names)) or len(names) != 686:
            raise ValueError('Unexpected archive inventory')
        for member in members:
            path = PurePosixPath(member.name)
            if not member.isfile() or path.is_absolute() or '..' in path.parts:
                raise ValueError('Unsafe archive member')
        manifest = json.load(source.extractfile('archive-manifest.json'))
        if set(names) != set(manifest['files']) | {'archive-manifest.json'}:
            raise ValueError('Manifest does not match archive')
        for member in members:
            if member.name == 'archive-manifest.json':
                continue
            data = source.extractfile(member).read()
            record = manifest['files'][member.name]
            if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
                raise ValueError('Member checksum mismatch: ' + member.name)
        output.mkdir(parents=True, exist_ok=False)
        source.extractall(output, filter='data')
    return dict(passed=True, archive_sha256=actual, bytes=archive.stat().st_size,
                files=686, verified_manifest_entries=685)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive')
    parser.add_argument('output')
    args = parser.parse_args()
    print(json.dumps(verify(args.archive, args.output), indent=2))
