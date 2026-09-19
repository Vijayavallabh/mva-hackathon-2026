"""Public presentation fixtures: evidence limits, plot and immutable release checks."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import track2_release_v12 as release

DECK = (release.ROOT / 'notes/track2-slides-v12.html').read_text()
PITCH = (release.ROOT / 'notes/track2-pitch-v12.md').read_text()
OLD_DECK = (release.ROOT / 'notes/track2-slides-v11.html').read_text()
REPORT = (release.ROOT / 'notes/track2-report-v12.md').read_text()
OLD_REPORT = (release.ROOT / 'notes/track2-report-v10.md').read_text()
DESCRIPTION = (release.ROOT / 'notes/track2-video-description-v12.md').read_text()


class PresentationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for name in release.INPUTS:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Synthetic public fixture\n')
        for name, text in [('notes/track2-slides-v12.html', DECK),
                           ('notes/track2-pitch-v12.md', PITCH),
                           ('notes/track2-slides-v11.html', OLD_DECK),
                           ('notes/track2-report-v12.md', REPORT),
                           ('notes/track2-report-v10.md', OLD_REPORT),
                           ('notes/track2-video-description-v12.md', DESCRIPTION)]:
            (self.root / name).write_text(text)
        (self.root / 'results/feat009').mkdir(parents=True)
        self.output = self.root / 'results/feat009/presentation_v12'
        for target, value in [('track2_release_v12.ROOT', self.root),
                              ('track2_release_v6.ROOT', self.root)]:
            mock = patch(target, value)
            mock.start()
            self.addCleanup(mock.stop)
        # Earlier versions have their own source/geometry tests and live verification.
        for target, result in [('track2_release_v12.history', 'a' * 64),
                               ('track2_release_v11.check_deck', {'static_deck_verified': True}),
                               ('track2_release_v11.scientific_checks', {'sources': 52})]:
            mock = patch(target, return_value=result)
            mock.start()
            self.addCleanup(mock.stop)

    def test_seven_slides_and_aligned_spoken_script(self):
        self.assertEqual(release.presentation_checks(DECK)['slides'], 7)
        self.assertEqual(release.narration_checks(PITCH)['narration_words'], 338)
        self.assertFalse(release.narration_checks(PITCH)['runtime_measured'])

    def test_model_and_hypothesis_limits_cannot_be_removed(self):
        for phrase in ('Force benefit not established', 'Neither branch established here',
                       'No post-hoc switching', 'no BUB1B or everolimus response shown',
                       'No rescue priority', 'Clinical exposure margin unknown'):
            with self.subTest(phrase=phrase), self.assertRaises(ValueError):
                release.presentation_checks(DECK.replace(phrase, 'Removed'))

    def test_cell_fates_and_safety_cannot_be_removed(self):
        for phrase in ('Daughter survival', 'tracking loss', 'Arrest / slippage',
                       'recovery and delayed injury', 'pause unexplained BUBR1 loss', 'HCQ reserve'):
            with self.subTest(phrase=phrase), self.assertRaises(ValueError):
                release.presentation_checks(DECK.replace(phrase, 'Removed'))

    def test_spoken_limits_and_slide_alignment_cannot_be_removed(self):
        for phrase in ('no switching after failure', '### Slide 4',
                       'whole blood is not free tissue\nexposure'):
            altered = PITCH.replace(phrase, 'Removed')
            self.assertNotEqual(PITCH, altered)
            with self.subTest(phrase=phrase), self.assertRaises(ValueError):
                release.narration_checks(altered)

    def test_active_markup_cover_line_and_plot_mutation_rejected(self):
        changes = [DECK.replace('</body>', '<script>1</script></body>'),
                   DECK.replace('cx="468.08"', 'cx="600"'),
                   DECK.replace('</section>', '<p>Research only. Trans phase unconfirmed. No experiments performed.</p></section>', 1)]
        for altered in changes:
            with self.assertRaises(ValueError):
                release.presentation_checks(altered)

    def test_required_acknowledgement_in_all_public_artifacts(self):
        acknowledgement = release.normalized(release.acknowledgement())
        with self.assertRaises(ValueError):
            release.presentation_checks(DECK.replace(acknowledgement, 'Thank you.'))
        for report, description in [(REPORT.replace('AWS and Anthropic.', 'Sponsors.'), DESCRIPTION),
                                    (REPORT, DESCRIPTION.replace('AWS and Anthropic.', 'Sponsors.'))]:
            with self.assertRaises(ValueError):
                release.report_checks(report, description)

    def test_methods_and_scientific_preservation(self):
        checked = release.report_checks(REPORT, DESCRIPTION)
        self.assertEqual(checked['template_answers'], 11)
        self.assertEqual(checked['abstract_words'], 228)
        for old, new in [('**A11 — ', '**Omitted — '),
                         ('Scientific rigor — 35%', 'Scientific rigor — 90%'),
                         ('## 1.', '## 1. Scientific edit')]:
            with self.subTest(old=old), self.assertRaises(ValueError):
                release.report_checks(REPORT.replace(old, new), DESCRIPTION)
        with self.assertRaises(ValueError):
            release.report_checks(REPORT.replace('## Acknowledgement', 'Extra ' * 501 + '\n## Acknowledgement'), DESCRIPTION)

    def test_build_verify_and_immutable_history(self):
        before = release.inputs()
        self.assertTrue(release.build(self.output)['historical_v1_through_v11_preserved'])
        self.assertEqual(before, release.inputs())
        with self.assertRaises(ValueError):
            release.build(self.output)
        for n in range(1, 12):
            with self.assertRaises(ValueError):
                release.location(self.output.parent / f'jvv7_track2_research_v{n}')

    def test_forged_copy_hash_and_readiness_fail(self):
        release.build(self.output)
        manifest_path = self.output / 'manifest.json'
        original = manifest_path.read_text()
        manifest = json.loads(original)
        manifest['upload_ready'] = True
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            release.verify(self.output)
        manifest = json.loads(original)
        name = 'jvv7_track2_pitch_v12.md'
        (self.output / name).write_text('Changed narration')
        manifest['files'][name] = hashlib.sha256((self.output / name).read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            release.verify(self.output)

    def test_input_drift_and_symlink_fail(self):
        release.build(self.output)
        p = self.root / 'notes/track2-challenge-review-20260919.md'
        p.write_text('Changed review')
        with self.assertRaises(ValueError):
            release.verify(self.output)
        deck = self.root / 'notes/track2-slides-v12.html'
        deck.unlink()
        deck.symlink_to(self.root / 'notes/track2-slides-v11.html')
        with self.assertRaises(ValueError):
            release.check_deck()


if __name__ == '__main__':
    unittest.main()
