"""Synthetic preservation checks for the visual-only snapshot adapter."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import track2_release_v7 as release
from test_track2_release_v6 import DECK


class VisualSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in release.INPUTS:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Synthetic public fixture\n')
        for name in ('notes/track2-slides-v6.html', 'notes/track2-slides-v7.html'):
            (self.root / name).write_text(DECK)
        (self.root / 'results/feat009').mkdir(parents=True)
        self.output = self.root / 'results/feat009/visual_v7'
        for target, value in (('track2_release_v7.ROOT', self.root),
                              ('track2_release_v6.ROOT', self.root)):
            mock = patch(target, value)
            mock.start()
            self.addCleanup(mock.stop)
        self.historical = patch('track2_release_v7.history', return_value='a' * 64).start()
        self.addCleanup(patch.stopall)

    def manifest(self):
        return self.output / 'manifest.json'

    def test_build_verify_and_preserve_historical_sources(self):
        before = release.inputs()
        value = release.build(self.output)
        self.assertTrue(value['integrity_verified'])
        self.assertEqual(before, release.inputs())
        self.assertFalse(value['upload_ready'])

    def test_visual_revision_cannot_change_wording_or_citations(self):
        p = self.root / 'notes/track2-slides-v7.html'
        for altered in (DECK.replace('Research only', 'Treatment ready', 1),
                        DECK.replace('>Primary source<', '>Unrelated claim<')):
            p.write_text(altered)
            with self.assertRaises(ValueError):
                release.build(self.output)
            self.assertFalse(self.output.exists())

    def test_line_breaks_preserve_words(self):
        p = self.root / 'notes/track2-slides-v7.html'
        p.write_text(DECK.replace('Research only', 'Research<br>only', 1))
        self.assertTrue(release.check_deck()['v6_slide_wording_and_links_preserved'])

    def test_inherits_active_markup_and_plot_geometry_rejection(self):
        p = self.root / 'notes/track2-slides-v7.html'
        for altered in (DECK.replace('</body>', '<script>1</script></body>'),
                        DECK.replace('cx="442.08"', 'cx="100"')):
            p.write_text(altered)
            with self.assertRaises(ValueError):
                release.check_deck()

    def test_existing_or_historical_output_is_rejected(self):
        release.build(self.output)
        with self.assertRaises(ValueError):
            release.build(self.output)
        for n in range(1, 7):
            with self.assertRaises(ValueError):
                release.location(self.output.parent / f'jvv7_track2_research_v{n}')

    def test_changed_copy_is_rejected_even_with_forged_file_hash(self):
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
                           ('clinical_exposure_margin', 4.0), ('video_url', 'https://example.org')):
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
        (self.root / 'notes/track2-v7-design.md').write_text('Drift')
        with self.assertRaises(ValueError):
            release.verify(self.output)

    def test_symlink_input_or_destination_is_rejected(self):
        p = self.root / 'notes/track2-slides-v7.html'
        p.unlink()
        p.symlink_to(self.root / 'notes/track2-slides-v6.html')
        with self.assertRaises(ValueError):
            release.check_deck()
        self.output.symlink_to(self.root / 'notes', target_is_directory=True)
        with self.assertRaises(ValueError):
            release.location(self.output)


if __name__ == '__main__':
    unittest.main()
