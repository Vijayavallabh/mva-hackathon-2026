"""Checks against missing controls, sign-selection and overclaimed model evidence."""
import copy
import json
from pathlib import Path
import unittest
from track2_esm_pilot import control_gate
from track2_latest_analysis import sequence_check


class LatestScoreTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads(Path('notes/track2-latest-model-plan.json').read_text())
        variants=self.plan['protein_controls']+[dict(variant='N1002K',group='candidate')]
        rows=[dict(window=w['name'],variant=v['variant'],group=v['group'],score=0.0 if v['group']=='primary_retained' else -1.0)
              for w in self.plan['protein_windows'] for v in variants]
        gate=control_gate([r for r in rows if r['group']!='candidate'])
        gate.update(repeat_max_abs_difference=0.0,numerical_pass=True)
        self.result=dict(model='synthetic',rows=rows,gate=gate,clinical_classification=False,drug_ranking_changed=False,phase_resolved=False)

    def test_valid_complete_design(self):
        self.assertTrue(sequence_check(self.result,self.plan)['gate']['pass'])

    def test_missing_candidate_rejected(self):
        self.result['rows'].pop()
        with self.assertRaises(ValueError):sequence_check(self.result,self.plan)

    def test_duplicated_control_rejected(self):
        self.result['rows'][0]=copy.deepcopy(self.result['rows'][1])
        with self.assertRaises(ValueError):sequence_check(self.result,self.plan)

    def test_relabelled_assay_control_rejected(self):
        self.result['rows'][0]['group']='primary_retained'
        with self.assertRaises(ValueError):sequence_check(self.result,self.plan)

    def test_nonfinite_candidate_rejected(self):
        self.result['rows'][-1]['score']=float('nan')
        with self.assertRaises(ValueError):sequence_check(self.result,self.plan)

    def test_contrary_candidate_sign_is_preserved(self):
        self.result['rows'][-1]['score']=4.0
        self.assertEqual(sequence_check(self.result,self.plan)['candidate'][-1]['score'],4.0)

    def test_honest_failed_control_retained(self):
        self.result['rows'][0]['score']=2.0
        self.result['gate'].update(control_gate([r for r in self.result['rows'] if r['group']!='candidate']))
        self.assertFalse(sequence_check(self.result,self.plan)['gate']['pass'])

    def test_invented_pass_rejected(self):
        self.result['rows'][0]['score']=2.0
        with self.assertRaises(ValueError):sequence_check(self.result,self.plan)

    def test_failed_repeat_cannot_remain_pass(self):
        self.result['gate']['repeat_max_abs_difference']=0.01
        with self.assertRaises(ValueError):sequence_check(self.result,self.plan)

    def test_no_clinical_promotion(self):
        self.result['clinical_classification']=True
        with self.assertRaises(ValueError):sequence_check(self.result,self.plan)


if __name__=='__main__':unittest.main()
