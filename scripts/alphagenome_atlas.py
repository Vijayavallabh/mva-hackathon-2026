#!/usr/bin/env python3
"""Bounded Atlas lookups: metadata, public control, two submission-derived alleles.

Only the repository .env is read, as data (never executed). SDK/native diagnostics
are muted for the entire authenticated operation. No exception text is retained.
"""
import argparse
import contextlib
import gc
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SDK_REVISION = "aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d"
HOST = "gdmscience.googleapis.com:443"
RPC_TIMEOUT = 45
CONNECT_TIMEOUT = 20
KEY_NAME = "ALPHAGENOME_API_KEY"
CONTROL = ("chr9", 128225994, "G", "A")
SUBMITTED = (("chr15", 40209701, "T", "G"), ("chr15", 40220612, "T", "G"))
COMPOSITE = ("AVI_SCORE", "AVI_SCORE_FEATURE_IMPORTANCE")
MOLECULAR = ("SPLICE_SITES", "SPLICE_SITE_USAGE", "SPLICE_JUNCTIONS", "RNA_SEQ",
             "ATAC", "DNASE", "CHIP_TF", "CHIP_HISTONE", "CAGE", "PROCAP",
             "POLYADENYLATION", "CONTACT_MAPS")
FEATURES = frozenset(("MERGED_SPLICING", "MAX_ABS_RNA_SEQ", "MAX_ABS_ATAC",
    "MAX_ABS_DNASE", "MAX_ABS_CHIP_TF", "MAX_ABS_CHIP_HISTONE", "MAX_ABS_CAGE",
    "MAX_ABS_PROCAP", "MAX_ABS_POLYADENYLATION", "MAX_ABS_CONTACT_MAPS",
    "ALPHAMISSENSE", "CACTUS_241_WAY", "PROTEIN_TERMINATION", "START_LOST",
    "STOP_LOST", "PHASTCONS_470_WAY", "IS_INSERTION", "IS_DELETION"))
REPORT_SHA256 = "6685a1f25b7e8da6e69bab57bf5bdb855dce0e22095d80c9f1a02ea80d37ed72"


class GateError(Exception):
    """Local policy/schema failure; deliberately carries no diagnostic text."""
    def __init__(self, code="unspecified"):
        self.code = code if code in {"score_set", "matrix_shape", "variant_identity",
            "quantile_shape_range", "missing_composite", "composite_shape_finite",
            "feature_names", "composite_quantile", "unspecified"} else "unspecified"
        super().__init__()


def load_key(path):
    """Parse exactly one literal key; forbid symlinks, broad permissions, expansion."""
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as handle:
        info = os.fstat(handle.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                or stat.S_IMODE(info.st_mode) & 0o077 or info.st_size > 65536):
            raise GateError()
        body = handle.read(65537)
    if len(body) > 65536:
        raise GateError()
    keys = []
    for line in body.decode("utf-8").splitlines():
        line = line.strip()
        if line.startswith("export "):
            line = line[7:].lstrip()
        if not re.match(r"ALPHAGENOME_API_KEY(?:\s|=|$)", line):
            continue
        match = re.fullmatch(
            r"ALPHAGENOME_API_KEY\s*=\s*(?:'([A-Za-z0-9_-]{20,200})'|"
            r'"([A-Za-z0-9_-]{20,200})"|([A-Za-z0-9_-]{20,200}))\s*(?:#.*)?', line)
        if not match:
            raise GateError()
        keys.append(next(v for v in match.groups() if v is not None))
    if len(keys) != 1:
        raise GateError()
    return keys[0]


@contextlib.contextmanager
def silence_diagnostics():
    """Single-threaded CLI only: cover Python streams and native fd writes."""
    sys.stdout.flush()
    sys.stderr.flush()
    saved = [os.dup(1), os.dup(2)]
    with open(os.devnull, "w") as sink:
        try:
            os.dup2(sink.fileno(), 1)
            os.dup2(sink.fileno(), 2)
            with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
                yield
        finally:
            for original, duplicate in zip((1, 2), saved):
                os.dup2(duplicate, original)
                os.close(duplicate)


