#!/usr/bin/env python3
"""Reproducibly verify the public-source Track 2 v41 literature refresh.

This is an evidence/provenance check, not biological validation and not a
systematic full-text review.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "notes/track2-literature-v41.md"
AUDIT = ROOT / "notes/track2-literature-audit-v41.json"
SOURCE_DIR = ROOT / "sources/public-literature-v41"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check() -> dict[str, Any]:
    require(NOTE.is_file(), "Missing v41 literature note")
    require(AUDIT.is_file(), "Missing v41 literature audit")
    audit = json.loads(AUDIT.read_text())
    note = NOTE.read_text()
    text = re.sub(r"\s+", " ", note).lower()

    require(audit["schema_version"] == 1, "Wrong literature-audit schema")
    searches = audit["searches"]
    require(
        [(x["database"], x["found"]) for x in searches]
        == [
            ("PubMed eSearch/eSummary/eFetch", 141),
            ("OpenAlex works search", 206),
            ("PubMed", 13),
            ("PubMed", 7),
            ("PubMed", 2),
        ],
        "Search coverage drift",
    )
    require(all(x["returned"] == 100 for x in searches[:2]), "Returned-count drift")

    receipts = audit["public_receipts"]
    require(len(receipts) == 21 and len(list(SOURCE_DIR.iterdir())) == 21, "Receipt count drift")
    for name, expected in receipts.items():
        path = SOURCE_DIR / name
        require(path.is_file(), f"Missing public receipt: {name}")
        require(digest(path) == expected, f"Receipt hash drift: {name}")

    expected_dispositions = {
        'everolimus':'unchanged_mechanistic_probe_only_on_hold',
        'hydroxychloroquine':'unchanged_reserve',
        'nad_sirt2':'unchanged_not_promoted',
    }
    require(audit['disposition_changes']['everolimus'] == expected_dispositions['everolimus'], 'Everolimus disposition drift')
    require(audit['disposition_changes']['hydroxychloroquine'] == expected_dispositions['hydroxychloroquine'], 'HCQ disposition drift')
    require(audit['disposition_changes']['nad_sirt2'] == expected_dispositions['nad_sirt2'], 'NAD/SIRT2 disposition drift')
    require(audit['disposition_changes']['rescue_priority'] is None and
            audit['disposition_changes']['clinical_exposure_margin'] is None and
            audit['disposition_changes']['phase'] == 'unconfirmed', 'Unsupported literature disposition')
    require(audit['biological_validation'] is False and audit['full_text_systematic_review'] is False,
            'Literature scope falsely promoted')
    require(any('not exhaustive full-text systematic review' in x.lower() for x in audit['limitations']),
            'Search limitation omitted')
    selected = audit["selected_sources"]
    require(len(selected) == 14, "Selected-source count drift")
    required_dois = {
        "10.1126/sciadv.ady6890",
        "10.1038/s42003-026-10384-9",
        "10.1093/nar/gkaf1517",
        "10.1038/s41467-026-70521-0",
        "10.1016/j.ceb.2025.102537",
        "10.3389/fendo.2026.1838559",
        "10.1093/humupd/dmag012",
        "10.1038/s41467-026-77795-4",
        "10.1136/jmg-2025-111325",
        "10.1080/01676830.2026.2715719",
        "10.1111/acel.70160",
        "10.1002/cbin.70033",
        "10.1158/0008-5472.CAN-26-0874",
        "10.1515/jpem-2025-0643",
    }
    require({x["doi"] for x in selected} == required_dois, "Selected-DOI drift")
    for source in selected:
        require(source["receipt"].startswith("sources/public-literature-v41/"), "Receipt path is outside public source scope")
        require(digest(ROOT / source["receipt"]) == source["sha256"], "Selected-source hash drift")
        require(source["title"] and source["journal"], "Incomplete selected-source metadata")

    required_note_phrases = [
        "does not change any drug disposition",
        "no rescue priority is established",
        "everolimus remains a mechanistic probe on hold",
        "hcq remains reserve",
        "corona/mcc readouts",
        "mitochondrial integrity/proteostasis markers",
        "k250/s16/s39 state only as a mechanistic endpoint",
        "do not promote a nad/sirt2 intervention",
        "heterozygous missense evidence",
    ]
    for phrase in required_note_phrases:
        require(phrase in text, f"Note boundary missing: {phrase}")

    # Prevent subject-data provenance and false disposition claims.
    forbidden = [
        "proband01",
        "wgs_ex2312012",
        "rescue priority is now",
        "everolimus is promoted",
        "nad/sirt2 is promoted",
        "hcq is reopened",
        "clinical exposure margin is established",
        "phase is confirmed",
    ]
    for phrase in forbidden:
        require(phrase not in text, f"False v41 claim: {phrase}")

    # Required DOI links in the note.
    for doi in required_dois:
        require(f"https://doi.org/{doi.lower()}" in note.lower(), f"Missing source link: {doi}")

    return {
        "passed": True,
        "version": 41,
        "searches": len(searches),
        "selected_sources": len(selected),
        "public_receipts": len(receipts),
        "repository_bytes": sum((SOURCE_DIR / name).stat().st_size for name in receipts),
        "subject_data_read": False,
        "drug_dispositions_changed": (
            audit['disposition_changes']['everolimus'] != 'unchanged_mechanistic_probe_only_on_hold' or
            audit['disposition_changes']['hydroxychloroquine'] != 'unchanged_reserve' or
            audit['disposition_changes']['nad_sirt2'] != 'unchanged_not_promoted' or
            audit['disposition_changes']['rescue_priority'] is not None
        ),
        "biological_validation": audit['biological_validation'],
        "full_text_systematic_review": audit['full_text_systematic_review'],
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
