#!/usr/bin/env python3
"""Offline adversarial tests: synthetic MCP only, no service or subject inputs."""
from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import time
import unittest
from unittest.mock import Mock, patch

import track2_firecrawl as fc


def envelope(value, ident=1):
    return {"jsonrpc": "2.0", "id": ident, "result": value}


def content(value):
    text = value if isinstance(value, str) else json.dumps(value)
    return envelope({"content": [{"type": "text", "text": text}]})


def ok(data):
    return {"status": "ok", "data": data}


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="firecrawl-offline-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.out = self.root / "output"
        self.out.mkdir()

    def client(self):
        client = fc.MCP.__new__(fc.MCP)
        client.out = self.out
        client.calls = []
        client.manifest = {"calls": client.calls}
        client.tools = {"synthetic_tool": {"name": "synthetic_tool"}}
        client.sequence = 0
        client.buffer = b""
        client.proc = Mock()
        client.proc.stdin = io.BytesIO()
        client.proc.stdout.fileno.return_value = 987654
        client.selector = Mock()
        client.selector.select.return_value = [(None, 1)]
        return client

    def entry(self, package='{"version":"synthetic-1"}'):
        dist = self.root / "package" / "dist"
        dist.mkdir(parents=True)
        entry = dist / "index.js"
        entry.write_text("// Synthetic fixture; never executed.\n")
        if package is not None:
            (dist.parent / "package.json").write_text(package)
        return entry

    def invoke(self, response, project=None):
        client = self.client()
        client.rpc = Mock(return_value=response)
        with patch("sys.stdout", new_callable=io.StringIO):
            result = client.call("synthetic", "synthetic_tool", {"query": "public literature"}, project=project)
        return client, result


class DecodeTests(Fixture):
    def test_json_and_plain_text_success(self):
        for value in ({"data": [{"title": "Public paper"}]}, "A public paper passage."):
            with self.subTest(value=value):
                result = fc.decode(content(value))
                self.assertEqual(result["status"], "ok")
                self.assertEqual(result["data"], value)

    def test_explicit_rpc_and_tool_errors_redact(self):
        responses = [
            {"jsonrpc": "2.0", "id": 1, "error": {"message": "synthetic-canary"}},
            envelope({"isError": True, "content": [{"type": "text", "text": "synthetic-canary"}]}),
            content({"success": False, "error": "synthetic-canary"}),
            content({"status": "failed", "error": "synthetic-canary"}),
            content({"status": "cancelled", "error": "synthetic-canary"}),
        ]
        for response in responses:
            with self.subTest(response=response):
                client, result = self.invoke(response)
                self.assertNotEqual(result["status"], "ok")
                self.assertIsNone(result["data"])
                self.assertNotIn("synthetic-canary", (self.out / "synthetic.json").read_text())
                self.assertIn("ended_utc", client.calls[0])

    def test_structured_error_without_mcp_flag_redacts(self):
        for value in ({"status": "error", "error": "synthetic-canary"}, {"error": "synthetic-canary"}):
            with self.subTest(value=value):
                _, result = self.invoke(content(value))
                self.assertNotEqual(result["status"], "ok")
                self.assertIsNone(result["data"])
                self.assertNotIn("synthetic-canary", (self.out / "synthetic.json").read_text())

    def test_unsupported_no_content_envelopes_fail_closed(self):
        bodies = (
            {"error": "synthetic-canary"},
            {"status": "failed", "detail": "synthetic-canary"},
            {"truncated": True, "data": ["synthetic-canary"]},
            {"structuredContent": {"title": "Unsupported response shape"}},
        )
        for body in bodies:
            with self.subTest(body=body):
                client, result = self.invoke(envelope(body))
                self.assertEqual(result["status"], "tool_error")
                self.assertIsNone(result["data"])
                self.assertNotIn("synthetic-canary", (self.out / "synthetic.json").read_text())
                self.assertIn("ended_utc", client.calls[0])

    def test_empty_content_is_not_success(self):
        for response in (envelope({}), envelope({"content": []}), content(""), content(" \n ")):
            with self.subTest(response=response):
                self.assertNotEqual(fc.decode(response)["status"], "ok")

    def test_known_no_result_markers(self):
        for marker in ("(no results)", "(paper not found)", "(no full-text passages available for this paper)"):
            with self.subTest(marker=marker):
                self.assertEqual(fc.decode(content(marker))["status"], "empty")

    def test_explicit_structured_empty_is_not_success(self):
        for value in ({"data": []}, {"data": {"web": []}}, {"papers": []}):
            with self.subTest(value=value):
                self.assertNotEqual(fc.decode(content(value))["status"], "ok")

    def test_plain_text_truncation_is_flagged(self):
        self.assertTrue(fc.decode(content("Result truncated at configured limit"))["possible_truncation"])

    def test_structured_truncation_is_flagged(self):
        result = fc.decode(content({"success": True, "truncated": True, "data": [{"title": "Partial paper"}]}))
        self.assertTrue(result.get("possible_truncation"))

    def test_malformed_response_is_accounted_without_exception_text(self):
        for response in (None, [], envelope(None), envelope({"content": None}), envelope({"content": [None]})):
            with self.subTest(response=response):
                client, result = self.invoke(response)
                self.assertNotEqual(result["status"], "ok")
                self.assertIsNone(result["data"])
                self.assertIn("ended_utc", client.calls[0])


