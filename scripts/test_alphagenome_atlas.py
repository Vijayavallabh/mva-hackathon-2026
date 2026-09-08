#!/usr/bin/env python3
"""Offline synthetic tests. No real .env, subject inputs or network calls."""
import contextlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

import numpy as np
import pandas as pd
import alphagenome_atlas as a

CANARY = "synthetic_secret_canary_1234567890"


def frame(matrix, names, variant="control"):
    return SimpleNamespace(X=np.array(matrix, dtype=float),
        obs=pd.DataFrame({"variant": [variant] * len(matrix)}),
        var=pd.DataFrame({"name": names}), layers={})


class SyntheticClient:
    def __init__(self, *args, metadata):
        self.key = metadata[0][1]
        self.query_count = 0

    def scorer_metadata(self):
        return {name: SimpleNamespace(name=name, is_signed=False,
            track_metadata=pd.DataFrame({"name": [name]}))
            for name in a.COMPOSITE + a.MOLECULAR}

    def query_variant(self, variant, requested_scorers):
        self.query_count += 1
        if self.query_count == 3:
            raise TimeoutError(CANARY)
        return {"AVI_SCORE": frame([[3.0]], ["AVI_SCORE"], variant),
            "AVI_SCORE_FEATURE_IMPORTANCE": frame(
                [list(range(18))], sorted(a.FEATURES), variant)}


def synthetic_lookup(client_type, mode="metadata"):
    """Exercise orchestration with no credential file, reference read or transport."""
    import grpc
    from alphagenome.atlas import atlas
    from alphagenome.protos import atlas_service_pb2_grpc
    ready = SimpleNamespace(result=lambda timeout: None)
    with mock.patch.object(a, "load_key", return_value=CANARY), \
            mock.patch.object(a, "submitted_preflight", return_value={"synthetic": True}), \
            mock.patch.object(grpc, "secure_channel", return_value=contextlib.nullcontext(object())), \
            mock.patch.object(grpc, "channel_ready_future", return_value=ready), \
            mock.patch.object(atlas_service_pb2_grpc, "AtlasServiceStub", return_value=object()), \
            mock.patch.object(atlas, "AtlasClient", client_type):
        return a.authenticated_lookup(Path("synthetic-key-not-read"), mode)


