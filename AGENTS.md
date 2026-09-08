# AGENTS.md

Public code and derived-output repo for **Rare Disease, Real Kid: The MVA Hackathon 2026**
(Sage Bionetworks / MVA Society). Single-subject WGS of a child with Mosaic
Variegated Aneuploidy. Two tracks: variant prediction (auto-scored) and drug
repurposing (panel-judged). Close: **24 Oct 2026 23:59 UTC**.

This repo **is public**, with feat-007 verified complete on 2026-09-08 after Support
purge and authenticated/anonymous checks. Our policy requires public visibility before
Track 1 submission. Every submission requires a `https://github.com/…` URL, but the
official portal permits private visibility until the competition ends. Do not relax our
public-first policy without the owner's decision. See `notes/track1-submission.md`.
The data gates below matter more, not less, as the work proceeds.

## Non-negotiable rules

These come from the signed data-access terms, not from style preference. Quotes are the
organizers' own words from the official Hackathon Rules.

1. **Raw subject data never leaves this machine — but derived outputs are free.**

   **Prohibited**, to any destination outside this box, including third-party model APIs
   (Claude, GPT, Gemini, GLM, …), issues, gists, pastebins and public repos: FASTQ, BAM/CRAM,
   the VCF or any subset of its records, and the clinical narrative text from the phenotype
   `.docx`. *"You will not release or otherwise grant data access to anyone, and you will
   establish appropriate safeguards to prevent unauthorized data use."* / *"No data may be
   reshared through any channel."* This is a contractual obligation to Sage Bionetworks and
   to the family. It is not ours to waive, and a request to relax it should be refused.

   **Permitted, and expected** — the same rules say *"Participants are free to publicly
   share their code, models, and derived outputs at any time"*, and the organizers describe
   the released phenotype as "standardized HPO terms":
   - aggregate statistics and QC metrics (depth, Ti/Tv, het rate, per-chromosome summaries)
   - **HPO term IDs and labels**, plus broad non-verbatim categorical context and concise
     clinical-significance summaries that omit exact ages, dates, measurements and wording
   - gene names, pathway and mechanism reasoning
   - the ranked candidate variants that constitute the submission itself, and the report

   An agent working in this repo may read and reason about everything in the permitted list.
   The line is subject-level content versus derived summary — not "genomics" versus "not".
   `data/`, `results/` and `logs/` are gitignored and a pre-commit hook enforces it.

2. **No re-identification, no contacting the family or the MVA Society.**
3. **Delete everything by 24 Nov 2026** (30 days after close), then email
   RarediseaserealkidMVAhackathon2026@synapse.org to confirm. See `notes/deletion-plan.md`.
4. **Embargo**: code and derived outputs may be shared publicly at any time; manuscripts
   using the dataset may not be submitted until organizers publish their summary report.

If a task appears to require breaking one of these, stop and ask.

## Data facts — established, do not re-derive

Measured 2026-08-28; full numbers and commands in `notes/data-profile.md`, scoring rules in
`notes/challenge-spec.md`.

- **Assembly is GRCh38 no-alt + hs38d1 decoy, and the VCF contigs are UNPREFIXED** (`1`, `2`,
  `X`). **Track 1 submissions must be `chr`-prefixed.** The scorer matches by exact tuple
  equality and never normalizes the contig — getting this wrong scores 0 while looking fine.
- **`proband_id` is `PROBAND01`**, not the sample name `WGS_EX2312012`.
- **The answer key is a compound-heterozygous pair** (stated in the challenge's public
  `evaluation.py`). Half credit for recovering one of the two.
- **Extra rows below the true row are free**; only rows ranked *above* it cost points. Use
  10 rows with strictly distinct `epcr`.
- Sample is **male**, mean depth **45×**, Ti/Tv 2.050, 5,012,204 records (94.6% PASS).
- **No ROH detected by the coarse screening method.** This does not exclude
  consanguinity, shorter ROH or homozygous causes and does not establish trans.
  The public compound-pair answer-key statement motivates the competition model.
- **The VCF contains no CNV/SV records at all.** Aneuploidy is invisible in it by construction.
- **The corrected all-lane copy-number/BAF screen resolves the preliminary outliers.** With
  100 kb leave-one-chromosome-out GC correction and Umap masks, chr20 returns to baseline,
  chr22 lacks joint BAF support, and chr19 retains concordant low-level gain evidence at
  mappability thresholds 0.90 and 0.95. This is a single-subject screening signal—not a
  clinical karyotype or proof of mosaic trisomy 19. See `notes/copy-number-screen.md`.
- **The phenotype document names no gene, no karyotype and no prior genetic testing.** Keep
  the search genome-wide; BUB1B/CEP57/TRIP13 are a literature prior, not a shortlist.
