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

## 2026-09-01 — session 6: commit-and-push policy

- Added a standing rule to commit every intended repository change, including tiny edits,
  and push all session commits to the configured `origin` after verification.
- Clarified that local tools may process gated inputs for assigned work, while hosted
  models remain limited to permitted derived outputs. Filesystem authorization cannot
  override the signed prohibition on data resharing.

This harness-only maintenance did not change feat-002 status or evidence.

## 2026-09-02 — session 7: local genomics teaching workspace

- Split the introductory data explanation into 12 short HTML lessons for a learner with
  AI, deep-learning, and statistics experience but no biology background.
- Added a local mission, curated primary resources, shared printable styling, an
  AI-to-genomics glossary, learner notes, and a prior-knowledge learning record.
- Added all teaching-workspace paths to `.gitignore` at the user's request. The lessons
  use synthetic examples and safe aggregate facts only; no protected VCF records or
  clinical narrative are present.
- Validated all 13 HTML files and their local navigation: zero broken local links.

This educational side task did not perform feat-002 phenotype extraction or change any
feature status/evidence. The active feature remains feat-002.

## 2026-09-02 — session 8: feat-002 HPO extraction

- Added `scripts/extract_hpo.py`, a standard-library pipeline that reads only
  `word/document.xml` inside the protected DOCX, retains embedded `HP:#######` identifiers,
  resolves labels from the official HPO OBO file, and writes only permitted derived output.
- Added a synthetic `--self-check` covering document-order extraction, deduplication,
  ontology lookup, and the disclosure boundary: surrounding example prose must not appear
  in the report.
- Fetched `hp.obo` release `2026-06-23` into gitignored `data/resources/`; recorded its
  source URL and SHA-256 in `notes/phenotype.md`.
- The real local run resolved all 8 embedded IDs. No narrative was printed, tracked, or
  sent outside this machine. The existing negative structural probe remains the basis for
  keeping the search genome-wide.

Verified: `uv run python scripts/extract_hpo.py --self-check` passed and
`uv run python scripts/extract_hpo.py` wrote 8 terms. Final `./init.sh` output:

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
85.00 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== OK ===
exit=0
```

Next: feat-003, toolchain and annotation resources.

## 2026-09-02 — session 9: Presentation/Notes context signals

The user explicitly requested that feat-002 include the combined Presentation/Notes
column rather than only its HPO IDs, so feat-002 was briefly reopened and feat-003 remained
queued.

- Extended `scripts/extract_hpo.py` to locate the combined Presentation/Notes table column
  and reduce each protected cell to a fixed vocabulary of broad lexical signals: proband or
  family context, prenatal/perinatal/postnatal timing, and quantitative, diagnostic,
  treatment, or longitudinal information type.
- The tracked output contains no source wording, ages, dates, measurements, or numeric
  values. A mixed proband/family result is retained as ambiguity rather than automatically
  assigning that phenotype or turning it into a ranking weight.
- Expanded the synthetic self-check to use a real WordprocessingML table and prove that
  protected example phrases do not appear in the generated Markdown.
- The real run classified all 8 HPO rows and wrote the safe signals to
  `notes/phenotype.md`.
- Two-axis review tightened the implementation: Word XML reading is shared between stages,
  postnatal timing now requires explicit postnatal language rather than generic diagnosis
  words, and the synthetic test explicitly rejects source phrases, numbers, dates, and
  measurements. A local four-word overlap audit across all 8 protected cells and the public
  note returned `verbatim_4word_overlap=0` without printing either source.

Final verification:

```text
self-check ok: IDs and context signals resolved; protected text not emitted
wrote /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/notes/phenotype.md with 8 HPO terms
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
85.00 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== OK ===
exit=0
```

Next: feat-003, toolchain and annotation resources.

## 2026-09-02 — session 10: reviewed phenotype context and harness update

The user provided explicit interpretation of the protected Presentation/Notes column and
asked that the durable harness and relevant analysis documents reflect it. The source prose
and exact quantitative details were not copied into tracked files.

- Replaced keyword-only context signals in `scripts/extract_hpo.py` with a reviewed,
  categorical mapping. Seven HPO terms describe PROBAND01; `HP:0200067` is retained
  separately as parental/family-history evidence. The script verifies that every expected
  ID still has a populated source row and detects ID-set or empty-row drift. Wording-only
  changes require a fresh human review.
- Recorded only broad timing and phenotype domains. Exact ages, dates, measurements and
  narrative wording remain local and untracked.
- Updated `AGENTS.md`, `feature_list.json`, `notes/data-profile.md`,
  `notes/prior-knowledge.md`, `notes/phenotype.md`, and `session-handoff.md`. Future ranking
  must use the whole multi-system constellation while preventing the family-history term
  from being represented as a proband observation.
- Harness validation remains **100/100**. A local privacy audit found
  `diff_verbatim_6word_overlap=0` across all protected Presentation/Notes rows and the
  tracked diff.
- Two-axis review corrected an overclaim: the script detects changed ID sets and empty
  context rows, not wording-only edits. It also replaced free-form subject scope with an
  enum and derives analysis role from that scope, preventing contradictory combinations.

Final verification:

```text
self-check ok: IDs and reviewed context resolved; protected text not emitted
wrote /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/notes/phenotype.md with 8 HPO terms
Harness validation: 100/100
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
85.00 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== OK ===
exit=0
```

Next: feat-003, toolchain and annotation resources.

## 2026-09-02 — session 11: complete privacy-safe phenotype semantics

The user clarified that the categorical table still omitted analysis-relevant meaning.
Expanded `PhenotypeContext` with concise, non-verbatim clinical significance for every
row: the investigation trigger, congenital renal involvement, growth relative to expected
context, persistent early growth/muscle impairment, co-occurring muscle loss, substantial
prematurity, severe fetal growth restriction, and recurrent parental loss preceding the
proband.

The source wording and exact quantitative details remain excluded. The extractor now
rejects any three-word overlap against both protected narrative-bearing table columns.
`AGENTS.md`, feat-002 evidence and the session handoff now explicitly route future agents
to the richer safe summary in `notes/phenotype.md`.
- Standards review found that safe content was manually verified but not enforced at
  runtime. The extractor now rejects digits/measurement units and any three-word overlap
  between reviewed summaries and the protected Clinical Feature or Presentation/Notes
  cells; the synthetic self-check exercises both rejection paths.
- A stricter follow-up review found two shorter source fragments that the initial six-word
  audit missed. Both were paraphrased; validation now checks three-word sequences across
  both narrative-bearing columns.
- Final current-tree audit, excluding explicitly permitted HPO labels:
  `current_tree_non_hpo_verbatim_3word_overlap=0`.
- Reachable-history audit found one affected commit (`05ed1cc`, two short overlaps). The
  current tree is clean, but feat-007 is now blocked from making the repository public until
  an explicitly authorized history rewrite and force-push removes that commit content.

Final verification:

```text
self-check ok: IDs and reviewed context resolved; protected text not emitted
wrote /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/notes/phenotype.md with 8 HPO terms
Harness validation: 100/100
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
85.00 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== OK ===
exit=0
```

Next: feat-003, toolchain and annotation resources.

## 2026-09-02 — session 12: phenotype interpretation policy

Closed the remaining semantic gap in the derived guidance. `notes/phenotype.md` and the
durable harness now state that the reproductive-history annotation is a clinically
meaningful dimension of phenotype input, not disposable metadata. It remains scoped to
family history rather than being represented as a PROBAND01 abnormality.

For chromosome-instability hypotheses, that family feature is compatible with inherited
susceptibility or a newly arising causal event; it cannot discriminate between them without
genomic evidence. Ranking guidance continues to prioritize the cross-system pattern over
any individual manifestation. Protected source wording remains excluded.

Final verification: extractor self-check passed; harness validation remained `100/100`;
`current_tree_non_hpo_verbatim_3word_overlap=0`; `./init.sh` returned:

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
85.00 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== OK ===
```

