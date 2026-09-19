#!/usr/bin/env python3
"""Synthetic-only v6 release tests; no subject, credential or real package reads."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import track2_release_v6 as release
from test_track2_release_v4 import evidence_fixture as previous_evidence_fixture


def evidence_fixture():
    value = previous_evidence_fixture()
    value['sources'].append({'id': 'arst1431', 'title': 'Synthetic primary-source metadata',
        'url': 'https://doi.org/' + release.ARST1431_DOI, 'kind': 'primary',
        'publication_model': 'Synthetic trial fixture', 'reading': 'selected_sections',
        'claim': 'Synthetic fixture only', 'limit': 'No real source retrieval'})
    return value

REPORT = ('Research draft 6. Trans phase remains unconfirmed. Fireworks GLM. Google DeepMind. '
          'Not used to train. Acknowledgement. Pralatrexate. Mitotic slippage. No clinical exposure margin.')
PITCH = 'Fireworks. Google DeepMind. Phase unconfirmed. Not a recorded video.'
SVG = '<svg viewBox="0 0 100 100" role="img" aria-label="Conceptual diagram"><circle cx="50" cy="50" r="20"/></svg>'
PLOT = ('<svg id="arst1431-plot" viewBox="0 0 1080 300" role="img" aria-label="Published ARST1431 hazard ratio">'
        '<line id="arst1431-axis" x1="90" x2="990" y1="200" y2="200"/>'
        '<line id="arst1431-ci" x1="186.36" x2="690.04" y1="100" y2="100"/>'
        '<circle id="arst1431-estimate" cx="442.08" cy="100" r="8"/>'
        '<line id="arst1431-null" x1="540" x2="540" y1="50" y2="200"/>'
        '<text id="arst1431-tick-low" x="90" y="230">0.5</text>'
        '<text id="arst1431-tick-mid" x="540" y="230">1</text>'
        '<text id="arst1431-tick-high" x="990" y="230">2</text></svg>')
PLOT_LABEL = ('<p>ARST1431 HR 0.86; 95% CI 0.58-1.26; 297 evaluable</p>'
              '<a href="https://doi.org/10.1016/S1470-2045(24)00255-9">Primary source</a>')
DECK = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta http-equiv="Content-Security-Policy" content="' + release.STATIC_CSP + '">'
        '<title>Test deck</title><style>body { color: #112233; } @media print { body { margin: 0; } }</style>'
        '</head><body><main>' + ''.join(
            f'<section id="slide-{i}"><h1>Research only</h1><p>Phase unconfirmed; no clinical exposure margin.</p>{PLOT + PLOT_LABEL if i == 3 else SVG}</section>'
            for i in range(1, 6)) + '</main></body></html>')


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


class VectorPolicyTests(unittest.TestCase):
    def check(self, deck=DECK):
        return release.boundaries(REPORT, PITCH, deck)

    def test_valid_static_vector_deck(self):
        self.assertEqual(self.check()['vector_figures'], 5)

    def test_published_plot_is_not_counted_as_a_proposed_schematic(self):
        value = self.check()
        self.assertEqual(value['published_data_plots'], 1)
        self.assertEqual(value['schematic_figures'], 4)
        self.assertEqual(value['arst1431_plot']['hazard_ratio'], 0.86)
        self.assertEqual(value['arst1431_plot']['confidence_interval_95'], [0.58, 1.26])

    def test_linear_axis_interpolation_is_rejected(self):
        # A plausible-looking point on a linear 0.5..2 axis is misleading here.
        with self.assertRaises(ValueError):
            self.check(DECK.replace('cx="442.08"', 'cx="306"'))

    def test_ci_null_and_point_geometry_must_agree_with_labels(self):
        for old, new in (('x1="186.36"', 'x1="200"'), ('x2="690.04"', 'x2="500"'),
                         ('x1="540" x2="540"', 'x1="530" x2="530"'),
                         ('cx="442.08" cy="100"', 'cx="442.08" cy="110"'),
                         ('x1="90" x2="990"', 'x1="990" x2="90"'),
                         ('x1="186.36"', 'x1="NaN"'), ('cx="442.08"', 'cx="inf"')):
            with self.subTest(new=new), self.assertRaises(ValueError):
                self.check(DECK.replace(old, new))

    def test_each_axis_tick_retains_value_and_position(self):
        for old, new in (('>0.5</text>', '>0.4</text>'), ('>1</text>', '>0</text>'),
                         ('>2</text>', '>3</text>'),
                         ('id="arst1431-tick-mid" x="540"', 'id="arst1431-tick-mid" x="450"')):
            with self.subTest(new=new), self.assertRaises(ValueError):
                self.check(DECK.replace(old, new))

    def test_published_plot_cannot_be_deleted_or_relabelled_by_id(self):
        for deck in (DECK.replace(PLOT, SVG), DECK.replace('arst1431-ci', 'other-ci'),
                     DECK.replace('arst1431-estimate', 'other-estimate')):
            with self.assertRaises(ValueError):
                self.check(deck)

    def test_direct_or_group_transforms_cannot_displace_checked_coordinates(self):
        for payload in (PLOT.replace('<circle ', '<circle transform="translate(100,0)" ', 1),
                        PLOT.replace('<line ', '<g transform="translate(100,0)"><line ', 1)
                            .replace('</svg>', '</g></svg>')):
            with self.assertRaises(ValueError):
                self.check(DECK.replace(PLOT, payload))

    def test_visible_published_values_cannot_be_replaced_by_comment_or_svg_description(self):
        for old in ('HR 0.86', '95% CI 0.58-1.26', '297 evaluable'):
            for replacement in ('<!-- ' + old + ' -->', '<desc>' + old + '</desc>'):
                with self.subTest(old=old, replacement=replacement), self.assertRaises(ValueError):
                    self.check(DECK.replace(old, replacement))

    def test_exact_primary_doi_required_for_published_plot(self):
        for deck in (DECK.replace(release.ARST1431_DOI, '10.1000/unrelated'),
                     DECK.replace(PLOT_LABEL, PLOT_LABEL.split('<a')[0])):
            with self.assertRaises(ValueError):
                self.check(deck)

    def test_basic_shapes_text_accessibility_and_namespace_allowed(self):
        drawing = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="Diagram">'
                   '<title>Conceptual diagram</title><desc>No experimental data.</desc>'
                   '<g fill="none" stroke="#123456" transform="translate(1,2)">'
                   '<path d="M1 2L3 4Z"/><line x1="1" x2="2" y1="3" y2="4"/>'
                   '<ellipse cx="5" cy="6" rx="1" ry="2"/><rect x="2" y="3" width="4" height="5"/>'
                   '<polygon points="1,2 3,4 5,6"/><text x="2" y="3"><tspan dy="1">Text</tspan></text>'
                   '</g></svg>')
        self.check(DECK.replace(SVG, drawing))

    def test_active_and_unapproved_html_tags_rejected(self):
        for tag in ('script', 'iframe', 'object', 'embed', 'form', 'base', 'link', 'img',
                    'audio', 'video', 'source', 'math', 'canvas', 'template', 'input'):
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                self.check(DECK.replace('<main>', '<main><' + tag + '></' + tag + '>'))

    def test_svg_active_elements_and_external_references_rejected(self):
        for payload in ('<script>alert(1)</script>', '<foreignObject><p>Text</p></foreignObject>',
                        '<use href="#a"/>', '<image href="https://example.org/a"/>',
                        '<animate attributeName="x"/>', '<set attributeName="x"/>',
                        '<filter/>', '<linearGradient/>', '<a href="https://example.org">x</a>'):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                self.check(DECK.replace('<circle cx="50" cy="50" r="20"/>', payload))

    def test_event_resource_and_unapproved_attributes_rejected(self):
        for attr in ('onclick="alert(1)"', 'onload="alert(1)"', 'href="https://example.org"',
                     'xlink:href="#a"', 'src="https://example.org"', 'filter="none"',
                     'data-secret="unknown"', 'aria-label'):
            with self.subTest(attr=attr), self.assertRaises(ValueError):
                self.check(DECK.replace('<circle ', '<circle ' + attr + ' ', 1))

    def test_duplicate_attributes_and_ids_rejected(self):
        for deck in (DECK.replace('id="slide-2"', 'id="slide-1"'),
                     DECK.replace('role="img"', 'role="img" role="img"', 1)):
            with self.assertRaises(ValueError):
                self.check(deck)

    def test_vector_label_and_role_required(self):
        for old, new in (('role="img"', 'role="presentation"'), ('role="img"', ''),
                         ('aria-label="Conceptual diagram"', ''),
                         ('aria-label="Conceptual diagram"', 'aria-label=" "')):
            with self.subTest(new=new), self.assertRaises(ValueError):
                self.check(DECK.replace(old, new, 1))

    def test_css_fetches_and_obfuscations_rejected(self):
        for css in ('@import "https://example.org/style";', '@font-face { src: url(a); }',
                    'body { background:url(//example.org/a); }',
                    'body { background:u/**/rl(//example.org/a); }',
                    'body { background:image-set("//example.org/a" 1x); }',
                    'body { background: image("//example.org/a"); }',
                    'body { behavior: expression(1); }', 'body { color: \\72 ed; }',
                    'body { background: src("//example.org/a"); }'):
            with self.subTest(css=css), self.assertRaises(ValueError):
                self.check(DECK.replace('body { color: #112233; }', css))

    def test_inline_css_entity_encoded_url_rejected(self):
        with self.assertRaises(ValueError):
            self.check(DECK.replace('<p>', '<p style="background:u&#114;l(//example.org/a)">', 1))

    def test_svg_resource_values_rejected(self):
        for value in ('url(#gradient)', 'url(//example.org/a)', '\\75rl(#a)', 'javascript:alert(1)'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.check(DECK.replace('<circle ', '<circle fill="' + value + '" ', 1))

    def test_fixed_single_csp_required(self):
        csp = '<meta http-equiv="Content-Security-Policy" content="' + release.STATIC_CSP + '">'
        for deck in (DECK.replace(csp, ''), DECK.replace(csp, csp * 2),
                     DECK.replace("default-src 'none'", "default-src *"),
                     DECK.replace('Content-Security-Policy', 'refresh')):
            with self.assertRaises(ValueError):
                self.check(deck)

    def test_only_https_or_internal_citation_links(self):
        for href in ('#slide-2', 'https://doi.org/10.1000/example'):
            self.check(DECK.replace('<main>', '<main><a href="' + href + '">Citation</a>'))
        for href in ('javascript:alert(1)', '//example.org', 'http://example.org',
                     'https://user:pass@example.org', 'https://example.org:999/a', '#',
                     'https://example.org/a&#10;', 'https://example.org\\a'):
            with self.subTest(href=href), self.assertRaises(ValueError):
                self.check(DECK.replace('<main>', '<main><a href="' + href + '">Citation</a>'))

    def test_exact_slide_structure_and_balanced_markup(self):
        for deck in (DECK.replace('id="slide-5"', 'id="slide-6"'),
                     DECK.replace('</section>', '</div>', 1), DECK.replace('</html>', ''),
                     DECK.replace(SVG, ''), DECK + '<html></html>',
                     DECK.replace('<main>', '<main><?processing bad?>')):
            with self.assertRaises(ValueError):
                self.check(deck)

    def test_vectors_cannot_all_be_placed_on_one_slide(self):
        deck = DECK.replace(SVG, '').replace('</section>', SVG * 5 + '</section>', 1)
        with self.assertRaises(ValueError):
            self.check(deck)

    def test_required_editorial_caveats_not_removed(self):
        for report, pitch, deck in ((REPORT.replace('unconfirmed', 'confirmed'), PITCH, DECK),
                (REPORT, PITCH.replace('Fireworks', 'Other'), DECK),
                (REPORT, PITCH, DECK.replace('Research only', 'Clinical plan')),
                (REPORT + ' No other AI providers have been used.', PITCH, DECK)):
            with self.assertRaises(ValueError):
                release.boundaries(report, pitch, deck)

    def test_equivalent_explicit_unknown_exposure_wording_allowed(self):
        alternate = REPORT.replace('No clinical exposure margin', 'All clinical exposure margins remain unknown')
        release.boundaries(alternate, PITCH, DECK)
        with self.assertRaises(ValueError):
            release.boundaries(alternate.replace('remain unknown', 'are established'), PITCH, DECK)


class ReleaseFixture(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='mva-v6-test-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        root_patch = patch.object(release, 'ROOT', self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)
        for source in release.INPUTS:
            path = self.root / source
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Synthetic fixture ' + source + '\n')
        (self.root / 'notes/track2-report-v6.md').write_text(REPORT)
        (self.root / 'notes/track2-pitch-v6.md').write_text(PITCH)
        (self.root / 'notes/track2-slides-v6.html').write_text(DECK)
        write_json(self.root / 'notes/track2-evidence-v4.json', evidence_fixture())
        self.history = {}
        for version in (1, 2, 3, 4, 5):
            path = self.root / f'results/feat009/jvv7_track2_research_v{version}'
            path.mkdir(parents=True)
            if version == 1:
                for name in release.LEGACY_V1_FILES:
                    (path / name).write_text('Historical v1 fixture')
                write_json(path / 'manifest.json', {'schema_version': 1,
                    'files': {name: hashlib.sha256((path / name).read_bytes()).hexdigest()
                              for name in release.LEGACY_V1_FILES}})
            else:
                write_json(path / 'manifest.json', {'synthetic': version})
                (path / 'sentinel').write_text('Historical fixture')
            self.history[version] = {p.name: p.read_bytes() for p in path.iterdir()}
        history_patch = patch.object(release.previous, 'verify', side_effect=self.history_check)
        self.prior_verify = history_patch.start()
        self.addCleanup(history_patch.stop)
        self.out = self.root / 'results/feat009/synthetic-v6'

    def history_check(self, _):
        for version in (2, 3, 4, 5):
            path = self.root / f'results/feat009/jvv7_track2_research_v{version}'
            if self.history[version] != {p.name: p.read_bytes() for p in path.iterdir()}:
                raise ValueError('synthetic historical drift')
        return {'integrity_verified': True}

    def build(self):
        result = release.build(self.out)
        self.assertTrue(result['integrity_verified'])
        return result

    def manifest(self):
        return json.loads((self.out / 'manifest.json').read_text())


class BuildTests(ReleaseFixture):
    def test_fixed_deck_check_returns_exact_validated_hash(self):
        result = release.check_deck()
        self.assertIs(result['static_deck_verified'], True)
        self.assertEqual(result['vector_figures'], 5)
        self.assertEqual(result['source_sha256'], hashlib.sha256(DECK.encode()).hexdigest())
        self.assertFalse(self.out.exists())

    def test_fixed_deck_check_rejects_active_payload_before_browser(self):
        path = self.root / 'notes/track2-slides-v6.html'
        path.write_text(DECK.replace('<main>', '<main><img src="file:///private"/>'))
        with self.assertRaises(ValueError):
            release.check_deck()

    def test_build_verify_preserves_sources_and_history(self):
        before = {name: (self.root / name).read_bytes() for name in release.INPUTS}
        result = self.build()
        self.assertEqual(result, release.verify(self.out))
        self.assertEqual(before, {name: (self.root / name).read_bytes() for name in release.INPUTS})
        self.history_check(None)
        self.assertEqual(set(self.manifest()['historical_manifest_hashes']), {'v1', 'v2', 'v3', 'v4', 'v5'})
        self.assertFalse(result['upload_ready'])
        self.assertTrue(result['historical_v5_preserved'])

    def test_compact_standalone_package_and_transitive_inputs(self):
        self.build()
        self.assertEqual(len(release.FILES), 8)
        self.assertNotIn('jvv7_track2_report_v4.md', release.FILES)
        self.assertLessEqual(release.previous.INPUTS, release.INPUTS)
        self.assertEqual(release.FILES['validation-v5.md'], 'notes/track2-validation-v5.md')
        self.assertIn('sources/research_track2_v6_visual_basis.md', release.INPUTS)
        self.assertEqual({p.name for p in self.out.iterdir()}, set(release.FILES) | {'manifest.json'})
        for name, source in release.FILES.items():
            self.assertEqual((self.out / name).read_bytes(), (self.root / source).read_bytes())

    def test_existing_destination_is_never_overwritten(self):
        self.out.mkdir()
        sentinel = self.out / 'sentinel'
        sentinel.write_text('retain')
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual(sentinel.read_text(), 'retain')
        self.prior_verify.assert_not_called()

    def test_path_scope_and_history_immutable(self):
        cases = [self.root, self.root / 'notes/new', self.out / 'nested',
                 self.root / 'results/feat009', self.out / '../escape',
                 self.root / 'results/feat009/space name']
        cases += [self.root / f'results/feat009/jvv7_track2_research_v{i}' for i in range(1, 6)]
        for path in cases:
            with self.subTest(path=path), self.assertRaises(ValueError):
                release.build(path)

    def test_symlink_output_or_parent_rejected(self):
        self.out.symlink_to(self.root / 'missing')
        with self.assertRaises(ValueError):
            self.build()
        self.out.unlink()
        parent = self.root / 'results/feat009'
        parent.rename(self.root / 'saved-results')
        parent.symlink_to(self.root / 'saved-results', target_is_directory=True)
        with self.assertRaises(ValueError):
            self.build()

    def test_source_symlink_or_missing_input_rejected_before_writes(self):
        source = self.root / 'notes/track2-v6-design.md'
        target = self.root / 'saved-source'
        source.rename(target)
        source.symlink_to(target)
        with self.assertRaises(ValueError):
            self.build()
        self.assertFalse(self.out.exists())
        source.unlink()
        with self.assertRaises(ValueError):
            self.build()
        self.assertFalse(self.out.exists())

    def test_history_failure_prevents_new_package(self):
        self.prior_verify.side_effect = ValueError('synthetic history failure')
        with self.assertRaises(ValueError):
            self.build()
        self.assertFalse(self.out.exists())

    def test_v1_legacy_bytes_checked_without_applying_current_science(self):
        (self.root / 'results/feat009/jvv7_track2_research_v1/sensitivity.json').write_text('changed')
        with self.assertRaises(ValueError):
            self.build()
        self.assertFalse(self.out.exists())
        self.prior_verify.assert_not_called()

    def test_history_symlink_rejected_before_prior_verifier(self):
        path = self.root / 'results/feat009/jvv7_track2_research_v4/sentinel'
        path.unlink()
        path.symlink_to(self.root / 'notes/track2-report-v6.md')
        with self.assertRaises(ValueError):
            self.build()
        self.prior_verify.assert_not_called()

    def test_midbuild_input_drift_does_not_produce_manifest(self):
        real_copy = release.shutil.copyfile
        def changed_copy(source, target):
            real_copy(source, target)
            (self.root / 'scripts/test_track2_release_v6.py').write_text('synthetic drift')
        with patch.object(release.shutil, 'copyfile', side_effect=changed_copy), self.assertRaises(ValueError):
            self.build()
        self.assertFalse((self.out / 'manifest.json').exists())

    def test_corrupt_copy_does_not_produce_manifest(self):
        def corrupt_copy(source, target):
            target.write_text('corrupt')
        with patch.object(release.shutil, 'copyfile', side_effect=corrupt_copy), self.assertRaises(ValueError):
            self.build()
        self.assertFalse((self.out / 'manifest.json').exists())

    def test_midbuild_history_drift_does_not_produce_manifest(self):
        real_copy = release.shutil.copyfile
        def changed_copy(source, target):
            real_copy(source, target)
            (self.root / 'results/feat009/jvv7_track2_research_v4/sentinel').write_text('drift')
        with patch.object(release.shutil, 'copyfile', side_effect=changed_copy), self.assertRaises(ValueError):
            self.build()
        self.assertFalse((self.out / 'manifest.json').exists())

    def test_evidence_cannot_be_promoted(self):
        for field, bad in (('phase', 'confirmed'), ('clinical_exposure_margin', 1),
                           ('clinical_efficacy', 'established')):
            value = evidence_fixture()
            value[field] = bad
            write_json(self.root / 'notes/track2-evidence-v4.json', value)
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.build()
            self.assertFalse(self.out.exists())

    def test_plot_cannot_point_to_unrelated_or_nonprimary_ledger_source(self):
        for key, bad in (('url', 'https://doi.org/10.1000/unrelated'), ('kind', 'regulatory')):
            value = evidence_fixture()
            value['sources'][-1][key] = bad
            write_json(self.root / 'notes/track2-evidence-v4.json', value)
            with self.subTest(field=key), self.assertRaises(ValueError):
                self.build()
            self.assertFalse(self.out.exists())

    def test_duplicate_json_keys_and_nonfinite_values_rejected(self):
        path = self.root / 'notes/track2-evidence-v4.json'
        for text in ('{"phase":"unconfirmed","phase":"confirmed"}', '{"bad":NaN}'):
            path.write_text(text)
            with self.assertRaises(ValueError):
                self.build()
            self.assertFalse(self.out.exists())


class VerifyTests(ReleaseFixture):
    def setUp(self):
        super().setUp()
        self.build()

    def test_manifest_unknown_and_missing_fields_rejected(self):
        original = self.manifest()
        bad = copy.deepcopy(original)
        bad['extra'] = True
        candidates = [bad]
        for name in original:
            bad = copy.deepcopy(original)
            del bad[name]
            candidates.append(bad)
        for manifest in candidates:
            write_json(self.out / 'manifest.json', manifest)
            with self.assertRaises(ValueError):
                release.verify(self.out)

    def test_truthy_and_coercible_readiness_claims_rejected(self):
        original = self.manifest()
        for field, bad in (('schema_version', 6.0), ('upload_ready', 0), ('upload_ready', True),
                ('upload_performed', 0), ('provider_settings_verified', True),
                ('phase', 'trans'), ('clinical_exposure_margin', False),
                ('video_url', 'https://example.org/video'), ('created_utc', '2026-09-19'),
                ('created_utc', '2026-09-19T12:00:00+05:30'), ('created_utc', 4),
                ('scope', 'Verified efficacy'), ('remaining_gates', []), ('stage', 'submitted')):
            value = copy.deepcopy(original)
            value[field] = bad
            write_json(self.out / 'manifest.json', value)
            with self.subTest(field=field, bad=bad), self.assertRaises(ValueError):
                release.verify(self.out)

    def test_evidence_summary_boolean_float_coercion_rejected(self):
        original = self.manifest()
        for field, bad in (('direct_pair_intervention_evidence', 0), ('sources', 1.0)):
            value = copy.deepcopy(original)
            value['evidence_checks']['scientific'][field] = bad
            write_json(self.out / 'manifest.json', value)
            with self.assertRaises(ValueError):
                release.verify(self.out)

    def test_package_tamper_even_with_updated_hash_rejected(self):
        path = self.out / 'validation-v5.md'
        path.write_text('tampered')
        with self.assertRaises(ValueError):
            release.verify(self.out)
        value = self.manifest()
        value['files'][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        write_json(self.out / 'manifest.json', value)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_current_bound_source_drift_rejected(self):
        (self.root / 'scripts/render_track2_slides_v6.mjs').write_text('drift')
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_unlisted_file_or_directory_rejected(self):
        extra = self.out / 'extra'
        extra.write_text('unexpected')
        with self.assertRaises(ValueError):
            release.verify(self.out)
        extra.unlink()
        extra.mkdir()
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_package_symlink_rejected(self):
        path = self.out / 'validation-v5.md'
        path.unlink()
        path.symlink_to(self.root / 'notes/track2-validation-v5.md')
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_manifest_file_or_input_set_cannot_be_shortened(self):
        original = self.manifest()
        for field in ('files', 'input_hashes'):
            value = copy.deepcopy(original)
            del value[field][next(iter(value[field]))]
            write_json(self.out / 'manifest.json', value)
            with self.assertRaises(ValueError):
                release.verify(self.out)

    def test_historical_manifest_forgery_rejected(self):
        value = self.manifest()
        value['historical_manifest_hashes']['v5'] = 'a' * 64
        write_json(self.out / 'manifest.json', value)
        with self.assertRaises(ValueError):
            release.verify(self.out)


if __name__ == '__main__':
    unittest.main(verbosity=2)