class DeadlineStub:
    """The SDK's create timeout is not an RPC deadline; impose one per call."""
    def __init__(self, stub):
        self.stub = stub

    def ListVariantScoresMetadata(self, request, metadata=None):
        return self.stub.ListVariantScoresMetadata(
            request, metadata=metadata, timeout=RPC_TIMEOUT)

    def GetDenseVariantScores(self, request, metadata=None):
        v = request.variant
        # Recheck the actual outgoing proto, not just CLI scope.
        if (v.chromosome, v.position, v.reference_bases, v.alternate_bases) not in (CONTROL, *SUBMITTED):
            raise GateError()
        return self.stub.GetDenseVariantScores(request, metadata=metadata, timeout=RPC_TIMEOUT)


def safe_error(error):
    """Allowlisted type/code only: never details(), repr(), args or traceback."""
    import grpc
    if isinstance(error, GateError):
        return {"kind": "local_gate_failure", "gate": error.code}
    cause = error
    for _ in range(4):
        if isinstance(cause, grpc.RpcError):
            status = cause.code()
            if isinstance(status, grpc.StatusCode):
                return {"kind": "rpc_failure", "grpc_status": status.name}
        cause = cause.__cause__
        if cause is None:
            break
    for cls, label in ((GateError, "local_gate_failure"),
                       (FileNotFoundError, "key_file_missing"),
                       (PermissionError, "permission_failure"),
                       (TimeoutError, "timeout"),
                       (grpc.FutureTimeoutError, "connection_timeout")):
        if isinstance(error, cls):
            return {"kind": label}
    return {"kind": "unclassified_failure"}


def metadata_payload(metadata):
    if not metadata:
        raise GateError()
    result = {}
    for name, item in metadata.items():
        if name != item.name or not re.fullmatch(r"[A-Z][A-Z0-9_]{0,100}", name):
            raise GateError()
        result[name] = {"is_signed": bool(item.is_signed),
                        "track_columns": list(item.track_metadata.columns),
                        "tracks": json.loads(item.track_metadata.to_json(orient="records"))}
    return result


def calibration(q):
    if q is None:
        return {"api_cdf_quantile": None, "phred_display": None}
    if not math.isfinite(q) or not 0 <= q <= 1:
        raise GateError()
    complement = 1 - q
    return {"api_cdf_quantile": q, "tail_fraction_unclipped": complement,
            "display_tail_floor": 1e-7, "display_clipped": complement < 1e-7,
            "phred_display": -10 * math.log10(max(1e-7, complement))}


def serialize_scores(scores, requested, variant, metadata=None):
    """Preserve metadata, matrix axes, nulls and all returned tracks; never flatten."""
    import numpy as np
    if not scores or not set(scores) <= set(requested):
        raise GateError("score_set")
    output = {}
    for name, item in scores.items():
        matrix = np.asarray(item.X)
        if matrix.ndim != 2 or matrix.shape != (len(item.obs), len(item.var)):
            raise GateError("matrix_shape")
        if "variant" not in item.obs or any(v != variant for v in item.obs["variant"]):
            raise GateError("variant_identity")
        obs = item.obs.drop(columns="variant").copy()
        obs["variant"] = str(variant)
        finite = np.isfinite(matrix)
        values = [[float(v) if math.isfinite(float(v)) else None for v in row] for row in matrix]
        quantiles = None
        signed = None if metadata is None else metadata[name]["is_signed"]
        semantics = "CDF" if name == "AVI_SCORE" else (
            "signed calibration: 2*CDF-1" if signed else "unsigned calibration: CDF"
        ) if signed is not None else "scorer_specific; not AVI CDF"
        if "quantiles" in item.layers:
            q = np.asarray(item.layers["quantiles"])
            # Only composite AVI is documented as a CDF. Molecular signed
            # calibration can be [-1,1]; retain without an AVI PHRED conversion.
            lower = -1 if signed and name != "AVI_SCORE" else 0
            if q.shape != matrix.shape or ((name == "AVI_SCORE" or signed is not None) and
                    np.any(np.isfinite(q) & ((q < lower) | (q > 1)))):
                raise GateError("quantile_shape_range")
            quantiles = [[float(v) if math.isfinite(float(v)) else None for v in row] for row in q]
        output[name] = {"shape": list(matrix.shape), "values": values,
                        "api_quantiles": quantiles, "finite_count": int(finite.sum()),
                        "calibration_semantics": semantics, "is_signed_metadata": signed,
                        "nonfinite_count": int((~finite).sum()),
                        "observations": json.loads(obs.to_json(orient="records")),
                        "tracks": json.loads(item.var.to_json(orient="records"))}
    return {"scorers": output, "missing_scorers": sorted(set(requested) - set(scores))}


