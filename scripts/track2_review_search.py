#!/usr/bin/env python3
"""Fixed public-only supplementary Track 2 search and primary full-text archive.

No subject input, arbitrary query, model service, credential or submission operation.
Retrieval is bounded and is not human screening. New ignored output directory only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.parse
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

from track2_public_search import parse_epmc

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
CUTOFF = "2026-09-08"
QUERIES = {
    "bubr1_interventions": 'TITLE_ABS:(BUBR1 OR BUB1B) AND TITLE_ABS:(rescue OR drug OR treatment OR pharmacological OR SIRT2 OR NAD OR rapamycin OR mTOR)',
    "mva_interventions": 'TITLE_ABS:"mosaic variegated aneuploidy" AND TITLE_ABS:(therapy OR treatment OR drug OR rescue)',
    "rms_rapalogs": 'TITLE_ABS:rhabdomyosarcoma AND TITLE_ABS:(rapamycin OR sirolimus OR everolimus OR RAD001 OR temsirolimus)',
    "rms_lysosome": 'TITLE_ABS:rhabdomyosarcoma AND TITLE_ABS:(hydroxychloroquine OR chloroquine OR autophagy OR proteostasis OR proteasome OR p97)',
    "everolimus_pediatric_pk": 'TITLE_ABS:everolimus AND TITLE_ABS:(child OR children OR pediatric OR paediatric) AND TITLE_ABS:(pharmacokinetics OR pharmacokinetic OR exposure)',
    "hcq_oncology_pk": 'TITLE_ABS:hydroxychloroquine AND TITLE_ABS:(cancer OR oncology OR tumor OR tumour) AND TITLE_ABS:(pharmacokinetics OR pharmacokinetic OR concentration OR exposure)',
    "hcq_randomized": 'TITLE_ABS:hydroxychloroquine AND TITLE_ABS:(cancer OR carcinoma OR glioblastoma) AND TITLE_ABS:(randomized OR randomised OR phase)',
    "aneuploid_selectivity": 'TITLE_ABS:aneuploidy AND TITLE_ABS:(hydroxychloroquine OR chloroquine OR AICAR OR proteotoxic OR proteostasis OR rapamycin)',
    "rms_metformin": 'TITLE_ABS:rhabdomyosarcoma AND TITLE_ABS:metformin',
    "rms_bortezomib": 'TITLE_ABS:rhabdomyosarcoma AND TITLE_ABS:bortezomib',
    "bubr1_readthrough": 'TITLE_ABS:(BUBR1 OR BUB1B) AND TITLE_ABS:(readthrough OR gentamicin OR ataluren OR phenylbutyrate OR stabilizer OR stabilisation)',
    "rms_comparators": 'TITLE_ABS:rhabdomyosarcoma AND TITLE_ABS:(vincristine OR irinotecan OR temozolomide) AND TITLE_ABS:(randomized OR randomised)',
}
FULLTEXTS = {
    "kwong2025": "PMC12581410",
    "hcq_pbpk2018": "PMC5931434",
    "rangwala2014": "PMC4203516",
    "myeloma_hcq2017": "PMC5566051",
    "tang2011": "PMC3532042",
    "gupta2024": "PMC11550893",
    "geoerger2012": "PMC3539305",
    "wagner2015": "PMC4501773",
    "sieben2020": "PMC6934189",
    "north2014": "PMC4194088",
    "santana2020": "PMC7103504",
    "rosenfeld2014": "PMC4203513",
    "karasic2019": "PMC6547080",
    "zeh2020": "PMC8086597",
    "metts2023": "PMC9972017",
    "lenvatinib2025": "PMC12716803",
    "oreilly2026": "PMC12863344",
    "peron2012": "PMC3480867",
    "tmz_autophagy2018": "PMC6202374",
    "combination2016": "PMC4965487",
    "metformin_sarcoma2013": "PMC3877110",
    "auranofin2017": "PMC5680568",
    "posaconazole2021": "PMC8493378",
}


def metadata_xml(data: bytes, expected_pmc: str) -> dict:
    root = ET.fromstring(data)
    if root.tag != "article":
        raise ValueError("not a primary article XML response")
    ids = {e.get("pub-id-type"): "".join(e.itertext()).strip() for e in root.findall("./front/article-meta/article-id")}
    found = ids.get("pmc", ids.get("pmcid", ""))
    if found.removeprefix("PMC") != expected_pmc.removeprefix("PMC"):
        raise ValueError("PMC article identity mismatch")
    title = " ".join("".join(e.itertext()) for e in root.findall("./front/article-meta/title-group/article-title"))
    if not title or root.find("body") is None:
        raise ValueError("article title or main text missing")
    return {"ids": ids, "title": title, "body_present": True, "full_text_retrieval_is_not_full_text_review": True}


def run(output: Path, mode: str) -> dict:
    output = output.resolve()
    if not output.is_relative_to(ROOT / "results/feat009"):
        raise ValueError("new output must be under results/feat009")
    output.mkdir(parents=True, exist_ok=False)
    manifest, searches = [], []

    def capture(key: str, url: str, extension: str, validator) -> object | None:
        row = {"id": key, "url": url, "retrieved_at": datetime.now(timezone.utc).isoformat()}
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MVA-Track2-public-review/1.0"})
            with urllib.request.urlopen(req, timeout=40) as response:
                data = response.read()
            name = key + "." + extension
            (output / name).write_bytes(data)
            row.update(file=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
            result = validator(data)
            row.update(status="ok")
            return result
        except (OSError, ValueError, ET.ParseError) as exc:
            row.update(status="error", error_type=type(exc).__name__)
            if isinstance(exc, urllib.error.HTTPError):
                row["http_status"] = exc.code
            return None
        finally:
            manifest.append(row)
            (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
            time.sleep(0.4)

    if mode in ("search", "all"):
        for key, query in QUERIES.items():
            dated = f'({query}) AND FIRST_PDATE:[1900-01-01 TO {CUTOFF}]'
            params = urllib.parse.urlencode({"query": dated, "format": "json", "pageSize": 1000, "resultType": "core"})
            result = capture(key, "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + params, "json", parse_epmc)
            if result is not None:
                count, rows = result
                searches.append({"id": key, "database": "Europe PMC", "query": dated, "hit_count": count,
                                 "retrieved_count": len(rows), "truncated": count > len(rows),
                                 "records": [{k: r.get(k) for k in ("id", "source", "title", "doi", "pmcid", "pubYear")} for r in rows]})
            print(json.dumps({"query": key, "result": None if result is None else {"hits": result[0], "retrieved": len(result[1])}}), flush=True)
    if mode in ("fulltexts", "all"):
        for key, pmc in FULLTEXTS.items():
            result = capture(key, f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/fullTextXML", "xml", lambda data, pmc=pmc: metadata_xml(data, pmc))
            print(json.dumps({"article": key, "metadata": result}), flush=True)
    unique = {(r["source"], r["id"]) for q in searches for r in q["records"]}
    by_doi = {}
    for q in searches:
        for r in q["records"]:
            if isinstance(r.get("doi"), str) and r["doi"].strip():
                by_doi.setdefault(r["doi"].lower(), set()).add((r["source"], r["id"]))
    summary = {"cutoff": CUTOFF, "mode": mode, "queries": searches, "unique_retrieved_records": len(unique),
               "failed_requests": sum(r["status"] != "ok" for r in manifest),
               "retrieval_complete": all(r["status"] == "ok" for r in manifest) and all(not q["truncated"] for q in searches),
               "script_sha256": SCRIPT_SHA256,
               "same_doi_record_groups": {doi: sorted(ids) for doi, ids in by_doi.items() if len(ids) > 1},
               "record_identity_policy": "Deduplicate on database source and ID; report cross-record DOI groups separately. Preprint/final papers and multiple reports of one trial still need manual study-level linkage.",
               "limitations": "Fixed first-page maximum 1000 per query. Overlapping citation records, not screened studies; no claim of exhaustive literature coverage or database independence."}
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("search", "fulltexts", "all"))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    summary = run(args.output, args.mode)
    print(json.dumps({k: v for k, v in summary.items() if k != "queries"}, indent=2))
    if not summary["retrieval_complete"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
