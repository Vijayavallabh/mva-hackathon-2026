"""Guard against missing-result, failed-worker and biomedical overclaim promotion."""
from copy import deepcopy
import json
import unittest
import check_track2_optical_v36 as optical


class CompletedOpticalTests(unittest.TestCase):
    def setUp(self):
        self.result=json.loads((optical.ROOT/'notes/track2-optical-results-v36.json').read_text())

    def test_completed_public_evidence_passes(self):
        self.assertTrue(optical.check()['passed'])

    def test_missing_mitotic_query_cannot_become_a_zero_score(self):
        self.result['arms']['mitotic']['query_baselines']['full_profile']['mrr']['BUB1B']=0
        with self.assertRaisesRegex(ValueError,'Missing query'):
            optical.validate(self.result)

    def test_failed_worker_cannot_be_promoted_to_completion(self):
        self.result['arms']['interphase']['waves']['models']['workers'][0]['returncode']=1
        with self.assertRaisesRegex(ValueError,'Failed GPU worker'):
            optical.validate(self.result)

    def test_baseline_omission_cannot_improve_comparison(self):
        del self.result['arms']['interphase']['baselines']['full_median_training_preprocessing']
        with self.assertRaisesRegex(ValueError,'Baseline omitted'):
            optical.validate(self.result)

    def test_coverage_counts_cannot_be_inflated(self):
        self.result['arms']['mitotic']['query_coverage']['BUB1B'][0]['cells']=20
        with self.assertRaisesRegex(ValueError,'BUB1B source counts'):
            optical.validate(self.result)

    def test_failed_practical_gain_cannot_be_marked_passed(self):
        r=self.result['arms']['mitotic']
        r['registered_nine_baseline_gain']['practical_gain_gate_passed']=True
        with self.assertRaisesRegex(ValueError,'Gain gate'):
            optical.validate(self.result)

    def test_pooled_encoder_cannot_be_called_unseen_acquisition(self):
        self.result['arms']['interphase']['unseen_acquisition_training']=True
        with self.assertRaisesRegex(ValueError,'Pooled acquisition'):
            optical.validate(self.result)

    def test_post_hoc_plate_control_cannot_be_called_prespecified(self):
        self.result['arms']['interphase']['plate_control']['post_hoc']=False
        with self.assertRaisesRegex(ValueError,'Post-hoc plate-control'):
            optical.validate(self.result)

    def test_post_hoc_result_cannot_change_original_gate(self):
        self.result['arms']['interphase']['plate_control']['original_gates_changed']=True
        with self.assertRaisesRegex(ValueError,'Post-hoc plate control promoted'):
            optical.validate(self.result)

    def test_no_clinical_or_drug_promotion_from_retrieval(self):
        for key,value in [('phase','confirmed'),('clinical_exposure_margin',2.0),
                          ('biological_validation',True),('drug_ranking_changed',True),('rescue_priority','everolimus')]:
            changed=deepcopy(self.result);changed[key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'Unsupported promotion'):
                optical.validate(changed)


if __name__=='__main__':unittest.main()
