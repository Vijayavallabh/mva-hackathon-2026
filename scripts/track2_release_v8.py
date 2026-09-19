#!/usr/bin/env python3
"""Scientifically aligned Track 2 presentation snapshot using the unchanged v6 report and narration."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil

import track2_release_v7 as previous

foundation = previous.previous

ROOT = previous.ROOT
require = previous.require
digest = previous.digest
checked_path = previous.checked_path
read_json = previous.read_json
FILES = {
    'jvv7_track2_slides_v8.html': 'notes/track2-slides-v8.html',
    'jvv7_track2_report_v6.md': 'notes/track2-report-v6.md',
    'jvv7_track2_pitch_v6.md': 'notes/track2-pitch-v6.md',
    'validation-v5.md': 'notes/track2-validation-v5.md',
    'evidence-v4.json': 'notes/track2-evidence-v4.json',
    'v8-design-and-use.md': 'notes/track2-v8-design.md',
}
INPUTS = previous.INPUTS | set(FILES.values()) | {
    'scripts/track2_release_v8.py', 'scripts/render_track2_slides_v8.mjs',
    'scripts/test_track2_release_v8.py',
}
SCOPE = 'Owner-requested cover-line removal and scientific visual revision; use the unchanged v6 report and narration with the v8 deck.'
FIELDS = {'schema_version', 'created_utc', 'files', 'input_hashes', 'historical_v7_manifest',
          'presentation', 'scope', 'upload_ready', 'upload_performed', 'video_url',
          'provider_settings_verified', 'phase', 'clinical_exposure_margin'}


# Reuse the reviewed static parser and exact published-plot geometry checks.
# Content checks are specific to the new presentation, not clinical validation.
REQUIRED = {
    1: ('everolimus', 'bub1b', 'non-cancer cells', 'bubr1 checkpoint'),
    2: ('different bubr1 alleles', 'phospho-p70 s6 kinase', 'phospho-4ebp1',
        'no rapalog rescue tested', 'first confirm mtorc1 excess',
        'only if excess is present', 'unproven transfer', 'function + safety'),
    3: ('arst1431', '297 evaluable', 'hr 0.86', '95% ci 0.58-1.26',
        'p = 0.44', 'does not test non-cancer everolimus rescue'),
    4: ('tissue-relevant function', 'deficient vs corrected', 'vehicle vs everolimus',
        'cis / trans / single / wt', 'first division', 'accurate / error',
        'daughter survival', 'death', 'arrest / slippage', 'tracking loss'),
    5: ('function', 'safety', 'exposure', 'replication', 'all four required',
        'stop if any criterion is unmet or unresolved', 'clinical exposure margin unknown',
        'trans phase unconfirmed', 'google deepmind', 'fireworks training/retention unverified'),
}
REMOVED_LINE = 'research only. trans phase unconfirmed. no experiments performed.'


def presentation_checks(deck):
    parser = foundation.DeckParser()
    parser.feed(deck)
    parser.close()
    parser.validate()
    content = previous.Content()
    content.feed(deck)
    slides = [' '.join(words).lower() for words in content.sections]
    require(REMOVED_LINE not in slides[0], 'owner-requested cover line was restored')
    for number, phrases in REQUIRED.items():
        for phrase in phrases:
            require(phrase in slides[number - 1], f'missing slide {number} evidence boundary: {phrase}')
    for link in ('https://doi.org/10.1038/ng1449',
                 'https://www.jci.org/articles/view/126863',
                 'https://doi.org/10.1172/JCI126863',
                 'https://doi.org/10.1172/JCI144781',
                 'https://doi.org/' + foundation.ARST1431_DOI,
                 'https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation-v5.md'):
        require(link in content.links, 'missing presentation source link')
    return {'slides': 5, 'vector_figures': 5, 'schematic_figures': 4,
            'published_data_plots': 1, 'requested_cover_line_removed': True,
            'scientific_content_checks_passed': True,
            'arst1431_hr': 0.86, 'arst1431_ci_95': [0.58, 1.26],
            'static_resource_policy': 'local_css_and_inline_svg_only'}


def check_deck():
    payload = checked_path(ROOT / 'notes/track2-slides-v8.html').read_bytes()
    return {'static_deck_verified': True, 'source_sha256': hashlib.sha256(payload).hexdigest(),
            **presentation_checks(payload.decode('utf-8'))}


def inputs():
    return {name: digest(ROOT / name) for name in sorted(INPUTS)}


def history():
    path = checked_path(ROOT / 'results/feat009/jvv7_track2_research_v7')
    require(previous.verify(path)['integrity_verified'] is True, 'historical v7 failed')
    return digest(path / 'manifest.json')


def location(path):
    path = checked_path(path)
    require(path.parent == ROOT / 'results/feat009', 'snapshot must be a direct feat009 child')
    require(re.fullmatch(r'[a-z0-9][a-z0-9_-]*', path.name), 'invalid snapshot name')
    require(path.name not in {f'jvv7_track2_research_v{i}' for i in range(1, 8)},
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
    manifest = {'schema_version': 8, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'files': copies, 'input_hashes': before, 'historical_v7_manifest': historical,
        'presentation': presentation, 'scope': SCOPE, 'upload_ready': False,
        'upload_performed': False, 'video_url': None, 'provider_settings_verified': False,
        'phase': 'unconfirmed', 'clinical_exposure_margin': None}
    with (path / 'manifest.json').open('x') as handle:
        handle.write(json.dumps(manifest, indent=2) + '\n')
    return verify(path)


def verify(path):
    path = location(path)
    manifest = read_json(path / 'manifest.json')
    foundation.exact_keys(manifest, FIELDS, 'manifest')
    require(type(manifest['schema_version']) is int and manifest['schema_version'] == 8,
            'wrong schema version')
    require(manifest['scope'] == SCOPE, 'scope changed')
    for key in ('upload_ready', 'upload_performed', 'provider_settings_verified'):
        require(manifest[key] is False, 'draft readiness changed')
    require(manifest['video_url'] is None and manifest['clinical_exposure_margin'] is None
            and manifest['phase'] == 'unconfirmed', 'scientific or delivery state changed')
    timestamp = datetime.fromisoformat(manifest['created_utc'])
    require(timestamp.tzinfo is not None and timestamp.utcoffset().total_seconds() == 0,
            'creation timestamp must be UTC')
    foundation.exact_keys(manifest['files'], FILES, 'file')
    require({p.name for p in path.iterdir()} == set(FILES) | {'manifest.json'}, 'unexpected file set')
    require(manifest['input_hashes'] == inputs(), 'input drift')
    for name, source in FILES.items():
        require(digest(path / name) == manifest['files'][name] == manifest['input_hashes'][source],
                'copied file drift')
    require(manifest['historical_v7_manifest'] == history(), 'historical drift')
    require(foundation.same_json(manifest['presentation'], check_deck()), 'presentation drift')
    return {'integrity_verified': True, 'files': len(FILES), 'bound_inputs': len(INPUTS),
            'historical_v1_through_v7_preserved': True, 'upload_ready': False,
            'cover_line_removed_and_scientific_checks_passed': True,
            'deck_sha256': manifest['files']['jvv7_track2_slides_v8.html']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check-deck', 'build', 'verify'])
    parser.add_argument('output', type=Path, nargs='?')
    args = parser.parse_args()
    if args.command == 'check-deck':
        if args.output is not None:
            parser.error('check-deck uses only the fixed v8 source')
        result = check_deck()
    else:
        if args.output is None:
            parser.error('build and verify require an output directory')
        result = {'build': build, 'verify': verify}[args.command](args.output)
    print(json.dumps(result, indent=2))
