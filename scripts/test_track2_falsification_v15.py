from copy import deepcopy
import json
import math
import unittest
import track2_falsification_v15 as audit


class FalsificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protein=json.loads((audit.ROOT/'notes/track2-latest-protein-results.json').read_text())
        cls.register=json.loads((audit.ROOT/'notes/track2-falsification-register-v15.json').read_text())

    def test_primary_success_does_not_erase_secondary_reversals(self):
        a=audit.sequence_sensitivity(self.protein)
        self.assertEqual((a['primary_pass'],a['all_control_pass'],a['all_control_fail']),(12,4,8))
        self.assertEqual((a['negative_retained_scores'],a['positive_impaired_scores']),(11,2))
        self.assertEqual(a['independent_biological_replications'],0)

    def test_missing_duplicate_unknown_and_nonfinite_scores_rejected(self):
        for mutate in [lambda r:r.pop(),lambda r:r.append(deepcopy(r[0])),
                       lambda r:r[0].update(score=math.nan),lambda r:r[0].update(score=True),
                       lambda r:r[0].update(group='primary_retained'),lambda r:r[0].update(variant='new')]:
            d=deepcopy(self.protein);mutate(next(iter(d['models'].values()))['rows'])
            with self.assertRaises(ValueError):audit.sequence_sensitivity(d)

    def test_model_omission_rejected(self):
        d=deepcopy(self.protein);d['models'].pop(next(iter(d['models'])))
        with self.assertRaises(ValueError):audit.sequence_sensitivity(d)

    def test_survivor_improvement_can_hide_worse_useful_output(self):
        e=audit.synthetic_examples()['selection']
        self.assertLess(e['error_among_completed'][1],e['error_among_completed'][0])
        self.assertLess(e['all_enrolled_success'][1],e['all_enrolled_success'][0])
        self.assertLess(e['difference_bounds'][1],0)
        for arm in ['control','treated']:
            d=e[arm];self.assertEqual(d['enrolled'],sum(v for k,v in d.items() if k!='enrolled'))

    def test_missingness_is_not_automatic_failure_or_success(self):
        bounds=audit.synthetic_examples()['missingness']['difference_bounds']
        self.assertEqual(bounds[0],0);self.assertGreater(bounds[1],0)

    def test_invalid_denominators_rejected(self):
        for args in [(0,0,0),(10,11,0),(10,5,6),(-1,0,0),(10,True,0),(10,2.1,0)]:
            with self.assertRaises(ValueError):audit.success_bounds(*args)

    def test_current_unknowns_hold_without_claiming_refutation(self):
        d=audit.check_register(self.register)
        self.assertEqual(d['decision'],'hold_unresolved')
        self.assertEqual(d['failed'],[])
        self.assertFalse(d['clinical_recommendation'])

    def all_met(self):
        gates=deepcopy(self.register['advancement_gates'])
        for name,g in gates.items():
            kind='observed_relevant_context'
            if name=='hypothesis_lock':kind='locked_protocol'
            if name=='source_integrity':kind='source_audit'
            g.update(status='met',evidence_kind=kind,evidence_refs=['synthetic-test-fixture'],rule_fixed_before_results=True)
        return gates

    def test_complete_evidence_only_allows_preclinical_review(self):
        d=audit.evaluate_advancement(self.all_met())
        self.assertEqual(d['decision'],'eligible_for_preclinical_review')
        self.assertFalse(d['clinical_recommendation'])

    def test_failed_safety_blocks_favorable_function(self):
        g=self.all_met();g['normal_tissue_safety']['status']='failed'
        self.assertEqual(audit.evaluate_advancement(g)['decision'],'stop_tested_context')

    def test_models_plans_and_source_audit_cannot_replace_biology(self):
        for kind in ['model_prediction','planned','source_audit','locked_protocol']:
            g=self.all_met();g['functional_benefit']['evidence_kind']=kind
            with self.assertRaises(ValueError):audit.evaluate_advancement(g)

    def test_source_audit_cannot_replace_exposure(self):
        g=self.all_met();g['exposure_match']['evidence_kind']='source_audit'
        with self.assertRaises(ValueError):audit.evaluate_advancement(g)

    def test_post_hoc_success_remains_exploratory(self):
        g=self.all_met();g['functional_benefit']['rule_fixed_before_results']=False
        self.assertEqual(audit.evaluate_advancement(g)['decision'],'hold_unresolved')

    def test_missing_prerequisite_and_unreferenced_result_rejected(self):
        g=self.all_met();g.pop('replication')
        with self.assertRaises(ValueError):audit.evaluate_advancement(g)
        g=self.all_met();g['replication']['evidence_refs']=[]
        with self.assertRaises(ValueError):audit.evaluate_advancement(g)

    def test_cyclic_or_missing_claims_rejected(self):
        r=deepcopy(self.register);r['claims'][0]['depends_on']=['G02']
        with self.assertRaises(ValueError):audit.check_register(r)
        r=deepcopy(self.register);r['claims']=r['claims'][:5]
        with self.assertRaises(ValueError):audit.check_register(r)

    def test_recorded_analysis_matches_recomputation(self):
        self.assertTrue(audit.check()['passed'])


if __name__=='__main__':unittest.main()
