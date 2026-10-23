#!/usr/bin/env python3
"""Verify the owner-facing Track 2 submission-prep checklist against current artifacts."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "notes/track2-submission-prep-v16.md"
CURRENT = ROOT / "notes/track2-current.json"
MATERIALS = ROOT / "notes/track2-submission-materials-v21.json"
OFFICIAL = ROOT / "sources/public-official-v52/tabs-submit_track2.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check() -> dict[str, Any]:
    require(CHECKLIST.is_file(), "Missing submission-prep checklist")
    require(CURRENT.is_file(), "Missing current artifact record")
    require(OFFICIAL.is_file(), "Missing official submit-tab receipt")
    note = CHECKLIST.read_text()
    text = re.sub(r"\s+", " ", note).lower()
    state = json.loads(CURRENT.read_text())
    official = OFFICIAL.read_text()

    require(MATERIALS.is_file(), "Missing exact submission-material receipt")
    materials = json.loads(MATERIALS.read_text())
    exact_files = {name: ROOT / record["path"] for name, record in {
        "pdf": materials["report_pdf"],
        "md": materials["report_markdown"],
        "workbook": materials["methods_workbook"],
        "slides": materials["slide_pdf"],
    }.items()}
    exact_files["bundle"] = ROOT / state["video_materials_bundle"]
    for name, path in exact_files.items():
        if path.is_file():
            require(not path.is_symlink(), f"Symlinked submission material: {name}")
    snapshot = ROOT / state["snapshot"]
    require(state["snapshot"].startswith("results/feat009/jvv7_track2_research_v48-verified"), "Unsafe current release-snapshot route")
    bundle = ROOT / state["video_materials_bundle"]
    require(bundle == exact_files["bundle"], "Checklist/current bundle drift")
    require(state["render_directory"] == str((ROOT / materials["slide_pdf"]["path"]).parent.relative_to(ROOT)), "Render-directory drift")
    require(state["document_directory"] == str((ROOT / materials["report_pdf"]["path"]).parent.relative_to(ROOT)), "Document-directory drift")
    require(state["status"]["upload_ready"] is False and state["status"]["upload_performed"] is False, "False submission state")

    for phrase in [
        "it is **not** a submission",
        "upload **one report file**",
        "either the pdf or markdown version, not both",
        "github repo url",
        "https://github.com/vijayavallabh/mva-hackathon-2026",
        "pitch video url:** absent",
        "team / display name:** `aeglos` (owner-selected public team name)",
        "no video has been recorded",
        "no video runtime has been measured",
        "no video url exists",
        "no authenticated hugging face identity/quota check exists",
        "no actual outside review has been recorded",
        "no submission has been performed, and no receipt exists",
        "do not prefill them",
    ]:
        require(phrase in text, "Checklist boundary missing: " + phrase)

    for forbidden in [
        "upload is ready",
        "**no video has been recorded",
        "**no video url exists",
        "quota is known",
        "**no submission has been performed",
        "biological validation is established",
        "prize eligibility is established",
    ]:
        require(forbidden not in text, "False checklist claim: " + forbidden)

    # The checklist must reflect the official form behavior captured in the current v52 public receipt.
    for phrase in [
        "MAX_TRACK2_SUBMISSIONS",
        "Team Participation",
        "When saving your report, please include your username (or team name) in the filename",
        "GitHub URL must start with `https://github.com/`",
        "A pitch video URL is required",
        "Report must be a PDF (.pdf) or Markdown (.md) file",
        "Team / Display Name (optional)",
        "GitHub repo URL *",
        "Pitch video URL *",
        "Report file (PDF or Markdown) *",
        "Notes for judges (optional)",
    ]:
        require(phrase in official, "Official submit-form behavior not captured: " + phrase)

    for key in ["report_pdf", "report_markdown", "methods_workbook", "slide_pdf"]:
        record = materials[key]
        path = ROOT / record["path"]
        if path.is_file():
            require(path.stat().st_size == record["bytes"] and digest(path) == record["sha256"], "Submission-material receipt drift: " + key)
    require("jvv7" in note, "Current filename convention omitted")
    identity = state.get("submission_identity", {})
    require(identity == {
        "owner_selected_date": "2026-10-23",
        "huggingface_username": "jvv7",
        "team_display_name": "Aeglos",
        "report_filename_convention": "jvv7",
        "authenticated_account_verified": False,
        "quota_checked": False,
    }, "Owner-selected public identity drift")
    require("sha-256" in text and "byte count" in text, "Receipt archive fields omitted")
    require("outside the deletion scope" in text, "Receipt-retention scope omitted")

    return {
        "passed": True,
        "version": 16,
        "huggingface_username": "jvv7",
        "team_display_name": "Aeglos",
        "authenticated_account_verified": False,
        "report_pdf_bytes": materials["report_pdf"]["bytes"],
        "report_md_bytes": materials["report_markdown"]["bytes"],
        "workbook_bytes": materials["methods_workbook"]["bytes"],
        "slide_pdf_bytes": materials["slide_pdf"]["bytes"],
        "bundle_bytes": exact_files["bundle"].stat().st_size if exact_files["bundle"].is_file() else None,
        "report_pdf_sha256": materials["report_pdf"]["sha256"],
        "report_md_sha256": materials["report_markdown"]["sha256"],
        "video_recorded": False,
        "video_url": None,
        "upload_ready": False,
        "upload_performed": False,
        "biological_validation": False,
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
