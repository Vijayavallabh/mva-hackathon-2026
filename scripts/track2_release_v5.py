#!/usr/bin/env python3
"""Offline v5 editorial/visual release; static vectors, immutable history, no upload.

Integrity checks bind bytes and conservative disclosure fields. They do not prove
scientific correctness, absence of all browser defects, or submission readiness.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit

import track2_release_v4 as previous

ROOT = Path(__file__).resolve().parents[1]
require = previous.require
exact_keys = previous.exact_keys
same_json = previous.same_json
STATIC_CSP = previous.STATIC_CSP
FILES = {
    'jvv7_track2_report_v5.md': 'notes/track2-report-v5.md',
    'jvv7_track2_pitch_v5.md': 'notes/track2-pitch-v5.md',
    'jvv7_track2_slides_v5.html': 'notes/track2-slides-v5.html',
    'validation-v5.md': 'notes/track2-validation-v5.md',
    'evidence-v4.json': 'notes/track2-evidence-v4.json',
    'v5-editorial-review.md': 'notes/track2-v5-editorial-review.md',
    'v5-design-review.md': 'notes/track2-v5-design.md',
    'v5-standards-review.md': 'notes/track2-v5-standards-review.md',
}
INPUTS = previous.INPUTS | set(FILES.values()) | {
    'scripts/track2_release_v5.py', 'scripts/test_track2_release_v5.py',
    'scripts/render_track2_slides_v5.mjs',
    'sources/research_track2_v5_visual_basis.md',
}
REMAINING_GATES = previous.REMAINING_GATES
LIMITS = previous.LIMITS
SCOPE = ('Editorial and visual refresh only; the v4 scientific evidence and decisions '
         'are unchanged. Figures are conceptual diagrams, not experimental results. '
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
    require(path.name not in {f'jvv7_track2_research_v{i}' for i in range(1, 5)},
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


def static_css(value):
    require(type(value) is str, 'missing CSS value')
    # Reject escapes and resource at-rules. Remove comments before checking tokens so
    # split spellings cannot hide a fetch. CSS is deliberately local and simple.
    require('\\' not in value, 'CSS escapes are not allowed')
    stripped = re.sub(r'/\*.*?\*/', '', value, flags=re.S)
    at_rules = re.sub(r'@media\s+print\b|@media\s+screen\s+and\s*\(max-width:\s*[0-9]+px\)|@page\b',
                      '', stripped, flags=re.I)
    require('@' not in at_rules, 'only print/page or narrow-screen layout at-rules are allowed')
    require(not re.search(r'url\s*\(|(?:image|image-set|src|expression)\s*\(|'
                          r'(?:https?|data|javascript|file)\s*:|(?<![-\w])behavior\s*:|-moz-binding',
                          stripped, re.I), 'CSS resource loads or active constructs are not allowed')


HTML_TAGS = {'html', 'head', 'meta', 'title', 'style', 'body', 'main', 'section',
    'header', 'footer', 'nav', 'a', 'h1', 'h2', 'h3', 'p', 'span', 'div', 'small',
    'strong', 'em', 'b', 'i', 'br', 'ul', 'ol', 'li', 'figure', 'figcaption'}
SVG_TAGS = {'svg', 'g', 'path', 'line', 'circle', 'ellipse', 'rect', 'polygon',
            'text', 'tspan', 'title', 'desc'}
GLOBAL_ATTRS = {'id', 'class', 'style', 'role', 'aria-label', 'aria-hidden'}
HTML_ATTRS = {'html': {'lang'}, 'meta': {'charset', 'http-equiv', 'content', 'name'},
              'a': {'href'}, 'section': {'aria-labelledby'}}
SVG_ATTRS = {'viewbox', 'xmlns', 'width', 'height', 'x', 'y', 'x1', 'x2', 'y1', 'y2',
    'cx', 'cy', 'r', 'rx', 'ry', 'd', 'points', 'fill', 'stroke', 'stroke-width',
    'stroke-linecap', 'stroke-linejoin', 'stroke-dasharray', 'opacity', 'fill-opacity',
    'stroke-opacity', 'transform', 'text-anchor', 'dominant-baseline', 'font-size',
    'font-weight', 'font-family', 'letter-spacing', 'dx', 'dy'}
VOID_TAGS = {'meta', 'br'}


class DeckParser(HTMLParser):
    """Strict local subset: no active elements, external resources or SVG references."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.ids = set()
        self.sections = []
        self.section_vectors = []
        self.svg_count = 0
        self.csp_count = 0
        self.html_count = 0

    def handle_starttag(self, tag, attrs):
        in_svg = 'svg' in self.stack
        require(tag in (SVG_TAGS if in_svg or tag == 'svg' else HTML_TAGS),
                'unapproved HTML or SVG element: ' + tag)
        attributes = dict(attrs)
        require(len(attributes) == len(attrs), 'duplicate deck attribute')
        allowed = GLOBAL_ATTRS | (SVG_ATTRS if in_svg or tag == 'svg' else HTML_ATTRS.get(tag, set()))
        for name, value in attrs:
            require(name in allowed and type(value) is str, 'unapproved or valueless deck attribute: ' + name)
            if name == 'style':
                static_css(value)
            elif name == 'href':
                self.check_link(value)
            elif name in {'id', 'class'}:
                require(re.fullmatch(r'[A-Za-z0-9_ -]+', value), 'invalid deck identifier')
            elif name in SVG_ATTRS:
                if name == 'xmlns':
                    require(value == 'http://www.w3.org/2000/svg', 'wrong SVG namespace')
                else:
                    require(not re.search(r'url\s*\(|@|\\|(?:https?|data|javascript|file)\s*:', value, re.I),
                            'SVG resources and escaped constructs are not allowed')
        if 'id' in attributes:
            require(attributes['id'] not in self.ids, 'duplicate deck ID')
            self.ids.add(attributes['id'])
        if tag == 'html':
            self.html_count += 1
            require(not self.stack and self.html_count == 1, 'nested or repeated HTML root')
        if tag == 'meta':
            require('head' in self.stack, 'metadata must be in head')
            if 'http-equiv' in attributes:
                require(attributes == {'http-equiv': 'Content-Security-Policy', 'content': STATIC_CSP},
                        'only the fixed restrictive Content-Security-Policy is allowed')
                self.csp_count += 1
            else:
                require(attributes == {'charset': 'utf-8'} or
                        attributes.get('name') in {'viewport', 'description', 'author'} and
                        set(attributes) == {'name', 'content'}, 'unapproved metadata')
        if tag == 'section':
            self.sections.append(attributes.get('id'))
            self.section_vectors.append(0)
        if tag == 'svg':
            require(not in_svg and attributes.get('role') == 'img' and
                    bool(attributes.get('aria-label', '').strip()), 'SVG needs a nonempty accessible label')
            require('section' in self.stack, 'SVG figures must belong to a slide')
            self.section_vectors[-1] += 1
            self.svg_count += 1
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    @staticmethod
    def check_link(value):
        require(not any(c.isspace() for c in value) and '\\' not in value, 'invalid deck link')
        if value.startswith('#'):
            require(re.fullmatch(r'#[A-Za-z0-9_-]+', value), 'invalid internal link')
            return
        try:
            parsed = urlsplit(value)
            allowed = parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password
            allowed = allowed and parsed.port in (None, 443)
        except ValueError as error:
            raise ValueError('invalid deck HTTPS link') from error
        require(allowed, 'citation links must be HTTPS without credentials')

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        require(bool(self.stack) and self.stack[-1] == tag, 'unbalanced deck markup: ' + tag)
        self.stack.pop()

    def handle_data(self, data):
        if self.stack and self.stack[-1] == 'style':
            static_css(data)
        elif not self.stack:
            require(not data.strip(), 'text outside document')

    def handle_decl(self, decl):
        require(decl.lower() == 'doctype html', 'only HTML doctype is allowed')

    def unknown_decl(self, data):
        raise ValueError('unknown deck declaration')

    def handle_pi(self, data):
        raise ValueError('deck processing instructions are not allowed')

    def validate(self):
        require(not self.stack and self.html_count == 1, 'incomplete HTML document')
        require(self.csp_count == 1, 'exactly one restrictive CSP is required')
        require(self.sections == [f'slide-{n}' for n in range(1, 6)], 'exactly five ordered slides are required')
        require(all(self.section_vectors), 'every slide design requires conceptual vectors')


