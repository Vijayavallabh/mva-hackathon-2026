#!/usr/bin/env python3
"""Read-only Track 1 uncertainty audits; never an uploader or clinical phase caller.

Only aggregate evidence and submitted-candidate summaries are printed. Native
records, sample values, phase identifiers and non-submission alleles stay local.
"""
from __future__ import annotations

import argparse
import csv
from contextlib import contextmanager
from dataclasses import asdict
from itertools import product
import json
import math
import os
from pathlib import Path
import tempfile

import pysam

from track1_submission import (
    PROBAND_ID, load_official_scorer, parse_variant, read_submission, sha256,
    validate_rows,
)


def submission_rows(path: Path):
    rows = read_submission(path)
    validate_rows(rows, require_ten=False)
    return rows


def pair_key(row):
    return frozenset(tuple(v) for suffix in ("1", "2")
                     if (v := parse_variant(row, suffix, 0)) is not None)


def provenance(path: Path, *, content_hash: bool = True):
    stat = path.stat()
    result = {"path": str(path), "size": stat.st_size, "mtime_ns": stat.st_mtime_ns}
    if content_hash:
        result["sha256"] = sha256(path)
    return result


def score_scenarios(path: Path):
    submission_rows(path)
    official = load_official_scorer()
    rows = official.load_submission(str(path))[PROBAND_ID]
    if any(len(row.variants) != 2 for row in rows):
        raise ValueError("scenario audit requires two distinct alleles in every row")
    # These deliberately non-genomic tokens represent unseen truth, not new variants.
    absent = [("HYPOTHETICAL_UNSUBMITTED", i, "A", "T") for i in (1, 2)]
    assumptions = [(f"submitted_pair_at_rank_{row.rank}", row.variants) for row in rows]
    for i, allele in enumerate(sorted(rows[0].variants), 1):
        assumptions.append((f"only_top_pair_allele_{i}_is_true_other_not_submitted",
                            frozenset((allele, absent[0]))))
    assumptions.append(("neither_true_allele_submitted", frozenset(absent)))
    scenarios = []
    for label, truth in assumptions:
        scenarios.append({"hypothetical_assumption": label,
                          **asdict(official.score_proband(PROBAND_ID, rows, truth))})
    return {
        "actual_competition_score": None,
        "official_receipt_checked": False,
        "guaranteed_perfect_score": False,
        "status": "HYPOTHETICAL_SCENARIOS_ONLY_NOT_A_SCORE_PREDICTION",
        "limitation": "No private answer key. Scenarios have no assigned probabilities. "
                      "EPCR is not calibrated confidence. This audit does not check reference normalization.",
        "submission": provenance(path),
        "scenarios": scenarios,
    }


