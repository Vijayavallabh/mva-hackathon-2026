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

Everything must be deleted by **24 Nov 2026** and confirmed by email —
see `notes/deletion-plan.md`. Full rules in `AGENTS.md`.

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

**Track 2 (feat-009) is in progress.** The [current v18 report](notes/track2-report-v18.md)
and [falsification review](notes/track2-falsification-review-v15.md) challenge the full
chain from genotype to useful function, tumour selectivity, exposure and safety.
No drug earns rescue priority; everolimus is an optional qualified mechanistic probe,
HCQ is reserve, phase is unconfirmed and clinical exposure margins are unknown.

The [19-claim register](notes/track2-falsification-register-v15.json) specifies support,
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
[validation plan](notes/track2-validation-v15.md) add controls for growth-rate and
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

Current materials: [six-page report source](notes/track2-report-v18.md),
[334-word narration](notes/track2-pitch-v18.md), [plain transcript](notes/track2-transcript-v18.txt),
[eight-slide deck](notes/track2-slides-v18.html) and
[video description](notes/track2-video-description-v18.md). The report leads with the
conditional approved-drug hypothesis, balanced evidence and a staged benefit/harm test.
The report is 27.18% shorter; the redesigned deck and rewritten pitch follow the
[official Track 2 brief](notes/track2-v18-brief-review.md), rechecked September 25.
It answers all eleven methods questions, including AI disclosure and a 166-word abstract.
The original methods workbook is also filled by the document exporter. Full
acknowledgement and historical model notices remain. The [readiness note](notes/track2-owner-readiness-v18.md)
retains recording/hosting, provider handling, unresolved distribution scope, owner/live
checks and receipt. These drafts do not establish a wet-lab result or an upload.

Start with the [reviewer guide](notes/track2-reviewer-guide-v18.md). Its public CPU check
needs no subject files, data/results folders, keys, network or model weights:

```bash
uv run --no-project python scripts/track2_public_review_v18.py
```

Use `scripts/track2_release_v18.py` for new research snapshots; the reviewer guide
documents PDF/workbook/slide regeneration and separates historical integrity checks.
All v1–v17 bound inputs/releases and submitted Track 1 v4 are preserved.
The [current-artifact record](notes/track2-current.json) and
[harness review](notes/track2-harness-review-v18.md) route the current work.
`./init.sh` checks artifact versions, narration, original models, new falsification
results and unresolved scientific/delivery status. The [official review](notes/track2-official-requirements-review-20260924.md)
checks live revision aeeef5ad49f51204a7439352e59e9d310aee5e9e; the
[community review](notes/track2-community-review-20260924.md) covers all 24 public
discussions and 68 latest visible comments. Rigor/impact/innovation/scalability receive
35/25/25/15 percent; hypotheses are permitted and three entries/latest-only applies.
No authenticated portal action occurred here. Current materials omit AF3/Atlas numerical
outputs and derived figures; this does not itself resolve CC BY scope for linked history.

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
GLM for public-literature synthesis; the current v18 disclosure names this route without
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
