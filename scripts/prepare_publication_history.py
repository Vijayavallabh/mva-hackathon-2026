"""Prepare a scrubbed mirror locally; never pushes or changes repository visibility.

The private source stays in memory. Only sanitized blob replacements and count/hash
reports are written under results/feat007. Source refs and the working tree are untouched.
"""

from __future__ import annotations

import argparse
import ast
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

from audit_publication import ROOT, audit, git, ngrams, source_patterns


def redact(text: str, patterns: dict[int, set[tuple[str, ...]]]) -> tuple[str, int]:
    """Break matched phrases by replacing words while retaining code punctuation.

    This intentionally favors conservative historical redaction over inferring whether
    an otherwise-public phrase was copied from the protected source.
    """
    tokens = list(re.finditer(r"[a-z]+", text, re.I))
    indices: set[int] = set()
    for size, protected in patterns.items():
        for i in range(len(tokens) - size + 1):
            if tuple(t.group().casefold() for t in tokens[i:i + size]) in protected:
                indices.add(i + size // 2)
    for index in sorted(indices, reverse=True):
        token = tokens[index]
        text = text[:token.start()] + "redacted" + text[token.end():]
    if any(ngrams(text, size) & protected for size, protected in patterns.items()):
        raise ValueError("redaction did not remove all phrase matches")
    return text, len(indices)


def prepare(destination: Path) -> dict:
    parent = (ROOT / "results/feat007").resolve()
    destination = destination.resolve()
    if destination.parent != parent or destination.exists():
        raise ValueError("destination must be a new direct child of results/feat007")
    parent.mkdir(parents=True, exist_ok=True)
    if git(ROOT, "status", "--porcelain"):
        raise ValueError("commit working-tree changes before preparing history")
    patterns = source_patterns(ROOT / "data/Challenge_Clinical_Phenotype_1.docx")
    before = audit(ROOT, patterns)
    replacements = {}
    changes = []
    for finding in before["findings"]:
        if finding["kind"] != "blob" or any(
            not key.startswith("protected_") for key in finding["counts"]
        ):
            raise ValueError("non-phrase finding requires separate remediation")
        oid = finding["object"]
        text = git(ROOT, "cat-file", "blob", oid).decode()
        cleaned, count = redact(text, patterns)
        if any(path.endswith(".py") for path in finding["paths"]):
            ast.parse(cleaned)
        replacements[oid] = base64.b64encode(cleaned.encode()).decode()
        changes.append({"old_blob": oid, "paths": finding["paths"],
                        "words_redacted": count})
    source_head = git(ROOT, "rev-parse", "HEAD").decode().strip()
    git(ROOT, "clone", "--quiet", "--mirror", "--no-hardlinks", str(ROOT), str(destination))
    replacement_path = parent / (destination.name + "-replacements.json")
    replacement_path.write_text(json.dumps(replacements) + "\n")
    callback = (
        "import os, json, base64\n"
        "if not hasattr(blob_callback, 'replacements'):\n"
        "    with open(os.environ['MVA_SANITIZED_REPLACEMENTS']) as handle:\n"
        "        blob_callback.replacements = json.load(handle)\n"
        "value = blob_callback.replacements.get(blob.original_id.decode())\n"
        "if value is not None:\n"
        "    blob.data = base64.b64decode(value)\n"
    )
    env = dict(os.environ, MVA_SANITIZED_REPLACEMENTS=str(replacement_path))
    result = subprocess.run(
        ["uv", "tool", "run", "--from", "git-filter-repo==2.47.0", "git-filter-repo",
         "--sensitive-data-removal", "--no-fetch", "--blob-callback", callback],
        cwd=destination, env=env, capture_output=True,
    )
    if result.returncode:
        raise RuntimeError("isolated git-filter-repo operation failed; no source refs changed")
    # A mirror of a checkout can contain remote-tracking refs too. They must all pass.
    after = audit(destination, patterns)
    if not after["passed"]:
        raise RuntimeError("cleaned mirror failed audit; no source refs changed")
    if git(ROOT, "rev-parse", "HEAD").decode().strip() != source_head:
        raise RuntimeError("source HEAD changed during preparation")
    report = {"source_head": source_head,
              "clean_head": git(destination, "rev-parse", "refs/heads/main").decode().strip(),
              "destination": str(destination), "filter_repo_version": "2.47.0",
              "changed_blobs": changes, "audit": after,
              "replacement_sha256": hashlib.sha256(replacement_path.read_bytes()).hexdigest()}
    (parent / (destination.name + "-report.json")).write_text(json.dumps(report, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        patterns = {3: {("fixture", "private", "phrase")}}
        cleaned, count = redact('value = "fixture private phrase"\n', patterns)
        ast.parse(cleaned)
        assert count == 1 and "fixture private phrase" not in cleaned
        print("history preparation self-check: phrase removed and Python syntax retained")
        return
    if args.destination is None:
        parser.error("--destination is required")
    print(json.dumps(prepare(args.destination), indent=2))


if __name__ == "__main__":
    main()
