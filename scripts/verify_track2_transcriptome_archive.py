#!/usr/bin/env python3
"""Verify the downloaded public v19 archive without extracting or executing it."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile


def digest(stream):
    h = hashlib.sha256()
    for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
        h.update(block)
    return h.hexdigest()


def verify(path, record):
    with path.open('rb') as f:
        actual = digest(f)
    if actual != record['sha256'] or path.stat().st_size != record['bytes']:
        raise ValueError('Archive bytes differ from the audited campaign')
    with tarfile.open(path, 'r:gz') as tar:
        members = tar.getmembers()
        names = [m.name for m in members]
        if len(names) != len(set(names)) or len(names) != record['files']:
            raise ValueError('Duplicate or incorrect archive membership')
        for m in members:
            p = PurePosixPath(m.name)
            if not m.isfile() or p.is_absolute() or '..' in p.parts or str(p) != m.name:
                raise ValueError('Unsafe archive member: ' + m.name)
        manifest_bytes = tar.extractfile('archive-manifest.json').read()
        if hashlib.sha256(manifest_bytes).hexdigest() != record['manifest_sha256']:
            raise ValueError('Archive manifest mismatch')
        manifest = json.loads(manifest_bytes)['files']
        if set(names) != set(manifest) | {'archive-manifest.json'}:
            raise ValueError('Unlisted or missing archive member')
        for name, expected in manifest.items():
            member = tar.getmember(name)
            if member.size != expected['bytes'] or digest(tar.extractfile(member)) != expected['sha256']:
                raise ValueError('Archive member hash mismatch: ' + name)
    return dict(passed=True, archive_sha256=actual, files=len(members), verified_member_hashes=len(manifest))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    args = parser.parse_args()
    audit = json.loads((Path(__file__).resolve().parents[1] / 'notes/track2-transcriptome-audit-v19.json').read_text())
    print(json.dumps(verify(args.archive, audit['archive']), indent=2))
