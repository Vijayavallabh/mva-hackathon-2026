"""Verify ./data matches the HF dataset repo file-for-file, byte-for-byte in size.

Run standalone: uv run python scripts/verify_data.py
Exits non-zero if anything is missing or truncated.
"""
import sys
from pathlib import Path

from huggingface_hub import HfApi

REPO = "SageBio/mva-hackathon-2026-data"
DATA = Path(__file__).resolve().parent.parent / "data"

# Repo metadata, not subject data. Excluded from download and edited upstream
# after ours landed, so size-checking them yields a permanent false INCOMPLETE.
SKIP = {"README.md", ".gitattributes"}


def check(data_dir: Path = DATA) -> list[str]:
    """Return a list of problems; empty list means the download is complete."""
    api = HfApi()
    problems = []
    for f in api.list_repo_tree(REPO, repo_type="dataset", recursive=True):
        want = getattr(f, "size", None)
        if want is None:  # directory entry
            continue
        if f.path in SKIP:
            continue
        local = data_dir / f.path
        if not local.exists():
            problems.append(f"MISSING  {f.path}")
        elif local.stat().st_size != want:
            problems.append(f"TRUNCATED {f.path} {local.stat().st_size}/{want}")
    return problems


def demo() -> None:
    """Self-check: an empty directory must report every remote file as missing."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        assert check(Path(tmp)), "checker reported OK against an empty dir"
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
