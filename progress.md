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