class CallTests(Fixture):
    def test_success_artifact_has_exact_hash_and_arguments(self):
        client, result = self.invoke(content({"title": "Public source"}))
        artifact = self.out / "synthetic.json"
        self.assertEqual(client.calls[0]["sha256"], hashlib.sha256(artifact.read_bytes()).hexdigest())
        self.assertEqual(json.loads(artifact.read_text()), result)
        self.assertEqual(client.calls[0]["arguments"], {"query": "public literature"})

    def test_rejects_unadvertised_tool_before_rpc(self):
        client = self.client()
        client.rpc = Mock()
        with self.assertRaises(ValueError):
            client.call("label", "not_advertised", {})
        client.rpc.assert_not_called()

    def test_rejects_unsafe_labels_before_rpc(self):
        for label in ("../escape", "/absolute", "a/b", ".", "", "line\nname"):
            with self.subTest(label=label):
                client = self.client()
                client.rpc = Mock()
                with self.assertRaises(ValueError):
                    client.call(label, "synthetic_tool", {})
                client.rpc.assert_not_called()

    def test_timeout_has_no_retry_and_retains_prior_success(self):
        client = self.client()
        client.rpc = Mock(side_effect=[content({"title": "Retained"}), TimeoutError("synthetic-canary")])
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            client.call("first", "synthetic_tool", {})
            result = client.call("second", "synthetic_tool", {})
        self.assertEqual(client.rpc.call_count, 2)
        self.assertNotEqual(result["status"], "ok")
        self.assertEqual(json.loads((self.out / "first.json").read_text())["data"], {"title": "Retained"})
        self.assertNotIn("synthetic-canary", stdout.getvalue() + (self.out / "manifest.json").read_text())
        self.assertIn("ended_utc", client.calls[-1])

    def test_projection_does_not_archive_other_monitors(self):
        value = {"data": [{"id": "ours", "name": "own-public"}, {"id": "other", "name": "unrelated-canary"}]}
        _, result = self.invoke(content(value), lambda data: fc.own_monitor_projection(data, "ours"))
        self.assertEqual(result["data"], {"own_monitor_found": True})
        self.assertNotIn("unrelated-canary", (self.out / "synthetic.json").read_text())

    def test_projection_failure_does_not_archive_raw_response(self):
        def fail_projection(value):
            raise ValueError("unrelated-canary")
        client, result = self.invoke(content({"data": "unrelated-canary"}), fail_projection)
        self.assertNotEqual(result["status"], "ok")
        self.assertNotIn("unrelated-canary", (self.out / "manifest.json").read_text())
        self.assertFalse((self.out / "synthetic.json").exists())
        self.assertIn("ended_utc", client.calls[0])

    def test_projection_accepts_nested_list_and_false_absence(self):
        self.assertEqual(fc.own_monitor_projection({"data": {"monitors": [{"id": "own"}]}}, "own"), {"own_monitor_found": True})
        self.assertEqual(fc.own_monitor_projection({"data": [{"id": "other"}]}, "own"), {"own_monitor_found": False})

    def test_malformed_monitor_projection_fails_closed(self):
        for value in ({"data": None}, {"data": {"monitors": None}}, {"data": 7}):
            with self.subTest(value=value):
                _, result = self.invoke(content(value), lambda data: fc.own_monitor_projection(data, "own"))
                self.assertNotEqual(result["status"], "ok")
                self.assertIsNone(result["data"])


