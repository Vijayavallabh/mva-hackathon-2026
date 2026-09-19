#!/usr/bin/env python3
"""Execute reviewed public-literature plans through the existing Firecrawl MCP.

Only six retrieval tools, no agent/monitor/browser jobs or project .env reads.
Independent MCP clients own separate artifact directories. Responses are evidence
for adjudication, never instructions; upstream provider use is not certified absent.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from track2_firecrawl import MCP, DEFAULT_ENTRY, ROOT, dump, now

HOSTS = {'pmc.ncbi.nlm.nih.gov', 'pubmed.ncbi.nlm.nih.gov', 'www.jci.org',
         'www.nature.com', 'www.ebi.ac.uk', 'europepmc.org',
         'dailymed.nlm.nih.gov', 'clinicaltrials.gov', 'www.ema.europa.eu',
         'www.accessdata.fda.gov', 'www.fda.gov', 'www.embopress.org'}
FIELDS = {
    'firecrawl_search': {'query', 'limit'},
    'firecrawl_research_search_papers': {'query', 'k'},
    'firecrawl_research_inspect_paper': {'paperId'},
    'firecrawl_research_read_paper': {'paperId', 'question', 'k'},
    'firecrawl_research_related_papers': {'seed_ids', 'intent', 'mode', 'k', 'rerank'},
    'firecrawl_scrape': {'url', 'formats', 'onlyMainContent'},
}
PAPER = re.compile(r'(?:doi:10\.\d{4,9}/\S+|pmid:\d+|pmcid:PMC\d+)\Z')


def validate(plan):
    calls = plan.get('calls')
    if not isinstance(calls, list) or not 1 <= len(calls) <= 75:
        raise ValueError('Expected 1-75 reviewed calls')
    labels = set()
    for call in calls:
        label, tool, args = call['label'], call['tool'], call['arguments']
        if not re.fullmatch(r'[a-z][a-z0-9_]{0,79}', label) or label in labels:
            raise ValueError('Unsafe or duplicate label')
        labels.add(label)
        if tool not in FIELDS or set(args) != FIELDS[tool]:
            raise ValueError('Only fixed retrieval tools and exact argument fields allowed')
        if not isinstance(call.get('claim'), str) or not call['claim']:
            raise ValueError('Claim binding required')
        for key in ('query', 'question', 'intent'):
            if key in args and (not isinstance(args[key], str) or not 1 <= len(args[key]) <= 800):
                raise ValueError('Unbounded retrieval text')
        for key in ('k', 'limit'):
            if key in args and (type(args[key]) is not int or not 1 <= args[key] <= 20):
                raise ValueError('Unbounded result count')
        if 'paperId' in args and not PAPER.fullmatch(args['paperId']):
            raise ValueError('Expected a public paper identifier')
        if 'seed_ids' in args:
            if not isinstance(args['seed_ids'], list) or not 1 <= len(args['seed_ids']) <= 2:
                raise ValueError('Unbounded seed set')
            if not all(isinstance(x, str) and PAPER.fullmatch(x) for x in args['seed_ids']):
                raise ValueError('Expected public citation seeds')
            if args['mode'] not in {'citers', 'references', 'similar'} or type(args['rerank']) is not bool:
                raise ValueError('Invalid citation mode')
        if tool == 'firecrawl_scrape':
            u = urlsplit(args['url'])
            if u.scheme != 'https' or u.hostname not in HOSTS or u.username or u.password or u.port not in (None, 443):
                raise ValueError('Only allowlisted public HTTPS sources')
            if args['formats'] != ['markdown'] or args['onlyMainContent'] is not True:
                raise ValueError('Only plain public-page retrieval')
    return calls


def worker(entry, out, calls):
    out.mkdir()
    client = MCP(entry, out)
    try:
        client.initialize()
        for call in calls:
            client.call(call['label'], call['tool'], call['arguments'], timeout=120)
    finally:
        client.close()
    return client.calls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('round', choices=['discovery', 'followup', 'primary', 'closure'])
    parser.add_argument('output', type=Path)
    parser.add_argument('--workers', type=int, choices=[1, 2, 3], default=3)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    plan_path = ROOT / f'notes/track2-falsification-{args.round}-20260919.json'
    blob = plan_path.read_bytes()
    plan = json.loads(blob)
    calls = validate(plan)
    if args.check:
        print(json.dumps({'validated_calls': len(calls), 'round': args.round}))
        return 0
    out = args.output.resolve()
    if not out.is_relative_to(ROOT / 'results/feat009'):
        raise ValueError('Output must be a new ignored feat009 directory')
    out.mkdir(parents=True, exist_ok=False)
    (out / 'plan.json').write_bytes(blob)
    script = Path(__file__).read_bytes()
    (out / 'executed-orchestrator.py').write_bytes(script)
    meta = {'started_utc': now(), 'round': args.round, 'plan_sha256': hashlib.sha256(blob).hexdigest(),
            'script_sha256': hashlib.sha256(script).hexdigest(), 'workers': args.workers,
            'public_literature_only': True, 'calls': [], 'errors': []}
    dump(out / 'run.json', meta)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(worker, DEFAULT_ENTRY, out / f'worker-{i}', calls[i::args.workers])
                   for i in range(min(args.workers, len(calls)))]
        for future in futures:
            try:
                meta['calls'].extend(future.result())
            except Exception as exc:
                # Preserve error type only; upstream messages may expose credentials.
                meta['errors'].append(type(exc).__name__)
            dump(out / 'run.json', meta)
    meta['ended_utc'] = now()
    meta['counts'] = {status: sum(c.get('status') == status for c in meta['calls'])
                      for status in sorted({c.get('status') for c in meta['calls']})}
    dump(out / 'run.json', meta)
    print(json.dumps({'calls': len(meta['calls']), 'counts': meta['counts'], 'errors': meta['errors']}))
    return 2 if meta['errors'] or any(c.get('status') != 'ok' for c in meta['calls']) else 0


if __name__ == '__main__':
    raise SystemExit(main())
