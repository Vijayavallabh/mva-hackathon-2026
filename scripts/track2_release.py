#!/usr/bin/env python3
"""Build/verify a v3 research snapshot while preserving the reviewed v2 package.

Offline integrity and disclosure checks only; never uploads, prescribes or verifies
scientific efficacy. No subject input. All package paths are fixed below.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

import track2_evidence as base

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / 'results/feat009/jvv7_track2_research_v2'
FILES = {
    'jvv7_track2_report_v3.md': 'notes/track2-report-v3.md',
    'jvv7_track2_pitch_v3.md': 'notes/track2-pitch-v3.md',
    'sources.json': 'notes/track2-sources.json',
    'candidates.json': 'notes/track2-candidates.json',
    'exposure.json': 'notes/track2-exposure.json',
    'validation-plan.md': 'notes/track2-validation.md',
    'validation-addendum.md': 'notes/track2-validation-v3.md',
    'scientific-exposure-review.md': 'notes/track2-final-review.md',
    'firecrawl-scientific-review.md': 'notes/track2-firecrawl-scientific-review.md',
    'firecrawl-capabilities.md': 'notes/firecrawl-capability-review.md',
    'firecrawl-run-review.md': 'notes/track2-firecrawl.md',
    'alphagenome-authenticated.md': 'notes/alphagenome-authenticated-results.md',
    'alphagenome-splicing.md': 'notes/alphagenome-splicing-results.md',
    'alphagenome-score-semantics.md': 'notes/alphagenome-score-semantics.md',
    'alphagenome-splicing-semantics.md': 'notes/alphagenome-splicing-semantics.md',
}
INPUTS = set(FILES.values()) | base.INPUT_PATHS | {
    'scripts/track2_release.py', 'scripts/track2_firecrawl.py',
    'scripts/test_track2_release.py', 'scripts/test_track2_firecrawl.py',
}


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    require(path.is_file() and not path.is_symlink(), 'missing or symlinked release input')
    return base.sha256(path)


def boundaries(report, pitch):
    report = re.sub(r'\s+', ' ', report).strip()
    pitch = re.sub(r'\s+', ' ', pitch).strip()
    for word in ('research draft 3', 'trans phase remains unconfirmed', 'Fireworks', 'GLM',
                 'Google DeepMind', 'not used to train', 'Acknowledgement', 'pralatrexate',
                 '0.08699', '0.04813', 'mitotic slippage'):
        require(word.lower() in report.lower(), 'missing v3 report boundary/disclosure: ' + word)
    require('no other ai providers have been used' not in report.lower(), 'obsolete provider attestation in v3 report')
    for word in ('Fireworks', 'Google DeepMind', 'phase unconfirmed', 'not a recorded'):
        require(word.lower() in pitch.lower(), 'missing v3 pitch boundary/disclosure: ' + word)


def location(path):
    require(not path.is_symlink(), 'symlinked package directory')
    path = path.resolve()
    require(path.is_relative_to(ROOT / 'results/feat009') and path != ROOT / 'results/feat009',
            'release must be a new subdirectory of results/feat009')
    require(not path.is_relative_to(V2.resolve()) and not path.is_relative_to(ROOT / 'results/feat009/jvv7_track2_research_v1'),
            'historical snapshots and their descendants are immutable')
    return path


def current_inputs():
    return {name: digest(ROOT / name) for name in sorted(INPUTS)}


def build(path):
    path = location(path)
    require(not path.exists(), 'release destination exists; never overwrite')
    base.verify(V2)
    sources, candidates = base.load_ledgers()
    boundaries((ROOT / FILES['jvv7_track2_report_v3.md']).read_text(),
               (ROOT / FILES['jvv7_track2_pitch_v3.md']).read_text())
    inputs = current_inputs()
    path.mkdir(parents=True, exist_ok=False)
    for name, source in FILES.items():
        shutil.copyfile(ROOT / source, path / name)
    manifest = {'schema_version': 3, 'stage': 'research_draft_not_submitted',
        'created_utc': datetime.now(timezone.utc).isoformat(), 'upload_performed': False,
        'video_url': None, 'upload_ready': False, 'phase': 'unconfirmed',
        'clinical_exposure_margin': None, 'base_ledger_checks': base.validate(sources, candidates),
        'historical_v2_manifest_sha256': digest(V2 / 'manifest.json'),
        'track1': base.check_track1(), 'input_hashes': inputs,
        'files': {name: digest(path / name) for name in sorted(FILES)},
        'additional_sources': 'New public-source horizon evidence is in firecrawl-scientific-review.md; it does not silently alter the 53-source/12-candidate baseline ledgers.',
        'remaining_gates': ['recorded three-minute hosted video', 'final owner review',
                            'live rules, disclosure and authenticated quota checks', 'portal upload and receipt'],
        'limits': 'Hashes are drift checks, not signatures, scientific validity or clinical readiness.'}
    require(inputs == current_inputs(), 'inputs changed during build')
    (path / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return verify(path)


def verify(path):
    path = location(path)
    digest(path / 'manifest.json')
    m = json.loads((path / 'manifest.json').read_text())
    require(m.get('schema_version') == 3 and m.get('stage') == 'research_draft_not_submitted', 'wrong release stage')
    require(m.get('upload_performed') is False and m.get('upload_ready') is False and m.get('video_url') is None,
            'draft cannot claim a video or upload readiness')
    require(m.get('phase') == 'unconfirmed' and 'clinical_exposure_margin' in m and m['clinical_exposure_margin'] is None,
            'phase and exposure remain unestablished')
    require(set(m.get('files', {})) == set(FILES), 'manifest file set mismatch')
    require({p.name for p in path.iterdir()} == set(FILES) | {'manifest.json'}, 'package file set mismatch')
    require(m.get('input_hashes') == current_inputs(), 'current-input drift; build a new snapshot')
    for name, source in FILES.items():
        require(digest(path / name) == m['files'][name] == m['input_hashes'][source], 'package file hash/source mismatch')
    boundaries((path / 'jvv7_track2_report_v3.md').read_text(), (path / 'jvv7_track2_pitch_v3.md').read_text())
    base.verify(V2)
    require(m.get('historical_v2_manifest_sha256') == digest(V2 / 'manifest.json'), 'historical v2 changed')
    require(m.get('track1') == base.check_track1(), 'Track 1 preservation mismatch')
    sources = json.loads((path / 'sources.json').read_text())
    candidates = json.loads((path / 'candidates.json').read_text())
    require(m.get('base_ledger_checks') == base.validate(sources, candidates), 'baseline ledger mismatch')
    return {'integrity_verified': True, 'files': len(FILES), 'upload_ready': False,
            'phase': 'unconfirmed', 'historical_v2_preserved': True,
            'report_sha256': m['files']['jvv7_track2_report_v3.md']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['build', 'verify'])
    p.add_argument('output', type=Path)
    args = p.parse_args()
    print(json.dumps({'build': build, 'verify': verify}[args.command](args.output), indent=2))


if __name__ == '__main__':
    main()
