#!/usr/bin/env python3
"""Offline, immutable v4 research snapshots; no subject input or upload capability.

Hashes bind current inputs and preserved historical releases, not scientific truth
or clinical readiness. A valid draft still requires provider-setting verification,
a recorded hosted video, live portal checks, owner approval and a receipt.
"""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
from datetime import datetime, timezone
from urllib.parse import urlsplit

import track2_release as previous

base = previous.base
ROOT = Path(__file__).resolve().parents[1]
PUBLIC_HOSTS = {
    'doi.org', 'pubmed.ncbi.nlm.nih.gov', 'pmc.ncbi.nlm.nih.gov', 'www.jci.org',
    'www.nature.com', 'english.nmpa.gov.cn', 'www.ema.europa.eu',
    'dailymed.nlm.nih.gov', 'labeling.pfizer.com', 'huggingface.co', 'deepmind.google',
}
PROVIDER_SETTINGS = {
    'openai_training': 'owner_attested_not_used_for_training',
    'fireworks_training': 'unverified', 'fireworks_retention': 'unverified',
    'fireworks_tier': 'owner_attested_api_credits',
    'google_deepmind': 'precomputed_output_api_and_downloads',
}
REQUIRED_DECISIONS = {
    'everolimus': ('constitutional', 'conditional_priority'),
    'hydroxychloroquine': ('tumour', 'reserve'),
    'pralatrexate': ('tumour', 'tumour_only_horizon'),
    'temsirolimus': ('tumour', 'benchmark_only'),
    'entinostat': ('tumour', 'deprioritize'),
    'vorinostat': ('tumour', 'deprioritize'),
    'niclosamide': ('tumour', 'deprioritize'),
    'posaconazole': ('tumour', 'deprioritize'),
    'pp2a_tools': ('mechanistic', 'exclude'),
    'senolysis': ('constitutional', 'exclude'),
    'readthrough': ('constitutional', 'exclude'),
}
DECISIONS = {'conditional_priority', 'reserve', 'tumour_only_horizon',
             'deprioritize', 'exclude', 'benchmark_only'}
READING = {'full_text', 'abstract', 'official_page', 'metadata_only',
           'selected_sections', 'abstract_and_indexed_excerpt'}
KINDS = {'primary', 'regulatory', 'correction', 'competition', 'database'}
FILES = {
    **previous.FILES,
    'jvv7_track2_report_v4.md': 'notes/track2-report-v4.md',
    'jvv7_track2_pitch_v4.md': 'notes/track2-pitch-v4.md',
    'jvv7_track2_slides_v4.html': 'notes/track2-slides-v4.html',
    'validation-v4.md': 'notes/track2-validation-v4.md',
    'evidence-v4.json': 'notes/track2-evidence-v4.json',
    'glm-review.md': 'notes/track2-glm-review.md',
    'glm-constitutional-review.md': 'notes/track2-glm-constitutional-review.md',
    'glm-oncology-review.md': 'notes/track2-glm-oncology-review.md',
    'v4-primary-review.md': 'notes/track2-v4-primary-review.md',
    'v4-final-review.md': 'notes/track2-v4-review.md',
}
INPUTS = set(FILES.values()) | previous.INPUTS | {
    'scripts/track2_release_v4.py', 'scripts/test_track2_release_v4.py',
    'scripts/track2_glm_review.py', 'scripts/test_track2_glm_review.py',
    'scripts/render_track2_slides.mjs', 'notes/track2-glm-plan.json',
}
REMAINING_GATES = [
    'recorded three-minute hosted video',
    'verify Fireworks training and retention settings with owner; API credits alone do not establish them',
    'final owner review of report, video and expanded provider disclosure',
    'live rules, public visibility, purge, disclosure and authenticated quota checks',
    'portal upload and independently archived receipt',
]
LIMITS = 'Hashes are drift checks, not signatures, scientific validity or clinical readiness.'
SOURCE_NOTE = ('V4 evidence is an adjudicated supplement; the preserved 53-source/12-candidate '
               'baseline is historical. Model proposals and repeated reviews are not independent studies.')
