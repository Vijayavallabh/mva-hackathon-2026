"""Adversarial offline tests. Public ledgers and synthetic fixtures; no subject reads."""
from __future__ import annotations

import copy
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import track2_evidence as evidence
import track2_public_search as search
from track2_public_search import parse_epmc, validate_body


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.sources, self.candidates = evidence.load_ledgers()

    def reject(self):
        with self.assertRaises((ValueError, KeyError, TypeError)):
            evidence.validate(self.sources, self.candidates)

    def test_reviewed_ledgers(self):
        result = evidence.validate(self.sources, self.candidates)
        self.assertEqual(result["candidates"], 12)
        self.assertEqual(result["decisions"]["conditional_screen"], 1)

    def test_duplicate_candidate(self):
        self.candidates["candidates"].append(copy.deepcopy(self.candidates["candidates"][0]))
        self.reject()

    def test_duplicate_source(self):
        self.sources["sources"].append(copy.deepcopy(self.sources["sources"][0]))
        self.reject()

    def test_doi_case_insensitive_duplicate(self):
        s = copy.deepcopy(self.sources["sources"][0])
        s["id"] = "duplicate_doi"
        s["doi"] = s["doi"].upper()
        self.sources["sources"].append(s)
        self.reject()

    def test_phase_cannot_be_promoted(self):
        self.candidates["phase"] = "trans"
        self.reject()

    def test_cannot_claim_treatment(self):
        self.candidates["clinical_use"] = "treatment"
        self.reject()

    def test_cannot_claim_pair_experiment(self):
        self.candidates["candidates"][0]["direct_pair_evidence"] = True
        self.reject()

    def test_cannot_claim_clinical_efficacy(self):
        self.candidates["candidates"][0]["clinical_efficacy"] = "established"
        self.reject()

    def test_invented_margin_rejected_including_nan(self):
        for value in [1.5, 0, -1, float("nan"), float("inf"), True]:
            with self.subTest(value=value):
                self.candidates["candidates"][0]["clinical_exposure_margin"] = value
                self.reject()

    def test_unknown_reference(self):
        self.candidates["candidates"][0]["support"] = ["imaginary"]
        self.reject()

    def test_no_counterevidence_rejected(self):
        self.candidates["candidates"][0]["counterevidence"] = []
        self.reject()

    def test_duplicate_reference_rejected(self):
        self.candidates["candidates"][0]["support"] *= 2
        self.reject()

    def test_regulatory_approval_not_inferred_from_paper(self):
        self.candidates["candidates"][0]["approval_source"] = "sieben2020"
        self.reject()

    def test_unverified_drug_cannot_enter_screen(self):
        self.candidates["candidates"][0]["approval"] = "not_verified"
        self.reject()

    def test_excluded_drug_cannot_be_silently_promoted(self):
        c = next(c for c in self.candidates["candidates"] if c["id"] == "ataluren")
        c["decision"] = "conditional_screen"
        self.reject()

    def test_missing_falsifier(self):
        self.candidates["candidates"][0]["falsifier"] = " "
        self.reject()

    def test_missing_safety(self):
        del self.candidates["candidates"][0]["normal_tissue_risk"]
        self.reject()

    def test_missing_unknown_margin_is_not_explicit_null(self):
        del self.candidates["candidates"][0]["clinical_exposure_margin"]
        self.reject()

    def test_unknown_evidence_class_rejected(self):
        self.candidates["candidates"][0]["evidence_level"] = "other_allele_animals"
        self.reject()

    def test_unknown_approval_state_rejected(self):
        self.candidates["candidates"][0]["approval"] = "approved_probably"
        self.reject()

    def test_empty_ledgers_rejected(self):
        self.candidates["candidates"] = []
        self.reject()

    def test_source_path_traversal_rejected(self):
        self.sources["sources"][0]["id"] = "../../outside"
        self.reject()

    def test_sensitivity_is_deterministic(self):
        a = evidence.sensitivities(self.sources, self.candidates)
        self.assertEqual(a, evidence.sensitivities(self.sources, self.candidates))
        self.assertEqual(a["require_direct_pair_intervention_evidence"], [])
        self.assertEqual(a["require_measured_clinical_exposure_margin"], [])
        self.assertEqual(a["baseline_conditional_screens"], ["everolimus"])
        self.assertEqual(a["remove_other_allele_animal_support"], [])
        self.assertEqual(a["remove_other_compound_or_cancer_support"], ["everolimus"])

    def test_offline_checks_do_not_open_network(self):
        with patch("urllib.request.urlopen", side_effect=AssertionError("network")):
            evidence.validate(self.sources, self.candidates)
            evidence.sensitivities(self.sources, self.candidates)

    def test_table_keeps_rejections(self):
        table = evidence.candidate_table(self.sources, self.candidates)
        self.assertIn("Ataluren", table)
        self.assertIn("exclude", table)
        self.assertIn("trans phase remains unconfirmed", table)


