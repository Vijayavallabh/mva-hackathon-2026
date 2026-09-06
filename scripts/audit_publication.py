"""Audit Git contents locally without emitting protected text or matching snippets.

All refs and their reachable blobs/commit metadata are checked by default. The local
phenotype source supplies the comparison vocabulary; it never enters the report.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
WORD = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
FORBIDDEN_PATH = re.compile(
    r"(^|/)(data|results|logs|\.venv|\.uv-cache)/|"
    r"\.(fastq|fq|bam|cram|vcf|bcf|docx)(\.gz)?($|\.)|"
    r"\.(bai|crai|tbi)$|(^|/)\.env($|\.)", re.I
)
SECRET = re.compile(
    r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|"
    r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{40,}|"
    r"hf_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16})\b"
)
VCF_RECORD = re.compile(
    r"^(?:chr)?(?:[0-9]{1,2}|X|Y|MT)\t[0-9]+\t[^\t\n]+\t[ACGTN]+\t"
    r"(?:[ACGTN]+|<[^>]+>)[\t,]", re.M
)


def git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if result.returncode:
        # Git errors can quote content or protected paths; fail without forwarding them.
        raise RuntimeError(f"git operation failed: {args[0]}")
    return result.stdout


def words(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.casefold())


def ngrams(text: str, size: int) -> set[tuple[str, ...]]:
    tokens = words(text)
    return {tuple(tokens[i:i + size]) for i in range(len(tokens) - size + 1)}


def source_patterns(docx: Path) -> dict[int, set[tuple[str, ...]]]:
    with zipfile.ZipFile(docx) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    tables = root.findall(".//w:tbl", WORD)
    if len(tables) != 1:
        raise ValueError("expected exactly one phenotype table")
    rows = tables[0].findall("w:tr", WORD)
    cells = [
        ["".join(t.text or "" for t in cell.findall(".//w:t", WORD))
         for cell in row.findall("w:tc", WORD)]
        for row in rows
    ]
    headers = [value.casefold() for value in cells[0]]
    feature = next(i for i, h in enumerate(headers) if "clinical" in h and "feature" in h)
    notes = next(i for i, h in enumerate(headers) if "present" in h and "note" in h)
    label = next(i for i, h in enumerate(headers) if "hpo" in h and "term" in h)
    permitted = set().union(*(ngrams(row[label], 3) for row in cells[1:]))
    table = set().union(*(ngrams(row[i], 3) for row in cells[1:] for i in (feature, notes)))
    # Longer narrative passages outside the table are checked too. Three-word matches
    # there would also flag generic scientific prose and document section headings.
    paragraphs = ["".join(t.text or "" for t in p.findall(".//w:t", WORD))
                  for p in root.findall(".//w:p", WORD)]
    narrative = set().union(*(ngrams(p, 8) for p in paragraphs))
    if len(cells) != 9 or not table or not narrative:
        raise ValueError("incomplete phenotype comparison vocabulary")
    return {3: table - permitted, 8: narrative}


def text_findings(text: str, patterns: dict[int, set[tuple[str, ...]]]) -> dict[str, int]:
    result = {f"protected_{size}word_matches": len(ngrams(text, size) & tokens)
              for size, tokens in patterns.items()}
    result["credential_patterns"] = len(SECRET.findall(text))
    result["vcf_record_patterns"] = len(VCF_RECORD.findall(text))
    return {key: count for key, count in result.items() if count}


def audit(repo: Path, patterns: dict[int, set[tuple[str, ...]]], current: bool = False,
          staged: bool = False):
    refs = git(repo, "for-each-ref", "--format=%(refname) %(objectname)").decode().splitlines()
    commits = git(repo, "rev-list", "HEAD" if current else "--all").decode().splitlines()
    if current:
        commits = commits[:1]
    if not refs or not commits:
        raise ValueError("refusing empty repository audit")
    blobs: dict[str, set[str]] = {}
    findings = []
    if not staged and not current:
        for line in git(repo, "rev-list", "--objects", "--all").decode().splitlines():
            oid = line.split()[0]
            if git(repo, "cat-file", "-t", oid).strip() == b"tag":
                metadata = git(repo, "cat-file", "tag", oid).decode("utf-8", errors="replace")
                matches = text_findings(metadata, patterns)
                if matches:
                    findings.append({"kind": "tag", "object": oid, "counts": matches})
    for commit in ([] if staged else commits):
        metadata = git(repo, "cat-file", "commit", commit).decode("utf-8", errors="replace")
        matches = text_findings(metadata, patterns)
        if matches:
            findings.append({"kind": "commit", "object": commit, "counts": matches})
        for record in git(repo, "ls-tree", "-rz", commit).split(b"\0"):
            if not record:
                continue
            meta, raw_path = record.split(b"\t", 1)
            mode, kind, oid = meta.decode().split()
            path = raw_path.decode("utf-8", errors="replace")
            if FORBIDDEN_PATH.search(path) or mode in ("120000", "160000"):
                findings.append({"kind": "forbidden_path_or_link", "commit": commit,
                                 "path": path})
            if kind == "blob":
                blobs.setdefault(oid, set()).add(path)
    if staged:
        for record in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
            if not record:
                continue
            metadata, raw_path = record.split(b"\t", 1)
            mode, oid, stage = metadata.decode().split()
            path = raw_path.decode("utf-8", errors="replace")
            if stage != "0" or FORBIDDEN_PATH.search(path) or mode in ("120000", "160000"):
                findings.append({"kind": "forbidden_or_unmerged_index_entry", "path": path})
            blobs.setdefault(oid, set()).add(path)
    for oid, paths in sorted(blobs.items()):
        size = int(git(repo, "cat-file", "-s", oid))
        if size > 5_000_000:
            findings.append({"kind": "oversized_blob", "object": oid, "paths": sorted(paths)})
            continue
        content = git(repo, "cat-file", "blob", oid)
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            findings.append({"kind": "binary_blob", "object": oid, "paths": sorted(paths)})
            continue
        matches = text_findings(text, patterns)
        if matches:
            findings.append({"kind": "blob", "object": oid, "paths": sorted(paths),
                             "counts": matches})
    return {"scope": "index" if staged else "HEAD" if current else "all_refs", "refs": refs,
            "commits_checked": 0 if staged else len(commits), "unique_blobs_checked": len(blobs),
            "findings": findings, "passed": not findings}


def self_check():
    patterns = {3: {("fixture", "private", "phrase")}, 8: set()}
    assert text_findings("fixture PRIVATE phrase", patterns)
    assert not text_findings("permitted phenotype label", patterns)
    assert FORBIDDEN_PATH.search("archive/sample.vcf.gz.tbi")
    assert FORBIDDEN_PATH.search("data/nested.txt")
    with tempfile.TemporaryDirectory(prefix="publication-audit-") as name:
        repo = Path(name)
        git(repo, "init", "-q")
        git(repo, "config", "user.name", "Audit fixture")
        git(repo, "config", "user.email", "fixture@example.invalid")
        (repo / "note.md").write_text("fixture private phrase\n")
        git(repo, "add", "note.md")
        git(repo, "commit", "-qm", "old fixture")
        (repo / "note.md").write_text("clean present text\n")
        git(repo, "commit", "-qam", "clean fixture")
        assert audit(repo, patterns, current=True)["passed"]
        assert not audit(repo, patterns)["passed"]
        git(repo, "tag", "-a", "fixture-tag", "-m", "fixture private phrase")
        assert any(item["kind"] == "tag" for item in audit(repo, patterns)["findings"])
    print("publication audit self-check: historical disclosure detected; current tree clean")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--docx", type=Path, default=ROOT / "data/Challenge_Clinical_Phenotype_1.docx")
    parser.add_argument("--current", action="store_true")
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if args.current and args.staged:
        parser.error("--current and --staged are mutually exclusive")
    report = audit(args.repo, source_patterns(args.docx), args.current, args.staged)
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(encoded, end="")
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
