#!/usr/bin/env python3
"""Build/verify current recording materials; this never records or submits a video."""
import argparse
import json
from pathlib import Path
import zipfile
import track2_release_v56 as release

ROOT=release.ROOT
SLIDES=ROOT/'results/feat009/v56-slides-final-20261023-1'
DOCS=ROOT/'results/feat009/v56-documents-final-20261023-1'
DEST=ROOT/'results/feat009/jvv7_track2_video_materials_v56_42.zip'
def sources():
    release.scientific_checks()
    render=json.loads((ROOT/'notes/track2-v56-render-audit-v1.json').read_text())
    docs=json.loads((ROOT/'notes/track2-v56-documents-audit-v1.json').read_text())
    expected={SLIDES/name:sha for name,sha in render['files'].items()}
    expected.update({DOCS/name:sha for name,sha in docs['export']['files'].items()})
    expected.update({DOCS/name:sha for name,sha in docs['pdf']['files'].items()})
    for path,sha in expected.items():
        release.require(path.is_file() and not path.is_symlink() and release.digest(path)==sha,
                        'Export changed or missing: '+path.name)
    files={path.name:path for path in expected if path.suffix != '.html'}
    files['jvv7_track2_slides_v49.html']=ROOT/'notes/track2-slides-v56.html'

    for name in ['track2-transcriptome-v19.md','track2-transcriptome-v19.svg','track2-transcriptome-reproduction-v19.md']:
        files[name]=ROOT/'notes'/name
    for name in ['track2-rnai-v23.md','track2-rnai-v23.svg','track2-rnai-validation-v23.md','track2-rnai-register-v23.json','track2-rnai-tail-sensitivity-v23.json']:
        files[name]=ROOT/'notes'/name
    for name in ['track2-crispr-v25.md','track2-crispr-validation-v25.md','track2-crispr-register-v25.json','track2-crispr-continuity-v25.json','track2-crispr-reproduction-v25.md']:
        files[name]=ROOT/'notes'/name
    for name in ['falsification-review','validation','falsification-register','decision-contract','evidence']:
        suffix='md' if name in {'falsification-review','validation'} else 'json'
        files[f'track2-{name}-v21.{suffix}']=ROOT/f'notes/track2-{name}-v21.{suffix}'
    for name in ['track2-falsification-v27.md','track2-falsification-v27.svg','track2-falsification-register-v27.json','track2-falsification-reproduction-v27.md']:
        files[name]=ROOT/'notes'/name
    for name in ['track2-orthogonal-v29.md','track2-orthogonal-validation-v29.md','track2-orthogonal-register-v29.json','track2-orthogonal-reproduction-v29.md','track2-orthogonal-summary-v29.json','track2-requirements-review-v30.md']:
        files[name]=ROOT/'notes'/name
    for name in ['track2-perturbseq-v31.md','track2-perturbseq-validation-v31.md','track2-perturbseq-register-v31.json','track2-perturbseq-reproduction-v31.md']:
        files[name]=ROOT/'notes'/name
    for name in ['track2-optical-progress-v33.md','track2-optical-source-review-v33.md','track2-optical-status-v33.json','track2-optical-plan-v33.json','track2-optical-amendment-v33.json','track2-requirements-review-v33.md','track2-requirements-v39.json','deletion-plan-v2.md']:
        files[name]=ROOT/'notes'/name
    for source in sorted(p for p in release.OPTICAL_INPUTS if p.startswith('notes/')):
        files[Path(source).name]=ROOT/source
    # Preserve only frozen v40 own-voice assets with unambiguous owner-facing names.
    for source in sorted(release.INPUTS):
        if source in {'notes/track2-pitch-v56.md','notes/track2-transcript-v56.txt','notes/track2-teleprompter-v56.html','notes/track2-narration-v56.json','notes/track2-recording-guide-v56.md','notes/track2-video-description-v56.md'}:files['jvv7_'+Path(source).name]=ROOT/source
    files['jvv7_track2_external-review-packet_v49.md']=ROOT/'notes/track2-external-review-packet-v49.md'
    files['jvv7_track2_reviewer-brief_v50.md']=ROOT/'notes/track2-reviewer-brief-v50.md'
    files['jvv7_track2_video-description_v47.md']=ROOT/'notes/track2-video-description-v47.md'
    files['jvv7_track2_judge-questions_v43.md']=ROOT/'notes/track2-judge-questions-v43.md'
    files['jvv7_track2_community-kit_v42.md']=ROOT/'notes/track2-community-kit-v42.md'
    files['jvv7_track2_recording-guide_v46.md']=ROOT/'notes/track2-recording-guide-v46.md'
    files['jvv7_track2_competition-strategy_v42.md']=ROOT/'notes/track2-competition-strategy-v42.md'
    files['jvv7_track2_lab-handoff_v43.md']=ROOT/'notes/track2-lab-handoff-v43.md'
    files['jvv7_track2_candidate-comparison_v51.md']=ROOT/'notes/track2-candidate-comparison-v51.md'
    files['jvv7_track2_requirements-review_v52.md']=ROOT/'notes/track2-requirements-review-v52.md'
    files['jvv7_track2_requirements-v52.json']=ROOT/'notes/track2-requirements-v52.json'
    files['jvv7_check_track2_requirements_v52.py']=ROOT/'scripts/check_track2_requirements_v52.py'
    files['jvv7_test_track2_requirements_v52.py']=ROOT/'scripts/test_track2_requirements_v52.py'
    files['jvv7_check_track2_submission_prep_v3.py']=ROOT/'scripts/check_track2_submission_prep_v3.py'
    files['jvv7_test_track2_submission_prep_v3.py']=ROOT/'scripts/test_track2_submission_prep_v3.py'
    files['jvv7_track2-submission-materials_v5.json']=ROOT/'notes/track2-submission-materials-v5.json'
    files['jvv7_track2-literature_v45.md']=ROOT/'notes/track2-literature-v45.md'
    files['jvv7_track2-external-review_v46.md']=ROOT/'notes/track2-external-review-v46.md'
    files['jvv7_track2-prompter-audit_v46.json']=ROOT/'notes/track2-prompter-audit-v46.json'
    files['jvv7_track2-literature-audit_v45.json']=ROOT/'notes/track2-literature-audit-v45.json'
    files['jvv7_check_track2_literature_v45.py']=ROOT/'scripts/check_track2_literature_v45.py'
    files['jvv7_test_track2_literature_v45.py']=ROOT/'scripts/test_track2_literature_v45.py'
    for name in ['reviewer-guide','owner-readiness']:
        files[f'jvv7_track2_{name}_v48.md']=ROOT/f'notes/track2-{name}-v48.md'
    # Preserve the reusable demo and its complete runnable kit in the recording bundle.
    from track2_community_kit_v37 import verify as verify_kit
    verify_kit()
    for name in ['track2-demo-v37.html','track2-demo-cases-v37.json','track2-community-kit-v37.md']:
        files[name]=ROOT/'notes'/name
    files['jvv7_track2_community_kit_v37.zip']=ROOT/'results/feat009/jvv7_track2_community_kit_v37.zip'
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