def composite_summary(serialized):
    if serialized["missing_scorers"]:
        raise GateError("missing_composite")
    s = serialized["scorers"]
    a, f = s["AVI_SCORE"], s["AVI_SCORE_FEATURE_IMPORTANCE"]
    if a["shape"] != [1, 1] or f["shape"] != [1, 18] or a["nonfinite_count"] or f["nonfinite_count"]:
        raise GateError("composite_shape_finite")
    names = [v.get("name") for v in f["tracks"]]
    if len(set(names)) != 18 or set(names) != FEATURES:
        raise GateError("feature_names")
    raw = a["values"][0][0]
    q = a["api_quantiles"]
    if q is not None and q[0][0] is None:
        raise GateError("composite_quantile")
    return {"raw_avi": raw, **calibration(None if q is None else q[0][0]),
            "attributions": dict(zip(names, f["values"][0])),
            "raw_minus_sum_attributions": raw - math.fsum(f["values"][0]),
            "attribution_baseline": "unknown; expected-gradients approximation, not exact additivity"}


def submitted_preflight():
    from track2_evidence import check_track1
    from track1_submission import DEFAULT_REFERENCE, DEFAULT_SAMTOOLS
    report = ROOT / "notes/track2-report.md"
    if hashlib.sha256(report.read_bytes()).hexdigest() != REPORT_SHA256:
        raise GateError()
    for chrom, position, ref, _ in SUBMITTED:
        fetched = subprocess.run([str(DEFAULT_SAMTOOLS), "faidx", str(DEFAULT_REFERENCE),
            f"{chrom.removeprefix('chr')}:{position}-{position}"], capture_output=True,
            text=True, timeout=15, check=True)
        if "".join(fetched.stdout.splitlines()[1:]).upper() != ref:
            raise GateError()
    return {"source": "notes/track2-report.md", "source_sha256": REPORT_SHA256,
            "track1": check_track1(), "assembly": "GRCh38", "variants": SUBMITTED,
            "trans_phase": "unconfirmed", "source_vcf_read": False,
            "local_reference_ref_match": True,
            "reference": str(DEFAULT_REFERENCE.relative_to(ROOT))}