class RPCTests(Fixture):
    def test_fragmented_response_and_notification_are_handled(self):
        client = self.client()
        notification = b'{"jsonrpc":"2.0","method":"notifications/message"}\n'
        body = json.dumps(envelope({"value": 1})).encode() + b"\n"
        with patch.object(fc.os, "read", side_effect=[notification + body[:12], body[12:]]):
            self.assertEqual(client.rpc("synthetic", {}), envelope({"value": 1}))
        request = json.loads(client.proc.stdin.getvalue())
        self.assertEqual(request["id"], 1)
        self.assertEqual(request["jsonrpc"], "2.0")

    def test_eof_fails_instead_of_returning_empty(self):
        client = self.client()
        with patch.object(fc.os, "read", return_value=b""):
            with self.assertRaises(RuntimeError):
                client.rpc("synthetic", {})

    def test_deadline_has_no_retry(self):
        client = self.client()
        client.selector.select.return_value = []
        with self.assertRaises(TimeoutError):
            client.rpc("synthetic", {}, timeout=0.01)
        self.assertEqual(client.sequence, 1)

    def test_response_byte_budget(self):
        client = self.client()
        with patch.object(fc, "MAX_RESPONSE", 50), patch.object(fc.os, "read", return_value=b"x" * 51):
            with self.assertRaises(RuntimeError):
                client.rpc("synthetic", {})

    def test_notification_stream_cannot_reset_byte_budget(self):
        client = self.client()
        line = b'{"method":"notice"}\n'
        with patch.object(fc, "MAX_RESPONSE", 50), patch.object(fc.os, "read", return_value=line):
            with self.assertRaises(RuntimeError):
                client.rpc("synthetic", {})

    def test_call_budget_applies_before_write(self):
        client = self.client()
        client.sequence = fc.MAX_CALLS
        with self.assertRaises(ValueError):
            client.rpc("synthetic", {})
        self.assertEqual(client.proc.stdin.getvalue(), b"")

    @unittest.skipUnless(hasattr(signal, "setitimer"), "POSIX deadline check")
    def test_full_stdin_pipe_cannot_defeat_rpc_deadline(self):
        client = self.client()
        read_fd, write_fd = os.pipe()
        self.addCleanup(os.close, read_fd)
        os.set_blocking(write_fd, False)
        while True:
            try:
                os.write(write_fd, b"x" * 4096)
            except BlockingIOError:
                break
        os.set_blocking(write_fd, True)
        client.proc.stdin = os.fdopen(write_fd, "wb", buffering=0)
        self.addCleanup(client.proc.stdin.close)
        def watchdog(signum, frame):
            raise TimeoutError("synthetic outer watchdog; RPC deadline was missed")
        old_handler = signal.signal(signal.SIGALRM, watchdog)
        previous_timer = signal.setitimer(signal.ITIMER_REAL, 0.3)
        started = time.monotonic()
        try:
            with self.assertRaises((TimeoutError, RuntimeError)):
                client.rpc("synthetic", {}, timeout=0.01)
        finally:
            signal.setitimer(signal.ITIMER_REAL, *previous_timer)
            signal.signal(signal.SIGALRM, old_handler)
        self.assertLess(time.monotonic() - started, 0.2, "stdin write outlived the declared RPC deadline")

    def test_wrong_id_never_accepted(self):
        client = self.client()
        wrong = json.dumps(envelope({"value": "wrong"}, 17)).encode() + b"\n"
        with patch.object(fc.os, "read", side_effect=[wrong, b""]):
            with self.assertRaises(RuntimeError):
                client.rpc("synthetic", {})


