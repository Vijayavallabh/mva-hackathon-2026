from pathlib import Path
import unittest
import track2_release_v16 as release


class V16ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.deck=(release.ROOT/'notes/track2-slides-v16.html').read_text()

    def test_current_science_and_narration(self):
        self.assertEqual(release.scientific_checks()['narration_words'],328)

    def test_sensitivity_or_primary_success_cannot_be_removed(self):
        for phrase in ['12/12 pass','8/12 fail separation','11/24 retained scores negative','Post-hoc sensitivity']:
            with self.subTest(phrase=phrase),self.assertRaises(ValueError):
                release.presentation_checks(self.deck.replace(phrase,'removed'))

    def test_unknown_is_not_rewritten_as_failed_biology(self):
        with self.assertRaises(ValueError):
            release.presentation_checks(self.deck.replace('Unknown: hold.','Unknown: disproven.'))

    def test_trial_uncertainty_and_acknowledgement_retained(self):
        for phrase in ['95% CI 0.58-1.26','We acknowledge their trust']:
            with self.subTest(phrase=phrase),self.assertRaises(ValueError):
                release.presentation_checks(self.deck.replace(phrase,'removed'))

    def test_source_discrepancy_cannot_disappear(self):
        with self.assertRaises(ValueError):
            release.presentation_checks(self.deck.replace('units unresolved','dose verified'))

    def test_historical_snapshot_names_protected(self):
        for version in range(1,16):
            with self.subTest(version=version),self.assertRaises(ValueError):
                release.location(release.ROOT/f'results/feat009/jvv7_track2_research_v{version}')

    def test_every_historical_input_is_bound(self):
        self.assertTrue(release.historical.INPUTS <= release.INPUTS)
        self.assertIn('notes/track2-evidence-v15.json',release.FILES.values())
        self.assertIn('notes/track2-validation-v15.md',release.FILES.values())

    def test_method_abstract_must_retain_new_counterevidence(self):
        report=(release.ROOT/'notes/track2-report-v16.md').read_text()
        for phrase in ['8/12','11/24','1,000-fold','unknown/hold']:
            with self.subTest(phrase=phrase),self.assertRaises(ValueError):
                release.report_checks(report.replace(phrase,'removed'))

    def test_current_ledger_cannot_point_to_historical_science(self):
        report=(release.ROOT/'notes/track2-report-v16.md').read_text()
        with self.assertRaises(ValueError):
            release.report_checks(report.replace('[v15 decision ledger]','[v10 decision ledger]'))

    def test_remote_assets_rejected(self):
        with self.assertRaises(ValueError):
            release.presentation_checks(self.deck.replace('</body>','<script src="https://example.org/x.js"></script></body>'))


if __name__=='__main__':unittest.main()
