#!/usr/bin/env python3
"""Archive every publicly listed Space discussion using anonymous GETs only."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
BASE='https://huggingface.co/api/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions'

def get(url):
    if not (url==BASE or url.startswith(BASE+'?p=') or re.fullmatch(re.escape(BASE)+r'/\d+',url)):
        raise ValueError('Only public discussion endpoints allowed')
    with urlopen(Request(url,headers={'User-Agent':'Track2-public-community-review/1'}),timeout=45) as r:
        data=r.read(5_000_001)
        if len(data)>5_000_000:raise ValueError('Oversize response')
        if not r.geturl().startswith(BASE):raise ValueError('Unexpected redirect')
    return data

def visible_comments(thread):
    return [e for e in thread['events'] if e['type']=='comment' and not e['data'].get('hidden',False)]

def safe_preview(raw):
    # Do not surface possible source-level variant/read records or identifying contacts.
    patterns=[r'(?im)^.*(?:\bchr(?:[0-9]{1,2}|X|Y|M)[:\t ]+\d{4,}|\b(?:[0-9]{1,2}|X|Y)[:\t]\d{4,}|\b(?:NC_|NM_|ENST)\d+.*[cg]\.\d+|\bPROBAND\d+|\bWGS_[A-Za-z0-9_]+|^@(?:[A-Z0-9]+:){3,}).*$',
              r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',
              r'(?i)\b(?:hf_[a-z0-9]{15,}|sk-[a-z0-9_-]{15,})\b']
    for pattern in patterns:raw=re.sub(pattern,'[local-only omitted detail]',raw)
    return raw

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=Path);a=p.parse_args()
    out=a.output.absolute()
    if out.parent!=ROOT/'results/feat009' or not re.fullmatch('[a-z0-9-]+',out.name):raise ValueError('Use new feat009 child')
    if any(q.is_symlink() for q in [ROOT,ROOT/'results',out.parent,out]):raise ValueError('No symlinks')
    out.mkdir(exist_ok=False)
    manifest=dict(started_utc=datetime.now(timezone.utc).isoformat(),anonymous_get_only=True,sources=[],
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scope='All listed open and closed public discussions; no hidden/deleted/private content or edit history')
    listing={};expected=None
    for page in range(100):
        url=BASE+f'?p={page}';data=get(url);x=json.loads(data);name=f'index-{page}.json';(out/name).write_bytes(data)
        manifest['sources'].append(dict(file=name,url=url,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)))
        if expected is None:expected=x['count']
        if expected!=x['count']:raise ValueError('Discussion listing changed during pagination')
        for d in x['discussions']:
            if d['num'] in listing:raise ValueError('Repeated discussion during pagination')
            listing[d['num']]=d
        if len(listing)==expected:break
        if not x['discussions']:raise ValueError('Incomplete listing')
    else:raise ValueError('Pagination bound exceeded')
    def fetch(num):
        url=BASE+f'/{num}';name=f'discussion-{num}.json'
        try:
            data=get(url);x=json.loads(data)
            if x['num']!=num:raise ValueError('Thread identity mismatch')
            (out/name).write_bytes(data)
            return dict(num=num,file=name,url=url,status='ok',sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),
                        comments=len(visible_comments(x)),events=len(x['events']))
        except Exception as e:return dict(num=num,url=url,status=type(e).__name__)
    with ThreadPoolExecutor(max_workers=3) as pool:threads=list(pool.map(fetch,sorted(listing)))
    manifest.update(listed_count=expected,listed_numbers=sorted(listing),closed_count=sum(d['status']=='closed' for d in listing.values()),threads=threads,
                    ended_utc=datetime.now(timezone.utc).isoformat(),complete=all(t['status']=='ok' for t in threads))
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    preview=[]
    for t in threads:
        if t['status']!='ok':continue
        x=json.loads((out/t['file']).read_text());preview.append(f"## #{x['num']} — {x['title']} [{x['status']}]\n")
        for e in visible_comments(x):
            raw=e['data'].get('latest',{}).get('raw','')
            preview.append(f"{e['author'].get('name','unknown')} | {e['createdAt']}\n{safe_preview(raw)}\n")
    (out/'local-review-preview.md').write_text('\n'.join(preview))
    print(json.dumps({k:manifest[k] for k in ['listed_count','listed_numbers','closed_count','complete']},indent=2))
    if not manifest['complete']:raise SystemExit(2)

if __name__=='__main__':main()