Next: feat-003, toolchain and annotation resources.

## 2026-09-02 — session 13: feat-003 toolchain and offline annotation bundle

- Added resumable, pinned local installers for bcftools/samtools/htslib 1.24, bwa-mem2
  2.2.1, pigz 2.8, VEP 116, GATK 4.7.0.0, Nextflow 26.04.6 and Temurin Java 17.0.20.1.
  No system package, conda or pip installation was used.
- Built the VCF-header reference deterministically from NCBI's GRCh38 no-alt + hs38d1
  analysis set and GIAB's T2T v2 exclusions, then removed leading `chr` prefixes. All
  5,012,204 VCF records match the resulting FASTA; REF mismatches: zero.
- Installed the Ensembl VEP 116 indexed GRCh38 cache, whose metadata confirms gnomAD exome
  and genome frequencies v4.1; pinned ClinVar GRCh38 release 20260822; reused HPO release
  2026-06-23. Exact sources and SHA-256 values are in `tools/resources.tsv`.
- Added a bounded parallel range downloader after Ensembl throttled a single connection.
  Chunk sizes and successful tar extraction guard the reassembly; incomplete downloads are
  never marked complete.
- Verified offline VEP on public benchmark rs699 with both gnomAD frequency flags:
  `gnomADe_AF=0.458` and `gnomADg_AF=0.5782`. No subject coordinate was sent to an
  external service.
- Updated `init.sh` so clean restart now checks the toolchain and resource bundle as well as
  the environment, disclosure gate and dataset integrity.

Final `./init.sh` output:

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
84.99 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== 5. local bioinformatics toolchain ===
bcftools 1.24
samtools 1.24
tabix (htslib) 1.24
2.2.1
pigz 2.8
Picard Version: 3.5.0
      version 26.04.6 build 12646
