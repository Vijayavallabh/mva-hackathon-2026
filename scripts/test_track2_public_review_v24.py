from copy import deepcopy
import json
import unittest
import track2_public_review_v24 as review

class PublicReviewTests(unittest.TestCase):
    def setUp(self):
        self.report=(review.ROOT/'notes/track2-report-v24.md').read_text()
        self.deck=(review.ROOT/'notes/track2-slides-v24.html').read_text()
        self.requirements=json.loads((review.ROOT/'notes/track2-requirements-v24.json').read_text())
        self.community=json.loads((review.ROOT/'notes/track2-community-audit-v24.json').read_text())

    def test_current_public_review_and_methods(self):
        result=review.check()
        self.assertEqual((result['slides'],result['narration_words'],result['methods_fields']),(9,342,11))
        self.assertEqual(result['claim_records'],32)
        self.assertFalse(result['upload_ready'])
        self.assertFalse(result['biological_validation'])

    def test_all_closed_and_open_threads_required(self):
        for mutate in [lambda c:c['threads'].pop(),lambda c:c['listed_numbers'].remove(25),lambda c:c.update(closed_count=0),lambda c:c.update(visible_comments=67)]:
            c=deepcopy(self.community);mutate(c)
            with self.assertRaises(ValueError):review.requirements_checks(self.requirements,c)

    def test_fetch_failure_cannot_be_called_complete(self):
        c=deepcopy(self.community);c['threads'][0]['status']='HTTPError'
        with self.assertRaises(ValueError):review.requirements_checks(self.requirements,c)

    def test_old_quota_or_invented_remaining_attempts_rejected(self):
        for change in [dict(submission_limit=1),dict(quota_remaining=3),dict(only_latest_reviewed=False)]:
            r=deepcopy(self.requirements);r.update(change)
            with self.assertRaises(ValueError):review.requirements_checks(r,self.community)

    def test_unverified_licensing_and_provider_promotions_rejected(self):
        for field in ['licensing_scope_resolved','provider_settings_verified']:
            r=deepcopy(self.requirements);r[field]=True
            with self.assertRaises(ValueError):review.requirements_checks(r,self.community)

    def test_required_disclosure_and_abstract_limit(self):
        with self.assertRaises(ValueError):review.report_checks(self.report.replace('**B9:','**X9:'))
        r=self.report.replace('We propose a qualified everolimus experiment',' '.join(['word']*501)+' We propose a qualified everolimus experiment')
        with self.assertRaises(ValueError):review.report_checks(r)
        for term in ['Fireworks','ColabFold','unverified']:
            with self.subTest(term=term),self.assertRaises(ValueError):review.report_checks(self.report.replace(term,'omitted'))

    def test_relative_report_links_rejected_for_upload(self):
        r=self.report.replace('https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v15.json','track2-evidence-v15.json')
        with self.assertRaises(ValueError):review.report_checks(r)

    def test_model_uncertainty_cannot_disappear(self):
        for term in ['8/12','11/24','1,000-fold']:
            with self.subTest(term=term),self.assertRaises(ValueError):review.report_checks(self.report.replace(term,'omitted'))

    def test_favourable_post_hoc_result_must_remain_qualified(self):
        for term in ['Favourable HT29','Post-hoc / shared-pattern removal','adjusted tail 0.042','5 reagents; minimum 6','Does not pass the full filter','Operational; uncalibrated']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(term,'omitted'))

    def test_compound_identity_and_nominal_exposure_cannot_disappear(self):
        for term in ['unresolved stereochemistry','0.1 µM nominal culture','All 6 fail drug QC','Replicate correlation missing','Neither benefit nor harm']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(term,'omitted'))

    def test_report_keeps_denominators_and_evidence_limits(self):
        for term in ['not distinct drugs or independent experiments','19 comparisons reuse 14','174/180','uncalibrated','does not match shRNA seed','0.042','0/42','not new neural-model inference']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.report_checks(self.report.replace(term,'omitted'))

    def test_joint_intervention_and_independent_genetic_controls_required(self):
        for term in ['Drug + qualified deficit','Independent genetic control','Every enrolled cell','Function + daughter fate']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(term,'omitted'))

    def test_trial_scope_and_synthetic_example_remain_in_report(self):
        self.assertIn('297 evaluable intermediate-risk RMS',self.report)
        self.assertIn('synthetic example, not experimental data',self.report)
        self.assertIn('20/80 (25%) to 5/45 (11.1%)',self.report)

    def test_frozen_campaign_audit_is_required(self):
        from unittest.mock import patch
        with patch.object(review,'digest',return_value='0'*64),self.assertRaises(ValueError):
            review.transcriptome_checks()

    def test_research_summary_retains_partial_positive_and_failed_drug_qc(self):
        result=review.transcriptome_checks()
        self.assertEqual(result['ht29_post_hoc_reagents'],5)
        self.assertAlmostEqual(result['ht29_post_hoc_adjusted_tail'],.041995800419958006)
        self.assertFalse(result['ht29_full_filter_passed'])
        self.assertEqual(result['phase2_reference_matching_qc_passes'],0)
        self.assertFalse(result['drug_ranking_changed'])

    def test_safety_gate_cannot_be_softened_or_promoted(self):
        for old,new in [('Failed safety','Possible benefit'),('Preclinical review only','Clinical treatment')]:
            with self.subTest(old=old),self.assertRaises(ValueError):review.presentation_checks(self.deck.replace(old,new))

    def test_primary_trial_uncertainty_and_indirectness_required(self):
        for term in ['Primary ITT difference','Sirolimus − placebo / 13 weeks','95% CI −4.61 to 0.34; p=0.089','40 older adults','Indirect for everolimus/MVA']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(term,'omitted'))

    def test_favourable_animal_counterweight_cannot_disappear(self):
        for term in ['Adult female mice','Exercise gains retained','Grip strength / PoWeR']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(term,'omitted'))

    def test_futility_and_invalidity_remain_different(self):
        for old in ['Invalid assay','Meaningful benefit excluded','Stop the tested claim']:
            with self.subTest(old=old),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(old,'omitted'))

    def test_rnai_counterweights_and_reuse_cannot_disappear(self):
        for term in ['45/54','0.01422','0.08532','Post-hoc sensitivity','Same experiments as v19','Uncalibrated tails','no BUB1B CRISPR profile']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(term,'omitted'))
        for term in ['not independent biological replication','0.21276','5/36','0/36','32 claim records','21/297','not sample sizes']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.report_checks(self.report.replace(term,'omitted'))

    def test_frozen_rnai_audit_cannot_be_rebound(self):
        from unittest.mock import patch
        with patch.object(review,'digest',return_value='0'*64),self.assertRaises(ValueError):
            review.rnai_checks()

    def test_full_acknowledgement_and_static_resources(self):
        for old,new in [('We acknowledge their trust','Thanks'),('</body>','<img src="https://example.com/x.png"></body>')]:
            with self.subTest(old=old),self.assertRaises(ValueError):review.presentation_checks(self.deck.replace(old,new))

if __name__=='__main__':unittest.main()
