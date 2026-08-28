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

Everything must be deleted by **24 Nov 2026** and confirmed by email —
see `notes/deletion-plan.md`. Full rules in `AGENTS.md`.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and a Hugging Face account approved for
`SageBio/mva-hackathon-2026-data`.

```bash
hf auth login                 # or export HF_TOKEN
./scripts/download_data.sh    # 85 GB into data/, resumable, ~25 min at 60 MB/s
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
| `scripts/` | `download_data.sh`, `verify_data.py`, `no_data_in_git.sh` |
| `tools/` | Bioinformatics binaries and recorded versions (created by feat-003) |
| `notes/` | Tracked markdown: data profile, challenge spec, prior hypotheses, HPO terms, deletion plan |
| `results/` | Derived output. Gitignored — contains subject genotypes. |
| `AGENTS.md` | Working rules, access terms, established data facts, definition of done |
| `feature_list.json` | Source of truth for what is done |
| `progress.md` | Session log |

## Status

feat-001 done: dataset downloaded and verified, 84.99 GB across 11 files.
feat-002 next: extract the HPO terms already embedded in the clinical phenotype document.

The data has been profiled but not yet analyzed — see `notes/data-profile.md` for the
measured baseline and the exact commands. In short: a 45× male genome, 5.01M variants at
Ti/Tv 2.050, called by Sentieon as a diploid germline SNV/indel set.

Two findings shape the plan. **The provided VCF contains no CNV or structural records at
all**, so MVA's defining mosaic aneuploidy cannot appear in it; a quick depth/BAF screen
excludes high-level aneuploidy but leaves low-level mosaicism (chr20 is the largest outlier)
unresolved and confounded with GC bias — that needs GC-corrected read-depth binning, not a
full re-call. And **there is no runs-of-homozygosity signal**, so with the challenge's own
scoring code stating a compound-heterozygous answer key, the working model is two different
rare damaging alleles in one gene. Realignment of the FASTQ lanes is kept as a targeted,
optional step aimed at recovering a second allele the germline caller could have dropped.

`notes/prior-knowledge.md` records the candidate genes considered before any data was
examined, and what the first pass did and did not do to that prior.

## Acknowledgement

Required in any output from this work:

> This work was made possible through the Hackathon, organized by Sage Bionetworks
> in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
> Evaluation, and Assessment Consortium for Science), with prize sponsorship from
> AWS and Anthropic. We are deeply grateful to the child and their family who
> generously contributed their data and their story to advance research into this
> rare disease. We acknowledge their trust in making this Hackathon possible.