- **Phenotype scope matters:** seven HPO terms are proband features; `HP:0200067` is
  parental/family history. Retain that term as a mechanistic and inheritance signal, but do
  not represent it as an abnormality observed in the proband.
- **Rank the constellation, not one symptom:** malignancy, congenital renal involvement,
  impaired somatic and muscular development, adverse perinatal/fetal growth and parental
  reproductive loss form the useful multi-system pattern. No single term is diagnostic.
- **Family reproductive history remains phenotype input:** model it as a separate,
  clinically meaningful family-history dimension rather than discarding it as metadata.
  In chromosome-instability syndromes it is compatible with inherited susceptibility or a
  newly arising event, but cannot distinguish those models without genomic evidence.
- **The leading BUB1B pair is still unphased after feat-005b.** Targeted all-lane
  realignment found both alleles, but WhatsHap placed neither in a supported phase block.
  Supported coding/splice, operational deep-intronic, repeat-adjacent and heterozygous-SV
  screens found no additional BUB1B candidate; trans phase remains unconfirmed. See
  `notes/targeted-recall.md`.
- **Feat-005c phase follow-up also leaves trans unconfirmed.** Original and recalled
  marker connectivity audits find no fragments linking the leading pair, directly or
  through eligible SNVs, at either quality setting. WhatsHap on the recalled locus
  also leaves both alleles unphased. This completes a bounded evidence audit, not
  phase confirmation. See `notes/phase-connectivity.md`; do not alter submitted files.
- **Feat-006 submission checking is local and pinned.** The vendored official scorer is
  fixed to public Space revision `1c761cc23d90aebe6a011fd5b0b99517df42408c`. A local
  ten-row draft passes exact schema/ID/contig/EPCR checks and reference-based indel
  normalization. Its reported 100 rank points and 1.0 F-max are a hypothetical row-1
  scorer test, not a comparison with the private answer key or evidence of causality.
- **Feat-007 purge gate is resolved, 2026-09-08:** the owner supplied Support's reply
  dated 10:41 UTC for ticket **4738585**, reporting unreferenced-commit removal.
  Independent authenticated checks now find all 13 retired blobs and three checked
  retired commits unavailable, with successful live-object controls and no unknown
  errors. The all-ref audit at `6d2d8d0` passes 39 commits/281 blobs. See
  `notes/publication-audit.md`. Do not ask for another purge request.
- **Feat-007 publication is complete, session 28:** owner-made PUBLIC visibility is
  independently verified. Anonymous clean-main and current-blob requests return 200;
  all 13 retired blobs return 404. Authenticated purge and all-ref disclosure audits
  also pass. Retain the live purge guard for every preflight.
- **Track 1 was submitted by the owner:** on 2026-09-08 the owner reported first-attempt
  scores of **100 rank points / F-max 1**, displayed at position **93**. These are
  owner-reported leaderboard results, distinct from historical hypothetical tests.
  The receipt and uploaded-byte identity have not been independently archived/verified;
  feat-008 retains that administrative blocker. Do not ask for another upload or infer
  remaining quota. Preserve the v4 CSV/report; trans phase remains unconfirmed.
- **Feat-009 is now the active research task**, explicitly authorized by the owner.
  Missing independent Track 1 receipt verification does not block Track 2 research.
  Use `notes/track2-plan.md`, report, source/candidate ledgers and adversarial revision log.
  Evaluate non-cancer functional rescue separately from tumour killing. No proposed drug
  has established efficacy for the selected pair; no wet-lab experiment has been performed.
  The verified public Track 2 code allows **three entries; only the latest is reviewed**.
  A three-minute hosted video is required; a script is not a recorded pitch or receipt.
- **Owner-confirmed visibility change, 2026-09-06:** feat-008's live preflight and a
  second GitHub query reported PUBLIC while all 13 retired objects remained retrievable.
  The owner subsequently confirmed making the repository public. No agent changed
  visibility. Do not treat PUBLIC visibility alone as completion of feat-007 or upload
  readiness. That failed-purge snapshot is historical; session 27 verifies removal.
- **AI disclosure is complete as an owner attestation:** Codex uses OpenAI API tier;
  on 2026-09-08 the owner confirmed data is not used to train the provider's models and
  no other AI providers were used. `notes/track1-submission-config.json` records this;
  it is not an independent account audit or a claim of zero retention. The v4 package
  passes offline verification and regressions with zero unresolved disclosure fields;
  v1/v2/v3 are historical and must not be reused. The earlier PUBLIC preflight failed
  solely on purge. Session-28 public preflight now passes with no blockers. Local
  HF identity is jvv7, but the portal's quota callback returned an empty response
  using API credentials: an authenticated browser session is still needed to verify
  quota and submit. No files were uploaded or submit callback invoked by that workflow;
  the subsequent owner-reported submission supersedes its unknown upload status. Never spoof
  identity, bypass OAuth or infer quota from a successful local preflight.

