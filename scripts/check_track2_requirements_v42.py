#!/usr/bin/env python3
"""Verify the bounded anonymous public-official refresh behind Track 2 v42.

This checks provenance and public discussion arithmetic. It is not an
authenticated portal check, biological validation, clinical assessment or
submission preflight.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "notes/track2-requirements-v42.json"
REVIEW = ROOT / "notes/track2-requirements-review-v42.md"
RECEIPTS = ROOT / "sources/public-official-v42"
BASELINE = ROOT / "notes/track2-requirements-v39.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visible_comments(thread: dict[str, Any]) -> int:
    return sum(
        event["type"] == "comment" and not event["data"].get("hidden", False)
        for event in thread["events"]
    )


def check() -> dict[str, Any]:
    require(AUDIT.is_file(), "Missing v42 requirements audit")
    require(REVIEW.is_file(), "Missing v42 requirements review")
    audit = json.loads(AUDIT.read_text())
    review = REVIEW.read_text()
    text = re.sub(r"\s+", " ", review).lower()
    baseline = json.loads(BASELINE.read_text())

    require(audit["schema_version"] == 42, "Wrong requirements schema")
    require(audit["revision"] == baseline["revision"] == "60e1c30e337ce6fe01813040dbe49979eb8c50aa", "Revision drift")
    require(audit["anonymous_get_only"] is True, "Refresh was not declared anonymous")

    required = {
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
    for key, value in required.items():
        require(baseline[key] == value, "Baseline requirement drift: " + key)
        require(audit["unchanged_requirements"][key] == value, "V42 requirement drift: " + key)

    expected_official = {
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
        if source["name"] in {"tabs/rules.py", "static/templates/methods_description_form.xlsx"}:
            require("receipt" not in source and source["sha256"] == expected_official[source["name"]],
                    "Omitted official source was not preserved by URL/hash: " + source["name"])
        else:
            path = ROOT / source["receipt"]
            require(path.is_file(), "Missing official receipt: " + source["name"])
            require(digest(path) == source["sha256"] == expected_official[source["name"]], "Official hash drift: " + source["name"])
        require(source["unchanged"] is True and source["http_status"] == 200, "Official retrieval drift")

    community = audit["community"]
    require(community["listed_count"] == community["threads"].__len__() == 31, "Thread count drift")
    require(community["closed_count"] == 16, "Closed count drift")
    require(community["visible_comments"] == 89, "Visible-comment count drift")
    require(community["complete"] is True and community["hidden_edit_history_reviewed"] is False, "Community scope drift")
    require(community["listing_receipt"] == "sources/public-official-v42/index-0.json", "Listing receipt drift")
    listing = json.loads((ROOT / community["listing_receipt"]).read_text())
    require(listing["count"] == 31, "Listing count drift")
    require({d["num"] for d in listing["discussions"]} == {t["num"] for t in community["threads"]}, "Listing/thread identity drift")

    for thread in community["threads"]:
        path = ROOT / thread["receipt"]
        require(path.is_file(), "Missing thread receipt: " + str(thread["num"]))
        payload = json.loads(path.read_text())
        require(payload["num"] == thread["num"], "Thread identity drift: " + str(thread["num"]))
        require(digest(path) == thread["sha256"], "Thread hash drift: " + str(thread["num"]))
        require(visible_comments(payload) == thread["visible_comments"], "Visible-comment drift: " + str(thread["num"]))
        require(payload["status"] == thread["status"], "Thread status drift: " + str(thread["num"]))

    recheck = audit.get("live_recheck")
    require(recheck == {
        "retrieved_utc": "2026-10-20T11:49:35Z",
        "space_revision": "60e1c30e337ce6fe01813040dbe49979eb8c50aa",
        "revision_unchanged": True,
        "listed_public_discussions": 31,
        "discussion_numbers_unchanged": True,
        "new_organizer_requirement_found": False,
        "scope": "Anonymous live revision and public discussion-listing consistency check; no authenticated account, quota or full-thread reread",
    }, "Live official recheck drift")
    require(any("11:49 UTC recheck confirms only Space revision" in x for x in audit["limitations"]),
            "Live recheck limitation omitted")

    changes = audit["material_changes"]
    require(changes == {
        "new_thread_32_pitch_video_published_example": True,
        "thread_31_organizer_synapse_alternative": True,
        "thread_29_participant_correction_irb_consent_routing": True,
        "thread_26_hash_only_reaction_metadata_change": True,
        "official_seven_files_unchanged": True,
    }, "Material-change drift")

    thread32 = next(t for t in community["threads"] if t["num"] == 32)
    require(thread32["visible_comments"] == 3, "Thread 32 comment count drift")
    thread31 = next(t for t in community["threads"] if t["num"] == 31)
    require(thread31["visible_comments"] == 2, "Thread 31 comment count drift")
    thread29 = next(t for t in community["threads"] if t["num"] == 29)
    require(thread29["visible_comments"] == 2, "Thread 29 comment count drift")
    thread26 = next(t for t in community["threads"] if t["num"] == 26)
    require(thread26["visible_comments"] == 1, "Thread 26 comment count drift")

    for phrase in [
        "seven official files remain byte-identical",
        "31 threads / 89 visible comments / 16 closed",
        "published paper as an example",
        "no script rewrite is mandated before recording",
        "synapse project",
        "public github remains our selected route",
        "irb/consent routing",
        "thread 26",
        "no organizer statement changed the submission deadline",
        "not a systematic literature search",
    ]:
        require(phrase in text, "Review boundary missing: " + phrase)
    for forbidden in ["quota is known", "upload is ready", "provider settings are verified", "establishes biological validation", "clinical safety recommendation"]:
        require(forbidden not in text, "False readiness/biology claim: " + forbidden)

    require(audit["provider_settings_verified"] is False and audit["licensing_scope_resolved"] is False and audit["upload_ready"] is False, "Unsupported readiness promotion")
    return {
        "passed": True,
        "version": 42,
        "official_sources": len(official),
        "public_threads": len(community["threads"]),
        "visible_comments": community["visible_comments"],
        "closed_threads": community["closed_count"],
        "requirements_changed": False,
        "anonymous_get_only": True,
        "live_recheck_passed": True,
        "provider_settings_verified": False,
        "licensing_scope_resolved": False,
        "upload_ready": False,
        "biological_validation": False,
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
