# Progress

## 2026-08-26 — session 1: repo, harness, data

Done:
- uv project created (`uv init --bare`, python 3.12), `huggingface_hub[cli]` added.
- Harness: `AGENTS.md`, `feature_list.json` (7 real features), `init.sh`, this file.
- Safety: `.gitignore` blocks `data/ results/ logs/` and every genomic extension;
  `scripts/no_data_in_git.sh` is symlinked as the git pre-commit hook and refuses
  any commit touching those paths.
- `scripts/download_data.sh` (resumable) + `scripts/verify_data.py` (compares every
  local file against the remote HF tree by size; `--self-check` proves the checker
  fails on an empty dir).
- HF access confirmed: user `jvv7`, gated approval active, LFS download works.
- 85 GB download started in background at ~64 MB/s.

Verified: `verify_data.py --self-check` → `self-check ok`;
`no_data_in_git.sh` → `no-data-in-git: ok`.

Next: feat-002, extract HPO terms from the clinical docx once the download lands.

Open question for the user: whether to run heavy realignment (feat-004) on the
local A100s or sync to PrakashDGX_H2's H100s. Data stays local by default.

## 2026-08-26 - session 1 continued: download complete

- 84.99 GB / 11 files landed; `./init.sh` reports
  `COMPLETE: all files present at expected size`. feat-001 done.
- Repo pushed private to `Vijayavallabh/mva-hackathon-2026`, local git identity
  set to `Vijayavallabh <be23b041@smail.iitm.ac.in>` (the global config on this
  box belongs to a different user, so this had to be set per-repo).
- Instruction file is `AGENTS.md`; `CLAUDE.md` is a gitignored local symlink.
- Dropped the `hf_transfer` extra - deprecated upstream, replaced by
  `HF_XET_HIGH_PERFORMANCE=1` in `scripts/download_data.sh`.
- Disk after download: 3.3 TB free on /mnt/md0.

Next: feat-002, HPO terms from the clinical docx.

## Resume

Run `./init.sh` from a clean shell. It is the only setup step; it is idempotent
and safe to re-run at any point.

## 2026-08-28 — session 2: harness audit, verification gate closed

Audited the harness (harness-creator validator: 96/100). The validator named
`lifecycle` as the bottleneck; that was a keyword check. The real defect was in
verification and it was live:

- `init.sh` step 4 ran `verify_data.py || echo "..."`, so a failed integrity
  check printed its error and the script still exited 0 with `=== OK ===`.
  The definition of done says "`./init.sh` passes" — for the one check that
  guards 85 GB of subject data, it could not fail. Fixed: step 4 now exits 1.
  Proved with a stubbed failure (`false` in place of the verify call) -> exit 1.
- That hole was masking a real `INCOMPLETE`: `TRUNCATED README.md 5062/5076`.
  Cause: the dataset's own README instructs `--exclude "README.md"
  ".gitattributes"`, `download_data.sh` never passed it, and upstream edited
  README.md after our copy landed. Both files are repo metadata, not subject
  data. Now excluded in `download_data.sh` and skipped in `verify_data.py`.
  All 11 payload files were and are intact — no re-download needed.
- `feat-001`'s evidence string claimed "COMPLETE" while the repo reported
  INCOMPLETE. Re-recorded against today's real run.
- `no_data_in_git.sh` did not cover `logs/` although `.gitignore` does. Added.
  Proved: staging `logs/download.log` now makes the gate exit 1.

Verified: `./init.sh` -> `COMPLETE: all files present at expected size`, exit 0.

Next: feat-002, HPO terms from the clinical docx. Unchanged.

## 2026-08-28 — session 3: data screening, plan re-aimed

The harness was built before anyone opened the data or read the challenge's scoring code.
Screened both; several planning assumptions were wrong. No analysis was run and no candidate
variant was proposed — this session only re-aimed the plan. Numbers and commands are in
`notes/data-profile.md`, scoring rules in `notes/challenge-spec.md`.

**Two submission-breaking facts, previously recorded nowhere:**

- The VCF's contigs are **unprefixed** (`1`, `2`, `X` — reference is
  `..._no_chr.fasta`), but Track 1 submissions must be **`chr`-prefixed**. The published
  `evaluation.py` matches by exact tuple equality on `(chrom, pos, ref, alt)` and only
  `.strip()`s the contig. Submitting VCF coordinates straight through scores 0 and looks
  well-formed while doing it.
- `proband_id` must be **`PROBAND01`**, not the sample name `WGS_EX2312012`.

**What the data says:**

- VCF: Sentieon 202308.02 Haplotyper → GVCFtyper, GATK 4.2.4.0 hard filters (no VQSR),
  called 2025-02-05. 5,012,204 records, 94.6% PASS, mean DP 45.1, Ti/Tv 2.050, 88% dbSNP.
  116,485 records on alt/random/decoy contigs to drop.
- **No CNV, SV or symbolic-allele records exist in it** — genotypes are only `0/1`, `1/1`,
  `1/2`. Mosaic aneuploidy cannot appear in this file by construction.
- Sample is **male** (chrX depth ratio 0.565, chrX het 8.1%; already public via the
  challenge page's own image alt-text).
- **Zero runs of homozygosity** at 1 Mb resolution → no consanguinity → expect two different
  rare alleles rather than a homozygote. The challenge's `evaluation.py` independently states
  the answer key is compound-heterozygous.
- Aneuploidy screen is **inconclusive, not negative**. chrX at ratio 0.565 works as a positive
  control, so the method detects real copy-number change; no autosome shows a full trisomy.
  But chr16/17/19/20/21/22 rise together in depth ratio, het% and BAF deviation — a
  GC/mappability gradient. chr20 is the largest outlier on every column (ratio 1.039, het
  70.4%, het:hom 2.38 vs ~1.60, BAF dev 0.090) and cannot be separated from bias without
  GC-corrected read-depth binning.
- FASTQ: NovaSeq A01973 run 164, 4 lanes, 2×149 bp, Phred+33, one library. 4.83× compression,
  ~385 GB uncompressed; a single `zcat` took 6m56s, so decompression alone is ~1 h serial.
  L003 R1's index ends `…GGAGA` where the other lanes end `…GGAGC` — worth checking.
- Phenotype docx: probed structurally only, narrative not read. 380 words, and it **already
  carries 8 embedded `HP:#######` IDs** — feat-002 is ID extraction, not narrative inference.
  It names no karyotype, no prior genetic testing and no candidate gene, so the search stays
  genome-wide.