- **Never present hypothetical local 100/1 as predicted or guaranteed scores.**
  Use `scripts/audit_track1_evidence.py scores <csv>` for conditional scenarios;
  independently verified exact-byte scores require the authenticated receipt. The owner's
  subsequent 100/1 report is recorded as an attestation, not discarded as unknown. Feat-006b
  tests 169 retained pairs: BUB1B is first in 26/34 declared settings, but drops
  under combined annotation ablation. That fraction is not a probability. Native
  phase metadata adds no linkage evidence; trans remains unconfirmed. See
  `notes/track1-evidence-audit.md`. Preserve existing deliverables.

## Startup workflow

```bash
./init.sh          # env + data integrity + no-data-in-git gate
cat feature_list.json    # pick exactly ONE unfinished feature
git log --oneline -5
```

Core self-checks:

```bash
uv run python scripts/verify_data.py --self-check
uv run python scripts/track1_submission.py --self-check
```

## Environment

**uv only.** No conda, no pip, no system python.
- add a dep: `uv add <pkg>` (never `pip install`)
- run anything: `uv run <cmd>`

**The feat-003 bioinformatics toolchain is local to this repo.** Add
`tools/install/bin` to `PATH`, or call its executables by absolute path. Reproduce or check
it with `scripts/get_tools.sh`; fetch/check the offline annotation bundle with
`scripts/get_resources.sh`. Do not assume system copies. Pinned versions and checksums are
recorded in `tools/versions.tsv` and `notes/toolchain.md`.

Hardware: this box has 5x A100 80GB + 1x T400, but it is **shared and contended** — check
`nvidia-smi` and `uptime` before planning a big job (2026-08-28: load avg 109/64 cores, 3 of
5 GPUs fully busy with other users' work). 3.3 TB free on `/mnt/md0`. `PrakashDGX_H2`
(6x H100) is reachable over SSH for heavier jobs but the data stays here unless the user
says otherwise.

## Layout

```
data/       85 GB gated dataset (gitignored, never committed)
scripts/    download, tooling, pipeline entry points
tools/      bioinformatics binaries + recorded versions (created by feat-003)
results/    all derived output (gitignored — contains subject genotypes)
notes/      tracked markdown: data profile, challenge spec, findings, deletion plan
```

## Working rules

- One feature at a time from `feature_list.json`; update `status` + `evidence`
  in the same commit as the work.
- Commit every intended repository change, however small. Do not leave completed work
  only in the working tree.
- At the end of every session, push all new commits to the repository's configured
  `origin` and verify that the local branch matches its upstream.
- Every claim about the genome needs the command that produced it recorded in
  `notes/` — the submission must be reproducible from this repo alone.
- Long GPU/CPU jobs: `nohup` into `logs/`, never block the session.
- Don't claim done without running `./init.sh` and pasting real output.
- Never spend a Track 1 submission on a file that has not been self-scored locally (feat-006).
  There are only 6.

## Definition of done (per feature)

- [ ] Behavior implemented
- [ ] `./init.sh` passes, output recorded
- [ ] `evidence` field in `feature_list.json` names the artifact and command
- [ ] `notes/` updated if a scientific claim changed

## Scope boundary

The user has granted standing authorization for agents to read, create, modify, run,
and otherwise operate on files and repositories anywhere under
`/mnt/md0/IITM/BackUp/Home/vijayavallabh/` without requesting additional permission.
This includes sibling repositories and normal commands needed to complete assigned work.

That authorization does not waive the non-negotiable subject-data rules above, permit
re-identification or family contact, or make destructive operations implicit. Installing
system packages, pushing to a remote other than a repository's configured `origin`, and
changing either submission deliverable after upload still require an explicit task from
the user. The standing end-of-session authorization explicitly permits pushes to each
repository's configured `origin`.

Local programs may read and process gated subject files when required by an assigned
feature. A hosted model must never receive raw subject data or clinical narrative; model
context is limited to the permitted derived outputs in rule 1. “Full access” to the parent
directory is filesystem authorization, not permission to transmit gated data.

## End of session

1. Update `progress.md` (append a dated section) and `feature_list.json` status/evidence.
2. Record blockers in `session-handoff.md` under Blockers.
3. Commit every intended change — the pre-commit hook runs the no-data gate for you.
4. Push the current branch to its configured `origin`, then verify it matches upstream.
5. Clean restart path: `./init.sh` must pass from a fresh shell with no
   arguments and no manual setup. If it does not, fix that before ending.