def phrases(text, required, label):
    normalized = re.sub(r'\s+', ' ', text).lower()
    for phrase in required:
        require(phrase.lower() in normalized, 'missing ' + label + ' boundary: ' + phrase)
    require('no other ai providers have been used' not in normalized, 'obsolete provider attestation')


def boundaries(report, pitch, deck):
    phrases(report, ('Research draft 5', 'trans phase remains unconfirmed', 'Fireworks',
        'GLM', 'Google DeepMind', 'not used to train', 'Acknowledgement', 'pralatrexate',
        'mitotic slippage'), 'report')
    normalized_report = re.sub(r'\s+', ' ', report).lower()
    require(any(text in normalized_report for text in ('no clinical exposure margin',
            'all clinical exposure margins remain unknown')), 'missing report exposure boundary')
    pitch = re.sub(r'phase\s+remains\s+unconfirmed', 'phase unconfirmed', pitch, flags=re.I)
    phrases(pitch, ('Fireworks', 'Google DeepMind', 'phase unconfirmed', 'not a recorded'), 'pitch')
    phrases(deck, ('phase unconfirmed', 'research only', 'clinical exposure margin'), 'deck')
    parser = DeckParser()
    parser.feed(deck)
    parser.close()
    parser.validate()
    return {'slides': len(parser.sections), 'conceptual_vector_figures': parser.svg_count,
            'static_resource_policy': 'local_css_and_inline_svg_only'}