openjdk version "17.0.20.1" 2026-08-18
=== 6. offline annotation resources ===
annotation resources ready
=== OK ===
```

Next: feat-004, the VCF triage and annotation baseline.

## 2026-09-02 — session 14: feat-004 VCF triage baseline

- Added a fully offline, checkpointed triage pipeline: PASS primary-contig filtering,
  biallelic normalization against the exact reference, exact-allele ClinVar annotation,
  Ensembl exon±20 bp intersection, VEP 116 coding/splice annotation and phenotype-aware
  candidate ranking.
- Added the pinned Ensembl 116 GTF, deterministic exon-window builder and HPO
  gene-to-phenotype release asset. Resource SHA-256 values are locked in
  `tools/resources.tsv`.
- The full run started from 5,012,204 records: 4,661,873 met PASS+primary criteria;
  normalization produced 4,727,745 biallelic records; exon windows retained 308,080; VEP
  yielded 29,701 coding/splice records. Ranking retained 418 rare damaging alleles across
  366 genes, generating 169 compound-pair and 195 dominant-singleton hypotheses after the
  review-corrected complete within-gene enumeration.
- The leading genome-wide compound hypothesis is BUB1B, comprising one stop-gained and one
  missense allele. Both are independent PASS 0/1 calls with DP/GQ 46/99 and 28/99 and
  balanced allele depth. The stop allele has non-conflicting ClinVar pathogenic support;
  the missense allele is absent from queried gnomAD fields and has concordant damaging
  SIFT/PolyPhen predictions. Phase remains unknown.
- The phenotype score averages all seven proband terms. `HP:0200067` is scored separately
  as family history; it contributes zero to the leading BUB1B score, proving the scope
  separation did not manufacture the result. Candidate output explicitly converts local
  unprefixed contigs to submission-style `chr` names.
- A live resource snapshot showed 465 GB available RAM and 3.75 TB free disk. CPU use was
  capped at eight workers on the shared 64-core host; no GPU or remote annotation service
  was used.
- Two-axis review tightened the baseline before handoff: ClinVar now requires exact allele
  matching; compound pairs are exhaustively enumerated rather than capped per gene; family
  history has the same coefficient under both inheritance hypotheses; explicit
  zero-frequency HPO associations are excluded; and stage checkpoints bind the pipeline
  code plus tool-version manifest. Shared allele rendering and typed model identifiers also
  remove the review's two maintainability smells.

Verification included `uv run python scripts/build_coding_regions.py --self-check`,
`uv run python scripts/rank_candidates.py --self-check`, Ruff checks, the complete local
pipeline, independent source-VCF re-query of the ranked pair, and final `./init.sh`.

Final `./init.sh` completed on 2026-09-03:

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
84.99 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== 5. local bioinformatics toolchain ===
bcftools 1.24
samtools 1.24
tabix (htslib) 1.24
2.2.1
pigz 2.8
Picard Version: 3.5.0
      version 26.04.6 build 12646
openjdk version "17.0.20.1" 2026-08-18
=== 6. offline annotation resources ===
annotation resources ready
=== OK ===
```

Next: feat-005a, GC-corrected copy-number and BAF screen.

## 2026-09-03 — session 15: feat-005a corrected copy-number and BAF screen

- Added a pinned GRCh38 Umap k=100 multi-read mappability asset and integrated checksum
  verification into the resumable offline resource installer.
- Added a checkpointed, all-lane pipeline that builds exact-reference 100 kb GC and
  mappability bins, streams BWA-MEM2 alignments through mate fixing, coordinate sorting and
  duplicate removal, and counts MAPQ≥30 primary aligned bases without retaining a BAM.
- The real run examined 938,213,206 SAM records, accepted 868,096,455 records and counted
  127,162,165,520 aligned bases. The primary analysis retained 25,883 autosomal bins,
  2,110,700 high-quality heterozygous SNVs and 25,767 populated 100 kb BAF bins.
- Replaced the preliminary 10 Mb comparison with leave-one-chromosome-out 0.5%-GC median
  curves, mappability/ACGT masks, sampling-variance-corrected BAF and deterministic 2,000-
  replicate chromosome-stratified 1 Mb block bootstraps. Each replicate jointly refits the
  target, GC model/normalizer and leave-target-out BAF baseline. Repeated the analysis at
  mappability thresholds 0.90 and 0.95.
- Chr20 is no longer a gain after correction and chr22 lacks BAF support. Chr19 retains
  joint support at both thresholds: primary depth ratio 1.02163 (95% CI 1.01803–1.02669)
  and BAF excess 0.000423 (95% CI 0.000222–0.000778). Simple depth and BAF conversions give
  a broad approximately 4–9% mosaic-fraction screening range.
- This is a credible single-subject screening signal, not clinical confirmation of mosaic
  trisomy 19. It does not establish small-variant inheritance or phase; the BUB1B pair's
  trans phase remains unconfirmed.
- Two-axis review widened the uncertainty model to joint chromosome-stratified 1 Mb block
  bootstraps, added exact R1/R2 lane-key validation, split checkpoint signatures by stage,
  corrected the feat-006 next-feature marker and removed stale README status text.

Reproduction and aggregate limitations are recorded in `notes/copy-number-screen.md`.
Verification included all three Python self-checks, shell syntax, the real all-lane run,
the ≥0.95 sensitivity run and the repository gates.

Next: feat-006, local scorer and submission conformance.

Final `./init.sh` completed on 2026-09-03:

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
84.99 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== 5. local bioinformatics toolchain ===
bcftools 1.24
samtools 1.24
tabix (htslib) 1.24
2.2.1
pigz 2.8
Picard Version: 3.5.0
      version 26.04.6 build 12646