class RetrievalTests(unittest.TestCase):
    def test_http_success_without_results_not_zero_hits(self):
        with self.assertRaises(ValueError):
            parse_epmc(b'{"version":"6.9"}')

    def test_true_zero_hits(self):
        self.assertEqual(parse_epmc(b'{"hitCount":0,"resultList":{"result":[]}}'), (0, []))

    def test_null_or_boolean_hits_fail(self):
        for hits in [None, True, "5", -1]:
            with self.subTest(hits=hits), self.assertRaises(ValueError):
                parse_epmc(json.dumps({"hitCount": hits, "resultList": {"result": []}}).encode())

    def test_non_public_urls_fail(self):
        for url in ["file:///etc/passwd", "http://www.nature.com/x", "https://127.0.0.1/x", "https://www.nature.com.attacker.test/x", "https://token@www.nature.com/x", "https://www.nature.com:444/x", "https://www.nature.com/x#fragment"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                evidence.checked_url(url)

    def test_known_url_succeeds(self):
        self.assertEqual(evidence.checked_url("https://www.nature.com/articles/ng1449"), "https://www.nature.com/articles/ng1449")

    def test_parenthesized_doi_is_not_truncated(self):
        source = {"doi": "10.1016/S1470-2045(24)00255-9", "title": "A trial"}
        result = evidence.check_metadata(source, {"message": {"DOI": source["doi"].lower(), "title": ["A trial"]}})
        self.assertTrue(result["title_matches"])
        self.assertFalse(result["claim_support_verified_by_metadata"])

    def test_wrong_doi_fails(self):
        with self.assertRaises(ValueError):
            evidence.check_metadata({"doi": "10.1000/a", "title": "A"}, {"message": {"DOI": "10.1000/b", "title": ["A"]}})

    def test_wrong_title_requires_review(self):
        result = evidence.check_metadata({"doi": "10.1000/a", "title": "A"}, {"message": {"DOI": "10.1000/a", "title": ["Wrong paper"]}})
        self.assertFalse(result["title_matches"])

    def test_title_subtitle_join(self):
        result = evidence.check_metadata({"doi": "10.1000/a", "title": "Main: a study"}, {"message": {"DOI": "10.1000/a", "title": ["Main"], "subtitle": ["a study"]}})
        self.assertTrue(result["title_matches"])

    def test_no_metadata_title_fails(self):
        with self.assertRaises(ValueError):
            evidence.check_metadata({"doi": "10.1000/a", "title": "A"}, {"message": {"DOI": "10.1000/a"}})

    def test_malformed_epmc_shapes_rejected(self):
        for obj in [None, [], {"hitCount": 0, "resultList": None}, {"hitCount": 1, "resultList": {"result": [None]}}, {"hitCount": 0, "resultList": {"result": [{}]}}, {"hitCount": 1, "resultList": {"result": [{}]}}]:
            with self.subTest(obj=obj), self.assertRaises(ValueError):
                parse_epmc(json.dumps(obj).encode())

    def test_epmc_good_record(self):
        obj = {"hitCount": 1, "resultList": {"result": [{"id": "1", "source": "MED", "title": "Public fixture"}]}}
        self.assertEqual(parse_epmc(json.dumps(obj).encode())[0], 1)

    def test_empty_or_service_error_is_failure_for_each_endpoint(self):
        for key in ["epmc-rescue", "pubmed-rescue", "clinicaltrials-mva", "NCT01222715", "space-info"]:
            for data in [b"", b" ", b'null', b'[]', b'{"error":"temporary failure"}']:
                with self.subTest(key=key, data=data), self.assertRaises(ValueError):
                    validate_body(key, data)

    def test_secondary_response_schemas(self):
        valid = {
            "pubmed-rescue": {"esearchresult": {"count": "1", "idlist": ["123"]}},
            "clinicaltrials-mva": {"studies": []},
            "NCT01222715": {"protocolSection": {"identificationModule": {"nctId": "NCT01222715"}}},
            "space-info": {"sha": "a" * 40},
        }
        for key, obj in valid.items():
            validate_body(key, json.dumps(obj).encode())
        for key, obj in [
            ("pubmed-rescue", {"esearchresult": {"count": None, "idlist": []}}),
            ("pubmed-rescue", {"esearchresult": {"count": "0", "idlist": [], "errorlist": {}}}),
            ("clinicaltrials-mva", {"studies": [None]}),
            ("NCT01222715", {"protocolSection": None}),
            ("space-info", {"sha": None}),
            ("space-info", {"sha": "../../outside"}),
        ]:
            with self.subTest(key=key, obj=obj), self.assertRaises(ValueError):
                validate_body(key, json.dumps(obj).encode())

    def test_code_response_must_be_python(self):
        validate_body("space-config.py", b"MAX_SUBMISSIONS = 3\n")
        with self.assertRaises(SyntaxError):
            validate_body("space-config.py", b"<html>Error</html>")

    def test_invalid_crossref_shapes_fail_cleanly(self):
        source = {"doi": "10.1000/a", "title": "A"}
        for obj in [None, [], {"message": None}, {"message": {"DOI": None}}, {"message": {"DOI": "10.1000/a", "title": [None]}}, {"message": {"DOI": "10.1000/a", "title": ["A"], "subtitle": None}}, {"message": {"DOI": "10.1000/a", "title": ["A"], "author": [None]}}]:
            with self.subTest(obj=obj), self.assertRaises(ValueError):
                evidence.check_metadata(source, obj)

    def test_complete_run_counts_empty_responses_as_failures(self):
        parent = search.ROOT / "results/feat009"
        parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="track2-search-test-", dir=parent) as tmp:
            with patch.object(search, "get_bytes", return_value=b""), patch.object(search.time, "sleep"):
                result = search.run(Path(tmp) / "empty-responses")
        self.assertEqual(result["failed_requests"], 10)
        self.assertEqual(result["queries"], [])
        self.assertFalse(result["complete"])

    def test_partial_search_cli_is_nonzero(self):
        with patch("sys.argv", ["search", "results/feat009/synthetic-unused"]), patch.object(search, "run", return_value={"queries": [], "failed_requests": 1, "complete": False}), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                search.main()
        self.assertEqual(error.exception.code, 1)

    def test_source_review_cli_is_nonzero(self):
        with patch("sys.argv", ["evidence", "sources", "results/feat009/synthetic-unused"]), patch.object(evidence, "fetch_sources", return_value={"needs_review": ["synthetic"]}), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                evidence.main()
        self.assertEqual(error.exception.code, 1)


