"""Verify ./data matches the HF dataset repo file-for-file, byte-for-byte in size.

Run standalone: uv run python scripts/verify_data.py
Exits non-zero if anything is missing or truncated.
"""
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple

from huggingface_hub import HfApi

REPO = "SageBio/mva-hackathon-2026-data"
DATA = Path(__file__).resolve().parent.parent / "data"

# Repo metadata, not subject data. Excluded from download and edited upstream
# after ours landed, so size-checking them yields a permanent false INCOMPLETE.
SKIP = {"README.md", ".gitattributes"}


class ExpectedFile(NamedTuple):
    path: str
    size: int


def check(
    data_dir: Path = DATA, repo_files: Iterable[object] | None = None
) -> list[str]:
    """Return a list of problems; empty list means the download is complete."""
    if repo_files is None:
        api = HfApi()
        repo_files = api.list_repo_tree(REPO, repo_type="dataset", recursive=True)

    problems = []
    for f in repo_files:
        want = getattr(f, "size", None)
        if want is None:  # directory entry
            continue
        path = getattr(f, "path")
        if path in SKIP:
            continue
        local = data_dir / path
        if not local.exists():
            problems.append(f"MISSING  {path}")
        elif local.stat().st_size != want:
            problems.append(f"TRUNCATED {path} {local.stat().st_size}/{want}")
    return problems


def demo() -> None:
    """Exercise missing, truncated, and complete cases without network access."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        data_dir = Path(tmp)
        expected = [ExpectedFile("fixture.bin", 3)]
        assert check(data_dir, expected) == ["MISSING  fixture.bin"]
        (data_dir / "fixture.bin").write_bytes(b"xx")
        assert check(data_dir, expected) == ["TRUNCATED fixture.bin 2/3"]
        (data_dir / "fixture.bin").write_bytes(b"xxx")
        assert check(data_dir, expected) == []
    print("self-check ok")


if __name__ == "__main__":
    if "--self-check" in sys.argv:
        demo()
        raise SystemExit(0)
    bad = check()
    for p in bad:
        print(p)
    total = sum(f.stat().st_size for f in DATA.rglob("*") if f.is_file())
    print(f"{total / 1e9:.2f} GB in {DATA}")
    print("INCOMPLETE" if bad else "COMPLETE: all files present at expected size")
    raise SystemExit(1 if bad else 0)
