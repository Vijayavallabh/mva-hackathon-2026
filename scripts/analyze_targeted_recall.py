#!/usr/bin/env python3
"""Summarize targeted re-calls, candidate-region SVs and read-backed phase."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import re
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import pysam

SEVERITY = {
    "transcript_ablation": 10,
    "splice_acceptor_variant": 10,
    "splice_donor_variant": 10,
    "stop_gained": 10,
    "frameshift_variant": 10,
    "stop_lost": 9,
    "start_lost": 9,
    "inframe_insertion": 7,
    "inframe_deletion": 7,
    "missense_variant": 6,
    "protein_altering_variant": 6,
    "splice_region_variant": 4,
}


@dataclass(frozen=True)
class VariantKey:
    chrom: str
    pos: int
    ref: str
    alt: str


@dataclass(frozen=True)
class NovelCall:
    key: VariantKey
    gene: str
    consequence: str
    impact: str
    max_af: float | None
    hgvsc: str
    hgvsp: str
    depth: int | None
    alt_depth: int | None
    vaf: float | None
    genotype_quality: float | None
    genotype: str


@dataclass
class CombinedCall:
    call: NovelCall
    callers: set[str]
    metrics: dict[str, NovelCall]


@dataclass(frozen=True)
class ScreenedCall:
    call: NovelCall
    callers: tuple[str, ...]
    max_depth: int | None
    max_alt_depth: int | None
    max_vaf: float | None
    max_gq: float | None
    nearest_exon_boundary_bp: int | None
    classes: tuple[str, ...]
    context_entropy: float
    longest_homopolymer: int


@dataclass(frozen=True)
class PhaseCall:
    found: bool
    phased: bool
    gt: tuple[int | None, ...]
    ps: int | None


def open_text(path: Path):
    return gzip.open(path, "rt") if path.suffix == ".gz" else path.open()


def consequence_score(consequence: str) -> int:
    return max((SEVERITY.get(term, 0) for term in consequence.split("&")), default=0)


def parse_float(value: str) -> float | None:
    values = []
    for token in re.split(r"[,&]", value or ""):
        try:
            parsed = float(token)
        except ValueError:
            continue
        if math.isfinite(parsed):
            values.append(parsed)
    return max(values) if values else None


def iter_vep_calls(path: Path):
    csq_fields: list[str] | None = None
    with open_text(path) as handle:
        for raw in handle:
            if raw.startswith("##INFO=<ID=CSQ"):
                match = re.search(r"Format: ([^\"]+)", raw)
                if not match:
                    raise ValueError(f"CSQ header lacks format in {path}")
                csq_fields = match.group(1).rstrip('>\n" ').split("|")
                continue
            if raw.startswith("#"):
                continue
            if csq_fields is None:
                raise ValueError(f"no CSQ header in {path}")
            fields = raw.rstrip("\n").split("\t")
            chrom, pos, _identifier, ref, alt = fields[:5]
            sample = {}
            if len(fields) >= 10:
                sample = dict(zip(fields[8].split(":"), fields[9].split(":"), strict=False))
            depth = int(sample["DP"]) if sample.get("DP", "").isdigit() else None
            ad = [int(value) for value in sample.get("AD", "").split(",") if value.isdigit()]
            alt_depth = ad[1] if len(ad) == 2 else None
            vaf = parse_float(sample.get("AF", ""))
            if vaf is None and depth and alt_depth is not None:
                vaf = alt_depth / depth
            genotype_quality = parse_float(sample.get("GQ", ""))
            info = {
                key: value
                for item in fields[7].split(";")
                for key, separator, value in [item.partition("=")]
                if separator
            }
            annotations = [
                dict(zip(csq_fields, value.split("|"), strict=False))
                for value in info.get("CSQ", "").split(",")
                if value
            ]
            if not annotations:
                continue
            annotation = max(
                annotations,
                key=lambda item: consequence_score(item.get("Consequence", "")),
            )
            afs = [
                parse_float(annotation.get(name, ""))
                for name in ("MAX_AF", "gnomADe_AF", "gnomADg_AF")
            ]
            max_af = max((value for value in afs if value is not None), default=None)
            yield NovelCall(
                VariantKey(chrom, int(pos), ref, alt),
                annotation.get("SYMBOL", ""),
                annotation.get("Consequence", ""),
                annotation.get("IMPACT", ""),
                max_af,
                annotation.get("HGVSc", ""),
                annotation.get("HGVSp", ""),
                depth,
                alt_depth,
                vaf,
                genotype_quality,
                sample.get("GT", ""),
            )


def collect_novel_calls(paths: dict[str, Path]):
    calls: dict[VariantKey, CombinedCall] = {}
    counts: dict[str, int] = {}
    for caller, path in paths.items():
        caller_count = 0
        for call in iter_vep_calls(path):
            caller_count += 1
            entry = calls.setdefault(call.key, CombinedCall(call, set(), {}))
            entry.callers.add(caller)
            entry.metrics[caller] = call
            previous = entry.call
            if consequence_score(call.consequence) > consequence_score(previous.consequence):
                entry.call = call
        counts[caller] = caller_count
    return calls, counts


def load_exon_boundaries(gtf: Path, genes: set[str]) -> dict[tuple[str, str], list[int]]:
    boundaries: dict[tuple[str, str], set[int]] = defaultdict(set)
    with gzip.open(gtf, "rt") as handle:
        for raw in handle:
            if raw.startswith("#"):
                continue
            fields = raw.rstrip("\n").split("\t")
            if len(fields) != 9 or fields[2] != "exon":
                continue
            match = re.search(r'gene_name "([^"]+)"', fields[8])
            if not match or match.group(1) not in genes:
                continue
            boundaries[(fields[0], match.group(1))].update((int(fields[3]), int(fields[4])))
    return {key: sorted(values) for key, values in boundaries.items()}


def sequence_complexity(sequence: str) -> tuple[float, int]:
    sequence = sequence.upper()
    counts = [sequence.count(base) for base in "ACGT"]
    observed = sum(counts)
    entropy = -sum((count / observed) * math.log2(count / observed) for count in counts if count)
    runs = re.findall(r"(A+|C+|G+|T+)", sequence)
    return entropy, max((len(run) for run in runs), default=0)


def screen_calls(
    calls: dict[VariantKey, CombinedCall], gtf: Path, reference: Path
) -> list[ScreenedCall]:
    boundaries = load_exon_boundaries(gtf, {entry.call.gene for entry in calls.values()})
    retained: list[ScreenedCall] = []
    with pysam.FastaFile(str(reference)) as fasta:
        for entry in calls.values():
            call = entry.call
            if not call.gene or (call.max_af is not None and call.max_af > 0.01):
                continue
            metrics = list(entry.metrics.values())
            max_depth = max(
                (item.depth for item in metrics if item.depth is not None), default=None
            )
            max_alt_depth = max(
                (item.alt_depth for item in metrics if item.alt_depth is not None),
                default=None,
            )
            max_vaf = max((item.vaf for item in metrics if item.vaf is not None), default=None)
            max_gq = max(
                (
                    item.genotype_quality
                    for item in metrics
                    if item.genotype_quality is not None
                ),
                default=None,
            )
            # Require actual alternate-read support and exclude near-reference and near-fixed
            # calls from the missed-heterozygous-allele screen.
            if max_depth is None or max_depth < 10 or max_alt_depth is None or max_alt_depth < 3:
                continue
            if max_vaf is None or not 0.10 <= max_vaf <= 0.90:
                continue
            exon_bounds = boundaries.get((call.key.chrom, call.gene), [])
            nearest = min((abs(call.key.pos - value) for value in exon_bounds), default=None)
            start = max(0, call.key.pos - 16)
            sequence = fasta.fetch(call.key.chrom, start, call.key.pos + 15)
            entropy, homopolymer = sequence_complexity(sequence)
            repeat_adjacent = entropy < 1.5 or homopolymer >= 6
            classes = []
            if consequence_score(call.consequence) >= 4:
                classes.append("coding_or_splice")
            if (
                "intron_variant" in call.consequence.split("&")
                and nearest is not None
                and nearest >= 20
            ):
                classes.append("deep_intronic_ge20bp")
            if repeat_adjacent:
                classes.append("repeat_adjacent")
            if not classes:
                continue
            retained.append(
                ScreenedCall(call, tuple(sorted(entry.callers)), max_depth, max_alt_depth,
                             max_vaf, max_gq, nearest, tuple(classes), entropy, homopolymer)
            )
    return retained


def write_novel_candidates(path: Path, retained: list[ScreenedCall]) -> int:
    retained.sort(
        key=lambda item: (
            len(item.callers),
            consequence_score(item.call.consequence),
            -(item.call.max_af if item.call.max_af is not None else -1),
        ),
        reverse=True,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(
            [
                "chrom",
                "pos",
                "ref",
                "alt",
                "gene",
                "consequence",
                "impact",
                "max_af",
                "callers",
                "max_depth",
                "max_alt_depth",
                "max_vaf",
                "max_genotype_quality",
                "nearest_exon_boundary_bp",
                "screen_classes",
                "context_entropy",
                "longest_homopolymer",
                "hgvsc",
                "hgvsp",
            ]
        )
        for item in retained:
            call = item.call
            writer.writerow(
                [
                    call.key.chrom,
                    call.key.pos,
                    call.key.ref,
                    call.key.alt,
                    call.gene,
                    call.consequence,
                    call.impact,
                    "" if call.max_af is None else f"{call.max_af:.8g}",
                    ",".join(item.callers),
                    item.max_depth,
                    item.max_alt_depth,
                    f"{item.max_vaf:.6g}",
                    "" if item.max_gq is None else f"{item.max_gq:.6g}",
                    "" if item.nearest_exon_boundary_bp is None else item.nearest_exon_boundary_bp,
                    ",".join(item.classes),
                    f"{item.context_entropy:.4f}",
                    item.longest_homopolymer,
                    call.hgvsc,
                    call.hgvsp,
                ]
            )
    return len(retained)


def load_gene_intervals(path: Path):
    manifest = json.loads(path.read_text())
    by_chrom: dict[str, list[dict[str, object]]] = defaultdict(list)
    for gene in manifest["genes"]:
        by_chrom[gene["chrom"]].append(gene)
    return manifest, by_chrom


def sv_interval(record: pysam.VariantRecord) -> tuple[int, int]:
    start = record.pos - 1
    end = max(start + 1, record.stop or start + 1)
    return start, end


def write_target_svs(bcf: Path, manifest: Path, output: Path):
    _manifest, genes_by_chrom = load_gene_intervals(manifest)
    total = 0
    overlaps = []
    with pysam.VariantFile(str(bcf)) as variants:
        for record in variants:
            total += 1
            start, end = sv_interval(record)
            genes = {
                str(gene["gene"])
                for gene in genes_by_chrom.get(record.chrom, [])
                if start < int(gene["end"]) and end > int(gene["start"])
            }
            chr2 = str(record.info.get("CHR2", record.chrom))
            pos2 = int(record.info.get("POS2", record.stop or record.pos)) - 1
            genes.update(
                str(gene["gene"])
                for gene in genes_by_chrom.get(chr2, [])
                if int(gene["start"]) <= pos2 < int(gene["end"])
            )
            if genes:
                overlaps.append((record, sorted(genes)))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["chrom", "pos", "end", "svtype", "filter", "genes"])
        for record, genes in overlaps:
            writer.writerow(
                [
                    record.chrom,
                    record.pos,
                    record.stop,
                    record.info.get("SVTYPE", ""),
                    ",".join(record.filter.keys()),
                    ",".join(genes),
                ]
            )
    return total, len(overlaps)


def existing_alleles_by_gene(path: Path) -> dict[str, dict[VariantKey, dict[str, str]]]:
    alleles: dict[str, dict[VariantKey, dict[str, str]]] = defaultdict(dict)
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            gene = row["gene"]
            for suffix in ("1", "2"):
                if not row.get(f"chrom_{suffix}"):
                    continue
                key = VariantKey(
                    row[f"chrom_{suffix}"].removeprefix("chr"),
                    int(row[f"pos_{suffix}"]),
                    row[f"ref_{suffix}"],
                    row[f"alt_{suffix}"],
                )
                alleles[gene][key] = {
                    "consequence": row.get(f"consequence_{suffix}", ""),
                    "max_af": row.get(f"max_af_{suffix}", ""),
                    "gt": row.get(f"gt_{suffix}", ""),
                }
    return alleles


def write_compound_reconstructions(
    path: Path, screened: list[ScreenedCall], existing_path: Path
) -> tuple[int, int]:
    existing = existing_alleles_by_gene(existing_path)
    best_gene_score: dict[str, float] = defaultdict(float)
    with existing_path.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            best_gene_score[row["gene"]] = max(
                best_gene_score[row["gene"]], float(row["total_score"])
            )
    rows = []
    for novel in screened:
        for key, old in existing.get(novel.call.gene, {}).items():
            evidence_score = (
                (2.0 if "coding_or_splice" in novel.classes else 0.0)
                + (0.5 if "deep_intronic_ge20bp" in novel.classes else 0.0)
                + (0.25 if "repeat_adjacent" in novel.classes else 0.0)
                + (1.0 if len(novel.callers) == 2 else 0.0)
                + (0.5 if novel.call.max_af is not None and novel.call.max_af <= 0.001 else 0.0)
            )
            rows.append(
                (best_gene_score[novel.call.gene] + evidence_score, evidence_score,
                 novel, key, old)
            )
    rows.sort(
        key=lambda row: (
            row[0],
            consequence_score(row[2].call.consequence),
            len(row[2].callers),
        ),
        reverse=True,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(
            [
                "gene",
                "review_rank",
                "existing_gene_best_score",
                "novel_evidence_score",
                "review_priority_score",
                "existing_chrom",
                "existing_pos",
                "existing_ref",
                "existing_alt",
                "existing_gt",
                "existing_consequence",
                "existing_max_af",
                "novel_chrom",
                "novel_pos",
                "novel_ref",
                "novel_alt",
                "novel_consequence",
                "novel_max_af",
                "novel_callers",
                "novel_vaf",
                "novel_screen_classes",
                "phase_status",
            ]
        )
        for rank, (priority_score, evidence_score, novel, key, old) in enumerate(rows, 1):
            call = novel.call
            writer.writerow(
                [
                    call.gene,
                    rank,
                    f"{best_gene_score[call.gene]:.6f}",
                    f"{evidence_score:.2f}",
                    f"{priority_score:.6f}",
                    key.chrom,
                    key.pos,
                    key.ref,
                    key.alt,
                    old["gt"],
                    old["consequence"],
                    old["max_af"],
                    call.key.chrom,
                    call.key.pos,
                    call.key.ref,
                    call.key.alt,
                    call.consequence,
                    "" if call.max_af is None else f"{call.max_af:.8g}",
                    ",".join(novel.callers),
                    f"{novel.max_vaf:.6g}",
                    ",".join(novel.classes),
                    "unconfirmed; no parental or shared read-backed phase",
                ]
            )
    return len(rows), len({row[2].call.gene for row in rows})


def leading_pair(path: Path) -> tuple[VariantKey, VariantKey]:
    with path.open(newline="") as handle:
        row = next(csv.DictReader(handle, delimiter="\t"))
    return tuple(
        VariantKey(
            row[f"chrom_{suffix}"].removeprefix("chr"),
            int(row[f"pos_{suffix}"]),
            row[f"ref_{suffix}"],
            row[f"alt_{suffix}"],
        )
        for suffix in ("1", "2")
    )


def phased_call(path: Path, key: VariantKey, sample: str):
    with pysam.VariantFile(str(path)) as variants:
        for record in variants.fetch(key.chrom, key.pos - 1, key.pos):
            if record.pos != key.pos or record.ref != key.ref or key.alt not in record.alts:
                continue
            call = record.samples[sample]
            return PhaseCall(True, call.phased, tuple(call.get("GT", ())), call.get("PS"))
    return PhaseCall(False, False, (), None)


def phase_relation(left: PhaseCall, right: PhaseCall):
    if not left.found or not right.found:
        return "unconfirmed", "one or both leading alleles absent from phased VCF"
    if not left.phased or not right.phased:
        return "unconfirmed", "one or both leading alleles are unphased"
    if left.ps is None or left.ps != right.ps:
        return "unconfirmed", "alleles are not in the same phase set"
    left_gt = list(left.gt)
    right_gt = list(right.gt)
    if sorted(left_gt) != [0, 1] or sorted(right_gt) != [0, 1]:
        return "unconfirmed", "one or both phased genotypes are not biallelic heterozygotes"
    relation = "cis" if left_gt.index(1) == right_gt.index(1) else "trans"
    return relation, "both alleles share a read-backed phase set"


def analyze(args: argparse.Namespace) -> dict[str, object]:
    calls, novel_counts = collect_novel_calls(
        {"haplotypecaller": args.hc_vep, "mutect2": args.mutect_vep}
    )
    screened = screen_calls(calls, args.gtf, args.reference)
    retained = write_novel_candidates(args.novel_candidates, screened)
    reconstruction_count, reconstruction_genes = write_compound_reconstructions(
        args.compound_reconstructions, screened, args.all_candidates
    )
    sv_total, sv_target = write_target_svs(args.delly, args.manifest, args.target_svs)
    left_key, right_key = leading_pair(args.candidates)
    left = phased_call(args.phased, left_key, "PROBAND01")
    right = phased_call(args.phased, right_key, "PROBAND01")
    relation, reason = phase_relation(left, right)
    both_callers = sum(len(entry.callers) == 2 for entry in calls.values())
    candidate_gene_counts = defaultdict(int)
    with args.novel_candidates.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            candidate_gene_counts[row["gene"]] += 1
    summary = {
        "target_manifest": json.loads(args.manifest.read_text()),
        "novel_calls_after_source_vcf_subtraction": novel_counts,
        "distinct_novel_calls": len(calls),
        "novel_calls_seen_by_both_callers": both_callers,
        "supported_rare_coding_splice_deep_intronic_or_repeat_adjacent_candidates": retained,
        "candidate_class_counts": {
            class_name: sum(class_name in item.classes for item in screened)
            for class_name in ("coding_or_splice", "deep_intronic_ge20bp", "repeat_adjacent")
        },
        "rare_candidate_gene_counts": dict(sorted(candidate_gene_counts.items())),
        "novel_existing_allele_reconstructions": reconstruction_count,
        "genes_with_novel_existing_allele_reconstructions": reconstruction_genes,
        "delly_pass_calls_in_target_enriched_bam": sv_total,
        "delly_pass_calls_overlapping_target_gene_windows": sv_target,
        "leading_pair_read_backed_phase": {
            "status": relation,
            "reason": reason,
            "allele_1": left.__dict__,
            "allele_2": right.__dict__,
        },
        "limitations": [
            "Single-subject tumor-only Mutect2 has no matched normal or panel of normals.",
            "Short-read phasing is conclusive only within a shared supported phase set.",
            "Candidate windows are hypothesis-driven and do not replace "
            "genome-wide interpretation.",
            "Deep intronic is operationally >=20 bp from the nearest Ensembl 116 exon "
            "boundary; no regulatory-effect prediction is implied.",
            "Novel/existing same-gene pairs are hypotheses; trans phase remains unconfirmed.",
        ],
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def self_check() -> None:
    assert phase_relation(
        PhaseCall(True, True, (0, 1), 10),
        PhaseCall(True, True, (1, 0), 10),
    )[0] == "trans"
    assert phase_relation(
        PhaseCall(True, True, (0, 1), 10),
        PhaseCall(True, True, (0, 1), 10),
    )[0] == "cis"
    assert phase_relation(
        PhaseCall(True, True, (0, 1), 10),
        PhaseCall(True, True, (1, 0), 11),
    )[0] == "unconfirmed"
    with tempfile.TemporaryDirectory(prefix="recall-analysis-") as name:
        vcf = Path(name) / "novel.vcf"
        vcf.write_text(
            '##fileformat=VCFv4.2\n'
            '##INFO=<ID=CSQ,Number=.,Type=String,Description="Format: '
            'Allele|Consequence|IMPACT|SYMBOL|HGVSc|HGVSp|MAX_AF|gnomADe_AF|'
            'gnomADg_AF">\n'
            '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n'
            '1\t10\t.\tA\tT\t.\tPASS\tCSQ=T|stop_gained|HIGH|GENE|c.1A>T|p.X|'
            '0.0001||\tGT:DP:AD:GQ\t0/1:20:10,10:99\n'
        )
        calls, counts = collect_novel_calls({"caller": vcf})
        assert counts == {"caller": 1}
        fasta = Path(name) / "ref.fa"
        fasta.write_text(">1\n" + "ACGT" * 20 + "\n")
        pysam.faidx(str(fasta))
        gtf = Path(name) / "genes.gtf.gz"
        with gzip.open(gtf, "wt") as handle:
            handle.write('1\ttest\texon\t1\t5\t.\t+\t.\tgene_name "GENE";\n')
        screened = screen_calls(calls, gtf, fasta)
        assert len(screened) == 1
        assert screened[0].classes == ("coding_or_splice",)
        assert write_novel_candidates(Path(name) / "out.tsv", screened) == 1
        assert sequence_complexity("AAAAAAAAAACGT")[1] == 10
    print("self-check ok: novel-call parsing, filtering and phase interpretation")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--hc-vep", type=Path)
    parser.add_argument("--mutect-vep", type=Path)
    parser.add_argument("--delly", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--phased", type=Path)
    parser.add_argument("--candidates", type=Path)
    parser.add_argument("--novel-candidates", type=Path)
    parser.add_argument("--target-svs", type=Path)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--gtf", type=Path)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--all-candidates", type=Path)
    parser.add_argument("--compound-reconstructions", type=Path)
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    required = [
        args.hc_vep,
        args.mutect_vep,
        args.delly,
        args.manifest,
        args.phased,
        args.candidates,
        args.novel_candidates,
        args.target_svs,
        args.summary,
        args.gtf,
        args.reference,
        args.all_candidates,
        args.compound_reconstructions,
    ]
    if any(path is None for path in required):
        parser.error("all analysis paths are required")
    summary = analyze(args)
    compact = {key: value for key, value in summary.items() if key != "target_manifest"}
    print(json.dumps(compact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
