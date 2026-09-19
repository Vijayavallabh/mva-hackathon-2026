"""Preservation and content-boundary checks using the public v8 deck fixture."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import track2_release_v8 as release

DECK = (release.ROOT / 'notes/track2-slides-v8.html').read_text()


class ScientificVisualSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in release.INPUTS:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Synthetic public fixture\n')
        self.deck = self.root / 'notes/track2-slides-v8.html'
        self.deck.write_text(DECK)
        (self.root / 'results/feat009').mkdir(parents=True)
        self.output = self.root / 'results/feat009/visual_v8'
        for target in ('track2_release_v8.ROOT', 'track2_release_v6.ROOT'):
            mock = patch(target, self.root)
            mock.start()
            self.addCleanup(mock.stop)
        mock = patch('track2_release_v8.history', return_value='a' * 64)
        self.historical = mock.start()
        self.addCleanup(mock.stop)

    def manifest(self):
        return self.output / 'manifest.json'

    def test_build_preserves_inputs_and_v8_identity(self):
        before = release.inputs()
        value = release.build(self.output)
        self.assertTrue(value['integrity_verified'])
        self.assertTrue(value['cover_line_removed_and_scientific_checks_passed'])
        self.assertEqual(before, release.inputs())
        self.assertFalse(value['upload_ready'])
        self.assertEqual(json.loads(self.manifest().read_text())['schema_version'], 8)

    def test_requested_cover_line_is_removed(self):
        self.assertTrue(release.check_deck()['requested_cover_line_removed'])
        self.deck.write_text(DECK.replace('</section>',
            '<p>Research only. Trans phase unconfirmed. No experiments performed.</p></section>', 1))
        with self.assertRaisesRegex(ValueError, 'cover line was restored'):
            release.check_deck()

    def test_scientific_boundaries_and_source_links_are_required(self):
        for phrase in ('No rapalog rescue tested', 'First confirm mTORC1 excess',
                       'Daughter survival', 'Trans phase unconfirmed',
                       'https://doi.org/10.1038/ng1449'):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, DECK)
                self.deck.write_text(DECK.replace(phrase, 'Removed'))
                with self.assertRaises(ValueError):
                    release.check_deck()

    def test_active_markup_and_inaccurate_plot_are_rejected(self):
        for altered in (DECK.replace('</body>', '<script>1</script></body>'),
                        DECK.replace('cx="468.08"', 'cx="100"')):
            self.assertNotEqual(DECK, altered)
            self.deck.write_text(altered)
            with self.assertRaises(ValueError):
                release.check_deck()

    def test_existing_or_historical_destination_is_rejected(self):
        release.build(self.output)
        with self.assertRaises(ValueError):
            release.build(self.output)
        for n in range(1, 8):
            with self.assertRaises(ValueError):
                release.location(self.output.parent / f'jvv7_track2_research_v{n}')

    def test_changed_copy_rejected_even_with_forged_file_hash(self):
        release.build(self.output)
        name = 'jvv7_track2_report_v6.md'
        p = self.output / name
        p.write_text('Changed report')
        manifest = json.loads(self.manifest().read_text())
        manifest['files'][name] = hashlib.sha256(p.read_bytes()).hexdigest()
        self.manifest().write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            release.verify(self.output)

    def test_readiness_history_and_input_drift_are_rejected(self):
        release.build(self.output)
        original = self.manifest().read_text()
        for key, value in (('upload_ready', 0), ('phase', 'confirmed'),
                           ('clinical_exposure_margin', 4.0), ('video_url', 'https://example.org'),
                           ('schema_version', 7)):
            manifest = json.loads(original)
            manifest[key] = value
            self.manifest().write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                release.verify(self.output)
        self.manifest().write_text(original)
        self.historical.return_value = 'b' * 64
        with self.assertRaises(ValueError):
            release.verify(self.output)
        self.historical.return_value = 'a' * 64
        (self.root / 'notes/track2-v8-design.md').write_text('Drift')
        with self.assertRaises(ValueError):
            release.verify(self.output)

    def test_symlink_input_and_destination_are_rejected(self):
        self.deck.unlink()
        self.deck.symlink_to(self.root / 'notes/track2-slides-v7.html')
        with self.assertRaises(ValueError):
            release.check_deck()
        self.output.symlink_to(self.root / 'notes', target_is_directory=True)
        with self.assertRaises(ValueError):
            release.location(self.output)


if __name__ == '__main__':
    unittest.main()
