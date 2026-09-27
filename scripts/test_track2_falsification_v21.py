import copy
import json
import unittest
from pathlib import Path
import track2_falsification_v21 as f

def fixture():
    # Arbitrary synthetic units. These values are not assay recommendations.
    return dict(schema_version=21,scope='qualified_non_cancer_model',evidence_kind='synthetic',
        gates={k:'pass' for k in f.GATES},benefit=dict(unit='synthetic benefit',interval=[3.,5.],margin=2.),
        harms={h:dict(unit='synthetic injury',interval=[-1.,1.],margin=2.) for h in f.HARMS},
        safety_stop_observed=False)

class Decisions(unittest.TestCase):
    def test_all_pass_only_allows_review(self):
        x=f.decide(fixture());self.assertEqual(x['decision'],'PRECLINICAL_REVIEW_ONLY');self.assertFalse(x['clinical_recommendation'])
    def test_every_unknown_prerequisite_holds(self):
        for key in f.GATES:
            with self.subTest(key=key):
                x=fixture();x['gates'][key]='unknown';self.assertEqual(f.decide(x)['decision'],'HOLD')
    def test_failed_assay_cannot_disprove_biology(self):
        x=fixture();x['gates']['assay_valid']='fail';x['benefit']['interval']=[-5,-3]
        self.assertEqual(f.decide(x)['decision'],'INVALID_HOLD')
    def test_unlocked_plan_is_not_confirmation(self):
        x=fixture();x['gates']['plan_locked']='fail';self.assertEqual(f.decide(x)['decision'],'INVALID_HOLD')
    def test_branch_failure_stays_scoped(self):
        for gate in ['model_qualified','branch_eligible']:
            x=fixture();x['gates'][gate]='fail';self.assertEqual(f.decide(x)['decision'],'STOP_BRANCH')
    def test_nonsignificance_does_not_pass_safety(self):
        for harm in f.HARMS:
            x=fixture();x['harms'][harm]['interval']=[-3,4]
            self.assertEqual(f.decide(x)['decision'],'HOLD')
    def test_injury_cannot_be_offset_by_benefit(self):
        for harm in f.HARMS:
            x=fixture();x['benefit']['interval']=[100,200];x['harms'][harm]['interval']=[3,4]
            self.assertEqual(f.decide(x)['decision'],'STOP_SAFETY_REVIEW')
    def test_injury_stops_even_with_unknown_exposure(self):
        x=fixture();x['gates']['exposure_bridge']='unknown';x['harms']['recovery']['interval']=[3,4]
        self.assertEqual(f.decide(x)['decision'],'STOP_SAFETY_REVIEW')
    def test_observed_trigger_stops_before_attribution(self):
        x=fixture();x['gates']['assay_valid']='unknown';x['safety_stop_observed']=True
        self.assertEqual(f.decide(x)['decision'],'STOP_SAFETY_REVIEW')
    def test_meaningful_benefit_excluded_is_scoped_futility(self):
        x=fixture();x['benefit']['interval']=[-1,1]
        self.assertEqual(f.decide(x)['decision'],'STOP_TESTED_BENEFIT')
    def test_ambiguous_benefit_is_not_negative(self):
        x=fixture();x['benefit']['interval']=[-1,5];self.assertEqual(f.decide(x)['decision'],'HOLD')
    def test_threshold_boundaries_hold(self):
        for target in ['benefit',*f.HARMS]:
            x=fixture();e=x['benefit'] if target=='benefit' else x['harms'][target]
            e['interval']=[2,2];self.assertEqual(f.decide(x)['decision'],'HOLD')
    def test_missing_measurement_or_margin_never_passes(self):
        for target in ['benefit',*f.HARMS]:
            for field in ['margin','interval']:
                x=fixture();e=x['benefit'] if target=='benefit' else x['harms'][target]
                e[field]=None;self.assertEqual(f.decide(x)['decision'],'HOLD')
    def test_nonfinite_and_bool_rejected(self):
        for value in [float('nan'),float('inf'),-float('inf'),True,'3']:
            x=fixture();x['benefit']['interval']=[value,5]
            with self.assertRaises(ValueError):f.decide(x)
    def test_bad_interval_rejected(self):
        for interval in [[5,3],[3],[3,4,5],'3,5']:
            x=fixture();x['benefit']['interval']=interval
            with self.assertRaises(ValueError):f.decide(x)
    def test_nonpositive_margin_rejected(self):
        for margin in [0,-1,True,float('nan')]:
            x=fixture();x['benefit']['margin']=margin
            with self.assertRaises(ValueError):f.decide(x)
    def test_missing_gate_or_harm_rejected(self):
        for area,key in [('gates','all_enrolled_accounted'),('harms','regeneration')]:
            x=fixture();del x[area][key]
            with self.assertRaises(ValueError):f.decide(x)
    def test_clinical_scope_rejected(self):
        x=fixture();x['scope']='patient_treatment'
        with self.assertRaises(ValueError):f.decide(x)
    def test_synthetic_results_cannot_be_called_unmeasured(self):
        x=fixture();x['evidence_kind']='not_measured'
        with self.assertRaises(ValueError):f.decide(x)
    def test_current_contract_is_unmeasured_hold(self):
        x=json.loads((f.ROOT/'notes/track2-decision-contract-v21.json').read_text())
        self.assertEqual(f.decide(x)['decision'],'HOLD')
    def test_missing_stop_assessment_holds(self):
        x=fixture();x['safety_stop_observed']=None;self.assertEqual(f.decide(x)['decision'],'HOLD')
    def test_register_and_decisions_preserved(self):self.assertTrue(f.check()['passed'])

class ArtifactClaims(unittest.TestCase):
    def setUp(self):
        self.register=json.loads((f.ROOT/'notes/track2-falsification-register-v21.json').read_text())
        self.baseline=json.loads((f.ROOT/'notes/track2-falsification-register-v15.json').read_text())
        self.evidence=json.loads((f.ROOT/'notes/track2-evidence-v21.json').read_text())
        self.old=json.loads((f.ROOT/'notes/track2-evidence-v15.json').read_text())
    def test_register_cannot_silently_promote_a_gate(self):
        self.register['advancement_gates']['functional_benefit']['status']='pass'
        with self.assertRaisesRegex(ValueError,'advancement gates'):
            f.validate_register(self.register,self.baseline)
    def test_unknown_dependency_rejected(self):
        self.register['claims'][0]['depends_on']=['invented']
        with self.assertRaisesRegex(ValueError,'dependency'):
            f.validate_register(self.register,self.baseline)
    def test_evidence_cannot_claim_known_phase_or_margin(self):
        for field,value in [('phase','trans'),('rescue_priority','everolimus'),('clinical_exposure_margin',2)]:
            changed=copy.deepcopy(self.evidence);changed[field]=value
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'promotion'):
                f.validate_evidence(changed,self.old)
    def test_duplicate_source_cannot_inflate_inventory(self):
        self.evidence['additional_sources'][1]=copy.deepcopy(self.evidence['additional_sources'][0])
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            f.validate_evidence(self.evidence,self.old)

if __name__=='__main__':unittest.main()