def check_deck():
    """Validate only the fixed public deck before local browser rendering."""
    path = checked_path(ROOT / 'notes/track2-slides-v5.html')
    require(path.is_file(), 'missing or nonregular deck file')
    payload = path.read_bytes()
    before = hashlib.sha256(payload).hexdigest()
    deck = payload.decode('utf-8')
    phrases(deck, ('phase unconfirmed', 'research only', 'clinical exposure margin'), 'deck')
    parser = DeckParser()
    parser.feed(deck)
    parser.close()
    parser.validate()
    return {'static_deck_verified': True, 'source_sha256': before,
            'slides': len(parser.sections), 'conceptual_vector_figures': parser.svg_count}


def current_inputs():
    return {name: digest(ROOT / name) for name in sorted(INPUTS)}


def history_checks():
    # The fixed v4 verifier recursively checks v2, v3, their bound sources and
    # Track 1 hashes. Precheck all leaf paths before it performs any reads.
    result = {}
    for version in (2, 3, 4):
        path = checked_path(ROOT / f'results/feat009/jvv7_track2_research_v{version}')
        require(path.is_dir(), 'missing historical package')
        for item in path.iterdir():
            digest(item)
        result[f'v{version}'] = digest(path / 'manifest.json')
    require(previous.verify(ROOT / 'results/feat009/jvv7_track2_research_v4').get('integrity_verified') is True,
            'historical v4 verification failed')
    return result


def document_checks(directory=None):
    def source(name):
        return directory / name if directory is not None else ROOT / FILES[name]
    for name in FILES:
        digest(source(name))
    deck = boundaries(source('jvv7_track2_report_v5.md').read_text(),
                      source('jvv7_track2_pitch_v5.md').read_text(),
                      source('jvv7_track2_slides_v5.html').read_text())
    return {'scientific': previous.validate_evidence(read_json(source('evidence-v4.json'))),
            'presentation': deck}


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
    manifest = {'schema_version': 5, 'stage': 'research_draft_not_submitted',
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
    require(type(manifest['schema_version']) is int and manifest['schema_version'] == 5 and
            manifest['stage'] == 'research_draft_not_submitted', 'wrong release stage')
    require(manifest['upload_performed'] is False and manifest['upload_ready'] is False and
            manifest['provider_settings_verified'] is False and manifest['video_url'] is None,
            'draft cannot claim upload, recorded video or verified provider settings')
    require(manifest['phase'] == 'unconfirmed' and manifest['clinical_exposure_margin'] is None,
            'phase and exposure must remain unestablished')
    previous.nonempty(manifest['created_utc'], 'creation timestamp')
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
        'historical_v2_preserved': True, 'historical_v3_preserved': True, 'historical_v4_preserved': True,
        'report_sha256': manifest['files']['jvv7_track2_report_v5.md'],
        'slides_sha256': manifest['files']['jvv7_track2_slides_v5.html']}


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