openjdk version "17.0.20.1" 2026-08-18
=== 6. offline annotation resources ===
annotation resources ready
=== OK ===
```

## 2026-09-03 — session 16: feat-006 local scorer and submission conformance

- Pinned the organizers' public Track 1 scorer and CSV template at Hugging Face Space
  revision `1c761cc23d90aebe6a011fd5b0b99517df42408c`. The scorer is byte-identical to
  upstream and its SHA-256 is mechanically verified before it can run.
- Added `scripts/track1_submission.py` to build a ten-row draft from the feat-004
  compound-pair ranking, enforce the exact official schema and `PROBAND01`, require
  `chr`-prefixed contigs and strictly distinct descending EPCRs, reject duplicate or
  incomplete hypotheses, and verify every allele against the exact reference with
  `bcftools norm`.
- The real local draft has ten pair hypotheses and 20 alleles. All 20 match the reference
  and are already minimal and left-aligned. Its check report binds the tested CSV and
  vendored scorer by SHA-256.
- Under the explicit hypothetical assumption that row 1 is the answer, the unmodified
  official scorer returns 100 rank points and F-max 1.0 at EPCR 0.95. No private answer key
  was accessed, so this is a plumbing/conformance result rather than a biological score.
- The draft EPCRs are deterministic rank-preserving placeholders, not calibrated
  probabilities. No Track 1 submission was uploaded or spent.
- The leading BUB1B pair remains an unphased hypothesis; trans phase remains unconfirmed.
- Two-axis review caught and fixed missing checksum enforcement/report binding, replaced
  anonymous allele tuples with named domain types, and required this final init evidence.

Verification commands:

```bash
uv run python scripts/verify_data.py --self-check
uv run python scripts/track1_submission.py --self-check
uv run python scripts/track1_submission.py build
uv run python scripts/track1_submission.py check
uv run python -m compileall -q scripts/track1_submission.py scripts/vendor/evaluation.py
```

Final `./init.sh` output:

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
84.99 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== 5. local bioinformatics toolchain ===
bcftools 1.24
samtools 1.24
tabix (htslib) 1.24
2.2.1
pigz 2.8
Picard Version: 3.5.0
      version 26.04.6 build 12646
openjdk version "17.0.20.1" 2026-08-18
=== 6. offline annotation resources ===
annotation resources ready
=== OK ===
```

Next: feat-007, history-safe publication. Do not start the destructive history rewrite or
change repository visibility without explicit authorization.
## 2026-09-04 — session 17: feat-005b targeted missed-allele screen

- Activated exactly one feature, feat-005b, and profiled live resources before the heavy
  run: 64 CPU cores, 446 GB available RAM and 3.65 TB free disk. Added pinned WhatsHap 2.8
  and DELLY 2.1.0 support.
- Realigned all four paired FASTQ lanes to the validated reference. The duplicate-removed
  BAM contains 934,025,028 primary reads, with 99.55% mapped and 98.27% properly paired.
- Re-called 185 genome-wide survivor genes plus CEP57 and TRIP13 literature-prior controls
  across 184 padded intervals (25,332,670 bases) with HaplotypeCaller and tumor-only
  Mutect2, normalized against the same reference, subtracted the feat-004 PASS baseline by
  exact allele identity and annotated offline.
- Added supported coding/splice, operational deep-intronic (>=20 bp from an exon boundary),
  and local repeat-adjacent screens. The 226-row local set contains 13, 203 and 62 calls in
  those overlapping classes. Same-gene reconstruction generated 314 local novel/existing
  hypotheses across 63 genes; none involves BUB1B, CEP57 or TRIP13.
- Built a separate 1 Mb-flank SV target (144 intervals; 340,005,156 bases), extracted all
  complete read pairs touching it and ran DELLY. Of 7,123 raw candidates, 984 are
  heterozygous, discovery-PASS, QUAL >= 300 and supported by at least five variant reads;
  125 touch a 20 kb gene window. None touches BUB1B or CEP57; one padded-TRIP13-window
  event remains an unvalidated local review item.
- WhatsHap used 432 multi-variant reads across the padded BUB1B locus. Both leading alleles
  were present but remained unphased with no phase-set identifier; trans phase remains
  unconfirmed. The Track 1 ordering is unchanged.
- Added checkpoint signatures, input-bound raw-call recovery guards, BAM integrity checks, an
  empty-call annotation guard, single-sample SV filtering, aggregate analysis and exact
  reproduction commands in `notes/targeted-recall.md`. All subject-level artifacts remain
  under ignored `results/feat005b/`.
- The required standards/specification review found that the first pass omitted explicit
  deep-intronic and repeat-context interpretation, did not reconstruct same-gene pairs,
  weakly filtered SVs and allowed unbound recovery reuse. All four gaps were corrected;
  the unused psutil dependency and dead fingerprint helper were removed.
- Verification: `./scripts/run_targeted_recall.sh --self-check`, both `samtools quickcheck`
  calls, `uv lock --check` and `git diff --check` pass. Final `./init.sh` output:

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
84.99 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== 5. local bioinformatics toolchain ===
bcftools 1.24
samtools 1.24
tabix (htslib) 1.24
2.2.1
pigz 2.8
Picard Version: 3.5.0
      version 26.04.6 build 12646
