#!/usr/bin/env python3
"""GC-correct depth and combine it with a mappability-filtered BAF screen."""

from __future__ import annotations

import argparse
import bisect
import csv
import json
import math
import random
import statistics
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

AUTOSOMES = frozenset(map(str, range(1, 23)))
TARGETS = ("19", "20", "22")


@dataclass(frozen=True)
class DepthBin:
    chrom: str
    start: int
    gc: float
    mappability: float
    acgt: float
    depth: float


def percentile(values: list[float], quantile: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return math.nan
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)


def trimmed_mean(values: list[float], fraction: float = 0.05) -> float:
    ordered = sorted(values)
    cut = int(len(ordered) * fraction)
    kept = ordered[cut : len(ordered) - cut] if cut else ordered
    return statistics.fmean(kept)


def load_depth(bins_path: Path, counts_path: Path, minimum_map: float, minimum_acgt: float) -> list[DepthBin]:
    counts: dict[tuple[str, int], int] = {}
    with counts_path.open() as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            counts[(row["chrom"], int(row["start"]))] = int(row["aligned_bases"])
    result = []
    with bins_path.open() as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            key = (row["chrom"], int(row["start"]))
            if key not in counts:
                raise ValueError(f"missing count for bin {key}")
            length = int(row["length"])
            item = DepthBin(
                chrom=row["chrom"],
                start=key[1],
                gc=float(row["gc_fraction"]),
                mappability=float(row["mappability"]),
                acgt=float(row["acgt_fraction"]),
                depth=counts[key] / length,
            )
            if item.chrom in AUTOSOMES and item.mappability >= minimum_map and item.acgt >= minimum_acgt:
                result.append(item)
    if len(result) < 100:
        raise ValueError("too few eligible autosomal bins")
    return result


def fit_gc_model(training: list[DepthBin]) -> tuple[object, float]:
    by_gc: dict[int, list[float]] = defaultdict(list)
    for item in training:
        by_gc[round(item.gc * 200)].append(item.depth)
    curve = {key: statistics.median(values) for key, values in by_gc.items() if len(values) >= 20}
    if len(curve) < 10:
        raise ValueError("insufficient leave-one-chromosome-out GC support")
    keys = sorted(curve)

    def expected(gc: float) -> float:
        value = gc * 200
        upper_index = bisect.bisect_left(keys, value)
        if upper_index == 0:
            return curve[keys[0]]
        if upper_index == len(keys):
            return curve[keys[-1]]
        lower, upper = keys[upper_index - 1], keys[upper_index]
        fraction = (value - lower) / (upper - lower)
        return curve[lower] * (1 - fraction) + curve[upper] * fraction

    normalizer = statistics.median(item.depth / expected(item.gc) for item in training)
    return expected, normalizer


def corrected_ratio(target: list[DepthBin], training: list[DepthBin]) -> float:
    expected, normalizer = fit_gc_model(training)
    return statistics.median(item.depth / expected(item.gc) / normalizer for item in target)  # type: ignore[operator]


