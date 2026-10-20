#!/usr/bin/env python3
"""Verify the public-source Track 2 v43 contrary-evidence literature addendum.

This checks provenance and documented scope. It is not biological validation and
not a systematic review.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "notes/track2-literature-v43.md"
AUDIT = ROOT / "notes/track2-literature-audit-v43.json"
SOURCE_DIR = ROOT / "sources/public-literature-v43"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check() -> dict[str, Any]:
    require(NOTE.is_file(), "Missing v43 literature note")
    require(AUDIT.is_file(), "Missing v43 literature audit")
    audit = json.loads(AUDIT.read_text())
    note = NOTE.read_text()
    text = re.sub(r"\s+", " ", note).lower()

    require(audit["schema_version"] == 1, "Wrong v43 audit schema")
    require(len(audit["searches"]) == 3, "v43 search-count drift")
    require(
        [x["found"] for x in audit["searches"]] == [1, 13, 13],
        "v43 search-result drift",
    )
    require(audit["biological_validation"] is False, "False biological validation")
    require(audit["full_text_systematic_review"] is False, "False systematic-review claim")
    require(
        any("not archived" in x.lower() for x in audit["limitations"]),
        "OpenAlex receipt limitation omitted",
    )

    dispositions = audit["disposition_changes"]
    require(
        dispositions["everolimus"] == "unchanged_mechanistic_probe_only_on_hold"
        and dispositions["hydroxychloroquine"] == "unchanged_reserve"
        and dispositions["nad_sirt2"] == "unchanged_not_promoted"
        and dispositions["rescue_priority"] is None
        and dispositions["clinical_exposure_margin"] is None
        and dispositions["phase"] == "unconfirmed",
        "Unsupported disposition change",
    )

    expected_files = {
        "crossref-elife-108275.json",
        "elife-108275-fulltext.xml",
        "pubmed-40410156-efetch.xml",
        "pubmed-elife108275-search.json",
        "pubmed-elife108275-summary.json",
    }
    actual_files = {p.name for p in SOURCE_DIR.iterdir() if p.is_file()}
    require(actual_files == expected_files, f"v43 source-file drift: {actual_files ^ expected_files}")

    selected = audit["selected_sources"]
    require(len(selected) == 2, "v43 selected-source drift")
    required_dois = {"10.7554/eLife.108275", "10.1038/s41467-025-59970-1"}
    require({x["doi"] for x in selected} == required_dois, "v43 selected-DOI drift")
    for source in selected:
        path = ROOT / source["receipt"]
        require(path.is_file(), f"Missing v43 source receipt: {source['receipt']}")
        require(digest(path) == source["sha256"], f"v43 source hash drift: {source['receipt']}")
        require(source["receipt"].startswith("sources/public-literature-v43/"), "Receipt outside v43 scope")
        require(bool(source["title"] and source["journal"] and source["reading_depth"]), "Incomplete metadata")

    # Verify the full-text source contains the claimed scope-limiting facts.
    fulltext = (SOURCE_DIR / "elife-108275-fulltext.xml").read_text()
    for phrase in [
        "Interplay between cohesin and TORC1 links chromosome segregation",
        "200 ng/ml",
        "mis4-G1487D",
        "reduced TORC1 activity also increased cohesin binding",
        "TORC1 is essential for cell growth",
        "Rapamycin only partially inhibits TORC1 activity",
    ]:
        require(phrase.lower() in fulltext.lower(), f"v43 full-text claim not present: {phrase}")
    for phrase in ["everolimus", "sirolimus", "BUB1B", "hTERT-RPE1"]:
        require(phrase.lower() not in fulltext.lower(), f"False source scope: {phrase}")

    required_note_phrases = [
        "does not change any drug disposition",
        "no rescue priority",
        "everolimus remains a mechanistic probe on hold",
        "hcq remains reserve",
        "no nad/sirt2 intervention is promoted",
        "fission yeast", "not mammalian mva",
        "did not test everolimus",
        "rapamycin and everolimus are not interchangeable",
        "all-enrolled daughter fate",
        "measure p70 s6 kinase and 4ebp1 phosphorylation",
        "clinical exposure margin",
        "not a systematic review",
    ]
    for phrase in required_note_phrases:
        require(phrase in text, f"v43 boundary missing: {phrase}")

    forbidden = [
        "proband01",
        "wgs_ex2312012",
        "everolimus is promoted",
        "nad/sirt2 is promoted",
        "hcq is reopened",
        "clinical exposure margin is established",
        "phase is confirmed",
        "supports everolimus specifically",
        "rescue priority is established",
    ]
    for phrase in forbidden:
        require(phrase not in text, f"False v43 claim: {phrase}")

    for doi in required_dois:
        require(f"https://doi.org/{doi.lower()}" in note.lower(), f"Missing v43 DOI link: {doi}")

    return {
        "passed": True,
        "version": 43,
        "searches": len(audit["searches"]),
        "selected_sources": len(selected),
        "public_receipts": len(actual_files),
        "repository_bytes": sum(p.stat().st_size for p in SOURCE_DIR.iterdir() if p.is_file()),
        "subject_data_read": False,
        "drug_dispositions_changed": False,
        "biological_validation": audit["biological_validation"],
        "full_text_systematic_review": audit["full_text_systematic_review"],
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
