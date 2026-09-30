"""Regression boundaries for scientific overstatements in v27."""
from copy import deepcopy
import json
import unittest
import check_track2_falsification_v27 as checker


class ClaimBoundaries(unittest.TestCase):
    def setUp(self):
        root=checker.ROOT/'notes'
        self.args=[json.loads((root/name).read_text()) for name in [
            'track2-saturation-results-v27.json','track2-specificity-results-v27.json',
            'track2-falsification-compute-v27.json','track2-falsification-register-v27.json']]
        self.args.append((root/'track2-falsification-v27.md').read_text())

    def test_public_review(self):self.assertTrue(checker.check()['passed'])

    def test_duplicated_contexts_not_independent_variants(self):
        self.args[0]['unique_single_substitution_identities']=179968
        with self.assertRaises(ValueError):checker.validate(*self.args)

    def test_negative_background_cannot_be_hidden(self):
        self.args[0]['models'][0]['windows'][0]['backgrounds']['whole_window']['negative_fraction']=.01
        with self.assertRaises(ValueError):checker.validate(*self.args)

    def test_secondary_control_failures_retained(self):
        for m in self.args[0]['models']:
            for w in m['windows']:w['expanded_gate']=True
        with self.assertRaises(ValueError):checker.validate(*self.args)

    def test_ht29_favorable_counterevidence_retained(self):
        r=next(r for r in self.args[1]['records'] if r['cell']=='HT29' and r['space']=='prime')
        r['representations']['residual_pc10']['queries'][0]['rnai_rank']=2000
        with self.assertRaises(ValueError):checker.validate(*self.args)

    def test_mcf7_sensitivity_cannot_be_erased(self):
        r=next(r for r in self.args[1]['records'] if r['cell']=='MCF7' and r['space']=='prime')
        for d in r['representations']['residual_pc10']['drug_rows']:
            if d['gene']=='BUB1B' and float(d['dose'])==.1:d['reversal_rank']=7
        with self.assertRaises(ValueError):checker.validate(*self.args)

    def test_toolkit_or_clinical_promotion_rejected(self):
        for index,key,value in [(2,'uplifting_toolkit_executed',True),(3,'clinical_exposure_margin',1),
                                (3,'independent_guide_qualified_contexts',1),(3,'rescue_priority','everolimus')]:
            args=deepcopy(self.args);args[index][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):checker.validate(*args)

    def test_scope_language_cannot_disappear(self):
        self.args[-1]=self.args[-1].replace('post-hoc sensitivity tests','confirmed causal effects')
        with self.assertRaises(ValueError):checker.validate(*self.args)


if __name__=='__main__':unittest.main()