openjdk version "17.0.20.1" 2026-08-18
Delly 2.1.0
=== 6. offline annotation resources ===
annotation resources ready
=== OK ===
```

## 2026-09-06 — session 18: feat-007 history cleanup; GitHub purge pending

- The user explicitly authorized feat-007, including its defined rewrite, force-push and
  eventual public visibility change. The source branch began at `65ad73d` and was clean.
- Added a repeatable local disclosure audit across all reachable commits/blobs, annotated
  tags, paths and ref names. Protected vocabulary stays in local memory; reports contain
  counts and identifiers only. Noncommit refs, suspicious credentials, prohibited paths and
  binary/oversized blobs fail the gate. Synthetic fixtures verify historical, tag and name
  disclosures, including removal from HEAD while old history still fails.
- Prepared an isolated packed mirror with pinned git-filter-repo 2.47.0. Conservative
  redaction changed 13 blob versions across seven paths and rewrote 22 of 26 commits.
  The verified mirror contained 188 unique blobs and zero audit findings. Current notes
  were then paraphrased for readability; scientific ranking and phase claims are unchanged.
- Preserved a local recovery bundle under ignored `results/feat007/`, adopted clean head
  `5581dfd`, and force-pushed configured origin with an explicit lease against `65ad73d`.
  Reachable local and remote history passed the audit and branch SHAs matched.
- GitHub still returned all 13 retired blobs by ID after the push. A known clean README
  blob also succeeded as an access-control check. Visibility remains PRIVATE. The feature
  remains `next`, not done; no submission was uploaded. GitHub must purge these objects
  before the public flip. The prepared Support request has not been sent.
- Integrated the staged phrase audit into the pre-commit gate when the local source is
  present. Startup installs a missing hook and rejects incompatible hooks without replacing
  them. Synthetic installation/invocation/dangling/nonexecutable-hook checks pass.
- Standards and specification reviews found and closed tag/name coverage gaps, an
  authentication-related false-pass risk in remote 404 handling, and incompatible-hook
  acceptance. Both final review reports have zero remaining findings.
- Verification: audit/rewrite/remote self-checks, hook regression checks, phenotype and
  Track 1 scorer self-checks, shell syntax, Python compilation and whitespace checks pass.
  The remote purge gate intentionally fails (13 retained objects, zero unknown errors).
  `notes/publication-audit.md` contains the commands and limitations; the deletion plan
  includes local recovery mirrors/bundles and unreachable Git objects.

Final fresh-shell `./init.sh` output (exit 0):

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
84.99 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== 5. local bioinformatics toolchain ===
bcftools 1.24
samtools 1.24
tabix (htslib) 1.24
2.2.1
pigz 2.8
Picard Version: 3.5.0
      version 26.04.6 build 12646
openjdk version "17.0.20.1" 2026-08-18
Delly 2.1.0
=== 6. offline annotation resources ===
annotation resources ready
=== OK ===
```

## 2026-09-06 — session 19: feat-008 local submission package

- Selected feat-008 as the one active feature; feat-007 is blocked pending remote object
  removal. No visibility change, Support message or competition upload was performed.
- Implemented `scripts/prepare_track1_package.py` with separate build, offline verification
  and live preflight. The package binds CSV/report/check bytes to committed source,
  configuration and evidence hashes; tampering and symlink payloads are rejected.
- Added a full report template with the exact ranked-pair table, phenotype/family scope,
  reproducible methods, screening limitations, explicit unconfirmed trans phase and an
  honest hypothetical-score explanation. Updated the ClinVar frequency caveat in notes.
- Corrected the public-first inference against the pinned official upload source: private
  visibility is permitted until competition end. Our stricter owner policy remains
  unchanged pending a decision. Required AI plan/tier and data-handling disclosures are
  unresolved and block preflight rather than being fabricated.
- Initial tests: package self-check, official scorer conformance/normalization self-check,
  data-verifier self-check, Python compilation and whitespace checks passed. Startup
  `./init.sh` completed successfully, including all resource checksum verification.
- Package generation, independent reviews and final verification are recorded below once
  executed. This feature is not done until a real authenticated upload has a receipt.

### Session 19 verification and handoff

- Built and verified `results/feat008/jvv7_genomewide_mva_v2/` at `c5bc2e0`;
  v1 is superseded. CSV SHA-256
  `a1f9315e223a07914589ce6884a66702b80e587ec5b7ad67f2ca1213f6caa225`,
  report SHA-256 `e4df63305f7cdb3e3e6deb97a8366f859e6a08fa0dc58caefe0c33eb27d7a98f`.
  Ten pairs and twenty normalized alleles pass. The local hypothetical row-1 score is
  still 100 / 1.0, not an official score; no upload occurred.
- `uv run python scripts/test_track1_package.py results/feat008/jvv7_genomewide_mva_v2`
  passed 18 publication-policy cases, three live-upstream cases, portable-copy validation
  and nine payload/manifest corruption rejections. Package self-check, data-verifier
  self-check, Python compilation and whitespace checks also passed.
- Full relevant regression command passed (exit 0):

  ```bash
  ./scripts/run_vcf_triage.sh --self-check &&
  ./scripts/run_copy_number_screen.sh --self-check &&
  ./scripts/run_targeted_recall.sh --self-check &&
  uv run python scripts/audit_publication.py --self-check &&
  uv run python scripts/check_publication_remote.py --self-check &&
  uv run python scripts/test_publication_hooks.py &&
  uv run python scripts/extract_hpo.py --self-check &&
  uv run python scripts/track1_submission.py --self-check
  ```

- Independent standards and specification reviews identified and closed the purge-policy
  gap, stale-upstream check, positional evidence naming and missing-AF wording issues.
  Re-review found no residual issues in either axis. See `notes/track1-submission.md`.
