#!/usr/bin/env python3
"""Select one named gene interval from a recall target manifest."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path


def select_interval(manifest: Path, output: Path, gene: str) -> dict[str, object]:
    data = json.loads(manifest.read_text())
    matches = [record for record in data["genes"] if record["gene"] == gene]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {gene} interval, found {len(matches)}")
    record = matches[0]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f"{record['chrom']}\t{record['start']}\t{record['end']}\n")
    return record


def self_check() -> None:
    with tempfile.TemporaryDirectory(prefix="phase-interval-") as name:
        root = Path(name)
        manifest = root / "targets.json"
        manifest.write_text(
            json.dumps(
                {
                    "genes": [
                        {"gene": "GENE1", "chrom": "1", "start": 10, "end": 20},
                        {"gene": "BUB1B", "chrom": "15", "start": 30, "end": 50},
                    ]
                }
            )
        )
        output = root / "phase.bed"
        selected = select_interval(manifest, output, "BUB1B")
        assert selected["chrom"] == "15"
        assert output.read_text() == "15\t30\t50\n"
    print("self-check ok: unique named-gene phase interval selection")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, nargs="?")
    parser.add_argument("output", type=Path, nargs="?")
    parser.add_argument("--gene", default="BUB1B")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if args.manifest is None or args.output is None:
        parser.error("manifest and output are required")
    selected = select_interval(args.manifest, args.output, args.gene)
    print(
        f"wrote one {args.gene} phase interval spanning "
        f"{int(selected['end']) - int(selected['start'])} bases"
    )


if __name__ == "__main__":
    main()
