"""Regression checks for coherent recording metrics and the qualification sequence."""
import unittest
from unittest.mock import patch
import track2_public_review_v40 as review
import track2_narration_v40 as timing
import build_track2_recording_v40 as recording


class PresentationTests(unittest.TestCase):
    def setUp(self):
        self.pitch = (review.ROOT/'notes/track2-pitch-v40.md').read_text()

    def test_complete_review_preserves_decisions(self):
        result = review.check()
        self.assertEqual((result['presentation_version'], result['narration_words'],
                          result['abstract_words'], result['claim_records']), (40, 367, 334, 58))
        self.assertFalse(result['upload_ready'])
        self.assertFalse(result['biological_validation'])
        self.assertEqual(result['teaching_demo']['version'], 37)

    def test_speaking_rates_use_actual_words_and_each_cue_duration(self):
        result = timing.summary(self.pitch)
        self.assertEqual(result['planned_words_per_minute'], 122.3)
        self.assertEqual(result['cues'][7]['planned_words_per_minute'], 142.1)
        changed = self.pitch.replace('A drug must', 'A proposed drug must')
        self.assertEqual(timing.summary(changed)['narration_words'], 368)
        self.assertIn('368-word', timing.guide_metrics(changed))
        # A future edit must also update the generated prompter footer.
        real_read = review.Path.read_text
        def read(path, *args, **kwargs):
            return changed if path.name == 'track2-pitch-v40.md' else real_read(path, *args, **kwargs)
        with patch.object(review.Path, 'read_text', read):
            self.assertIn('368 narration words', recording.rendered())

    def test_gaps_overlaps_empty_durations_and_wrong_order_rejected(self):
        for old, new in [('0:18-0:40','0:19-0:40'), ('0:18-0:40','0:17-0:40'),
                         ('0:18-0:40','0:18-0:18'), ('Slide 2 /','Slide 22 /'),
                         ('2:48-3:00','2:48-3:01')]:
            with self.subTest(new=new), self.assertRaises(ValueError):
                timing.summary(self.pitch.replace(old,new))

    def test_separate_routes_and_synthetic_arm_labels_remain_visible(self):
        deck=(review.ROOT/'notes/track2-slides-v40.html').read_text()
        for qualifier in ['1. First qualify function','2. Qualify a separate hypothesis',
                          'Opposing site/context evidence','Deficit + vehicle','Deficit + probe']:
            with self.subTest(qualifier=qualifier), self.assertRaises(ValueError):
                review.presentation_checks(deck.replace(qualifier,'omitted'))


if __name__ == '__main__':
    unittest.main()
