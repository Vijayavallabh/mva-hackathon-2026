#!/usr/bin/env python3
"""Offline v6 editorial/visual release; static vectors, immutable history, no upload.

Integrity checks bind bytes and conservative disclosure fields. They do not prove
scientific correctness, absence of all browser defects, or submission readiness.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import shutil

import track2_release_v5 as previous

scientific = previous.previous

ROOT = Path(__file__).resolve().parents[1]
require = previous.require
exact_keys = previous.exact_keys
same_json = previous.same_json
STATIC_CSP = previous.STATIC_CSP
FILES = {
    'jvv7_track2_report_v6.md': 'notes/track2-report-v6.md',
    'jvv7_track2_pitch_v6.md': 'notes/track2-pitch-v6.md',
    'jvv7_track2_slides_v6.html': 'notes/track2-slides-v6.html',
    'validation-v5.md': 'notes/track2-validation-v5.md',
    'evidence-v4.json': 'notes/track2-evidence-v4.json',
    'v6-scientific-review.md': 'notes/track2-v6-scientific-review.md',
    'v6-design-review.md': 'notes/track2-v6-design.md',
    'v6-standards-review.md': 'notes/track2-v6-standards-review.md',
}
INPUTS = previous.INPUTS | set(FILES.values()) | {
    'scripts/track2_release_v6.py', 'scripts/test_track2_release_v6.py',
    'scripts/render_track2_slides_v6.mjs',
    'sources/research_track2_v6_visual_basis.md',
}
REMAINING_GATES = previous.REMAINING_GATES
LIMITS = previous.LIMITS
SCOPE = ('Presentation redesign only; the v4 scientific evidence and decisions are unchanged. '
         'ARST1431 is a redraw of a published hazard ratio and confidence interval; '
         'other figures are proposed or explanatory schematics, not experimental results. '
         'No recording, hosted video, provider-setting audit or upload was performed.')
MANIFEST_KEYS = {'schema_version', 'stage', 'created_utc', 'upload_performed',
    'upload_ready', 'video_url', 'phase', 'clinical_exposure_margin',
    'provider_settings_verified', 'input_hashes', 'files', 'historical_manifest_hashes',
    'evidence_checks', 'remaining_gates', 'limits', 'scope'}


def checked_path(path):
    path = Path(path)
    require('..' not in path.parts, 'path traversal is not allowed')
    path = path.absolute()
    require(path.is_relative_to(ROOT), 'path escapes repository')
    cursor = ROOT
    require(not cursor.is_symlink(), 'symlinked repository root')
    for part in path.relative_to(ROOT).parts:
        cursor /= part
        require(not cursor.is_symlink(), 'symlinked path component')
    require(path.resolve().is_relative_to(ROOT), 'resolved path escapes repository')
    return path


def location(path):
    path = checked_path(path)
    output_root = ROOT / 'results/feat009'
    require(path.parent == output_root, 'release must be a direct child of results/feat009')
    require(re.fullmatch(r'[a-z0-9][a-z0-9_-]*', path.name), 'invalid release directory name')
    require(path.name not in {f'jvv7_track2_research_v{i}' for i in range(1, 6)},
            'historical snapshots are immutable')
    return path


def digest(path):
    path = checked_path(path)
    require(path.is_file(), 'missing or nonregular release file')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    path = checked_path(path)
    digest(path)
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    def reject_constant(_):
        raise ValueError('nonfinite JSON number is not allowed')
    return json.loads(path.read_text(), object_pairs_hook=unique_pairs, parse_constant=reject_constant)


# Reuse the frozen v5 HTML/SVG/CSS subset without mutating its module globals.
phrases = previous.phrases
ARST1431_DOI = '10.1016/S1470-2045(24)00255-9'
LEGACY_V1_FILES = {'candidate-evidence.md', 'candidates.json', 'jvv7_track2_pitch_v1.md',
                   'jvv7_track2_report_v1.md', 'sensitivity.json', 'sources.json', 'validation-plan.md'}


class DeckParser(previous.DeckParser):
    """The frozen static subset plus one identified published-data plot.

    The coordinate check validates this deliberately fixed illustration. It is
    not a scientific source audit or a general SVG/CSS rendering verifier.
    """
    def __init__(self):
        super().__init__()
        self.in_plot = False
        self.plot_count = 0
        self.plot_nodes = {}
        self.active_tick = None
        self.slide3_text = []
        self.slide3_links = []

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        attributes = dict(attrs)
        if tag == 'svg' and attributes.get('id') == 'arst1431-plot':
            require(self.sections[-1] == 'slide-3', 'published ARST1431 plot must be on slide 3')
            self.in_plot = True
            self.plot_count += 1
        if self.in_plot:
            require('transform' not in attributes, 'published plot coordinates must be untransformed')
            if attributes.get('id', '').startswith('arst1431-'):
                self.plot_nodes[attributes['id']] = {'tag': tag, 'attrs': attributes, 'text': ''}
            if tag == 'text':
                name = attributes.get('id', '')
                self.active_tick = name if name.startswith('arst1431-tick-') else None
        if self.sections and self.sections[-1] == 'slide-3' and tag == 'a':
            self.slide3_links.append(attributes.get('href', ''))

    def handle_endtag(self, tag):
        if tag == 'text':
            self.active_tick = None
        if tag == 'svg':
            self.in_plot = False
        super().handle_endtag(tag)

    def handle_data(self, data):
        super().handle_data(data)
        if self.sections and self.sections[-1] == 'slide-3' and not any(
                tag in self.stack for tag in ('style', 'title', 'desc')):
            self.slide3_text.append(data)
        if self.in_plot and self.active_tick:
            self.plot_nodes[self.active_tick]['text'] += data

    def plot_node(self, name, tag):
        node = self.plot_nodes.get('arst1431-' + name)
        require(node is not None and node['tag'] == tag, 'missing or wrong published plot element: ' + name)
        return node

    @staticmethod
    def number(node, name):
        value = node['attrs'].get(name)
        try:
            result = float(value)
        except (TypeError, ValueError) as error:
            raise ValueError('invalid published plot coordinate: ' + name) from error
        require(math.isfinite(result), 'nonfinite published plot coordinate')
        return result

    def validate(self):
        super().validate()
        require(self.svg_count == 5 and self.section_vectors == [1] * 5,
                'v6 requires exactly one figure on each slide')
        require(self.plot_count == 1, 'exactly one identified published-data plot is required')
        axis = self.plot_node('axis', 'line')
        left, right = self.number(axis, 'x1'), self.number(axis, 'x2')
        require(right > left and self.number(axis, 'y1') == self.number(axis, 'y2'),
                'published HR axis must run horizontally from 0.5 to 2')
        def expected(value):
            return left + (right - left) * math.log(value / 0.5) / math.log(4)
        def at(node, attr, value):
            require(abs(self.number(node, attr) - expected(value)) <= 0.1,
                    'published HR or CI position does not match logarithmic axis')
        for name, value in (('low', 0.5), ('mid', 1), ('high', 2)):
            tick = self.plot_node('tick-' + name, 'text')
            require(tick['text'].strip() == str(value), 'wrong logarithmic axis tick label')
            at(tick, 'x', value)
        interval = self.plot_node('ci', 'line')
        at(interval, 'x1', 0.58)
        at(interval, 'x2', 1.26)
        require(self.number(interval, 'y1') == self.number(interval, 'y2'),
                'confidence interval must be horizontal')
        estimate = self.plot_node('estimate', 'circle')
        at(estimate, 'cx', 0.86)
        require(self.number(estimate, 'cy') == self.number(interval, 'y1'),
                'estimate must lie on its confidence interval')
        null = self.plot_node('null', 'line')
        at(null, 'x1', 1)
        at(null, 'x2', 1)
        text = re.sub(r'\s+', ' ', ' '.join(self.slide3_text)).replace('–', '-').replace('−', '-')
        for pattern in (r'HR\s*0\.86', r'95%\s*CI\s*0\.58\s*-\s*1\.26',
                        r'ARST1431', r'297\s+evaluable'):
            require(re.search(pattern, text, re.I), 'missing visible published-data label: ' + pattern)
        require(any(link == 'https://doi.org/' + ARST1431_DOI for link in self.slide3_links),
                'published plot needs the exact primary-source DOI link on slide 3')


def presentation_checks(deck):
    phrases(deck, ('phase unconfirmed', 'research only', 'clinical exposure margin'), 'deck')
    parser = DeckParser()
    parser.feed(deck)
    parser.close()
    parser.validate()
    return {'slides': len(parser.sections), 'vector_figures': parser.svg_count,
            'schematic_figures': 4, 'published_data_plots': 1,
            'arst1431_plot': {'hazard_ratio': 0.86, 'confidence_interval_95': [0.58, 1.26],
                             'axis': 'logarithmic', 'axis_range': [0.5, 2], 'doi': ARST1431_DOI},
            'static_resource_policy': 'local_css_and_inline_svg_only'}


def boundaries(report, pitch, deck):
    phrases(report, ('Research draft 6', 'trans phase remains unconfirmed', 'Fireworks',
        'GLM', 'Google DeepMind', 'not used to train', 'Acknowledgement', 'pralatrexate',
        'mitotic slippage'), 'report')
    normalized_report = re.sub(r'\s+', ' ', report).lower()
    require(any(text in normalized_report for text in ('no clinical exposure margin',
            'all clinical exposure margins remain unknown')), 'missing report exposure boundary')
    pitch = re.sub(r'phase\s+remains\s+unconfirmed', 'phase unconfirmed', pitch, flags=re.I)
    phrases(pitch, ('Fireworks', 'Google DeepMind', 'phase unconfirmed', 'not a recorded'), 'pitch')
    return presentation_checks(deck)


def check_deck():
    """Validate only the fixed public deck before local browser rendering."""
    path = checked_path(ROOT / 'notes/track2-slides-v6.html')
    require(path.is_file(), 'missing or nonregular deck file')
    payload = path.read_bytes()
    before = hashlib.sha256(payload).hexdigest()
    deck = payload.decode('utf-8')
    return {'static_deck_verified': True, 'source_sha256': before, **presentation_checks(deck)}


def current_inputs():
    return {name: digest(ROOT / name) for name in sorted(INPUTS)}


def history_checks():
    # The fixed v5 verifier recursively checks v2, v3, v4, their bound sources and
    # Track 1 hashes. Precheck all leaf paths before it performs any reads.
    result = {}
    for version in (1, 2, 3, 4, 5):
        path = checked_path(ROOT / f'results/feat009/jvv7_track2_research_v{version}')
        require(path.is_dir(), 'missing historical package')
        for item in path.iterdir():
            digest(item)
        if version == 1:
            # V1's current-source inputs legitimately predate the revised v2
            # evidence. Check its archived bytes without applying later science.
            legacy = read_json(path / 'manifest.json')
            require(type(legacy.get('schema_version')) is int and legacy['schema_version'] == 1,
                    'wrong historical v1 schema')
            exact_keys(legacy.get('files'), LEGACY_V1_FILES, 'historical v1 file')
            require({item.name for item in path.iterdir()} == LEGACY_V1_FILES | {'manifest.json'},
                    'historical v1 file set changed')
            require(all(digest(path / name) == value for name, value in legacy['files'].items()),
                    'historical v1 file hash mismatch')
        result[f'v{version}'] = digest(path / 'manifest.json')
    require(previous.verify(ROOT / 'results/feat009/jvv7_track2_research_v5').get('integrity_verified') is True,
            'historical v5 verification failed')
    return result


def document_checks(directory=None):
    def source(name):
        return directory / name if directory is not None else ROOT / FILES[name]
    for name in FILES:
        digest(source(name))
    deck = boundaries(source('jvv7_track2_report_v6.md').read_text(),
                      source('jvv7_track2_pitch_v6.md').read_text(),
                      source('jvv7_track2_slides_v6.html').read_text())
    evidence = read_json(source('evidence-v4.json'))
    scientific_checks = scientific.validate_evidence(evidence)
    require(any(item['id'] == 'arst1431' and item['kind'] == 'primary' and
                item['url'] == 'https://doi.org/' + ARST1431_DOI for item in evidence['sources']),
            'published plot must map to the unchanged primary-source ledger entry')
    return {'scientific': scientific_checks, 'presentation': deck}


def build(path):
    path = location(path)
    require(not path.exists(), 'release destination exists; never overwrite')
    inputs = current_inputs()
    history = history_checks()
    evidence = document_checks()
    path.mkdir(parents=True, exist_ok=False)
    for name, source in FILES.items():
        digest(ROOT / source)
        checked_path(path / name)
        shutil.copyfile(ROOT / source, path / name)
    files = {name: digest(path / name) for name in sorted(FILES)}
    require(all(files[name] == inputs[source] for name, source in FILES.items()), 'copy/source mismatch')
    require(current_inputs() == inputs and history_checks() == history, 'inputs or history changed during build')
    manifest = {'schema_version': 6, 'stage': 'research_draft_not_submitted',
        'created_utc': datetime.now(timezone.utc).isoformat(), 'upload_performed': False,
        'upload_ready': False, 'video_url': None, 'phase': 'unconfirmed',
        'clinical_exposure_margin': None, 'provider_settings_verified': False,
        'input_hashes': inputs, 'files': files, 'historical_manifest_hashes': history,
        'evidence_checks': evidence, 'remaining_gates': REMAINING_GATES, 'limits': LIMITS, 'scope': SCOPE}
    with (path / 'manifest.json').open('x') as handle:
        handle.write(json.dumps(manifest, indent=2) + '\n')
    return verify(path)


def verify(path):
    path = location(path)
    require(path.is_dir(), 'missing package directory')
    manifest = read_json(path / 'manifest.json')
    exact_keys(manifest, MANIFEST_KEYS, 'manifest')
    require(type(manifest['schema_version']) is int and manifest['schema_version'] == 6 and
            manifest['stage'] == 'research_draft_not_submitted', 'wrong release stage')
    require(manifest['upload_performed'] is False and manifest['upload_ready'] is False and
            manifest['provider_settings_verified'] is False and manifest['video_url'] is None,
            'draft cannot claim upload, recorded video or verified provider settings')
    require(manifest['phase'] == 'unconfirmed' and manifest['clinical_exposure_margin'] is None,
            'phase and exposure must remain unestablished')
    scientific.nonempty(manifest['created_utc'], 'creation timestamp')
    try:
        timestamp = datetime.fromisoformat(manifest['created_utc'])
    except ValueError as error:
        raise ValueError('invalid creation timestamp') from error
    require(timestamp.tzinfo is not None and timestamp.utcoffset().total_seconds() == 0,
            'creation timestamp must be UTC')
    require(same_json(manifest['remaining_gates'], REMAINING_GATES) and
            manifest['limits'] == LIMITS and manifest['scope'] == SCOPE, 'release limitations or gates changed')
    exact_keys(manifest['files'], FILES, 'manifest file')
    exact_keys(manifest['input_hashes'], INPUTS, 'manifest input')
    require({item.name for item in path.iterdir()} == set(FILES) | {'manifest.json'}, 'package file set mismatch')
    require(manifest['input_hashes'] == current_inputs(), 'current-input drift; build a new snapshot')
    for name, source in FILES.items():
        require(digest(path / name) == manifest['files'][name] == manifest['input_hashes'][source],
                'package file hash/source mismatch')
    require(same_json(manifest['evidence_checks'], document_checks(path)), 'evidence or presentation summary mismatch')
    require(manifest['historical_manifest_hashes'] == history_checks(), 'historical package changed')
    return {'integrity_verified': True, 'files': len(FILES), 'upload_ready': False,
        'provider_settings_verified': False, 'phase': 'unconfirmed',
        'historical_v1_preserved': True, 'historical_v2_preserved': True,
        'historical_v3_preserved': True, 'historical_v4_preserved': True, 'historical_v5_preserved': True,
        'report_sha256': manifest['files']['jvv7_track2_report_v6.md'],
        'slides_sha256': manifest['files']['jvv7_track2_slides_v6.html']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'verify', 'check-deck'])
    parser.add_argument('output', type=Path, nargs='?')
    args = parser.parse_args()
    if args.command == 'check-deck':
        if args.output is not None:
            parser.error('check-deck accepts no path; only the fixed public deck is checked')
        result = check_deck()
    else:
        if args.output is None:
            parser.error('build and verify require an output directory')
        result = {'build': build, 'verify': verify}[args.command](args.output)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
