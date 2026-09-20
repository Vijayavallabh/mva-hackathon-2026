#!/usr/bin/env python3
"""Download only pinned public model resources; never inspect subject inputs or keys."""
import concurrent.futures
from datetime import datetime, timezone
import json
from pathlib import Path
import urllib.request
from track2_esm_pilot import digest, write_json

ROOT = Path('/home/prachh/v/mva-track2-expanded-latest-20260921')


def fetch_model(item):
    from huggingface_hub import HfApi, hf_hub_download
    repo, revision = item['repository'], item['revision']
    info = HfApi(token=False).model_info(repo, revision=revision, files_metadata=True)
    if info.sha != revision:
        raise ValueError('Pinned revision mismatch')
    dest = ROOT / 'cache/models' / repo.replace('/', '_')
    dest.mkdir(parents=True, exist_ok=True)
    selected = [s for s in info.siblings if not s.rfilename.startswith(('images/', '.'))]
    if sum(s.size for s in selected) > 65_000_000_000:
        raise ValueError('Public checkpoint exceeded fixed size bound')
    manifest = dict(repository=repo, revision=revision, files=[], created_utc=datetime.now(timezone.utc).isoformat())
    for entry in selected:
        path = Path(hf_hub_download(repo, entry.rfilename, revision=revision, local_dir=dest, token=False))
        sha = digest(path)
        expected = entry.lfs.sha256 if entry.lfs else None
        if path.stat().st_size != entry.size or (expected and sha != expected):
            raise ValueError('Checkpoint upstream digest/size mismatch')
        manifest['files'].append(dict(name=entry.rfilename, bytes=entry.size, sha256=sha, upstream_lfs_sha256=expected))
    write_json(ROOT / 'outputs' / (repo.replace('/', '_') + '-weights.json'), manifest)
    print(json.dumps(dict(download_complete=repo, files=len(selected))), flush=True)


def main():
    plan = json.loads((ROOT / 'inputs/latest-plan.json').read_text())
    # Three downloads in parallel; bounded to the six registered model repositories.
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(fetch_model, item): item['repository'] for item in plan['models']}
        statuses = []
        for future in concurrent.futures.as_completed(futures):
            repo = futures[future]
            try:
                future.result()
                statuses.append(dict(repository=repo, completed=True))
            except Exception as error:
                statuses.append(dict(repository=repo, completed=False, error=str(error)))
            write_json(ROOT / 'outputs/download-status.json', statuses)
    if not all(r['completed'] for r in statuses):
        raise RuntimeError('One or more pinned public downloads failed; see status')


if __name__ == '__main__':
    main()