def authenticated_lookup(key_path, mode):
    """All dependencies/client/channel destroyed under muted diagnostics."""
    os.environ["GRPC_VERBOSITY"] = "NONE"
    os.environ.pop("GRPC_TRACE", None)
    result = {"state": "started", "completed_steps": []}
    key = None
    client = None
    with silence_diagnostics():
        try:
            import grpc
            from alphagenome.atlas import atlas
            from alphagenome.data import genome
            from alphagenome.protos import atlas_service_pb2_grpc
            direct = json.loads(importlib.metadata.distribution("alphagenome").read_text("direct_url.json"))
            if direct.get("vcs_info", {}).get("commit_id") != SDK_REVISION:
                raise GateError()
            if mode in ("submitted-pair", "submitted-composites"):
                result["preflight"] = submitted_preflight()
            key = load_key(key_path)
            with grpc.secure_channel(
                HOST, grpc.ssl_channel_credentials(),
                options=(("grpc.enable_retries", 0),
                         ("grpc.max_receive_message_length", 64 * 1024 * 1024)),
            ) as channel:
                grpc.channel_ready_future(channel).result(timeout=CONNECT_TIMEOUT)
                client = atlas.AtlasClient(
                    DeadlineStub(atlas_service_pb2_grpc.AtlasServiceStub(channel)),
                    metadata=[("x-goog-api-key", key)])
                result["scorers"] = metadata_payload(client.scorer_metadata())
                result["completed_steps"].append("metadata")
                if mode != "metadata":
                    needed = COMPOSITE + (MOLECULAR if mode == "submitted-pair" else ())
                    if not set(needed) <= set(result["scorers"]):
                        raise GateError()
                    variant = genome.Variant(*CONTROL)
                    result["active_step"] = "public_control"
                    control = serialize_scores(client.query_variant(variant,
                        requested_scorers=COMPOSITE), COMPOSITE, variant, result["scorers"])
                    result["control"] = {"variant": CONTROL, "output": control,
                                         "summary": composite_summary(control)}
                    result["completed_steps"].append("control")
                if mode in ("submitted-pair", "submitted-composites"):
                    result["candidates"] = []
                    for definition in SUBMITTED:
                        variant = genome.Variant(*definition)
                        result["active_step"] = f"{variant}:composite"
                        composite = serialize_scores(client.query_variant(variant,
                            requested_scorers=COMPOSITE), COMPOSITE, variant, result["scorers"])
                        candidate = {"variant": definition, "composite": composite,
                                     "summary": composite_summary(composite)}
                        result["candidates"].append(candidate)
                        if mode == "submitted-composites":
                            result["completed_steps"].append(str(variant))
                            continue
                        result["active_step"] = f"{variant}:molecular"
                        # Predeclared all-track, all-gene set. Interpret BUB1B rows
                        # separately offline; neighbouring-gene effects remain labelled.
                        candidate["molecular"] = serialize_scores(client.query_variant(
                            variant, requested_scorers=MOLECULAR), MOLECULAR, variant, result["scorers"])
                        result["completed_steps"].append(str(variant))
                # Guard even against an unexpected server credential echo.
                if key in json.dumps(result, allow_nan=False):
                    raise GateError()
                del client
            result["state"] = "metadata_retrieved" if mode == "metadata" else "lookup_retrieved"
        except Exception as error:
            result.update(state="unavailable", error=safe_error(error))
        finally:
            # Exception tracebacks can keep an SDK client alive. Finalizers must
            # run before restoring Python/native streams on failure as well.
            client = None
            gc.collect()
        # Includes partial results after a failure; never return a secret echo.
        if key is not None and key in json.dumps(result, allow_nan=False):
            return {"state": "unavailable", "error": {"kind": "credential_echo_blocked"}}
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--mode", choices=("metadata", "control", "submitted-pair", "submitted-composites"), default="metadata")
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / "results/feat009") or output.exists():
        print("Refusing output: use a new directory under results/feat009.")
        return 2
    output.mkdir(parents=True)
    manifest = {"created_at": datetime.now(timezone.utc).isoformat(),
                "sdk_revision": SDK_REVISION, "atlas_dataset_version": None,
                "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "host": HOST, "mode": args.mode, "organism": "HOMO_SAPIENS",
                "request_scope": {"control": CONTROL if args.mode != "metadata" else None,
                                  "submitted_variants": SUBMITTED if args.mode.startswith("submitted-") else [],
                                  "composite_scorers": COMPOSITE if args.mode != "metadata" else [],
                                  "molecular_scorers": MOLECULAR if args.mode == "submitted-pair" else [],
                                  "filters": "none; all returned genes/tracks retained",
                                  "raw_subject_input": False, "on_demand_inference": False},
                "rpc_timeout_seconds": RPC_TIMEOUT, "connect_timeout_seconds": CONNECT_TIMEOUT,
                "state": "started"}
    path = output / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    result = authenticated_lookup(ROOT / ".env", args.mode)
    if "scorers" in result:
        payload = json.dumps(result.pop("scorers"), indent=2, allow_nan=False) + "\n"
        (output / "scorers.json").write_text(payload)
        manifest["scorers_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
        result["scorer_count"] = len(json.loads(payload))
    if "control" in result or "candidates" in result:
        payload = json.dumps({k: result.pop(k) for k in ("control", "candidates") if k in result}, indent=2, allow_nan=False) + "\n"
        (output / "scores.json").write_text(payload)
        manifest["scores_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    manifest.update(result, completed_at=datetime.now(timezone.utc).isoformat())
    path.write_text(json.dumps(manifest, indent=2, allow_nan=False) + "\n")
    print(json.dumps({k: manifest[k] for k in ("state", "error", "scorer_count") if k in manifest}))
    return 0 if result["state"] in ("metadata_retrieved", "lookup_retrieved") else 2


if __name__ == "__main__":
    raise SystemExit(main())
