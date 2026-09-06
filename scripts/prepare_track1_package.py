"""Build and verify a local Track 1 CSV/report package. This script never uploads.

Fresh live preflight is separate from reproducible offline package verification. A
successful offline check is not an upload receipt and never consumes a submission.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from audit_publication import audit, source_patterns, text_findings
from track1_submission import (
    ROOT, DEFAULT_CANDIDATES, DEFAULT_REFERENCE, DEFAULT_BCFTOOLS,
    OFFICIAL_REVISION,
    build_submission, check_submission, read_submission, sha256,
)

CONFIG = ROOT / "notes/track1-submission-config.json"
TEMPLATE = ROOT / "notes/track1-report-template.md"
OUT = ROOT / "results/feat008"
SPACE = "SageBio/rare-disease-real-kid-mva-hackathon-2026"
PORTAL_PATH = "tabs/submit_track1.py"
PORTAL_SHA256 = "685a3b6d57ef3a1c49a8be47845b10d77cb576ed2d30b5a90879b09707659b86"
AI_FIELDS = ("ai_provider", "ai_tool", "ai_plan_or_tier", "ai_data_handling_setting", "other_ai_providers")
REPOSITORY = "Vijayavallabh/mva-hackathon-2026"
CODE_FILES = [
    "scripts/prepare_track1_package.py", "scripts/track1_submission.py",
    "scripts/vendor/evaluation.py", "scripts/track1_submission_template.csv",
    "scripts/audit_publication.py", "scripts/check_publication_remote.py",
    "scripts/rank_candidates.py", "scripts/run_vcf_triage.sh",
    "scripts/run_targeted_recall.sh", "scripts/analyze_targeted_recall.py",
    "scripts/run_copy_number_screen.sh", "scripts/analyze_copy_number.py",
    "notes/track1-report-template.md", "notes/track1-submission-config.json",
    "tools/versions.tsv", "tools/resources.tsv", "pyproject.toml", "uv.lock",
]
BASELINE_QC = ROOT / "results/feat004/candidate_qc.json"
RECALL_SUMMARY = ROOT / "results/feat005b/summary.json"
EVIDENCE = [DEFAULT_CANDIDATES, BASELINE_QC, RECALL_SUMMARY]


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def required_config(config: dict) -> None:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", config["hf_username"]):
        raise ValueError("invalid HF username")
    if config["github_url"] != f"https://github.com/{REPOSITORY}":
        raise ValueError("unexpected repository URL")
    if type(config["require_public_repository_before_upload"]) is not bool:
        raise ValueError("public-first policy must be explicit")
    for key in ("display_name", *AI_FIELDS):
        value = config[key]
        if value is not None and (not isinstance(value, str) or "\n" in value):
            raise ValueError(f"invalid single-line disclosure field: {key}")


def missing_disclosure(config: dict) -> list[str]:
    return [key for key in AI_FIELDS if not config.get(key) or
            str(config[key]).strip().upper() in {"", "UNCONFIRMED", "UNKNOWN", "TODO"}]


def ranking_table(rows: list[dict]) -> str:
    lines = ["| Rank | Gene | Allele 1 (GRCh38) | Allele 2 (GRCh38) | EPCR |",
             "|---|---|---|---|---|"]
    for rank, row in enumerate(rows, 1):
        gene = row["notes"].split()[0]
        alleles = [f"{row[f'chrom_{s}']}:{row[f'pos_{s}']} {row[f'ref_{s}']}>{row[f'alt_{s}']}"
                   for s in ("1", "2")]
        lines.append(f"| {rank} | {gene} | {alleles[0]} | {alleles[1]} | {row['epcr']} |")
    return "\n".join(lines)


def render_report(rows: list[dict], config: dict, revision: str, csv_hash: str, name: str) -> str:
    disclosure = "; ".join(
        f"{label}: {config.get(key) or 'UNCONFIRMED — owner input required'}"
        for key, label in (
            ("ai_provider", "Provider"), ("ai_tool", "Tool"),
            ("ai_plan_or_tier", "Plan/tier"),
            ("ai_data_handling_setting", "Account data-handling setting"),
            ("other_ai_providers", "Other AI providers used"),
        )
    ) + "."
    replacements = {
        "PARTICIPANT": config["display_name"] or config["hf_username"],
        "GITHUB_URL": config["github_url"], "CODE_REVISION": revision,
        "CSV_SHA256": csv_hash, "PACKAGE_NAME": name,
        "AI_DISCLOSURE": disclosure, "RANKING_TABLE": ranking_table(rows),
    }
    text = TEMPLATE.read_text()
    for key, value in replacements.items():
        text = text.replace("{{" + key + "}}", value)
    if "{{" in text or "}}" in text:
        raise ValueError("unresolved report template field")
    return text


def assert_evidence() -> None:
    qc = json.loads(BASELINE_QC.read_text())
    expected = {"annotated_rare_damaging_variants": 418,
                "compound_heterozygous_pair_hypotheses": 169, "dominant_singleton_hypotheses": 195}
    if any(qc.get(k) != v for k, v in expected.items()):
        raise ValueError("baseline evidence changed; review report before packaging")
    recall = json.loads(RECALL_SUMMARY.read_text())
    expected = {"delly_pass_calls_in_target_enriched_bam": 984,
                "delly_pass_calls_overlapping_target_gene_windows": 125,
                "novel_existing_allele_reconstructions": 314,
                "genes_with_novel_existing_allele_reconstructions": 63,
                "supported_rare_coding_splice_deep_intronic_or_repeat_adjacent_candidates": 226}
    if any(recall.get(k) != v for k, v in expected.items()):
        raise ValueError("recall evidence changed; review report before packaging")
    if recall["candidate_class_counts"] != {
        "coding_or_splice": 13, "deep_intronic_ge20bp": 203, "repeat_adjacent": 62
    } or recall["leading_pair_read_backed_phase"]["status"] != "unconfirmed":
        raise ValueError("recall classes or phase changed; review report")


def assert_leading_pair(rows: list[dict]) -> None:
    row = rows[0]
    expected = {("chr15", "40209701", "T", "G"), ("chr15", "40220612", "T", "G")}
    actual = {tuple(row[f"{f}_{s}"] for f in ("chrom", "pos", "ref", "alt")) for s in ("1", "2")}
    if actual != expected or not row["notes"].startswith("BUB1B "):
        raise ValueError("leading pair differs from reviewed report")


def build(name: str) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]+", name):
        raise ValueError("package name must contain only letters, digits, underscore or hyphen")
    if git("status", "--porcelain"):
        raise ValueError("commit all intended changes before building an immutable package")
    config = json.loads(CONFIG.read_text())
    required_config(config)
    if not name.startswith(config["hf_username"] + "_"):
        raise ValueError("package filename must start with the authenticated participant name")
    assert_evidence()
    directory = OUT / name
    directory.mkdir(parents=True, exist_ok=False)
    csv_path = directory / f"{name}.csv"
    report_path = directory / f"{name}_report.md"
    build_submission(DEFAULT_CANDIDATES, csv_path)
    checked = check_submission(csv_path, DEFAULT_REFERENCE, DEFAULT_BCFTOOLS, True, 1)
    rows = read_submission(csv_path)
    assert_leading_pair(rows)
    revision = git("rev-parse", "HEAD")
    report_path.write_text(render_report(rows, config, revision, sha256(csv_path), name))
    patterns = source_patterns(ROOT / "data/Challenge_Clinical_Phenotype_1.docx")
    for path in (csv_path, report_path):
        if text_findings(path.read_text(), patterns):
            raise ValueError("package disclosure check failed; nothing uploaded")
    check_path = directory / "local-check.json"
    check_path.write_text(json.dumps(checked, indent=2) + "\n")
    manifest = {
        "schema_version": 1, "package_name": name, "code_revision": revision,
        "created_at": datetime.now(timezone.utc).isoformat(), "config": config,
        "files": {p.name: sha256(p) for p in (csv_path, report_path, check_path)},
        "code_files": {p: sha256(ROOT / p) for p in CODE_FILES},
        "evidence_files": {str(p.relative_to(ROOT)): sha256(p) for p in EVIDENCE},
        "csv_file": csv_path.name, "report_file": report_path.name,
        "official_revision": OFFICIAL_REVISION, "portal_sha256": PORTAL_SHA256,
        "unresolved_disclosure_fields": missing_disclosure(config),
        "upload_performed": False,
    }
    (directory / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return verify(directory)


def verify_payload_files(directory: Path, manifest: dict) -> None:
    name = manifest["package_name"]
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]+", name):
        raise ValueError("invalid package name")
    expected_files = {f"{name}.csv", f"{name}_report.md", "local-check.json"}
    if set(manifest["files"]) != expected_files or any(Path(p).name != p for p in expected_files):
        raise ValueError("invalid package file inventory")
    if manifest["csv_file"] != f"{name}.csv" or manifest["report_file"] != f"{name}_report.md":
        raise ValueError("invalid deliverable filenames")
    for filename, expected in manifest["files"].items():
        path = directory / filename
        if path.is_symlink() or not path.is_file() or sha256(path) != expected:
            raise ValueError(f"package bytes changed or missing: {filename}")


def verify(directory: Path) -> dict:
    directory = directory.resolve()
    manifest = json.loads((directory / "manifest.json").read_text())
    if (manifest["schema_version"] != 1 or manifest["official_revision"] != OFFICIAL_REVISION
            or manifest["portal_sha256"] != PORTAL_SHA256):
        raise ValueError("unsupported package version or official contract")
    config = manifest["config"]
    required_config(config)
    verify_payload_files(directory, manifest)
    name = manifest["package_name"]
    if not name.startswith(config["hf_username"] + "_"):
        raise ValueError("package name does not identify configured participant")
    if manifest["unresolved_disclosure_fields"] != missing_disclosure(config) or manifest["upload_performed"] is not False:
        raise ValueError("manifest misstates disclosure or upload status")
    revision = manifest["code_revision"]
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("invalid code revision")
    if subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", revision, "HEAD"],
                      capture_output=True).returncode:
        raise ValueError("package revision is not in current history")
    if set(manifest["code_files"]) != set(CODE_FILES):
        raise ValueError("incomplete code provenance")
    if set(manifest["evidence_files"]) != {str(p.relative_to(ROOT)) for p in EVIDENCE}:
        raise ValueError("incomplete evidence provenance")
    for group in ("code_files", "evidence_files"):
        for relative, expected in manifest[group].items():
            if sha256(ROOT / relative) != expected:
                raise ValueError(f"{group} changed; build a new package after review")
            if group == "code_files":
                committed = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{revision}:{relative}"])
                if hashlib.sha256(committed).hexdigest() != expected:
                    raise ValueError("code provenance does not match recorded revision")
    if json.loads(CONFIG.read_text()) != config:
        raise ValueError("submission settings changed; build a new package")
    assert_evidence()
    csv_path = directory / manifest["csv_file"]
    rows = read_submission(csv_path)
    assert_leading_pair(rows)
    report = (directory / manifest["report_file"]).read_text()
    expected_report = render_report(rows, config, manifest["code_revision"], sha256(csv_path), name)
    if report != expected_report:
        raise ValueError("report does not correspond to this CSV/config/revision")
    checked = check_submission(csv_path, DEFAULT_REFERENCE, DEFAULT_BCFTOOLS, True, 1)
    stored = json.loads((directory / "local-check.json").read_text())
    # A copied package has a different path but must retain identical checked bytes.
    if {k: v for k, v in stored.items() if k != "submission"} != {
        k: v for k, v in checked.items() if k != "submission"
    }:
        raise ValueError("stored local check differs from a fresh validation")
    patterns = source_patterns(ROOT / "data/Challenge_Clinical_Phenotype_1.docx")
    if any(text_findings(path.read_text(), patterns)
           for path in (csv_path, directory / manifest["report_file"])):
        raise ValueError("package fails current disclosure check")
    return {"package": str(directory), "offline_valid": True,
            "csv_sha256": sha256(csv_path), "report_sha256": sha256(directory / manifest["report_file"]),
            "row_count": checked["row_count"],
            "reference_normalized_alleles": checked["reference_normalized_alleles"],
            "unresolved_disclosure_fields": missing_disclosure(config),
            "upload_performed": False}


def upstream_is_synchronized() -> bool:
    """Check the actual configured origin branch, not only its cached tracking ref."""
    try:
        branch = git("symbolic-ref", "--short", "HEAD")
        remote = git("config", "--get", f"branch.{branch}.remote")
        merge = git("config", "--get", f"branch.{branch}.merge")
        if remote != "origin" or not merge.startswith("refs/heads/"):
            return False
        response = subprocess.run(["git", "-C", str(ROOT), "ls-remote", "--exit-code", remote, merge],
                                  capture_output=True, text=True, timeout=30)
        expected = f"{git('rev-parse', 'HEAD')}\t{merge}"
        return (response.returncode == 0 and response.stdout.strip() == expected
                and git("rev-parse", "HEAD") == git("rev-parse", "@{u}"))
    except (subprocess.SubprocessError, OSError):
        return False


def publication_blockers(public_first: bool, visibility: str, purge_passed: bool | None) -> list[str]:
    blockers = []
    if visibility not in {"PRIVATE", "PUBLIC"}:
        blockers.append("GitHub repository visibility is not verified PRIVATE or PUBLIC")
    if public_first and visibility != "PUBLIC":
        blockers.append("repository policy requires PUBLIC visibility before upload")
    if (public_first or visibility == "PUBLIC") and purge_passed is not True:
        blockers.append("GitHub removed-object purge gate has not passed")
    return blockers


def preflight(directory: Path) -> dict:
    result = verify(directory)
    config = json.loads((directory / "manifest.json").read_text())["config"]
    blockers = [f"AI disclosure missing: {k}" for k in missing_disclosure(config)]
    if git("status", "--porcelain") or not upstream_is_synchronized():
        blockers.append("working tree or upstream is not synchronized")
    if not audit(ROOT, source_patterns(ROOT / "data/Challenge_Clinical_Phenotype_1.docx"))["passed"]:
        blockers.append("reachable-history disclosure audit failed")
    remote = subprocess.run(["gh", "repo", "view", REPOSITORY, "--json", "visibility,url"],
                            capture_output=True, text=True)
    if remote.returncode:
        blockers.append("GitHub repository status unavailable")
        visibility = "UNKNOWN"
    else:
        visibility = json.loads(remote.stdout)["visibility"]
    public_first = config["require_public_repository_before_upload"]
    purge_passed = None
    if public_first or visibility == "PUBLIC":
        removed = subprocess.run(["uv", "run", "python", str(ROOT / "scripts/check_publication_remote.py")],
                                 cwd=ROOT, capture_output=True)
        purge_passed = removed.returncode == 0
    blockers.extend(publication_blockers(public_first, visibility, purge_passed))
    source_url = f"https://huggingface.co/spaces/{SPACE}/resolve/main/{PORTAL_PATH}"
    try:
        head = subprocess.run(["git", "ls-remote", f"https://huggingface.co/spaces/{SPACE}.git", "HEAD"],
                              capture_output=True, text=True, timeout=30)
        if head.returncode or head.stdout.split()[0] != OFFICIAL_REVISION:
            blockers.append("official Space revision changed or unavailable; review before upload")
        with urllib.request.urlopen(source_url, timeout=30) as response:
            current = hashlib.sha256(response.read()).hexdigest()
        if current != PORTAL_SHA256:
            blockers.append("official upload contract changed; review before using a submission")
    except Exception:
        blockers.append("cannot verify current official upload contract")
    result.update({"github_visibility": visibility, "blockers": blockers,
                   "ready_for_authenticated_submission": not blockers})
    # Quota is an authenticated portal fact. This program does not invent remaining attempts.
    result["remaining_attempts"] = "must verify in authenticated portal immediately before upload"
    return result


def self_check():
    config = json.loads(CONFIG.read_text())
    required_config(config)
    unresolved = dict(config, ai_plan_or_tier=None)
    assert "ai_plan_or_tier" in missing_disclosure(unresolved)
    invalid = dict(config, require_public_repository_before_upload="false")
    try:
        required_config(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError("string false must not bypass public-first policy")
    with tempfile.TemporaryDirectory(prefix="track1-package-check-") as name:
        directory = Path(name)
        filenames = ["fixture.csv", "fixture_report.md", "local-check.json"]
        for filename in filenames:
            (directory / filename).write_text("fixture bytes")
        manifest = {"package_name": "fixture", "csv_file": "fixture.csv",
                    "report_file": "fixture_report.md",
                    "files": {p: sha256(directory / p) for p in filenames}}
        verify_payload_files(directory, manifest)
        for filename in filenames:
            path = directory / filename
            path.write_text("tampered")
            try:
                verify_payload_files(directory, manifest)
            except ValueError:
                pass
            else:
                raise AssertionError("edited deliverable accepted")
            path.write_text("fixture bytes")
        path.unlink()
        path.symlink_to(directory / "fixture.csv")
        try:
            verify_payload_files(directory, manifest)
        except ValueError:
            pass
        else:
            raise AssertionError("symlink deliverable accepted")
    print("package self-check: disclosure, explicit policy, three tamper cases and symlink rejection pass")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check", action="store_true")
    commands = parser.add_subparsers(dest="command")
    build_cmd = commands.add_parser("build")
    build_cmd.add_argument("--name", required=True)
    for command in ("verify", "preflight"):
        commands.add_parser(command).add_argument("package", type=Path)
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if args.command == "build":
        result = build(args.name)
    elif args.command == "verify":
        result = verify(args.package)
    elif args.command == "preflight":
        result = preflight(args.package)
    else:
        parser.error("choose build, verify or preflight")
    print(json.dumps(result, indent=2))
    if args.command == "preflight" and not result["ready_for_authenticated_submission"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
