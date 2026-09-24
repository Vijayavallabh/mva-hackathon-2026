from copy import deepcopy
import json
import unittest
import check_track2_harness as harness


class CurrentStateTests(unittest.TestCase):
    def setUp(self):
        self.state=json.loads((harness.ROOT/'notes/track2-current.json').read_text())
        self.features=json.loads((harness.ROOT/'feature_list.json').read_text())['features']
        self.documents={n:(harness.ROOT/n).read_text() for n in ['AGENTS.md','session-handoff.md','README.md']}

    def test_current_harness_and_presentation_pass(self):
        self.assertTrue(harness.check()['passed'])

    def test_stale_versions_rejected(self):
        self.state['presentation_version']=13
        with self.assertRaises(ValueError):harness.validate(self.state,self.features,self.documents)

    def test_mixed_and_unsafe_paths_rejected(self):
        for value in ['notes/track2-pitch-v13.md','../outside.md','data/subject.vcf']:
            state=deepcopy(self.state);state['artifacts']['pitch']=value
            with self.subTest(value=value),self.assertRaises(ValueError):
                harness.validate(state,self.features,self.documents)

    def test_false_readiness_or_scientific_promotion_rejected(self):
        for key,value in [('upload_ready',True),('video_recorded',True),('video_url','https://example.org/video'),
                          ('phase','trans'),('clinical_exposure_margin',10),('rescue_priority','everolimus'),
                          ('provider_settings_verified',True),('licensing_scope_resolved',True)]:
            state=deepcopy(self.state);state['status'][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):
                harness.validate(state,self.features,self.documents)

    def test_multiple_active_features_rejected(self):
        self.features[0]['status']='in_progress'
        with self.assertRaises(ValueError):harness.validate(self.state,self.features,self.documents)

    def test_stale_current_label_rejected(self):
        self.documents['README.md']+='\nUse the current v12 disclosure.'
        with self.assertRaisesRegex(ValueError,'mislabeled current'):
            harness.validate(self.state,self.features,self.documents)

    def test_stale_release_instruction_rejected(self):
        version=self.state['presentation_version']
        self.documents['AGENTS.md']=self.documents['AGENTS.md'].replace(f'scripts/track2_release_v{version}.py','scripts/track2_release_v13.py')
        with self.assertRaises(ValueError):harness.validate(self.state,self.features,self.documents)

    def test_model_count_drift_rejected(self):
        self.state['model_campaign']['structures']=300
        with self.assertRaises(ValueError):harness.validate(self.state,self.features,self.documents)


if __name__=='__main__':unittest.main()
