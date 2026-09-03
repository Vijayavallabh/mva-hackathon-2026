#!/usr/bin/env python3
"""Build and rigorously check a Track 1 submission with the official scorer.

The private answer key is not available locally.  ``check`` therefore reports the exact
official score under an explicit, hypothetical assumption that one selected submitted row
is the truth.  This proves scoring/conformance behavior without claiming validation against
the hidden causal variants.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import re
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from types import ModuleType
from typing import NamedTuple

ROOT = Path(__file__).resolve().parent.parent
OFFICIAL_SCORER = ROOT / "scripts/vendor/evaluation.py"
OFFICIAL_TEMPLATE = ROOT / "scripts/track1_submission_template.csv"
DEFAULT_CANDIDATES = ROOT / "results/feat004/compound_het_candidates.tsv"
DEFAULT_SUBMISSION = ROOT / "results/feat006/track1_candidate.csv"
DEFAULT_REPORT = ROOT / "results/feat006/track1_candidate.check.json"
DEFAULT_REFERENCE = (
    ROOT
    / "data/resources/reference/"
    "GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_"
    "maskedGRC_exclusions_v2_no_chr.fasta"
)
DEFAULT_BCFTOOLS = ROOT / "tools/install/bin/bcftools"
DEFAULT_SAMTOOLS = ROOT / "tools/install/bin/samtools"
PROBAND_ID = "PROBAND01"
OFFICIAL_REVISION = "1c761cc23d90aebe6a011fd5b0b99517df42408c"
OFFICIAL_SCORER_SHA256 = "6d18b581e65a45e1ccc120071d588e740c2e42e983ff50704c60a40232b19180"
TRACKED_TEMPLATE_SHA256 = "0c9cc378c6f8025b7fd538c37fd0331bff5a9f7dd53fd2e9ccbfe2a2da659643"
SCHEMA = (
    "proband_id",
    "chrom_1",
    "pos_1",
    "ref_1",
    "alt_1",
    "chrom_2",
    "pos_2",
    "ref_2",
    "alt_2",
    "epcr",
    "finding_type",
    "notes",
)
ALLELE_RE = re.compile(r"[ACGT]+")
BUILD_EPCR = (0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50)


class ConformanceError(ValueError):
    """A submission violates an official or predeclared readiness rule."""


class Variant(NamedTuple):
    chrom: str
    pos: int
    ref: str
    alt: str


@dataclass(frozen=True)
class SubmittedVariant:
    csv_row: int
    allele_number: str
    variant: Variant


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_official_scorer() -> ModuleType:
    observed_hash = sha256(OFFICIAL_SCORER)
    if observed_hash != OFFICIAL_SCORER_SHA256:
        raise RuntimeError(
            f"vendored scorer checksum mismatch: {observed_hash}; "
            f"expected {OFFICIAL_SCORER_SHA256}"
        )
    spec = importlib.util.spec_from_file_location("official_track1_evaluation", OFFICIAL_SCORER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load official scorer: {OFFICIAL_SCORER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_submission(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ConformanceError("submission has no header")
        if tuple(reader.fieldnames) != SCHEMA:
            raise ConformanceError(
                "header must exactly match the official ordered schema: " + ",".join(SCHEMA)
            )
        rows = list(reader)
    for row_number, row in enumerate(rows, 2):
        if None in row or any(value is None for value in row.values()):
            raise ConformanceError(
                f"row {row_number}: row width does not match the official schema"
            )
    if not rows:
        raise ConformanceError("submission must contain at least one row")
    if len(rows) > 10:
        raise ConformanceError(f"submission has {len(rows)} rows; official maximum is 10")
    return rows


def parse_variant(
    row: dict[str, str], suffix: str, row_number: int
) -> Variant | None:
    fields = tuple(row[f"{name}_{suffix}"].strip() for name in ("chrom", "pos", "ref", "alt"))
    if suffix == "2" and not any(fields):
        return None
    if not all(fields):
        raise ConformanceError(
            f"row {row_number}: allele {suffix} must have all four fields or, for allele 2, none"
        )
    chrom, pos_text, ref, alt = fields
    if not chrom.startswith("chr") or len(chrom) == 3 or any(char.isspace() for char in chrom):
        raise ConformanceError(f"row {row_number}: chromosome must be chr-prefixed: {chrom!r}")
    if not pos_text.isascii() or not pos_text.isdigit() or int(pos_text) <= 0:
        raise ConformanceError(f"row {row_number}: position must be a positive integer")
    if not ALLELE_RE.fullmatch(ref) or not ALLELE_RE.fullmatch(alt):
        raise ConformanceError(
            f"row {row_number}: REF and ALT must be uppercase unambiguous DNA alleles"
        )
    if ref == alt:
        raise ConformanceError(f"row {row_number}: REF and ALT must differ")
    return Variant(chrom, int(pos_text), ref, alt)


def validate_rows(
    rows: list[dict[str, str]], require_ten: bool
) -> list[SubmittedVariant]:
    if require_ten and len(rows) != 10:
        raise ConformanceError(
            f"submission-ready mode requires exactly 10 rows; found {len(rows)}"
        )
    variants: list[SubmittedVariant] = []
    epcrs: list[float] = []
    seen_sets: set[frozenset] = set()
    for row_number, row in enumerate(rows, 2):
        if row["proband_id"] != PROBAND_ID:
            raise ConformanceError(
                f"row {row_number}: proband_id must be exactly {PROBAND_ID}"
            )
        first = parse_variant(row, "1", row_number)
        second = parse_variant(row, "2", row_number)
        assert first is not None
        if second == first:
            raise ConformanceError(f"row {row_number}: a pair cannot repeat the same allele")
        variant_set = frozenset((first, second) if second else (first,))
        if variant_set in seen_sets:
            raise ConformanceError(f"row {row_number}: duplicate variant hypothesis")
        seen_sets.add(variant_set)
        variants.extend(
            SubmittedVariant(row_number, suffix, variant)
            for suffix, variant in (("1", first), ("2", second))
            if variant
        )
        try:
            epcr = float(row["epcr"])
        except ValueError as error:
            raise ConformanceError(f"row {row_number}: EPCR is not numeric") from error
        if not math.isfinite(epcr) or not 0 < epcr <= 1:
            raise ConformanceError(f"row {row_number}: EPCR must be finite and in (0,1]")
        epcrs.append(epcr)
        finding_type = row["finding_type"]
        if finding_type not in {"primary", "secondary"}:
            raise ConformanceError(
                f"row {row_number}: finding_type must be exactly primary or secondary"
            )
    if len(set(epcrs)) != len(epcrs):
        raise ConformanceError("EPCR values must be strictly distinct")
    if epcrs != sorted(epcrs, reverse=True):
        raise ConformanceError("rows must already be ordered by descending EPCR")
    return variants


def validate_reference_normalization(
    variants: list[SubmittedVariant], reference: Path, bcftools: Path
) -> None:
    if not reference.is_file():
        raise ConformanceError(f"reference FASTA not found: {reference}")
    if not bcftools.is_file():
        raise ConformanceError(f"bcftools not found: {bcftools}")
    expected: dict[str, tuple[Variant, int, str]] = {}
    with tempfile.TemporaryDirectory(prefix="track1-normalize-") as temp_name:
        temp = Path(temp_name)
        source = temp / "submitted.vcf"
        fai = Path(f"{reference}.fai")
        if not fai.is_file():
            raise ConformanceError(f"reference FASTA index not found: {fai}")
        contig_lengths = {
            fields[0]: int(fields[1])
            for line in fai.read_text().splitlines()
            if len(fields := line.split("\t")) >= 2
        }
        local_contigs = sorted(
            {item.variant.chrom.removeprefix("chr") for item in variants}
        )
        missing_contigs = set(local_contigs) - set(contig_lengths)
        if missing_contigs:
            raise ConformanceError(
                "submission contigs absent from reference: " + ", ".join(sorted(missing_contigs))
            )
        lines = ["##fileformat=VCFv4.2"]
        lines.extend(
            f"##contig=<ID={contig},length={contig_lengths[contig]}>"
            for contig in local_contigs
        )
        lines.append("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO")
        for index, item in enumerate(variants, 1):
            chrom, pos, ref, alt = item.variant
            local_chrom = chrom.removeprefix("chr")
            identifier = f"v{index}"
            expected[identifier] = (
                Variant(local_chrom, pos, ref, alt),
                item.csv_row,
                item.allele_number,
            )
            lines.append(f"{local_chrom}\t{pos}\t{identifier}\t{ref}\t{alt}\t.\tPASS\t.")
        source.write_text("\n".join(lines) + "\n")
        command = [
            str(bcftools),
            "norm",
            "--check-ref",
            "e",
            "--fasta-ref",
            str(reference),
            "--output-type",
            "v",
            str(source),
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        if completed.returncode:
            detail = completed.stderr.strip() or "unknown error"
            raise ConformanceError(f"reference/normalization check failed: {detail}")
        observed: dict[str, Variant] = {}
        for line in completed.stdout.splitlines():
            if line.startswith("#"):
                continue
            chrom, pos, identifier, ref, alt, *_rest = line.split("\t")
            observed[identifier] = Variant(chrom, int(pos), ref, alt)
    if set(observed) != set(expected):
        raise ConformanceError("normalization changed the number or identity of submitted alleles")
    for identifier, expected_entry in expected.items():
        expected_variant, row_number, suffix = expected_entry
        if observed[identifier] != expected_variant:
            normalized_variant = observed[identifier]
            rendered = (
                f"chr{normalized_variant[0]}:{normalized_variant[1]}:"
                f"{normalized_variant[2]}>{normalized_variant[3]}"
            )
            raise ConformanceError(
                f"row {row_number} allele {suffix} is not minimal and left-aligned; use {rendered}"
            )


def official_hypothetical_score(path: Path, assumed_truth_rank: int):
    official = load_official_scorer()
    submissions = official.load_submission(str(path))
    if set(submissions) != {PROBAND_ID}:
        raise ConformanceError("official scorer did not load exactly PROBAND01")
    rows = submissions[PROBAND_ID]
    if not 1 <= assumed_truth_rank <= len(rows):
        raise ConformanceError(
            f"assumed truth rank must be between 1 and {len(rows)}"
        )
    assumed_truth = rows[assumed_truth_rank - 1].variants
    return official.score_proband(PROBAND_ID, rows, assumed_truth)


def check_submission(
    path: Path,
    reference: Path,
    bcftools: Path,
    require_ten: bool,
    assumed_truth_rank: int,
) -> dict[str, object]:
    rows = read_submission(path)
    variants = validate_rows(rows, require_ten=require_ten)
    validate_reference_normalization(variants, reference, bcftools)
    score = official_hypothetical_score(path, assumed_truth_rank)
    return {
        "conformant": True,
        "official_scorer_revision": OFFICIAL_REVISION,
        "submission": str(path.resolve()),
        "submission_sha256": sha256(path),
        "official_scorer_sha256": sha256(OFFICIAL_SCORER),
        "row_count": len(rows),
        "distinct_epcr_count": len({row["epcr"] for row in rows}),
        "reference_normalized_alleles": len(variants),
        "hypothetical_truth_rank": assumed_truth_rank,
        "hypothetical_official_score": asdict(score),
        "score_limitation": (
            "The private answer key was not used. This score assumes the selected submitted "
            "row is causal and is a scorer/conformance test, not biological validation."
        ),
    }


def build_submission(candidates_path: Path, output_path: Path) -> int:
    with candidates_path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required = {
            f"{field}_{suffix}"
            for field in ("chrom", "pos", "ref", "alt")
            for suffix in ("1", "2")
        }
        required.update({"model", "gene"})
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ConformanceError("candidate table lacks required compound-pair columns")
        selected: list[dict[str, str]] = []
        seen: set[frozenset] = set()
        for candidate in reader:
            if candidate["model"] != "compound_heterozygous":
                continue
            alleles: list[Variant] = []
            for suffix in ("1", "2"):
                raw = tuple(
                    candidate[f"{field}_{suffix}"].strip()
                    for field in ("chrom", "pos", "ref", "alt")
                )
                if not all(raw):
                    break
                chrom, pos, ref, alt = raw
                try:
                    alleles.append(Variant(chrom, int(pos), ref, alt))
                except ValueError as error:
                    raise ConformanceError(
                        f"candidate table has a non-integer position: {pos!r}"
                    ) from error
            if len(alleles) != 2:
                continue
            key = frozenset(alleles)
            if len(key) != 2 or key in seen:
                continue
            seen.add(key)
            selected.append(candidate)
            if len(selected) == 10:
                break
    if len(selected) != 10:
        raise ConformanceError(f"need 10 distinct compound-pair hypotheses; found {len(selected)}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCHEMA)
        writer.writeheader()
        for candidate, epcr in zip(selected, BUILD_EPCR, strict=True):
            row = {
                "proband_id": PROBAND_ID,
                "epcr": f"{epcr:.2f}",
                "finding_type": "primary",
                "notes": (
                    f"{candidate['gene']} unphased compound-heterozygous hypothesis; "
                    "trans phase unconfirmed"
                ),
            }
            for suffix in ("1", "2"):
                for field in ("chrom", "pos", "ref", "alt"):
                    row[f"{field}_{suffix}"] = candidate[f"{field}_{suffix}"].strip()
            writer.writerow(row)
    return len(selected)


def write_fixture(path: Path, rows: int = 10) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCHEMA)
        writer.writeheader()
        for index in range(rows):
            writer.writerow(
                {
                    "proband_id": PROBAND_ID,
                    "chrom_1": "chr1",
                    "pos_1": str(index + 1),
                    "ref_1": "A",
                    "alt_1": "C",
                    "chrom_2": "chr1",
                    "pos_2": str(index + 21),
                    "ref_2": "A",
                    "alt_2": "G",
                    "epcr": f"{1 - index / 20:.2f}",
                    "finding_type": "primary",
                    "notes": "synthetic self-check",
                }
            )


def self_check() -> None:
    assert sha256(OFFICIAL_SCORER) == OFFICIAL_SCORER_SHA256
    assert sha256(OFFICIAL_TEMPLATE) == TRACKED_TEMPLATE_SHA256
    with tempfile.TemporaryDirectory(prefix="track1-self-check-") as temp_name:
        temp = Path(temp_name)
        reference = temp / "reference.fa"
        reference.write_text(">1\n" + "A" * 80 + "\n")
        subprocess.run([str(DEFAULT_SAMTOOLS), "faidx", str(reference)], check=True)
        valid = temp / "valid.csv"
        write_fixture(valid)
        report = check_submission(valid, reference, DEFAULT_BCFTOOLS, True, 1)
        assert report["row_count"] == 10
        assert report["hypothetical_official_score"]["rank_points"] == 100.0
        assert report["hypothetical_official_score"]["f_max"] == 1.0
        rank_two = official_hypothetical_score(valid, 2)
        assert rank_two.full_match_rank == 2
        assert rank_two.rank_points == 50.0
        assert math.isclose(rank_two.f_max, 2 / 3)
        official = load_official_scorer()
        official_rows = official.load_submission(str(valid))[PROBAND_ID]
        recovered = next(iter(official_rows[0].variants))
        partial_truth = frozenset((recovered, ("chr1", 80, "A", "T")))
        partial = official.score_proband(PROBAND_ID, official_rows, partial_truth)
        assert partial.full_match_rank is None
        assert partial.partial_match_rank == 1
        assert partial.rank_points == 50.0

        def must_fail(mutator, message: str) -> None:
            rows = read_submission(valid)
            mutator(rows)
            invalid = temp / f"invalid-{message}.csv"
            with invalid.open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=SCHEMA)
                writer.writeheader()
                writer.writerows(rows)
            try:
                checked = read_submission(invalid)
                variants = validate_rows(checked, require_ten=True)
                validate_reference_normalization(variants, reference, DEFAULT_BCFTOOLS)
            except ConformanceError:
                return
            raise AssertionError(f"self-check accepted {message}")

        must_fail(lambda rows: rows[0].update(proband_id="WGS_EX2312012"), "wrong-pid")
        must_fail(lambda rows: rows[0].update(chrom_1="1"), "unprefixed-contig")
        must_fail(lambda rows: rows[1].update(epcr=rows[0]["epcr"]), "duplicate-epcr")
        must_fail(lambda rows: rows[0].update(pos_2=""), "partial-second-allele")
        must_fail(lambda rows: rows.append(dict(rows[-1])), "eleven-rows")
        must_fail(
            lambda rows: rows[0].update(pos_1="2", ref_1="AA", alt_1="A"),
            "non-left-aligned-indel",
        )

        candidates = temp / "candidates.tsv"
        fields = ["model", "gene"] + [
            f"{field}_{suffix}"
            for suffix in ("1", "2")
            for field in ("chrom", "pos", "ref", "alt")
        ]
        with candidates.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
            writer.writeheader()
            for index in range(10):
                writer.writerow(
                    {
                        "model": "compound_heterozygous",
                        "gene": f"GENE{index}",
                        "chrom_1": "chr1",
                        "pos_1": index + 1,
                        "ref_1": "A",
                        "alt_1": "C",
                        "chrom_2": "chr1",
                        "pos_2": index + 21,
                        "ref_2": "A",
                        "alt_2": "G",
                    }
                )
        built = temp / "built.csv"
        assert build_submission(candidates, built) == 10
        assert len(read_submission(built)) == 10
    print("self-check ok: build, strict conformance, normalization and official scoring")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check", action="store_true")
    subparsers = parser.add_subparsers(dest="command")
    build = subparsers.add_parser("build", help="build a ten-row draft from feat-004 pairs")
    build.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    build.add_argument("--output", type=Path, default=DEFAULT_SUBMISSION)
    check = subparsers.add_parser("check", help="check and hypothetically self-score a CSV")
    check.add_argument("submission", type=Path, nargs="?", default=DEFAULT_SUBMISSION)
    check.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    check.add_argument("--bcftools", type=Path, default=DEFAULT_BCFTOOLS)
    check.add_argument("--allow-fewer-than-10", action="store_true")
    check.add_argument("--assume-truth-rank", type=int, default=1)
    check.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.self_check:
        self_check()
        return
    if args.command == "build":
        count = build_submission(args.candidates, args.output)
        print(f"wrote {args.output} with {count} compound-pair hypotheses")
        return
    if args.command == "check":
        report = check_submission(
            args.submission,
            args.reference,
            args.bcftools,
            not args.allow_fewer_than_10,
            args.assume_truth_rank,
        )
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True))
        return
    raise SystemExit("choose build or check, or pass --self-check")


if __name__ == "__main__":
    main()
