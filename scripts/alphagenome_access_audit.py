#!/usr/bin/env python3
"""Bounded public AlphaGenome Atlas access audit, NOT variant scoring.

Fixed public URLs only; no VCF, sequence, variant, API-key or arbitrary-URL input.
Never authenticates, invokes a model, follows sign-in redirects or downloads an
entire score archive. Prefix availability is not dataset integrity or a result.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import http.client
import json
from pathlib import Path
import re
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REVISION = "aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d"
BASE = f"https://raw.githubusercontent.com/google-deepmind/alphagenome/{REVISION}"
PORTAL = "https://deepmind.google.com/science/alphagenome"
SOURCES = {
    "portal": (PORTAL + "/atlas", "catalog", (b"AlphaGenome", b"avi_scores_snvs_tabix.zip")),
    "terms": (PORTAL + "/terms", "terms", (b"AlphaGenome",)),
    "sdk_readme": (BASE + "/README.md", "documentation", (b"AlphaGenome Atlas", b"Terms")),
    "atlas_client": (BASE + "/src/alphagenome/atlas/atlas.py", "documentation", (b"class AtlasClient:", b"def scorer_metadata(")),
    "atlas_protocol": (BASE + "/src/alphagenome/protos/atlas_service.proto", "documentation", (b"GetDenseVariantScores", b"ListVariantScoresMetadata")),
    "avi_archive": (PORTAL + "/_/download/atlas/avi_scores_snvs_tabix.zip", "archive", ()),
    "splicing_archive": (PORTAL + "/_/download/atlas/combined_splicing_snvs_tabix.zip", "archive", ()),
}
ALLOWED_URLS = frozenset(s[0] for s in SOURCES.values())
SCRIPT_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
DOC_LIMIT = 2_000_000
PREFIX_SIZE = 4096


class FixedRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if newurl != req.full_url:
            # Even a login page or another fixed resource is not this artifact.
            raise urllib.error.URLError("redirect rejected; exact artifact required")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def assess(source: str, status: int, headers: dict, body: bytes) -> dict:
    if source not in SOURCES:
        raise ValueError("unknown fixed public source")
    _, kind, tokens = SOURCES[source]
    headers = {k.lower(): v for k, v in headers.items()}
    if status not in (200, 206):
        return {"state": "unavailable", "reason": "http_error"}
    length = headers.get("content-length")
    if length is not None and (not re.fullmatch(r"\d+", length) or int(length) != len(body)):
        return {"state": "unavailable", "reason": "declared_length_mismatch"}
    if kind == "archive":
        match = re.fullmatch(r"bytes 0-(\d+)/(\d+)", headers.get("content-range", ""))
        if status != 206 or not match or int(match[1]) != PREFIX_SIZE - 1 or int(match[2]) < PREFIX_SIZE or len(body) != PREFIX_SIZE:
            return {"state": "unavailable", "reason": "bounded_range_not_verified"}
        if body[:4] != b"PK\x03\x04":
            return {"state": "unavailable", "reason": "not_a_zip_prefix"}
        return {"state": "prefix_available_only", "total_bytes_reported": int(match[2]),
                "reason": "not_full_download_or_integrity_verification"}
    if status != 200 or not body or len(body) > DOC_LIMIT or not all(t in body for t in tokens):
        return {"state": "unavailable", "reason": "missing_or_invalid_document"}
    if kind == "terms":
        # A JS application shell is not a review of the complete operative terms.
        return {"state": "page_retrieved_terms_unverified", "reason": "requires_complete_terms_review"}
    if kind == "catalog":
        return {"state": "catalog_metadata_retrieved", "reason": "not_authenticated_portal_or_scores"}
    return {"state": "documentation_retrieved"}


def probe(source: str, opener) -> tuple[dict, bytes]:
    if source not in SOURCES:
        raise ValueError("unknown fixed public source")
    url, kind, _ = SOURCES[source]
    headers = {"User-Agent": "mva-public-atlas-access-audit/1.0", "Accept-Encoding": "identity"}
    if kind == "archive":
        headers["Range"] = f"bytes=0-{PREFIX_SIZE - 1}"
    request = urllib.request.Request(url, headers=headers, method="GET")
    record = {"id": source, "url": url, "retrieved_at": datetime.now(timezone.utc).isoformat(),
              "http_status": None, "kind": kind}
    body = b""
    try:
        with opener.open(request, timeout=20) as response:
            record["http_status"] = response.status
            if response.geturl() != url:
                raise urllib.error.URLError("unexpected final URL")
            limit = PREFIX_SIZE if kind == "archive" else DOC_LIMIT
            body = response.read(limit + 1)
            record.update(assess(source, response.status, dict(response.headers), body))
    except urllib.error.HTTPError as exc:
        record.update(http_status=exc.code, state="unavailable", reason="http_error")
        # Fixed public endpoint errors only; never emit an authenticated error body.
        try:
            body = exc.read(4096)
        except (urllib.error.URLError, OSError, http.client.HTTPException) as body_error:
            record["reason"] = "http_error_body_" + type(body_error).__name__
        finally:
            exc.close()
    except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
        record.update(state="unavailable", reason=type(exc).__name__)
    record["bytes_retained"] = len(body)
    record["sha256"] = hashlib.sha256(body).hexdigest()
    return record, body


def summarize(records: list[dict]) -> dict:
    if len(records) != len(SOURCES) or {r["id"] for r in records} != set(SOURCES):
        raise ValueError("missing or duplicate source observation")
    missing = [r["id"] for r in records if r["state"] == "unavailable"]
    return {
        "observed_sources": len(records), "unavailable_sources": missing,
        "archive_prefixes_available": [r["id"] for r in records if r["state"] == "prefix_available_only"],
        "atlas_scores_obtained": False, "subject_inputs_read": False,
        "hosted_inference_performed": False, "credentials_used": False,
        "operative_terms_verified": False, "clinical_exposure_margin": None,
        "phase": "unconfirmed", "ranking_changed": False,
        "interpretation": "Public access observations only. No score, zero effect, benignity, phase or drug-response result follows.",
    }


def run(output: Path, opener=None) -> dict:
    output = output.resolve()
    if not output.is_relative_to(ROOT / "results/feat009") or output == ROOT / "results/feat009":
        raise ValueError("new output directory must be under results/feat009")
    output.mkdir(parents=True, exist_ok=False)
    opener = opener or urllib.request.build_opener(FixedRedirects())
    records = []
    manifest = {"schema_version": 1, "sdk_revision": REVISION, "script_sha256": SCRIPT_SHA256,
                "requests": records, "summary": {"state": "in_progress", "completed_sources": 0}}
    manifest_path = output / "access-audit.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    for source in SOURCES:
        record, body = probe(source, opener)
        (output / (source + ".response")).write_bytes(body)
        records.append(record)
        manifest["summary"]["completed_sources"] = len(records)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    summary = summarize(records)
    manifest["summary"] = summary
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    summary = run(args.output)
    print(json.dumps(summary, indent=2))
    if summary["unavailable_sources"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
