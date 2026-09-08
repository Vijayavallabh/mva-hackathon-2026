#!/usr/bin/env python3
"""Offline Track 2 evidence checks and reproducible research-package preparation.

Optional `sources` downloads public citation metadata and official pages only.
No raw-data input, medical recommendation engine, portal client or upload function.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from track2_exposure import audit as audit_exposure

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
SOURCES = ROOT / "notes/track2-sources.json"
CANDIDATES = ROOT / "notes/track2-candidates.json"
COPY_INPUTS = {
    "jvv7_track2_report_v2.md": "notes/track2-report.md",
    "jvv7_track2_pitch_v2.md": "notes/track2-pitch.md",
    "validation-plan.md": "notes/track2-validation.md",
    "sources.json": "notes/track2-sources.json",
    "candidates.json": "notes/track2-candidates.json",
    "scientific-exposure-review.md": "notes/track2-final-review.md",
    "exposure.json": "notes/track2-exposure.json",
}
INPUT_PATHS = set(COPY_INPUTS.values()) | {"notes/track2-plan.md", "notes/track2-search.md", "notes/track2-devils-advocate.md",
    "scripts/track2_evidence.py", "scripts/track2_public_search.py", "scripts/track2_review_search.py", "scripts/track2_exposure.py"}
PACKAGE_FILES = set(COPY_INPUTS) | {"candidate-evidence.md", "sensitivity.json", "exposure-audit.json"}
DECISIONS = {"conditional_screen", "benchmark_only", "deprioritize", "exclude"}
SOURCE_KINDS = {"primary", "correction", "regulatory", "registry", "competition", "database"}
EVIDENCE_LEVELS = {"contradictory_cell_evidence", "cross_disease_hypothesis", "mechanistic_tool", "other_allele_animal", "other_compound_or_cancer", "other_intervention_animal", "pediatric_cancer_preclinical", "same_tumour_clinical_not_genotype"}
APPROVAL_STATES = {"combination_not_verified", "not_current_in_reviewed_jurisdiction", "not_verified", "verified_other_indication"}
PUBLIC_HOSTS = {"www.nature.com", "pubmed.ncbi.nlm.nih.gov", "pmc.ncbi.nlm.nih.gov", "pubchem.ncbi.nlm.nih.gov", "aacrjournals.org", "www.jci.org", "www.sciencedirect.com", "ascopubs.org", "dailymed.nlm.nih.gov", "www.ema.europa.eu", "clinicaltrials.gov", "huggingface.co", "api.crossref.org"}
TRACK1 = {
    "jvv7_genomewide_mva_v4.csv": "a1f9315e223a07914589ce6884a66702b80e587ec5b7ad67f2ca1213f6caa225",
    "jvv7_genomewide_mva_v4_report.md": "f36bacbc506d5a717ee7a55f174fed3f376ed7beacd83d11091e57d319d0d68b",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def checked_url(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    require(p.scheme == "https" and p.hostname in PUBLIC_HOSTS and not p.username and not p.password
            and p.port in (None, 443) and not p.fragment, "source URL is not an allowed public HTTPS endpoint")
    return url


def validate(sources: dict, candidates: dict) -> dict:
    require(isinstance(sources, dict) and isinstance(candidates, dict), "ledger must be an object")
    require(isinstance(sources.get("sources"), list) and isinstance(candidates.get("candidates"), list), "ledger entries must be arrays")
    require(sources.get("schema_version") == candidates.get("schema_version") == 1, "unsupported schema")
    require(candidates.get("phase") == "unconfirmed", "phase must remain unconfirmed in this research package")
    require(candidates.get("clinical_use") == "research_only", "research-only boundary missing")
    registry = {}
    dois = set()
    for s in sources["sources"]:
        require(re.fullmatch(r"[a-z][a-z0-9_]*", s["id"]) is not None and s["id"] not in registry, "invalid or duplicate source ID")
        for key in ["title", "url", "kind", "model", "reading", "claim", "limit"]:
            require(isinstance(s.get(key), str) and bool(s[key].strip()), f"missing source {key}")
        require(s["kind"] in SOURCE_KINDS, "unknown source kind")
        checked_url(s["url"])
        if "doi" in s:
            doi = s["doi"].lower()
            require(re.fullmatch(r"10\.\d{4,9}/[^\s]+", doi) is not None and doi not in dois, "invalid or duplicate DOI")
            dois.add(doi)
        if s["kind"] == "database":
            require(type(s.get("expected_cid")) is int and s["expected_cid"] > 0
                    and isinstance(s.get("expected_molecular_weight"), str), "chemical database identity missing")
        registry[s["id"]] = s
    require(bool(registry), "empty source ledger")
    seen = set()
    for c in candidates["candidates"]:
        require(re.fullmatch(r"[a-z][a-z0-9_]*", c["id"]) is not None and c["id"] not in seen, "invalid or duplicate candidate ID")
        seen.add(c["id"])
        for key in ["name", "role", "approval", "jurisdiction", "approved_use", "target_direction", "bridge", "evidence_level", "normal_tissue_risk", "exposure_gap", "falsifier", "next_test"]:
            require(isinstance(c.get(key), str) and bool(c[key].strip()), f"missing candidate {key}")
        require(c.get("decision") in DECISIONS, "invalid research decision")
        require(c["evidence_level"] in EVIDENCE_LEVELS, "unknown evidence rationale class")
        require(c["approval"] in APPROVAL_STATES, "unknown approval state")
        require(c.get("direct_pair_evidence") is False, "no direct-pair intervention experiment is established")
        require(c.get("clinical_efficacy") == "unestablished", "clinical efficacy must not be inferred")
        for kind in ["support", "counterevidence"]:
            require(isinstance(c.get(kind), list) and bool(c[kind]), f"missing {kind}")
            require(len(c[kind]) == len(set(c[kind])) and all(s in registry for s in c[kind]), "unknown or duplicate citation")
        approval_source = c.get("approval_source")
        if c["approval"] == "verified_other_indication":
            require(approval_source in registry and registry[approval_source]["kind"] == "regulatory", "approval needs a regulatory source")
        else:
            require(c["decision"] == "exclude", "unverified/non-current approval cannot enter the shortlist")
        if approval_source is not None:
            require(approval_source in registry and registry[approval_source]["kind"] == "regulatory", "invalid regulatory citation")
        require("clinical_exposure_margin" in c, "explicit exposure margin field required, even when unknown")
        margin = c["clinical_exposure_margin"]
        require(margin is None, "no clinical exposure margin has been measured; do not manufacture one")
    require(bool(seen), "empty candidate ledger")
    return {"sources": len(registry), "candidates": len(seen), "decisions": {d: sum(c["decision"] == d for c in candidates["candidates"]) for d in sorted(DECISIONS)},
            "direct_pair_intervention_evidence": 0, "clinical_efficacy_established": 0, "phase": "unconfirmed"}


def load_ledgers() -> tuple[dict, dict]:
    sources, candidates = json.loads(SOURCES.read_text()), json.loads(CANDIDATES.read_text())
    validate(sources, candidates)
    return sources, candidates


def sensitivities(sources: dict, candidates: dict) -> dict:
    """Evidence ablation is a stress test of rationale, not a numerical drug rank."""
    validate(sources, candidates)
    chosen = [c for c in candidates["candidates"] if c["decision"] == "conditional_screen"]
    return {
        "baseline_conditional_screens": [c["id"] for c in chosen],
        "require_direct_pair_intervention_evidence": [c["id"] for c in chosen if c["direct_pair_evidence"]],
        "require_measured_clinical_exposure_margin": [c["id"] for c in chosen if c["clinical_exposure_margin"] is not None],
        "remove_other_allele_animal_support": [c["id"] for c in chosen if c["evidence_level"] != "other_allele_animal"],
        "remove_other_compound_or_cancer_support": [c["id"] for c in chosen if c["evidence_level"] != "other_compound_or_cancer"],
        "interpretation": "Conditional research prioritization depends on indirect evidence. Remaining entries are not validated drugs or independent replications.",
    }


def normalize_title(title: str) -> str:
    s = unicodedata.normalize("NFKD", html.unescape(re.sub(r"<[^>]*>", "", title))).lower()
    return "".join(c for c in s if c.isalnum())


def check_metadata(source: dict, obj: dict) -> dict:
    require(isinstance(obj, dict) and isinstance(obj.get("message"), dict), "invalid citation metadata envelope")
    m = obj.get("message", {})
    require(isinstance(m.get("DOI"), str) and m["DOI"].lower() == source["doi"].lower(), "DOI mismatch")
    titles = m.get("title", [])
    require(isinstance(titles, list) and bool(titles) and all(isinstance(t, str) and t.strip() for t in titles), "citation metadata has no valid title")
    require(isinstance(m.get("subtitle", []), list) and all(isinstance(t, str) for t in m.get("subtitle", [])), "invalid citation subtitle")
    require(isinstance(m.get("author", []), list) and all(isinstance(a, dict) for a in m.get("author", [])), "invalid citation authors")
    expected, actual = normalize_title(source["title"]), normalize_title(titles[0])
    # Crossref sometimes separates the main title and subtitle.
    joined = normalize_title(" ".join(titles + m.get("subtitle", [])))
    matched = expected == actual or expected == joined
    return {"doi": m["DOI"], "title": titles[0], "subtitle": m.get("subtitle", []), "title_matches": matched,
            "authors": [{"given": a.get("given", ""), "family": a.get("family", "")} for a in m.get("author", [])],
            "published": m.get("published", {}), "journal": m.get("container-title", []),
            "updates": m.get("update-to", []), "relation": m.get("relation", {}),
            "claim_support_verified_by_metadata": False}


class PublicRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        checked_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def check_chemical_metadata(source: dict, obj: dict) -> dict:
    require(isinstance(obj, dict) and isinstance(obj.get("PropertyTable"), dict), "invalid chemical property envelope")
    rows = obj["PropertyTable"].get("Properties")
    require(isinstance(rows, list) and len(rows) == 1 and isinstance(rows[0], dict), "invalid chemical property records")
    r = rows[0]
    require(type(r.get("CID")) is int and r["CID"] == source["expected_cid"], "compound identity mismatch")
    require(r.get("MolecularWeight") == source["expected_molecular_weight"], "molecular-weight mismatch")
    return {"cid": r["CID"], "molecular_weight": r["MolecularWeight"], "clinical_efficacy_inferred": False}


def new_output(path: Path) -> Path:
    path = path.resolve()
    require(path.is_relative_to(ROOT / "results/feat009"), "output must be a new directory under results/feat009")
    path.mkdir(parents=True, exist_ok=False)
    return path


def fetch_sources(path: Path) -> dict:
    sources, _ = load_ledgers()
    sources_hash = sha256(SOURCES)
    path = new_output(path)
    rows = []
    opener = urllib.request.build_opener(PublicRedirect())
    for s in sources["sources"]:
        url = ("https://api.crossref.org/works/" + urllib.parse.quote(s["doi"], safe="") if "doi" in s else s["url"])
        row = {"id": s["id"], "url": checked_url(url), "retrieved_at": datetime.now(timezone.utc).isoformat()}
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MVA-Track2-public-evidence/1.0"})
            with opener.open(req, timeout=30) as response:
                b = response.read()
            (path / (s["id"] + (".json" if "doi" in s or s["kind"] == "database" else ".html"))).write_bytes(b)
            row.update(sha256=hashlib.sha256(b).hexdigest(), bytes=len(b), status="retrieved")
            if "doi" in s:
                row["metadata"] = check_metadata(s, json.loads(b))
                row["status"] = "metadata_match" if row["metadata"]["title_matches"] else "title_review_required"
            elif s["kind"] == "database":
                row["metadata"] = check_chemical_metadata(s, json.loads(b))
                row["status"] = "chemical_identity_match"
            else:
                # HTTP success alone may be an anti-bot page, not the desired document.
                require(len(b) > 2000 and not any(x in b.lower() for x in [b"checking your browser", b"just a moment..."]), "source body needs manual review")
                row["status"] = "page_retrieved_content_review_separate"
        except (ValueError, KeyError, TypeError, urllib.error.URLError, OSError) as exc:
            row.update(status="error", error_type=type(exc).__name__)
        rows.append(row)
        (path / "verification.json").write_text(json.dumps({"sources_sha256": sources_hash, "script_sha256": SCRIPT_SHA256, "sources": rows}, indent=2) + "\n")
    result = {"source_count": len(rows), "metadata_matches": sum(r["status"] == "metadata_match" for r in rows),
              "chemical_identity_matches": sum(r["status"] == "chemical_identity_match" for r in rows),
              "needs_review": [r["id"] for r in rows if r["status"] in {"error", "title_review_required"}],
              "note": "Identifiers and page provenance only; inspect claim support and corrections separately."}
    (path / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def check_track1() -> dict:
    path = ROOT / "results/feat008/jvv7_genomewide_mva_v4"
    for name, expected in TRACK1.items():
        require(sha256(path / name) == expected, "submitted Track 1 artifact changed")
    return {"unchanged_local_v4_hashes": TRACK1, "uploaded_bytes_independently_verified": False}


def candidate_table(sources: dict, candidates: dict) -> str:
    index = {s["id"]: s for s in sources["sources"]}
    lines = ["# Track 2 candidate evidence table", "", "Research only. All clinical efficacy is unestablished; trans phase remains unconfirmed.", "",
             "| Candidate | Research decision | Rationale | Main objection / stop criterion | Sources |",
             "|---|---|---|---|---|"]
    for c in candidates["candidates"]:
        ids = list(dict.fromkeys(c["support"] + c["counterevidence"]))
        links = ", ".join(f'[{i}]({index[i]["url"]})' for i in ids)
        values = [c["name"], c["decision"], c["bridge"], c["falsifier"], links]
        lines.append("| " + " | ".join(v.replace("|", "\\|").replace("\n", " ") for v in values) + " |")
    return "\n".join(lines) + "\n"


def build(path: Path) -> dict:
    sources, candidates = load_ledgers()
    track1 = check_track1()
    report = ROOT / "notes/track2-report.md"
    inputs = [ROOT / p for p in sorted(INPUT_PATHS)]
    require(all(p.is_file() for p in inputs), "research input missing")
    for phrase in ["trans phase remains unconfirmed", "research", "OpenAI", "API tier", "not used to train", "Acknowledgement"]:
        require(phrase.lower() in report.read_text().lower(), f"report lacks required boundary/disclosure: {phrase}")
    exposure = json.loads((ROOT / "notes/track2-exposure.json").read_text())
    exposure_result = audit_exposure(exposure, {s["id"]: s for s in sources["sources"]})
    path = new_output(path)
    for name, source in COPY_INPUTS.items():
        shutil.copyfile(ROOT / source, path / name)
    (path / "candidate-evidence.md").write_text(candidate_table(sources, candidates))
    (path / "sensitivity.json").write_text(json.dumps(sensitivities(sources, candidates), indent=2) + "\n")
    (path / "exposure-audit.json").write_text(json.dumps(exposure_result, indent=2) + "\n")
    manifest = {"schema_version": 2, "stage": "research_draft_not_submitted", "upload_performed": False, "video_url": None,
                "created_at": datetime.now(timezone.utc).isoformat(), "checks": validate(sources, candidates), "track1": track1,
                "input_hashes": {str(p.relative_to(ROOT)): sha256(p) for p in inputs},
                "files": {p.name: sha256(p) for p in sorted(path.iterdir())},
                "remaining_gates": ["final recorded three-minute pitch and hosted URL", "live rules, disclosure and authenticated quota", "final owner review and portal receipt"],
                "future_research_not_submission_prerequisite": "Proposed laboratory and exposure experiments have not been performed. A research proposal must not label them as measured results."}
    (path / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def verify(path: Path) -> dict:
    """Verify package integrity and current inputs, not scientific validity or upload readiness."""
    path = path.resolve()
    require(path.is_relative_to(ROOT / "results/feat009") and path.is_dir(), "package must be under results/feat009")
    manifest = json.loads((path / "manifest.json").read_text())
    require(manifest.get("schema_version") == 2 and manifest.get("stage") == "research_draft_not_submitted", "not a current v2 research package; preserve historical snapshots")
    require(manifest.get("upload_performed") is False and manifest.get("video_url") is None, "draft must not imply upload or a hosted pitch")
    expected = PACKAGE_FILES
    require(set(manifest.get("files", {})) == expected, "package file set mismatch")
    require({p.name for p in path.iterdir()} == expected | {"manifest.json"}, "unexpected or missing package file")
    for name, digest in manifest["files"].items():
        target = path / name
        require(not target.is_symlink() and target.is_file() and sha256(target) == digest, "package hash mismatch")
    sources = json.loads((path / "sources.json").read_text())
    candidates = json.loads((path / "candidates.json").read_text())
    require(validate(sources, candidates) == manifest.get("checks"), "package ledger checks mismatch")
    require(json.loads((path / "sensitivity.json").read_text()) == sensitivities(sources, candidates), "sensitivity output mismatch")
    require((path / "candidate-evidence.md").read_text() == candidate_table(sources, candidates), "candidate table mismatch")
    exposure_result = audit_exposure(json.loads((path / "exposure.json").read_text()), {s["id"]: s for s in sources["sources"]})
    require(json.loads((path / "exposure-audit.json").read_text()) == exposure_result, "exposure audit mismatch")
    require(set(manifest.get("input_hashes", {})) == INPUT_PATHS, "input manifest mismatch")
    for name, digest in manifest["input_hashes"].items():
        require(sha256(ROOT / name) == digest, "research input changed; build a new package")
    for output, source in COPY_INPUTS.items():
        require(manifest["files"][output] == manifest["input_hashes"][source], "copied input mismatch")
    require(manifest.get("track1") == check_track1(), "Track 1 preservation record mismatch")
    return {"integrity_verified": True, "stage": manifest["stage"], "files": len(expected), "upload_ready": False,
            "note": "Hashes detect drift, not malicious replacement of both files and manifest, claim validity, or completed laboratory experiments."}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["check", "sensitivity", "sources", "build", "verify", "track1"])
    p.add_argument("output", nargs="?", type=Path)
    args = p.parse_args()
    if args.command in {"sources", "build", "verify"}:
        require(args.output is not None, "output directory required")
        result = {"sources": fetch_sources, "build": build, "verify": verify}[args.command](args.output)
    elif args.command == "track1":
        result = check_track1()
    else:
        sources, candidates = load_ledgers()
        result = validate(sources, candidates) if args.command == "check" else sensitivities(sources, candidates)
    print(json.dumps(result, indent=2))
    if args.command == "sources" and result["needs_review"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
