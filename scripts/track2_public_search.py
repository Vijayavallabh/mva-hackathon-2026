#!/usr/bin/env python3
"""Reproduce fixed, public-only Track 2 literature searches; no subject-file inputs.

Responses and provenance go to a new ignored directory. Never sends credentials,
genotypes, phenotype text or caller-supplied queries. Network failures are recorded,
not reinterpreted as zero hits. This is a bounded scoping search, not exhaustive.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUTOFF = "2026-09-08"
PAGE_SIZE = 1000
QUERIES = {
    "mechanism": 'TITLE_ABS:(BUB1B OR BUBR1) AND TITLE_ABS:("mosaic variegated" OR mutation OR deficiency)',
    "rescue": 'TITLE_ABS:(BUB1B OR BUBR1) AND TITLE_ABS:(drug OR rescue OR treatment OR SIRT2 OR mTOR)',
    "tumour_trials": 'TITLE_ABS:rhabdomyosarcoma AND TITLE_ABS:(temsirolimus OR everolimus OR hydroxychloroquine OR bortezomib) AND TITLE_ABS:(trial OR randomized)',
    "aneuploid_stress": 'TITLE_ABS:aneuploidy AND TITLE_ABS:(chloroquine OR hydroxychloroquine OR AICAR OR "17-AAG")',
    "contradictions": 'TITLE_ABS:(BUBR1 OR BUB1B) AND TITLE_ABS:(nicotinamide OR metformin OR phenylbutyrate OR gentamicin)',
}


def get_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "MVA-Track2-public-evidence/1.0"})
    with urllib.request.urlopen(req, timeout=35) as response:
        return response.read()


def parse_epmc(data: bytes) -> tuple[int, list]:
    obj = json.loads(data)
    hits = obj.get("hitCount")
    rows = obj.get("resultList", {}).get("result")
    if type(hits) is not int or hits < 0 or not isinstance(rows, list):
        raise ValueError("invalid Europe PMC result schema; not zero hits")
    return hits, rows


def run(output: Path) -> dict:
    output = output.resolve()
    if not output.is_relative_to(ROOT / "results" / "feat009"):
        raise ValueError("output must be a new directory under results/feat009")
    output.mkdir(parents=True, exist_ok=False)
    records = []

    def capture(key: str, url: str, extension: str = "json") -> bytes | None:
        row = {"id": key, "url": url, "retrieved_at": datetime.now(timezone.utc).isoformat()}
        try:
            data = get_bytes(url)
            path = output / f"{key}.{extension}"
            path.write_bytes(data)
            row.update(status="ok", file=path.name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
            return data
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            row.update(status="error", error_type=type(exc).__name__)
            return None
        finally:
            records.append(row)
            (output / "manifest.json").write_text(json.dumps(records, indent=2) + "\n")
            time.sleep(0.4)

    summaries = []
    for key, query in QUERIES.items():
        dated = f'({query}) AND FIRST_PDATE:[1900-01-01 TO {CUTOFF}]'
        params = urllib.parse.urlencode({"query": dated, "format": "json", "pageSize": PAGE_SIZE, "resultType": "core"})
        raw = capture("epmc-" + key, "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + params)
        if raw:
            try:
                hits, rows = parse_epmc(raw)
            except (ValueError, TypeError):
                records[-1].update(status="invalid_response", error_type="schema")
                (output / "manifest.json").write_text(json.dumps(records, indent=2) + "\n")
                continue
            summaries.append({"id": key, "database": "Europe PMC", "query": dated, "hit_count": hits,
                              "retrieved_count": len(rows), "truncated": hits is not None and hits > len(rows),
                              "records": [{k: r.get(k) for k in ["id", "source", "title", "authorString", "pubYear", "doi", "pmcid", "pubTypeList", "isOpenAccess"]} for r in rows]})

    params = urllib.parse.urlencode({"db": "pubmed", "term": '(BUB1B OR BUBR1) AND (drug OR rescue OR treatment) AND ("1900/01/01"[Date - Publication] : "2026/09/08"[Date - Publication])', "retmode": "json", "retmax": 100})
    capture("pubmed-rescue", "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + params)
    params = urllib.parse.urlencode({"query.cond": "mosaic variegated aneuploidy", "format": "json", "pageSize": 100})
    capture("clinicaltrials-mva", "https://clinicaltrials.gov/api/v2/studies?" + params)
    for nct in ["NCT01222715", "NCT02567435"]:
        capture(nct, "https://clinicaltrials.gov/api/v2/studies/" + nct)
    public_base = "https://huggingface.co/"
    info = capture("space-info", public_base + "api/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026")
    if info:
        rev = json.loads(info)["sha"]
        for name in ["config.py", "tabs/submit_track2.py", "tabs/about.py", "utils.py"]:
            capture("space-" + name.replace("/", "-"), public_base + "spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/raw/" + rev + "/" + name, "txt")
    result = {"cutoff": CUTOFF, "queries": summaries, "failed_requests": sum(r["status"] != "ok" for r in records),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "note": "Bounded first-page scoping retrieval; Europe PMC and PubMed overlap. Trial status is as retrieved, not date-filtered."}
    (output / "search-summary.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    summary = run(args.output)
    print(json.dumps({"queries": [{k: q[k] for k in ["id", "hit_count", "retrieved_count", "truncated"]} for q in summary["queries"]], "failed_requests": summary["failed_requests"]}, indent=2))
