#!/usr/bin/env python3
"""Stream SAM and accumulate aligned reference bases in fixed bins."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

CIGAR = re.compile(r"(\d+)([MIDNSHP=X])")
REFERENCE_CONSUMING = frozenset("MDN=X")
ALIGNED = frozenset("M=X")
REJECT_FLAGS = 0x4 | 0x100 | 0x200 | 0x400 | 0x800


def read_bins(path: Path) -> tuple[dict[str, int], dict[str, list[int]], dict[str, list[int]]]:
    sizes: dict[str, int] = {}
    counts: dict[str, list[int]] = {}
    ends: dict[str, list[int]] = {}
    with path.open() as handle:
        header = next(handle).rstrip().split("\t")
        required = ["chrom", "start", "end", "length"]
        if header[:4] != required:
            raise ValueError(f"unexpected bin header: {header}")
        for line in handle:
            fields = line.rstrip().split("\t")
            chrom, start, end, length = fields[:4]
            start_i, end_i, length_i = int(start), int(end), int(length)
            if chrom not in sizes:
                sizes[chrom] = length_i
                counts[chrom] = []
                ends[chrom] = []
            if start_i != len(counts[chrom]) * sizes[chrom] or end_i - start_i != length_i:
                raise ValueError("bins must be ordered, contiguous and fixed-width except at contig ends")
            counts[chrom].append(0)
            ends[chrom].append(end_i)
    return sizes, counts, ends


def add_segment(values: list[int], start: int, end: int, bin_size: int) -> None:
    while start < end:
        index = start // bin_size
        stop = min(end, (index + 1) * bin_size)
        values[index] += stop - start
        start = stop


def count_stream(
    stream: object, sizes: dict[str, int], counts: dict[str, list[int]], minimum_mapq: int
) -> Counter[str]:
    stats: Counter[str] = Counter()
    for raw in stream:  # type: ignore[union-attr]
        if raw.startswith("@"):
            continue
        stats["records"] += 1
        fields = raw.rstrip().split("\t", 11)
        if len(fields) < 6:
            raise ValueError("malformed SAM record")
        flag = int(fields[1])
        chrom = fields[2].removeprefix("chr")
        mapq = int(fields[4])
        if flag & REJECT_FLAGS:
            stats["rejected_flag"] += 1
            continue
        if mapq < minimum_mapq:
            stats["rejected_mapq"] += 1
            continue
        if chrom not in counts:
            stats["rejected_nonprimary"] += 1
            continue
        position = int(fields[3]) - 1
        for length_text, operation in CIGAR.findall(fields[5]):
            length = int(length_text)
            if operation in ALIGNED:
                add_segment(counts[chrom], position, position + length, sizes[chrom])
                stats["aligned_bases"] += length
            if operation in REFERENCE_CONSUMING:
                position += length
        stats["accepted_records"] += 1
    return stats


def write_counts(
    path: Path, counts: dict[str, list[int]], sizes: dict[str, int], ends: dict[str, list[int]]
) -> None:
    with path.open("w") as handle:
        handle.write("chrom\tstart\tend\taligned_bases\n")
        for chrom, values in counts.items():
            for index, value in enumerate(values):
                start = index * sizes[chrom]
                handle.write(f"{chrom}\t{start}\t{ends[chrom][index]}\t{value}\n")


def run(bins: Path, output: Path, stats_path: Path, minimum_mapq: int, stream: object = sys.stdin) -> None:
    sizes, counts, ends = read_bins(bins)
    stats = count_stream(stream, sizes, counts, minimum_mapq)
    write_counts(output, counts, sizes, ends)
    stats_path.write_text(json.dumps(dict(sorted(stats.items())), indent=2) + "\n")


def self_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        bins = root / "bins.tsv"
        output = root / "counts.tsv"
        stats = root / "stats.json"
        bins.write_text(
            "chrom\tstart\tend\tlength\tacgt_fraction\tgc_fraction\tmappability\n"
            "1\t0\t10\t10\t1\t0.5\t1\n1\t10\t20\t10\t1\t0.5\t1\n"
        )
        sam = (
            "@HD\tVN:1.6\n"
            "a\t0\t1\t8\t60\t8M\t*\t0\t0\tAAAAAAAA\tFFFFFFFF\n"
            "b\t256\t1\t1\t60\t5M\t*\t0\t0\tAAAAA\tFFFFF\n"
            "c\t0\t1\t1\t10\t5M\t*\t0\t0\tAAAAA\tFFFFF\n"
        )
        run(bins, output, stats, 30, stream=sam.splitlines(keepends=True))
        rows = output.read_text().splitlines()
        assert rows[1].endswith("\t3") and rows[2].endswith("\t5")
        observed = json.loads(stats.read_text())
        assert observed["accepted_records"] == 1 and observed["aligned_bases"] == 8
    print("count_alignment_depth self-check ok")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bins", nargs="?", type=Path)
    parser.add_argument("output", nargs="?", type=Path)
    parser.add_argument("stats", nargs="?", type=Path)
    parser.add_argument("--minimum-mapq", type=int, default=30)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if None in (args.bins, args.output, args.stats):
        parser.error("bins, output and stats paths are required")
    run(args.bins, args.output, args.stats, args.minimum_mapq)


if __name__ == "__main__":
    main()
