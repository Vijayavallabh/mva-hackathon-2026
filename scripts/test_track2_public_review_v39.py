"""Keep source qualifiers and runnable review instructions in the revised proposal."""
import unittest
import track2_public_review_v39 as review


class QualificationReviewTests(unittest.TestCase):
    def test_complete_review_preserves_science_and_delivery_limits(self):
        result = review.check()
        self.assertEqual((result['presentation_version'], result['narration_words'],
                          result['abstract_words'], result['claim_records']), (39, 364, 334, 58))
        self.assertFalse(result['upload_ready'])
        self.assertFalse(result['biological_validation'])
        self.assertEqual(result['teaching_demo']['version'], 37)

    def test_essential_context_cannot_disappear(self):
        report = (review.ROOT / 'notes/track2-report-v39.md').read_text()
        for qualifier in ['heterozygous BubR1+/X753', 'females had no median-lifespan',
                          'Mouse K243 corresponds to human K250', 'spontaneous tumors',
                          'availability, clone feasibility and functional qualification remain unconfirmed']:
            # Match case independently so this also covers a sentence-start qualifier.
            import re
            pattern = re.escape(qualifier).replace(r'\ ', r'\s+')
            altered, matches = re.subn(pattern, 'context omitted', report, flags=re.I)
            self.assertGreater(matches, 0, qualifier)
            with self.subTest(qualifier=qualifier), self.assertRaises(ValueError):
                review.report_checks(altered)

    def test_documented_command_must_exist(self):
        report = (review.ROOT / 'notes/track2-report-v39.md').read_text()
        with self.assertRaisesRegex(ValueError, 'Missing documented command'):
            review.report_checks(report.replace('scripts/track2_demo_v37.py', 'scripts/track2_demo_v39.py'))

    def test_narration_cue_gap_rejected(self):
        pitch = (review.ROOT / 'notes/track2-pitch-v39.md').read_text()
        with self.assertRaisesRegex(ValueError, 'Noncontiguous timing'):
            review.narration(pitch.replace('0:18-0:40', '0:19-0:40'))


if __name__ == '__main__':
    unittest.main()
