#!/usr/bin/env python3
"""Synthetic-only v4 package tests; never touch actual releases or subject inputs."""
from __future__ import annotations

import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import track2_release_v4 as release


def evidence_fixture():
    return {
        "schema_version": 4, "phase": "unconfirmed", "clinical_use": "research_only",
        "clinical_exposure_margin": None, "direct_pair_intervention_evidence": False,
        "clinical_efficacy": "unestablished",
        "sources": [{"id": "synthetic_source", "title": "Synthetic paper",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC123/", "kind": "primary",
            "publication_model": "Synthetic cell model", "reading": "selected_sections",
            "claim": "Synthetic hypothesis, not clinical efficacy", "limit": "Synthetic test only"}],
        "decisions": [{"id": identifier, "name": identifier, "scope": scope, "decision": decision,
            "support": ["synthetic_source"], "counterevidence": ["synthetic_source"],
            "rationale": "Synthetic indirect rationale", "stop_rule": "Stop if harm",
            "clinical_exposure_margin": None} for identifier, scope, decision in (
                ("everolimus", "constitutional", "conditional_priority"),
                ("hydroxychloroquine", "tumour", "reserve"),
                ("pralatrexate", "tumour", "tumour_only_horizon"),
                ("temsirolimus", "tumour", "benchmark_only"),
                ("entinostat", "tumour", "deprioritize"),
                ("vorinostat", "tumour", "deprioritize"),
                ("niclosamide", "tumour", "deprioritize"),
                ("posaconazole", "tumour", "deprioritize"),
                ("pp2a_tools", "mechanistic", "exclude"),
                ("senolysis", "constitutional", "exclude"),
                ("readthrough", "constitutional", "exclude"))],
        "provider_settings": {
            "openai_training": "owner_attested_not_used_for_training",
            "fireworks_training": "unverified", "fireworks_retention": "unverified",
            "fireworks_tier": "owner_attested_api_credits",
            "google_deepmind": "precomputed_output_api_and_downloads"},
    }


