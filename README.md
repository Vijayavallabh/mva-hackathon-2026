# MVA Hackathon 2026

Working repo for [Rare Disease, Real Kid: The MVA Hackathon 2026](https://sagebio-rare-disease-real-kid-mva-hackathon-2026.hf.space/),
run by Sage Bionetworks with the MVA Society, Hugging Face and BEACON.

The dataset is whole-genome sequencing from one child with Mosaic Variegated
Aneuploidy, an ultra-rare condition with fewer than 50 known cases and no
established treatment. The family released it hoping someone finds the causal
variant. Two tracks:

- **Track 1 — variant prediction.** Rank the variant(s) driving the condition
  from the VCF, the FASTQ lanes and the clinical phenotype. Scored automatically
  against the NHS-confirmed answer on rank points and F-max. Six submissions allowed.
- **Track 2 — drug repurposing.** Characterize the mechanism and propose approved
  drugs that plausibly act on it. Judged by a panel on rigor (35%), impact (25%),
  innovation (25%), scalability (15%). Public code reviewed 8 Sep permits three
  entries; only the latest is reviewed. Recheck live rules before submission.

Submissions close **24 Oct 2026, 23:59 UTC**.

The optical follow-up has a documented [coordinate-exclusion correction](notes/track2-optical-correction-v35.md).
Four absolute centroid columns slipped into the original v33 model inputs. Those
fits are excluded from gain claims; corrected fitting and validation use separate
v35 outputs. The [completed v36 comparison](notes/track2-optical-v36.md) integrates the correction,
all controls and their limitations; the frozen v34 progress presentation is historical.

## This repository contains no subject data, and never will

Access is gated and the terms are binding, not advisory. `data/`, `results/` and
`logs/` are gitignored, every genomic file extension is gitignored everywhere,
and `scripts/no_data_in_git.sh` runs as a pre-commit hook that refuses any commit
touching them. Raw subject data — FASTQ, BAM, VCF records, the clinical narrative —
does not leave this machine, including into third-party model APIs.

Derived outputs are a different matter and are meant to be shared: the rules state
participants "are free to publicly share their code, models, and derived outputs at any
time". So aggregate statistics, HPO term IDs and labels, gene names and the submitted
candidate variants are tracked here deliberately. This repo goes **public** before the
first Track 1 submission under our current local policy. The official portal requires a
GitHub URL but permits private visibility until the competition ends; changing our stricter
policy requires the owner's decision.

Local tooling may process gated inputs for assigned analyses, but hosted model context is
restricted to permitted derived outputs. Filesystem authorization never permits uploading
raw subject data or the clinical narrative to a model API.

Commit every intended repository change, even a tiny one. At the end of each session,
push all new commits to the configured `origin` after verification.

Everything must be deleted and confirmed by **23 Nov 2026** at **cnb@sagebase.org** —
see `notes/deletion-plan-v2.md`, which corrects earlier frozen deadlines and the recipient. Full rules in `AGENTS.md`.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and a Hugging Face account approved for
`SageBio/mva-hackathon-2026-data`.

```bash
hf auth login                 # or export HF_TOKEN
./scripts/download_data.sh    # 85 GB into data/, resumable, ~25 min at 60 MB/s
./scripts/get_tools.sh        # pinned local bioinformatics toolchain
./scripts/get_resources.sh    # matching reference + offline annotation resources
./init.sh                     # env + integrity + safety gates
```

`init.sh` is idempotent and is the only setup step. It verifies every local file
against the remote dataset tree, so a partial download is reported rather than
silently analyzed.

## Two details that silently score zero

Written down because there are only six submissions and both look fine when wrong:

- **The VCF's contigs are unprefixed** (`1`, `2`, `X`) but Track 1 submissions must be
  **`chr`-prefixed**. The scorer matches by exact tuple equality and never normalizes.
- **`proband_id` must be `PROBAND01`**, not the sample name `WGS_EX2312012` in the filenames.

Both, plus the scoring mechanics, are in `notes/challenge-spec.md`.

## Layout

| Path | Contents |
|---|---|
| `data/` | 85 GB gated dataset: 1 VCF + index, 8 FASTQ lanes, clinical phenotype docx. Gitignored. |
| `scripts/` | data, toolchain, resource, phenotype and verification entry points |
| `tools/` | Gitignored local binaries plus tracked version/checksum metadata |
| `notes/` | Tracked markdown: data profile, challenge spec, prior hypotheses, HPO terms, deletion plan |
| `results/` | Derived output. Gitignored — contains subject genotypes. |
| `AGENTS.md` | Working rules, access terms, established data facts, definition of done |
| `feature_list.json` | Source of truth for what is done |
| `notes/track2-current.json` | Current Track 2 artifacts and unresolved status |
| `progress.md` | Session log |

## Status

**Track 1: owner-reported first-submission scores are 100 rank points / F-max 1**, at
leaderboard position 93 (2026-09-08). Receipt and uploaded-byte identity have not been
independently verified. This is a reported competition result, not the earlier local
hypothetical 100/1 test. It does not establish allele function or phase:
**trans phase remains unconfirmed**. The submitted v4 CSV/report are preserved.

The [reviewer brief](notes/track2-reviewer-brief-v42.md) summarizes the proposed
experiment. [Competition priorities](notes/track2-competition-strategy-v42.md) map
work to the four weighted criteria and organizer announcement 28.

**Session 78: v40 clarifies the qualification sequence and recording workflow.**
The deck puts endogenous functional qualification before either intervention route,
labels the synthetic comparison arms and explains the optical metric. The report
states the comparative rationale and a specific contribution claim. A shared parser
checks all 367 narration words and the cue rates against the recording guide,
transcript and teleprompter. The ten-page report, workbook and nine-slide exports
remain research materials; no measured recording or submission exists. V39 and all
earlier bound inputs, source captures, drug decisions and the v37 demo/kit are preserved.

**Session 77: v39 qualifies endogenous function before advancing a drug hypothesis.**
The [source adjudication](notes/track2-rehearsal-adjudication-v39.md) narrows the
carrier-muscle mTOR rationale, corrects SIRT2 site/sex claims and retains opposing
somatic evidence. The [candidate comparison](notes/track2-candidate-comparison-v39.md)
and [qualification amendment](notes/track2-qualification-amendment-v39.md) define
falsifiers and the next experiment. Everolimus remains a conditional probe on HOLD;
no rescue-priority drug is established. The proposed engineered hTERT-RPE1 comparator
is not an available patient model. Use the current [v42 outside-review packet](notes/track2-external-review-packet-v42.md);
owner rehearsal and AI-assisted checks do not count as independent feedback.

**Session 75: v37 connects the proposal to the judging criteria and adds a working demo.**
Use the [nine-page report](notes/track2-report-v37.md),
[nine slides](notes/track2-slides-v37.html), [368-word script](notes/track2-pitch-v37.md),
[plain transcript](notes/track2-transcript-v37.txt) and
[reviewer guide](notes/track2-reviewer-guide-v37.md). The
[current record](notes/track2-current.json) routes the PDF, workbook and recording ZIP.
The [offline demo](notes/track2-demo-v37.html), [small reuse kit](notes/track2-community-kit-v37.md),
[laboratory handoff](notes/track2-lab-handoff-v37.md) and [reviewer questions](notes/track2-judge-questions-v37.md)
make the method inspectable. The owner chose their own voice: use the
[timed recording guide](notes/track2-recording-guide-v37.md) and [teleprompter](notes/track2-teleprompter-v37.html).
The 17 synthetic examples and actual unmeasured state test software behavior;
they do not establish clinical performance or external adoption.

The [follow-up assessment](notes/track2-competitive-review-v38.md) identifies remaining
work on the drug rationale, novelty and reader comprehension. An
[outside-review packet](notes/track2-external-review-packet-v38.md) and
[candidate comparison](notes/track2-candidate-comparison-v38.md) are ready for the
reviewer the owner can arrange. No outside review has occurred. These are review
additions; at that point the presentation and release remained v37, with drug decisions unchanged.

The preceding research used all eight H100s; 16 corrected fits and both full-cell/median campaigns
completed. Full interphase means recover BUB1B at ranks 1/3/3/2, with substantial
fourth-guide sensitivity. Neither arm passes the practical neural-gain gate;
mitotic coverage remains missing. Equal-cap learning improves on sampled means,
without beating full-data profiles. No drug or clinical claim is promoted.
The [complete analysis](notes/track2-optical-v36.md), six new falsification records
and all earlier research remain checked. There are 58 claim records across seven
registers. Review with `uv run --no-project python scripts/check_track2_harness_v47.py`;
original qualification evidence remains in `notes/track2-transcriptome-v19.md`.
Recording/hosting, provider/distribution questions, live checks and receipt remain open.

**Session 72: v34 materials distinguish pending optical work from validated results.**
The [report](notes/track2-report-v34.md), [nine slides](notes/track2-slides-v34.html),
[336-word narration](notes/track2-pitch-v34.md) and [reviewer guide](notes/track2-reviewer-guide-v34.md)
retain all completed research. The [v33 progress record](notes/track2-optical-progress-v33.md)
adds verified mitotic coverage and the registered eight-GPU study. Only one BUB1B
guide meets the mitotic minimum; model gains and interphase analysis remain unvalidated.
The [October 19 refresh](notes/track2-requirements-review-v33.md) corrects deletion
and confirmation to November 23 at cnb@sagebase.org. Frozen releases remain intact.

**Session 71: presentation and harness v32 integrate public Perturb-seq falsification.**
The [report](notes/track2-report-v32.md), [nine slides](notes/track2-slides-v32.html),
[335-word narration](notes/track2-pitch-v32.md) and [reviewer guide](notes/track2-reviewer-guide-v32.md)
include the completed [v31 RPE1/K562 analysis](notes/track2-perturbseq-v31.md).
A detectable BUB1B response does not qualify a specific disease surrogate. One shared
guide pair, selected controls and weak cross-cell matching strengthen the requirement
for independent restoration and relevant function before drug matching. All eight H100s
completed the calculation; the archive and local replay passed. There are 52 claim
records across six registers, with no drug, phase or exposure promotion.

**Session 70: presentation and harness v30 integrate the completed v29 research.**
The [report](notes/track2-report-v30.md), [nine slides](notes/track2-slides-v30.html),
[326-word narration](notes/track2-pitch-v30.md) and methods answers now include
ProteinMPNN control failures, endpoint-specific controls and held-out expression/QC
results. The [reviewer guide](notes/track2-reviewer-guide-v30.md) covers 47 claim records.
The [October 6 official refresh](notes/track2-requirements-review-v30.md) covers 26
public discussions and 79 visible comments. Later judging does not extend the October
24 submission deadline; the deletion deadline was corrected to November 23 in the October 19 refresh. No biological or delivery status
is promoted. Earlier releases remain preserved.

**Session 69: completed v29 structural and expression falsification on all eight H100s.**
The [new research addendum](notes/track2-orthogonal-v29.md) records 67,584 fixed-site
ProteinMPNN samples using Anthropic's toolkit and 400 held-out expression fits.
Structural controls pass only 1/24 primary and 0/24 expanded comparisons; backbone
sensitivity and an endpoint-specific D882N literature conflict limit interpretation.
HT29 agreement survives stricter adjustment and CRISPR QC restriction. MCF7 has no
QC-qualified BUB1B query. Drug decisions remain unchanged.

The [v29 reviewer guide](notes/track2-reviewer-guide-v29.md) covers 47 claim records,
complete provenance and the combined `scripts/check_track2_harness_v29.py` check.
At session 69, presentation v28 required the separate addendum. V30 now integrates
those results and preserves v28. All v29 GPU jobs have finished.

**Session 68: Track 2 v28 materials and harness are synchronized.** The
[report](notes/track2-report-v28.md), [nine slides](notes/track2-slides-v28.html),
[330-word narration](notes/track2-pitch-v28.md) and methods workbook integrate
completed v27 protein-background and expression-specificity research. HT29 retains
retrieval ranks 2–5; MCF7 BUB1B reversal weakens from 7 to 1,184 while MTOR stays first.
The [reviewer guide](notes/track2-reviewer-guide-v28.md) covers all 42 claim records.
No rescue priority or clinical margin is established. Earlier releases remain intact.

**Session 67 research remains frozen.** All eight H100s completed four protein models
and expression sensitivities. The [v27 record](notes/track2-falsification-v27.md) retains
full matrices, compute provenance, failed controls and favorable exceptions. Session 68
integrates those results without new GPU/model execution.

**Session 65: completed eight-GPU CRISPR falsification.** The
[v25 findings](notes/track2-crispr-v25.md) add 2,474,445,074 expression comparisons,
strengthening HT29 as an assay-qualification lead. Favorable MCF7 everolimus/MTOR
connections remain separate from its failed BUB1B model qualification. New source-well
checks detect regrouped old experiments under new IDs. One BUB1B guide and no joint
functional rescue mean no drug promotion. The
[v25 reviewer guide](notes/track2-reviewer-guide-v25.md) connects the full evidence,
validation changes and combined `scripts/check_track2_harness_v25.py` check.
Presentation v24 remains frozen; the later v26 materials integrate this addendum.

**Session 64: integrated presentation and harness.** The v24 report, nine-slide deck,
342-word script and methods export incorporate the v23 RNAi findings. Seed-associated
similarity, favorable HT29 evidence and finite-reference sensitivity now appear together,
with concrete model-qualification changes. New release checks bind both research
campaigns; earlier versions remain intact.

**Session 63: eight-GPU RNAi falsification.** The [v23 addendum](notes/track2-rnai-v23.md)
adds 1.54 billion pair comparisons and 5.84 million matched-control evaluations.
Seed and batch controls weaken unqualified target attribution. HT29 retains a favorable
signal, but finite-reference sensitivity removes the primary threshold crossings.
[Five new claim challenges](notes/track2-rnai-register-v23.json) and
[revised qualification controls](notes/track2-rnai-validation-v23.md) strengthen the
next experiment. GPU execution was bursty; no independent BUB1B experiment or drug
benefit is established. V22 presentation files remain frozen.

**Session 62: presentation update.** The v22 report, eight-slide deck and 337-word
narration give functional counterevidence its own slide and distinguish five decision
outcomes. Computational qualification is combined without losing the HT29 exception
or identity/QC limits. V21 science and all earlier releases remain unchanged.

**Session 61: falsification revision.** The [27-claim audit](notes/track2-falsification-review-v21.md)
adds primary counterevidence and favourable counterweights, challenges the uncalibrated
expression filter, and sharpens the [validation plan](notes/track2-validation-v21.md).
The [v21 ledger](notes/track2-evidence-v21.json) preserves every v15 drug disposition.
The proposed decision contract returns HOLD with unmeasured biology and null margins.
An invalid assay, imprecision, scoped futility and safety failure now have different
consequences. No wet-lab result, new model inference or candidate promotion is claimed.

**Track 2 (feat-009) is in progress.** Read the [integrated v43 report](notes/track2-report-v43.md)
and the complete [v19 research record](notes/track2-transcriptome-v19.md).
The [falsification review](notes/track2-falsification-review-v21.md) challenges the full
chain from genotype to useful function, tumour selectivity, exposure and safety.
No drug earns rescue priority; everolimus is an optional qualified mechanistic probe,
HCQ is reserve, phase is unconfirmed and clinical exposure margins are unknown.

The [27-claim register](notes/track2-falsification-register-v21.json) specifies support,
contrary evidence, falsifiers, stop/reopening rules and next actions. The new offline
checker distinguishes unresolved evidence from failed hypotheses and prevents model-only
or planned evidence from satisfying biological advancement gates. All-pass evidence
could permit only preclinical review. The software does not validate biology.

Two concrete findings change the narrative. All four newer protein models still pass
the original primary gate, but adding retained secondary controls breaks separation in
8/12 model/window comparisons; 11/24 retained-function scores are negative. This is
post-hoc sensitivity, not a new accuracy estimate. Visual inspection of the Balnis
supplement also confirms an unresolved 10 mM versus 10 micromolar discrepancy across
related ex vivo methods; the disputed concentration is quarantined. All original
results, narrow successes, prior failures and positive safety counterweights remain.

The [63-source/11-decision ledger](notes/track2-evidence-v15.json) and
[validation plan](notes/track2-validation-v21.md) add controls for growth-rate and
flux-reporter artifacts, missingness, meaningful-effect/safety bounds and delayed
injury. Synthetic examples demonstrate how fewer abnormal survivors can coexist with
worse useful output; they are explicitly not laboratory data. Bounded public searches,
Firecrawl failures, source identities, hashes and reading limits are archived.

The completed [earlier](notes/track2-model-expansion.md) and
[newer](notes/track2-latest-models.md) model campaigns are preserved. The newer campaign
contains 84 protein scores, 192 structures and 100 DNA comparisons. Impaired controls
fold confidently; ESM3 WT variability is large; BRCA1/Evo performance does not validate
BUB1B. No new GPU inference was needed for v15. BindCraft2 remains deferred without a
defined functional target and experimental validation route.

**Standing objective:** actively seek evidence that can falsify each consequential
assumption; revise or abandon the approach when warranted. Use the original
[falsification plan](notes/track2-falsification-plan.md) and current claim register
throughout research and before promotion/release. Apply the same standard to benefit,
harm and alternative candidates. Missing evidence and search failures are not disproof.

Current materials: [report source](notes/track2-report-v47.md),
[369-word narration](notes/track2-pitch-v46.md), [plain transcript](notes/track2-transcript-v46.txt),
[nine-slide deck](notes/track2-slides-v47.html) and
[video description](notes/track2-video-description-v46.md). The
[v41 literature addendum](notes/track2-literature-v41.md), the
[v43 TORC1-segregation addendum](notes/track2-literature-v43.md), [v45 checkpoint/computational-drug addendum](notes/track2-literature-v45.md) and their
[audits](notes/track2-literature-audit-v45.json) add public-source readout evidence
without changing drug decisions. The mechanism and four-arm drug experiment lead the presentation, followed by
the synthetic denominator example and completed optical comparison. Favorable BUB1B
morphology, failed practical neural gain, guide/plate sensitivity and missing mitotic
coverage remain distinct. All eleven methods answers and the 334-word abstract match
the workbook export. Prior scientific details remain in linked research records.

Start with the [combined v45 reviewer guide](notes/track2-reviewer-guide-v48.md). One
public CPU command checks integrated v47 materials and completed v19/v21/v23/v25/v27/v29/v31/v36 findings plus the v45 literature audit:

```bash
uv run --no-project python scripts/check_track2_harness_v47.py
```

It requires no subject files, data/results folders, keys, network, Git history or model
weights. The check verifies consistency, not biological efficacy. The versioned public
presentation reviewer and release/bundle scripts use v47, while the 369-word voice and
recording materials preserve v46 wording. Earlier versions remain available and bound
inputs stay unchanged. The [current artifact record](notes/track2-current.json),
[harness review](notes/track2-harness-review-v47.md) and `./init.sh` route current work.

The [v48 readiness note](notes/track2-owner-readiness-v48.md) lists exact current deliverables and outstanding recording,
runtime measurement, hosting, provider handling, distribution scope, live checks and
receipt. The full [v42 requirements refresh](notes/track2-requirements-review-v42.md) found
31 threads/89 visible comments/16 closed. Thread 32 permits a clearly labeled published-paper
example in the pitch; thread 31 documents a Synapse alternative; thread 29 reinforces
IRB/consent routing. The current anonymous [v44 deadline refresh](notes/track2-requirements-review-v44.md)
found the Space revision, all seven official files and the discussion number/status/title
listing unchanged at 31/16; it did not reread thread bodies. Delete and confirm to cnb@sagebase.org by November 23, as specified in
[the active deletion plan](notes/deletion-plan-v2.md). The new materials omit AF3/Atlas numerical
outputs and derived figures, which does not resolve CC BY scope for linked history.

The historical [baseline evidence ledger](notes/track2-candidates.json) assesses twelve
entries; the [v3 report](notes/track2-report-v3.md) and all earlier snapshots are preserved.
The historical [scientific/exposure review](notes/track2-final-review.md) assigned
everolimus a conditional priority and demoted hydroxychloroquine to reserve. V9 supersedes
the everolimus priority while preserving that review and its source record.
The 53-source review and [exposure ledger](notes/track2-exposure.json) establish no clinical
efficacy or therapeutic margin. No laboratory experiments or Track 2 upload have occurred.
The current pitch is updated; recording and a hosted URL remain outstanding. Earlier scripts are historical.
The [Firecrawl follow-up](notes/track2-firecrawl.md) exercised all 26 advertised MCP
tools and added eight independently checked source documents at explicitly limited
reading depths. Pralatrexate is a new fusion-positive RMS tumour-only horizon;
rapamycin/slippage evidence strengthens [cell-fate safety gates](notes/track2-validation-v3.md).
The baseline 53-source/12-candidate ledgers and historical v2 package remain unchanged.
V3 integrates Atlas and Fireworks-hosted GLM disclosure; self-hosting is not a guarantee
of local inference, zero retention or no training. No clinical exposure margin follows.
The [expanded GLM literature review](notes/track2-glm-review.md) now separates ten
topic comparisons and adversarial rereads from independent primary-source adjudication.
It adds PP2A/senescence/readthrough controls and TBX/azole/HDAC exposure checks, including
entinostat's jurisdiction-specific approval. Raw GLM errors and retrieval gaps are
explicitly retained; v4 integrates their verified findings without changing v3 package bytes.
The [authenticated AlphaGenome Atlas follow-up](notes/alphagenome-authenticated-results.md)
retrieved both candidate AVI scores and feature attributions. These mainly reuse
termination, AlphaMissense and conservation evidence; detailed molecular retrieval
remains incomplete. No phase, drug ranking or exposure conclusion changed. The addendum
records Google DeepMind API use and output terms separately from earlier disclosures.
The [offline merged-splicing lookup](notes/alphagenome-splicing-results.md) now fills
the aggregate-score gap: both candidates have small predicted effects, not evidence
of benignity or experimentally normal splicing. Tissue/junction detail remains missing.

Feat-001 through feat-006, including feat-005b targeted recall and feat-005c phase follow-up, are complete.
The local Track 1 draft has been checked against a
pinned copy of the official scorer and exact reference normalization. Feat-008 retains
only an independent receipt-archive task; [submission notes](notes/track1-submission.md)
distinguish local validation, owner attestation and receipt verification. This does not
block authorized Track 2 research. **Feat-007 is complete:** the repository is PUBLIC,
and authenticated/anonymous checks confirm all 13 retired objects are unavailable
while live-object controls succeed. Reachable history passes the disclosure audit.
See [the publication audit](notes/publication-audit.md) and
[Support correspondence record](notes/github-support-request.md).

**2026-09-08 Support update:** the owner supplied the 10:41 UTC reply associated with
ticket **4738585**. Independent purge and public-access verification pass. The fresh
submission preflight had no blockers. API identity alone did not establish portal
authentication; the owner subsequently reported submitting. Do not upload again merely
to obtain a receipt. No files were uploaded by the agent workflow. On 2026-09-08 the owner completed
the AI disclosure: OpenAI/Codex API tier, data not used for model training, and no other
AI providers at that time. Subsequent session-35 work uses Google DeepMind Atlas
precomputed predictions, as disclosed in the addendum above; the submitted Track 1
files remain unchanged. Session 37 additionally used Firecrawl with Fireworks-hosted
GLM for public-literature synthesis; the historical v40 disclosure names this route without
assuming additional-provider account settings. The earlier attestation does not claim zero retention; purge
was verified separately.

The data profile and first two analyses are complete — see `notes/data-profile.md`,
`notes/vcf-triage.md` and `notes/copy-number-screen.md` for measured results and exact
commands. The baseline is a 45× male genome with 5.01M variants at Ti/Tv 2.050, called by
Sentieon as a diploid germline SNV/indel set.

Three findings shape the plan. **The provided VCF contains no CNV or structural records.**
The corrected all-lane depth/BAF screen resolves the preliminary chr20 outlier as bias,
finds no joint support on chr22, and retains a credible low-level chr19 gain signal that
still requires orthogonal clinical confirmation. **There is no runs-of-homozygosity
signal in the coarse screen**, which does not exclude consanguinity or shorter ROH.
The challenge's public compound-heterozygous answer-key statement motivates the
working model of two different rare damaging alleles in one gene. The first genome-wide
triage ranks a BUB1B pair first. Targeted all-lane realignment screened supported
coding/splice, operational deep-intronic, repeat-adjacent and heterozygous structural calls,
then reconstructed same-gene novel/existing pairs. It found no additional BUB1B candidate;
read-backed phasing left both leading sites outside a supported phase block. Trans phase
remains unconfirmed.

The current ten-row draft is in gitignored `results/feat006/`. It has the exact official
schema, `PROBAND01`, `chr`-prefixed contigs, distinct descending EPCRs, and 20 alleles that
match the reference and are already minimal and left-aligned. Its local score of 100 rank
points and F-max 1.0 assumes that row 1 is the hidden truth; it verifies scorer behavior but
does not reveal the private answer key or validate the candidate biologically.

`notes/prior-knowledge.md` records the candidate genes considered before any data was
examined, and what the first pass did and did not do to that prior.
`notes/copy-number-screen.md` records the corrected screen, commands and limitations.

## Acknowledgement

Required in any output from this work:

> This work was made possible through the Hackathon, organized by Sage Bionetworks
> in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
> Evaluation, and Assessment Consortium for Science), with prize sponsorship from
> AWS and Anthropic. We are deeply grateful to the child and their family who
> generously contributed their data and their story to advance research into this
> rare disease. We acknowledge their trust in making this Hackathon possible.


## Current Track 2 state

The current revision, v47, integrates the external-review adjudication, explicit candidate selection, decision-contribution
table, four-arm experiment, primary endpoint/units, software-vs-biology boundary and v46 narration without
changing drug disposition.
Use `notes/track2-reviewer-guide-v43.md` and `notes/track2-owner-readiness-v43.md`.
Reproduce the literature check with `scripts/check_track2_literature_v45.py` and the combined harness with `scripts/check_track2_harness_v47.py`.
