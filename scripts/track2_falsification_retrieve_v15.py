#!/usr/bin/env python3
"""Bounded public-only v15 search; archive successes and failures, never retry."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen
from track2_falsification_sources import fetch, validate
from track2_firecrawl import ROOT, MCP, DEFAULT_ENTRY, dump, now

PLAN = ROOT / 'notes/track2-falsification-search-v15.json'

def run(mode, output):
    out = output.resolve()
    if out.parent != ROOT / 'results/feat009':
        raise ValueError('Use a new directory directly under results/feat009')
    out.mkdir(exist_ok=False)
    source = ROOT / 'notes/track2-falsification-followup-v15.json' if mode == 'followup' else PLAN
    blob = source.read_bytes()
    plan = json.loads(blob)
    (out / 'plan.json').write_bytes(blob)
    (out / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
    if mode == 'firecrawl':
        client = MCP(DEFAULT_ENTRY, out)
        try:
            client.initialize()
            for row in plan['firecrawl_queries']:
                client.call(row['id'], 'firecrawl_search',
                            {'query': row['query'], 'limit': 6}, timeout=40)
        finally:
            client.close()
        return
    records = validate(plan['records'])
    audit = dict(started_utc=now(), plan_sha256=hashlib.sha256(blob).hexdigest(), records=[], downloads=[])
    with ThreadPoolExecutor(max_workers=3) as pool:
        for row in pool.map(lambda r: fetch(r, out), records):
            audit['records'].append(row)
            dump(out / 'retrieval.json', audit)
    for name, url in plan['fixed_public_downloads'].items():
        row = dict(id=name, url=url)
        try:
            with urlopen(Request(url, headers={'User-Agent':'Track2-public-review/1'}), timeout=35) as response:
                data = response.read(5_000_001)
            if len(data) > 5_000_000:
                raise ValueError('Oversized public source')
            suffix = '.pdf' if name == 'balnis_supplement' else '.html'
            if suffix == '.pdf' and not data.startswith(b'%PDF'):
                raise ValueError('Not a PDF')
            (out / (name + suffix)).write_bytes(data)
            row.update(status='ok', bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        except Exception as exc:
            row['status'] = type(exc).__name__
        audit['downloads'].append(row)
        print(json.dumps(row), flush=True)
    audit['ended_utc'] = now()
    dump(out / 'retrieval.json', audit)

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=['records','firecrawl','followup'])
    p.add_argument('output', type=Path)
    a = p.parse_args()
    run(a.mode, a.output)
