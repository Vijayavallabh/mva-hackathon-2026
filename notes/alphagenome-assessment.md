# AlphaGenome Atlas: attempted use and application decision

2026-09-08, session 33, feat-009; baseline `d1e32b7` (clean, upstream-matched).
User requests rigorous use of AlphaGenome Atlas if relevant. This addendum does not
change uploaded Track 1 files or the reviewed Track 2 v2 research snapshot.

## Outcome

**Session 35 supersedes the access status below:** the owner configured the key
locally. Authenticated metadata, the public control and both candidate AVI/feature
lookups succeeded. Detailed molecular retrieval failed. See the
[authenticated results and disclosure](alphagenome-authenticated-results.md).
No phase, drug-priority or exposure conclusion changes; v4/v2 snapshots are preserved.
The following session-33/34 observations remain historical, not current access status.

**Session 36:** the owner-downloaded merged-splicing archive passed local integrity
checks and exact indexed lookups. [Offline results](alphagenome-splicing-results.md)
provide both candidate aggregate scores; no new hosted inference occurred. The
remaining gap is tissue/junction detail, not absence of every splicing prediction.

**Relevant for optional molecular interpretation; no Atlas scores obtained.** The
official resource launched today. We inspected its primary manuscript, pinned SDK,
public catalogue and downloadable-artifact routes. Both advertised score-download
endpoints returned HTTP 500 in bounded requests. Neither common API-key environment
variable was configured; no authenticated lookup or hosted inference was attempted.

Do not translate these access failures into a zero score, benignity, no splice effect,
or absence of support. No score-bearing data have been analysed and no candidate or
drug ranking changes. Trans phase remains unconfirmed; clinical exposure margins remain
unknown. The scientific rationale and source citations are in the independently written
[primary-source review](alphagenome-primary-review.md).

## Scope and acceptance criteria

1. Identify the official new Atlas and distinguish it from base AlphaGenome and third-party
   resources; pin the inspected code and distinguish dataset release from study coverage.
2. Determine whether the outputs address an unresolved question, without treating an
   annotation ensemble as an independent experiment or a drug-response predictor.
3. Attempt bounded access to public resources without raw subject input, authentication,
   arbitrary URLs, hosted model calls or multi-gigabyte transfers.
4. Record failed/partial requests and provenance, with synthetic tests for false success
   and interrupted transport. Missing data must stay missing.
5. Preserve existing submissions/snapshots and independently review the new work; run
   repository checks, record evidence, commit and push. No claim that scores were obtained
   is an acceptance requirement: availability depends on the external resource.

## Reproducible access observations

```bash
uv run python scripts/alphagenome_access_audit.py results/feat009/alphagenome-access-v2
uv run python scripts/test_alphagenome_access_audit.py
```

The first command creates a **new** directory: change the suffix when repeating it.
It returned exit **2**, intentionally indicating unavailable resources. It made seven
fixed public GET requests, retained at most 2 MB per document and 4,097 bytes when a
server ignored the 4,096-byte archive range, and used no credentials. Expected successful
archive probes require a valid 206 range and ZIP prefix; even that would prove neither
complete archive integrity nor any variant score.

| Resource | Observed response | Interpretation |
|---|---:|---|
| Portal | 200; 184,469 bytes | Public application shell/catalogue metadata, not scores or a tested interactive session |
| Terms page | 200; 184,469 bytes | Application shell; complete operative terms not verified or accepted |
| Pinned SDK README | 200; 12,132 bytes | Documentation retrieved |
| Pinned Atlas client | 200; 16,105 bytes | Implementation retrieved; requests transmit variant/interval fields when actually invoked |
| Pinned Atlas protocol | 200; 6,053 bytes | API schema retrieved, not an API result |
| AVI SNV archive, range 0–4095 | 500; 21-byte error | Unavailable in this observation |
| Merged-splicing SNV archive, same range | 500; 21-byte error | Unavailable in this observation |

The manifest `results/feat009/alphagenome-access-v2/access-audit.json` stores UTC request
times, exact fixed URLs, statuses, retained-byte hashes and the executing script hash.
The earlier v1 snapshot and exploratory HEAD/range observations are retained as historical
attempts, not replaced. These observations do not prove a worldwide outage or that a
signed-in browser would fail. No login control was bypassed and no endpoint was guessed
to evade access controls.

The inspected SDK revision is `aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d` (0.9.0
Atlas addition). It is **not** a verified version identifier for the underlying Atlas
dataset. Exact release/data hashes would still be required for a score-bearing analysis.

## Scientific value test before using a score

