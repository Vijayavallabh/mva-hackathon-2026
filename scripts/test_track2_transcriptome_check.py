"""Reject misleading interpretations and incomplete public campaign exports."""
import copy
import json
from pathlib import Path
import unittest
from check_track2_transcriptome import validate,validate_followup

ROOT=Path(__file__).resolve().parents[1]


class PublicCampaignChecks(unittest.TestCase):
    def setUp(self):
        self.first,self.second,self.identity=[json.loads((ROOT/'notes'/name).read_text()) for name in
            ['track2-transcriptome-results-v19.json','track2-transcriptome-phase2-results-v19.json','track2-transcriptome-identity-v19.json']]

    def check(self):return validate(self.first,self.second,self.identity)

    def test_complete_export(self):self.assertTrue(self.check()['passed'])

    def test_no_priority_promotion(self):
        self.first['rescue_priority']='everolimus'
        with self.assertRaises(ValueError):self.check()

    def test_missing_gpu(self):
        self.second['gpu_runs'].pop()
        with self.assertRaises(ValueError):self.check()

    def test_duplicate_context(self):
        self.first['queries'][1]=copy.deepcopy(self.first['queries'][0])
        with self.assertRaises(ValueError):self.check()

    def test_identity_not_name_only(self):
        self.identity['eligible_identity_id']='BRD-A25736793'
        with self.assertRaises(ValueError):self.check()

    def test_query_failure_cannot_be_erased(self):
        q=self.first['queries'][0];q['operational_query_gate']=not q['operational_query_gate']
        with self.assertRaises(ValueError):self.check()

    def test_nonfinite_score(self):
        self.first['queries'][0]['spaces'][0]['named_compounds'][0]['correlation']=float('nan')
        with self.assertRaises(ValueError):self.check()

    def test_nonfinite_query_is_not_a_negative_result(self):
        self.first['queries'][0]['median_target_z']=float('nan')
        with self.assertRaises(ValueError):self.check()

    def test_drug_qc_cannot_be_overridden(self):
        r=self.first['queries'][0]['spaces'][0]['named_compounds'][0];r['quality_pass']=not r['quality_pass']
        with self.assertRaises(ValueError):self.check()

    def test_incomplete_resampling(self):
        self.first['queries'][0]['null_draws']=9999
        with self.assertRaises(ValueError):self.check()

    def test_post_hoc_cannot_replace_primary(self):
        f=json.loads((ROOT/'notes/track2-transcriptome-followup-results-v19.json').read_text())
        self.assertTrue(validate_followup(f,self.first))
        f['primary_gate_replaced']=True
        with self.assertRaises(ValueError):validate_followup(f,self.first)

    def test_post_hoc_must_remain_labelled(self):
        f=json.loads((ROOT/'notes/track2-transcriptome-followup-results-v19.json').read_text())
        f['post_hoc']=False
        with self.assertRaises(ValueError):validate_followup(f,self.first)

    def test_nonfinite_followup_is_not_a_negative_result(self):
        f=json.loads((ROOT/'notes/track2-transcriptome-followup-results-v19.json').read_text())
        f['rows'][0]['split_median']=float('nan')
        with self.assertRaises(ValueError):validate_followup(f,self.first)


if __name__=='__main__':unittest.main()
