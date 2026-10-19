import copy
import json
import unittest
import track2_public_review_v37 as review

class RubricReviewTests(unittest.TestCase):
    def test_current_public_review(self):
        r=review.check()
        self.assertEqual((r['presentation_version'],r['narration_words'],r['abstract_words']),(37,368,295))
        self.assertEqual(r['requirements']['public_discussions'],30)
        self.assertFalse(r['biological_validation'])

    def test_teaching_examples_cannot_be_presented_as_validated(self):
        report=(review.ROOT/'notes/track2-report-v37.md').read_text()
        for phrase in ['17 synthetic cases and one actual unmeasured state','not a representative','not been co-developed with the family']:
            with self.subTest(phrase=phrase),self.assertRaises(ValueError):
                review.report_checks(report.replace(phrase,'validated'))

    def test_incomplete_community_capture_rejected(self):
        r=json.loads((review.ROOT/'notes/track2-requirements-v37.json').read_text())
        c=json.loads((review.ROOT/'notes/track2-community-audit-v37.json').read_text())
        c['threads'].pop()
        with self.assertRaisesRegex(ValueError,'Thread coverage'):review.requirements_checks(r,c)

    def test_gap_in_recording_cues_rejected(self):
        pitch=(review.ROOT/'notes/track2-pitch-v37.md').read_text()
        with self.assertRaises(ValueError):review.narration(pitch.replace('0:18-0:40','0:19-0:40'))

if __name__=='__main__':unittest.main()