Both leading alleles are SNVs according to the permitted derived report, so the initial
SNV release is potentially applicable. No raw genotype file was needed for this finding.
The following are prospective analyses, not completed results:

| Question | Potential useful output | What would not answer it |
|---|---|---|
| Is there an unexpected RNA-processing hypothesis? | Transcript-resolved splicing scores, raw effects and relevant context | A composite score dominated by an already-known termination consequence |
| Does the missense allele have additional regulatory effects? | Separated molecular subscores and attributions | Reusing AlphaMissense/conservation inside AVI as independent validation |
| Which experiment changes? | A testable RNA/splicing comparison with allele and isogenic controls | Adding another high score without a changed falsifiable experiment |
| Is the pair in trans? | No Atlas output establishes this | Simulated haplotypes assume, rather than observe, phase |
| Is everolimus or HCQ effective at safe exposure? | No Atlas output directly establishes this | Variant impact, predicted expression or SHAP interpreted as drug response/PK |

Predeclare the exact submitted candidate scope and relevant transcripts/contexts before
viewing scores. Preserve all requested molecular outputs, including weak and contradictory
effects, instead of selecting only a maximum. Verify GRCh38 REF and coordinates locally:
the SDK's Variant constructor takes a 1-based position, whereas intervals are 0-based,
half-open. Do not infer a dataset's coordinate conventions solely from the client.
[Official coordinate/score documentation](https://www.alphagenomedocs.com/faqs.html)

AVI combines existing annotations and frequency-proxy training; chromosome 15 is in its
training set, but exact candidate overlap is unknown. Therefore do not call an eventual
lookup out-of-sample validation. A PHRED rank is not a pathogenicity probability, and
an unsigned impact score does not supply drug-intervention direction. Local inference
with base AlphaGenome would not reproduce the new AVI ensemble. Details and primary
evidence are in the companion review.

## Safe next access routes

1. **Preferred: public artifact, then local lookup.** Confirm the complete applicable
   terms and retry the documented archive endpoint when accessible. Check actual size,
   version, checksum, compression, index and schema before a deliberate download. Fetch
   a public reference resource without subject-dependent requests, then do any candidate
   matching entirely on this machine. Do not download the full petabyte-scale Atlas.
2. **Alternative: owner-configured API access.** If the owner elects this route, they must
   complete the provider's account/terms workflow and store the key locally—never paste
   it into chat, tracked files or logs. Recheck the exact approved payload first. Raw VCF
   records/subsets, sequences from the subject and clinical narrative remain prohibited;
   public gene/reference queries and permitted submission-derived outputs are a separate
   category, not a waiver for source-file upload. Start with public metadata/control data.
3. **Local base model is a different experiment.** Gated weights, model terms, hardware
   availability and reproducible setup need separate checks. It cannot be substituted
   for an unperformed Atlas/AVI lookup. No model installation or GPU job ran here.

Resource check: approximately 3,250 GB free disk and 452 GB available RAM, but all four
visible A100s were busy (99–100% utilization); one T400 was idle. Device discovery does
not mean a GPU is available. The resource skill's script ran using ephemeral
`uv run --with psutil` after plain execution lacked that dependency; project dependencies
were unchanged. Snapshot: `results/feat009/alphagenome-resources-20260908.json`.
No large download was warranted while bounded access and full terms remained unresolved.

## Independent devil's-advocate review

**Standards:** two P2 issues found in the new access script. A declared Content-Length
mismatch could pass document validation, and interrupted normal/error-body reads could
abort collection before a manifest was written. Fixes reject declared truncation, catch
transport/body-read failures and checkpoint completed observations with explicit
`in_progress` status. Seven new tests cover these failures; **33 tests pass**.
Independent recheck reproduced the attacks and reports both resolved, with no directly
introduced regression. Historical artifacts and protected files were untouched.

**Specification/science:** independent checking of the manuscript's relevant sections,
PDF hash and pinned source supports the release, calibration, training/dependence and
licence distinctions. No material finding remained. This was not a replication of
Atlas predictions or an exhaustive benchmark audit.

The access audit and relevance assessment are complete; actual score retrieval remains
unperformed because of the observed access limitations. Feat-009's report/video/submission
workflow can proceed without inventing Atlas evidence. The reviewed Track 2 v2 bundle
and 53-source drug-evidence ledger remain unchanged; this addendum is not a new submitted
report, hosted pitch, clinical validation or extra AI-provider inference run.

## Session 34 continuation: rendering resolved, score access still unavailable

The owner asked to continue. At baseline `af8a58b`, the new fixed-endpoint run
`uv run python scripts/alphagenome_access_audit.py results/feat009/alphagenome-access-v3`
again returned exit 2: five document/catalogue responses and two HTTP 500 score
archives. Neither common API-key environment variable was configured. Earlier attempts
remain preserved. No score, patient query or hosted inference was produced.

There was material progress on the document-access issue. A fresh, unauthenticated
headless Chrome profile rendered the official downloads page and output terms. Adding
`--virtual-time-budget=10000` allowed the service-terms page's asynchronous content to
appear. The initial plain rendered page had only navigation, so it is not evidence
that the terms require sign-in. Complete service/output text was read by the main and
independent research agents. No cookie-agreement, account-registration or terms-acceptance
button was clicked. Account eligibility and all incorporated Google policies were not
independently audited; this is not legal approval.

Reproduction pattern (use a new output directory/profile; browser sandbox stays enabled):

```bash
atlas_profile=$(mktemp -d /tmp/atlas-browser-check.XXXXXX)
timeout 45s google-chrome --headless=new --disable-gpu --no-first-run \
  --user-data-dir="$atlas_profile" --timeout=30000 --virtual-time-budget=10000 \
  --dump-dom https://deepmind.google.com/science/alphagenome/terms
```

Captured rendered documents:

| Artifact under `results/feat009/` | SHA-256 |
|---|---|
| `alphagenome-browser-v2/terms-rendered.html` | `150ee80ca3715b90de608f6e79daa26a16e6ff400266c172f8fef71965dab954` |
| `alphagenome-browser-v1/output-terms-rendered.html` | `834e1e5d244b9ee0d3941bce19d498fb671609200bc92962f8a02b4fb7f3bd2b` |
| `alphagenome-browser-v1/downloads-rendered.html` | `402a0c1ffb9fdbca162f08cb404f3c3cd45041550e9740163c4794c5b8fd4982` |

The [current service terms](https://deepmind.google.com/science/alphagenome/terms)
are modified 8 September 2026; the [output terms](https://deepmind.google.com/science/alphagenome/output-terms)
are effective 25 June 2025. AVI and its feature breakdown have different stated treatment;
do not apply the permissive-artifact exception to every output. The prior conclusion
that readable terms were unavailable is superseded, not the unchanged score-access result.
The official `alphagenome.google/downloads` link redirects to the same downloads page,
not an alternative working archive.

### Actual offline metadata extraction

We retrieved the official science-skills AVI helper at revision
`28b8482603a420708c8896f6fe5e06c276d9933d` and extracted only literal assignments from
its `AviFeature` enum using `ast.parse` and `ast.literal_eval`. The foreign program was
**not executed/imported**; its environment-file loading and API routines were not run.
The independently cached source and main download are retained locally. Source SHA-256:
`2e82f51cdcb022e251a0bd4619b1dcd926d45ef020f40e260081e5fc3f9f3f60`.

Final JSON: `results/feat009/alphagenome-browser-v1/feature-definitions-final.json`.
The parser asserted 18 unique definitions and typed name/category/scorer tuples. It
found **ten definitions tied to molecular scorers and eight annotation/indicator
definitions**. Definition order is not a measured importance ranking. An initial
extraction ran before the parallel download completed and failed; its empty JSON
file is not evidence. The final extraction used the independently cached pinned source.

| Static feature group | Count | Relevance to an eventual interpretation |
|---|---:|---|
| Splicing, RNA-seq, ATAC, DNase, TF/histone ChIP, CAGE, PRO-cap, polyadenylation, contact maps | 10 | Potential regulatory hypotheses; no predictions or tissue measurements obtained here |
| AlphaMissense | 1 | Potential overlap with existing protein-impact evidence |
| Cactus and PhastCons conservation | 2 | Potential overlap with conservation evidence |
| Protein termination, start lost, stop lost | 3 | May restate coding consequences rather than add functional evidence |
| Insertion and deletion indicators | 2 | Not an aneuploidy/CNV assay; the helper's broad “Structural Variant” category must not be misread |

[Pinned source and enum](https://github.com/google-deepmind/science-skills/blob/28b8482603a420708c8896f6fe5e06c276d9933d/skills/alphagenome_variant_impact_score/scripts/alphagenome_atlas_avi.py)
defines these fields; it does not supply their values for our candidates. The helper's
score and experimental-metadata paths still require a key. No alternative unkeyed score
route was found in the official source. Full reproducible extraction command is in
the session 34 progress record.

Next requirement for actual results remains working archive access or owner-configured
API access with an approved non-protected payload. Do not mistake this genuine metadata
work for AVI scoring or keep creating new score hypotheses from repeated access failures.
