from copy import deepcopy
import json
import unittest
import track2_public_review_v34 as review


class IntegratedEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.report=(review.ROOT/'notes/track2-report-v34.md').read_text()
        self.deck=(review.ROOT/'notes/track2-slides-v34.html').read_text()
        self.results=json.loads((review.ROOT/'notes/track2-perturbseq-results-v31.json').read_text())

    def test_complete_review_preserves_all_claims_and_hold(self):
        result=review.check()
        self.assertEqual((result['claim_records'],result['slides'],result['narration_words']),(52,9,336))
        self.assertFalse(result['upload_ready'])
        self.assertFalse(result['biological_validation'])

    def test_displayed_correlations_cannot_disagree_with_results(self):
        for value in ['0.6572','0.1197','0.1043','0.5836']:
            deck=self.deck.replace(value,'0.9999')
            with self.subTest(value=value),self.assertRaises(ValueError):
                review.perturbseq_numbers(self.results,self.report,deck)

    def test_wrong_rank_denominators_rejected(self):
        for value in ['171.5 / 2,154','323.5 / 2,077']:
            with self.subTest(value=value),self.assertRaises(ValueError):
                review.perturbseq_numbers(self.results,self.report,self.deck.replace(value,'1 / 100'))

    def test_guide_dependence_and_control_gap_cannot_disappear(self):
        for value in ['One shared guide pair','Repeated splits reuse cells','no unselected-control sensitivity']:
            with self.subTest(value=value),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(value,''))

    def test_prior_control_failures_and_drug_query_gap_retained(self):
        for value in ['0/24','Retrieval: missing','Model gains unvalidated']:
            with self.subTest(value=value),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(value,''))

    def test_safety_override_cannot_be_relabelled(self):
        with self.assertRaises(ValueError):
            review.presentation_checks(self.deck.replace('Stop; review injury','Proceed with benefit'))

    def test_optical_chart_cannot_inflate_guide_coverage(self):
        changed=self.deck.replace('>11</text>','>25</text>')
        with self.assertRaisesRegex(ValueError,'Optical chart'):
            review.presentation_checks(changed)

    def test_optical_pending_status_cannot_disappear(self):
        for phrase in ['Model gains unvalidated','Interphase analysis pending']:
            with self.subTest(phrase=phrase),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(phrase,''))

    def test_required_acknowledgement_and_disclosure_retained(self):
        with self.assertRaises(ValueError):
            review.report_checks(self.report.replace('We acknowledge their trust','Thank you'))
        with self.assertRaises(ValueError):
            review.report_checks(self.report.replace('Fireworks-hosted','Undisclosed-hosted'))

    def test_missing_and_resampling_limits_remain_explicit(self):
        for phrase in ['unselected-control sensitivity is unavailable','not neural inference','52 claim records']:
            report=self.report.replace(phrase,'')
            with self.subTest(phrase=phrase),self.assertRaises(ValueError):
                review.perturbseq_numbers(self.results,report,self.deck)

    def test_no_quota_or_compliance_inference(self):
        rules=json.loads((review.ROOT/'notes/track2-requirements-v34.json').read_text())
        community=json.loads((review.ROOT/'notes/track2-community-audit-v34.json').read_text())
        for key,value in [('quota_remaining',3),('licensing_scope_resolved',True),('submission_limit',1)]:
            changed=deepcopy(rules);changed[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):
                review.requirements_checks(changed,community)

    def test_missing_repository_links_rejected(self):
        with self.assertRaisesRegex(ValueError,'Missing repository link'):
            review.repository_links('https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-requirements-review-v34.md')

    def test_stale_video_word_count_rejected(self):
        desc=(review.ROOT/'notes/track2-video-description-v34.md').read_text()
        with self.assertRaisesRegex(ValueError,'word count'):
            review.description_checks(desc.replace('336-word','326-word'),review.methods_answers(self.report),336)


if __name__=='__main__':unittest.main()