class StartupTests(Fixture):
    def test_post_spawn_registration_failure_closes_child(self):
        entry = self.entry()
        proc = Mock()
        selector = Mock()
        selector.register.side_effect = RuntimeError('synthetic registration failure')
        with patch.object(fc.subprocess, 'Popen', return_value=proc), patch.object(fc.selectors, 'DefaultSelector', return_value=selector):
            with self.assertRaises(RuntimeError):
                fc.MCP(entry, self.out)
        proc.terminate.assert_called_once()
        proc.stdin.close.assert_called_once()
        proc.stdout.close.assert_called_once()
        selector.close.assert_called_once()

    def test_child_environment_does_not_inherit_credentials(self):
        with patch.dict(os.environ, {"SYNTHETIC_API_KEY": "never-inherit", "NODE_OPTIONS": "--require=untrusted", "PYTHONPATH": "untrusted", "HTTP_PROXY": "untrusted"}):
            env = fc.child_env()
        self.assertNotIn("never-inherit", json.dumps(env))
        self.assertNotIn("NODE_OPTIONS", env)
        self.assertNotIn("PYTHONPATH", env)
        self.assertNotIn("HTTP_PROXY", env)
        self.assertNotIn("HOME", env)
        self.assertEqual(env["FIRECRAWL_API_URL"], "http://127.0.0.1:3002")

    def test_constructor_isolated_cwd_and_entry_provenance(self):
        entry = self.entry()
        proc = Mock()
        proc.stdin = io.BytesIO()
        proc.stdout = io.BytesIO()
        observed = {}
        def popen(command, **kwargs):
            observed.update(kwargs)
            self.assertEqual(list(Path(kwargs["cwd"]).iterdir()), [])
            self.assertEqual(command[-1], str(entry))
            return proc
        with patch.object(fc.subprocess, "Popen", side_effect=popen), patch.object(fc.selectors, "DefaultSelector", return_value=Mock()):
            client = fc.MCP(entry, self.out)
        self.addCleanup(client.tmp.cleanup)
        self.assertNotEqual(Path(observed["cwd"]), fc.ROOT)
        self.assertEqual(observed["stderr"], subprocess.DEVNULL)
        self.assertTrue(observed["start_new_session"])
        self.assertEqual(client.manifest["mcp_entry_sha256"], hashlib.sha256(entry.read_bytes()).hexdigest())
        self.assertEqual(client.manifest["mcp_package_version"], "synthetic-1")
        client.close()
        self.assertFalse(Path(observed["cwd"]).exists())

    def test_invalid_entry_is_rejected_without_process(self):
        target = self.root / "target.js"
        target.write_text("// fixture")
        link = self.root / "index.js"
        link.symlink_to(target)
        for entry in (self.root / "missing" / "index.js", target, link):
            with self.subTest(entry=entry), patch.object(fc.subprocess, "Popen") as popen:
                with self.assertRaises(ValueError):
                    fc.MCP(entry, self.out)
                popen.assert_not_called()

    def test_constructor_metadata_failure_does_not_orphan_child(self):
        entry = self.entry(package="not-json")
        proc = Mock()
        with patch.object(fc.subprocess, "Popen", return_value=proc) as popen, patch.object(fc.selectors, "DefaultSelector", return_value=Mock()):
            with self.assertRaises((ValueError, RuntimeError)):
                fc.MCP(entry, self.out)
        self.assertTrue(not popen.called or proc.terminate.called or proc.kill.called, "constructor failed after spawning an unclosed child")

    def test_discovery_records_tools_and_sends_initialized(self):
        client = self.client()
        tools = [{"name": "synthetic_tool", "inputSchema": {"type": "object"}}]
        client.rpc = Mock(side_effect=[envelope({"protocolVersion": "2025-06-18", "capabilities": {"tools": {}}, "serverInfo": {"name": "fixture", "version": "1"}}), envelope({"tools": tools})])
        self.assertEqual(set(client.initialize()), {"synthetic_tool"})
        self.assertEqual(client.manifest["advertised_tools"], ["synthetic_tool"])
        self.assertEqual(json.loads(client.proc.stdin.getvalue())["method"], "notifications/initialized")
        self.assertTrue((self.out / "tools.json").exists())

    def test_discovery_rejects_duplicate_tool_names(self):
        client = self.client()
        client.rpc = Mock(side_effect=[envelope({"protocolVersion": "2025-06-18", "capabilities": {"tools": {}}, "serverInfo": {"name": "fixture", "version": "1"}}), envelope({"tools": [{"name": "duplicate"}, {"name": "duplicate"}]})])
        with self.assertRaises((ValueError, RuntimeError)):
            client.initialize()

    def test_close_kills_after_termination_timeout(self):
        client = self.client()
        client.tmp = Mock()
        client.proc.wait.side_effect = [subprocess.TimeoutExpired("synthetic", 5), 0]
        client.close()
        client.proc.kill.assert_called_once()
        client.selector.close.assert_called_once()
        client.tmp.cleanup.assert_called_once()
        self.assertIn("ended_utc", client.manifest)

    def test_main_refuses_outside_output_and_existing_directory(self):
        for out in (self.root / "outside", self.root / "results" / "feat009" / "existing"):
            if out.name == "existing":
                out.mkdir(parents=True)
                (out / "sentinel").write_text("preserve")
            with self.subTest(out=out), patch.object(fc, "ROOT", self.root), patch("sys.argv", ["test", "discover", str(out)]), patch.object(fc, "MCP") as constructor:
                with self.assertRaises((ValueError, FileExistsError)):
                    fc.main()
                constructor.assert_not_called()
                if out.name == "existing":
                    self.assertEqual((out / "sentinel").read_text(), "preserve")

    def test_main_closes_after_workflow_failure(self):
        out = self.root / "results" / "feat009" / "fresh"
        client = Mock()
        client.initialize.return_value = {"fixture": {}}
        with patch.object(fc, "ROOT", self.root), patch("sys.argv", ["test", "research", str(out)]), patch.object(fc, "MCP", return_value=client), patch.object(fc, "research", side_effect=RuntimeError("synthetic")), patch("sys.stdout", new_callable=io.StringIO):
            with self.assertRaises(RuntimeError):
                fc.main()
        client.close.assert_called_once()

    def test_main_returns_failure_for_failed_rpc_calls(self):
        out = self.root / "results" / "feat009" / "fresh"
        client = WorkflowClient(out)
        client.initialize = Mock(return_value={"synthetic_tool": {}})
        client.close = Mock()
        def failed_workflow(value):
            value.calls.append({"label": "synthetic", "tool": "synthetic_tool", "status": "tool_error"})
            value.manifest["calls"] = value.calls
        with patch.object(fc, "ROOT", self.root), patch("sys.argv", ["test", "research", str(out)]), patch.object(fc, "MCP", return_value=client), patch.object(fc, "research", side_effect=failed_workflow), patch("sys.stdout", new_callable=io.StringIO):
            result = fc.main()
        self.assertNotIn(result, (None, 0), "all failed calls must not produce a successful CLI exit")
        client.close.assert_called_once()


