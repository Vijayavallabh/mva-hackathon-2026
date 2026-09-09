#!/usr/bin/env python3
"""Offline synthetic GLM-runner tests: no service, credentials, or subject data."""
from __future__ import annotations

import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from urllib.parse import parse_qs, urlsplit

import track2_glm_review as glm


PUBLIC = "https://pmc.ncbi.nlm.nih.gov/articles/PMC1234567/"


def ok(data, **extra):
    return {"status": "ok", "data": data, **extra}


def completed(summary="Synthetic unverified public-source review.", model=glm.MODEL, **extra):
    return ok({"status": "completed", "model": model, "data": {"summary": summary}}, **extra)


def item(ident="fixture", challenge="Challenge the synthetic claim against the public source."):
    return {"id": ident, "urls": [PUBLIC], "query": "public synthetic literature",
            "question": "Which result is measured rather than hypothesized?", "challenge": challenge}


class FakeClient:
    def __init__(self, out, starts=None, statuses=None):
        self.out = out
        self.calls = []
        self.sequence = 0
        self.starts = list(starts) if starts is not None else None
        self.statuses = list(statuses) if statuses is not None else None
        self.jobs_started = 0
        self.closed = False

    def initialize(self):
        self.sequence += 2
        return {name: {} for name in ("firecrawl_search", "firecrawl_agent", "firecrawl_agent_status")}

    def call(self, label, name, arguments, **kwargs):
        self.sequence += 1
        if self.sequence > 120:
            raise ValueError("synthetic MCP budget exhausted")
        self.calls.append({"label": label, "tool": name, "arguments": copy.deepcopy(arguments)})
        if name == "firecrawl_search":
            return ok({"data": {"web": [{"url": PUBLIC}]}})
        if name == "firecrawl_agent":
            self.jobs_started += 1
            return self.starts.pop(0) if self.starts is not None else ok({"id": "synthetic-job-" + str(self.jobs_started)})
        if name == "firecrawl_agent_status":
            result = self.statuses.pop(0) if self.statuses is not None else completed()
            if isinstance(result, BaseException):
                raise result
            return result
        raise AssertionError("Unexpected tool: " + name)

    def close(self):
        self.closed = True


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="glm-runner-offline-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.out = self.root / "out"
        self.out.mkdir()
        self.sleep = patch.object(glm.time, "sleep").start()
        self.addCleanup(patch.stopall)

    def round(self, client, **kwargs):
        return glm.agent_round(client, "review", [PUBLIC], "Synthetic public review prompt", **kwargs)

    def run_dossier(self, dossier=None, starts=None, statuses=None):
        dossier = dossier or item()
        client = FakeClient(self.out / dossier["id"], starts=starts, statuses=statuses)
        with patch.object(glm, "ReviewMCP", return_value=client):
            result = glm.run_dossier(dossier, self.out, self.root / "synthetic-index.js")
        return client, result


