import copy,json,unittest
from pathlib import Path
from track2_evo2_result_audit import check_summary

class EvoOutputAuditTests(unittest.TestCase):
 def setUp(self):
  root=Path(__file__).resolve().parents[1]
  self.result=json.loads((root/'notes/track2-evo2-7b-results.json').read_text())
  self.plan=json.loads((root/'notes/track2-evo2-plan.json').read_text())
  path=root/'results/feat009/evo2-public-inputs-v1/inputs.json'
  if not path.exists():self.skipTest('Public benchmark input archive absent; reproduce via resource script')
  self.doc=json.loads(path.read_text())
 def test_complete_real_output(self):self.assertTrue(check_summary(self.result,self.doc,self.plan)['arithmetic_checked'])
 def test_wrong_allele_identity_rejected(self):
  self.result['candidate_scores'][0]['ref']='A'
  with self.assertRaises(ValueError):check_summary(self.result,self.doc,self.plan)
 def test_score_arithmetic_corruption_rejected(self):
  self.result['candidate_scores'][0]['delta_mean_strands']+=0.1
  with self.assertRaises(ValueError):check_summary(self.result,self.doc,self.plan)
 def test_false_clinical_promotion_rejected(self):
  self.result['clinical_classification']=True
  with self.assertRaises(ValueError):check_summary(self.result,self.doc,self.plan)
 def test_missing_control_cannot_be_hidden(self):
  self.result['benchmark'].pop()
  with self.assertRaises(ValueError):check_summary(self.result,self.doc,self.plan)

if __name__=='__main__':unittest.main()