class WorkflowClient:
    def __init__(self, out, overrides=None):
        self.out = out
        self.manifest = {}
        self.calls = []
        self.overrides = overrides or {}

    def call(self, label, name, arguments, **kwargs):
        self.calls.append((label, name, arguments, kwargs))
        value = self.overrides.get(label, ok({}))
        if isinstance(value, BaseException):
            raise value
        return value


class WorkflowTests(Fixture):
    def test_monitor_advanced_body_contains_complete_public_target(self):
        client = WorkflowClient(self.out)
        fc.capabilities(client)
        args = next(args for label, _, args, _ in client.calls if label == 'monitor_create')
        self.assertEqual(set(args), {'body'})
        body = args['body']
        self.assertIs(body['judgeEnabled'], False)
        self.assertEqual(body['targets'], [{'type': 'scrape', 'urls': [fc.PUBLIC_GENE]}])
        self.assertEqual(body['schedule'], {'text': 'every day', 'timezone': 'UTC'})
        self.assertNotIn('webhook', body)
        self.assertNotIn('notification', body)

    def test_research_fixed_public_scope_and_bounded_calls(self):
        client = WorkflowClient(self.out)
        fc.research(client)
        self.assertLess(len(client.calls), fc.MAX_CALLS)
        encoded = json.dumps(client.calls)
        self.assertNotIn("filePath", encoded)
        self.assertNotIn(".env", encoded)
        self.assertNotIn("PROBAND", encoded)
        self.assertEqual(sum(name == "firecrawl_search" for _, name, _, _ in client.calls), len(fc.QUERIES))
        for _, name, arguments, _ in client.calls:
            if name == "firecrawl_scrape":
                self.assertTrue(arguments["url"].startswith("https://www.jci.org/articles/view/"))

    def test_parse_only_fixed_public_scrape_html(self):
        client = WorkflowClient(self.out, {"public_gene": ok({"html": "<h1>Synthetic public gene</h1>"})})
        with patch.object(fc.time, "sleep"):
            fc.capabilities(client)
        parse = [args for _, name, args, _ in client.calls if name == "firecrawl_parse"]
        self.assertEqual(len(parse), 1)
        path = Path(parse[0]["filePath"])
        self.assertEqual(path.parent, self.out)
        self.assertEqual(path.read_text(), "<h1>Synthetic public gene</h1>")

    def test_temporary_monitor_ids_bound_to_own_creation(self):
        client = WorkflowClient(self.out, {"monitor_create": ok({"data": {"id": "synthetic-own"}}), "monitor_delete": ok({"success": True})})
        with patch.object(fc.time, "sleep"):
            fc.capabilities(client)
        own_calls = [(name, args, kwargs) for _, name, args, kwargs in client.calls if name.startswith("firecrawl_monitor_") and name != "firecrawl_monitor_create"]
        for name, args, kwargs in own_calls:
            if name == "firecrawl_monitor_list":
                self.assertTrue(callable(kwargs["project"]))
            else:
                self.assertEqual(args["id"], "synthetic-own")
        self.assertEqual(client.calls[-1][1], "firecrawl_monitor_delete")
        self.assertTrue(client.manifest["temporary_monitor_deleted"])

    def test_empty_delete_response_does_not_claim_deleted(self):
        client = WorkflowClient(self.out, {"monitor_create": ok({"data": {"id": "synthetic-own"}}), "monitor_delete": ok({})})
        with patch.object(fc.time, "sleep"):
            fc.capabilities(client)
        self.assertFalse(client.manifest.get("temporary_monitor_deleted", False))

    def test_interaction_cleanup_exception_does_not_skip_monitor_delete(self):
        client = WorkflowClient(self.out, {
            "interact_public_gene": ok({"scrapeId": "synthetic-browser"}),
            "interact_stop": {"status": "tool_error", "data": None},
            "interact_cleanup": RuntimeError("synthetic-cleanup-failure"),
            "monitor_create": ok({"data": {"id": "synthetic-own"}}),
            "monitor_delete": ok({"success": True}),
        })
        with patch.object(fc.time, "sleep"):
            try:
                fc.capabilities(client)
            except RuntimeError:
                pass
        self.assertIn("monitor_delete", [label for label, _, _, _ in client.calls])

    def test_polling_is_finite_and_monitor_deleted_when_status_never_finishes(self):
        client = WorkflowClient(self.out, {
            "agent_primary_audit": ok({"id": "synthetic-agent"}),
            "monitor_create": ok({"data": {"id": "synthetic-own"}}),
            "monitor_run": ok({"id": "synthetic-check"}),
            "monitor_delete": ok({"success": True}),
        })
        with patch.object(fc.time, "sleep") as sleep:
            fc.capabilities(client)
        self.assertLessEqual(sleep.call_count, 30)
        self.assertEqual(sum(label.startswith("agent_status_") for label, _, _, _ in client.calls), 12)
        self.assertEqual(sum(label.startswith("monitor_check_") for label, _, _, _ in client.calls), 18)
        self.assertEqual(client.calls[-1][1], "firecrawl_monitor_delete")


if __name__ == "__main__":
    unittest.main()
