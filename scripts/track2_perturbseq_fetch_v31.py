#!/usr/bin/env python3
"""Fetch a fixed public Perturb-seq dataset, retaining source checksums and failures."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import time
import urllib.request

ARTICLE = 'https://api.figshare.com/v2/articles/20029387'
NAMES = ['rpe1_raw_bulk_01.h5ad', 'rpe1_normalized_bulk_01.h5ad',
         'rpe1_raw_singlecell_01.h5ad', 'K562_essential_raw_bulk_01.h5ad',
         'K562_essential_normalized_bulk_01.h5ad', 'K562_essential_raw_singlecell_01.h5ad']


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def fetch(root):
    inputs = root / 'inputs'
    inputs.mkdir(exist_ok=True)
    metadata = urllib.request.urlopen(ARTICLE, timeout=60).read()
    (inputs / 'figshare-article.json').write_bytes(metadata)
    article = json.loads(metadata)
    files = {f['name']: f for f in article['files']}
    assert set(NAMES) <= files.keys()
    assert article['license']['name'] == 'CC BY 4.0'
    def one(name):
        f = files[name]
        dest = inputs / name
        assert not dest.exists(), f'Refusing overwrite: {dest}'
        part = inputs / (name + '.partial')
        assert not part.exists(), f'Inspect retained partial before retry: {part}'
        start = time.monotonic()
        md5 = hashlib.md5()
        sha = hashlib.sha256()
        count = 0
        request = urllib.request.Request(f['download_url'], headers={'User-Agent': 'Track2-public-research/31'})
        with urllib.request.urlopen(request, timeout=120) as response, part.open('xb') as out:
            for block in iter(lambda: response.read(8 * 1024 * 1024), b''):
                out.write(block)
                md5.update(block)
                sha.update(block)
                count += len(block)
        assert count == f['size'], (name, count, f['size'])
        expected = f.get('computed_md5') or ''
        assert not expected or expected == md5.hexdigest(), f'MD5 mismatch: {name}'
        row = dict(name=name, file_id=f['id'], bytes=count, source_url=f['download_url'],
                   md5=md5.hexdigest(), sha256=sha.hexdigest(), provider_md5=expected or None,
                   provider_md5_verified=bool(expected), elapsed_seconds=time.monotonic()-start)
        part.rename(dest)
        save(inputs / (name + '.receipt.json'), row)
        print(json.dumps(row), flush=True)
        return row
    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(one, NAMES))
    save(root / 'outputs' / 'download-complete.json', dict(
        article=ARTICLE, doi=article.get('doi'), version=article.get('version'),
        license=article['license'], files=rows, public_data_only=True))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('root', type=Path)
    fetch(p.parse_args().root)
