"""Regressions for scientific boundaries introduced by the protein-background and specificity integration."""
import unittest
from unittest.mock import patch
import track2_public_review_v28 as review


class V28PublicReviewTests(unittest.TestCase):
    def setUp(self):
        self.report=(review.ROOT/'notes/track2-report-v28.md').read_text()
        self.deck=(review.ROOT/'notes/track2-slides-v28.html').read_text()

    def test_integrated_materials_preserve_drug_decision(self):
        result=review.check()
        self.assertEqual((result['slides'],result['narration_words'],result['methods_fields']), (9,330,11))
        self.assertEqual(result['claim_records'],42)
        self.assertEqual(result['abstract_words'],271)
        self.assertEqual(result['crispr']['bub1b_guides'],1)
        self.assertFalse(result['crispr']['drug_ranking_changed'])
        self.assertFalse(result['upload_ready'])
        self.assertFalse(result['biological_validation'])

    def test_profile_count_cannot_replace_guide_independence(self):
        for term in ['1 guide','One HT29 batch fails QC','Independent guides needed','Tumour-line assay lead']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(term,'independently validated'))

    def test_favorable_ht29_result_and_sensitivity_remain(self):
        for term in ['0.3712','0.1510','Ranks 2–5','4 / 4 → 4 / 5']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(term,'omitted'))

    def test_drug_quality_cannot_repair_failed_query_quality(self):
        for term in ['Drug QC passes','BUB1B query QC fails','RNAi/CRISPR disagree','HT29 drug profile fails QC']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(term,'qualified rescue'))

    def test_favorable_drug_result_is_retained_with_identity_and_nominal_units(self):
        for term in ['7 → 1,184','1 → 1','−0.2144','−0.0297','0.2836','0.2250','reference-matching chemistry','0.1 µM nominal culture']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(term,'omitted'))

    def test_cross_context_and_source_well_reuse_cannot_disappear(self):
        for term in ['Different cells and separate perturbations','Joint functional rescue remains untested']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(term,'joint rescue demonstrated'))
        for term in ['regroup three older singleton wells','cannot be combined into one experiment','zero passing profiles']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.report_checks(self.report.replace(term,'omitted'))

    def test_old_rnai_findings_and_finite_reference_limits_remain(self):
        for term in ['45/54','0.01422','0.08532','0.21276','5/36','0/36','not independent biological replication','0/14','0/42','0.042']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.report_checks(self.report.replace(term,'omitted'))

    def test_execution_count_is_not_biological_validation(self):
        for term in ['2,474,445,074','285,488','1.231 seconds','8% GPU utilization','not independent biological review']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.report_checks(self.report.replace(term,'omitted'))

    def test_joint_function_and_editing_controls_required(self):
        for term in ['Drug + qualified deficit','Every enrolled cell','Function + daughter fate','editing-stress controls']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(term,'omitted'))

    def test_frozen_crispr_audit_cannot_be_rebound(self):
        with patch.object(review,'digest',return_value='0'*64),self.assertRaises(ValueError):
            review.crispr_checks()

    def test_disclosure_and_abstract_are_enforced(self):
        for term in ['Fireworks','ColabFold','unverified']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.report_checks(self.report.replace(term,'omitted'))
        inflated=self.report.replace('We propose a qualified everolimus experiment', ' '.join(['word']*501)+' We propose a qualified everolimus experiment')
        with self.assertRaises(ValueError):review.report_checks(inflated)

    def test_delivery_and_safety_cannot_be_promoted(self):
        for term in ['Failed safety','Preclinical review only','Clinical exposure margin unknown']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(term,'clinically validated'))
        for term in ['We acknowledge their trust','</body>']:
            replacement='Thanks' if term.startswith('We') else '<img src="https://example.com/x.png"></body>'
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.presentation_checks(self.deck.replace(term,replacement))

    def test_backgrounds_do_not_become_pathogenicity_calibration(self):
        for term in ['71.6%','89.8%','matched N→K','not p-values or pathogenicity probabilities','second-most','19,950']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.report_checks(self.report.replace(term,'omitted'))

    def test_projection_cannot_become_causal_adjustment(self):
        for term in ['not a symmetrically held-out','attenuation does not prove','residual cosine is not a causal estimate','not a robust rescue rationale']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.report_checks(self.report.replace(term,'omitted'))

    def test_frozen_v27_audit_cannot_be_rebound(self):
        with patch.object(review,'digest',return_value='0'*64),self.assertRaises(ValueError):
            review.v27_checks()

    def test_new_inference_and_toolkit_nonuse_are_disclosed(self):
        for term in ['local ESMC/ESM3 protein inference','not installed','FP32','1,004.196 seconds','not continuous eight-GPU saturation']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                review.report_checks(self.report.replace(term,'omitted'))


if __name__=='__main__':unittest.main()