class PackageTests(unittest.TestCase):
    def setUp(self):
        parent = evidence.ROOT / "results/feat009"
        parent.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="track2-test-", dir=parent)
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "package"
        # Unit tests do not require or inspect submitted subject-derived artifacts.
        self.track1 = patch.object(evidence, "check_track1", return_value={"synthetic_test": True})
        self.track1.start()
        self.addCleanup(self.track1.stop)
        evidence.build(self.path)

    def manifest(self):
        return json.loads((self.path / "manifest.json").read_text())

    def save_manifest(self, obj):
        (self.path / "manifest.json").write_text(json.dumps(obj))

    def reject(self):
        with self.assertRaises((ValueError, FileNotFoundError)):
            evidence.verify(self.path)

    def test_valid_research_package_not_upload_ready(self):
        result = evidence.verify(self.path)
        self.assertTrue(result["integrity_verified"])
        self.assertFalse(result["upload_ready"])

    def test_cannot_overwrite_package(self):
        with self.assertRaises(FileExistsError):
            evidence.build(self.path)

    def test_changed_report_rejected(self):
        (self.path / "jvv7_track2_report_v2.md").write_text("tampered")
        self.reject()

    def test_extra_file_rejected(self):
        (self.path / "unexpected.txt").write_text("synthetic")
        self.reject()

    def test_missing_file_rejected(self):
        (self.path / "validation-plan.md").unlink()
        self.reject()

    def test_manifest_path_traversal_rejected(self):
        manifest = self.manifest()
        manifest["files"]["../../outside"] = "00"
        self.save_manifest(manifest)
        self.reject()

    def test_input_path_traversal_rejected(self):
        manifest = self.manifest()
        manifest["input_hashes"]["../../outside"] = "00"
        self.save_manifest(manifest)
        self.reject()

    def test_stale_input_hash_rejected(self):
        manifest = self.manifest()
        manifest["input_hashes"]["notes/track2-report.md"] = "00"
        self.save_manifest(manifest)
        self.reject()

    def test_forged_upload_stage_rejected(self):
        manifest = self.manifest()
        manifest["upload_performed"] = True
        self.save_manifest(manifest)
        self.reject()

    def test_forged_video_rejected(self):
        manifest = self.manifest()
        manifest["video_url"] = "https://video.invalid/not-real"
        self.save_manifest(manifest)
        self.reject()

    def test_table_tamper_even_with_updated_file_hash(self):
        target = self.path / "candidate-evidence.md"
        target.write_text("Guaranteed treatment")
        manifest = self.manifest()
        manifest["files"][target.name] = evidence.sha256(target)
        self.save_manifest(manifest)
        self.reject()

    def test_sensitivity_tamper_even_with_updated_file_hash(self):
        target = self.path / "sensitivity.json"
        target.write_text("{}")
        manifest = self.manifest()
        manifest["files"][target.name] = evidence.sha256(target)
        self.save_manifest(manifest)
        self.reject()

    def test_exposure_audit_tamper_even_with_updated_file_hash(self):
        target = self.path / "exposure-audit.json"
        target.write_text('{"clinical_exposure_margin": 100}')
        manifest = self.manifest()
        manifest["files"][target.name] = evidence.sha256(target)
        self.save_manifest(manifest)
        self.reject()

    def test_exposure_ledger_cannot_invent_margin(self):
        target = self.path / "exposure.json"
        data = json.loads(target.read_text())
        data["clinical_exposure_margin"] = 100
        target.write_text(json.dumps(data))
        manifest = self.manifest()
        manifest["files"][target.name] = evidence.sha256(target)
        self.save_manifest(manifest)
        self.reject()

    def test_final_review_copy_is_bound(self):
        target = self.path / "scientific-exposure-review.md"
        target.write_text("unreviewed replacement")
        manifest = self.manifest()
        manifest["files"][target.name] = evidence.sha256(target)
        self.save_manifest(manifest)
        self.reject()

    def test_copy_mismatch_even_with_updated_file_hash(self):
        target = self.path / "jvv7_track2_report_v2.md"
        target.write_text("changed public report")
        manifest = self.manifest()
        manifest["files"][target.name] = evidence.sha256(target)
        self.save_manifest(manifest)
        self.reject()

    def test_symlink_rejected(self):
        target = self.path / "candidate-evidence.md"
        replacement = Path(self.tmp.name) / "synthetic-table.md"
        target.rename(replacement)
        target.symlink_to(replacement)
        self.reject()

    def test_outside_output_rejected(self):
        with tempfile.TemporaryDirectory(prefix="track2-outside-test-") as tmp:
            with self.assertRaises(ValueError):
                evidence.new_output(Path(tmp) / "not-in-results")

    def test_missing_input_does_not_create_partial_package(self):
        target = Path(self.tmp.name) / "new-package"
        with patch.object(evidence, "ROOT", Path(self.tmp.name)), self.assertRaises(ValueError):
            evidence.build(target)
        self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
