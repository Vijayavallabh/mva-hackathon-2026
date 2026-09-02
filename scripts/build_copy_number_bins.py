#!/usr/bin/env python3
"""Build fixed GRCh38 bins with reference GC and Umap multi-read mappability."""

from __future__ import annotations

import argparse
import gzip
import tempfile
from dataclasses import dataclass
from pathlib import Path

PRIMARY = tuple(map(str, range(1, 23))) + ("X", "Y")
REQUIRED_MAPPABILITY = frozenset(map(str, range(1, 23)))


@dataclass
class Bin:
    chrom: str
    start: int
    end: int
    acgt: int = 0
    gc: int = 0
    map_sum: float = 0.0


def read_fasta(path: Path, bin_size: int) -> tuple[dict[str, list[Bin]], dict[str, int]]:
    bins: dict[str, list[Bin]] = {}
    lengths: dict[str, int] = {}
    chrom: str | None = None
    sequence: list[str] = []

    def consume() -> None:
        if chrom not in PRIMARY:
            return
        seq = "".join(sequence).upper()
        lengths[chrom] = len(seq)
        chrom_bins: list[Bin] = []
        for start in range(0, len(seq), bin_size):
            chunk = seq[start : start + bin_size]
            a = chunk.count("A")
            c = chunk.count("C")
            g = chunk.count("G")
            t = chunk.count("T")
            chrom_bins.append(
                Bin(chrom=chrom, start=start, end=start + len(chunk), acgt=a + c + g + t, gc=c + g)
            )
        bins[chrom] = chrom_bins

    with path.open() as handle:
        for line in handle:
            if line.startswith(">"):
                consume()
                chrom = line[1:].split()[0].removeprefix("chr")
                sequence = []
            else:
                sequence.append(line.strip())
        consume()
    return bins, lengths


def add_mappability(path: Path, bins: dict[str, list[Bin]], lengths: dict[str, int], bin_size: int) -> None:
    seen: set[str] = set()
    with gzip.open(path, "rt") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line or line.startswith(("track", "browser", "#")):
                continue
            fields = line.rstrip().split("\t")
            if len(fields) != 4:
                raise ValueError(f"mappability line {line_number}: expected four columns")
            chrom = fields[0].removeprefix("chr")
            if chrom not in bins:
                continue
            start, end = int(fields[1]), int(fields[2])
            value = float(fields[3])
            if not (0 <= start < end <= lengths[chrom]) or not (0.0 <= value <= 1.0):
                raise ValueError(f"mappability line {line_number}: invalid interval or value")
            seen.add(chrom)
            while start < end:
                index = start // bin_size
                stop = min(end, bins[chrom][index].end)
                bins[chrom][index].map_sum += (stop - start) * value
                start = stop
    missing = REQUIRED_MAPPABILITY - seen
    if missing:
        raise ValueError(f"mappability track lacks primary contigs: {sorted(missing)}")


def write_bins(path: Path, bins: dict[str, list[Bin]]) -> None:
    with path.open("w") as handle:
        handle.write("chrom\tstart\tend\tlength\tacgt_fraction\tgc_fraction\tmappability\n")
        for chrom in PRIMARY:
            for item in bins[chrom]:
                length = item.end - item.start
                gc_fraction = item.gc / item.acgt if item.acgt else 0.0
                handle.write(
                    f"{chrom}\t{item.start}\t{item.end}\t{length}\t"
                    f"{item.acgt / length:.8f}\t{gc_fraction:.8f}\t{item.map_sum / length:.8f}\n"
                )


def build(reference: Path, mappability: Path, output: Path, bin_size: int) -> None:
    if bin_size <= 0:
        raise ValueError("bin size must be positive")
    bins, lengths = read_fasta(reference, bin_size)
    if set(bins) != set(PRIMARY):
        raise ValueError("reference lacks one or more primary chromosomes")
    add_mappability(mappability, bins, lengths, bin_size)
    write_bins(output, bins)


def self_check() -> None:
    fasta = ">chr1\nACGTNNGC\n>X\nGGCCAAAA\n>Y\nTTTTCCCC\n" + "".join(
        f">{chrom}\nACGT\n" for chrom in PRIMARY if chrom not in {"1", "X", "Y"}
    )
    map_lines = ["track type=bedGraph\n"]
    for chrom in PRIMARY:
        length = 8 if chrom in {"1", "X", "Y"} else 4
        if chrom != "Y":
            map_lines.append(f"chr{chrom}\t0\t{length}\t1.0\n")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        ref = root / "ref.fa"
        track = root / "map.gz"
        out = root / "bins.tsv"
        ref.write_text(fasta)
        with gzip.open(track, "wt") as handle:
            handle.writelines(map_lines)
        build(ref, track, out, 4)
        rows = out.read_text().splitlines()
        assert rows[1] == "1\t0\t4\t4\t1.00000000\t0.50000000\t1.00000000"
        assert rows[2].startswith("1\t4\t8\t4\t0.50000000\t1.00000000\t1.00000000")
        assert rows[-1].endswith("\t0.00000000")
        assert len(rows) == 1 + len(PRIMARY) + 3
    print("build_copy_number_bins self-check ok")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("reference", nargs="?", type=Path)
    parser.add_argument("mappability", nargs="?", type=Path)
    parser.add_argument("output", nargs="?", type=Path)
    parser.add_argument("--bin-size", type=int, default=100_000)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if None in (args.reference, args.mappability, args.output):
        parser.error("reference, mappability and output are required")
    build(args.reference, args.mappability, args.output, args.bin_size)


if __name__ == "__main__":
    main()
