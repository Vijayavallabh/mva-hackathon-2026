from copy import deepcopy
import json
from pathlib import Path
import unittest
import check_track2_rnai_v23 as review

class RNAiEvidenceChecks(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((review.ROOT/'notes/track2-rnai-results-v23.json').read_text())
        self.sensitivity=json.loads((review.ROOT/'notes/track2-rnai-tail-sensitivity-v23.json').read_text())
        self.register=json.loads((review.ROOT/'notes/track2-rnai-register-v23.json').read_text())

    def check(self):return review.validate(self.data,self.sensitivity,self.register)

    def test_complete_analysis(self):self.assertTrue(self.check()['passed'])

    def test_missing_worker(self):
        self.data['gpu_runs'].pop()
        with self.assertRaises(ValueError):self.check()

    def test_unknown_cannot_become_negative(self):
        for row in self.data['rows']:
            for n in row['bub1b']['nulls']:
                if n['tail'] is None:n['tail']=1.0
        with self.assertRaises(ValueError):self.check()

    def test_drop_finite_reference_counterweight(self):
        self.sensitivity['finite_reference_BH_excess_count']=5
        with self.assertRaises(ValueError):self.check()

    def test_wrong_finite_tail(self):
        self.sensitivity['rows'][0]['finite_reference_tail']=.4
        with self.assertRaises(ValueError):self.check()

    def test_fabricated_independent_experiment(self):
        self.data['independent_experiments_added']=1
        with self.assertRaises(ValueError):self.check()

    def test_bub1b_crispr_cannot_be_inferred(self):
        self.data['rows'][0]['crispr_bub1b_present']=True
        with self.assertRaises(ValueError):self.check()

    def test_drug_promotion_rejected(self):
        self.data['status']['rescue_priority']='everolimus'
        with self.assertRaises(ValueError):self.check()

    def test_count_inflation(self):
        self.data['summary']['null_sets']+=1
        with self.assertRaises(ValueError):self.check()

    def test_falsifier_required(self):
        self.register['claims'][0]['falsifier']=''
        with self.assertRaises(ValueError):self.check()

if __name__=='__main__':unittest.main()
