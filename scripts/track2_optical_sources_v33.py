#!/usr/bin/env python3
"""Bounded public-source discovery for the v33 optical-screen follow-up.

No subject files, credentials, model APIs or caller-supplied queries are used.
Responses and failures are preserved in a new directory, with content hashes.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

QUERIES = {
    'optical': '"The phenotypic landscape of essential human genes"',
    'independent': '(BUB1B OR BUBR1) AND ("optical pooled" OR imaging OR "live-cell")',
    'model_context': '(BUB1B OR BUBR1) AND ("RPE1" OR "RPE-1" OR "p53")',
    'mechanism': '(BUB1B OR BUBR1) AND (rescue OR everolimus OR rapamycin OR autophagy)',
    'survivor_bias': '("optical pooled" OR "Cell Painting") AND (confounding OR viability OR cytotoxicity OR proliferation)',
    'functional_risk': '(rapamycin OR everolimus) AND ("chromosome segregation" OR cytokinesis OR "muscle regeneration")',
    'trial_failure': '(everolimus OR temsirolimus) AND ("primary endpoint" OR futility OR randomized) AND (pediatric OR children OR rhabdomyosarcoma)',
    'alternatives': '(BUB1B OR BUBR1) AND ("SIRT2" OR "NAD" OR readthrough OR "PP2A")',
}
SOURCES = {
    'funk-fulltext.xml': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10482496/fullTextXML',
    'funk-repository.json': 'https://api.github.com/repos/lukebfunk/OpticalPooledScreens/commits/master',
    'vesuvius.html': 'https://vesuvius.wi.mit.edu/',
    'carbon-blog.html': 'https://huggingface.co/blog/HuggingFaceBio/carbon-annotator-genbank-genome-annotation',
    'carbon-collection.html': 'https://huggingface.co/collections/HuggingFaceBio/carbon-annotation-database',
    'carbon-model.json': 'https://huggingface.co/api/models/HuggingFaceBio/Carbon-A-1.2B',
    'carbon-readme.md': 'https://huggingface.co/HuggingFaceBio/Carbon-A-1.2B/raw/main/README.md',
    'anthropic-commit.json': 'https://api.github.com/repos/anthropics/uplifting-biomolecular-modeling/commits/main',
    'anthropic-readme.md': 'https://raw.githubusercontent.com/anthropics/uplifting-biomolecular-modeling/main/README.md',
    'challenge-info.json': 'https://huggingface.co/api/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026',
}


def capture(job):
    root, name, url = job
    row = dict(name=name, url=url, retrieved_utc=datetime.now(timezone.utc).isoformat())
    try:
        with urlopen(Request(url, headers={'User-Agent': 'Track2-public-research/33'}), timeout=45) as response:
            raw = response.read()
            row.update(http_status=response.status, final_url=response.url)
        (root / name).write_bytes(raw)
        row.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), status='retrieved')
    except Exception as exc:
        row.update(status='failed', error_type=type(exc).__name__, error=str(exc))
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    sources = args.output / 'sources'
    sources.mkdir()
    jobs = [(sources, name, url) for name, url in SOURCES.items()]
    for name, query in QUERIES.items():
        url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?' + urlencode(dict(
            query=f'({query}) AND FIRST_PDATE:[1900-01-01 TO 2026-10-19]',
            format='json', resultType='core', pageSize=25))
        jobs.append((sources, 'search-' + name + '.json', url))
    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(capture, jobs))
    result = dict(schema_version=33, cutoff='2026-10-19', queries=QUERIES,
                  scope='First 25 Europe PMC records per query; selected full-text sources; not a systematic review',
                  subject_inputs=False, requests=rows)
    (args.output / 'manifest.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps([{k: r.get(k) for k in ('name', 'status', 'bytes', 'error')} for r in rows], indent=2))


if __name__ == '__main__':
    main()