class PlanTests(unittest.TestCase):
    def test_actual_public_plan_has_ten_reviews_and_seven_challenges(self):
        plan = json.loads(glm.PLAN.read_text())
        dossiers = glm.validate_plan(plan)
        self.assertEqual(len(dossiers), 10)
        self.assertEqual(sum(bool(d.get("challenge")) for d in dossiers), 7)
        self.assertEqual(sum(1 + bool(d.get("challenge")) for d in dossiers), 17)
        self.assertTrue(next(d for d in dossiers if d["id"] == "mtor")["challenge"])
        self.assertTrue(all(len(d["urls"]) <= 10 for d in dossiers))

    def test_valid_small_plan(self):
        plan = {"version": 1, "dossiers": [item()]}
        self.assertEqual(glm.validate_plan(plan), plan["dossiers"])

    def test_plan_count_and_version_bounds(self):
        for plan in ({"version": 2, "dossiers": [item()]}, {"version": 1, "dossiers": []},
                     {"version": 1, "dossiers": [item(str(i)) for i in range(11)]}):
            with self.subTest(plan=plan), self.assertRaises(ValueError):
                glm.validate_plan(plan)

    def test_id_safety_and_uniqueness(self):
        for ident in ("../outside", "Upper", "has_space", "", "é", "/absolute", 7):
            with self.subTest(ident=ident), self.assertRaises(ValueError):
                glm.validate_plan({"version": 1, "dossiers": [item(ident)]})
        with self.assertRaises(ValueError):
            glm.validate_plan({"version": 1, "dossiers": [item(), item()]})

    def test_source_count_and_duplicates(self):
        for urls in ([], [PUBLIC] * 2, [PUBLIC + str(i) for i in range(11)], (PUBLIC,)):
            dossier = item()
            dossier["urls"] = urls
            with self.subTest(urls=urls), self.assertRaises(ValueError):
                glm.validate_plan({"version": 1, "dossiers": [dossier]})

    def test_refuses_nonpublic_url_routes(self):
        for url in ("http://pmc.ncbi.nlm.nih.gov/", "file:///synthetic", "https://127.0.0.1/",
                    "https://example.org/", "https://user:pass@pmc.ncbi.nlm.nih.gov/",
                    "https://pmc.ncbi.nlm.nih.gov:443/", "https://pmc.ncbi.nlm.nih.gov:8443/"):
            dossier = item()
            dossier["urls"] = [url]
            with self.subTest(url=url), self.assertRaises(ValueError):
                glm.validate_plan({"version": 1, "dossiers": [dossier]})

    def test_prompts_are_bounded_and_optional_challenge_is_valid(self):
        for field in ("question", "query", "challenge"):
            for value in ("", "x" * 4001, 17):
                dossier = item()
                dossier[field] = value
                with self.subTest(field=field, value=str(value)[:20]), self.assertRaises(ValueError):
                    glm.validate_plan({"version": 1, "dossiers": [dossier]})
        self.assertEqual(len(glm.validate_plan({"version": 1, "dossiers": [item(challenge=None)]})), 1)

    def test_optional_reviewer_context_is_bounded(self):
        for value in (17, [], "x" * 1801):
            dossier = item()
            dossier["reviewer_checks"] = value
            with self.subTest(value=str(value)[:20]), self.assertRaises(ValueError):
                glm.validate_plan({"version": 1, "dossiers": [dossier]})

    def test_prefix_preserves_unverified_research_boundaries(self):
        for phrase in ("untrusted evidence", "not independently verified", "No patient data",
                       "not independent", "Do not equate cytostasis", "unbound human tissue exposure"):
            self.assertIn(phrase.lower(), glm.PREFIX.lower())

    def test_abstract_mapping_preserves_exact_paper_identifiers(self):
        mapping = {
            PUBLIC: "PMCID:PMC1234567",
            "https://pubmed.ncbi.nlm.nih.gov/1234567/": "EXT_ID:1234567 AND SRC:MED",
            "https://www.jci.org/articles/view/126863": 'DOI:"10.1172/JCI126863"',
            "https://www.embopress.org/doi/full/10.15252/embj.201386907": 'DOI:"10.15252/embj.201386907"',
            "https://www.nature.com/articles/s41598-024-66545-5": 'DOI:"10.1038/s41598-024-66545-5"',
            "https://pubmed.ncbi.nlm.nih.gov/?term=10.1016%2FS1470-2045%2824%2900255-9": 'DOI:"10.1016/S1470-2045(24)00255-9"',
        }
        for source, query in mapping.items():
            with self.subTest(source=source):
                parsed = urlsplit(glm.abstract_record(source))
                self.assertEqual(parsed.scheme, "https")
                self.assertEqual(parsed.hostname, "www.ebi.ac.uk")
                self.assertEqual(parsed.path, "/europepmc/webservices/rest/search")
                self.assertEqual(parse_qs(parsed.query), {"query": [query], "format": ["json"],
                                                         "resultType": ["core"], "pageSize": ["1"]})

    def test_parenthesized_doi_is_quoted_as_one_search_value(self):
        source = "https://pubmed.ncbi.nlm.nih.gov/?term=10.1016%2FS1470-2045%2824%2900255-9"
        mapped = glm.abstract_record(source)
        self.assertEqual(parse_qs(urlsplit(mapped).query)["query"], ['DOI:"10.1016/S1470-2045(24)00255-9"'])
        self.assertIn("DOI%3A%2210.1016%2FS1470-2045%2824%2900255-9%22", mapped)

    def test_official_label_and_notice_urls_are_unchanged(self):
        for source in ("https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=synthetic",
                       "https://english.nmpa.gov.cn/2024-04/30/c_1049690.htm"):
            with self.subTest(source=source):
                self.assertEqual(glm.abstract_record(source), source)

    def test_actual_plan_mapping_stays_on_allowed_public_hosts(self):
        for dossier in glm.validate_plan(json.loads(glm.PLAN.read_text())):
            for source in dossier["urls"]:
                mapped = urlsplit(glm.abstract_record(source))
                self.assertEqual(mapped.scheme, "https")
                self.assertIn(mapped.hostname, glm.ALLOWED_HOSTS)