**Environment reality check:** no bioinformatics tooling is installed at all (no bcftools,
samtools, tabix, bwa-mem2, vep, gatk, pigz); `AGENTS.md` pointed at a `scripts/get_tools.sh`
and `tools/` that did not exist. Outbound network is open, so VEP cache / gnomAD / ClinVar /
`hp.obo` are fetchable. The box is contended: load avg 109 on 64 cores, 3 of 5 A100s busy.
3.3 TB free.

**Changes made:**

- `feature_list.json` rewritten, 7 → 11 features. feat-002 retargeted to HPO ID extraction.
  New feat-003 (toolchain + annotation resources), feat-006 (local scorer and submission
  conformance — never spend one of 6 attempts on a formatting bug), feat-007 (make this repo
  public, which every Track 1 submission requires, not just Track 2). The old aneuploidy
  feature split into feat-005a (cheap GC-corrected CN/BAF screen) and feat-005b (targeted,
  optional realignment justified by recovering a missed second allele rather than by
  aneuploidy detection).
- `AGENTS.md` rule 1 **narrowed rather than deleted**: raw subject data still never leaves
  the box, including into third-party model APIs; aggregate statistics, HPO IDs and labels,
  gene names and submission-bound candidate variants are explicitly permitted, on the basis
  of the organizers' own "code, models, and derived outputs" allowance. Added a "Data facts"
  block, fixed the dangling `get_tools.sh`/`tools/` reference, noted the repo goes public.
- New `notes/data-profile.md` and `notes/challenge-spec.md`. `notes/prior-knowledge.md` got
  a dated "checked against the data" section with the pre-data prior left intact.
  `notes/phenotype.md` restructured for the embedded HPO IDs.
- Git history audited before planning the public flip: 4 commits, 15 tracked files, nothing
  ever under `data/`, `results/` or `logs/`.

Verified: `./init.sh` → `COMPLETE: all files present at expected size`, exit 0.

Next: feat-002, extract the 8 embedded HPO IDs. feat-003 (toolchain) unblocks in parallel
and is the real prerequisite for everything after.

## 2026-09-01 — session 4: harness reliability maintenance

Re-ran the structural harness audit: 100/100 across instructions, state, verification,
scope, and lifecycle. Live bootstrap checks exposed two issues the structural score could
not detect:

- `uv.toml` and `init.sh` direct uv to the gitignored repository-local `.uv-cache/`, so
  startup and standalone verification do not depend on a writable global user cache.
- `verify_data.py --self-check` now uses a local fixture covering missing, truncated, and
  complete files. Only the real dataset-integrity check contacts Hugging Face.
- `session-handoff.md` no longer suggests starting feat-003 in parallel with feat-002;
  `feature_list.json` assigns the narrowly required `hp.obo` fetch to feat-002, and exactly
  one feature remains active.

Active feature and next step remain feat-002. This maintenance did not perform phenotype
work or change feature status/evidence.

Verified with `./init.sh` on 2026-09-01: `self-check ok`, `84.99 GB`,
`COMPLETE: all files present at expected size`, `=== OK ===`.

## 2026-09-01 — session 5: parent-directory authorization

- Recorded the user's standing authorization in `AGENTS.md`: agents may operate without
  additional permission anywhere below
  `/mnt/md0/IITM/BackUp/Home/vijayavallabh/`, including sibling repositories.
- Added the parent directory as a trusted project in `.codex/config.toml`.
- Preserved contractual subject-data restrictions and explicit-task requirements for
  destructive work, system-package installation, unusual remote pushes, and changes to
  uploaded submission deliverables.

This harness-only maintenance did not change feat-002 status or evidence.
