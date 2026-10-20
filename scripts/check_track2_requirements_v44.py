#!/usr/bin/env python3
"""Verify the anonymous live v44 deadline refresh."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "notes/track2-requirements-v44.json"
REVIEW = ROOT / "notes/track2-requirements-review-v44.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check() -> dict[str, Any]:
    require(AUDIT.is_file(), "Missing v44 requirements audit")
    require(REVIEW.is_file(), "Missing v44 requirements review")
    audit = json.loads(AUDIT.read_text())
    text = re.sub(r"\s+", " ", REVIEW.read_text()).lower()

    require(audit["schema_version"] == 44, "Wrong v44 schema")
    require(audit["anonymous_get_only"] is True, "Not anonymous GET-only")
    require(audit["revision"] == "60e1c30e337ce6fe01813040dbe49979eb8c50aa", "Revision drift")
    require(audit["retrieved_utc"] == "2026-10-20T15:34:56Z", "Timestamp drift")

    expected_hashes = {
        "README.md": "9660de914f8f77523faded810d0756d390321649f00e2151eb5cdb8b818c6a3f",
        "config.py": "a65e67fca2fb698ac3f3fe6610e585f549cf29f175d636ce77543d7db6dc8bdc",
        "tabs/about.py": "57d25b20a840d57e09268ca6e8615e85579bf65a99829095690e68c2463d5cf3",
        "tabs/rules.py": "16aa61b9580abc21e6ea69e994cdb27341e1b85b1d00a57da889520a94295906",
        "tabs/faq.py": "36c3e51e9735a6d2ffacfccea2246a28a13658038988ac88317c5aa05ad71c53",
        "tabs/submit_track2.py": "f48d576ab052df34527222b7693f956e15e5376ef68eddedcf0c4f04736bf65c",
        "static/templates/methods_description_form.xlsx": "61aab080a2868a3b724e76692b83c24812112e305cd3a8b03f8f91a6b2414441",
    }
    official = audit["official_sources"]
    require(len(official) == 7, "Official source count drift")
    for source in official:
        require(source["sha256"] == expected_hashes[source["name"]], "Official hash drift: " + source["name"])
        require(source["http_status"] == 200 and source["unchanged"] is True, "Official retrieval drift")

    listing = audit["discussion_listing"]
    require(listing["count"] == 31 and listing["closed_count"] == 16, "Listing count drift")
    require(listing["numbers"] == [1,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32], "Discussion identity drift")
    require(listing["status_and_titles_unchanged_from_v42"] is True, "Listing status/title drift")
    require(listing["visible_comment_counts_not_reread"] is True, "False full-thread reread")
    require(listing["new_organizer_requirement_found"] is False, "False new requirement")

    required = audit["unchanged_requirements"]
    expected = {
        "deadline_utc": "2026-10-24T23:59:00Z",
        "judging_end_date": "2026-12-17",
        "winner_announcement_date": "2026-12-18",
        "submission_limit": 3,
        "only_latest_reviewed": True,
        "quota_remaining": None,
        "required_ai_cell": "B9",
        "abstract_word_limit": 500,
        "video_duration_seconds": 180,
        "video_hosts": ["youtube.com", "youtu.be", "vimeo.com"],
        "rubric_weights": {"scientific_rigor": 35, "potential_impact": 25, "innovation": 25, "scalability": 15},
        "data_deletion_deadline": "2026-11-23",
        "data_deletion_confirmation_email": "cnb@sagebase.org",
    }
    require(required == expected, "Requirement drift")

    changes = audit["material_changes"]
    require(changes == {
        "official_seven_files_unchanged": True,
        "space_revision_unchanged": True,
        "discussion_listing_unchanged_by_number_status_and_title": True,
        "new_organizer_requirement_found": False,
    }, "Material-change drift")

    for phrase in [
        "anonymous public-source refresh",
        "not a contact, authenticated account check or submission preflight",
        "did not reread every discussion thread",
        "october 24, 23:59 utc",
        "180 seconds",
        "35/25/25/15",
        "quota remains unknown",
        "november 23",
        "cnb@sagebase.org",
        "no drug disposition",
        "not biological validation",
    ]:
        require(phrase in text, "Review boundary missing: " + phrase)

    for forbidden in ["quota is known", "upload is ready", "provider settings are verified", "establishes biological validation", "clinical safety recommendation", "submission was performed"]:
        require(forbidden not in text, "False claim: " + forbidden)

    require(audit["provider_settings_verified"] is False, "False provider verification")
    require(audit["licensing_scope_resolved"] is False, "False licensing resolution")
    require(audit["upload_ready"] is False, "False upload readiness")

    return {
        "passed": True,
        "version": 44,
        "official_sources": len(official),
        "public_threads": listing["count"],
        "closed_threads": listing["closed_count"],
        "requirements_changed": False,
        "anonymous_get_only": True,
        "provider_settings_verified": False,
        "licensing_scope_resolved": False,
        "upload_ready": False,
        "biological_validation": False,
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
