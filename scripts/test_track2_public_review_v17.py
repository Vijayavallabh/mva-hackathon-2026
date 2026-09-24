from copy import deepcopy
import json
import unittest
import track2_public_review_v17 as review

class PublicReviewTests(unittest.TestCase):
    def setUp(self):
        self.report=(review.ROOT/'notes/track2-report-v17.md').read_text()
        self.deck=(review.ROOT/'notes/track2-slides-v17.html').read_text()
        self.requirements=json.loads((review.ROOT/'notes/track2-requirements-v17.json').read_text())
        self.community=json.loads((review.ROOT/'notes/track2-community-audit-v17.json').read_text())

    def test_current_public_review_and_methods(self):
        result=review.check()
        self.assertEqual((result['slides'],result['narration_words'],result['methods_fields']),(8,342,11))
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
        with self.assertRaises(ValueError):review.report_checks(self.report.replace('**B9 —','**X9 —'))
        r=self.report.replace('We propose a falsifiable test of everolimus,',' '.join(['word']*501)+' We propose a falsifiable test of everolimus,')
        with self.assertRaises(ValueError):review.report_checks(r)
        for term in ['Fireworks','ColabFold','unverified']:
            with self.subTest(term=term),self.assertRaises(ValueError):review.report_checks(self.report.replace(term,'omitted'))

    def test_relative_report_links_rejected_for_upload(self):
        r=self.report.replace('https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v15.json','track2-evidence-v15.json')
        with self.assertRaises(ValueError):review.report_checks(r)

    def test_model_uncertainty_cannot_disappear(self):
        for term in ['8/12','11/24','1,000-fold']:
            with self.subTest(term=term),self.assertRaises(ValueError):review.report_checks(self.report.replace(term,'omitted'))

    def test_synthetic_example_must_not_become_patient_data(self):
        with self.assertRaises(ValueError):review.presentation_checks(self.deck.replace('Synthetic example · not data','Observed patient response'))

    def test_bar_lengths_share_a_percentage_scale(self):
        for old,new in [('width="44.444444"','width="128"'),('width="240"','width="290"')]:
            with self.subTest(old=old),self.assertRaises(ValueError):review.presentation_checks(self.deck.replace(old,new))

    def test_clinical_trial_uncertainty_and_scope(self):
        for term in ['95% CI 0.58–1.26','Not non-cancer everolimus rescue','p=0.44']:
            with self.subTest(term=term),self.assertRaises(ValueError):review.presentation_checks(self.deck.replace(term,'omitted'))

    def test_safety_gate_cannot_be_softened_or_promoted(self):
        for old,new in [('Failed safety','Possible benefit'),('Preclinical review only','Clinical treatment')]:
            with self.subTest(old=old),self.assertRaises(ValueError):review.presentation_checks(self.deck.replace(old,new))

    def test_full_acknowledgement_and_static_resources(self):
        for old,new in [('We acknowledge their trust','Thanks'),('</body>','<img src="https://example.com/x.png"></body>')]:
            with self.subTest(old=old),self.assertRaises(ValueError):review.presentation_checks(self.deck.replace(old,new))

if __name__=='__main__':unittest.main()
