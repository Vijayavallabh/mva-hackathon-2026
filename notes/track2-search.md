# Track 2 search and source provenance

Review date: 2026-09-08. **Adaptive rapid scoping review**, not a preregistered
systematic review. Primary task: identify falsifiable approved-drug hypotheses and
their strongest objections. No raw subject data or protected narrative was queried.
Source claims are paraphrased; copyrighted full pages remain in ignored local caches.

## Public competition contract

The unauthenticated Space API returned revision
`1c761cc23d90aebe6a011fd5b0b99517df42408c`, also the previously pinned revision.
The following public files were fetched at that revision, not a moving branch:

| File | SHA-256 |
|---|---|
| `config.py` | `a65e67fca2fb698ac3f3fe6610e585f549cf29f175d636ce77543d7db6dc8bdc` |
| `tabs/submit_track2.py` | `f48d576ab052df34527222b7693f956e15e5376ef68eddedcf0c4f04736bf65c` |
| `tabs/about.py` | `1867b07f24d987fbb728c756c2d2bc4ab5f302d7c7804f53fe7b6a8b4c83ae43` |
| `utils.py` | `b53ae3bbce7e0c9729f27a53f4e315e85590e4cdddce4155c5d966d6aed1d9e9` |

The [configuration](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/1c761cc23d90aebe6a011fd5b0b99517df42408c/config.py)
sets Track 2 maximum entries to **3**, not 1. The
[submission instructions](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/1c761cc23d90aebe6a011fd5b0b99517df42408c/tabs/submit_track2.py)
say only the latest entry is reviewed. Required: participant-identifying report filename
(`.md` or `.pdf`), GitHub URL, three-minute YouTube/Vimeo pitch URL, and AI-provider,
plan/tier and data-handling disclosure. Teams designate one submitter. Rigor/impact/
innovation/scalability weights are 35/25/25/15. Repository publication is already complete.
Public code is not an authenticated quota/receipt check; no Track 2 upload was invoked.

## Reproduction and query evolution

```bash
uv run python scripts/track2_public_search.py results/feat009/search-new
uv run python scripts/track2_evidence.py sources results/feat009/sources-new
uv run python scripts/track2_evidence.py check
uv run python scripts/test_track2_evidence.py
```

Output directories must be new and under `results/feat009`. The search runner accepts
no subject-file input and no caller-supplied query. It records public response bytes,
request URL, retrieval time and SHA-256. Current summaries also record script SHA-256.
Historical runs predate that addition; their exact queries remain in their manifests.
HTTP success is not evidence of a valid result schema or a fully read article.
Independent review led to endpoint-specific schema checks for all JSON responses,
Python syntax checks for fetched public code, explicit empty/error-envelope failures,
and nonzero exit status when collection is partial. Revalidation with the revised parser
passes all 14 cached responses from the expanded run. All 30 source-cache byte hashes
and the final source-ledger hash match; 19 DOI/title pairs pass the revised validator too.
These offline rechecks preserve retrieval dates rather than inventing new retrievals.

The preferred skill search service had no configured authentication and started device
authorization. It was stopped without authentication or research retrieval. Public web,
Europe PMC, PubMed, Crossref and ClinicalTrials.gov were used instead. No additional
AI provider or image-generation service was used.

### Europe PMC

Every query below is ANDed with `FIRST_PDATE:[1900-01-01 TO 2026-09-08]`.
API format is JSON, `resultType=core`; default relevance order. Current code requests
up to 1,000 records per query on one page. More hits would still be explicitly truncated;
no pagination or comprehensive manual screening is claimed.