STATIC_CSP = "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"
MANIFEST_KEYS = {'schema_version', 'stage', 'created_utc', 'upload_performed', 'upload_ready',
    'video_url', 'phase', 'clinical_exposure_margin', 'provider_settings_verified',
    'input_hashes', 'files', 'historical_manifest_hashes', 'track1', 'base_ledger_checks',
    'evidence_checks', 'remaining_gates', 'limits', 'additional_sources'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact_keys(value, keys, label):
    require(type(value) is dict and set(value) == set(keys), label + ' fields mismatch')


def same_json(left, right):
    """JSON equality without Python's False == 0 == 0.0 coercion."""
    return json.dumps(left, sort_keys=True, allow_nan=False) == json.dumps(right, sort_keys=True, allow_nan=False)


def nonempty(value, label):
    require(type(value) is str and bool(value.strip()), 'missing ' + label)


def identifier(value, label):
    require(type(value) is str and re.fullmatch(r'[a-z][a-z0-9_]*', value) is not None,
            'invalid ' + label)


def public_url(value):
    nonempty(value, 'source URL')
    require(not any(c.isspace() for c in value), 'whitespace in source URL')
    try:
        parsed = urlsplit(value)
        valid = (parsed.scheme == 'https' and parsed.hostname in PUBLIC_HOSTS
                 and not parsed.username and not parsed.password
                 and parsed.port in (None, 443) and not parsed.fragment)
    except ValueError as error:
        raise ValueError('invalid public source URL') from error
    require(valid, 'source URL is not an allowed public HTTPS endpoint')


def validate_evidence(value):
    """Validate claims' structure and conservative state, not their scientific truth."""
    exact_keys(value, {'schema_version', 'phase', 'clinical_use', 'clinical_exposure_margin',
        'direct_pair_intervention_evidence', 'clinical_efficacy', 'sources', 'decisions',
        'provider_settings'}, 'evidence')
    require(type(value['schema_version']) is int and value['schema_version'] == 4,
            'unsupported evidence schema')
    require(value['phase'] == 'unconfirmed' and value['clinical_use'] == 'research_only',
            'research-only unconfirmed-phase boundary required')
    require(value['clinical_exposure_margin'] is None
            and value['direct_pair_intervention_evidence'] is False
            and value['clinical_efficacy'] == 'unestablished', 'unsupported efficacy or exposure claim')
    require(value['provider_settings'] == PROVIDER_SETTINGS, 'provider settings must retain unresolved checks')
    require(type(value['sources']) is list and value['sources'], 'empty source list')
    registry = set()
    urls = set()
    for source in value['sources']:
        exact_keys(source, {'id', 'title', 'url', 'kind', 'publication_model', 'reading',
                            'claim', 'limit'}, 'source')
        identifier(source['id'], 'source ID')
        require(source['id'] not in registry, 'duplicate source ID')
        registry.add(source['id'])
        for field in ('title', 'publication_model', 'claim', 'limit', 'kind', 'reading'):
            nonempty(source[field], 'source ' + field)
        require(source['kind'] in KINDS and source['reading'] in READING, 'unknown source category')
        public_url(source['url'])
        parsed = urlsplit(source['url'])
        canonical = (parsed.hostname, parsed.path.rstrip('/'), parsed.query)
        require(canonical not in urls, 'duplicate source URL; do not double-count a source')
        urls.add(canonical)
    require(type(value['decisions']) is list and value['decisions'], 'empty decision list')
    seen = {}
    for decision in value['decisions']:
        exact_keys(decision, {'id', 'name', 'scope', 'decision', 'support', 'counterevidence',
                             'rationale', 'stop_rule', 'clinical_exposure_margin'}, 'decision')
        identifier(decision['id'], 'decision ID')
        require(decision['id'] not in seen, 'duplicate decision ID')
        seen[decision['id']] = decision
        for field in ('name', 'scope', 'decision', 'rationale', 'stop_rule'):
            nonempty(decision[field], 'decision ' + field)
        require(decision['scope'] in {'constitutional', 'tumour', 'mechanistic'}
                and decision['decision'] in DECISIONS, 'unknown decision category')
        require(decision['clinical_exposure_margin'] is None, 'clinical margin must remain null')
        for field in ('support', 'counterevidence'):
            citations = decision[field]
            require(type(citations) is list and citations
                    and all(type(item) is str for item in citations), 'missing decision citations')
            require(len(citations) == len(set(citations)) and set(citations) <= registry,
                    'unknown or duplicate citation')
    require(set(seen) == set(REQUIRED_DECISIONS), 'fixed v4 decision set mismatch')
    for name, (scope, decision) in REQUIRED_DECISIONS.items():
        require(name in seen and seen[name]['scope'] == scope and seen[name]['decision'] == decision,
                'required candidate decision mismatch: ' + name)
        if decision in {'conditional_priority', 'reserve', 'tumour_only_horizon'}:
            require([item['id'] for item in value['decisions'] if item['decision'] == decision] == [name],
                    'unexpected promotion to ' + decision)
    return {'sources': len(registry), 'decisions': len(seen),
            'conditional_priority': ['everolimus'], 'reserve': ['hydroxychloroquine'],
            'tumour_only_horizon': ['pralatrexate'], 'clinical_exposure_margin': None,
            'phase': 'unconfirmed', 'direct_pair_intervention_evidence': False,
            'clinical_efficacy': 'unestablished', 'provider_settings_verified': False}


def checked_path(path):
    """Reject lexical traversal and every symlink component before reading or writing."""
    path = Path(path)
    require('..' not in path.parts, 'path traversal is not allowed')
    path = path.absolute()
    require(path.is_relative_to(ROOT), 'path escapes repository')
    cursor = ROOT
    require(not cursor.is_symlink(), 'symlinked repository root')
    for part in path.relative_to(ROOT).parts:
        cursor = cursor / part
        require(not cursor.is_symlink(), 'symlinked path component')
    require(path.resolve().is_relative_to(ROOT), 'resolved path escapes repository')
    return path


def location(path):
    path = checked_path(path)
    output_root = ROOT / 'results/feat009'
    require(path.is_relative_to(output_root) and path != output_root,
            'release must be a new subdirectory of results/feat009')
    for version in (1, 2, 3):
        historical = output_root / f'jvv7_track2_research_v{version}'
        require(not path.is_relative_to(historical), 'historical snapshots are immutable')
    for parent in path.parents:
        if parent == output_root:
            break
        require(not (parent / 'manifest.json').exists(), 'cannot nest a release inside a package')
    return path


def digest(path):
    path = checked_path(path)
    require(path.is_file(), 'missing or nonregular release file')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
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


class DeckParser(HTMLParser):
    """Allow a self-contained static deck with CSS and citation links, no active loads."""
    def handle_starttag(self, tag, attrs):
        require(tag not in {'script', 'iframe', 'object', 'embed', 'form', 'base', 'link',
                            'img', 'audio', 'video', 'source', 'svg', 'math'},
                'deck must be static HTML without external assets or active content')
        attributes = dict(attrs)
        require(len(attributes) == len(attrs), 'duplicate deck attribute')
        for name, value in attrs:
            require(not name.startswith('on') and name not in {'src', 'srcset', 'action', 'formaction',
                    'background', 'poster', 'srcdoc', 'ping'}, 'active deck attribute is not allowed')
            if name == 'href':
                require(tag == 'a' and type(value) is str
                        and (value.startswith('#') or value.startswith('https://')),
                        'deck links must be citation anchors or HTTPS')
            if tag == 'meta' and name == 'http-equiv':
                require(type(value) is str and value.lower() == 'content-security-policy'
                        and set(attributes) == {'http-equiv', 'content'}
                        and attributes['content'] == STATIC_CSP,
                        'only the fixed resource-blocking Content-Security-Policy is allowed')
            if name == 'style':
                require(type(value) is str and not re.search(r'url\s*\(|@import|expression\s*\(|\\', value, re.I),
                        'deck inline style cannot load resources or use escaped active constructs')


def boundaries(report, pitch, deck):
    def phrases(text, required, label):
        normalized = re.sub(r'\s+', ' ', text).lower()
        for phrase in required:
            require(phrase.lower() in normalized, 'missing ' + label + ' boundary: ' + phrase)
        require('no other ai providers have been used' not in normalized,
                'obsolete provider attestation')
    phrases(report, ('Research draft 4', 'trans phase remains unconfirmed', 'Fireworks', 'GLM',
                     'Google DeepMind', 'not used to train', 'Acknowledgement', 'pralatrexate',
                     'mitotic slippage', 'no clinical exposure margin'), 'report')
    pitch = re.sub(r'phase\s+remains\s+unconfirmed', 'phase unconfirmed', pitch, flags=re.I)
    phrases(pitch, ('Fireworks', 'Google DeepMind', 'phase unconfirmed', 'not a recorded'), 'pitch')
    phrases(deck, ('phase unconfirmed', 'research only', 'clinical exposure margin'), 'deck')
    require(re.search(r'<html\b', deck, re.I) and re.search(r'<section\b', deck, re.I),
            'deck must contain HTML sections')
    require(not re.search(r'url\s*\(|@import|expression\s*\(|\\', deck, re.I),
            'deck CSS cannot load resources or use escaped active constructs')
    DeckParser().feed(deck)


def current_inputs():
    return {name: digest(ROOT / name) for name in sorted(INPUTS)}


def track1_checks():
    for name in base.TRACK1:
        digest(ROOT / 'results/feat008/jvv7_genomewide_mva_v4' / name)
    return base.check_track1()


def history_checks():
    result = {}
    for version, validator in ((2, base.verify), (3, previous.verify)):
        path = checked_path(ROOT / f'results/feat009/jvv7_track2_research_v{version}')
        require(path.is_dir(), 'missing historical package')
        for item in path.iterdir():
            digest(item)
        require(validator(path).get('integrity_verified') is True, 'historical check failed')
        result[f'v{version}'] = digest(path / 'manifest.json')
    return result


def document_checks(directory=None):
    def source(name):
        return (directory / name) if directory is not None else ROOT / FILES[name]
    for name in FILES:
        digest(source(name))
    boundaries(source('jvv7_track2_report_v4.md').read_text(),
               source('jvv7_track2_pitch_v4.md').read_text(),
               source('jvv7_track2_slides_v4.html').read_text())
    evidence = validate_evidence(read_json(source('evidence-v4.json')))
    baseline = base.validate(read_json(source('sources.json')), read_json(source('candidates.json')))
    return evidence, baseline


def build(path):
    path = location(path)
    require(not path.exists(), 'release destination exists; never overwrite')
    inputs = current_inputs()
    track1 = track1_checks()
    history = history_checks()
    evidence, baseline = document_checks()
    path.mkdir(parents=True, exist_ok=False)
    for name, source in FILES.items():
        digest(ROOT / source)
        checked_path(path / name)
        shutil.copyfile(ROOT / source, path / name)
    files = {name: digest(path / name) for name in sorted(FILES)}
    require(all(files[name] == inputs[source] for name, source in FILES.items()), 'copy/source mismatch')
    require(current_inputs() == inputs, 'inputs changed during build')
    require(same_json(track1_checks(), track1) and history_checks() == history,
            'preserved artifacts changed during build')
    manifest = {
        'schema_version': 4, 'stage': 'research_draft_not_submitted',
        'created_utc': datetime.now(timezone.utc).isoformat(), 'upload_performed': False,
        'upload_ready': False, 'video_url': None, 'phase': 'unconfirmed',
        'clinical_exposure_margin': None, 'provider_settings_verified': False,
        'input_hashes': inputs, 'files': files, 'historical_manifest_hashes': history,
        'track1': track1, 'base_ledger_checks': baseline, 'evidence_checks': evidence,
        'remaining_gates': REMAINING_GATES, 'limits': LIMITS, 'additional_sources': SOURCE_NOTE,
    }
    with (path / 'manifest.json').open('x') as handle:
        handle.write(json.dumps(manifest, indent=2) + '\n')
    return verify(path)


def verify(path):
    path = location(path)
    require(path.is_dir(), 'missing package directory')
    manifest = read_json(path / 'manifest.json')
    exact_keys(manifest, MANIFEST_KEYS, 'manifest')
    require(type(manifest['schema_version']) is int and manifest['schema_version'] == 4
            and manifest['stage'] == 'research_draft_not_submitted', 'wrong release stage')
    require(manifest['upload_performed'] is False and manifest['upload_ready'] is False
            and manifest['provider_settings_verified'] is False and manifest['video_url'] is None,
            'draft cannot claim upload, a recorded video, or verified provider settings')
    require(manifest['phase'] == 'unconfirmed' and manifest['clinical_exposure_margin'] is None,
            'phase and exposure must remain unestablished')
    nonempty(manifest['created_utc'], 'creation timestamp')
    try:
        timestamp = datetime.fromisoformat(manifest['created_utc'])
    except ValueError as error:
        raise ValueError('invalid creation timestamp') from error
    require(timestamp.tzinfo is not None and timestamp.utcoffset().total_seconds() == 0,
            'creation timestamp must be UTC')
    require(manifest['remaining_gates'] == REMAINING_GATES and manifest['limits'] == LIMITS
            and manifest['additional_sources'] == SOURCE_NOTE, 'release limitations or gates changed')
    exact_keys(manifest['files'], FILES, 'manifest file')
    exact_keys(manifest['input_hashes'], INPUTS, 'manifest input')
    require({item.name for item in path.iterdir()} == set(FILES) | {'manifest.json'},
            'package file set mismatch')
    require(manifest['input_hashes'] == current_inputs(), 'current-input drift; build a new snapshot')
    for name, source in FILES.items():
        require(digest(path / name) == manifest['files'][name] == manifest['input_hashes'][source],
                'package file hash/source mismatch')
    evidence, baseline = document_checks(path)
    require(same_json(manifest['evidence_checks'], evidence) and same_json(manifest['base_ledger_checks'], baseline),
            'evidence or baseline summary mismatch')
    require(same_json(manifest['track1'], track1_checks()), 'Track 1 preservation mismatch')
    require(manifest['historical_manifest_hashes'] == history_checks(), 'historical package changed')
    return {'integrity_verified': True, 'files': len(FILES), 'upload_ready': False,
            'provider_settings_verified': False, 'phase': 'unconfirmed',
            'historical_v2_preserved': True, 'historical_v3_preserved': True,
            'report_sha256': manifest['files']['jvv7_track2_report_v4.md'],
            'slides_sha256': manifest['files']['jvv7_track2_slides_v4.html']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'verify'])
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    print(json.dumps({'build': build, 'verify': verify}[args.command](args.output), indent=2))


if __name__ == '__main__':
    main()
