from copy import deepcopy
import json
import unittest
from pathlib import Path
import tempfile
import shutil
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

    def test_missing_research_addendum_rejected(self):
        self.state.pop('research_addendum')
        with self.assertRaisesRegex(ValueError, 'research addendum'):
            harness.validate(self.state,self.features,self.documents)

    def test_every_research_route_is_checked(self):
        for field in list(harness.RESEARCH_PATHS) + ['archive']:
            state=deepcopy(self.state);state['research_addendum'][field]='data/subject.vcf'
            with self.subTest(field=field),self.assertRaises(ValueError):
                harness.validate(state,self.features,self.documents)

    def test_fabricated_research_counts_and_promotion_rejected(self):
        for field,value in [('gpus',80),('gpus',8.0),('compound_profiles',999999),
                            ('query_compound_comparisons',1),('resampled_reagent_sets',1),
                            ('primary_query_gates_passed',14),('drug_ranking_changed',True),
                            ('status','running')]:
            state=deepcopy(self.state);state['research_addendum'][field]=value
            with self.subTest(field=field,value=value),self.assertRaises(ValueError):
                harness.validate(state,self.features,self.documents)

    def test_combined_review_cannot_silently_fall_back_to_v18(self):
        for field,value in [('script','scripts/track2_public_review_v18.py'),
                            ('guide','notes/track2-reviewer-guide-v18.md'),
                            ('readiness','notes/track2-owner-readiness-v18.md')]:
            state=deepcopy(self.state);state['current_review'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):
                harness.validate(state,self.features,self.documents)

    def test_integrated_versions_preserve_research_version(self):
        self.assertEqual(self.state['presentation_version'],21)
        self.assertEqual(self.state['harness_version'],21)
        self.assertEqual(self.state['research_addendum']['version'],19)
        self.state['harness_review']='notes/track2-harness-review-v18.md'
        with self.assertRaisesRegex(ValueError,'Stale harness'):
            harness.validate(self.state,self.features,self.documents)

    def test_correct_independent_version_labels_accepted(self):
        self.documents['README.md']+='\nUse the current v21 harness and current v19 addendum with the current v21 presentation and current v21 ledger.'
        harness.validate(self.state,self.features,self.documents)

    def test_stale_addendum_label_rejected(self):
        self.documents['README.md']+='\nUse the current v18 addendum.'
        with self.assertRaisesRegex(ValueError,'mislabeled current'):
            harness.validate(self.state,self.features,self.documents)

    def test_missing_reviewer_route_in_entry_docs_rejected(self):
        for name in self.documents:
            docs=deepcopy(self.documents)
            docs[name]=docs[name].replace(harness.CURRENT_REVIEW['guide'],'old-guide.md')
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,'combined research route'):
                harness.validate(self.state,self.features,docs)

    def test_public_paths_reject_parent_and_leaf_symlinks(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);(root/'real').mkdir();(root/'real/public.txt').write_text('public')
            (root/'alias').symlink_to(root/'real',target_is_directory=True)
            (root/'leaf.txt').symlink_to(root/'real/public.txt')
            for relative in ['alias/public.txt','leaf.txt','../outside.txt']:
                with self.subTest(relative=relative),self.assertRaises(ValueError):
                    harness.public_path(root,relative)

    def test_frozen_audit_cannot_be_rewritten_to_omit_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);(root/'notes').mkdir()
            audit=json.loads((harness.ROOT/harness.RESEARCH_PATHS['audit']).read_text())
            audit['public_input_sha256']={}
            (root/harness.RESEARCH_PATHS['audit']).write_text(json.dumps(audit))
            with self.assertRaisesRegex(ValueError,'Frozen campaign audit changed'):
                harness.campaign_audit(root)

    def test_missing_bound_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            audit=json.loads((harness.ROOT/harness.RESEARCH_PATHS['audit']).read_text())
            for relative in list(audit['public_input_sha256'])+[harness.RESEARCH_PATHS['audit']]:
                dest=root/relative;dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(harness.ROOT/relative,dest)
            (root/harness.RESEARCH_PATHS['followup_results']).unlink()
            with self.assertRaisesRegex(ValueError,'Missing public artifact'):
                harness.campaign_audit(root)

    def test_isolated_public_review_uses_no_protected_paths_or_network(self):
        from audit_track2_harness import audit
        result=audit()
        self.assertTrue(result['passed'])
        self.assertFalse(result['project_environment_used'])
        self.assertEqual(set(result['blocked_probes']),
                         {'network','process','protected_path','credentials','external_path','write'})
        self.assertEqual(result['review']['research_addendum']['post_hoc_full_filters_passed'],0)


class ResearchSummaryTests(unittest.TestCase):
    def setUp(self):
        self.first,self.second,self.followup,self.identity,self.audit=[json.loads(
            (harness.ROOT/harness.RESEARCH_PATHS[k]).read_text()) for k in
            ['primary_results','phase2_results','followup_results','identity_audit','audit']]

    def check(self):
        return harness.research_summary(self.first,self.second,self.followup,self.identity,self.audit)

    def test_summary_matches_completed_outputs(self):
        r=self.check()
        self.assertEqual(r['resampled_reagent_sets'],560000)
        self.assertEqual(r['primary_query_gates_passed'],0)
        self.assertEqual(r['ht29_post_hoc_reagents'],5)
        self.assertFalse(r['ht29_full_filter_passed'])

    def test_inflated_comparison_counts_rejected(self):
        self.audit['score_vectors'][0]['profiles']+=1
        self.audit['score_vectors'][0]['comparisons']+=39
        with self.assertRaises(ValueError):self.check()

    def test_lost_followup_query_coverage_rejected(self):
        self.followup['gpu_runs'][0]['query_ids'].pop()
        with self.assertRaisesRegex(ValueError,'query coverage'):self.check()

    def test_failed_drug_qc_cannot_become_qualified_evidence(self):
        for q in self.second['queries']:
            for space in q['spaces']:
                for r in space['named_compounds']:
                    if r['compound']=='everolimus' and r['compound_id']==self.identity['eligible_identity_id']:
                        r['quality_pass']=True
        with self.assertRaises(ValueError):self.check()

    def test_favourable_ht29_counterweight_cannot_disappear(self):
        self.followup['rows']=[r for r in self.followup['rows'] if not
            (r['cell_id']=='HT29' and r['arm']=='provider_members_shared_pc1_removed')]
        with self.assertRaisesRegex(ValueError,'HT29 counterweight'):self.check()

    def test_partial_positive_cannot_become_full_pass(self):
        row=next(r for r in self.followup['rows'] if r['cell_id']=='HT29' and
                 r['arm']=='provider_members_shared_pc1_removed')
        row['same_operational_filter']=True
        with self.assertRaises(ValueError):self.check()


if __name__=='__main__':unittest.main()