| ID | Exact focused query before date filter |
|---|---|
| mechanism | `TITLE_ABS:(BUB1B OR BUBR1) AND TITLE_ABS:("mosaic variegated" OR mutation OR deficiency)` |
| rescue | `TITLE_ABS:(BUB1B OR BUBR1) AND TITLE_ABS:(drug OR rescue OR treatment OR SIRT2 OR mTOR)` |
| tumour_trials | `TITLE_ABS:rhabdomyosarcoma AND TITLE_ABS:(temsirolimus OR everolimus OR hydroxychloroquine OR bortezomib) AND TITLE_ABS:(trial OR randomized)` |
| aneuploid_stress | `TITLE_ABS:aneuploidy AND TITLE_ABS:(chloroquine OR hydroxychloroquine OR AICAR OR "17-AAG")` |
| contradictions | `TITLE_ABS:(BUBR1 OR BUB1B) AND TITLE_ABS:(nicotinamide OR metformin OR phenylbutyrate OR gentamicin)` |

Three retrieval stages must not be conflated:

| Run | Mechanism | Rescue | Tumour trials | Aneuploid stress | Contradictions |
|---|---:|---:|---:|---:|---:|
| Broad full-text v2: hits / retrieved | 3,677 / 100 | 5,923 / 100 | 1,282 / 100 | 899 / 100 | 440 / 100 |
| Focused first pass: hits / retrieved | 138 / 100 | 404 / 100 | 7 / 7 | 12 / 12 | 5 / 5 |
| Focused expanded page: hits / retrieved | 138 / 138 | 404 / 404 | 7 / 7 | 12 / 12 | 5 / 5 |

These are overlapping query results, **not unique studies or full-text inclusion counts**.
The broad run used the earlier non-title/abstract variants of these themes; exact strings
are preserved in `results/feat009/search-20260908-v2/manifest.json`. Focused first-pass
provenance is in `results/feat009/search-20260908-focused/`. The expanded run in
`results/feat009/search-20260908-expanded/` retrieved all reported hits for these five
particular queries, with zero failed requests. Retrieval completeness for a query is
not comprehensive reading or completeness of the literature search.

An initial run in `search-20260908/` supplied an unsupported sort parameter. Europe PMC
returned HTTP 200 with a version-only object, not search results. Its old null/zero
summary is **invalid and excluded**, not evidence of no literature. The parser now rejects
missing/noninteger hit counts and missing results; regression tests cover this failure.
Some direct full-text XML requests also failed. Selected journal/PMC sections or abstracts
were used, and the source ledger records reading depth honestly.

### Complementary channels

- PubMed ESearch: `(BUB1B OR BUBR1) AND (drug OR rescue OR treatment) AND
  ("1900/01/01"[Date - Publication] : "2026/09/08"[Date - Publication])`.
  First reviewed run: 570 hits, first 100 identifiers retrieved. This is overlapping
  coverage with Europe PMC, not 100 independent confirmations.
- ClinicalTrials.gov API v2: condition query `mosaic variegated aneuploidy`, page size
  100, returned `studies: []`. This does not rule out differently indexed trials,
  unregistered work or eligibility in broader oncology studies. Registrations
  NCT01222715 and NCT02567435 were separately retrieved and compared with publications.
  Registry status is as retrieved, not retrospectively date-filtered.
- Adaptive public-web searches included BUB1B/BUBR1 rescue, NAD/SIRT2/NMN/nicotinamide,
  mTOR and allele-specific mouse work; aneuploidy with autophagy/proteasome/AMPK stress;
  RMS temsirolimus trials; current official labels; and ataluren regulatory decisions.
  Generic Asn1002Lys/N1002K functional-literature queries found no direct intervention
  study in the reviewed results. That is not proof none exists. Search-engine ranking
  is mutable and no PRISMA count is assigned to these exploratory searches.
- Crossref verifies DOI/title metadata, authorship, journal/date and returned correction
  relations. The JCI corrigendum was independently read; absent metadata links cannot
  establish that a paper has no other correction or retraction.
- DailyMed and EMA supply approved-use jurisdiction and safety boundaries. Approval
  in one indication is not approval in MVA or proof of a pediatric cancer exposure window.

## Explicit screening decisions

The seven focused RMS trial-search results were individually considered:

