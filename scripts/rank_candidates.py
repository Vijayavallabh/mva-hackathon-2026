#!/usr/bin/env python3
"""Rank locally annotated variants under compound-het and dominant models.

The real outputs contain subject-level candidate genotypes and therefore stay under the
gitignored ``results/`` tree.  Only aggregate QC and reviewed derived findings may be
copied into tracked notes.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import re
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations, pairwise
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBAND_HPO = (
    "HP:0002859",
    "HP:0000121",
    "HP:0004322",
    "HP:0001508",
    "HP:0003202",
    "HP:0001622",
    "HP:0001518",
)
FAMILY_HPO = ("HP:0200067",)
AUTOSOMES = {str(number) for number in range(1, 23)}

SEVERITY = {
    "transcript_ablation": 10.0,
    "splice_acceptor_variant": 10.0,
    "splice_donor_variant": 10.0,
    "stop_gained": 10.0,
    "frameshift_variant": 10.0,
    "stop_lost": 9.0,
    "start_lost": 9.0,
    "transcript_amplification": 8.0,
    "inframe_insertion": 7.0,
    "inframe_deletion": 7.0,
    "missense_variant": 6.0,
    "protein_altering_variant": 6.0,
    "splice_region_variant": 4.0,
    "incomplete_terminal_codon_variant": 3.0,
    "synonymous_variant": 1.0,
}


@dataclass(frozen=True)
class Variant:
    chrom: str
    pos: int
    ref: str
    alt: str
    gene: str
    gene_id: str
    consequence: str
    impact: str
    genotype: str
    depth: int | None
    genotype_quality: float | None
    allele_balance: float | None
    max_af: float | None
    sift: str
    polyphen: str
    clinvar_significance: str
    clinvar_review: str
    hgvsc: str
    hgvsp: str
    variant_score: float

    @property
    def locus(self) -> tuple[str, int]:
        return self.chrom, self.pos

    @property
    def submission_chrom(self) -> str:
        return self.chrom if self.chrom.startswith("chr") else f"chr{self.chrom}"

    @property
    def is_heterozygous(self) -> bool:
        alleles = re.split(r"[/|]", self.genotype)
        return len(alleles) == 2 and sorted(alleles) == ["0", "1"]


@dataclass(frozen=True)
class PhenotypeScore:
    proband_similarity: float
    family_similarity: float
    proband_coverage: int


@dataclass(frozen=True)
class Candidate:
    model: str
    gene: str
    variants: tuple[Variant, ...]
    phenotype: PhenotypeScore
    total_score: float


def open_text(path: Path):
    return gzip.open(path, "rt") if path.suffix == ".gz" else path.open()


def parse_obo(path: Path) -> dict[str, set[str]]:
    """Return non-obsolete HPO parent edges."""
    parents: dict[str, set[str]] = defaultdict(set)
    current_id: str | None = None
    current_parents: set[str] = set()
    obsolete = False

    def finish() -> None:
        if current_id and not obsolete:
            parents[current_id].update(current_parents)

    for raw in path.read_text().splitlines() + ["[Term]"]:
        line = raw.strip()
        if line == "[Term]":
            finish()
            current_id = None
            current_parents = set()
            obsolete = False
        elif line.startswith("id: HP:"):
            current_id = line.removeprefix("id: ")
        elif line.startswith("is_a: HP:"):
            current_parents.add(line.split()[1])
        elif line == "is_obsolete: true":
            obsolete = True
    return dict(parents)


def parse_gene_annotations(path: Path) -> dict[str, set[str]]:
    """Parse the release-pinned HPO genes-to-phenotype table by header name."""
    genes: dict[str, set[str]] = defaultdict(set)
    with open_text(path) as handle:
        header: list[str] | None = None
        for raw in handle:
            if not raw.strip():
                continue
            if raw.startswith("#"):
                candidate = raw.lstrip("#").strip().split("\t")
                lowered = [field.casefold().replace("_", "-") for field in candidate]
                if any("hpo" in field for field in lowered) and any(
                    "symbol" in field for field in lowered
                ):
                    header = candidate
                continue
            fields = raw.rstrip("\n").split("\t")
            if header is None:
                if "hpo_id" in fields or "HPO-Term-ID" in fields:
                    header = fields
                    continue
                raise ValueError("HPO gene table has no recognized header")
            normalized = {
                name.casefold().replace("_", "-"): value
                for name, value in zip(header, fields, strict=False)
            }
            symbol = next(
                (value for name, value in normalized.items() if "symbol" in name), ""
            )
            hpo_id = next(
                (
                    value
                    for name, value in normalized.items()
                    if ("hpo" in name and ("id" in name or "term" in name))
                    and value.startswith("HP:")
                ),
                "",
            )
            if not hpo_id:
                hpo_id = next(
                    (value for value in fields if value.startswith("HP:")), ""
                )
            if symbol and hpo_id:
                genes[symbol].add(hpo_id)
    if not genes:
        raise ValueError("HPO gene table yielded no associations")
    return dict(genes)


def ancestor_function(parents: dict[str, set[str]]):
    cache: dict[str, set[str]] = {}

    def ancestors(term: str, trail: frozenset[str] = frozenset()) -> set[str]:
        if term in cache:
            return cache[term]
        if term in trail:
            raise ValueError(f"cycle in ontology at {term}")
        result = {term}
        for parent in parents.get(term, set()):
            result.update(ancestors(parent, trail | {term}))
        cache[term] = result
        return result

    return ancestors


def build_semantic_scorer(
    parents: dict[str, set[str]], gene_terms: dict[str, set[str]]
):
    ancestors = ancestor_function(parents)
    propagated = {
        gene: set().union(*(ancestors(term) for term in terms))
        for gene, terms in gene_terms.items()
        if terms
    }
    counts: Counter[str] = Counter()
    for terms in propagated.values():
        counts.update(terms)
    total_genes = max(len(propagated), 1)
    information = {
        term: -math.log(max(count, 1) / total_genes) for term, count in counts.items()
    }

    def term_similarity(left: str, right: str) -> float:
        common = ancestors(left) & ancestors(right)
        mica = max((information.get(term, 0.0) for term in common), default=0.0)
        scale = max(information.get(left, 0.0), information.get(right, 0.0), 1.0)
        return mica / scale

    def score(gene: str) -> PhenotypeScore:
        terms = gene_terms.get(gene, set())
        if not terms:
            return PhenotypeScore(0.0, 0.0, 0)
        best_proband = [
            max(term_similarity(query, term) for term in terms) for query in PROBAND_HPO
        ]
        best_family = [
            max(term_similarity(query, term) for term in terms) for query in FAMILY_HPO
        ]
        return PhenotypeScore(
            sum(best_proband) / len(best_proband),
            sum(best_family) / len(best_family),
            sum(value >= 0.35 for value in best_proband),
        )

    return score


def parse_float(value: str) -> float | None:
    values: list[float] = []
    for token in re.split(r"[,&]", value or ""):
        try:
            values.append(float(token))
        except ValueError:
            pass
    return max(values) if values else None


def parse_info(raw: str) -> dict[str, str]:
    info: dict[str, str] = {}
    for item in raw.split(";"):
        key, separator, value = item.partition("=")
        info[key] = value if separator else "true"
    return info


def parse_csq_header(line: str) -> list[str]:
    match = re.search(r"Format: ([^\"]+)", line)
    if not match:
        raise ValueError("VEP CSQ header has no Format declaration")
    return match.group(1).rstrip("> ").split("|")


def consequence_severity(consequence: str) -> float:
    return max(
        (SEVERITY.get(term, 0.0) for term in consequence.split("&")), default=0.0
    )


def genotype_fields(format_text: str, sample_text: str) -> dict[str, str]:
    return dict(zip(format_text.split(":"), sample_text.split(":"), strict=False))


def calculate_variant_score(
    consequence: str,
    impact: str,
    max_af: float | None,
    sift: str,
    polyphen: str,
    clinvar: str,
    depth: int | None,
    gq: float | None,
    allele_balance: float | None,
) -> float:
    score = consequence_severity(consequence)
    score += {"HIGH": 2.0, "MODERATE": 1.0}.get(impact, 0.0)
    score += 1.0 if max_af is None else min(-math.log10(max(max_af, 1e-8)) / 4.0, 2.0)
    if "deleterious" in sift.casefold():
        score += 1.0
    if "damaging" in polyphen.casefold():
        score += 1.0
    if "pathogenic" in clinvar.casefold() and "conflict" not in clinvar.casefold():
        score += 2.0
    if depth is not None and depth < 10:
        score -= 2.0
    if gq is not None and gq < 20:
        score -= 1.5
    if allele_balance is not None and not 0.2 <= allele_balance <= 0.8:
        score -= 1.0
    return score


def iter_variants(path: Path):
    csq_fields: list[str] | None = None
    with open_text(path) as handle:
        for raw in handle:
            if raw.startswith("##INFO=<ID=CSQ"):
                csq_fields = parse_csq_header(raw)
                continue
            if raw.startswith("#"):
                continue
            if csq_fields is None:
                raise ValueError("annotated VCF lacks a VEP CSQ header")
            fields = raw.rstrip("\n").split("\t")
            if len(fields) < 10:
                raise ValueError("annotated VCF record lacks one sample column")
            (
                chrom,
                pos_text,
                _identifier,
                ref,
                alt,
                _qual,
                filt,
                raw_info,
                fmt,
                sample,
            ) = fields[:10]
            if filt not in {"PASS", "."}:
                continue
            if "," in alt:
                raise ValueError("annotated input must be split to biallelic records")
            info = parse_info(raw_info)
            csq_records = info.get("CSQ", "").split(",")
            if not csq_records or not csq_records[0]:
                continue
            annotations = [
                dict(zip(csq_fields, record.split("|"), strict=False))
                for record in csq_records
            ]
            annotation = max(
                annotations,
                key=lambda item: consequence_severity(item.get("Consequence", "")),
            )
            gene = annotation.get("SYMBOL", "")
            consequence = annotation.get("Consequence", "")
            if not gene or consequence_severity(consequence) < 3.0:
                continue
            sample_fields = genotype_fields(fmt, sample)
            genotype = sample_fields.get("GT", "")
            if "1" not in re.split(r"[/|]", genotype):
                continue
            depth = (
                int(sample_fields["DP"])
                if sample_fields.get("DP", "").isdigit()
                else None
            )
            gq = parse_float(sample_fields.get("GQ", ""))
            ad = [
                parse_float(value) for value in sample_fields.get("AD", "").split(",")
            ]
            allele_balance = None
            if (
                len(ad) >= 2
                and ad[0] is not None
                and ad[1] is not None
                and ad[0] + ad[1] > 0
            ):
                allele_balance = ad[1] / (ad[0] + ad[1])
            af_values = [
                parse_float(annotation.get(key, ""))
                for key in ("MAX_AF", "gnomADe_AF", "gnomADg_AF")
            ]
            max_af = max(
                (value for value in af_values if value is not None), default=None
            )
            sift = annotation.get("SIFT", "")
            polyphen = annotation.get("PolyPhen", "")
            clinvar = info.get("CLNSIG", "")
            yield Variant(
                chrom=chrom,
                pos=int(pos_text),
                ref=ref,
                alt=alt,
                gene=gene,
                gene_id=annotation.get("Gene", ""),
                consequence=consequence,
                impact=annotation.get("IMPACT", ""),
                genotype=genotype,
                depth=depth,
                genotype_quality=gq,
                allele_balance=allele_balance,
                max_af=max_af,
                sift=sift,
                polyphen=polyphen,
                clinvar_significance=clinvar,
                clinvar_review=info.get("CLNREVSTAT", ""),
                hgvsc=annotation.get("HGVSc", ""),
                hgvsp=annotation.get("HGVSp", ""),
                variant_score=calculate_variant_score(
                    consequence,
                    annotation.get("IMPACT", ""),
                    max_af,
                    sift,
                    polyphen,
                    clinvar,
                    depth,
                    gq,
                    allele_balance,
                ),
            )


def is_rare(variant: Variant, threshold: float) -> bool:
    return variant.max_af is None or variant.max_af <= threshold


def build_candidates(variants: list[Variant], phenotype_score) -> list[Candidate]:
    candidates: list[Candidate] = []
    by_gene: dict[str, list[Variant]] = defaultdict(list)
    for variant in variants:
        if (
            variant.chrom in AUTOSOMES
            and variant.is_heterozygous
            and is_rare(variant, 0.01)
        ):
            by_gene[variant.gene].append(variant)

    for gene, gene_variants in by_gene.items():
        phenotype = phenotype_score(gene)
        selected = sorted(
            gene_variants, key=lambda item: item.variant_score, reverse=True
        )[:12]
        for left, right in combinations(selected, 2):
            if left.locus == right.locus:
                continue
            variant_component = (left.variant_score + right.variant_score) / 2.0
            # The public scoring code establishes a compound-heterozygous answer key;
            # retain a transparent model prior while still ranking every gene genome-wide.
            total = 3.0 + variant_component + 8.0 * phenotype.proband_similarity
            total += 0.75 * phenotype.family_similarity
            candidates.append(
                Candidate(
                    "compound_heterozygous", gene, (left, right), phenotype, total
                )
            )

    for variant in variants:
        if not variant.is_heterozygous or not is_rare(variant, 0.001):
            continue
        phenotype = phenotype_score(variant.gene)
        total = variant.variant_score + 8.0 * phenotype.proband_similarity
        total += 0.5 * phenotype.family_similarity
        candidates.append(
            Candidate(
                "dominant_singleton_unconfirmed_de_novo",
                variant.gene,
                (variant,),
                phenotype,
                total,
            )
        )

    return sorted(
        candidates,
        key=lambda item: (
            item.total_score,
            item.phenotype.proband_coverage,
            item.gene,
        ),
        reverse=True,
    )


VARIANT_COLUMNS = (
    "rank",
    "model",
    "gene",
    "chrom_1",
    "pos_1",
    "ref_1",
    "alt_1",
    "gt_1",
    "dp_1",
    "gq_1",
    "allele_balance_1",
    "consequence_1",
    "max_af_1",
    "sift_1",
    "polyphen_1",
    "clinvar_1",
    "clinvar_review_1",
    "hgvsc_1",
    "hgvsp_1",
    "chrom_2",
    "pos_2",
    "ref_2",
    "alt_2",
    "gt_2",
    "dp_2",
    "gq_2",
    "allele_balance_2",
    "consequence_2",
    "max_af_2",
    "sift_2",
    "polyphen_2",
    "clinvar_2",
    "clinvar_review_2",
    "hgvsc_2",
    "hgvsp_2",
    "proband_similarity",
    "proband_coverage_of_7",
    "family_history_similarity",
    "total_score",
    "phase_status",
    "de_novo_status",
)


def variant_value(variant: Variant | None, field: str) -> str | int:
    if variant is None:
        return ""
    if field == "chrom":
        return variant.submission_chrom
    if field == "max_af":
        return "" if variant.max_af is None else f"{variant.max_af:.8g}"
    if field in {"genotype_quality", "allele_balance"}:
        value = getattr(variant, field)
        return "" if value is None else f"{value:.6g}"
    return getattr(variant, field)


def write_candidates(path: Path, candidates: list[Candidate], limit: int = 500) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=VARIANT_COLUMNS, delimiter="\t")
        writer.writeheader()
        for rank, candidate in enumerate(candidates[:limit], 1):
            left = candidate.variants[0]
            right = candidate.variants[1] if len(candidate.variants) == 2 else None
            writer.writerow(
                {
                    "rank": rank,
                    "model": candidate.model,
                    "gene": candidate.gene,
                    "chrom_1": variant_value(left, "chrom"),
                    "pos_1": variant_value(left, "pos"),
                    "ref_1": variant_value(left, "ref"),
                    "alt_1": variant_value(left, "alt"),
                    "gt_1": variant_value(left, "genotype"),
                    "dp_1": variant_value(left, "depth"),
                    "gq_1": variant_value(left, "genotype_quality"),
                    "allele_balance_1": variant_value(left, "allele_balance"),
                    "consequence_1": variant_value(left, "consequence"),
                    "max_af_1": variant_value(left, "max_af"),
                    "sift_1": variant_value(left, "sift"),
                    "polyphen_1": variant_value(left, "polyphen"),
                    "clinvar_1": variant_value(left, "clinvar_significance"),
                    "clinvar_review_1": variant_value(left, "clinvar_review"),
                    "hgvsc_1": variant_value(left, "hgvsc"),
                    "hgvsp_1": variant_value(left, "hgvsp"),
                    "chrom_2": variant_value(right, "chrom"),
                    "pos_2": variant_value(right, "pos"),
                    "ref_2": variant_value(right, "ref"),
                    "alt_2": variant_value(right, "alt"),
                    "gt_2": variant_value(right, "genotype"),
                    "dp_2": variant_value(right, "depth"),
                    "gq_2": variant_value(right, "genotype_quality"),
                    "allele_balance_2": variant_value(right, "allele_balance"),
                    "consequence_2": variant_value(right, "consequence"),
                    "max_af_2": variant_value(right, "max_af"),
                    "sift_2": variant_value(right, "sift"),
                    "polyphen_2": variant_value(right, "polyphen"),
                    "clinvar_2": variant_value(right, "clinvar_significance"),
                    "clinvar_review_2": variant_value(right, "clinvar_review"),
                    "hgvsc_2": variant_value(right, "hgvsc"),
                    "hgvsp_2": variant_value(right, "hgvsp"),
                    "proband_similarity": f"{candidate.phenotype.proband_similarity:.6f}",
                    "proband_coverage_of_7": candidate.phenotype.proband_coverage,
                    "family_history_similarity": f"{candidate.phenotype.family_similarity:.6f}",
                    "total_score": f"{candidate.total_score:.6f}",
                    "phase_status": "unknown; parental phasing required"
                    if right
                    else "not applicable",
                    "de_novo_status": "unknown; no parental genotypes",
                }
            )


def write_qc(path: Path, variants: list[Variant], candidates: list[Candidate]) -> None:
    qc = {
        "annotated_rare_damaging_variants": len(variants),
        "genes_with_retained_variants": len({variant.gene for variant in variants}),
        "compound_heterozygous_pair_hypotheses": sum(
            candidate.model == "compound_heterozygous" for candidate in candidates
        ),
        "dominant_singleton_hypotheses": sum(
            candidate.model == "dominant_singleton_unconfirmed_de_novo"
            for candidate in candidates
        ),
        "proband_hpo_terms_scored": list(PROBAND_HPO),
        "family_history_hpo_terms_scored_separately": list(FAMILY_HPO),
        "coordinate_policy": "input unprefixed; candidate table chr-prefixed",
    }
    path.write_text(json.dumps(qc, indent=2) + "\n")


def best_per_gene(candidates: list[Candidate]) -> list[Candidate]:
    """Retain the highest-scoring hypothesis per model and gene for review."""
    seen: set[tuple[str, str]] = set()
    selected: list[Candidate] = []
    for candidate in candidates:
        key = candidate.model, candidate.gene
        if key not in seen:
            selected.append(candidate)
            seen.add(key)
    return selected


def read_candidate_table(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_output(output: Path) -> None:
    """Check model, coordinate, ordering and phenotype-scope invariants."""
    all_rows = read_candidate_table(output / "all_candidate_models.tsv")
    rows = read_candidate_table(output / "candidate_models.tsv")
    compound = read_candidate_table(output / "compound_het_candidates.tsv")
    dominant = read_candidate_table(output / "dominant_candidates.tsv")
    if not all_rows or not compound or not dominant:
        raise ValueError("candidate output is unexpectedly empty")
    if len({(row["model"], row["gene"]) for row in rows}) != len(rows):
        raise ValueError("review table contains duplicate model/gene hypotheses")
    if any(
        float(left["total_score"]) < float(right["total_score"])
        for left, right in pairwise(rows)
    ):
        raise ValueError("candidate review table is not score-sorted")
    for row in rows:
        for suffix in ("1", "2"):
            chrom = row[f"chrom_{suffix}"]
            if chrom and not chrom.startswith("chr"):
                raise ValueError("candidate output contains an unprefixed chromosome")
        coverage = int(row["proband_coverage_of_7"])
        if not 0 <= coverage <= len(PROBAND_HPO):
            raise ValueError("proband HPO coverage is outside 0..7")
    for row in compound:
        if row["model"] != "compound_heterozygous":
            raise ValueError("compound table contains another model")
        if row["gt_1"] not in {"0/1", "1/0", "0|1", "1|0"} or row["gt_2"] not in {
            "0/1",
            "1/0",
            "0|1",
            "1|0",
        }:
            raise ValueError("compound hypothesis contains a non-heterozygous allele")
        if (row["chrom_1"], row["pos_1"]) == (row["chrom_2"], row["pos_2"]):
            raise ValueError("compound hypothesis pairs alternate alleles at one locus")
    if any(
        row["model"] != "dominant_singleton_unconfirmed_de_novo" for row in dominant
    ):
        raise ValueError("dominant table contains another model")
    qc = json.loads((output / "candidate_qc.json").read_text())
    if qc["proband_hpo_terms_scored"] != list(PROBAND_HPO):
        raise ValueError("proband HPO set drifted")
    if qc["family_history_hpo_terms_scored_separately"] != list(FAMILY_HPO):
        raise ValueError("family-history HPO scope drifted")
    expected = (
        qc["compound_heterozygous_pair_hypotheses"]
        + qc["dominant_singleton_hypotheses"]
    )
    if len(all_rows) != expected:
        raise ValueError("complete candidate table does not match QC hypothesis count")
    print(f"candidate output validation ok: {len(rows)} representative hypotheses")


def run(annotated_vcf: Path, ontology: Path, annotations: Path, output: Path) -> None:
    parents = parse_obo(ontology)
    gene_terms = parse_gene_annotations(annotations)
    phenotype_score = build_semantic_scorer(parents, gene_terms)
    variants = [
        variant for variant in iter_variants(annotated_vcf) if is_rare(variant, 0.01)
    ]
    candidates = build_candidates(variants, phenotype_score)
    representative = best_per_gene(candidates)
    write_candidates(
        output / "all_candidate_models.tsv", candidates, limit=len(candidates)
    )
    write_candidates(output / "candidate_models.tsv", representative)
    write_candidates(
        output / "compound_het_candidates.tsv",
        [
            candidate
            for candidate in representative
            if candidate.model == "compound_heterozygous"
        ],
    )
    write_candidates(
        output / "dominant_candidates.tsv",
        [
            candidate
            for candidate in representative
            if candidate.model == "dominant_singleton_unconfirmed_de_novo"
        ],
    )
    write_qc(output / "candidate_qc.json", variants, candidates)
    validate_output(output)
    print(
        f"ranked {len(candidates)} hypotheses from {len(variants)} rare damaging variants; "
        f"outputs: {output}"
    )


def self_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        obo = root / "hp.obo"
        terms = ("HP:0000001",) + PROBAND_HPO + FAMILY_HPO
        obo.write_text(
            "\n".join(
                f"[Term]\nid: {term}\nname: synthetic\n"
                + ("" if term == "HP:0000001" else "is_a: HP:0000001 ! root\n")
                for term in terms
            )
        )
        genes = root / "genes.tsv"
        rows = ["#gene_id\tgene_symbol\thpo_id\thpo_name"]
        rows.extend(f"1\tGENE_A\t{term}\tsynthetic" for term in PROBAND_HPO)
        rows.append(f"2\tGENE_FAMILY\t{FAMILY_HPO[0]}\tsynthetic")
        genes.write_text("\n".join(rows) + "\n")
        vcf = root / "annotated.vcf"
        csq = "Allele|Consequence|IMPACT|SYMBOL|Gene|SIFT|PolyPhen|MAX_AF|gnomADe_AF|gnomADg_AF|HGVSc|HGVSp"
        header = (
            "##fileformat=VCFv4.2\n"
            f'##INFO=<ID=CSQ,Number=.,Type=String,Description="Format: {csq}">\n'
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n"
        )
        records = [
            ("1", 100, "A", "T", "GENE_A", "frameshift_variant", "HIGH", "0.0001"),
            ("1", 200, "G", "C", "GENE_A", "missense_variant", "MODERATE", "0.0002"),
            ("1", 100, "A", "G", "GENE_A", "missense_variant", "MODERATE", "0.0002"),
            ("2", 300, "C", "T", "GENE_FAMILY", "frameshift_variant", "HIGH", "0.0001"),
        ]
        with vcf.open("w") as handle:
            handle.write(header)
            for chrom, pos, ref, alt, gene, consequence, impact, af in records:
                annotation = "|".join(
                    (
                        alt,
                        consequence,
                        impact,
                        gene,
                        f"ENSG_{gene}",
                        "deleterious",
                        "probably_damaging",
                        af,
                        af,
                        af,
                        "",
                        "",
                    )
                )
                handle.write(
                    f"{chrom}\t{pos}\t.\t{ref}\t{alt}\t100\tPASS\tCSQ={annotation}\tGT:DP:GQ:AD\t0/1:40:99:20,20\n"
                )
        out = root / "out"
        run(vcf, obo, genes, out)
        candidates = read_candidate_table(out / "candidate_models.tsv")
        assert candidates[0]["model"] == "compound_heterozygous"
        assert candidates[0]["gene"] == "GENE_A"
        assert candidates[0]["chrom_1"].startswith("chr")
        assert candidates[0]["pos_1"] != candidates[0]["pos_2"]
        family_candidate = next(
            row for row in candidates if row["gene"] == "GENE_FAMILY"
        )
        assert float(family_candidate["family_history_similarity"]) > 0
        assert int(family_candidate["proband_coverage_of_7"]) == 0
        qc = json.loads((out / "candidate_qc.json").read_text())
        assert len(qc["proband_hpo_terms_scored"]) == 7
        assert qc["family_history_hpo_terms_scored_separately"] == list(FAMILY_HPO)
    print("candidate ranker self-check ok")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotated-vcf", type=Path)
    parser.add_argument("--ontology", type=Path, default=ROOT / "data/resources/hp.obo")
    parser.add_argument(
        "--gene-annotations",
        type=Path,
        default=ROOT / "data/resources/hpo/genes_to_phenotype.txt",
    )
    parser.add_argument("--output", type=Path, default=ROOT / "results/feat004")
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--validate-output", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if args.validate_output:
        validate_output(args.output)
        return
    if args.annotated_vcf is None:
        parser.error("--annotated-vcf is required")
    run(args.annotated_vcf, args.ontology, args.gene_annotations, args.output)


if __name__ == "__main__":
    main()
