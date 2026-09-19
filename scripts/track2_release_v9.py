#!/usr/bin/env python3
"""Adversarially revised Track 2 snapshot; evidence checks and immutable history, no upload."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil

import track2_release_v8 as previous

foundation = previous.foundation

ROOT = previous.ROOT
require = previous.require
digest = previous.digest
checked_path = previous.checked_path
read_json = previous.read_json
FILES = {
    'jvv7_track2_slides_v9.html': 'notes/track2-slides-v9.html',
    'jvv7_track2_report_v9.md': 'notes/track2-report-v9.md',
    'jvv7_track2_pitch_v9.md': 'notes/track2-pitch-v9.md',
    'validation-v9.md': 'notes/track2-validation-v9.md',
    'evidence-v9.json': 'notes/track2-evidence-v9.json',
    'adversarial-review-v9.md': 'notes/track2-adversarial-v9.md',
}
INPUTS = previous.INPUTS | set(FILES.values()) | {
    'scripts/track2_release_v9.py', 'scripts/render_track2_slides_v9.mjs',
    'scripts/test_track2_release_v9.py',
}
SCOPE = 'Adversarial revision: everolimus is a mechanistic probe only; revised evidence, protocol and presentation; no rescue-priority candidate.'
FIELDS = {'schema_version', 'created_utc', 'files', 'input_hashes', 'historical_v8_manifest',
          'presentation', 'scope', 'upload_ready', 'upload_performed', 'video_url',
          'provider_settings_verified', 'phase', 'clinical_exposure_margin'}


# Reuse the reviewed static parser and exact published-plot geometry checks.
# Content checks are specific to the new presentation, not clinical validation.
REQUIRED = {
    1: ('everolimus', 'bub1b', 'non-cancer cells', 'bubr1 checkpoint'),
    2: ('different bubr1 alleles', 'phospho-p70 s6 kinase', 'phospho-4ebp1',
        'no rapalog rescue tested', 'human stromal cells', 'late passage; not this genotype',
        '50 nm / 24 h', 'nominal culture exposure', 'bubr1 protein',
        'test function and harm', 'higher mtorc1 alone is insufficient'),
    3: ('arst1431', '297 evaluable', 'hr 0.86', '95% ci 0.58-1.26',
        'p = 0.44', 'does not test non-cancer everolimus rescue'),
    4: ('tissue-relevant function', 'deficient vs corrected', 'vehicle vs everolimus',
        'cis / trans / single / wt', 'first division', 'accurate / error',
        'daughter survival', 'death', 'arrest / slippage', 'tracking loss', 'track bubr1 + flux'),
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
    content = previous.previous.Content()
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
                 'https://doi.org/10.1016/j.redox.2023.102701',
                 'https://doi.org/' + foundation.ARST1431_DOI,
                 'https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation-v9.md'):
        require(link in content.links, 'missing presentation source link')
    return {'slides': 5, 'vector_figures': 5, 'schematic_figures': 4,
            'published_data_plots': 1, 'requested_cover_line_removed': True,
            'scientific_content_checks_passed': True,
            'arst1431_hr': 0.86, 'arst1431_ci_95': [0.58, 1.26],
            'static_resource_policy': 'local_css_and_inline_svg_only'}


def check_deck():
    payload = checked_path(ROOT / 'notes/track2-slides-v9.html').read_bytes()
    return {'static_deck_verified': True, 'source_sha256': hashlib.sha256(payload).hexdigest(),
            **presentation_checks(payload.decode('utf-8'))}


def scientific_checks():
    ledger = read_json(ROOT / 'notes/track2-evidence-v9.json')
    require(ledger['schema_version'] == 9 and ledger['phase'] == 'unconfirmed', 'wrong evidence state')
    require(ledger['clinical_exposure_margin'] is None
            and ledger['direct_pair_intervention_evidence'] is False
            and ledger['clinical_efficacy'] == 'unestablished', 'unsupported clinical evidence')
    sources = {s['id']: s for s in ledger['sources']}
    require(len(sources) == len(ledger['sources']) == 36, 'source identity/count drift')
    decisions = {d['id']: d for d in ledger['decisions']}
    require(len(decisions) == len(ledger['decisions']) == 11, 'decision identity/count drift')
    for d in decisions.values():
        require(d['clinical_exposure_margin'] is None, 'invented clinical margin')
        require(set(d['support'] + d['counterevidence']) <= sources.keys(), 'unbound source')
        require(d['decision'] != 'conditional_priority', 'rescue priority restored')
    require(decisions['everolimus']['decision'] == 'mechanistic_probe_only', 'priority downgrade lost')
    require(decisions['hydroxychloroquine']['decision'] == 'reserve', 'HCQ promoted')
    for id in ('goutas2023', 'quy2013', 'castets2019'):
        require(id in decisions['everolimus']['counterevidence'], 'contrary evidence lost')
    require('abutaleb2023' in decisions['everolimus']['support'], 'positive counterweight lost')
    require(sources['goutas2023']['url'] == 'https://doi.org/10.1016/j.redox.2023.102701', 'wrong adverse source')
    require(ledger['adversarial_review']['rescued_or_clinically_prioritized_candidates'] == [], 'unsupported candidate promotion')
    expected = [('everolimus', 100, 'nM', 3), ('everolimus', 50, 'nM', 24),
                ('hydroxychloroquine', 100, 'uM', 2)]
    rows = ledger['new_exposure_observations']
    require(len(rows) == len(expected), 'missing exposure condition')
    for row, values in zip(rows, expected):
        require(tuple(row[k] for k in ('analyte', 'concentration', 'unit', 'hours')) == values,
                'exposure/time condition drift')
        require(row['source'] == 'goutas2023' and row['matrix'] == 'culture_medium'
                and row['basis'] == 'nominal' and row['clinical_exposure_margin'] is None
                and row['endpoint'] == 'BUBR1_protein_abundance', 'invalid exposure interpretation')
    report = checked_path(ROOT / 'notes/track2-report-v9.md').read_text()
    prior = checked_path(ROOT / 'notes/track2-report-v6.md').read_text()
    require(report.split('## Acknowledgement\n', 1)[1] == prior.split('## Acknowledgement\n', 1)[1],
            'required acknowledgement changed')
    for phrase in ('mechanistic probe', 'Goutas 2023', '50 nM', '100 micromolar',
                   'compensatory', 'Abutaleb 2023', 'clinical exposure margins remain unknown'):
        require(phrase.lower() in report.lower(), 'missing report qualification: ' + phrase)
    require(ledger['provider_settings'] == read_json(ROOT / 'notes/track2-evidence-v4.json')['provider_settings'],
            'provider attestation changed')
    return {'sources': 36, 'decisions': 11, 'rescue_priority_candidates': [],
            'clinical_exposure_margin': None, 'interpretation': 'Content and integrity checks, not scientific proof.'}


def inputs():
    return {name: digest(ROOT / name) for name in sorted(INPUTS)}


def history():
    path = checked_path(ROOT / 'results/feat009/jvv7_track2_research_v8')
    require(previous.verify(path)['integrity_verified'] is True, 'historical v8 failed')
    return digest(path / 'manifest.json')


def location(path):
    path = checked_path(path)
    require(path.parent == ROOT / 'results/feat009', 'snapshot must be a direct feat009 child')
    require(re.fullmatch(r'[a-z0-9][a-z0-9_-]*', path.name), 'invalid snapshot name')
    require(path.name not in {f'jvv7_track2_research_v{i}' for i in range(1, 9)},
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
    manifest = {'schema_version': 9, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'files': copies, 'input_hashes': before, 'historical_v8_manifest': historical,
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
    require(type(manifest['schema_version']) is int and manifest['schema_version'] == 9,
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
    require(manifest['historical_v8_manifest'] == history(), 'historical drift')
    require(foundation.same_json(manifest['presentation'], check_deck()), 'presentation drift')
    return {'integrity_verified': True, 'files': len(FILES), 'bound_inputs': len(INPUTS),
            'historical_v1_through_v8_preserved': True, 'upload_ready': False,
            'cover_line_removed_and_scientific_checks_passed': True,
            'deck_sha256': manifest['files']['jvv7_track2_slides_v9.html']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check-deck', 'check', 'build', 'verify'])
    parser.add_argument('output', type=Path, nargs='?')
    args = parser.parse_args()
    if args.command == 'check':
        if args.output is not None:
            parser.error('check uses only the fixed v9 inputs')
        result = scientific_checks()
    elif args.command == 'check-deck':
        if args.output is not None:
            parser.error('check-deck uses only the fixed v9 source')
        result = check_deck()
    else:
        if args.output is None:
            parser.error('build and verify require an output directory')
        result = {'build': build, 'verify': verify}[args.command](args.output)
    print(json.dumps(result, indent=2))
