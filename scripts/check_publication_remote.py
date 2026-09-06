"""Check GitHub visibility and removed-object availability without emitting blob bodies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = "Vijayavallabh/mva-hackathon-2026"


def removed_object_status(oid: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", oid):
        raise ValueError("invalid object identifier")
    result = subprocess.run(
        ["gh", "api", "--silent", f"repos/{REPOSITORY}/git/blobs/{oid}"],
        capture_output=True,
    )
    if result.returncode == 0:
        return "retrievable"
    if b"HTTP 404" in result.stderr:
        return "not_found"
    return "unknown_error"


def availability_gate(control_status: str, statuses: list[dict[str, str]]) -> bool:
    return (control_status == "retrievable" and bool(statuses)
            and all(item["status"] == "not_found" for item in statuses))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=ROOT / "notes/publication-removed-objects.json")
    parser.add_argument("--output", type=Path, default=ROOT / "results/feat007/remote-gate.json")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        for returncode, stderr, expected in (
            (0, b"", "retrievable"),
            (1, b"gh: Not Found (HTTP 404)", "not_found"),
            (1, b"authentication required (HTTP 401)", "unknown_error"),
            (1, b"connection failed", "unknown_error"),
        ):
            result = subprocess.CompletedProcess([], returncode, b"", stderr)
            with patch("subprocess.run", return_value=result):
                assert removed_object_status("a" * 40) == expected
        missing = [{"status": "not_found"}]
        assert availability_gate("retrievable", missing)
        assert not availability_gate("not_found", missing)
        assert not availability_gate("unknown_error", missing)
        assert not availability_gate("retrievable", [{"status": "retrievable"}])
        print("remote publication self-check: missing, retained and unknown objects distinguished")
        return
    manifest = json.loads(args.manifest.read_text())
    if manifest["repository"] != REPOSITORY:
        raise ValueError("removed-object inventory belongs to a different repository")
    objects = manifest["removed_blob_ids"]
    if not objects or len(objects) != len(set(objects)):
        raise ValueError("expected a nonempty unique removed-object inventory")
    query = subprocess.run(
        ["gh", "repo", "view", REPOSITORY, "--json", "visibility,url,nameWithOwner"],
        capture_output=True,
    )
    if query.returncode:
        raise RuntimeError("cannot establish GitHub repository identity/visibility")
    identity = json.loads(query.stdout)
    if identity["nameWithOwner"] != REPOSITORY:
        raise ValueError("unexpected GitHub repository")
    control_query = subprocess.run(
        ["gh", "api", f"repos/{REPOSITORY}/contents/README.md?ref=main", "--jq", ".sha"],
        capture_output=True,
    )
    if control_query.returncode:
        raise RuntimeError("cannot establish a known reachable remote blob for access control")
    control_oid = control_query.stdout.decode().strip()
    control_status = removed_object_status(control_oid)
    statuses = [{"object": oid, "status": removed_object_status(oid)} for oid in objects]
    report = {"repository": identity,
              "removed_objects_checked": len(statuses),
              "still_retrievable": sum(x["status"] == "retrievable" for x in statuses),
              "unknown_errors": sum(x["status"] == "unknown_error" for x in statuses),
              "reachable_blob_control": {"object": control_oid, "status": control_status},
              "objects": statuses,
              "removed_object_gate_passed": availability_gate(control_status, statuses)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "objects"}, indent=2))
    raise SystemExit(0 if report["removed_object_gate_passed"] else 1)


if __name__ == "__main__":
    main()
