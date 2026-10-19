"""Check final numerical display, safety decisions and required attribution."""
import json
import unittest
import track2_public_review_v36 as review


class PresentationTests(unittest.TestCase):
    def setUp(self):
        self.report=(review.ROOT/'notes/track2-report-v36.md').read_text()
        self.deck=(review.ROOT/'notes/track2-slides-v36.html').read_text()

    def test_full_public_review(self):
        result=review.check()
        self.assertEqual((result['slides'],result['claim_records']),(9,58))
        self.assertFalse(result['biological_validation'])
        self.assertFalse(result['upload_ready'])

    def test_displayed_baseline_cannot_be_lowered(self):
        results=json.loads((review.ROOT/'notes/track2-optical-results-v36.json').read_text())
        best=max(v['macro_mrr'] for v in results['arms']['interphase']['baselines'].values())
        changed=self.deck.replace(f'>{best:.4f}</text>','>0.0001</text>')
        with self.assertRaisesRegex(ValueError,'strongest baseline'):
            review.optical_numbers(results,self.report,changed)

    def test_synthetic_example_cannot_look_experimental(self):
        with self.assertRaises(ValueError):
            review.presentation_checks(self.deck.replace('Synthetic example, not experimental data.','Observed result.'))

    def test_safety_failure_cannot_advance(self):
        with self.assertRaises(ValueError):
            review.presentation_checks(self.deck.replace('Stop; review injury','Advance despite injury'))

    def test_required_provider_and_acknowledgement_remain(self):
        for text in ['Fireworks-hosted','We acknowledge their trust']:
            with self.subTest(text=text),self.assertRaises(ValueError):
                review.report_checks(self.report.replace(text,'Omitted'))

    def test_active_html_rejected(self):
        with self.assertRaises(ValueError):
            review.presentation_checks(self.deck.replace('</body>','<script>alert(1)</script></body>'))

    def test_unfinished_results_rejected(self):
        with self.assertRaisesRegex(ValueError,'Unfinished'):
            review.report_checks(self.report+'\nPENDING\n')


if __name__=='__main__':unittest.main()
