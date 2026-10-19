#!/usr/bin/env python3
"""Download the checksum-bound, public Funk optical-screen data on the owner host.

Requires the reviewed Harvard Dataverse metadata. No source subject inputs.
Existing successful files are verified before reuse. Failed partials are retained.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import time
from urllib.request import Request, urlopen

METADATA_SHA256 = '8596a110ae68aa73579c0bd28d8bb68b3e61d9297dd24c0a9a4886efb5262903'
DIRECTORIES = {s: s + '-reclassified_cp_phenotype_normalized.parquet' for s in ['mitotic', 'interphase']}
MIN_FREE_BYTES = 128 * 1024**3


def write_json(path, data):
    temp = path.with_name(path.name + '.writing')
    temp.write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')
    temp.replace(path)


def hashes(path):
    md5, sha = hashlib.md5(), hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(8 * 1024**2), b''):
            md5.update(block)
            sha.update(block)
    return md5.hexdigest(), sha.hexdigest()


def selected_files(metadata, arm):
    raw = metadata.read_bytes()
    if hashlib.sha256(raw).hexdigest() != METADATA_SHA256:
        raise ValueError('Unreviewed Dataverse metadata')
    version = json.loads(raw)['data']['latestVersion']
    if version['datasetPersistentId'] != 'doi:10.7910/DVN/VYKTI5' or version['versionNumber'] != 2:
        raise ValueError('Wrong public dataset/version')
    if 'creativecommons.org/licenses/by/4.0/' not in version['termsOfUse']:
        raise ValueError('Unexpected data terms')
    rows = [r for r in version['files'] if r['directoryLabel'] == DIRECTORIES[arm]]
    for row in rows:
        if row['restricted'] or Path(row['label']).name != row['label']:
            raise ValueError('Restricted file or unsafe name')
        if row['dataFile']['checksum']['type'] != 'MD5':
            raise ValueError('Missing provider MD5')
    return rows


def fetch_one(root, arm, row):
    data = row['dataFile']
    target = root / 'inputs' / arm / row['label']
    receipt = root / 'outputs' / 'downloads' / f"{data['id']}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    expected_md5 = data['checksum']['value']
    if target.exists():
        md5, sha = hashes(target)
        if target.stat().st_size != data['filesize'] or md5 != expected_md5:
            raise ValueError(f'Existing file mismatch: {target}')
        if not receipt.exists() or json.loads(receipt.read_text())['sha256'] != sha:
            raise ValueError(f'Existing file lacks matching receipt: {target}')
        return json.loads(receipt.read_text())
    url = f"https://dataverse.harvard.edu/api/access/datafile/{data['id']}"
    for attempt in range(1, 4):
        part = target.with_name(target.name + f'.attempt{attempt}.partial')
        failed = receipt.with_name(receipt.stem + f'.attempt{attempt}.failed.json')
        if part.exists() or failed.exists():
            continue
        if shutil.disk_usage(root).free - data['filesize'] < MIN_FREE_BYTES:
            raise RuntimeError('Free-space floor reached; existing artifacts preserved')
        start = time.monotonic()
        result = dict(file_id=data['id'], arm=arm, file=row['label'], source_url=url,
                      expected_bytes=data['filesize'], expected_md5=expected_md5,
                      retrieved_utc=datetime.now(timezone.utc).isoformat(), attempt=attempt)
        try:
            md5, sha, count = hashlib.md5(), hashlib.sha256(), 0
            req = Request(url, headers={'User-Agent': 'Track2-public-optical/33'})
            with urlopen(req, timeout=120) as response, part.open('xb') as out:
                for block in iter(lambda: response.read(8 * 1024**2), b''):
                    count += len(block)
                    if count > data['filesize']:
                        raise ValueError('Response exceeds declared size')
                    out.write(block)
                    md5.update(block)
                    sha.update(block)
            if count != data['filesize'] or md5.hexdigest() != expected_md5:
                raise ValueError('Provider size/MD5 mismatch')
            result.update(bytes=count, md5=md5.hexdigest(), sha256=sha.hexdigest(),
                          elapsed_seconds=time.monotonic()-start, provider_md5_verified=True,
                          status='complete')
            part.rename(target)
            write_json(receipt, result)
            return result
        except Exception as exc:
            result.update(status='failed', error_type=type(exc).__name__, error=str(exc),
                          elapsed_seconds=time.monotonic()-start)
            write_json(failed, result)
            print(json.dumps(result), flush=True)
            time.sleep(min(10 * attempt, 30))
    raise RuntimeError(f'No successful attempt: {arm}/{row["label"]}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--arm', choices=list(DIRECTORIES), required=True)
    parser.add_argument('--workers', type=int, choices=range(1, 5), default=4)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_relative_to(Path('/home/prachh/v')):
        raise ValueError('This public-data downloader is restricted to the authorized remote folder')
    rows = selected_files(root / 'inputs/dataverse-metadata.json', args.arm)
    status_path = root / 'outputs' / f'download-{args.arm}-status.json'
    results, errors = [], []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        jobs = {pool.submit(fetch_one, root, args.arm, row): row for row in rows}
        for future in as_completed(jobs):
            try:
                results.append(future.result())
            except Exception as exc:
                errors.append(dict(file=jobs[future]['label'], error=str(exc)))
            status = dict(arm=args.arm, completed=len(results), total=len(rows), errors=errors,
                          completed_bytes=sum(r['bytes'] for r in results),
                          expected_bytes=sum(r['dataFile']['filesize'] for r in rows),
                          updated_utc=datetime.now(timezone.utc).isoformat())
            write_json(status_path, status)
            print(json.dumps(status), flush=True)
    if errors:
        raise SystemExit(1)
    write_json(root / 'outputs' / f'download-{args.arm}-complete.json', dict(
        **status, metadata_sha256=METADATA_SHA256,
        files=sorted(results, key=lambda r: r['file_id'])))


if __name__ == '__main__':
    main()
