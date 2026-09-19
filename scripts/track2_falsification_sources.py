#!/usr/bin/env python3
"""Archive fixed public primary records after Firecrawl discovery, without retries."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
from track2_firecrawl import ROOT, dump, now

MAX_BYTES = 5_000_000


def check_identity(record, data):
    """Optional primary-identity guard; discovery queries intentionally allow many hits."""
    expected = record.get('expected_pmcid')
    if expected:
        hits = data.get('resultList', {}).get('result', [])
        if len(hits) != 1 or hits[0].get('pmcid') != expected:
            raise ValueError('Primary record identity mismatch')


def validate(records):
    if not isinstance(records, list) or not 1 <= len(records) <= 40:
        raise ValueError('Expected bounded public records')
    seen = set()
    for r in records:
        u = urlsplit(r['url'])
        if not re.fullmatch(r'[a-z][a-z0-9_]{0,79}', r['id']) or r['id'] in seen:
            raise ValueError('Unsafe or duplicate record id')
        seen.add(r['id'])
        allowed = ((u.hostname == 'www.ebi.ac.uk' and u.path.startswith('/europepmc/webservices/rest/'))
                   or (u.hostname == 'clinicaltrials.gov' and u.path.startswith('/api/v2/studies/')))
        if u.scheme != 'https' or not allowed or u.username or u.password or u.port not in (None, 443):
            raise ValueError('Only fixed public literature/registry APIs')
        if r['format'] not in ('json', 'xml'):
            raise ValueError('Expected structured primary record')
    return records


def fetch(r, out):
    record = dict(r, started_utc=now())
    try:
        with urlopen(Request(r['url'], headers={'User-Agent': 'Track2-public-literature-review/1'}), timeout=45) as response:
            blob = response.read(MAX_BYTES + 1)
            if len(blob) > MAX_BYTES:
                raise ValueError('Oversized public record')
            if r['format'] == 'json':
                check_identity(r, json.loads(blob))
            else:
                root = ET.fromstring(blob)
                if root.tag != 'article':
                    raise ValueError('Not an article XML')
                text = '\n\n'.join(' '.join(e.itertext()) for e in root.iter()
                                   if e.tag in ('article-title', 'title', 'p', 'table-wrap'))
                (out / (r['id'] + '.txt')).write_text(text)
            (out / (r['id'] + '.' + r['format'])).write_bytes(blob)
            record.update(status='ok', bytes=len(blob), sha256=hashlib.sha256(blob).hexdigest())
    except HTTPError as exc:
        record.update(status='http_error', http_status=exc.code)
    except Exception as exc:
        record.update(status=type(exc).__name__)
    record['ended_utc'] = now()
    print(json.dumps({'id': r['id'], 'status': record['status']}), flush=True)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--supplement', action='store_true')
    args = parser.parse_args()
    suffix = '-supplement' if args.supplement else ''
    source = ROOT / f'notes/track2-falsification-records{suffix}-20260919.json'
    blob = source.read_bytes()
    records = validate(json.loads(blob)['records'])
    out = args.output.resolve()
    if not out.is_relative_to(ROOT / 'results/feat009'):
        raise ValueError('Use a new ignored feat009 output directory')
    out.mkdir(parents=True, exist_ok=False)
    (out / 'plan.json').write_bytes(blob)
    script = Path(__file__).read_bytes()
    (out / 'executed-script.py').write_bytes(script)
    manifest = {'started_utc': now(), 'plan_sha256': hashlib.sha256(blob).hexdigest(),
                'script_sha256': hashlib.sha256(script).hexdigest(), 'records': []}
    dump(out / 'retrieval.json', manifest)
    with ThreadPoolExecutor(max_workers=3) as pool:
        for r in pool.map(lambda item: fetch(item, out), records):
            manifest['records'].append(r)
            dump(out / 'retrieval.json', manifest)
    manifest['ended_utc'] = now()
    dump(out / 'retrieval.json', manifest)
    return 2 if any(r['status'] != 'ok' for r in manifest['records']) else 0


if __name__ == '__main__':
    raise SystemExit(main())