class Tests(unittest.TestCase):
    def keyfile(self, body, mode=0o600):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / ".env"
        path.write_text(body)
        path.chmod(mode)
        return path

    def test_literal_formats(self):
        for value in (CANARY, repr(CANARY), '"' + CANARY + '"'):
            p = self.keyfile("UNRELATED=do_not_execute\nexport ALPHAGENOME_API_KEY = " + value + " # test\n")
            self.assertEqual(a.load_key(p), CANARY)

    def test_key_rejections(self):
        for value in ("", "short", "$(unsafe)", '"${SECRET}"', '"unterminated', "has spaces"):
            with self.assertRaises(a.GateError):
                a.load_key(self.keyfile("ALPHAGENOME_API_KEY=" + value))

    def test_duplicate(self):
        with self.assertRaises(a.GateError):
            a.load_key(self.keyfile(("ALPHAGENOME_API_KEY=" + CANARY + "\n") * 2))

    def test_missing(self):
        with self.assertRaises(a.GateError):
            a.load_key(self.keyfile("UNRELATED=value"))

    def test_permissions(self):
        for mode in (0o644, 0o640, 0o604):
            with self.assertRaises(a.GateError):
                a.load_key(self.keyfile("ALPHAGENOME_API_KEY=" + CANARY, mode))

    def test_symlink(self):
        p = self.keyfile("ALPHAGENOME_API_KEY=" + CANARY)
        link = p.parent / "link"
        link.symlink_to(p)
        with self.assertRaises(OSError):
            a.load_key(link)

    def test_oversized(self):
        with self.assertRaises(a.GateError):
            a.load_key(self.keyfile("x" * 65537))

    def test_canary_diagnostics(self):
        code = """import os,sys
sys.path.insert(0, 'scripts')
import alphagenome_atlas as a
with a.silence_diagnostics():
    print('synthetic_secret_canary_1234567890')
    print('synthetic_secret_canary_1234567890',file=sys.stderr)
    os.write(1,b'synthetic_secret_canary_1234567890')
    os.write(2,b'synthetic_secret_canary_1234567890')
print('safe')
"""
        r = subprocess.run([sys.executable, "-c", code], cwd=a.ROOT, capture_output=True, text=True, check=True)
        self.assertEqual(r.stdout.strip(), "safe")
        self.assertEqual(r.stderr, "")

    def test_error_redaction(self):
        self.assertNotIn(CANARY, json.dumps(a.safe_error(ValueError(CANARY))))

    def test_authenticated_error_redaction(self):
        class FailureClient(SyntheticClient):
            def scorer_metadata(self):
                raise ValueError(self.key)

        result = synthetic_lookup(FailureClient)
        self.assertEqual(result["state"], "unavailable")
        self.assertNotIn(CANARY, json.dumps(result))
        self.assertEqual(result["completed_steps"], [])

    def test_composite_only_scope(self):
        calls = []
        class CompositeClient(SyntheticClient):
            def query_variant(self, variant, requested_scorers):
                calls.append((str(variant), requested_scorers))
                self.query_count = 0
                return super().query_variant(variant, requested_scorers)
        result = synthetic_lookup(CompositeClient, "submitted-composites")
        self.assertEqual(result["state"], "lookup_retrieved")
        self.assertEqual(len(result["candidates"]), 2)
        self.assertEqual(len(calls), 3)
        self.assertTrue(all(s == a.COMPOSITE for _, s in calls))
        self.assertTrue(all("molecular" not in c for c in result["candidates"]))

    def test_control_failure_stops_candidates(self):
        calls = []
        class WrongControlClient(SyntheticClient):
            def query_variant(self, variant, requested_scorers):
                calls.append(str(variant))
                return {"AVI_SCORE": frame([[1]], ["AVI_SCORE"], "wrong")}
        result = synthetic_lookup(WrongControlClient, "submitted-composites")
        self.assertEqual(result["state"], "unavailable")
        self.assertEqual(len(calls), 1)
        self.assertNotIn("candidates", result)

    def test_authenticated_server_echo_blocked(self):
        class EchoClient(SyntheticClient):
            def scorer_metadata(self):
                metadata = super().scorer_metadata()
                metadata["AVI_SCORE"].track_metadata["name"] = self.key
                return metadata

        result = synthetic_lookup(EchoClient)
        self.assertEqual(result["state"], "unavailable")
        self.assertEqual(result["error"]["kind"], "credential_echo_blocked")
        self.assertNotIn(CANARY, json.dumps(result))

    def test_failed_client_finalizer_diagnostics_muted(self):
        code = """import gc,json,os,sys
sys.path.insert(0, 'scripts')
from test_alphagenome_atlas import SyntheticClient, synthetic_lookup
class DiagnosticClient(SyntheticClient):
    def scorer_metadata(self):
        raise TimeoutError(self.key)
    def __del__(self):
        print(self.key)
        print(self.key, file=sys.stderr)
        os.write(1, self.key.encode())
        os.write(2, self.key.encode())
result = synthetic_lookup(DiagnosticClient)
gc.collect()
print(json.dumps({'state': result['state']}))
"""
        process = subprocess.run([sys.executable, "-c", code], cwd=a.ROOT,
            capture_output=True, text=True, check=True)
        self.assertNotIn(CANARY, process.stdout + process.stderr)
        self.assertEqual(json.loads(process.stdout), {"state": "unavailable"})
        self.assertEqual(process.stderr, "")

    def test_molecular_failure_preserves_successful_composite(self):
        result = synthetic_lookup(SyntheticClient, "submitted-pair")
        self.assertEqual(result["state"], "unavailable")
        self.assertEqual(result["error"]["kind"], "timeout")
        self.assertEqual(result["completed_steps"], ["metadata", "control"])
        self.assertTrue(result["active_step"].endswith(":molecular"))
        self.assertEqual(len(result["candidates"]), 1)
        candidate = result["candidates"][0]
        self.assertEqual(candidate["variant"], a.SUBMITTED[0])
        self.assertEqual(candidate["summary"]["raw_avi"], 3.0)
        self.assertEqual(len(candidate["summary"]["attributions"]), 18)
        self.assertNotIn("molecular", candidate)
        self.assertNotIn(CANARY, json.dumps(result))

    def test_rpc_deadline(self):
        stub = mock.Mock()
        bounded = a.DeadlineStub(stub)
        bounded.ListVariantScoresMetadata("request", metadata=[("key", CANARY)])
        self.assertEqual(stub.ListVariantScoresMetadata.call_args.kwargs["timeout"], 45)

    def test_variant_allowlist(self):
        from alphagenome.data import genome
        stub = mock.Mock()
        bounded = a.DeadlineStub(stub)
        for definition in (a.CONTROL, *a.SUBMITTED):
            bounded.GetDenseVariantScores(SimpleNamespace(variant=genome.Variant(*definition).to_proto()))
        self.assertEqual(stub.GetDenseVariantScores.call_count, 3)
        self.assertEqual(stub.GetDenseVariantScores.call_args.kwargs["timeout"], 45)
        with self.assertRaises(a.GateError):
            bounded.GetDenseVariantScores(SimpleNamespace(variant=genome.Variant("chr1", 1, "A", "G").to_proto()))
        self.assertEqual(stub.GetDenseVariantScores.call_count, 3)

    def test_quantile_semantics(self):
        self.assertAlmostEqual(a.calibration(0.99)["phred_display"], 20)
        self.assertTrue(a.calibration(1)["display_clipped"])
        self.assertEqual(a.calibration(1)["tail_fraction_unclipped"], 0)
        self.assertEqual(a.calibration(0)["phred_display"], 0)
        self.assertIsNone(a.calibration(None)["phred_display"])

    def test_bad_quantiles(self):
        for q in (-0.1, 1.1, math.nan, math.inf):
            with self.assertRaises(a.GateError):
                a.calibration(q)

    def test_signed_molecular_quantile_is_not_avi_cdf(self):
        score = frame([[1.0]], ["track"])
        score.layers["quantiles"] = np.array([[-0.97]])
        result = a.serialize_scores({"RNA_SEQ": score}, ["RNA_SEQ"], "control",
            {"RNA_SEQ": {"is_signed": True}})["scorers"]["RNA_SEQ"]
        self.assertEqual(result["api_quantiles"], [[-0.97]])
        self.assertEqual(result["calibration_semantics"], "signed calibration: 2*CDF-1")
        self.assertNotIn("phred_display", result)

    def test_unsigned_molecular_negative_quantile_rejected(self):
        score = frame([[1.0]], ["track"])
        score.layers["quantiles"] = np.array([[-0.97]])
        with self.assertRaises(a.GateError):
            a.serialize_scores({"RNA_SEQ": score}, ["RNA_SEQ"], "control",
                {"RNA_SEQ": {"is_signed": False}})

    def test_avi_quantile_remains_cdf_even_with_signed_metadata(self):
        for value in (-0.97, 1.1):
            score = frame([[1.0]], ["AVI_SCORE"])
            score.layers["quantiles"] = np.array([[value]])
            with self.subTest(value=value), self.assertRaises(a.GateError):
                a.serialize_scores({"AVI_SCORE": score}, ["AVI_SCORE"], "control",
                    {"AVI_SCORE": {"is_signed": True}})

    def composite(self, names=None):
        return a.serialize_scores({"AVI_SCORE": frame([[3.0]], ["AVI_SCORE"]),
            "AVI_SCORE_FEATURE_IMPORTANCE": frame([list(range(18))], names or sorted(a.FEATURES))}, a.COMPOSITE, "control")

    def test_name_binding_not_enum_order(self):
        names = list(reversed(sorted(a.FEATURES)))
        summary = a.composite_summary(self.composite(names))
        self.assertEqual(summary["attributions"][names[0]], 0)
        self.assertEqual(summary["raw_minus_sum_attributions"], 3 - sum(range(18)))

    def test_duplicate_features(self):
        with self.assertRaises(a.GateError):
            a.composite_summary(self.composite(["ALPHAMISSENSE"] * 18))

    def test_unknown_features(self):
        with self.assertRaises(a.GateError):
            a.composite_summary(self.composite(["UNKNOWN"] + sorted(a.FEATURES)[1:]))

    def test_empty_scores(self):
        with self.assertRaises(a.GateError):
            a.serialize_scores({}, a.COMPOSITE, "control")

    def test_wrong_identity(self):
        with self.assertRaises(a.GateError):
            a.serialize_scores({"RNA_SEQ": frame([[1]], ["track"], "wrong")}, ["RNA_SEQ"], "control")

    def test_missing_identity(self):
        f = frame([[1]], ["track"])
        f.obs = pd.DataFrame(index=[0])
        with self.assertRaises(a.GateError):
            a.serialize_scores({"RNA_SEQ": f}, ["RNA_SEQ"], "control")

    def test_nonfinite_preserved(self):
        r = a.serialize_scores({"RNA_SEQ": frame([[math.nan, math.inf, 0]], ["a", "b", "c"])}, ["RNA_SEQ", "ATAC"], "control")
        self.assertEqual(r["scorers"]["RNA_SEQ"]["values"], [[None, None, 0]])
        self.assertEqual(r["scorers"]["RNA_SEQ"]["nonfinite_count"], 2)
        self.assertEqual(r["missing_scorers"], ["ATAC"])

    def test_shape_rejected(self):
        f = frame([[1]], ["track"])
        f.X = np.array([1])
        with self.assertRaises(a.GateError):
            a.serialize_scores({"RNA_SEQ": f}, ["RNA_SEQ"], "control")

    def test_unknown_scorer(self):
        with self.assertRaises(a.GateError):
            a.serialize_scores({"X": frame([[1]], ["track"])}, ["RNA_SEQ"], "control")

    def test_metadata_empty(self):
        with self.assertRaises(a.GateError):
            a.metadata_payload({})


if __name__ == "__main__":
    unittest.main()
