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
  innovation (25%), scalability (15%). One submission.

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
first Track 1 submission, which requires a GitHub URL.

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
| `progress.md` | Session log |

## Status

Feat-001 through feat-006, including the optional feat-005b targeted recall, are complete.
The local Track 1 draft has been checked against a
pinned copy of the official scorer and exact reference normalization. The next feature is
feat-007: remove the two protected-text overlaps from reachable history, re-audit, and only
then make the repository public. That history rewrite must be explicitly authorized before
it runs.

The data profile and first two analyses are complete — see `notes/data-profile.md`,
`notes/vcf-triage.md` and `notes/copy-number-screen.md` for measured results and exact
commands. The baseline is a 45× male genome with 5.01M variants at Ti/Tv 2.050, called by
Sentieon as a diploid germline SNV/indel set.

Three findings shape the plan. **The provided VCF contains no CNV or structural records.**
The corrected all-lane depth/BAF screen resolves the preliminary chr20 outlier as bias,
finds no joint support on chr22, and retains a credible low-level chr19 gain signal that
still requires orthogonal clinical confirmation. **There is no runs-of-homozygosity
signal**, so with the challenge's public compound-heterozygous answer-key statement, the
working model is two different rare damaging alleles in one gene. The first genome-wide
triage ranks a BUB1B pair first. Targeted all-lane realignment found no additional BUB1B
coding/splice or high-quality window-overlapping structural allele, and read-backed phasing
left both leading sites outside a supported phase block. Trans phase remains unconfirmed.

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
