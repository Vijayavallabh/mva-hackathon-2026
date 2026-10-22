"""Regression checks for coherent recording metrics and the v43 literature supplement."""
import unittest
from unittest.mock import patch
import track2_public_review_v52 as review
import track2_narration_v46 as timing
import build_track2_recording_v46 as recording
import check_track2_literature_v45 as literature


class PresentationTests(unittest.TestCase):
    def setUp(self):
        self.pitch=(review.ROOT/'notes/track2-pitch-v46.md').read_text()
        self.report=(review.ROOT/'notes/track2-report-v52.md').read_text()

    def test_complete_review_preserves_decisions_and_adds_literature_provenance(self):
        result=review.check()
        self.assertEqual((result['presentation_version'],result['narration_words'],
                          result['abstract_words'],result['claim_records']),(52,339,428,58))
        self.assertEqual(result['literature_refresh'],
                         {'passed':True,'version':45,'searches':7,'selected_sources':4,
                          'public_receipts':14,'repository_bytes':94130,
                          'subject_data_read':False,'drug_dispositions_changed':False,
                          'biological_validation':False,'full_text_systematic_review':False,'new_gpu_campaign':False})
        self.assertFalse(result['upload_ready'])
        self.assertFalse(result['biological_validation'])
        self.assertEqual(result['teaching_demo']['version'],37)

    def test_new_mechanistic_readouts_and_dispositions_are_reported(self):
        text=review.normalized(self.report).lower()
        for phrase in ['targeted contrary-evidence refreshes','checkpoint-architecture readouts',
                      'k250/s16/s39','no drug disposition changed','everolimus remains a mechanistic probe on hold',
                      'hcq remains reserve']:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase,text)

    def test_literature_checker_preserves_public_provenance(self):
        literature.check()
        note=(review.ROOT/'notes/track2-literature-v45.md').read_text().lower()
        for phrase in ['proband01','wgs_ex2312012']:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase,note)

    def test_speaking_rates_use_actual_words_and_each_cue_duration(self):
        result=timing.summary(self.pitch)
        self.assertEqual(result['planned_words_per_minute'],123.0)
        self.assertEqual(result['cues'][7]['planned_words_per_minute'],142.1)
        changed=self.pitch.replace('A drug must','A proposed drug must')
        self.assertEqual(timing.summary(changed)['narration_words'],370)
        self.assertIn('370-word',timing.guide_metrics(changed))
        real_read=review.Path.read_text
        def read(path,*args,**kwargs):
            return changed if path.name=='track2-pitch-v46.md' else real_read(path,*args,**kwargs)
        with patch.object(review.Path,'read_text',read):
            self.assertIn('370 narration words',recording.rendered())

    def test_gaps_overlaps_empty_durations_and_wrong_order_rejected(self):
        for old,new in [('0:18-0:40','0:19-0:40'),('0:18-0:40','0:17-0:40'),
                        ('0:18-0:40','0:18-0:18'),('Slide 2 /','Slide 22 /'),
                        ('2:48-3:00','2:48-3:01')]:
            with self.subTest(new=new),self.assertRaises(ValueError):
                timing.summary(self.pitch.replace(old,new))

    def test_v43_slides_only_reroute_current_report_not_silent_history(self):
        deck=(review.ROOT/'notes/track2-slides-v52.html').read_text()
        self.assertIn('notes/track2-report-v52.md',deck)
        for qualifier in ['1. First qualify function','2. Qualify a separate hypothesis',
                          'Opposing site/context evidence','Deficient + vehicle','Deficient + probe','Software verification only']:
            with self.subTest(qualifier=qualifier),self.assertRaises(ValueError):
                review.presentation_checks(deck.replace(qualifier,'omitted'))


if __name__=='__main__':unittest.main()
