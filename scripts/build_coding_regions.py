#!/usr/bin/env python3
"""Build merged primary-contig exon windows from a release-pinned Ensembl GTF."""

from __future__ import annotations

import argparse
import gzip
import tempfile
from collections import defaultdict
from pathlib import Path

PRIMARY = {str(number) for number in range(1, 23)} | {"X", "Y", "M"}


def build(source: Path, output: Path, flank: int = 20) -> tuple[int, int]:
    intervals: dict[str, list[tuple[int, int]]] = defaultdict(list)
    with gzip.open(source, "rt") as handle:
        for raw in handle:
            if raw.startswith("#"):
                continue
            fields = raw.rstrip("\n").split("\t")
            if len(fields) != 9 or fields[2] != "exon":
                continue
            chrom = "M" if fields[0] == "MT" else fields[0]
            if chrom not in PRIMARY:
                continue
            start = max(int(fields[3]) - 1 - flank, 0)
            end = int(fields[4]) + flank
            intervals[chrom].append((start, end))

    merged_count = 0
    covered_bases = 0
    output.parent.mkdir(parents=True, exist_ok=True)
    chrom_order = [str(number) for number in range(1, 23)] + ["X", "Y", "M"]
    with output.open("w") as handle:
        for chrom in chrom_order:
            merged: list[list[int]] = []
            for start, end in sorted(intervals.get(chrom, [])):
                if merged and start <= merged[-1][1]:
                    merged[-1][1] = max(merged[-1][1], end)
                else:
                    merged.append([start, end])
            for start, end in merged:
                handle.write(f"{chrom}\t{start}\t{end}\n")
                merged_count += 1
                covered_bases += end - start
    if not merged_count:
        raise ValueError("GTF yielded no primary-contig exon windows")
    return merged_count, covered_bases


def self_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "synthetic.gtf.gz"
        output = root / "regions.bed"
        with gzip.open(source, "wt") as handle:
            handle.write("##gtf-version 3\n")
            handle.write('1\ttest\texon\t11\t20\t.\t+\t.\tgene_id "A";\n')
            handle.write('1\ttest\texon\t25\t30\t.\t+\t.\tgene_id "A";\n')
            handle.write('MT\ttest\texon\t1\t2\t.\t+\t.\tgene_id "M";\n')
            handle.write('GL0001\ttest\texon\t1\t2\t.\t+\t.\tgene_id "ALT";\n')
        count, bases = build(source, output, flank=2)
        assert output.read_text() == "1\t8\t32\nM\t0\t4\n"
        assert (count, bases) == (2, 28)
    print("coding-region builder self-check ok")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", nargs="?", type=Path)
    parser.add_argument("output", nargs="?", type=Path)
    parser.add_argument("--flank", type=int, default=20)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if args.source is None or args.output is None:
        parser.error("source and output are required")
    if args.flank < 0:
        parser.error("--flank must be non-negative")
    count, bases = build(args.source, args.output, args.flank)
    print(f"wrote {count} merged exon windows covering {bases} bases")


if __name__ == "__main__":
    main()
