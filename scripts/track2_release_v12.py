#!/usr/bin/env python3
"""Website-aligned v12 presentation and report; unchanged v10 science, no upload."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil

import track2_release_v11 as previous
import track2_release_v5 as static
from track2_release_v7 import Content

foundation = previous.foundation

ROOT = previous.ROOT
require = previous.require
digest = previous.digest
checked_path = previous.checked_path
read_json = previous.read_json
FILES = {
    'jvv7_track2_slides_v12.html': 'notes/track2-slides-v12.html',
    'jvv7_track2_pitch_v12.md': 'notes/track2-pitch-v12.md',
    'jvv7_track2_report_v12.md': 'notes/track2-report-v12.md',
    'validation-v10.md': 'notes/track2-validation-v10.md',
    'evidence-v10.json': 'notes/track2-evidence-v10.json',
    'falsification-review-v10.md': 'notes/track2-falsification-cycle1.md',
    'website-review-v12.md': 'notes/track2-challenge-review-20260919.md',
    'video-description-v12.md': 'notes/track2-video-description-v12.md',
}
INPUTS = previous.INPUTS | set(FILES.values()) | {
    'scripts/track2_release_v12.py', 'scripts/render_track2_slides_v12.mjs',
    'scripts/test_track2_release_v12.py', 'scripts/track2_challenge_review.py',
}
SCOPE = 'Website-aligned seven-page presentation and methods report; unchanged v10 science, no recording or upload.'
FIELDS = {'schema_version', 'created_utc', 'files', 'input_hashes', 'historical_v11_manifest',
          'presentation', 'scope', 'upload_ready', 'upload_performed', 'video_url',
          'provider_settings_verified', 'phase', 'clinical_exposure_margin'}
REQUIRED = {**{n: previous.REQUIRED[n] for n in range(2, 6)},
    1: ('everolimus', 'bub1b', 'non-cancer cells', 'mechanistic probe',
        'approved mtorc1 inhibitor; mva use unproven', 'stop-gain suggests loss of function',
        'missense effect and trans phase unconfirmed'),
    6: ('impact', 'innovation', 'scalability', 'requalify each model',
        'advance: function + safety + exposure + replication',
        'stop if unmet or unresolved; pause unexplained bubr1 loss',
        'no rescue priority', 'hcq reserve', 'clinical exposure margin unknown',
        'trans phase unconfirmed', 'no experiments performed', 'fireworks training/retention unverified'),
    7: ('with thanks to the child,', 'full acknowledgement'),
}

LABEL = 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2'
LINKS = previous.LINKS + (LABEL,
    'https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v12.md',
    'https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/1c761cc23d90aebe6a011fd5b0b99517df42408c/tabs/rules.py')


def normalized(text):
    return re.sub(r'\s+', ' ', text).strip()


def acknowledgement():
    return checked_path(ROOT / 'notes/track2-report-v10.md').read_text().split('## Acknowledgement\n', 1)[1].strip()



class DeckParser(static.DeckParser):
    # Keep the reviewed static element/resource policy; only cardinality changes.
    def validate(self):
        require(not self.stack and self.html_count == 1, 'incomplete HTML document')
        require(self.csp_count == 1, 'exactly one restrictive CSP is required')
        require(self.sections == [f'slide-{n}' for n in range(1, 8)], 'exactly seven ordered slides required')
        require(self.svg_count == 6 and self.section_vectors == [1] * 6 + [0], 'six figures followed by a text acknowledgement required')


def presentation_checks(deck):
    parser = DeckParser()
    parser.feed(deck)
    parser.close()
    parser.validate()
    content = Content()
    content.feed(deck)
    slides = [' '.join(s).lower() for s in content.sections]
    require(previous.previous.REMOVED_LINE not in slides[0], 'owner-requested cover line was restored')
    for n, phrases in REQUIRED.items():
        for phrase in phrases:
            require(phrase in slides[n-1], f'missing slide {n} evidence boundary: {phrase}')
    require(set(LINKS) <= set(content.links), 'missing primary/protocol source link')
    # The already-validated historical plot is preserved exactly, now on slide 4.
    previous.check_deck()
    old = checked_path(ROOT / 'notes/track2-slides-v11.html').read_text()
    pattern = r'<svg id="arst1431-plot".*?</svg>'
    plots, prior = re.findall(pattern, deck, re.S), re.findall(pattern, old, re.S)
    require(len(plots) == len(prior) == 1 and plots == prior, 'published ARST1431 plot changed')
    fourth = re.search(r'<section[^>]+id="slide-4".*?</section>', deck, re.S)
    require(fourth is not None and plots[0] in fourth.group(), 'plot must be on slide 4')
    require(normalized(acknowledgement()).lower() in slides[6], 'full visible acknowledgement required')
    return {'slides': 7, 'vector_figures': 6, 'schematic_figures': 5,
        'published_data_plots': 1, 'requested_cover_line_removed': True,
        'scientific_content_checks_passed': True, 'visible_words': [len(s) for s in content.sections],
        'arst1431_hr': 0.86, 'arst1431_ci_95': [0.58, 1.26],
        'static_resource_policy': 'local_css_and_inline_svg_only'}


def check_deck():
    payload = checked_path(ROOT / 'notes/track2-slides-v12.html').read_bytes()
    return {'static_deck_verified': True, 'source_sha256': hashlib.sha256(payload).hexdigest(),
            **presentation_checks(payload.decode('utf-8'))}


def narration_checks(pitch):
    require(pitch.count('## Narration\n') == pitch.count('## Recording notes') == 1, 'missing narration delimiters')
    spoken = pitch.split('## Narration\n', 1)[1].split('## Recording notes', 1)[0]
    headings = re.findall(r'### Slide (\d+) / [^\n]+', spoken)
    require(headings == list('1234567'), 'seven ordered narration sections required')
    parts = re.split(r'### Slide [^\n]+\n', spoken)[1:]
    counts = [len(p.split()) for p in parts]
    require(320 <= sum(counts) <= 365, 'narration exceeds declared three-minute planning range')
    phrases = ('approved mtorc1 inhibitor', 'missense effect and phase remain unconfirmed',
        'mechanistic probe', 'force improvement', 'different models',
        'does not establish everolimus benefit here', 'neither is established',
        'no switching after failure', 'daughter survival and tracking loss separately',
        'whole blood is not free tissue exposure', 'hcq remains reserve',
        'pause unexplained bubr1 loss', 'requalify each model',
        'no rescue priority, clinical margin or experimental result is established',
        'fireworks training and retention remain unverified')
    flat = re.sub(r'\s+', ' ', spoken).lower()
    require(all(p in flat for p in phrases), 'missing spoken scientific boundary')
    require(f'Narration contains {sum(counts)} whitespace-separated words' in pitch, 'incorrect word count')
    require('/'.join(map(str, counts)) in pitch, 'incorrect per-slide word count')
    return {'narration_words': sum(counts), 'words_per_slide': counts, 'runtime_measured': False}


def report_checks(report, description):
    old = checked_path(ROOT / 'notes/track2-report-v10.md').read_text()
    require(report.split('## 1.', 1)[1].split('## 7.', 1)[0] ==
            old.split('## 1.', 1)[1].split('## 7.', 1)[0], 'scientific sections 1-6 changed')
    ack = normalized(acknowledgement())
    for text in (report, description):
        require(normalized(text.split('## Acknowledgement\n', 1)[1]) == ack,
                'full acknowledgement changed')
        flat = normalized(text).lower()
        require('training and retention' in flat or 'training/retention' in flat,
                'provider policy disclosure missing')
        require('unverified' in flat, 'provider policy uncertainty missing')
    require(all(f'**A{i} — ' in report for i in range(7, 18)), 'missing template answer')
    abstract = report.split('**A17 — Method abstract (under 500 words).**', 1)[1].split('## Acknowledgement', 1)[0]
    require(100 <= len(abstract.split()) <= 500, 'abstract outside declared word limit')
    for phrase in ('Scientific rigor — 35%', 'Potential impact — 25%', 'Innovation — 25%',
                   'Scalability — 15%', 'Total person-hours', 'have not been',
                   'Three entries are allowed; only the latest is reviewed'):
        require(phrase in report, f'missing methods/rubric boundary: {phrase}')
    return {'scientific_sections_1_through_6_preserved': True, 'template_answers': 11,
            'abstract_words': len(abstract.split()), 'full_acknowledgement_in_report_and_description': True}


def scientific_checks():
    result = previous.scientific_checks()
    return {**result,
        **narration_checks(checked_path(ROOT / 'notes/track2-pitch-v12.md').read_text()),
        **report_checks(checked_path(ROOT / 'notes/track2-report-v12.md').read_text(),
                        checked_path(ROOT / 'notes/track2-video-description-v12.md').read_text())}


def inputs():
    return {name: digest(ROOT / name) for name in sorted(INPUTS)}


def history():
    path = checked_path(ROOT / 'results/feat009/jvv7_track2_research_v11')
    require(previous.verify(path)['integrity_verified'] is True, 'historical v11 failed')
    return digest(path / 'manifest.json')


def location(path):
    path = checked_path(path)
    require(path.parent == ROOT / 'results/feat009', 'snapshot must be a direct feat009 child')
    require(re.fullmatch(r'[a-z0-9][a-z0-9_-]*', path.name), 'invalid snapshot name')
    require(path.name not in {f'jvv7_track2_research_v{i}' for i in range(1, 12)},
            'historical snapshots are immutable')
    return path


def build(path):
    path = location(path)
    require(not path.exists(), 'output exists; use a new snapshot')
    scientific_checks()
    before, historical, presentation = inputs(), history(), check_deck()
    path.mkdir(exist_ok=False)
    for name, source in FILES.items():
        shutil.copyfile(checked_path(ROOT / source), path / name)
    copies = {name: digest(path / name) for name in FILES}
    require(all(copies[name] == before[source] for name, source in FILES.items()), 'copy drift')
    require(inputs() == before and history() == historical, 'input or historical drift')
    manifest = {'schema_version': 12, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'files': copies, 'input_hashes': before, 'historical_v11_manifest': historical,
        'presentation': presentation, 'scope': SCOPE, 'upload_ready': False,
        'upload_performed': False, 'video_url': None, 'provider_settings_verified': False,
        'phase': 'unconfirmed', 'clinical_exposure_margin': None}
    with (path / 'manifest.json').open('x') as handle:
        handle.write(json.dumps(manifest, indent=2) + '\n')
    return verify(path)


def verify(path):
    scientific_checks()
    path = location(path)
    manifest = read_json(path / 'manifest.json')
    foundation.exact_keys(manifest, FIELDS, 'manifest')
    require(type(manifest['schema_version']) is int and manifest['schema_version'] == 12,
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
    require(manifest['historical_v11_manifest'] == history(), 'historical drift')
    require(foundation.same_json(manifest['presentation'], check_deck()), 'presentation drift')
    return {'integrity_verified': True, 'files': len(FILES), 'bound_inputs': len(INPUTS),
            'historical_v1_through_v11_preserved': True, 'upload_ready': False,
            'cover_line_removed_and_scientific_checks_passed': True,
            'deck_sha256': manifest['files']['jvv7_track2_slides_v12.html']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check-deck', 'check', 'build', 'verify'])
    parser.add_argument('output', type=Path, nargs='?')
    args = parser.parse_args()
    if args.command == 'check':
        if args.output is not None:
            parser.error('check uses only the fixed v12 inputs')
        result = scientific_checks()
    elif args.command == 'check-deck':
        if args.output is not None:
            parser.error('check-deck uses only the fixed v12 source')
        result = check_deck()
    else:
        if args.output is None:
            parser.error('build and verify require an output directory')
        result = {'build': build, 'verify': verify}[args.command](args.output)
    print(json.dumps(result, indent=2))