- `git push origin main` pushed the implementation and fixes. The subsequent real
  `prepare_track1_package.py preflight results/feat008/jvv7_genomewide_mva_v2` returned
  exit 1 for three missing AI disclosure fields and the failed obsolete-object purge.
  Live official revision and origin synchronization checks passed.
- **Unexpected external state:** around 17:44 UTC, GitHub reported PUBLIC twice even
  though this session did not change visibility. The checker still found 13/13 retired
  objects retrievable, with zero unknown errors and a successful control. Owner approval
  to restore PRIVATE was requested; no response was available at this checkpoint.
  The safety gate correctly prevented treating PUBLIC alone as readiness.

Final fresh-shell `./init.sh` output (exit 0):

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
84.99 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== 5. local bioinformatics toolchain ===
bcftools 1.24
samtools 1.24
tabix (htslib) 1.24
2.2.1
pigz 2.8
Picard Version: 3.5.0
      version 26.04.6 build 12646
openjdk version "17.0.20.1" 2026-08-18
Delly 2.1.0
=== 6. offline annotation resources ===
annotation resources ready
=== OK ===
```

## 2026-09-06 — session 20: owner-confirmed public visibility and API tier

- The owner clarified that they made the repository public and that Codex uses API tier.
  Saved `API tier (owner-confirmed)` in `notes/track1-submission-config.json` and updated
  the harness/handoff to distinguish an explained owner action from an unknown change.
- API tier does not establish account-specific data sharing, training or retention.
  `ai_data_handling_setting` and `other_ai_providers` remain unresolved; requested these
  remaining details without inventing them or waiving the historical-object purge gate.
- No visibility change, Support message or upload was performed. Feat-008 remains active
  and unfinished. The latest remote availability check still found 13 retired objects.
- The immutable v2 package is now historical/stale because its configuration changed.
  Do not alter its files or upload it. Complete disclosure and build a new v3 package.
- `uv run python scripts/prepare_track1_package.py --self-check` passed. An explicit
  configuration regression asserted the API-tier value, exactly two missing fields and
  rejection of v2 with `code_files changed; build a new package after review`.
- `uv run python scripts/audit_publication.py --staged --output
  results/feat008/api-tier-staged-audit.json` scanned 60 blobs with zero findings;
  `git diff --check` passed. Final startup verification is recorded below.

Fresh-shell `./init.sh` completed with exit 0:

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
84.99 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== 5. local bioinformatics toolchain ===
bcftools 1.24
samtools 1.24
tabix (htslib) 1.24
2.2.1
pigz 2.8
Picard Version: 3.5.0
      version 26.04.6 build 12646
openjdk version "17.0.20.1" 2026-08-18
Delly 2.1.0
=== 6. offline annotation resources ===
annotation resources ready
=== OK ===
```

## 2026-09-06 — session 21: refreshed v3 draft, upload still blocked

- Continued feat-008's safe local preparation after the owner asked what comes next.
  The request to ignore the purge gate was not implemented: it conflicts with the
  non-negotiable data-access rules. No visibility change, external message or upload.
- `uv run python scripts/prepare_track1_package.py build --name jvv7_genomewide_mva_v3`
  produced the updated report using the committed owner-confirmed API tier at `cdfb444`.
  Candidate ranking, scientific interpretation and unconfirmed trans phase are unchanged.
- CSV SHA-256: `a1f9315e223a07914589ce6884a66702b80e587ec5b7ad67f2ca1213f6caa225`.
  Report SHA-256: `eb836b42dc8b10c3dc010384edd124bd8e3c02a738a9106e097c887de42d421f`.
- `uv run python scripts/test_track1_package.py results/feat008/jvv7_genomewide_mva_v3`
  passed 18 publication-policy cases, three live-upstream cases, portable-copy verification
  and nine corruption rejections. Build/verify confirmed 10 pairs and 20 normalized alleles.
  Package and official-scorer self-checks also passed; no private answer key was queried.
- `uv run python scripts/prepare_track1_package.py preflight results/feat008/jvv7_genomewide_mva_v3`
  exited 1: account data-handling disclosure, other AI providers and the purge gate remain
  unresolved. GitHub PUBLIC visibility, live upstream and official contract checks passed.
  No remaining-attempt count, actual score or receipt is claimed.
- Staged disclosure audit: 60 blobs, zero findings. Updated the harness, feature evidence
  and handoff to point to v3 and require missing inputs before another package revision.
  V1/v2 remain untouched historical artifacts. Whitespace checks passed.

Fresh-shell `./init.sh` completed with exit 0:

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
84.99 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== 5. local bioinformatics toolchain ===
bcftools 1.24
samtools 1.24
tabix (htslib) 1.24
2.2.1
pigz 2.8
Picard Version: 3.5.0
      version 26.04.6 build 12646
