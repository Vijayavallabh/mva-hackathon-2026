#!/usr/bin/env python3
"""Audit public-study exposure units without inferring clinical doses or margins.

Converting ng/mL to nM changes units only: it does not change analyte, matrix,
binding, population, time course, or a surrogate into a functional endpoint.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "notes/track2-exposure.json"
MATRICES = {"whole_blood", "plasma", "reported_plasma_unresolved", "culture_medium"}
BASES = {"total", "nominal", "unresolved", "unbound"}
KINDS = {"concentration", "auc"}


def positive(value) -> bool:
    return type(value) in (int, float) and math.isfinite(value) and value > 0


def convert(value: float, unit: str, molecular_weight: float, kind: str) -> tuple[float, str]:
    if not positive(value) or not positive(molecular_weight):
        raise ValueError("concentration and molecular weight must be positive finite numbers")
    factors = {"concentration": {"ng/mL": 1000 / molecular_weight, "nM": 1, "uM": 1000, "mM": 1_000_000},
               "auc": {"ng*h/mL": 1000 / molecular_weight, "nM*h": 1}}
    if kind not in factors or unit not in factors[kind]:
        raise ValueError("unit/quantity mismatch; AUC is not concentration and dose is not exposure")
    converted = value * factors[kind][unit]
    if not math.isfinite(converted):
        raise ValueError("converted quantity overflow")
    return converted, "nM" if kind == "concentration" else "nM*h"


def comparison_barriers(a: dict, b: dict) -> list[str]:
    """Explain why two numerical exposures cannot establish a therapeutic margin."""
    barriers = []
    for key in ("analyte", "matrix", "basis", "kind", "time_context", "endpoint"):
        if a.get(key) != b.get(key):
            barriers.append("different_" + key)
    if any(r.get("matrix") == "reported_plasma_unresolved" or r.get("basis") == "unresolved" for r in (a, b)):
        barriers.append("unresolved_measurement")
    if any(r.get("provenance") != "measured" for r in (a, b)):
        barriers.append("model_or_label_not_matched_measurement")
    # This review contains public cross-model data, not a validated patient-specific bridge.
    barriers.append("no_validated_genotype_matched_normal_tumour_bridge")
    return barriers


def audit(ledger: dict, source_ids: set[str]) -> dict:
    if not isinstance(ledger, dict) or type(ledger.get("schema_version")) is not int or ledger.get("schema_version") != 1 or ledger.get("clinical_use") != "research_only" or ledger.get("clinical_exposure_margin", "missing") is not None:
        raise ValueError("unsupported exposure schema or manufactured clinical margin")
    analytes, records = ledger.get("analytes"), ledger.get("records")
    if not isinstance(analytes, dict) or not analytes or not isinstance(records, list) or not records:
        raise ValueError("missing exposure records/analytes")
    for a in analytes.values():
        if not isinstance(a, dict) or not positive(a.get("molecular_weight")) or a.get("source") not in source_ids:
            raise ValueError("invalid molecular-weight provenance")
    converted, indexed = [], {}
    for r in records:
        if not isinstance(r, dict):
            raise ValueError("exposure record must be an object")
        for k in ("id", "analyte", "source", "locator", "population", "time_context", "endpoint", "limitation"):
            if not isinstance(r.get(k), str) or not r[k].strip():
                raise ValueError("exposure record missing " + k)
        if r["id"] in indexed or r["source"] not in source_ids or r["analyte"] not in analytes:
            raise ValueError("duplicate exposure ID or unknown source/analyte")
        if r.get("matrix") not in MATRICES or r.get("basis") not in BASES or r.get("kind") not in KINDS or r.get("provenance") not in {"measured", "model_derived", "label_reference"}:
            raise ValueError("unrecognized exposure semantics")
        values = r.get("values")
        if not isinstance(values, list) or not 1 <= len(values) <= 2 or not all(positive(v) for v in values) or values != sorted(values):
            raise ValueError("invalid positive ordered exposure values")
        translated = [convert(v, r.get("unit"), analytes[r["analyte"]]["molecular_weight"], r["kind"]) for v in values]
        converted.append({"id": r["id"], "values": [round(v[0], 6) for v in translated], "unit": translated[0][1],
                          "matrix": r["matrix"], "basis": r["basis"], "endpoint": r["endpoint"], "time_context": r["time_context"],
                          "clinical_exposure_margin": None})
        indexed[r["id"]] = r
    comparisons = []
    pairs = ledger.get("comparisons")
    if not isinstance(pairs, list):
        raise ValueError("comparisons must be an explicit array")
    for pair in pairs:
        if not isinstance(pair, list) or len(pair) != 2 or any(not isinstance(i, str) or i not in indexed for i in pair):
            raise ValueError("unknown comparison record")
        comparisons.append({"records": pair, "barriers": comparison_barriers(*(indexed[i] for i in pair)), "clinical_exposure_margin": None})
    return {"records": converted, "comparisons": comparisons, "clinical_exposure_margin": None,
            "interpretation": "Unit conversions only; no drug efficacy, clinical target, dose or therapeutic margin inferred."}


def main() -> None:
    sources = json.loads((ROOT / "notes/track2-sources.json").read_text())
    print(json.dumps(audit(json.loads(LEDGER.read_text()), {s["id"] for s in sources["sources"]}), indent=2))


if __name__ == "__main__":
    main()