def finite_number(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("nonfinite ranking field")
    return number


def rank_sensitivity(csv_path: Path, candidates_path: Path):
    submitted = submission_rows(csv_path)
    target = pair_key(submitted[0])
    with candidates_path.open() as handle:
        records = list(csv.DictReader(handle, delimiter="\t"))
    rows = [r for r in records if r["model"] == "compound_heterozygous"]
    if not rows or sum(pair_key(r) == target for r in rows) != 1:
        raise ValueError("leading submitted pair must occur exactly once in all-pair table")
    if len({pair_key(r) for r in rows}) != len(rows):
        raise ValueError("duplicate pair in all-pair table")
    prepared = []
    for row in rows:
        phi = finite_number(row["proband_similarity"])
        family = finite_number(row["family_history_similarity"])
        coverage = int(row["proband_coverage_of_7"])
        if not (0 <= phi <= 1 and 0 <= family <= 1 and 0 <= coverage <= 7):
            raise ValueError("phenotype field outside its domain")
        missing = predictions = clinvar = 0
        for suffix in ("1", "2"):
            missing += row[f"max_af_{suffix}"] == ""
            predictions += "deleterious" in row[f"sift_{suffix}"].casefold()
            predictions += "damaging" in row[f"polyphen_{suffix}"].casefold()
            sig = row[f"clinvar_{suffix}"].casefold()
            clinvar += 2 * ("pathogenic" in sig and "conflict" not in sig)
        prepared.append({"key": pair_key(row), "gene": row["gene"], "phi": phi,
                         "family": family, "coverage": coverage,
                         "baseline": finite_number(row["total_score"]),
                         "missing": missing / 2, "predictions": predictions / 2,
                         "clinvar": clinvar / 2})
    # Frozen declared grid; weights of zero are ablation controls, not preferred models.
    settings = [(p, f, m, True, True) for p, f, m in
                product((0.0, 4.0, 8.0, 12.0, 16.0), (0.0, 0.5, 2.0), (0.0, 1.0))]
    settings.extend([(8.0, 0.5, 1.0, False, True), (8.0, 0.5, 1.0, True, False),
                     (8.0, 0.5, 1.0, False, False), (8.0, 0.5, 0.0, False, False)])
    scenarios = []
    for p, f, m, use_predictions, use_clinvar in settings:
        def adjusted(row):
            return (row["baseline"] + (p - 8) * row["phi"] + (f - 0.5) * row["family"]
                    + (m - 1) * row["missing"]
                    - (not use_predictions) * row["predictions"]
                    - (not use_clinvar) * row["clinvar"])
        ranked = sorted(prepared, key=lambda r: (adjusted(r), r["coverage"], r["gene"]),
                        reverse=True)
        index = next(i for i, r in enumerate(ranked) if r["key"] == target)
        target_score = adjusted(ranked[index])
        scenarios.append({"proband_weight": p, "family_weight": f,
                          "missing_af_credit": m, "prediction_bonus": use_predictions,
                          "clinvar_bonus": use_clinvar, "leading_pair_rank": index + 1,
                          "top_gene": ranked[0]["gene"],
                          "leading_pair_margin_over_best_other": target_score - max(
                              adjusted(r) for r in ranked if r["key"] != target),
                          "leading_pair_score_ties": sum(
                              abs(adjusted(r) - target_score) <= 1e-5 for r in ranked) - 1})
    return {"status": "CONDITIONAL_RANK_SENSITIVITY_NOT_VALIDATION",
            "submission": provenance(csv_path), "candidate_table": provenance(candidates_path),
            "retained_pairs_tested": len(rows), "retained_genes_tested": len({r["gene"] for r in rows}),
            "scenario_count": len(scenarios),
            "leading_pair_best_rank": min(s["leading_pair_rank"] for s in scenarios),
            "leading_pair_worst_rank": max(s["leading_pair_rank"] for s in scenarios),
            "scenarios": scenarios,
            "limitation": "Fixed retained candidate universe and rounded baseline scores. "
                          "Does not test discarded variants, every transcript, alternative callers, "
                          "phenotype annotation bias or clinical causality. Grid frequencies are not probabilities."}


def present(value):
    return value is not None and value not in ("", ".", (), (None,), (".",))


def phase_encoding(record, sample):
    """Private in-memory representation. Never serialize its identifiers or GT."""
    call = record.samples[sample]
    gt = call.get("GT")
    heterozygous = gt in ((0, 1), (1, 0))
    result = {"GT_PS": None, "PGT_PID": None, "invalid_pgt": False,
              "gt_phased": bool(call.phased), "heterozygous": heterozygous,
              "hp_present": present(call.get("HP"))}
    if heterozygous and call.phased and present(call.get("PS")):
        result["GT_PS"] = (call["PS"], gt.index(1))
    if present(call.get("PGT")):
        pgt = call["PGT"]
        if not heterozygous or pgt not in ("0|1", "1|0"):
            result["invalid_pgt"] = True
        elif present(call.get("PID")):
            result["PGT_PID"] = (call["PID"], pgt.split("|").index("1"))
    return result


def compare_encodings(encodings):
    relations = {}
    for scheme in ("GT_PS", "PGT_PID"):
        left, right = [e[scheme] if e else None for e in encodings]
        relations[scheme] = ("unconfirmed" if not left or not right or left[0] != right[0]
                             else "cis" if left[1] == right[1] else "trans")
    positive = set(relations.values()) - {"unconfirmed"}
    if any(e and (e["invalid_pgt"] or e["hp_present"]) for e in encodings):
        overall = "manual_review_required"
    elif len(positive) > 1:
        overall = "conflicting_encodings"
    else:
        overall = next(iter(positive), "unconfirmed")
    return relations, overall


@contextmanager
def native_diagnostics_guard():
    """Contain C-library stderr; any diagnostic fails closed without exposing it.

    File-descriptor redirection is process-global: this CLI is single-threaded.
    The temporary diagnostic bytes stay local and are discarded without reading.
    """
    with tempfile.TemporaryFile() as diagnostics:
        saved = os.dup(2)
        try:
            os.dup2(diagnostics.fileno(), 2)
            try:
                yield
            except Exception:
                raise ValueError("native VCF processing failed; details suppressed") from None
        finally:
            os.dup2(saved, 2)
            os.close(saved)
        if diagnostics.seek(0, os.SEEK_END):
            raise ValueError("native VCF diagnostic detected; details suppressed")


def native_phase(csv_path: Path, vcf_path: Path, expected_sample: str, index_path: Path | None = None):
    leading = submission_rows(csv_path)[0]
    targets = sorted(pair_key(leading))
    if len(targets) != 2 or targets[0][0] != targets[1][0]:
        raise ValueError("leading row must be a same-chromosome pair")
    if any(len(ref) != 1 or len(alt) != 1 for _, _, ref, alt in targets):
        raise ValueError("native phase audit currently requires biallelic SNV targets")
    statuses, encodings = [], []
    with native_diagnostics_guard(), pysam.VariantFile(
        vcf_path, index_filename=str(index_path) if index_path else None
    ) as vcf:
        if list(vcf.header.samples) != [expected_sample]:
            raise ValueError("VCF sample identity mismatch; no sample inferred")
        for chrom, pos, ref, alt in targets:
            local_chrom = chrom if chrom in vcf.header.contigs else chrom.removeprefix("chr")
            # Numeric fetch is zero-based, half-open (not the VCF's one-based POS).
            matches = [r for r in vcf.fetch(local_chrom, pos - 1, pos)
                       if r.pos == pos and r.ref == ref and r.alts == (alt,)]
            encoding = phase_encoding(matches[0], expected_sample) if len(matches) == 1 else None
            encodings.append(encoding)
            statuses.append({"exact_match_count": len(matches),
                             "heterozygous": bool(encoding and encoding["heterozygous"]),
                             "gt_phased": bool(encoding and encoding["gt_phased"]),
                             "gt_ps_present": bool(encoding and encoding["GT_PS"]),
                             "pgt_pid_present": bool(encoding and encoding["PGT_PID"]),
                             "invalid_pgt": bool(encoding and encoding["invalid_pgt"]),
                             "uninterpreted_hp_present": bool(encoding and encoding["hp_present"])})
        declared = [key for key in ("GT", "PS", "PGT", "PID", "HP") if key in vcf.header.formats]
    relations, overall = compare_encodings(encodings)
    return {"status": "NATIVE_PHASE_ENCODING_AUDIT_NOT_CLINICAL_CONFIRMATION",
            "submission": provenance(csv_path), "vcf": provenance(vcf_path, content_hash=False),
            "explicit_index": provenance(index_path) if index_path else None,
            "declared_phase_fields": declared, "targets": statuses,
            "encoded_relations": relations, "combined_encoding_status": overall,
            "biological_phase_confirmed": False,
            "limitation": "Missing tags, separate groups, or unphased calls do not establish cis or trans. "
                          "Explicit shared groups required; implicit chromosome-wide phase is not assumed. "
                          "Positive encodings require caller/read evidence review; HP is flagged for review. "
                          "VCF provenance is size/mtime, not a content checksum."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    scores = subs.add_parser("scores", help="hypothetical score scenarios, never an official score")
    ranking = subs.add_parser("ranking", help="fixed-universe ranking sensitivity")
    phase = subs.add_parser("phase", help="inspect native phase metadata without emitting records")
    for command in (scores, ranking, phase):
        command.add_argument("submission", type=Path)
    ranking.add_argument("--candidates", type=Path, required=True)
    phase.add_argument("--vcf", type=Path, required=True)
    phase.add_argument("--sample", required=True)
    phase.add_argument("--index", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "scores":
            result = score_scenarios(args.submission)
        elif args.command == "ranking":
            result = rank_sensitivity(args.submission, args.candidates)
        else:
            result = native_phase(args.submission, args.vcf, args.sample, args.index)
        result["audit_script_sha256"] = sha256(Path(__file__))
        print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    except (ValueError, KeyError, OSError, TypeError) as error:
        # htslib/record exception text can contain subject-level fields: do not echo it.
        raise SystemExit(f"Evidence audit failed ({type(error).__name__}); check local inputs; no records emitted.") from None


if __name__ == "__main__":
    main()
