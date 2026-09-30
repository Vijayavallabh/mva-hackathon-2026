#!/usr/bin/env python3
"""Download anonymous public LINCS2020 objects into a new owner-host campaign.

Source data are not redistributed in the public repository. Verify bytes against
the S3 multipart ETag (16 MiB parts) as well as recording SHA256 and source headers.
No credentials, subject files, model provider or project .env are read.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.request

BASE = 'https://s3.amazonaws.com/macchiato.clue.io/builds/LINCS2020/'
FILES = {
    'siginfo_beta.txt': 'siginfo_beta.txt',
    'geneinfo_beta.txt': 'geneinfo_beta.txt',
    'cellinfo_beta.txt': 'cellinfo_beta.txt',
    'compoundinfo_beta.txt': 'compoundinfo_beta.txt',
    'level5_beta_trt_xpr_n142901x12328.gctx': 'level5/level5_beta_trt_xpr_n142901x12328.gctx',
    'level5_beta_trt_cp_n720216x12328.gctx': 'level5/level5_beta_trt_cp_n720216x12328.gctx',
}


def fetch(root, name, source):
    url = BASE + source
    with urllib.request.urlopen(urllib.request.Request(url, method='HEAD'), timeout=60) as r:
        headers = dict(r.headers)
        size = int(r.headers['Content-Length'])
        etag = r.headers['ETag'].strip('"')
    path = root / 'inputs' / name
    if not path.exists():
        tmp = path.with_suffix(path.suffix + '.partial')
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.ftruncate(fd, size)
        chunk = 64 * 1024**2

        def part(start):
            end = min(size, start + chunk) - 1
            for attempt in range(3):
                try:
                    request = urllib.request.Request(url, headers={
                        'Range': f'bytes={start}-{end}', 'If-Match': '"' + etag + '"'})
                    with urllib.request.urlopen(request, timeout=120) as r:
                        if r.status != 206 or r.headers.get('Content-Range') != f'bytes {start}-{end}/{size}':
                            raise ValueError('Range or object version mismatch')
                        data = r.read()
                    if len(data) != end - start + 1:
                        raise ValueError('Short range')
                    written = 0
                    while written < len(data):
                        written += os.pwrite(fd, data[written:], start + written)
                    return
                except Exception:
                    if attempt == 2:
                        raise
                    time.sleep(2 * (attempt + 1))

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                list(pool.map(part, range(0, size, chunk)))
        finally:
            os.close(fd)
        tmp.rename(path)
    if path.stat().st_size != size:
        raise ValueError(f'Length mismatch: {name}')
    sha = hashlib.sha256()
    part_hashes = []
    with path.open('rb') as f:
        while block := f.read(16 * 1024**2):
            sha.update(block)
            part_hashes.append(hashlib.md5(block).digest())
    computed = (hashlib.md5(b''.join(part_hashes)).hexdigest() + '-' + str(len(part_hashes))
                if '-' in etag else part_hashes[0].hex())
    if computed != etag:
        raise ValueError(f'Source ETag mismatch: {name}: {computed} != {etag}')
    result = dict(name=name, url=url, bytes=size, sha256=sha.hexdigest(), source_etag=etag,
                  etag_verified=True, multipart_bytes=16 * 1024**2, headers=headers)
    print(json.dumps({k: result[k] for k in ['name', 'bytes', 'sha256', 'etag_verified']}), flush=True)
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('root', type=Path)
    a = p.parse_args()
    records = [fetch(a.root, name, source) for name, source in FILES.items()]
    with (a.root / 'outputs/source-manifest.json').open('x') as f:
        json.dump(dict(source='Broad LINCS2020 public S3', files=records), f, indent=2)
    (a.root / 'outputs/download-complete.txt').write_text(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + '\n')
