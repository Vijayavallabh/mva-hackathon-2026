#!/usr/bin/env python3
"""Synthetic transport tests; no real network or protected data."""
import io
import http.client
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock
import urllib.error
import urllib.request

import alphagenome_access_audit as audit


class Response(io.BytesIO):
    def __init__(self, body, status=200, headers=None, url=None):
        super().__init__(body)
        self.status = status
        self.headers = headers or {}
        self.url = url

    def geturl(self):
        return self.url


class Tests(unittest.TestCase):
    def prefix(self, body=None, status=206, header="bytes 0-4095/88500000000"):
        return audit.assess("avi_archive", status, {"Content-Range": header},
                            body if body is not None else b"PK\x03\x04" + b"x" * 4092)

    def test_fixed_unknown_source(self):
        with self.assertRaises(ValueError):
            audit.probe("https://example.com/subject", mock.Mock())

    def test_document_empty(self):
        self.assertEqual(audit.assess("sdk_readme", 200, {}, b"")["state"], "unavailable")

    def test_document_error_page(self):
        self.assertEqual(audit.assess("sdk_readme", 200, {}, b"Error")["state"], "unavailable")

    def test_document_partial(self):
        self.assertEqual(audit.assess("sdk_readme", 206, {}, b"AlphaGenome Atlas Terms")["state"], "unavailable")

    def test_document_oversized(self):
        self.assertEqual(audit.assess("sdk_readme", 200, {}, b"AlphaGenome Atlas Terms" + b"x" * audit.DOC_LIMIT)["state"], "unavailable")

    def test_document_valid(self):
        self.assertEqual(audit.assess("sdk_readme", 200, {}, b"AlphaGenome Atlas Terms")["state"], "documentation_retrieved")

    def test_document_declared_truncation(self):
        self.assertEqual(audit.assess("sdk_readme", 200, {"Content-Length": "99999"}, b"AlphaGenome Atlas Terms")["reason"], "declared_length_mismatch")

    def test_document_malformed_length(self):
        self.assertEqual(audit.assess("sdk_readme", 200, {"Content-Length": "many"}, b"AlphaGenome Atlas Terms")["state"], "unavailable")

    def test_document_correct_length(self):
        body = b"AlphaGenome Atlas Terms"
        self.assertEqual(audit.assess("sdk_readme", 200, {"Content-Length": str(len(body))}, body)["state"], "documentation_retrieved")

    def test_catalog_not_prediction(self):
        self.assertEqual(audit.assess("portal", 200, {}, b"AlphaGenome avi_scores_snvs_tabix.zip")["state"], "catalog_metadata_retrieved")

    def test_terms_shell_never_terms_approval(self):
        self.assertEqual(audit.assess("terms", 200, {}, b"AlphaGenome")["state"], "page_retrieved_terms_unverified")

    def test_good_prefix_not_whole_download(self):
        self.assertEqual(self.prefix()["state"], "prefix_available_only")

    def test_range_ignored(self):
        self.assertEqual(self.prefix(status=200)["state"], "unavailable")

    def test_range_wrong_start(self):
        self.assertEqual(self.prefix(header="bytes 1-4096/88500000000")["state"], "unavailable")

    def test_range_unknown_total(self):
        self.assertEqual(self.prefix(header="bytes 0-4095/*")["state"], "unavailable")

    def test_range_total_invalid(self):
        self.assertEqual(self.prefix(header="bytes 0-4095/100")["state"], "unavailable")

    def test_range_short_body(self):
        self.assertEqual(self.prefix(body=b"PK\x03\x04")["state"], "unavailable")

    def test_range_fake_html(self):
        self.assertEqual(self.prefix(body=b"<html>" + b"x" * 4090)["state"], "unavailable")

    def test_http_errors_unknown_not_zero(self):
        for code in (401, 403, 404, 429, 500, 503):
            opener = mock.Mock()
            opener.open.side_effect = urllib.error.HTTPError(audit.SOURCES["avi_archive"][0], code, "error", {}, io.BytesIO(b"error"))
            record, _ = audit.probe("avi_archive", opener)
            self.assertEqual(record["state"], "unavailable")
            self.assertEqual(record["http_status"], code)

    def test_timeout(self):
        opener = mock.Mock()
        opener.open.side_effect = TimeoutError()
        self.assertEqual(audit.probe("atlas_client", opener)[0]["state"], "unavailable")

    def test_http_error_body_timeout(self):
        opener = mock.Mock()
        error_body = mock.Mock()
        error_body.read.side_effect = TimeoutError()
        opener.open.side_effect = urllib.error.HTTPError(audit.SOURCES["avi_archive"][0], 503, "", {}, error_body)
        record, _ = audit.probe("avi_archive", opener)
        self.assertEqual(record["state"], "unavailable")
        self.assertEqual(record["http_status"], 503)
        self.assertEqual(record["reason"], "http_error_body_TimeoutError")

    def test_incomplete_normal_body(self):
        opener = mock.Mock()
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.geturl.return_value = audit.SOURCES["sdk_readme"][0]
        response.status = 200
        response.read.side_effect = http.client.IncompleteRead(b"partial", 9000)
        opener.open.return_value = response
        record, _ = audit.probe("sdk_readme", opener)
        self.assertEqual(record["state"], "unavailable")
        self.assertEqual(record["reason"], "IncompleteRead")

    def test_redirect_blocked(self):
        request = urllib.request.Request(audit.SOURCES["portal"][0])
        with self.assertRaises(urllib.error.URLError):
            audit.FixedRedirects().redirect_request(request, None, 302, "", {}, "https://accounts.google.com/")

    def test_request_has_no_auth_and_body(self):
        opener = mock.Mock()
        url = audit.SOURCES["avi_archive"][0]
        opener.open.return_value = Response(b"PK\x03\x04" + b"x" * 4092, 206, {"Content-Range": "bytes 0-4095/9000"}, url)
        record, _ = audit.probe("avi_archive", opener)
        request = opener.open.call_args.args[0]
        self.assertIsNone(request.data)
        self.assertEqual(request.method, "GET")
        self.assertFalse(any("key" in k.lower() or "auth" in k.lower() for k in request.headers))
        self.assertEqual(record["state"], "prefix_available_only")

    def test_ignored_range_read_bounded(self):
        opener = mock.Mock()
        opener.open.return_value = Response(b"x" * 20000, url=audit.SOURCES["avi_archive"][0])
        record, body = audit.probe("avi_archive", opener)
        self.assertEqual(len(body), audit.PREFIX_SIZE + 1)
        self.assertEqual(record["state"], "unavailable")

    def test_final_url_mismatch(self):
        opener = mock.Mock()
        opener.open.return_value = Response(b"AlphaGenome", url="https://accounts.google.com/")
        self.assertEqual(audit.probe("portal", opener)[0]["state"], "unavailable")

    def test_summary_requires_exact_set(self):
        with self.assertRaises(ValueError):
            audit.summarize([])

    def test_summary_never_manufactures_scores(self):
        records = [{"id": k, "state": "prefix_available_only" if v[1] == "archive" else "documentation_retrieved"} for k, v in audit.SOURCES.items()]
        summary = audit.summarize(records)
        self.assertFalse(summary["atlas_scores_obtained"])
        self.assertIsNone(summary["clinical_exposure_margin"])
        self.assertEqual(summary["phase"], "unconfirmed")

    def test_output_scope(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                audit.run(Path(directory) / "outside")

    def test_existing_snapshot_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.object(audit, "ROOT", Path(directory)):
                output = Path(directory) / "results/feat009/existing"
                output.mkdir(parents=True)
                with self.assertRaises(FileExistsError):
                    audit.run(output, mock.Mock())

    def test_interrupted_run_preserves_completed_observations(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "results/feat009/new"
            record = {"id": "portal", "state": "catalog_metadata_retrieved"}
            with mock.patch.object(audit, "ROOT", Path(directory)), mock.patch.object(audit, "probe", side_effect=[(record, b"public"), KeyboardInterrupt()]):
                with self.assertRaises(KeyboardInterrupt):
                    audit.run(output, mock.Mock())
            manifest = json.loads((output / "access-audit.json").read_text())
            self.assertEqual(manifest["requests"], [record])
            self.assertEqual(manifest["summary"], {"state": "in_progress", "completed_sources": 1})

    def test_failed_run_retains_other_successes(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "results/feat009/new"
            observations = [({"id": k, "state": "unavailable" if k == "avi_archive" else "documentation_retrieved"}, b"public") for k in audit.SOURCES]
            with mock.patch.object(audit, "ROOT", Path(directory)), mock.patch.object(audit, "probe", side_effect=observations):
                summary = audit.run(output, mock.Mock())
            self.assertEqual(summary["unavailable_sources"], ["avi_archive"])
            self.assertEqual(len(json.loads((output / "access-audit.json").read_text())["requests"]), 7)

    def test_cli_rejects_variant_argument(self):
        p = subprocess.run(["uv", "run", "python", str(Path(audit.__file__)), "--variant", "not-an-input"], capture_output=True)
        self.assertNotEqual(p.returncode, 0)


if __name__ == "__main__":
    unittest.main()