def spatial_blocks(items: list[object], block_size: int, coordinates: object) -> dict[str, list[list[object]]]:
    grouped: dict[tuple[str, int], list[object]] = defaultdict(list)
    for item in items:
        chrom, start = coordinates(item)  # type: ignore[operator]
        grouped[(chrom, start // block_size)].append(item)
    result: dict[str, list[list[object]]] = defaultdict(list)
    for (chrom, _), values in sorted(grouped.items()):
        result[chrom].append(values)
    return result


def resample_stratified(blocks: dict[str, list[list[object]]], rng: random.Random) -> list[object]:
    sampled: list[object] = []
    for chrom in sorted(blocks, key=int):
        chrom_blocks = blocks[chrom]
        for block in rng.choices(chrom_blocks, k=len(chrom_blocks)):
            sampled.extend(block)
    return sampled


def joint_depth_interval(
    target: list[DepthBin], training: list[DepthBin], block_size: int, seed: int, replicates: int
) -> tuple[float, float]:
    target_blocks = spatial_blocks(target, block_size, lambda item: (item.chrom, item.start))
    training_blocks = spatial_blocks(training, block_size, lambda item: (item.chrom, item.start))
    rng = random.Random(seed)
    estimates = []
    for _ in range(replicates):
        sampled_target = resample_stratified(target_blocks, rng)
        sampled_training = resample_stratified(training_blocks, rng)
        estimates.append(corrected_ratio(sampled_target, sampled_training))  # type: ignore[arg-type]
    return percentile(estimates, 0.025), percentile(estimates, 0.975)


def load_baf(
    path: Path, eligible_bins: set[tuple[str, int]], bin_size: int
) -> tuple[dict[str, list[tuple[int, float]]], Counter[str]]:
    per_bin: dict[tuple[str, int], list[float]] = defaultdict(list)
    site_counts: Counter[str] = Counter()
    with path.open() as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            chrom = row["chrom"].removeprefix("chr")
            position = int(row["pos"]) - 1
            if (chrom, position // bin_size * bin_size) not in eligible_bins:
                continue
            ref_count, alt_count = int(row["ref_count"]), int(row["alt_count"])
            total = ref_count + alt_count
            if total <= 0:
                continue
            deviation = alt_count / total - 0.5
            per_bin[(chrom, position // bin_size * bin_size)].append(
                deviation * deviation - 0.25 / total
            )
            site_counts[chrom] += 1
    result: dict[str, list[tuple[int, float]]] = defaultdict(list)
    for (chrom, start), values in per_bin.items():
        result[chrom].append((start, trimmed_mean(values)))
    return result, site_counts


def joint_baf_interval(
    target: list[tuple[int, float]],
    background: dict[str, list[tuple[int, float]]],
    block_size: int,
    seed: int,
    replicates: int,
) -> tuple[float, float]:
    target_items: list[object] = [("0", start, value) for start, value in target]
    background_items: list[object] = [
        (chrom, start, value) for chrom, values in background.items() for start, value in values
    ]
    target_blocks = spatial_blocks(target_items, block_size, lambda item: (item[0], item[1]))
    background_blocks = spatial_blocks(background_items, block_size, lambda item: (item[0], item[1]))
    rng = random.Random(seed)
    estimates = []
    for _ in range(replicates):
        sampled_target = resample_stratified(target_blocks, rng)
        sampled_background = resample_stratified(background_blocks, rng)
        estimates.append(
            trimmed_mean([item[2] for item in sampled_target])
            - trimmed_mean([item[2] for item in sampled_background])
        )
    return percentile(estimates, 0.025), percentile(estimates, 0.975)


def mosaic_from_excess(excess: float) -> float:
    deviation = math.sqrt(max(0.0, excess))
    return min(1.0, 4 * deviation / max(1e-9, 1 - 2 * deviation))


def analyze(
    bins_path: Path,
    counts_path: Path,
    baf_path: Path,
    output_json: Path,
    output_tsv: Path,
    bin_size: int,
    minimum_map: float,
    minimum_acgt: float,
    replicates: int,
) -> dict[str, object]:
    items = load_depth(bins_path, counts_path, minimum_map, minimum_acgt)
    eligible = {(item.chrom, item.start) for item in items}
    baf, baf_site_counts = load_baf(baf_path, eligible, bin_size)
    autosomal_baf = [value for chrom, values in baf.items() if chrom in AUTOSOMES for _, value in values]
    if len(autosomal_baf) < 100:
        raise ValueError("too few eligible heterozygous SNVs")
    chromosomes: dict[str, dict[str, object]] = {}
    for index, chrom in enumerate(TARGETS):
        target_depth = [item for item in items if item.chrom == chrom]
        training_depth = [item for item in items if item.chrom != chrom]
        ratio = corrected_ratio(target_depth, training_depth)
        depth_ci = joint_depth_interval(
            target_depth, training_depth, bin_size * 10, 1000 + index, replicates
        )
        baf_values = baf.get(chrom, [])
        if len(baf_values) >= 20:
            background_baf = {key: values for key, values in baf.items() if key != chrom}
            baseline_baf = trimmed_mean([value for values in background_baf.values() for _, value in values])
            baf_excess = trimmed_mean([value for _, value in baf_values]) - baseline_baf
            baf_ci = joint_baf_interval(
                baf_values, background_baf, bin_size * 10, 2000 + index, replicates
            )
        else:
            baf_excess, baf_ci = math.nan, (math.nan, math.nan)
        depth_support = depth_ci[0] > 1.01
        baf_support = baf_ci[0] > 0
        if depth_support and baf_support:
            conclusion = "supports_low_level_mosaic_gain"
        elif depth_ci[0] <= 1.0 <= depth_ci[1] and (math.isnan(baf_ci[0]) or baf_ci[0] <= 0):
            conclusion = "no_gain_after_correction"
        else:
            conclusion = "not_jointly_supported"
        chromosomes[chrom] = {
            "eligible_depth_bins": len(target_depth),
            "depth_ratio": ratio,
            "depth_ratio_ci95": list(depth_ci),
            "depth_mosaic_fraction_estimate": max(0.0, 2 * (ratio - 1)),
            "eligible_baf_sites": baf_site_counts[chrom],
            "eligible_baf_100kb_bins": len(baf_values),
            "baf_excess_variance": baf_excess,
            "baf_excess_variance_ci95": list(baf_ci),
            "baf_mosaic_fraction_estimate": mosaic_from_excess(baf_excess) if not math.isnan(baf_excess) else math.nan,
            "conclusion": conclusion,
        }

    summary: dict[str, object] = {
        "method": {
            "bin_size": bin_size,
            "minimum_mappability": minimum_map,
            "minimum_acgt_fraction": minimum_acgt,
            "gc_correction": "leave-one-chromosome-out 0.5%-GC median curve with linear interpolation",
            "bootstrap_replicates": replicates,
            "depth_interval": "chromosome-stratified 1 Mb block bootstrap jointly refitting target, GC curve and normalizer",
            "baf_metric": "trimmed mean of (BAF-0.5)^2 minus binomial sampling variance",
            "baf_interval": "chromosome-stratified 1 Mb block bootstrap jointly resampling target and leave-target-out baseline",
            "joint_support_rule": "depth CI lower bound >1.01 and BAF excess CI lower bound >0",
        },
        "eligible_autosomal_bins": len(items),
        "eligible_autosomal_baf_sites": sum(baf_site_counts.values()),
        "eligible_autosomal_baf_100kb_bins": len(autosomal_baf),
        "chromosomes": chromosomes,
        "targets": {chrom: chromosomes.get(chrom) for chrom in TARGETS},
        "limitations": [
            "single-subject copy-number screen without a matched control cohort; intervals do not capture between-sample technical variation",
            "mosaic fraction estimates are approximate and not a clinical karyotype",
            "this analysis does not establish phase for any small-variant pair",
        ],
    }
    output_json.write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    with output_tsv.open("w") as handle:
        handle.write("chrom\tdepth_ratio\tdepth_ci_low\tdepth_ci_high\tbaf_excess\tbaf_ci_low\tbaf_ci_high\tconclusion\n")
        for chrom, values in chromosomes.items():
            dci = values["depth_ratio_ci95"]
            bci = values["baf_excess_variance_ci95"]
            handle.write(
                f"{chrom}\t{values['depth_ratio']:.6f}\t{dci[0]:.6f}\t{dci[1]:.6f}\t"
                f"{values['baf_excess_variance']:.8f}\t{bci[0]:.8f}\t{bci[1]:.8f}\t{values['conclusion']}\n"
            )
    return summary


def synthetic_case(root: Path, mosaic: bool) -> dict[str, object]:
    bins = root / "bins.tsv"
    counts = root / "counts.tsv"
    baf_path = root / "baf.tsv"
    with bins.open("w") as b, counts.open("w") as c, baf_path.open("w") as a:
        b.write("chrom\tstart\tend\tlength\tacgt_fraction\tgc_fraction\tmappability\n")
        c.write("chrom\tstart\tend\taligned_bases\n")
        a.write("chrom\tpos\tdp\tref_count\talt_count\n")
        for chrom in ("1", "2", "19", "20", "22"):
            for index in range(500):
                start = index * 1000
                gc = 0.35 + (index % 30) / 100
                gc_bias = 0.8 + gc
                ratio = 1.08 if mosaic and chrom == "20" else 1.0
                b.write(f"{chrom}\t{start}\t{start + 1000}\t1000\t1\t{gc:.3f}\t0.99\n")
                c.write(f"{chrom}\t{start}\t{start + 1000}\t{round(40000 * gc_bias * ratio)}\n")
                for site in range(5):
                    alt = 27 if mosaic and chrom == "20" and (index + site) % 2 else 23 if mosaic and chrom == "20" else 25
                    a.write(f"{chrom}\t{start + site + 1}\t50\t{50 - alt}\t{alt}\n")
    return analyze(bins, counts, baf_path, root / "out.json", root / "out.tsv", 1000, 0.9, 0.95, 200)


def self_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        positive = synthetic_case(root, True)
        assert positive["targets"]["20"]["conclusion"] == "supports_low_level_mosaic_gain"  # type: ignore[index]
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        negative = synthetic_case(root, False)
        assert negative["targets"]["20"]["conclusion"] == "no_gain_after_correction"  # type: ignore[index]
    print("analyze_copy_number self-check ok")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bins", nargs="?", type=Path)
    parser.add_argument("counts", nargs="?", type=Path)
    parser.add_argument("baf", nargs="?", type=Path)
    parser.add_argument("output_json", nargs="?", type=Path)
    parser.add_argument("output_tsv", nargs="?", type=Path)
    parser.add_argument("--bin-size", type=int, default=100_000)
    parser.add_argument("--minimum-mappability", type=float, default=0.9)
    parser.add_argument("--minimum-acgt", type=float, default=0.95)
    parser.add_argument("--bootstrap-replicates", type=int, default=2000)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    required = (args.bins, args.counts, args.baf, args.output_json, args.output_tsv)
    if None in required:
        parser.error("bins, counts, BAF, JSON and TSV paths are required")
    analyze(*required, args.bin_size, args.minimum_mappability, args.minimum_acgt, args.bootstrap_replicates)


if __name__ == "__main__":
    main()