class EvidenceTests(unittest.TestCase):
    def test_valid_public_evidence_preserves_unknowns(self):
        result = release.validate_evidence(evidence_fixture())
        self.assertEqual(result["sources"], 1)
        self.assertEqual(result["decisions"], 11)
        self.assertEqual(result["conditional_priority"], ["everolimus"])
        self.assertEqual(result["reserve"], ["hydroxychloroquine"])
        self.assertIsNone(result["clinical_exposure_margin"])

    def test_repeated_url_cannot_be_counted_as_another_source(self):
        value = evidence_fixture()
        duplicate = copy.deepcopy(value['sources'][0])
        duplicate['id'] = 'another_source'
        value['sources'].append(duplicate)
        with self.assertRaises(ValueError):
            release.validate_evidence(value)

    def test_exact_top_level_fields_and_types(self):
        original = evidence_fixture()
        for value in (None, [], 'wrong', 4, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                release.validate_evidence(value)
        for field in original:
            value = copy.deepcopy(original)
            del value[field]
            with self.subTest(missing=field), self.assertRaises(ValueError):
                release.validate_evidence(value)
        value = copy.deepcopy(original)
        value['predicted_efficacy'] = 0.8
        with self.assertRaises(ValueError):
            release.validate_evidence(value)

    def test_rejects_nonliteral_research_boundaries(self):
        for key, bad in (('schema_version', 4.0), ('schema_version', True),
                         ('phase', 'confirmed_trans'), ('clinical_use', 'treatment'),
                         ('clinical_exposure_margin', 0), ('clinical_exposure_margin', False),
                         ('clinical_exposure_margin', 'unknown'), ('clinical_efficacy', 'established'),
                         ('direct_pair_intervention_evidence', True),
                         ('direct_pair_intervention_evidence', 0)):
            value = evidence_fixture()
            value[key] = bad
            with self.subTest(key=key, bad=bad), self.assertRaises(ValueError):
                release.validate_evidence(value)

    def test_provider_settings_cannot_silently_become_verified(self):
        for key in evidence_fixture()['provider_settings']:
            value = evidence_fixture()
            value['provider_settings'][key] = 'verified'
            with self.subTest(key=key), self.assertRaises(ValueError):
                release.validate_evidence(value)

    def test_source_records_are_nonempty_strict_and_unique(self):
        for field in evidence_fixture()['sources'][0]:
            value = evidence_fixture()
            del value['sources'][0][field]
            with self.subTest(missing=field), self.assertRaises(ValueError):
                release.validate_evidence(value)
        for bad in ([], None, {}, [None], ['wrong']):
            value = evidence_fixture()
            value['sources'] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                release.validate_evidence(value)
        value = evidence_fixture()
        value['sources'].append(copy.deepcopy(value['sources'][0]))
        with self.assertRaises(ValueError):
            release.validate_evidence(value)

    def test_source_text_and_categories_are_not_coerced(self):
        for field in ('id', 'title', 'publication_model', 'claim', 'limit', 'kind', 'reading'):
            for bad in ('', ' ', None, 3, []):
                value = evidence_fixture()
                value['sources'][0][field] = bad
                with self.subTest(field=field, bad=bad), self.assertRaises(ValueError):
                    release.validate_evidence(value)
        for key, bad in (('id', '../source'), ('kind', 'model_proposal'), ('reading', 'unread')):
            value = evidence_fixture()
            value['sources'][0][key] = bad
            with self.subTest(key=key), self.assertRaises(ValueError):
                release.validate_evidence(value)

    def test_only_allowlisted_public_https_sources(self):
        for url in ('http://pmc.ncbi.nlm.nih.gov/a', 'https://example.com/a',
                    'https://pmc.ncbi.nlm.nih.gov@evil.test/a',
                    'https://user@pmc.ncbi.nlm.nih.gov/a', 'https://pmc.ncbi.nlm.nih.gov:80/a',
                    'https://pmc.ncbi.nlm.nih.gov:wrong/a', 'https://pmc.ncbi.nlm.nih.gov/a#fragment',
                    'https://pmc.ncbi.nlm.nih.gov/a\n', 'file:///tmp/a', None, 2):
            value = evidence_fixture()
            value['sources'][0]['url'] = url
            with self.subTest(url=url), self.assertRaises(ValueError):
                release.validate_evidence(value)

    def test_abstract_and_selected_section_readings_are_supported_without_fulltext_claim(self):
        for reading in ('selected_sections', 'abstract_and_indexed_excerpt', 'abstract', 'official_page'):
            value = evidence_fixture()
            value['sources'][0]['reading'] = reading
            self.assertEqual(release.validate_evidence(value)['sources'], 1)

    def test_decisions_require_all_fields_and_types(self):
        for field in evidence_fixture()['decisions'][0]:
            value = evidence_fixture()
            del value['decisions'][0][field]
            with self.subTest(missing=field), self.assertRaises(ValueError):
                release.validate_evidence(value)
        for bad in ([], {}, None, [None], ['wrong']):
            value = evidence_fixture()
            value['decisions'] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                release.validate_evidence(value)

    def test_decision_unknown_and_duplicate_citations_rejected(self):
        for key in ('support', 'counterevidence'):
            for bad in ([], None, 'synthetic_source', ['unknown'], [None], [['nested']],
                        ['synthetic_source', 'synthetic_source']):
                value = evidence_fixture()
                value['decisions'][0][key] = bad
                with self.subTest(key=key, bad=bad), self.assertRaises(ValueError):
                    release.validate_evidence(value)

    def test_candidate_promotions_and_missing_pivotal_decisions_rejected(self):
        for index in range(len(evidence_fixture()['decisions'])):
            value = evidence_fixture()
            value['decisions'].pop(index)
            with self.subTest(missing=index), self.assertRaises(ValueError):
                release.validate_evidence(value)
        for decision in ('conditional_priority', 'reserve', 'tumour_only_horizon'):
            value = evidence_fixture()
            extra = copy.deepcopy(value['decisions'][0])
            extra.update(id='invented_candidate', decision=decision)
            value['decisions'].append(extra)
            with self.subTest(decision=decision), self.assertRaises(ValueError):
                release.validate_evidence(value)

    def test_candidate_scope_and_unknown_categories_rejected(self):
        for key, bad in (('scope', 'tumour'), ('scope', None), ('decision', 'recommend'),
                         ('clinical_exposure_margin', 0.1), ('name', ''), ('stop_rule', [])):
            value = evidence_fixture()
            value['decisions'][0][key] = bad
            with self.subTest(key=key, bad=bad), self.assertRaises(ValueError):
                release.validate_evidence(value)

    def test_duplicate_candidate_and_quantified_efficacy_rejected(self):
        value = evidence_fixture()
        value['decisions'].append(copy.deepcopy(value['decisions'][0]))
        with self.assertRaises(ValueError):
            release.validate_evidence(value)
        value = evidence_fixture()
        value['decisions'][0]['predicted_efficacy'] = 0.9
        with self.assertRaises(ValueError):
            release.validate_evidence(value)

    def test_mechanistic_exclusions_and_repeated_nonpromoted_roles_are_valid(self):
        value = evidence_fixture()
        self.assertEqual(sum(item['decision'] == 'exclude' for item in value['decisions']), 3)
        self.assertEqual(sum(item['decision'] == 'deprioritize' for item in value['decisions']), 4)
        self.assertEqual(release.validate_evidence(value)['decisions'], 11)

    def test_every_frozen_decision_scope_and_role_is_required(self):
        original = evidence_fixture()
        for index, item in enumerate(original['decisions']):
            for field, bad in (('scope', 'mechanistic' if item['scope'] != 'mechanistic' else 'tumour'),
                               ('decision', 'exclude' if item['decision'] != 'exclude' else 'deprioritize')):
                value = copy.deepcopy(original)
                value['decisions'][index][field] = bad
                with self.subTest(candidate=item['id'], field=field), self.assertRaises(ValueError):
                    release.validate_evidence(value)

    def test_extra_nonpromoted_decision_is_rejected(self):
        value = evidence_fixture()
        extra = copy.deepcopy(value['decisions'][-1])
        extra['id'] = 'unrequested_extra'
        value['decisions'].append(extra)
        with self.assertRaises(ValueError):
            release.validate_evidence(value)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


REPORT_WORDS = ('Research draft 4', 'trans phase remains unconfirmed', 'Fireworks', 'GLM',
                'Google DeepMind', 'not used to train', 'Acknowledgement', 'pralatrexate',
                'mitotic slippage', 'no clinical exposure margin')
PITCH_WORDS = ('Fireworks', 'Google DeepMind', 'phase unconfirmed', 'not a recorded')
DECK = '<!doctype html><html><head><style>section{color:black}</style></head><body><section>Research only. Phase unconfirmed. Clinical exposure margin unknown.</section></body></html>'


class ReleaseFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='track2-v4-offline-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.start_patch(patch.object(release, 'ROOT', self.root))
        for source in release.INPUTS:
            path = self.root / source
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Synthetic fixture for ' + source + '\n')
        self.report = self.root / 'notes/track2-report-v4.md'
        self.report.write_text('\n'.join(REPORT_WORDS) + '\n')
        self.pitch = self.root / 'notes/track2-pitch-v4.md'
        self.pitch.write_text('\n'.join(PITCH_WORDS) + '\n')
        self.deck = self.root / 'notes/track2-slides-v4.html'
        self.deck.write_text(DECK)
        self.evidence = self.root / 'notes/track2-evidence-v4.json'
        write_json(self.evidence, evidence_fixture())
        self.history = {}
        for version in (1, 2, 3):
            path = self.root / f'results/feat009/jvv7_track2_research_v{version}'
            path.mkdir(parents=True)
            write_json(path / 'manifest.json', {'synthetic': version})
            (path / 'sentinel').write_text('Immutable synthetic history ' + str(version))
            self.history[version] = {item.name: item.read_bytes() for item in path.iterdir()}
        self.out = self.root / 'results/feat009/synthetic_v4'
        self.verify_v2 = self.start_patch(patch.object(release.base, 'verify', side_effect=self.check_history))
        self.verify_v3 = self.start_patch(patch.object(release.previous, 'verify', side_effect=self.check_history))
        self.track1 = {'unchanged_local_v4_hashes': {'synthetic.csv': 'a' * 64},
                       'uploaded_bytes_independently_verified': False}
        track1_path = self.root / 'results/feat008/jvv7_genomewide_mva_v4'
        track1_path.mkdir(parents=True)
        for name in release.base.TRACK1:
            (track1_path / name).write_text('Synthetic Track 1 preservation fixture')
        self.track1_check = self.start_patch(patch.object(release.base, 'check_track1', return_value=self.track1))
        self.baseline = {'sources': 53, 'candidates': 12, 'synthetic': True}
        self.start_patch(patch.object(release.base, 'validate', return_value=self.baseline))
        for name in ('sources', 'candidates', 'exposure'):
            write_json(self.root / f'notes/track2-{name}.json', {'synthetic': name})

    def start_patch(self, patcher):
        result = patcher.start()
        self.addCleanup(patcher.stop)
        return result

    def check_history(self, path):
        version = int(path.name[-1])
        expected = self.history[version]
        if {item.name: item.read_bytes() for item in path.iterdir()} != expected:
            raise ValueError('synthetic historical package changed')
        return {'integrity_verified': True}

    def build(self):
        result = release.build(self.out)
        self.assertIs(result['integrity_verified'], True)
        return result

    def manifest(self):
        return json.loads((self.out / 'manifest.json').read_text())

    def put_manifest(self, value):
        write_json(self.out / 'manifest.json', value)


class BuildTests(ReleaseFixture):
    def test_build_and_read_only_verify_with_exact_source_bytes(self):
        result = self.build()
        before = {item.name: item.read_bytes() for item in self.out.iterdir()}
        self.assertEqual(release.verify(self.out), result)
        self.assertEqual(before, {item.name: item.read_bytes() for item in self.out.iterdir()})
        manifest = self.manifest()
        self.assertEqual(manifest['schema_version'], 4)
        self.assertIs(manifest['upload_ready'], False)
        self.assertIs(manifest['upload_performed'], False)
        self.assertIsNone(manifest['video_url'])
        self.assertEqual(set(manifest['input_hashes']), release.INPUTS)
        for name, source in release.FILES.items():
            self.assertEqual((self.out / name).read_bytes(), (self.root / source).read_bytes())
        self.verify_v2.assert_called()
        self.verify_v3.assert_called()
        self.track1_check.assert_called()

    def test_exact_fixed_file_set_and_transitive_bindings(self):
        self.build()
        expected = {
            'jvv7_track2_report_v3.md', 'jvv7_track2_pitch_v3.md', 'sources.json', 'candidates.json',
            'exposure.json', 'validation-plan.md', 'validation-addendum.md', 'scientific-exposure-review.md',
            'firecrawl-scientific-review.md', 'firecrawl-capabilities.md', 'firecrawl-run-review.md',
            'alphagenome-authenticated.md', 'alphagenome-splicing.md', 'alphagenome-score-semantics.md',
            'alphagenome-splicing-semantics.md', 'jvv7_track2_report_v4.md', 'jvv7_track2_pitch_v4.md',
            'jvv7_track2_slides_v4.html', 'validation-v4.md', 'evidence-v4.json', 'glm-review.md',
            'glm-constitutional-review.md', 'glm-oncology-review.md', 'v4-primary-review.md', 'v4-final-review.md',
        }
        self.assertEqual(set(release.FILES), expected)
        self.assertEqual({p.name for p in self.out.iterdir()}, expected | {'manifest.json'})
        self.assertLessEqual(release.previous.INPUTS, release.INPUTS)
        self.assertLessEqual({'scripts/track2_release_v4.py', 'scripts/test_track2_release_v4.py',
                             'scripts/track2_glm_review.py', 'scripts/test_track2_glm_review.py',
                             'scripts/render_track2_slides.mjs', 'notes/track2-glm-plan.json'}, release.INPUTS)

    def test_build_preserves_all_source_and_historical_bytes(self):
        before = {source: (self.root / source).read_bytes() for source in release.INPUTS}
        self.build()
        self.assertEqual(before, {source: (self.root / source).read_bytes() for source in release.INPUTS})
        for version in (1, 2, 3):
            self.check_history(self.root / f'results/feat009/jvv7_track2_research_v{version}')

    def test_existing_directory_is_never_overwritten(self):
        self.out.mkdir()
        (self.out / 'sentinel').write_text('retain')
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertEqual((self.out / 'sentinel').read_text(), 'retain')
        self.assertEqual({p.name for p in self.out.iterdir()}, {'sentinel'})
        self.verify_v2.assert_not_called()

    def test_existing_file_is_never_overwritten(self):
        self.out.write_text('retain')
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertEqual(self.out.read_text(), 'retain')

    def test_rejects_root_outside_traversal_and_historical_paths_before_writes(self):
        cases = [self.root, self.root / 'notes/new', self.root / 'results/feat009',
                 self.root / 'results/feat009/new/../escape']
        for version in (1, 2, 3):
            path = self.root / f'results/feat009/jvv7_track2_research_v{version}'
            cases.extend([path, path / 'nested'])
        for path in cases:
            with self.subTest(path=path), self.assertRaises(ValueError):
                release.build(path)
        for version in (1, 2, 3):
            self.check_history(self.root / f'results/feat009/jvv7_track2_research_v{version}')

    def test_cannot_nest_inside_any_manifest_bearing_package(self):
        prior = self.root / 'results/feat009/other_snapshot'
        prior.mkdir()
        (prior / 'manifest.json').write_text('{}')
        with self.assertRaises(ValueError):
            release.build(prior / 'nested/deeper')
        self.assertEqual({p.name for p in prior.iterdir()}, {'manifest.json'})

    def test_symlink_destination_and_dangling_symlink_rejected(self):
        for destination in (self.root / 'notes', self.root / 'missing'):
            self.out.symlink_to(destination, target_is_directory=True)
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                release.build(self.out)
            self.out.unlink()

    def test_symlink_parent_within_or_outside_results_rejected(self):
        alias = self.root / 'results/feat009/alias'
        for destination in (self.root / 'notes', self.root / 'results/feat009/jvv7_track2_research_v3',
                            self.root / 'results/feat009'):
            alias.symlink_to(destination, target_is_directory=True)
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                release.build(alias / 'new')
            alias.unlink()

    def test_symlink_input_leaf_rejected_before_creation(self):
        source = self.root / 'notes/track2-glm-plan.json'
        target = self.root / 'synthetic'
        target.write_bytes(source.read_bytes())
        source.unlink()
        source.symlink_to(target)
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertFalse(self.out.exists())

    def test_symlink_input_directory_rejected_before_creation(self):
        (self.root / 'notes').rename(self.root / 'saved-notes')
        (self.root / 'notes').symlink_to(self.root / 'saved-notes', target_is_directory=True)
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertFalse(self.out.exists())

    def test_missing_input_rejected_before_creation(self):
        (self.root / 'scripts/test_track2_release_v4.py').unlink()
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertFalse(self.out.exists())

    def test_historical_and_track1_failures_stop_before_output_creation(self):
        for mock in (self.verify_v2, self.verify_v3, self.track1_check):
            original = mock.side_effect
            mock.side_effect = ValueError('synthetic drift')
            with self.subTest(mock=mock), self.assertRaises(ValueError):
                release.build(self.out)
            self.assertFalse(self.out.exists())
            mock.side_effect = original

    def test_input_drift_during_copy_leaves_no_manifest(self):
        real_copy = release.shutil.copyfile
        changed = False
        def copy_with_drift(source, target):
            nonlocal changed
            result = real_copy(source, target)
            if not changed:
                changed = True
                (self.root / 'scripts/test_track2_release_v4.py').write_text('drift')
            return result
        with patch.object(release.shutil, 'copyfile', side_effect=copy_with_drift):
            with self.assertRaises(ValueError):
                release.build(self.out)
        self.assertFalse((self.out / 'manifest.json').exists())

    def test_corrupted_copy_leaves_no_manifest(self):
        real_copy = release.shutil.copyfile
        def corrupt_copy(source, target):
            result = real_copy(source, target)
            target.write_text('corrupt')
            return result
        with patch.object(release.shutil, 'copyfile', side_effect=corrupt_copy):
            with self.assertRaises(ValueError):
                release.build(self.out)
        self.assertFalse((self.out / 'manifest.json').exists())

    def test_historical_drift_during_copy_leaves_no_manifest(self):
        real_copy = release.shutil.copyfile
        def copy_with_drift(source, target):
            result = real_copy(source, target)
            (self.root / 'results/feat009/jvv7_track2_research_v3/sentinel').write_text('drift')
            return result
        with patch.object(release.shutil, 'copyfile', side_effect=copy_with_drift):
            with self.assertRaises(ValueError):
                release.build(self.out)
        self.assertFalse((self.out / 'manifest.json').exists())

    def test_evidence_duplicate_json_key_is_rejected(self):
        text = json.dumps(evidence_fixture()).replace('"phase": "unconfirmed"',
            '"phase": "confirmed", "phase": "unconfirmed"')
        self.evidence.write_text(text)
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertFalse(self.out.exists())

    def test_nonfinite_json_is_rejected(self):
        text = json.dumps(evidence_fixture()).replace('"clinical_exposure_margin": null',
                                                    '"clinical_exposure_margin": NaN', 1)
        self.evidence.write_text(text)
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertFalse(self.out.exists())

    def test_track1_symlink_is_rejected_before_upstream_reads(self):
        track1_path = self.root / 'results/feat008/jvv7_genomewide_mva_v4'
        name = next(iter(release.base.TRACK1))
        path = track1_path / name
        target = self.root / 'saved-track1'
        target.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(target)
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertFalse(self.out.exists())
        self.verify_v2.assert_not_called()


class VerifyTests(ReleaseFixture):
    def setUp(self):
        super().setUp()
        self.build()

    def test_boolean_integer_coercion_cannot_forge_summary(self):
        manifest = self.manifest()
        manifest['evidence_checks']['direct_pair_intervention_evidence'] = 0
        self.put_manifest(manifest)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_integer_float_coercion_cannot_forge_summary(self):
        manifest = self.manifest()
        manifest['evidence_checks']['sources'] = 1.0
        self.put_manifest(manifest)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_plain_package_tamper_rejected(self):
        (self.out / 'validation-v4.md').write_text('tamper')
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_updated_hash_cannot_hide_source_mismatch(self):
        path = self.out / 'validation-v4.md'
        path.write_text('tamper')
        manifest = self.manifest()
        manifest['files'][path.name] = sha(path)
        self.put_manifest(manifest)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_extra_file_and_subdirectory_rejected(self):
        extra = self.out / 'extra'
        extra.write_text('unlisted')
        with self.assertRaises(ValueError):
            release.verify(self.out)
        extra.unlink()
        extra.mkdir()
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_missing_package_file_cannot_be_removed_from_manifest(self):
        path = self.out / 'validation-v4.md'
        path.unlink()
        with self.assertRaises(ValueError):
            release.verify(self.out)
        manifest = self.manifest()
        del manifest['files'][path.name]
        self.put_manifest(manifest)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_manifest_input_set_cannot_be_shortened_or_expanded(self):
        original = self.manifest()
        for remove in (True, False):
            manifest = copy.deepcopy(original)
            if remove:
                del manifest['input_hashes']['scripts/test_track2_release_v4.py']
            else:
                manifest['input_hashes']['invented'] = 'a' * 64
            self.put_manifest(manifest)
            with self.subTest(remove=remove), self.assertRaises(ValueError):
                release.verify(self.out)

    def test_manifest_extra_or_missing_top_level_fields_rejected(self):
        original = self.manifest()
        manifest = copy.deepcopy(original)
        manifest['invented'] = True
        self.put_manifest(manifest)
        with self.assertRaises(ValueError):
            release.verify(self.out)
        for field in original:
            manifest = copy.deepcopy(original)
            del manifest[field]
            self.put_manifest(manifest)
            with self.subTest(missing=field), self.assertRaises(ValueError):
                release.verify(self.out)

    def test_manifest_wrong_container_types_rejected(self):
        original = self.manifest()
        for field in ('files', 'input_hashes', 'evidence_checks', 'base_ledger_checks',
                      'historical_manifest_hashes', 'track1'):
            for bad in (None, [], 'wrong', 4):
                manifest = copy.deepcopy(original)
                manifest[field] = bad
                self.put_manifest(manifest)
                with self.subTest(field=field, bad=bad), self.assertRaises(ValueError):
                    release.verify(self.out)

    def test_current_input_drift_rejected(self):
        for source in ('notes/track2-report-v4.md', 'notes/track2-glm-plan.json',
                       'scripts/track2_release_v4.py', 'scripts/test_track2_release_v4.py'):
            path = self.root / source
            original = path.read_bytes()
            path.write_text('changed')
            with self.subTest(source=source), self.assertRaises(ValueError):
                release.verify(self.out)
            path.write_bytes(original)

    def test_renderer_change_invalidates_snapshot(self):
        self.assertIn('scripts/render_track2_slides.mjs', release.INPUTS)
        (self.root / 'scripts/render_track2_slides.mjs').write_text('Changed preview renderer')
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_package_symlink_leaf_rejected_even_with_identical_bytes(self):
        path = self.out / 'validation-v4.md'
        path.unlink()
        path.symlink_to(self.root / release.FILES[path.name])
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_manifest_symlink_rejected(self):
        manifest = self.out / 'manifest.json'
        target = self.root / 'saved-manifest'
        target.write_bytes(manifest.read_bytes())
        manifest.unlink()
        manifest.symlink_to(target)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_package_directory_and_parent_alias_rejected(self):
        alias = self.root / 'results/feat009/alias'
        alias.symlink_to(self.out, target_is_directory=True)
        with self.assertRaises(ValueError):
            release.verify(alias)
        alias.unlink()
        alias.symlink_to(self.out.parent, target_is_directory=True)
        with self.assertRaises(ValueError):
            release.verify(alias / self.out.name)

    def test_manifest_draft_boundary_values_are_strict(self):
        original = self.manifest()
        cases = [('schema_version', 3), ('schema_version', 4.0), ('schema_version', True),
                 ('stage', 'submitted'), ('phase', 'trans'), ('clinical_exposure_margin', 0),
                 ('clinical_exposure_margin', False), ('clinical_exposure_margin', 'unknown'),
                 ('video_url', 'https://example.com/video')]
        for key in ('upload_ready', 'upload_performed', 'provider_settings_verified'):
            cases.extend([(key, True), (key, 0), (key, 'false')])
        for key, bad in cases:
            manifest = copy.deepcopy(original)
            manifest[key] = bad
            self.put_manifest(manifest)
            with self.subTest(key=key, bad=bad), self.assertRaises(ValueError):
                release.verify(self.out)

    def test_creation_timestamp_is_utc_string(self):
        original = self.manifest()
        for bad in (None, 1, 'yesterday', '2026-09-19T12:00:00', '2026-09-19T12:00:00+05:30'):
            manifest = copy.deepcopy(original)
            manifest['created_utc'] = bad
            self.put_manifest(manifest)
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                release.verify(self.out)

    def test_release_gates_and_limits_cannot_be_removed(self):
        original = self.manifest()
        for key, bad in (('remaining_gates', []), ('remaining_gates', ['upload']),
                         ('limits', 'verified scientific evidence'), ('additional_sources', 'independent studies')):
            manifest = copy.deepcopy(original)
            manifest[key] = bad
            self.put_manifest(manifest)
            with self.subTest(key=key), self.assertRaises(ValueError):
                release.verify(self.out)

    def test_historical_manifest_hash_tamper_rejected(self):
        original = self.manifest()
        for version in ('v2', 'v3'):
            manifest = copy.deepcopy(original)
            manifest['historical_manifest_hashes'][version] = '0' * 64
            self.put_manifest(manifest)
            with self.subTest(version=version), self.assertRaises(ValueError):
                release.verify(self.out)

    def test_actual_historical_package_drift_rejected(self):
        for version in (2, 3):
            path = self.root / f'results/feat009/jvv7_track2_research_v{version}/sentinel'
            original = path.read_bytes()
            path.write_text('changed')
            with self.subTest(version=version), self.assertRaises(ValueError):
                release.verify(self.out)
            path.write_bytes(original)

    def test_historical_symlink_input_rejected(self):
        path = self.root / 'results/feat009/jvv7_track2_research_v3/sentinel'
        target = self.root / 'saved-historical'
        target.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(target)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_track1_claim_forgery_including_boolean_coercion_rejected(self):
        original = self.manifest()
        for bad in ({}, {'unchanged_local_v4_hashes': {'synthetic.csv': 'a' * 64},
                         'uploaded_bytes_independently_verified': 0}):
            manifest = copy.deepcopy(original)
            manifest['track1'] = bad
            self.put_manifest(manifest)
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                release.verify(self.out)

    def test_baseline_summary_forgery_rejected(self):
        manifest = self.manifest()
        manifest['base_ledger_checks']['sources'] = 53.0
        self.put_manifest(manifest)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_evidence_revalidation_catches_coordinated_hash_forgery(self):
        value = evidence_fixture()
        value['phase'] = 'confirmed_trans'
        write_json(self.evidence, value)
        copied = self.out / 'evidence-v4.json'
        write_json(copied, value)
        manifest = self.manifest()
        manifest['files'][copied.name] = sha(copied)
        manifest['input_hashes']['notes/track2-evidence-v4.json'] = sha(self.evidence)
        self.put_manifest(manifest)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_disclosure_revalidation_catches_coordinated_hash_forgery(self):
        self.report.write_text(self.report.read_text().replace('Fireworks', ''))
        copied = self.out / 'jvv7_track2_report_v4.md'
        copied.write_bytes(self.report.read_bytes())
        manifest = self.manifest()
        manifest['files'][copied.name] = sha(copied)
        manifest['input_hashes']['notes/track2-report-v4.md'] = sha(self.report)
        self.put_manifest(manifest)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_duplicate_manifest_keys_rejected(self):
        path = self.out / 'manifest.json'
        path.write_text(path.read_text().replace('"upload_ready": false',
                                               '"upload_ready": true, "upload_ready": false'))
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_cli_verify_is_read_only(self):
        before = {p.name: p.read_bytes() for p in self.out.iterdir()}
        with patch('sys.argv', ['test', 'verify', str(self.out)]), patch('sys.stdout', new_callable=io.StringIO) as stdout:
            release.main()
        self.assertIs(json.loads(stdout.getvalue())['upload_ready'], False)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.out.iterdir()})


