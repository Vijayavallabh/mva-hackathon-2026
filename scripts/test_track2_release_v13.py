import unittest
import track2_release_v13 as release

class ModelPresentationTests(unittest.TestCase):
 def setUp(self):self.deck=(release.ROOT/'notes/track2-slides-v13.html').read_text()
 def test_current_deck_and_narration(self):
  result=release.scientific_checks()
  self.assertEqual(result['slides'],8)
  self.assertEqual(result['narration_words'],329)
 def test_external_script_is_rejected(self):
  with self.assertRaises(ValueError):release.presentation_checks(self.deck.replace('</head>','<script src="https://example.org/model.js"></script></head>'))
 def test_control_limitation_cannot_be_deleted(self):
  with self.assertRaises(ValueError):release.presentation_checks(self.deck.replace('Impaired controls also fold','Candidate is validated'))
 def test_cross_gene_limit_cannot_be_deleted(self):
  with self.assertRaises(ValueError):release.presentation_checks(self.deck.replace('BRCA1 benchmark does not validate BUB1B','Validated clinical predictor'))
 def test_trial_estimate_cannot_be_rewritten(self):
  with self.assertRaises(ValueError):release.presentation_checks(self.deck.replace('HR 0.86','HR 0.20'))
 def test_full_acknowledgement_required(self):
  with self.assertRaises(ValueError):release.presentation_checks(self.deck.replace('We acknowledge their trust in making this Hackathon possible.','Thank you.'))
 def test_no_wetlab_boundary_required(self):
  with self.assertRaises(ValueError):release.presentation_checks(self.deck.replace('No wet-lab experiments.','Rescue demonstrated.'))
 def test_old_snapshot_location_is_protected(self):
  with self.assertRaises(ValueError):release.location(release.ROOT/'results/feat009/jvv7_track2_research_v12')

if __name__=='__main__':unittest.main()
