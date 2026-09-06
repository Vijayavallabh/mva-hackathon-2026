"""Offline regression checks on a copied, locally generated Track 1 package.

Only the four small package files are copied. No upload or source-data copy occurs.
"""

import argparse
import json
import shutil
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from prepare_track1_package import publication_blockers, upstream_is_synchronized, verify
from track1_submission import sha256


def run_checks(package: Path) -> None:
    for public_first in (True, False):
        for visibility in ("PRIVATE", "PUBLIC", "UNKNOWN"):
            for purged in (True, False, None):
                allowed = not publication_blockers(public_first, visibility, purged)
                expected = ((visibility == "PRIVATE" and not public_first)
                            or (visibility == "PUBLIC" and purged is True))
                assert allowed == expected, (public_first, visibility, purged)
    revision = "a" * 40
    answers = {("symbolic-ref", "--short", "HEAD"): "main",
               ("config", "--get", "branch.main.remote"): "origin",
               ("config", "--get", "branch.main.merge"): "refs/heads/main",
               ("rev-parse", "HEAD"): revision, ("rev-parse", "@{u}"): revision}
    with patch("prepare_track1_package.git", side_effect=lambda *args: answers[args]):
        for remote_revision, exit_code, expected in ((revision, 0, True), ("b" * 40, 0, False),
                                                     (revision, 1, False)):
            with patch("prepare_track1_package.subprocess.run", return_value=SimpleNamespace(
                returncode=exit_code, stdout=f"{remote_revision}\trefs/heads/main\n"
            )):
                assert upstream_is_synchronized() == expected
    verify(package)
    mutations = (
        "csv_bytes", "report_bytes", "check_bytes", "symlink", "inventory",
        "report_rehashed", "wrong_revision", "false_upload", "false_disclosure",
    )
    with tempfile.TemporaryDirectory(prefix="track1-package-regression-") as temporary:
        root = Path(temporary)
        copied = root / "portable"
        copied.mkdir()
        original = json.loads((package / "manifest.json").read_text())
        for filename in ["manifest.json", *original["files"]]:
            shutil.copyfile(package / filename, copied / filename)
        assert verify(copied)["offline_valid"], "unchanged copied package must verify"
        for mutation in mutations:
            directory = root / mutation
            shutil.copytree(copied, directory)
            manifest_path = directory / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            csv_path = directory / manifest["csv_file"]
            report_path = directory / manifest["report_file"]
            if mutation == "csv_bytes":
                csv_path.write_text(csv_path.read_text() + "edited")
            elif mutation in {"report_bytes", "report_rehashed"}:
                report_path.write_text(report_path.read_text() + "edited")
                if mutation == "report_rehashed":
                    manifest["files"][report_path.name] = sha256(report_path)
            elif mutation == "check_bytes":
                (directory / "local-check.json").write_text("{}")
            elif mutation == "symlink":
                csv_path.unlink()
                csv_path.symlink_to(copied / csv_path.name)
            elif mutation == "inventory":
                manifest["files"]["../unexpected"] = "0" * 64
            elif mutation == "wrong_revision":
                manifest["code_revision"] = "0" * 40
            elif mutation == "false_upload":
                manifest["upload_performed"] = True
            elif mutation == "false_disclosure":
                manifest["unresolved_disclosure_fields"] = ["fabricated"]
            manifest_path.write_text(json.dumps(manifest))
            try:
                verify(directory)
            except ValueError:
                pass
            else:
                raise AssertionError(f"mutation accepted: {mutation}")
    print(f"package regression: 18 publication-policy cases, 3 live-upstream cases, portable copy, "
          f"{len(mutations)} corruptions pass; no upload")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    run_checks(parser.parse_args().package.resolve())
