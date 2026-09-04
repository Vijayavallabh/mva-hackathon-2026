#!/usr/bin/env python3
"""Build padded gene-body intervals from the genome-wide feat-004 survivors."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import re
import tempfile
from collections import defaultdict
from pathlib import Path

PRIMARY_CONTIGS = {str(value) for value in range(1, 23)} | {"X", "Y", "M"}
ESTABLISHED_MVA_GENES = {"BUB1B", "CEP57", "TRIP13"}
ATTRIBUTE_RE = re.compile(r'(\S+) "([^"]*)"')


def open_text(path: Path):
    return gzip.open(path, "rt") if path.suffix == ".gz" else path.open()


def candidate_genes(path: Path) -> set[str]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None or "gene" not in reader.fieldnames:
            raise ValueError("candidate table has no gene column")
        genes = {row["gene"].strip() for row in reader if row["gene"].strip()}
    if not genes:
        raise ValueError("candidate table yielded no genes")
    return genes | ESTABLISHED_MVA_GENES


def parse_gene_spans(path: Path, selected: set[str]):
    spans: dict[str, list[tuple[str, int, int]]] = defaultdict(list)
    with open_text(path) as handle:
        for raw in handle:
            if raw.startswith("#"):
                continue
            fields = raw.rstrip("\n").split("\t")
            if len(fields) != 9 or fields[2] != "gene" or fields[0] not in PRIMARY_CONTIGS:
                continue
            attributes = dict(ATTRIBUTE_RE.findall(fields[8]))
            gene = attributes.get("gene_name", "")
            if gene in selected:
                spans[gene].append((fields[0], int(fields[3]) - 1, int(fields[4])))
    return dict(spans)


def merge_intervals(intervals: list[tuple[str, int, int]]) -> list[tuple[str, int, int]]:
    merged: list[list[object]] = []
    contig_order = {str(value): value for value in range(1, 23)} | {"X": 23, "Y": 24, "M": 25}
    for chrom, start, end in sorted(
        intervals, key=lambda item: (contig_order[item[0]], item[1], item[2])
    ):
        if merged and merged[-1][0] == chrom and start <= int(merged[-1][2]):
            merged[-1][2] = max(int(merged[-1][2]), end)
        else:
            merged.append([chrom, start, end])
    return [(str(chrom), int(start), int(end)) for chrom, start, end in merged]


def build(
    candidates: Path,
    gtf: Path,
    bed: Path,
    manifest: Path,
    padding: int,
) -> dict[str, object]:
    selected = candidate_genes(candidates)
    spans = parse_gene_spans(gtf, selected)
    missing = sorted(selected - set(spans))
    if missing:
        raise ValueError("candidate genes absent from GTF: " + ", ".join(missing))
    padded: list[tuple[str, int, int]] = []
    gene_records: list[dict[str, object]] = []
    for gene in sorted(spans):
        chromosomes = {span[0] for span in spans[gene]}
        if len(chromosomes) != 1:
            raise ValueError(f"gene {gene} occurs on multiple primary contigs")
        chrom = next(iter(chromosomes))
        start = max(0, min(span[1] for span in spans[gene]) - padding)
        end = max(span[2] for span in spans[gene]) + padding
        padded.append((chrom, start, end))
        gene_records.append({"gene": gene, "chrom": chrom, "start": start, "end": end})
    merged = merge_intervals(padded)
    bed.parent.mkdir(parents=True, exist_ok=True)
    with bed.open("w") as handle:
        for chrom, start, end in merged:
            handle.write(f"{chrom}\t{start}\t{end}\n")
    summary: dict[str, object] = {
        "candidate_source": str(candidates),
        "gtf_source": str(gtf),
        "padding_bases": padding,
        "selected_gene_count": len(selected),
        "merged_interval_count": len(merged),
        "target_bases": sum(end - start for _chrom, start, end in merged),
        "established_mva_genes_forced": sorted(ESTABLISHED_MVA_GENES),
        "genes": gene_records,
    }
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def self_check() -> None:
    with tempfile.TemporaryDirectory(prefix="recall-intervals-") as name:
        root = Path(name)
        candidates = root / "candidates.tsv"
        candidates.write_text("gene\nBUB1B\nGENE2\n")
        gtf = root / "genes.gtf"
        gtf.write_text(
            '1\ttest\tgene\t101\t200\t.\t+\t.\tgene_id "g1"; gene_name "BUB1B";\n'
            '1\ttest\tgene\t251\t300\t.\t+\t.\tgene_id "g2"; gene_name "GENE2";\n'
            '2\ttest\tgene\t101\t120\t.\t+\t.\tgene_id "g3"; gene_name "CEP57";\n'
            '3\ttest\tgene\t101\t120\t.\t+\t.\tgene_id "g4"; gene_name "TRIP13";\n'
        )
        summary = build(candidates, gtf, root / "targets.bed", root / "manifest.json", 25)
        assert summary["selected_gene_count"] == 4
        assert summary["merged_interval_count"] == 3
        assert (root / "targets.bed").read_text().splitlines()[0] == "1\t75\t325"
    print("self-check ok: candidate gene selection, padding and interval merging")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidates", type=Path, nargs="?")
    parser.add_argument("gtf", type=Path, nargs="?")
    parser.add_argument("bed", type=Path, nargs="?")
    parser.add_argument("manifest", type=Path, nargs="?")
    parser.add_argument("--padding", type=int, default=20_000)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if None in (args.candidates, args.gtf, args.bed, args.manifest):
        parser.error("candidates, gtf, bed and manifest are required")
    if args.padding < 0:
        parser.error("--padding must be non-negative")
    summary = build(args.candidates, args.gtf, args.bed, args.manifest, args.padding)
    print(
        f"wrote {summary['merged_interval_count']} intervals spanning "
        f"{summary['target_bases']} bases for {summary['selected_gene_count']} genes"
    )


if __name__ == "__main__":
    main()
