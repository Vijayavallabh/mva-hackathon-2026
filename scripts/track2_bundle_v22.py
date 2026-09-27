#!/usr/bin/env python3
"""Build/verify current recording materials; this never records or submits a video."""
import argparse
import json
from pathlib import Path
import zipfile
import track2_release_v22 as release

ROOT=release.ROOT
SLIDES=ROOT/'results/feat009/v22-slides-final-20260927'
DOCS=ROOT/'results/feat009/v22-documents-final-b-20260927'
DEST=ROOT/'results/feat009/jvv7_track2_video_materials_v22.zip'


def sources():
    release.scientific_checks()
    render=json.loads((ROOT/'notes/track2-v22-render-audit.json').read_text())
    docs=json.loads((ROOT/'notes/track2-v22-documents-audit.json').read_text())
    expected={SLIDES/name:sha for name,sha in render['files'].items()}
    expected.update({DOCS/name:sha for name,sha in docs['export']['files'].items()})
    expected.update({DOCS/name:sha for name,sha in docs['pdf']['files'].items()})
    for path,sha in expected.items():
        release.require(path.is_file() and not path.is_symlink() and release.digest(path)==sha,
                        'Export changed or missing: '+path.name)
    files={path.name:path for path in expected if path.suffix != '.html'}
    files['jvv7_track2_slides_v22.html']=ROOT/'notes/track2-slides-v22.html'
    for name in ['pitch','transcript','video-description','reviewer-guide','owner-readiness']:
        suffix='txt' if name=='transcript' else 'md'
        files[f'jvv7_track2_{name}_v22.{suffix}']=ROOT/f'notes/track2-{name}-v22.{suffix}'
    for name in ['track2-transcriptome-v19.md','track2-transcriptome-v19.svg','track2-transcriptome-reproduction-v19.md']:
        files[name]=ROOT/'notes'/name
    for name in ['falsification-review','validation','falsification-register','decision-contract','evidence']:
        suffix='md' if name in {'falsification-review','validation'} else 'json'
        files[f'track2-{name}-v21.{suffix}']=ROOT/f'notes/track2-{name}-v21.{suffix}'
    return files


def verify():
    files=sources()
    with zipfile.ZipFile(DEST) as z:
        release.require(z.testzip() is None,'ZIP CRC failure')
        release.require(set(z.namelist())==set(files)|{'SHA256SUMS.json'} and len(z.namelist())==len(files)+1,
                        'Unexpected bundle contents')
        m=json.loads(z.read('SHA256SUMS.json'))
        release.require(m==dict(files={name:release.digest(path) for name,path in files.items()},
                               scope='Recording and review materials; not a recorded video or submission receipt',
                               upload_ready=False,video_recorded=False), 'Bundle manifest drift')
        for name,path in files.items():
            release.require(z.read(name)==path.read_bytes(), 'Bundled file drift: '+name)
    return dict(verified=True,path=str(DEST.relative_to(ROOT)),files=len(files)+1,
                bytes=DEST.stat().st_size,sha256=release.digest(DEST),upload_ready=False,video_recorded=False)


def build():
    files=sources()
    release.require(not DEST.exists() and not DEST.is_symlink(), 'Existing bundle protected')
    m=dict(files={name:release.digest(path) for name,path in files.items()},
           scope='Recording and review materials; not a recorded video or submission receipt',
           upload_ready=False,video_recorded=False)
    with zipfile.ZipFile(DEST,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for name,path in files.items(): z.write(path,name)
        z.writestr('SHA256SUMS.json',json.dumps(m,indent=2)+'\n')
    return verify()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['build','verify'])
    print(json.dumps({'build':build,'verify':verify}[p.parse_args().command](),indent=2))
