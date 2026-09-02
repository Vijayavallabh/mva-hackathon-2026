#!/usr/bin/env python3
"""Build the VCF-matching no-chr, v2-masked GRCh38 + hs38d1 reference."""

from __future__ import annotations

import argparse
import gzip
from pathlib import Path


def load_intervals(path: Path) -> dict[str, list[tuple[int, int]]]:
    intervals: dict[str, list[tuple[int, int]]] = {}
    for raw in path.read_text().splitlines():
        if not raw or raw.startswith("#"):
            continue
        chrom, start, end, *_ = raw.split("\t")
        intervals.setdefault(chrom.removeprefix("chr"), []).append((int(start), int(end)))
    return intervals


def normalized_name(header: str) -> str:
    name = header[1:].split()[0]
    return name.removeprefix("chr")


def build(source: Path, exclusions: Path, output: Path) -> None:
    intervals = load_intervals(exclusions)
    output.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(source, "rt") as src, output.open("w") as dst:
        name = ""
        offset = 0
        for line in src:
            if line.startswith(">"):
                name = normalized_name(line)
                offset = 0
                dst.write(f">{name}\n")
                continue
            sequence = list(line.strip())
            for start, end in intervals.get(name, []):
                left = max(start - offset, 0)
                right = min(end - offset, len(sequence))
                if left < right:
                    sequence[left:right] = "N" * (right - left)
            dst.write("".join(sequence) + "\n")
            offset += len(sequence)


def self_check() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "source.fa.gz"
        bed = root / "mask.bed"
        out = root / "out.fa"
        with gzip.open(source, "wt") as handle:
            handle.write(">chr1 description\nACGT\nACGT\n>HLA-A*01\nAAAA\n")
        bed.write_text("chr1\t2\t6\n")
        build(source, bed, out)
        assert out.read_text() == ">1\nACNN\nNNGT\n>HLA-A*01\nAAAA\n"
    print("reference builder self-check ok")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", nargs="?", type=Path)
    parser.add_argument("exclusions", nargs="?", type=Path)
    parser.add_argument("output", nargs="?", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if not all((args.source, args.exclusions, args.output)):
        parser.error("source, exclusions, and output are required")
    build(args.source, args.exclusions, args.output)


if __name__ == "__main__":
    main()