openjdk version "17.0.20.1" 2026-08-18
Delly 2.1.0
=== 6. offline annotation resources ===
annotation resources ready
=== OK ===
```

## 2026-09-08 — session 22: completed owner AI disclosure

- Owner confirmed no other AI providers were used and data is not used to train the
  provider's models. Recorded both in `notes/track1-submission-config.json`, alongside
  the earlier OpenAI/Codex API-tier confirmation. No zero-retention or independent
  account-verification claim is added; subject-data safeguards remain unchanged.
- Updated current harness/README/submission guidance. Feat-008 remains active and
  unfinished; feat-007's independent purge gate is unresolved. No upload or external
  message was authorized or performed.
- Package and official-scorer self-checks pass. Built v4 from committed `13f06ad` with
  `uv run python scripts/prepare_track1_package.py build --name jvv7_genomewide_mva_v4`.
  `verify results/feat008/jvv7_genomewide_mva_v4` passes: 10 pairs, 20 reference-normalized
  alleles, zero unresolved disclosure fields. V1/v2/v3 remain untouched and historical.
- `uv run python scripts/test_track1_package.py results/feat008/jvv7_genomewide_mva_v4`
  passes 18 publication-policy cases, three live-upstream cases, portable copying and
  nine corruption rejections. Ranking and unconfirmed trans phase are unchanged.
- CSV SHA-256: `a1f9315e223a07914589ce6884a66702b80e587ec5b7ad67f2ca1213f6caa225`.
  Report SHA-256: `f36bacbc506d5a717ee7a55f174fed3f376ed7beacd83d11091e57d319d0d68b`.
- `uv run python scripts/prepare_track1_package.py preflight results/feat008/jvv7_genomewide_mva_v4`
  exits 1 solely on the independent purge gate. GitHub is PUBLIC; all 13 retired objects
  remain retrievable, with zero unknown errors and a successful reachable-object control.
  Live origin synchronization and the pinned official contract pass. No upload, remaining
  quota, official score or receipt is claimed. No visibility change or Support message.
- `git diff --check` passes. Fresh-shell `./init.sh` completed with exit 0:

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
84.99 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== 5. local bioinformatics toolchain ===
bcftools 1.24
samtools 1.24
tabix (htslib) 1.24
2.2.1
pigz 2.8
Picard Version: 3.5.0
      version 26.04.6 build 12646
openjdk version "17.0.20.1" 2026-08-18
Delly 2.1.0
=== 6. offline annotation resources ===
annotation resources ready
=== OK ===
```

## 2026-09-08 — session 23: purge resolution and concrete Support handoff

- Worked only on feat-007 at the owner's explicit request. No repeat history rewrite,
  remote deletion, visibility change, gate bypass or Track 1 upload was performed.
- `uv run python scripts/audit_publication.py --output results/feat007/current-history.json`
  passes at `3c64b87`: 34 reachable commits, 251 unique blobs, zero findings.
- Fresh configured-origin inventory advertises main/HEAD only. GitHub API reports ADMIN
  access, PUBLIC visibility, zero forks, PRs, Actions runs, releases and issues.
- `uv run python scripts/check_publication_remote.py` exits 1: 13/13 retired objects
  retrievable, zero unknown errors, successful current-blob control. Its self-check passes.
  Separate unauthenticated standard-library API requests returned 200 for all 13 objects
  and the control; only status counts were emitted, not protected response bodies.
- Checked GitHub's official sensitive-data-removal and support-ticket documentation.
  The remaining operation is Support-run server-side GC/cache removal. Prepared request
  now includes PUBLIC visibility, current availability evidence, zero affected PRs, earliest
  changed commit from the rewrite map and no LFS involvement. No protected attachments.
- The available environment has repository CLI access but no authenticated Support
  portal session/integration. Request remains unsent with no ticket ID. The owner must
  sign into the Support portal and send it. Recommended temporary PRIVATE containment,
  without overriding the owner's previous deliberate visibility choice.
- Updated harness, feature evidence, publication audit and handoff. Skill-guided state
  records the external dependency without falsely marking feat-007 complete. V4 stays
  unchanged and locally valid; trans phase remains unconfirmed. `git diff --check` passes.

Fresh-shell `./init.sh` completed with exit 0:

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
84.99 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== 5. local bioinformatics toolchain ===
bcftools 1.24
samtools 1.24
tabix (htslib) 1.24
2.2.1
pigz 2.8
Picard Version: 3.5.0
      version 26.04.6 build 12646
openjdk version "17.0.20.1" 2026-08-18
Delly 2.1.0
=== 6. offline annotation resources ===
annotation resources ready
=== OK ===
```

## 2026-09-08 — session 24: owner Support ticket and private containment

- Owner reports submitting GitHub Support ticket **4738585** and restoring PRIVATE
  visibility. `gh repo view Vijayavallabh/mva-hackathon-2026 --json visibility,url`
  independently confirms PRIVATE. Ticket contents/status remain owner-reported;
  this environment has no authenticated Support portal session.
- `uv run python scripts/check_publication_remote.py` exits 1: PRIVATE repository,
  13/13 retired objects still retrievable under authentication, zero unknown errors,
  successful reachable-blob control. Containment is not removal; feat-007 stays blocked.
- Updated harness, feature evidence, README, publication/submission notes and Support
  request header. Kept the original request draft explicitly historical rather than
  presenting it as a verified transcript of the owner's submitted ticket. Do not ask
  for another ticket; await Support's response on 4738585, then verify before publication.
- V4 package verification passes with unchanged hashes, 10 pairs, 20 normalized alleles
  and zero missing disclosures. No package rebuild, upload, visibility change, external
  message or continuous monitoring was performed. Trans phase remains unconfirmed.
- `git diff --check` passes. Fresh-shell `./init.sh` completed with exit 0:

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
84.99 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== 5. local bioinformatics toolchain ===
bcftools 1.24
samtools 1.24
tabix (htslib) 1.24
2.2.1
pigz 2.8
Picard Version: 3.5.0
      version 26.04.6 build 12646
openjdk version "17.0.20.1" 2026-08-18
Delly 2.1.0
=== 6. offline annotation resources ===
annotation resources ready
=== OK ===
```

