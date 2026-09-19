#!/usr/bin/env python3
"""Archive public challenge pages/source/template with anonymous GETs; never submit."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SPACE = 'SageBio/rare-disease-real-kid-mva-hackathon-2026'
HOST = 'https://sagebio-rare-disease-real-kid-mva-hackathon-2026.hf.space'
PATHS = ('README.md', 'config.py', 'tabs/about.py', 'tabs/rules.py', 'tabs/faq.py',
         'tabs/submit_track2.py', 'static/templates/methods_description_form.xlsx')


def get(url):
    with urlopen(Request(url, headers={'User-Agent': 'Track2-public-challenge-review/1'}), timeout=45) as r:
        data = r.read(5_000_001)
        if len(data) > 5_000_000:
            raise ValueError('Oversized public response')
        return data, r.geturl()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    out = args.output.absolute()
    if out.parent != ROOT / 'results/feat009' or not re.fullmatch(r'[a-z0-9-]+', out.name):
        raise ValueError('Use a new direct feat009 child')
    if any(p.is_symlink() for p in (ROOT, ROOT / 'results', out.parent, out)):
        raise ValueError('Symlinked output')
    out.mkdir(exist_ok=False)
    manifest = {'started_utc': datetime.now(timezone.utc).isoformat(), 'anonymous_get_only': True,
                'sources': [], 'executed_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (out / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
    meta_url = 'https://huggingface.co/api/spaces/' + SPACE
    meta, resolved = get(meta_url)
    (out / 'space.json').write_bytes(meta)
    revision = json.loads(meta)['sha']
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('Invalid public revision')
    manifest.update(revision=revision, metadata_url=resolved, metadata_sha256=hashlib.sha256(meta).hexdigest())
    jobs = [(p, f'https://huggingface.co/spaces/{SPACE}/resolve/{revision}/{p}') for p in PATHS]
    jobs += [('live-config.json', HOST + '/config'), ('live-index.html', HOST + '/')]

    def fetch(job):
        name, url = job
        record = {'path': name, 'url': url}
        try:
            data, final = get(url)
            target = out / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            record.update(status='ok', bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), resolved_url=final)
        except Exception as error:
            record.update(status=type(error).__name__)
        return record

    with ThreadPoolExecutor(max_workers=3) as pool:
        manifest['sources'] = list(pool.map(fetch, jobs))
    manifest['ended_utc'] = datetime.now(timezone.utc).isoformat()
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    config_path = out / 'live-config.json'
    if config_path.exists():
        components = json.loads(config_path.read_text())['components']
        text = '\n\n'.join(c['props']['value'] for c in components
                         if c['type'] == 'markdown' and isinstance(c.get('props', {}).get('value'), str))
        (out / 'live-markdown.txt').write_text(text)
    print(json.dumps({'revision': revision, 'sources': manifest['sources']}, indent=2))
    return 2 if any(x['status'] != 'ok' for x in manifest['sources']) else 0


if __name__ == '__main__':
    raise SystemExit(main())
