#!/usr/bin/env python3
"""Local SNV fragment-connectivity audit, not a haplotype or clinical phase caller.

Only aggregate evidence is emitted. Reads, marker alleles, identifiers and edges
remain in memory. No network calls. Input files are never modified.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import hashlib
import sys

import pysam


def load_markers(inputs, chrom, start, end, targets):
    """Union of eligible heterozygous SNVs, with ambiguous positions removed.

    Unfiltered records are accepted only for explicitly designated recall inputs.
    Do not use pysam's FILTER membership test: PASS can match an empty FILTER.
    """
    markers = defaultdict(set)
    per_input = []
    for path, allow_unfiltered in inputs:
        counts = Counter()
        with pysam.VariantFile(path) as vcf:
            if list(vcf.header.samples) != ["PROBAND01"]:
                raise ValueError("each marker VCF must contain only PROBAND01")
            for record in vcf.fetch(chrom, start, end):
                call = next(iter(record.samples.values()))
                if set(call.get("GT") or ()) != {0, 1} or len(call["GT"]) != 2:
                    continue
                counts["heterozygous_records"] += 1
                filters = set(record.filter.keys())
                if filters != {"PASS"} and not (allow_unfiltered and not filters):
                    continue
                counts["unfiltered_heterozygous_records" if not filters else "pass_heterozygous_records"] += 1
                if len(record.alleles) != 2 or any(
                    len(a) != 1 or a not in "ACGT" for a in record.alleles
                ):
                    continue
                if (call.get("GQ") or 0) < 20 or (call.get("DP") or 0) < 10:
                    continue
                markers[record.start].add(tuple(record.alleles))
                counts["accepted_snv_records"] += 1
        per_input.append({"allow_unfiltered": allow_unfiltered, **dict(counts)})
    ambiguous = sum(len(alleles) != 1 for alleles in markers.values())
    result = {pos: next(iter(alleles)) for pos, alleles in markers.items() if len(alleles) == 1}
    for pos, alleles in targets:
        if result.get(pos) != alleles:
            raise ValueError("a target is absent, conflicting or fails marker quality filters")
    return result, per_input, ambiguous


def read_observations(read, markers, baseq):
    observations = {}
    if read.query_sequence is None or read.query_qualities is None:
        return observations
    for query_pos, ref_pos in read.get_aligned_pairs(matches_only=True):
        if ref_pos not in markers or read.query_qualities[query_pos] < baseq:
            continue
        base = read.query_sequence[query_pos]
        if base in markers[ref_pos]:
            observations[ref_pos] = markers[ref_pos].index(base)
    return observations


def merge_observations(existing, incoming):
    # A discordant overlapping mate call remains excluded even if a third call agrees.
    for pos, allele in incoming.items():
        if pos in existing and existing[pos] != allele:
            existing[pos] = None
        else:
            existing[pos] = allele


def component(edges, source, minimum):
    neighbors = defaultdict(set)
    for (left, right), count in edges.items():
        if count >= minimum:
            neighbors[left].add(right)
            neighbors[right].add(left)
    visited = {source}
    todo = [source]
    while todo:
        for neighbor in neighbors[todo.pop()] - visited:
            visited.add(neighbor)
            todo.append(neighbor)
    return visited


def summarize_fragments(fragments, targets):
    edges = Counter()
    direct = Counter()
    covered = [Counter(), Counter()]
    informative = conflicts = 0
    for calls in fragments.values():
        conflicts += sum(value is None for value in calls.values())
        calls = {pos: allele for pos, allele in calls.items() if allele is not None}
        informative += len(calls) >= 2
        edges.update(combinations(sorted(calls), 2))
        for index, target in enumerate(targets):
            if target in calls:
                covered[index][calls[target]] += 1
        if all(target in calls for target in targets):
            direct["".join("A" if calls[pos] else "R" for pos in targets)] += 1
    connectivity = {}
    for minimum in (1, 3):
        left = component(edges, targets[0], minimum)
        right = component(edges, targets[1], minimum)
        connectivity[str(minimum)] = {
            "targets_connected": targets[1] in left,
            "target_component_sizes": [len(left), len(right)],
            "target_neighbor_counts": [
                sum(target in edge and count >= minimum for edge, count in edges.items())
                for target in targets
            ],
        }
    return {
        "fragments_with_marker_observations": len(fragments),
        "fragments_with_at_least_two_markers": informative,
        "conflicting_fragment_site_calls_excluded": conflicts,
        "target_fragment_support": [
            {"reference": c[0], "alternate": c[1]} for c in covered
        ],
        "direct_target_pair_fragments": {key: direct[key] for key in ("RR", "RA", "AR", "AA")},
        "connectivity_by_minimum_edge_fragments": connectivity,
    }


def audit_reads(bam_path, chrom, start, end, markers, targets, mapq, baseq):
    fragments = defaultdict(dict)
    counts = Counter()
    lengths = []
    template_lengths = []
    with pysam.AlignmentFile(bam_path, "rb") as bam:
        groups = bam.header.to_dict().get("RG", [])
        group_samples = {g["ID"]: g.get("SM") for g in groups}
        if not groups or set(group_samples.values()) != {"PROBAND01"}:
            raise ValueError("BAM read-group sample identity is not exclusively PROBAND01")
        for read in bam.fetch(chrom, start, end):
            counts["fetched_alignments"] += 1
            if (read.is_unmapped or read.is_secondary or read.is_supplementary
                    or read.is_duplicate or read.is_qcfail or read.mapping_quality < mapq):
                continue
            if not read.has_tag("RG") or read.get_tag("RG") not in group_samples:
                raise ValueError("eligible alignment has missing or unrecognized read group")
            counts["accepted_alignments"] += 1
            lengths.append(read.query_length or 0)
            paired = (read.is_paired and read.is_proper_pair and not read.mate_is_unmapped
                      and read.reference_id == read.next_reference_id)
            if paired and read.is_read1:
                template_lengths.append(abs(read.template_length))
            observations = read_observations(read, markers, baseq)
            if not observations:
                continue
            # Only proper pairs can link their two alignments. Other primary reads
            # contribute individually, never via mate position/template length alone.
            key = (read.get_tag("RG"), read.query_name,
                   "pair" if paired else (read.is_read1, read.reference_start))
            merge_observations(fragments[key], observations)
    summary = summarize_fragments(fragments, targets)
    summary.update({"mapq": mapq, "baseq": baseq, "alignment_counts": dict(counts),
                    "read_length_max": max(lengths, default=0),
                    "proper_pair_template_length_median": median(template_lengths),
                    "proper_pair_template_length_max": max(template_lengths, default=0)})
    return summary


def median(values):
    values = sorted(values)
    if not values:
        return None
    n = len(values)
    return (values[(n - 1) // 2] + values[n // 2]) / 2


def phase_status(path, chrom, targets):
    """Read categorical status only; never emit marker records or phase-set IDs."""
    calls = []
    with pysam.VariantFile(path) as vcf:
        if list(vcf.header.samples) != ["PROBAND01"]:
            raise ValueError("phased VCF must contain only PROBAND01")
        for pos, alleles in targets:
            matches = [rec for rec in vcf.fetch(chrom, pos, pos + 1)
                       if rec.start == pos and tuple(rec.alleles) == alleles]
            if len(matches) != 1:
                calls.append(None)
                continue
            sample = matches[0].samples["PROBAND01"]
            calls.append((sample.phased, sample.get("GT"), sample.get("PS")))
    found = [call is not None for call in calls]
    phased = [bool(call and call[0]) for call in calls]
    same_set = bool(all(phased) and calls[0][2] is not None and calls[0][2] == calls[1][2])
    biallelic_het = all(call and call[1] in ((0, 1), (1, 0)) for call in calls)
    relation = "unconfirmed"
    if same_set and biallelic_het:
        relation = "cis" if calls[0][1] == calls[1][1] else "trans"
    return {"path": str(path), "targets_found": found, "targets_phased": phased,
            "shared_phase_set": same_set, "encoded_phase_relation": relation,
            "qualification": "VCF encoding only; any positive result requires evidence review"}


def target_argument(value):
    pos, ref, alt = value.split(":")
    if int(pos) < 1 or len(ref) != 1 or len(alt) != 1 or ref == alt or any(a not in "ACGT" for a in (ref, alt)):
        raise argparse.ArgumentTypeError("target must be a 1-based POS:REF:ALT SNV")
    return int(pos) - 1, (ref, alt)


def self_check():
    disconnected = summarize_fragments({"a": {10: 0}, "b": {20: 1}}, [10, 20])
    assert not disconnected["connectivity_by_minimum_edge_fragments"]["1"]["targets_connected"]
    connected = summarize_fragments({"a": {10: 0, 15: 1}, "b": {15: 1, 20: 0}}, [10, 20])
    assert connected["connectivity_by_minimum_edge_fragments"]["1"]["targets_connected"]
    assert not connected["connectivity_by_minimum_edge_fragments"]["3"]["targets_connected"]
    assert sum(connected["direct_target_pair_fragments"].values()) == 0
    for calls, label in (({10: 0, 20: 0}, "RR"), ({10: 0, 20: 1}, "RA"),
                         ({10: 1, 20: 0}, "AR"), ({10: 1, 20: 1}, "AA")):
        assert summarize_fragments({"a": calls}, [10, 20])["direct_target_pair_fragments"][label] == 1
    calls = {10: 0}
    merge_observations(calls, {10: 1, 20: 0})
    merge_observations(calls, {10: 0})
    assert calls == {10: None, 20: 0}
    read = pysam.AlignedSegment()
    read.query_name = "synthetic"
    read.query_sequence = "ACTG"
    read.reference_start = 10
    read.cigarstring = "2M1D2M"
    read.query_qualities = [30, 5, 30, 30]
    assert read_observations(read, {10: ("A", "G"), 11: ("C", "T"),
                                    12: ("A", "G"), 13: ("T", "C")}, 20) == {10: 0, 13: 0}
    assert median([3, 1, 2, 4]) == 2.5
    print("phase audit self-check: disconnection, indirect links, support threshold, four pair states, mate conflicts, base quality and CIGAR pass")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bam", type=Path)
    parser.add_argument("--vcf", type=Path, action="append")
    parser.add_argument("--unfiltered-vcf", type=Path, action="append", default=[],
                        help="Additional recall VCF: explicitly allow FILTER=dot as well as PASS")
    parser.add_argument("--phased-vcf", type=Path, action="append", default=[])
    parser.add_argument("--bed", type=Path)
    parser.add_argument("--left", type=target_argument)
    parser.add_argument("--right", type=target_argument)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if any(getattr(args, key) is None for key in ("bam", "vcf", "bed", "left", "right")):
        parser.error("bam, vcf, bed and both target SNVs are required")
    chrom, start, end = args.bed.read_text().strip().split()
    start, end = int(start), int(end)
    targets = [args.left, args.right]
    if not start <= targets[0][0] < targets[1][0] < end:
        parser.error("targets must be ordered, distinct and within the BED interval")
    marker_inputs = [(p, False) for p in args.vcf] + [(p, True) for p in args.unfiltered_vcf]
    markers, input_counts, ambiguous = load_markers(marker_inputs, chrom, start, end, targets)
    report = {
        "method": "SNV-only fragment connectivity; not a phase caller",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "pysam_version": pysam.__version__,
        "inputs": [{"path": str(p), "size": p.stat().st_size, "mtime_ns": p.stat().st_mtime_ns}
                   for p in [args.bam, *args.vcf, *args.unfiltered_vcf, *args.phased_vcf, args.bed]],
        "interval_size_bp": end - start,
        "target_distance_bp": targets[1][0] - targets[0][0],
        "marker_input_counts": input_counts,
        "accepted_union_snv_markers": len(markers),
        "ambiguous_marker_positions_excluded": ambiguous,
        "nearest_other_snv_distance_bp": [min(abs(pos - target[0]) for pos in markers if pos != target[0]) for target in targets],
        "sensitivity_runs": [audit_reads(args.bam, chrom, start, end, markers,
                                        [t[0] for t in targets], mq, bq)
                             for mq, bq in ((30, 20), (20, 13))],
        "phased_vcf_checks": [phase_status(path, chrom, targets) for path in args.phased_vcf],
        "phase_conclusion": "unconfirmed; connectivity alone never establishes cis or trans",
        "limitations": ["SNVs only; indels and structural alleles are not graph nodes",
                        "Edges measure co-observation, not phase consistency or calibrated confidence",
                        "No parental genotypes or long-read data added",
                        "Input sizes/mtimes are provenance metadata, not full BAM content hashes"],
    }
    json.dump(report, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