## 2026-09-08 — session 25: feat-008 execution recheck, blocked before upload

- Selected feat-008 from the queue in response to the request to execute the next
  feature. The existing v4 deliverables remain unchanged; no new package was needed.
- At clean, synchronized HEAD `8476cc2`, package and official-scorer self-checks pass.
  `uv run python scripts/test_track1_package.py results/feat008/jvv7_genomewide_mva_v4`
  passes 18 policy cases, three live-upstream cases, portable copy and nine corruptions.
- `uv run python scripts/prepare_track1_package.py preflight results/feat008/jvv7_genomewide_mva_v4`
  confirms offline validity, unchanged hashes, 10 pairs, 20 normalized alleles and no
  unresolved disclosure fields. Live upstream, reachable-history audit and official
  contract checks pass. Exit 1 reports exactly two blockers: PRIVATE visibility under
  the public-first policy and failed remote purge. The nested check reports 13/13
  retired objects retrievable, zero unknown errors and a successful access control.
- Marked feat-008 `blocked` instead of `next`; updated submission notes and handoff
  using the harness-creator skill's evidence-based state guidance. No implementation
  change was needed, so no implementation-completion code review was triggered.
  Ticket 4738585 remains owner-reported; no Support response was accessed. Keep private
  pending purge verification. No upload, spent attempt, receipt, official score,
  visibility change or external message. Trans phase remains unconfirmed.
- Fresh-shell `./init.sh` completed with exit 0; actual output follows:

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
84.99 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== 5. local bioinformatics toolchain ===
bcftools 1.24
samtools 1.24
tabix (htslib) 1.24
2.2.1
pigz 2.8
Picard Version: 3.5.0
      version 26.04.6 build 12646
openjdk version "17.0.20.1" 2026-08-18
Delly 2.1.0
=== 6. offline annotation resources ===
annotation resources ready
=== OK ===
```

## 2026-09-08 — session 26: additional phase analysis, feat-005c

- The owner requested trans-phase work. Added the bounded feat-005c follow-up rather
  than treating the request as evidence of trans or permission to change a submission.
  Scientific-critical-thinking guidance kept graph connectivity, encoded phase and
  biological confirmation distinct; pysam was used only for local indexed processing.
- `scripts/audit_phase_connectivity.py` audits source-marker and HaplotypeCaller-union
  SNV graphs in the existing BUB1B interval at two MAPQ/base-quality settings and two
  edge-support thresholds. Final artifacts are
  `results/feat005c/source-connectivity-final.json` and `union-connectivity-final.json`.
  Full commands and filters are in `notes/phase-connectivity.md`.
- Measured 48 original / 49 union eligible SNVs; zero fragments observe both targets,
  and both are singleton components at all settings. Target separation is 10,911 bp;
  local maximum read length is 149 bp and median proper-pair template length is 442 bp.
  Individual candidate support is retained, but it cannot establish relative phase.
- WhatsHap 2.8 independently phased the existing recalled locus, with 58 usable
  heterozygous variants. It completed successfully, but both candidates remain present
  and unphased without a shared phase set. Final aggregate JSON checks both original
  and recalled phase outputs. No source records, read bases, names or marker edges
  were emitted to model context or transmitted externally.
- `uv run python scripts/audit_phase_connectivity.py --self-check` passes.
  `uv run python scripts/test_phase_connectivity.py` passes 16 synthetic integration
  tests. `uv run python -m compileall -q scripts/audit_phase_connectivity.py scripts/test_phase_connectivity.py`
  and `./scripts/run_targeted_recall.sh --self-check` pass. Specification and standards
  review of `b827f17...c75926a` found zero blocking findings; optional filter-test
  suggestions were implemented and retested. No static typechecker is configured.
- `uv run python scripts/prepare_track1_package.py verify results/feat008/jvv7_genomewide_mva_v4`
  passes with unchanged CSV/report hashes; package regressions also pass. No deliverable,
  ranking, visibility or submission was changed. The owner's announced intention to
  publish/submit is not a verified external action or receipt. No new live publication
  status was inferred. Trans phase remains unconfirmed.
- Harness-creator guidance informed the explicit distinction between completed analysis
  and unresolved biological phase. Updated feature evidence, AGENTS, targeted-recall
  notes and handoff. Fresh-shell `./init.sh` completed with exit 0; actual output:

```text
=== 1. uv environment ===
huggingface_hub 1.28.0
=== 2. no subject data in git ===
no-data-in-git: ok
=== 3. verify_data self-check ===
self-check ok
=== 4. dataset integrity ===
84.99 GB in /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026/data
COMPLETE: all files present at expected size
=== 5. local bioinformatics toolchain ===
bcftools 1.24
samtools 1.24
tabix (htslib) 1.24
2.2.1
pigz 2.8
Picard Version: 3.5.0
      version 26.04.6 build 12646
openjdk version "17.0.20.1" 2026-08-18
Delly 2.1.0
=== 6. offline annotation resources ===
annotation resources ready
=== OK ===
```
