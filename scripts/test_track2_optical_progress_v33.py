from copy import deepcopy
import json
import unittest
import check_track2_optical_progress_v33 as review


class ProgressBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.status = json.loads((review.ROOT/'notes/track2-optical-status-v33.json').read_text())

    def test_preparation_and_launch_do_not_establish_gain(self):
        r = review.check()
        self.assertIsNone(r['full_model_gain'])
        self.assertEqual(r['bub1b_mitotic_retrieval'], 'insufficient_guide_coverage')

    def test_smoke_and_partial_runs_cannot_be_promoted(self):
        for key, value in [('model_results_validated', True), ('full_model_gain', 0.5),
                           ('research_status', 'complete'), ('smoke_excluded', False),
                           ('drug_ranking_changed', True)]:
            s = deepcopy(self.status); s[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                review.validate(s)

    def test_low_coverage_cannot_be_silently_requalified(self):
        s = deepcopy(self.status)
        s['mitotic_preparation']['query_coverage']['BUB1B'][0]['meets_20_cell_minimum'] = True
        with self.assertRaises(ValueError): review.validate(s)

    def test_shuffled_controls_cannot_be_counted_as_real_label_seeds(self):
        s = deepcopy(self.status)
        s['mitotic_worker_registration']['workers'][4]['shuffled'] = False
        with self.assertRaises(ValueError): review.validate(s)


if __name__ == '__main__': unittest.main()