| PMID | Decision and reason |
|---|---|
| 38936378 | Include: randomized phase III ARST1431, negative primary endpoint; central counterevidence. |
| 31513481 | Include: randomized relapse selection trial ARST0921; active comparator limits attribution. |
| 22033322 | Include: pediatric monotherapy phase II; missed early response threshold, retain late RMS response. |
| 25446280 | Include: phase II cixutumumab/temsirolimus, no objective responses; negative translation evidence. |
| 37243336 | Context only: ARST1431 feasibility report, not an independent efficacy confirmation of the final trial. |
| 24249672 | Context only: phase I temsirolimus/irinotecan/temozolomide; feasibility is not controlled efficacy or the same regimen. |
| 37016270 | Exclude as primary claim support: secondary vinorelbine meta-analysis, not a BUB1B intervention experiment. |

The smaller aneuploid-stress and contradiction result groups informed Tang/North/Lyu
selection. Animal aging, heart-specific phenotypes, meiotic studies, unrelated tumour
overexpression, in-silico-only screens and preprints in other diseases were not promoted
to direct MVA drug evidence. A retrieved other-tumour BUB1B-inhibition paper can represent
the opposite intervention direction from constitutional rescue. Disease- or compound-name
overlap alone was never an inclusion criterion for efficacy.

Selection was adaptive and performed by an AI-assisted reviewer; it was not independent
duplicate title/abstract screening. The later two-agent review challenges the selected
claims and implementation, but does not retrospectively turn selection into a systematic
review. Exact patient-allele interventions, negative unpublished studies, languages not
read and unindexed records remain important coverage gaps.

## Evidence inventory and verification

The session-31 ledger contained 30 distinct source IDs: 19 DOI-bearing papers/notices and
11 official label/decision/registry/competition pages. Each recorded model, claim,
reading depth and limitation. Its twelve candidate entries then comprised
two conditional screens, one benchmark, three deprioritizations and six exclusions.
These are manually reasoned decisions, not generated efficacy estimates.

The initial 28-source identity check passed all 17 DOI/title matches with no retrieval
errors (`results/feat009/source-verification-v1/`). Two further primary negative studies
were added and overbroad reading-depth labels corrected; that historical hash is not
the final source-ledger hash. The updated verification is stored separately in
`results/feat009/source-verification-v2/`: **30 sources, 19 DOI/title matches, zero
retrieval errors or title-review flags**, and 11 official pages fetched. Metadata success does not validate claims;
official-page retrieval also does not by itself establish that every section was read.

Bibliographic checks supplement, not replace, the explicit correction-aware content
review. The bundled literature-review citation verifier was also called on the exact
ledger DOI strings, avoiding its Markdown regex's truncation of parenthesized DOIs.
Its DOI-resolution check is weaker than the repository's exact identifier/title match;
neither constitutes clinical validation. Actual pass/error counts are recorded in progress.

## Session 32 supplementary review

See [the final review](track2-final-review.md) for all twelve additional fixed query
themes/counts, 941 distinct source/ID records, selected-text reading limits, public XML
access failures, exposure quantities and updated decisions. The final search-only run
`results/feat009/final-review-search-v2-20260908/` has zero failed or truncated queries.
One DOI appears under both a MED and a PPR identifier; these are not independent studies.
Other overlapping reports/versions still need study-level linking before any meta-analysis.

The current curated ledger contains **52 sources: 39 DOI-bearing papers/notices,
11 official pages and two PubChem molecular-identity records**. All 39 DOI/title pairs
matched in source-verification-v3. Its two small valid PubChem JSON responses were initially
rejected by the HTML-page size heuristic, not by an identity mismatch or API failure.
The revised implementation uses a typed CID/molecular-weight check for these records.
The subsequent verification artifact and actual test counts are recorded in progress.

HCQ is now deprioritized: twelve entries comprise one conditional screen, one benchmark,
four deprioritizations and six exclusions. New clinical response exceptions, negative
endpoints and horizon findings are preserved. No claim of exhaustive screening, clinical
efficacy or a measured normal/tumour therapeutic margin follows from these counts.
