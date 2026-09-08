#!/usr/bin/env python3
"""Offline adversarial tests for supplementary public retrieval and exposure semantics."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

import track2_evidence as evidence
import track2_exposure as exposure
import track2_review_search as search


class ExposureTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(exposure.LEDGER.read_text())
        self.ids = {s["id"] for s in evidence.load_ledgers()[0]["sources"]}

    def reject(self):
        with self.assertRaises(ValueError):
            exposure.audit(self.data, self.ids)

    def test_real_public_quantities_do_not_establish_margin(self):
        result = exposure.audit(self.data, self.ids)
        self.assertEqual(len(result["records"]), 8)
        self.assertTrue(all(r["clinical_exposure_margin"] is None for r in result["records"] + result["comparisons"]))

    def test_everolimus_unit_conversion(self):
        self.assertAlmostEqual(exposure.convert(5, "ng/mL", 958.22, "concentration")[0], 5.218008, places=5)

    def test_parent_not_sulfate_mass(self):
        result = exposure.audit(self.data, self.ids)
        r = next(r for r in result["records"] if r["id"] == "hcq_rosenfeld_split")
        self.assertAlmostEqual(r["values"][0], 5314.081572, places=5)
        self.assertNotAlmostEqual(r["values"][0], 1785 * 1000 / 433.95)

    def test_auc_cannot_be_concentration(self):
        with self.assertRaises(ValueError):
            exposure.convert(307, "nM*h", 958.22, "concentration")

    def test_auc_unit_preserved(self):
        self.assertEqual(exposure.convert(307, "nM*h", 958.22, "auc"), (307, "nM*h"))

    def test_dose_cannot_be_exposure(self):
        with self.assertRaises(ValueError):
            exposure.convert(200, "mg", 335.9, "concentration")

    def test_nonfinite_negative_boolean_zero_rejected(self):
        for bad in (float("nan"), float("inf"), -1, 0, True, "5", None):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                exposure.convert(bad, "ng/mL", 958.22, "concentration")

    def test_overflow_rejected(self):
        with self.assertRaises(ValueError):
            exposure.convert(1e308, "mM", 958.22, "concentration")

    def test_invalid_weight_rejected(self):
        self.data["analytes"]["everolimus"]["molecular_weight"] = 0
        self.reject()

    def test_unknown_mass_provenance_rejected(self):
        self.data["analytes"]["everolimus"]["source"] = "fabricated"
        self.reject()

    def test_manufactured_margin_rejected(self):
        self.data["clinical_exposure_margin"] = 5
        self.reject()

    def test_missing_margin_rejected(self):
        del self.data["clinical_exposure_margin"]
        self.reject()

    def test_boolean_schema_rejected(self):
        self.data["schema_version"] = True
        self.reject()

    def test_duplicate_record_rejected(self):
        self.data["records"].append(copy.deepcopy(self.data["records"][0]))
        self.reject()

    def test_unknown_record_source_rejected(self):
        self.data["records"][0]["source"] = "made_up"
        self.reject()

    def test_missing_time_context_rejected(self):
        del self.data["records"][0]["time_context"]
        self.reject()

    def test_unknown_analyte_rejected(self):
        self.data["records"][0]["analyte"] = "salt_not_parent"
        self.reject()

    def test_range_order_rejected(self):
        self.data["records"][0]["values"] = [15, 5]
        self.reject()

    def test_bad_matrix_rejected(self):
        self.data["records"][0]["matrix"] = "imagined_tumour"
        self.reject()

    def test_whole_blood_not_plasma(self):
        a, b = self.data["records"][3:5]
        self.assertIn("different_matrix", exposure.comparison_barriers(a, b))

    def test_peak_not_trough(self):
        a, b = self.data["records"][:2]
        self.assertIn("different_time_context", exposure.comparison_barriers(a, b))

    def test_nominal_not_unbound(self):
        a = copy.deepcopy(self.data["records"][0])
        b = copy.deepcopy(a)
        a["basis"], b["basis"] = "nominal", "unbound"
        self.assertIn("different_basis", exposure.comparison_barriers(a, b))

    def test_same_units_not_validated_bridge(self):
        a = self.data["records"][0]
        self.assertIn("no_validated_genotype_matched_normal_tumour_bridge", exposure.comparison_barriers(a, a))

    def test_unresolved_matrix_remains_unresolved(self):
        a = self.data["records"][-1]
        self.assertIn("unresolved_measurement", exposure.comparison_barriers(a, a))

    def test_unknown_comparison_rejected(self):
        self.data["comparisons"] = [["invented", "evero_label_trough"]]
        self.reject()


class PublicRetrievalTests(unittest.TestCase):
    XML = b'<article><front><article-meta><article-id pub-id-type="pmcid">PMC123</article-id><title-group><article-title>Public synthetic test</article-title></title-group></article-meta></front><body><p>Test only</p></body></article>'

    def test_primary_xml_identity(self):
        result = search.metadata_xml(self.XML, "PMC123")
        self.assertTrue(result["body_present"])
        self.assertTrue(result["full_text_retrieval_is_not_full_text_review"])

    def test_wrong_article_rejected(self):
        with self.assertRaises(ValueError):
            search.metadata_xml(self.XML, "PMC456")

    def test_captcha_not_full_text(self):
        with self.assertRaises(ValueError):
            search.metadata_xml(b"<html><body>Checking your browser</body></html>", "PMC123")

    def test_missing_body_rejected(self):
        with self.assertRaises(ValueError):
            search.metadata_xml(self.XML.replace(b"<body><p>Test only</p></body>", b""), "PMC123")

    def run_search(self, bodies):
        parent = evidence.ROOT / "results/feat009"
        with tempfile.TemporaryDirectory(prefix="public-review-test-", dir=parent) as tmp:
            with patch.object(search, "QUERIES", {"first": "public", "second": "public"}), patch("urllib.request.urlopen", side_effect=bodies), patch("time.sleep"), contextlib.redirect_stdout(io.StringIO()):
                path = Path(tmp) / "new"
                result = search.run(path, "search")
                manifest = json.loads((path / "manifest.json").read_text())
        return result, manifest

    def test_real_zero_results_are_valid(self):
        raw = b'{"hitCount":0,"resultList":{"result":[]}}'
        result, _ = self.run_search([io.BytesIO(raw), io.BytesIO(raw)])
        self.assertTrue(result["retrieval_complete"])

    def test_http_success_invalid_shape_not_zero(self):
        raw = b'{"hitCount":0,"resultList":{"result":[]}}'
        result, manifest = self.run_search([io.BytesIO(b'{"version":"6"}'), io.BytesIO(raw)])
        self.assertEqual(result["failed_requests"], 1)
        self.assertFalse(result["retrieval_complete"])
        self.assertEqual(len(result["queries"]), 1)
        self.assertEqual(manifest[0]["status"], "error")

    def test_truncation_not_complete(self):
        raw = b'{"hitCount":1001,"resultList":{"result":[]}}'
        result, _ = self.run_search([io.BytesIO(raw), io.BytesIO(raw)])
        self.assertFalse(result["retrieval_complete"])
        self.assertTrue(all(q["truncated"] for q in result["queries"]))

    def test_http_error_retains_status(self):
        raw = b'{"hitCount":0,"resultList":{"result":[]}}'
        error = urllib.error.HTTPError("https://public.invalid/", 404, "not found", {}, None)
        result, manifest = self.run_search([error, io.BytesIO(raw)])
        self.assertEqual(result["failed_requests"], 1)
        self.assertEqual(manifest[0]["http_status"], 404)

    def test_deduplication_preserves_distinct_database_ids(self):
        raw = b'{"hitCount":1,"resultList":{"result":[{"id":"1","source":"MED","title":"Synthetic","doi":"10.1000/example"}]}}'
        result, _ = self.run_search([io.BytesIO(raw), io.BytesIO(raw)])
        self.assertEqual(result["unique_retrieved_records"], 1)

    def test_partial_cli_exits_nonzero(self):
        with patch("sys.argv", ["review", "search", "results/feat009/unused"]), patch.object(search, "run", return_value={"retrieval_complete": False}), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                search.main()
        self.assertEqual(error.exception.code, 1)

    def test_short_valid_chemical_json(self):
        source = {"expected_cid": 3652, "expected_molecular_weight": "335.9"}
        body = {"PropertyTable": {"Properties": [{"CID": 3652, "MolecularWeight": "335.9"}]}}
        self.assertFalse(evidence.check_chemical_metadata(source, body)["clinical_efficacy_inferred"])

    def test_wrong_chemical_identity_or_mass(self):
        source = {"expected_cid": 3652, "expected_molecular_weight": "335.9"}
        for row in ({"CID": 4091, "MolecularWeight": "335.9"}, {"CID": 3652, "MolecularWeight": "433.95"}, {"CID": True, "MolecularWeight": "335.9"}):
            with self.subTest(row=row), self.assertRaises(ValueError):
                evidence.check_chemical_metadata(source, {"PropertyTable": {"Properties": [row]}})

    def test_chemical_error_envelope_rejected(self):
        with self.assertRaises(ValueError):
            evidence.check_chemical_metadata({}, {"Fault": "Service unavailable"})


if __name__ == "__main__":
    unittest.main()
