# AlphaGenome Atlas: attempted use and application decision

2026-09-08, session 33, feat-009; baseline `d1e32b7` (clean, upstream-matched).
User requests rigorous use of AlphaGenome Atlas if relevant. This addendum does not
change uploaded Track 1 files or the reviewed Track 2 v2 research snapshot.

## Outcome

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
