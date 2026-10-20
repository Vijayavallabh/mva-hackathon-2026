#!/usr/bin/env python3
"""Verify the targeted v45 public falsification-literature addendum."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "notes/track2-literature-v45.md"
AUDIT = ROOT / "notes/track2-literature-audit-v45.json"
SOURCE_DIR = ROOT / "sources/public-literature-v45"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check() -> dict[str, Any]:
    require(NOTE.is_file(), "Missing v45 literature note")
    require(AUDIT.is_file(), "Missing v45 literature audit")
    audit = json.loads(AUDIT.read_text())
    note = NOTE.read_text()
    text = re.sub(r"\s+", " ", note).lower()

    require(audit["schema_version"] == 1, "Wrong v45 audit schema")
    require(len(audit["searches"]) == 7, "v45 search-count drift")
    require([x["found"] for x in audit["searches"]] == [10, 3, 1, 3, 11, 3, 1], "v45 search-result drift")
    for search in audit["searches"]:
        receipt = ROOT / search["query_receipt"]
        require(receipt.is_file(), "Missing v45 search receipt: " + search["name"])
        require(digest(receipt) not in {"", None}, "Unreadable receipt")
    require(audit["biological_validation"] is False and audit["full_text_systematic_review"] is False,
            "False v45 scope promotion")
    require(audit["new_gpu_campaign"] is False, "False GPU campaign claim")

    dispositions = audit["disposition_changes"]
    require(dispositions["everolimus"] == "unchanged_mechanistic_probe_only_on_hold", "Everolimus promoted")
    require(dispositions["hydroxychloroquine"] == "unchanged_reserve", "HCQ promoted")
    require(dispositions["nad_sirt2"] == "unchanged_not_promoted", "NAD/SIRT2 promoted")
    require(dispositions["griseofulvin"] == "not_promoted_tumour_killing_context_only", "Griseofulvin promoted")
    require(dispositions["norlichexanthone"] == "not_promoted_tumour_killing_context_only", "Norlichexanthone promoted")
    require(dispositions["vorinostat"] == "unchanged_deprioritized_tumour_only", "Vorinostat promoted")
    require(dispositions["rescue_priority"] is None and dispositions["clinical_exposure_margin"] is None and dispositions["phase"] == "unconfirmed", "Unsupported clinical claim")

    selected = audit["selected_sources"]
    require(len(selected) == 4, "v45 selected-source drift")
    dois = {x["doi"] for x in selected}
    require(dois == {"10.1016/j.bioorg.2026.110130", "10.1016/j.compbiolchem.2026.109012", "10.1093/nar/gkaf1517", "10.1126/sciadv.ady6890"}, "v45 DOI drift")
    for source in selected:
        require(source["full_text_obtained"] is False, "False full-text claim: " + source["doi"])
        require(bool(source["title"] and source["journal"] and source["reading_depth"]), "Incomplete source metadata")
        if source["receipt"]:
            path = ROOT / source["receipt"]
            require(path.is_file(), "Missing selected-source receipt: " + source["doi"])
            require(digest(path) == source["sha256"], "Selected-source hash drift: " + source["doi"])

    expected_files = {
        "crossref-norlichexanthone.json",
        "europepmc-norlichexanthone.json",
        "openalex-norlichexanthone-search.json",
        "pubmed-41895167-efetch.xml",
        "pubmed-41895167-summary.json",
        "pubmed-42330849-efetch.xml",
        "pubmed-42330849-summary.json",
        "pubmed-bub1b-drug-repurposing-2025-2026-search.json",
        "pubmed-bubr1-corona-2025-2026-search.json",
        "pubmed-bubr1-mcc-2025-2026-search.json",
        "pubmed-mtor-chromosome-segregation-human-2020-2026-search.json",
        "pubmed-mva-treatment-2025-2026-search.json",
        "pubmed-rapamycin-chromosome-segregation-human-2020-2026-search.json",
        "unpaywall-norlichexanthone.json",
    }
    actual_files = {p.name for p in SOURCE_DIR.iterdir() if p.is_file()}
    require(actual_files == expected_files, f"v45 source-file drift: {actual_files ^ expected_files}")

    # The two full PubMed records must contain the claimed abstract facts.
    norlich = (SOURCE_DIR / "pubmed-42330849-efetch.xml").read_text().lower()
    for phrase in ["mad1 and bubr1", "mad1-mad2 interaction", "norlichexanthone", "tpr", "multipolar spindles"]:
        require(phrase in norlich, "Norlichexanthone abstract claim missing: " + phrase)
    comp = (SOURCE_DIR / "pubmed-41895167-efetch.xml").read_text().lower()
    for phrase in ["tpx2 and bub1b", "virtual-screening", "vorinostat", "breast cancer"]:
        require(phrase in comp, "Computational BUB1B paper claim missing: " + phrase)

    required_note_phrases = [
        "it does **not** change any drug disposition",
        "everolimus remains a mechanistic probe on hold",
        "hcq remains reserve",
        "this is **tumour-cell killing**, not deficient-normal rescue",
        "does not promote griseofulvin or norlichexanthone for mva",
        "computational docking to bub1b is not useful function",
        "do not run another gpu campaign",
        "not a systematic review",
        "no biological validation",
    ]
    for phrase in required_note_phrases:
        require(phrase in text, "v45 note boundary missing: " + phrase)

    forbidden = [
        "proband01", "wgs_ex2312012", "everolimus is promoted", "hcq is reopened",
        "nad/sirt2 is promoted", "griseofulvin is promoted", "norlichexanthone is promoted",
        "vorinostat is reopened", "rescue priority is established", "clinical exposure margin is established",
        "phase is confirmed", "biological validation is established",
    ]
    for phrase in forbidden:
        require(phrase not in text, "False v45 claim: " + phrase)

    for doi in dois:
        require(f"https://doi.org/{doi.lower()}" in note.lower(), "Missing DOI link: " + doi)

    return {
        "passed": True,
        "version": 45,
        "searches": len(audit["searches"]),
        "selected_sources": len(selected),
        "public_receipts": len(actual_files),
        "repository_bytes": sum(p.stat().st_size for p in SOURCE_DIR.iterdir() if p.is_file()),
        "subject_data_read": False,
        "drug_dispositions_changed": False,
        "biological_validation": False,
        "full_text_systematic_review": False,
        "new_gpu_campaign": False,
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