class RoundTests(Fixture):
    def test_invalid_prompt_lengths_are_rejected_without_any_call(self):
        for prompt in ("", "x" * 10001):
            with self.subTest(length=len(prompt)):
                client = FakeClient(self.out)
                job = glm.agent_round(client, "review", [PUBLIC], prompt)
                self.assertEqual(job["state"], "rejected_locally")
                self.assertEqual(client.calls, [])
                self.assertFalse(job["server_cancellation_attempted"])
                self.assertFalse(job["verified_claims"])
                self.assertIn("ended_utc", job)

    def test_exact_10000_character_prompt_is_allowed(self):
        client = FakeClient(self.out)
        job = glm.agent_round(client, "review", [PUBLIC], "x" * 10000)
        self.assertEqual(job["state"], "completed")
        self.assertEqual(client.jobs_started, 1)

    def test_recovery_polls_identified_job_without_duplicate_start(self):
        client = FakeClient(self.out)
        ident = "00000000-0000-4000-8000-000000000001"
        job = glm.agent_round(client, "review", [PUBLIC], "", existing_job_id=ident)
        self.assertEqual(job["state"], "completed")
        self.assertTrue(job["adopted_existing_job"])
        self.assertEqual(client.jobs_started, 0)
        self.assertEqual(client.calls[0]["arguments"], {"id": ident})

    def test_recovery_rejects_invalid_id_before_polling(self):
        client = FakeClient(self.out)
        with self.assertRaises(ValueError):
            glm.agent_round(client, "review", [PUBLIC], "synthetic", existing_job_id="not-a-uuid")
        self.assertEqual(client.calls, [])

    def test_success_retains_exact_proposal_and_hash_without_verifying_claims(self):
        client = FakeClient(self.out)
        job = self.round(client)
        path = self.out / "review-proposal.md"
        self.assertEqual(job["state"], "completed")
        self.assertEqual(job["model"], glm.MODEL)
        self.assertFalse(job["verified_claims"])
        self.assertEqual(job["proposal_sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertEqual(job["proposal_characters"], len(path.read_text()) - 1)
        self.assertEqual(json.loads((self.out / "review-job.json").read_text()), job)

    def test_start_request_contains_only_supplied_public_urls_and_prompt(self):
        client = FakeClient(self.out)
        self.round(client)
        self.assertEqual(client.calls[0]["tool"], "firecrawl_agent")
        self.assertEqual(client.calls[0]["arguments"], {"urls": [PUBLIC], "prompt": "Synthetic public review prompt"})
        self.assertEqual(client.calls[1]["arguments"], {"id": "synthetic-job-1"})

    def test_missing_or_invalid_start_id_cannot_complete(self):
        for data in ({}, {"id": None}, {"id": ""}, {"id": 17}):
            with self.subTest(data=data):
                client = FakeClient(self.out, starts=[ok(data)])
                job = self.round(client)
                self.assertNotEqual(job["state"], "completed")
                self.assertEqual(len(client.calls), 1)
                self.assertFalse((self.out / "review-proposal.md").exists())

    def test_start_timeout_does_not_assert_server_work_never_started(self):
        client = FakeClient(self.out, starts=[{"status": "TimeoutError", "data": None}])
        job = self.round(client)
        self.assertNotIn(job["state"], ("completed", "not_started", "cancelled"))
        self.assertIs(job.get("server_cancellation_attempted"), False)
        self.assertIn("ended_utc", job)
        self.assertEqual(len(client.calls), 1)

    def test_completed_model_identity_must_match(self):
        client = FakeClient(self.out, statuses=[completed(model="different-model")])
        job = self.round(client)
        self.assertEqual(job["state"], "invalid_completion")
        self.assertFalse((self.out / "review-proposal.md").exists())

    def test_invalid_completion_summaries(self):
        for summary in (None, [], "", " \n ", "x" * 100001):
            with self.subTest(summary=str(summary)[:20]):
                client = FakeClient(self.out, statuses=[completed(summary=summary)])
                job = self.round(client)
                self.assertEqual(job["state"], "invalid_completion")
                self.assertFalse((self.out / "review-proposal.md").exists())

    def test_malformed_completion_body(self):
        for body in (None, [], "wrong-shape"):
            client = FakeClient(self.out, statuses=[ok({"status": "completed", "model": glm.MODEL, "data": body})])
            with self.subTest(body=body):
                self.assertEqual(self.round(client)["state"], "invalid_completion")

    def test_flagged_truncation_cannot_be_accepted_as_complete(self):
        client = FakeClient(self.out, statuses=[completed(possible_truncation=True)])
        job = self.round(client)
        self.assertNotEqual(job["state"], "completed")
        self.assertFalse((self.out / "review-proposal.md").exists())

    def test_reported_failure_and_cancellation_are_terminal(self):
        for state in ("failed", "cancelled"):
            with self.subTest(state=state):
                client = FakeClient(self.out, statuses=[ok({"status": state, "model": glm.MODEL})])
                job = self.round(client)
                self.assertEqual(job["state"], state)
                self.assertEqual(len(client.calls), 2)
                self.assertFalse(job["server_cancellation_attempted"])

    def test_raw_mcp_terminal_failure_is_preserved_without_error_text(self):
        def response(value):
            return {"result": {"content": [{"type": "text", "text": json.dumps(value)}]}}
        client = glm.ReviewMCP.__new__(glm.ReviewMCP)
        client.out = self.out
        client.calls = []
        client.manifest = {"calls": client.calls}
        client.tools = {name: {} for name in ("firecrawl_agent", "firecrawl_agent_status")}
        start = response({"id": "synthetic-job"})
        failed = response({"status": "failed", "model": glm.MODEL,
                           "error": "synthetic-secret-canary"})
        with patch.object(glm.MCP, "rpc", side_effect=[start, failed, failed, failed]) as rpc, patch("sys.stdout", new_callable=io.StringIO) as stdout:
            job = self.round(client, polls=3)
        self.assertEqual(job["state"], "failed")
        self.assertEqual(rpc.call_count, 2, "confirmed failure must not consume all polls")
        public_artifacts = "".join(path.read_text() for path in self.out.glob("*.json"))
        self.assertNotIn("synthetic-secret-canary", public_artifacts + stdout.getvalue())

    def test_nonterminal_poll_limit_is_unknown_not_cancelled(self):
        client = FakeClient(self.out, statuses=[ok({"status": "processing"})] * 3)
        job = self.round(client, polls=3, interval=7)
        self.assertEqual(job["state"], "unknown_nonterminal")
        self.assertEqual(len(client.calls), 4)
        self.assertEqual(self.sleep.call_count, 2)
        self.sleep.assert_called_with(7)
        self.assertFalse(job["server_cancellation_attempted"])
        self.assertIn("ended_utc", job)

    def test_transport_poll_failures_are_not_empty_evidence_or_cancellation(self):
        client = FakeClient(self.out, statuses=[{"status": "TimeoutError", "data": None}] * 2)
        job = self.round(client, polls=2)
        self.assertEqual(job["state"], "unknown_nonterminal")
        self.assertFalse(job["server_cancellation_attempted"])
        self.assertNotIn("proposal_sha256", job)


class DossierTests(Fixture):
    def test_explicit_null_reviewer_context_does_not_crash_after_review(self):
        dossier = item()
        dossier["reviewer_checks"] = None
        glm.validate_plan({"version": 1, "dossiers": [dossier]})
        client, record = self.run_dossier(dossier)
        self.assertTrue(record["complete"])
        self.assertEqual(client.jobs_started, 2)

    def test_review_and_same_model_challenge_complete(self):
        client, record = self.run_dossier()
        self.assertTrue(record["complete"])
        self.assertEqual([job["round"] for job in record["jobs"]], ["review", "challenge"])
        self.assertTrue(client.closed)
        self.assertEqual(json.loads((client.out / "dossier.json").read_text()), record)
        requests = [c["arguments"] for c in client.calls if c["tool"] == "firecrawl_agent"]
        self.assertEqual(len(requests), 2)
        self.assertTrue(all(r["urls"] == [PUBLIC] for r in requests))
        self.assertIn("UNTRUSTED PRIOR MODEL PROPOSAL (not evidence; omissions explicitly marked)", requests[1]["prompt"])
        self.assertIn((client.out / "review-proposal.md").read_text(), requests[1]["prompt"])

    def test_long_prior_review_uses_marked_bounded_head_and_tail(self):
        summary = "H" * 2400 + "omitted-middle-canary" * 400 + "T" * 2400
        client, record = self.run_dossier(statuses=[completed(summary=summary), completed()])
        selection = json.loads((client.out / "challenge-selection.json").read_text())
        prompt = [c["arguments"]["prompt"] for c in client.calls if c["label"] == "challenge_start"][0]
        self.assertTrue(record["complete"])
        self.assertTrue(selection["partial_prior_review"])
        self.assertLessEqual(selection["selected_characters"], 5000)
        self.assertLessEqual(len(prompt), 10000)
        self.assertIn("[Middle omitted: partial prior-review audit only]", prompt)
        self.assertNotIn("omitted-middle-canary", prompt)
        self.assertIn("H" * 2400, prompt)
        self.assertIn("T" * 2399, prompt)
        self.assertEqual(selection["full_prior_sha256"], hashlib.sha256((client.out / "review-proposal.md").read_bytes()).hexdigest())

    def test_short_prior_review_selection_is_explicitly_complete(self):
        client, record = self.run_dossier()
        selection = json.loads((client.out / "challenge-selection.json").read_text())
        self.assertTrue(record["complete"])
        self.assertFalse(selection["partial_prior_review"])
        self.assertEqual(selection["full_prior_characters"], selection["selected_characters"])

    def test_combined_long_questions_reject_challenge_before_model_call(self):
        dossier = item()
        dossier["question"] = "q" * 4000
        dossier["challenge"] = "c" * 4000
        client, record = self.run_dossier(dossier, statuses=[completed(summary="x" * 6000)])
        self.assertFalse(record["complete"])
        self.assertEqual(client.jobs_started, 1)
        self.assertEqual(record["jobs"][-1]["state"], "rejected_locally")

    def test_optional_challenge_is_not_invented(self):
        client, record = self.run_dossier(item(challenge=None))
        self.assertTrue(record["complete"])
        self.assertEqual(len(record["jobs"]), 1)
        self.assertEqual(client.jobs_started, 1)

    def test_invalid_first_review_does_not_launch_challenge(self):
        client, record = self.run_dossier(statuses=[completed(model="not-expected")])
        self.assertFalse(record["complete"])
        self.assertEqual(client.jobs_started, 1)
        self.assertEqual(len(record["jobs"]), 1)

    def test_failed_challenge_preserves_successful_review(self):
        client, record = self.run_dossier(statuses=[completed(), ok({"status": "failed"})])
        self.assertFalse(record["complete"])
        self.assertTrue((client.out / "review-proposal.md").is_file())
        self.assertFalse((client.out / "challenge-proposal.md").exists())
        self.assertEqual(record["jobs"][0]["state"], "completed")
        self.assertTrue(client.closed)

    def test_oversized_prior_review_blocks_challenge_without_silent_clipping(self):
        summary = "x" * 35001
        client, record = self.run_dossier(statuses=[completed(summary=summary)])
        self.assertFalse(record["complete"])
        self.assertIn("challenge_blocker", record)
        self.assertEqual(client.jobs_started, 1)
        self.assertEqual((client.out / "review-proposal.md").read_text(), summary + "\n")
        self.assertTrue(client.closed)

    def test_full_two_round_poll_budget_stays_below_mcp_limit(self):
        statuses = ([ok({"status": "processing"})] * 47 + [completed()]) * 2
        client, record = self.run_dossier(statuses=statuses)
        self.assertTrue(record["complete"])
        self.assertEqual(client.sequence, 101)  # initialize/list + discovery + 2*(start+48 polls)
        self.assertLess(client.sequence, 120)
        self.assertEqual(client.jobs_started, 2)

    def test_existing_dossier_is_never_overwritten(self):
        existing = self.out / "fixture"
        existing.mkdir()
        (existing / "sentinel").write_text("preserve")
        with patch.object(glm, "ReviewMCP") as constructor:
            with self.assertRaises(FileExistsError):
                glm.run_dossier(item(), self.out, self.root / "index.js")
        constructor.assert_not_called()
        self.assertEqual((existing / "sentinel").read_text(), "preserve")

    def test_worker_exception_closes_client_and_records_incomplete_dossier(self):
        dossier = item()
        client = FakeClient(self.out / dossier["id"], statuses=[RuntimeError("synthetic failure")])
        with patch.object(glm, "ReviewMCP", return_value=client):
            with self.assertRaises(RuntimeError):
                glm.run_dossier(dossier, self.out, self.root / "index.js")
        self.assertTrue(client.closed)
        self.assertFalse(json.loads((client.out / "dossier.json").read_text())["complete"])


class ProjectionTests(Fixture):
    def call_status(self, value=None, raw=None, name="firecrawl_agent_status"):
        response = raw if raw is not None else {
            "result": {"content": [{"type": "text", "text": json.dumps(value)}]}}
        client = glm.ReviewMCP.__new__(glm.ReviewMCP)
        client.out = self.out
        client.calls = []
        client.manifest = {"calls": client.calls}
        client.tools = {name: {}}
        with patch.object(glm.MCP, "rpc", return_value=response), patch("sys.stdout", new_callable=io.StringIO):
            return client.call("synthetic_status", name, {"id": "synthetic-own-job"})

    def test_failure_and_cancellation_have_only_safe_terminal_metadata(self):
        for state in ("failed", "cancelled"):
            with self.subTest(state=state):
                result = self.call_status({"status": state, "model": glm.MODEL,
                                           "error": "synthetic-secret-canary", "private_debug": "synthetic-secret-canary"})
                self.assertEqual(result["status"], "ok")
                self.assertEqual(result["data"]["terminal_state"], state)
                self.assertEqual(result["data"]["error_category"], "service_failure")
                self.assertEqual(set(result["data"]), {"terminal_state", "model", "error_category"})
                self.assertNotIn("synthetic-secret-canary", (self.out / "synthetic_status.json").read_text())

    def test_unvalidated_model_field_cannot_carry_error_payload(self):
        for model in ({"debug": "synthetic-secret-canary"}, ["synthetic-secret-canary"], "synthetic-secret-canary"):
            with self.subTest(model=model):
                result = self.call_status({"status": "failed", "model": model, "error": "failed"})
                self.assertNotIn("synthetic-secret-canary", json.dumps(result))
                self.assertNotIn("synthetic-secret-canary", (self.out / "synthetic_status.json").read_text())

    def test_content_filter_error_is_not_mislabelled_missing_source_content(self):
        result = self.call_status({"status": "failed", "model": glm.MODEL,
                                   "error": "Provider content filter rejected the request"})
        self.assertEqual(result["data"]["error_category"], "service_failure")

    def test_explicit_no_content_error_has_specific_category(self):
        result = self.call_status({"status": "failed", "model": glm.MODEL,
                                   "error": "No content found from supplied URLs"})
        self.assertEqual(result["data"]["error_category"], "no_content")

    def test_rpc_error_and_iserror_do_not_become_trusted_terminal_results(self):
        for response in (
            {"error": {"message": "synthetic-secret-canary"}},
            {"result": {"isError": True, "content": [{"type": "text", "text": "synthetic-secret-canary"}]}},
        ):
            with self.subTest(response=response):
                result = self.call_status(raw=response)
                self.assertNotEqual(result["status"], "ok")
                self.assertIsNone(result["data"])
                self.assertNotIn("synthetic-secret-canary", (self.out / "synthetic_status.json").read_text())

    def test_projection_does_not_modify_successful_summary_or_other_tools(self):
        value = {"status": "completed", "model": glm.MODEL, "data": {"summary": "Synthetic public output"}}
        result = self.call_status(value)
        self.assertEqual(result["data"], value)
        failed_search = self.call_status({"status": "failed", "error": "synthetic-secret-canary"}, name="firecrawl_search")
        self.assertNotEqual(failed_search["status"], "ok")
        self.assertIsNone(failed_search["data"])

    def test_malformed_status_envelopes_are_sanitized_failures(self):
        for response in ({"result": None}, {"result": {"content": None}},
                         {"result": {"content": [None]}}, {"result": {"content": [{"type": "text", "text": 7}]}}):
            with self.subTest(response=response):
                result = self.call_status(raw=response)
                self.assertNotEqual(result["status"], "ok")
                self.assertIsNone(result["data"])


class ChallengeOnlyTests(Fixture):
    def setUp(self):
        super().setUp()
        patch.object(glm, "ROOT", self.root).start()
        self.source = self.root / "results/feat009/glm-literature-abstracts-v2"
        self.prior = self.source / "fixture"
        self.prior.mkdir(parents=True)
        self.proposal = self.prior / "review-proposal.md"
        self.proposal.write_text("Synthetic prior unverified public review.\n")
        self.metadata_path = self.prior / "review-job.json"
        self.metadata = {"state": "completed", "model": glm.MODEL, "round": "review",
                         "proposal_sha256": hashlib.sha256(self.proposal.read_bytes()).hexdigest(),
                         "verified_claims": False}
        self.metadata_path.write_text(json.dumps(self.metadata))

    def invoke(self):
        client = FakeClient(self.out / "fixture")
        self.last_client = client
        with patch.object(glm, "ReviewMCP", return_value=client):
            record = glm.run_dossier(item(), self.out, self.root / "index.js", self.source)
        return client, record

    def test_challenge_only_preserves_prior_and_starts_only_one_job(self):
        before = {p.name: p.read_bytes() for p in self.prior.iterdir()}
        client, record = self.invoke()
        self.assertTrue(record["complete"])
        self.assertEqual(len(record["jobs"]), 1)
        self.assertEqual(record["jobs"][0]["round"], "challenge")
        self.assertEqual(client.jobs_started, 1)
        self.assertFalse(any(c["tool"] == "firecrawl_search" for c in client.calls))
        self.assertEqual(record["prior_proposal_sha256"], self.metadata["proposal_sha256"])
        self.assertEqual(record["prior_proposal"], str(self.proposal.relative_to(self.root)))
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.prior.iterdir()})
        self.assertTrue(client.closed)

    def test_proposal_byte_drift_is_rejected_before_model_call(self):
        self.proposal.write_text("changed bytes")
        with self.assertRaises(ValueError):
            self.invoke()
        self.assertEqual(self.last_client.jobs_started, 0)
        self.assertTrue(self.last_client.closed)

    def test_wrong_model_and_incomplete_state_are_rejected(self):
        for key, bad in (("model", "other-model"), ("state", "unknown_nonterminal"),
                         ("proposal_sha256", "0" * 64)):
            with self.subTest(key=key):
                altered = dict(self.metadata)
                altered[key] = bad
                self.metadata_path.write_text(json.dumps(altered))
                # Each attempt gets a separate new output directory.
                original_out = self.out
                self.out = self.root / ("output-" + key)
                self.out.mkdir()
                try:
                    with self.assertRaises(ValueError):
                        self.invoke()
                    self.assertEqual(self.last_client.jobs_started, 0)
                    self.assertTrue(self.last_client.closed)
                finally:
                    self.out = original_out

    def test_symlinked_proposal_is_rejected_even_with_matching_hash(self):
        alternate = self.root / "other-public-proposal.md"
        alternate.write_bytes(self.proposal.read_bytes())
        self.proposal.unlink()
        self.proposal.symlink_to(alternate)
        with self.assertRaises(ValueError):
            self.invoke()
        self.assertEqual(self.last_client.jobs_started, 0)

    def test_symlinked_metadata_is_rejected(self):
        alternate = self.root / "other-metadata.json"
        alternate.write_bytes(self.metadata_path.read_bytes())
        self.metadata_path.unlink()
        self.metadata_path.symlink_to(alternate)
        with self.assertRaises(ValueError):
            self.invoke()
        self.assertEqual(self.last_client.jobs_started, 0)

    def test_symlinked_source_root_is_rejected(self):
        alternate = self.root / "other-run"
        self.source.rename(alternate)
        self.source.symlink_to(alternate, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.invoke()
        self.assertEqual(self.last_client.jobs_started, 0)

    def test_symlinked_dossier_cannot_escape_prior_run(self):
        alternate = self.root / "other-dossier"
        self.prior.rename(alternate)
        self.prior.symlink_to(alternate, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.invoke()
        self.assertEqual(self.last_client.jobs_started, 0)

    def test_selection_hash_uses_prior_file_bytes_not_newline_normalization(self):
        self.proposal.write_bytes(b"Synthetic public review.\r\nSecond line.\r\n")
        self.metadata["proposal_sha256"] = hashlib.sha256(self.proposal.read_bytes()).hexdigest()
        self.metadata_path.write_text(json.dumps(self.metadata))
        client, record = self.invoke()
        self.assertTrue(record["complete"])
        selection = json.loads((client.out / "challenge-selection.json").read_text())
        self.assertEqual(selection["full_prior_sha256"], record["prior_proposal_sha256"])


class MainTests(Fixture):
    def setUp(self):
        super().setUp()
        self.plan_path = self.root / "public-plan.json"
        self.plan_bytes = json.dumps({"version": 1, "dossiers": [item("one"), item("two", None)]}).encode()
        self.plan_path.write_bytes(self.plan_bytes)
        self.target = self.root / "results/feat009/fresh"
        self.root_patch = patch.object(glm, "ROOT", self.root)
        self.plan_patch = patch.object(glm, "PLAN", self.plan_path)
        self.root_patch.start()
        self.plan_patch.start()

    def invoke(self, output=None, selected=None, complete=True, extra=None):
        argv = ["test", str(output or self.target)]
        if selected is not None:
            argv += ["--dossiers", *selected]
        if extra:
            argv += extra
        def worker(dossier, root, entry, challenge_source=None):
            return {"id": dossier["id"], "complete": complete,
                    "jobs": [{"state": "completed" if complete else "unknown_nonterminal"}]}
        with patch("sys.argv", argv), patch.object(glm, "run_dossier", side_effect=worker) as run, patch("sys.stdout", new_callable=io.StringIO) as stdout:
            code = glm.main()
        return code, run, stdout.getvalue()

    def test_manifest_binds_plan_runner_selected_scope_and_limits(self):
        code, run, stdout = self.invoke(selected=["two"])
        manifest = json.loads((self.target / "run.json").read_text())
        self.assertEqual(code, 0)
        self.assertTrue(manifest["complete"])
        self.assertEqual(manifest["dossiers"], ["two"])
        self.assertEqual((self.target / "plan.json").read_bytes(), self.plan_bytes)
        self.assertEqual(manifest["plan_sha256"], hashlib.sha256(self.plan_bytes).hexdigest())
        self.assertEqual(manifest["runner_sha256"], hashlib.sha256((self.target / "executed-runner.py").read_bytes()).hexdigest())
        self.assertEqual(manifest["max_parallel_workers"], 2)
        self.assertNotIn("max_parallel_jobs", manifest)
        self.assertIs(manifest["clinical_efficacy_established"], False)
        self.assertIn("not independent evidence", " ".join(manifest["limitations"]))
        self.assertIn("does not cancel", " ".join(manifest["limitations"]))
        self.assertEqual(run.call_count, 1)
        self.assertTrue(json.loads(stdout)["complete"])

    def test_partial_run_returns_nonzero_with_retained_results(self):
        code, run, stdout = self.invoke(complete=False)
        manifest = json.loads((self.target / "run.json").read_text())
        self.assertEqual(code, 2)
        self.assertFalse(manifest["complete"])
        self.assertEqual(len(manifest["results"]), 2)
        self.assertIn("ended_utc", manifest)
        self.assertEqual(json.loads(stdout)["completed_glm_jobs"], 0)

    def test_abstract_cli_archives_original_and_effective_scope(self):
        code, run, _ = self.invoke(extra=["--abstract-records"])
        manifest = json.loads((self.target / "run.json").read_text())
        effective_path = self.target / "effective-plan.json"
        effective = json.loads(effective_path.read_text())
        self.assertEqual(code, 0)
        self.assertTrue(manifest["abstract_records"])
        self.assertEqual(manifest["effective_plan_sha256"], hashlib.sha256(effective_path.read_bytes()).hexdigest())
        self.assertEqual((self.target / "plan.json").read_bytes(), self.plan_bytes)
        for dossier in effective["dossiers"]:
            self.assertEqual(dossier["original_urls"], [PUBLIC])
            self.assertEqual(dossier["urls"], [glm.abstract_record(PUBLIC)])
            self.assertIn("NOT full text", dossier["question"])
            self.assertIn("Mark unavailable details unknown", dossier["question"])

    def test_current_effective_plan_challenges_fit_prompt_budget(self):
        public_plan = Path(glm.__file__).resolve().parents[1] / "notes/track2-glm-plan.json"
        self.plan_path.write_bytes(public_plan.read_bytes())
        _, run, _ = self.invoke(extra=["--abstract-records"])
        trial_root = self.root / "prompt-budget-checks"
        trial_root.mkdir()
        for call in run.call_args_list:
            dossier = call.args[0]
            if not dossier.get("challenge"):
                continue
            with self.subTest(dossier=dossier["id"]):
                client = FakeClient(trial_root / dossier["id"], statuses=[completed(summary="x" * 12000), completed()])
                with patch.object(glm, "ReviewMCP", return_value=client):
                    record = glm.run_dossier(dossier, trial_root, self.root / "index.js")
                self.assertTrue(record["complete"])
                self.assertEqual(client.jobs_started, 2)
                for request in client.calls:
                    if request["tool"] == "firecrawl_agent":
                        self.assertLessEqual(len(request["arguments"]["prompt"]), 10000)

    def test_challenge_only_requires_abstract_mode_and_enabled_selection(self):
        for selected, flags in ((["one"], ["--challenge-only"]),
                                (["two"], ["--challenge-only", "--abstract-records"]),
                                (None, ["--challenge-only", "--abstract-records"])):
            with self.subTest(selected=selected, flags=flags), patch("sys.stderr", new_callable=io.StringIO):
                with self.assertRaises(SystemExit):
                    self.invoke(selected=selected, extra=flags)
                self.assertFalse(self.target.exists())

    def test_challenge_only_refuses_missing_prior_review(self):
        with patch("sys.stderr", new_callable=io.StringIO), self.assertRaises(SystemExit):
            self.invoke(selected=["one"], extra=["--challenge-only", "--abstract-records"])
        self.assertFalse(self.target.exists())

    def test_challenge_only_cli_uses_fixed_prior_run_not_arbitrary_input(self):
        source = self.root / "results/feat009/glm-literature-abstracts-v2"
        prior = source / "one"
        prior.mkdir(parents=True)
        (prior / "review-proposal.md").write_text("Synthetic prior public review")
        code, run, _ = self.invoke(selected=["one"], extra=["--challenge-only", "--abstract-records"])
        self.assertEqual(code, 0)
        self.assertEqual(run.call_args.args[3], source)
        self.assertTrue(json.loads((self.target / "run.json").read_text())["challenge_only"])

    def test_unknown_or_duplicate_selection_fails_before_output(self):
        for selected in (["unknown"], ["one", "one"]):
            with self.subTest(selected=selected), patch("sys.stderr", new_callable=io.StringIO):
                with self.assertRaises(SystemExit):
                    self.invoke(selected=selected)
                self.assertFalse(self.target.exists())

    def test_rejects_existing_output(self):
        self.target.mkdir(parents=True)
        (self.target / "sentinel").write_text("preserve")
        with self.assertRaises(FileExistsError):
            self.invoke()
        self.assertEqual((self.target / "sentinel").read_text(), "preserve")

    def test_rejects_outside_output_and_output_root(self):
        for path in (self.root / "outside", self.root / "results/feat009"):
            with self.subTest(path=path), patch("sys.stderr", new_callable=io.StringIO):
                with self.assertRaises(SystemExit):
                    self.invoke(output=path)

    def test_refuses_to_nest_output_in_immutable_research_snapshots(self):
        for version in (1, 2, 3):
            package = self.root / f"results/feat009/jvv7_track2_research_v{version}"
            package.mkdir(parents=True)
            (package / "manifest.json").write_text('{"synthetic":"historical"}')
            nested = package / "new_glm_run"
            with self.subTest(version=version), patch("sys.stderr", new_callable=io.StringIO):
                with self.assertRaises((SystemExit, ValueError)):
                    self.invoke(output=nested)
                self.assertFalse(nested.exists())
                self.assertEqual({p.name for p in package.iterdir()}, {"manifest.json"})


if __name__ == "__main__":
    unittest.main()