class BoundaryTests(ReleaseFixture):
    def test_each_report_boundary_required(self):
        for word in REPORT_WORDS:
            self.report.write_text('\n'.join(item for item in REPORT_WORDS if item != word))
            with self.subTest(word=word), self.assertRaises(ValueError):
                release.build(self.out)
            self.assertFalse(self.out.exists())

    def test_each_pitch_boundary_required(self):
        for word in PITCH_WORDS:
            self.pitch.write_text('\n'.join(item for item in PITCH_WORDS if item != word))
            with self.subTest(word=word), self.assertRaises(ValueError):
                release.build(self.out)
            self.assertFalse(self.out.exists())

    def test_case_and_whitespace_normalization(self):
        self.report.write_text(self.report.read_text().upper().replace(' ', '\n'))
        self.pitch.write_text(self.pitch.read_text().upper().replace(' ', '  '))
        self.build()

    def test_equivalent_phase_remains_unconfirmed_pitch_wording(self):
        self.pitch.write_text(self.pitch.read_text().replace('phase unconfirmed', 'phase remains unconfirmed'))
        self.build()

    def test_obsolete_provider_attestation_rejected(self):
        for path in (self.report, self.pitch, self.deck):
            original = path.read_text()
            path.write_text(original + '\nNo other AI providers have been used.\n')
            with self.subTest(path=path), self.assertRaises(ValueError):
                release.build(self.out)
            self.assertFalse(self.out.exists())
            path.write_text(original)

    def test_deck_boundaries_and_structure_required(self):
        for token in ('Research only', 'Phase unconfirmed', 'Clinical exposure margin', '<html>', '<section>'):
            self.deck.write_text(DECK.replace(token, 'removed'))
            with self.subTest(token=token), self.assertRaises(ValueError):
                release.build(self.out)
            self.assertFalse(self.out.exists())

    def test_deck_disallows_external_assets_and_active_content(self):
        fragments = ('<script>alert(1)</script>', '<script src="https://example.com/x.js"></script>',
                     '<img src="https://example.com/pixel">', '<link href="x.css">', '<iframe src="x"></iframe>',
                     '<object data="https://example.com"></object>', '<form action="https://example.com"></form>',
                     '<svg><use href="x"></use></svg>', '<meta http-equiv="refresh" content="0;url=https://example.com">',
                     '<body onload="alert(1)">', '<a href="javascript:alert(1)">x</a>',
                     '<a href="file:///tmp/private">x</a>', '<a href="https://example.com" ping="https://example.com">x</a>',
                     '<style>div{background:url(https://example.com/pixel)}</style>',
                     '<style>@import "https://example.com/style";</style>',
                     '<style>div{background:u\\72l(x)}</style>')
        for fragment in fragments:
            self.deck.write_text(DECK.replace('</body>', fragment + '</body>'))
            with self.subTest(fragment=fragment), self.assertRaises(ValueError):
                release.build(self.out)
            self.assertFalse(self.out.exists())

    def test_deck_allows_static_css_and_citation_links(self):
        self.deck.write_text(DECK.replace('</section>',
            '<a href="https://doi.org/10.1234/synthetic">Citation</a><a href="#slide2">Next</a></section>'))
        self.build()

    def test_deck_allows_only_exact_resource_blocking_csp(self):
        csp = "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"
        self.deck.write_text(DECK.replace('<head>', '<head><meta http-equiv="Content-Security-Policy" content="' + csp + '">'))
        self.build()

    def test_deck_rejects_weakened_csp_and_duplicate_attributes(self):
        for fragment in ('<meta http-equiv="Content-Security-Policy" content="default-src *">',
                         '<meta http-equiv="Content-Security-Policy" http-equiv="refresh" content="0">',
                         '<div style="background:&#117;rl(https://example.com/pixel)"></div>'):
            self.deck.write_text(DECK.replace('</body>', fragment + '</body>'))
            with self.subTest(fragment=fragment), self.assertRaises(ValueError):
                release.build(self.out)
            self.assertFalse(self.out.exists())


if __name__ == "__main__":
    unittest.main()
