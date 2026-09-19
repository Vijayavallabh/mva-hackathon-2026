#!/usr/bin/env python3
"""Visual-only Track 2 snapshot using the unchanged v6 report and narration."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil

import track2_release_v6 as previous

ROOT = previous.ROOT
require = previous.require
digest = previous.digest
checked_path = previous.checked_path
read_json = previous.read_json
FILES = {
    'jvv7_track2_slides_v7.html': 'notes/track2-slides-v7.html',
    'jvv7_track2_report_v6.md': 'notes/track2-report-v6.md',
    'jvv7_track2_pitch_v6.md': 'notes/track2-pitch-v6.md',
    'validation-v5.md': 'notes/track2-validation-v5.md',
    'evidence-v4.json': 'notes/track2-evidence-v4.json',
    'v7-design-and-use.md': 'notes/track2-v7-design.md',
}
INPUTS = previous.INPUTS | set(FILES.values()) | {
    'scripts/track2_release_v7.py', 'scripts/render_track2_slides_v7.mjs',
    'scripts/test_track2_release_v7.py',
}
SCOPE = 'Visual refinement only; use the unchanged v6 report and 297-word narration with the v7 deck.'
FIELDS = {'schema_version', 'created_utc', 'files', 'input_hashes', 'historical_v6_manifest',
          'presentation', 'scope', 'upload_ready', 'upload_performed', 'video_url',
          'provider_settings_verified', 'phase', 'clinical_exposure_margin'}


class Content(HTMLParser):
    """Compare displayed wording per slide, independently of layout and line breaks."""
    def __init__(self):
        super().__init__()
        self.sections = []
        self.links = []
        self.in_section = False
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'section':
            self.in_section = True
            self.sections.append([])
        if tag in {'title', 'desc', 'style'}:
            self.hidden += 1
        if self.in_section and tag == 'a':
            self.links.append(dict(attrs).get('href'))

    def handle_endtag(self, tag):
        if tag == 'section':
            self.in_section = False
        if tag in {'title', 'desc', 'style'}:
            self.hidden -= 1

    def handle_data(self, data):
        if self.in_section and not self.hidden:
            self.sections[-1].extend(data.split())


def check_deck():
    payload = checked_path(ROOT / 'notes/track2-slides-v7.html').read_bytes()
    deck = payload.decode('utf-8')
    presentation = previous.presentation_checks(deck)
    a, b = Content(), Content()
    a.feed(deck)
    b.feed(checked_path(ROOT / 'notes/track2-slides-v6.html').read_text())
    require(a.sections == b.sections and a.links == b.links,
            'visual revision changed slide wording or source links')
    return {'static_deck_verified': True, 'source_sha256': hashlib.sha256(payload).hexdigest(),
            'v6_slide_wording_and_links_preserved': True, **presentation}


def inputs():
    return {name: digest(ROOT / name) for name in sorted(INPUTS)}


def history():
    path = checked_path(ROOT / 'results/feat009/jvv7_track2_research_v6')
    require(previous.verify(path)['integrity_verified'] is True, 'historical v6 failed')
    return digest(path / 'manifest.json')


def location(path):
    path = checked_path(path)
    require(path.parent == ROOT / 'results/feat009', 'snapshot must be a direct feat009 child')
    require(re.fullmatch(r'[a-z0-9][a-z0-9_-]*', path.name), 'invalid snapshot name')
    require(path.name not in {f'jvv7_track2_research_v{i}' for i in range(1, 7)},
            'historical snapshots are immutable')
    return path


def build(path):
    path = location(path)
    require(not path.exists(), 'output exists; use a new snapshot')
    before, historical, presentation = inputs(), history(), check_deck()
    path.mkdir(exist_ok=False)
    for name, source in FILES.items():
        shutil.copyfile(checked_path(ROOT / source), path / name)
    copies = {name: digest(path / name) for name in FILES}
    require(all(copies[name] == before[source] for name, source in FILES.items()), 'copy drift')
    require(inputs() == before and history() == historical, 'input or historical drift')
    manifest = {'schema_version': 7, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'files': copies, 'input_hashes': before, 'historical_v6_manifest': historical,
        'presentation': presentation, 'scope': SCOPE, 'upload_ready': False,
        'upload_performed': False, 'video_url': None, 'provider_settings_verified': False,
        'phase': 'unconfirmed', 'clinical_exposure_margin': None}
    with (path / 'manifest.json').open('x') as handle:
        handle.write(json.dumps(manifest, indent=2) + '\n')
    return verify(path)


def verify(path):
    path = location(path)
    manifest = read_json(path / 'manifest.json')
    previous.exact_keys(manifest, FIELDS, 'manifest')
    require(type(manifest['schema_version']) is int and manifest['schema_version'] == 7,
            'wrong schema version')
    require(manifest['scope'] == SCOPE, 'scope changed')
    for key in ('upload_ready', 'upload_performed', 'provider_settings_verified'):
        require(manifest[key] is False, 'draft readiness changed')
    require(manifest['video_url'] is None and manifest['clinical_exposure_margin'] is None
            and manifest['phase'] == 'unconfirmed', 'scientific or delivery state changed')
    timestamp = datetime.fromisoformat(manifest['created_utc'])
    require(timestamp.tzinfo is not None and timestamp.utcoffset().total_seconds() == 0,
            'creation timestamp must be UTC')
    previous.exact_keys(manifest['files'], FILES, 'file')
    require({p.name for p in path.iterdir()} == set(FILES) | {'manifest.json'}, 'unexpected file set')
    require(manifest['input_hashes'] == inputs(), 'input drift')
    for name, source in FILES.items():
        require(digest(path / name) == manifest['files'][name] == manifest['input_hashes'][source],
                'copied file drift')
    require(manifest['historical_v6_manifest'] == history(), 'historical drift')
    require(previous.same_json(manifest['presentation'], check_deck()), 'presentation drift')
    return {'integrity_verified': True, 'files': len(FILES), 'bound_inputs': len(INPUTS),
            'historical_v1_through_v6_preserved': True, 'upload_ready': False,
            'slide_wording_and_source_links_unchanged': True,
            'deck_sha256': manifest['files']['jvv7_track2_slides_v7.html']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check-deck', 'build', 'verify'])
    parser.add_argument('output', type=Path, nargs='?')
    args = parser.parse_args()
    if args.command == 'check-deck':
        if args.output is not None:
            parser.error('check-deck uses only the fixed v7 source')
        result = check_deck()
    else:
        if args.output is None:
            parser.error('build and verify require an output directory')
        result = {'build': build, 'verify': verify}[args.command](args.output)
    print(json.dumps(result, indent=2))
