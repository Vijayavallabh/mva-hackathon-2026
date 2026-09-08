# Data profile — measured 2026-08-28

Every number here was produced by a command recorded below, run locally on `data/`.
This file holds **aggregate statistics only**: no genotypes, no variant positions, no
clinical narrative. That is the boundary set in `AGENTS.md` rule 1.

Nothing here is a claim about the cause of the child's condition. No candidate variant
has been looked for yet.

---

## 1. The provided VCF

`data/WGS_EX2312012_HGWCNDSX7.vcf.gz` — 315,153,971 bytes, with `.tbi`.

**Provenance, from the header:**

- Sentieon `202308.02` `Haplotyper` (GVCF mode, `--call_conf 10`) → `GVCFtyper`
  (`--emit_conf 10`, dbSNP138), then GATK `4.2.4.0` `VariantFiltration`.
- Called **2025-02-05**, on DNAnexus. Single sample, column name `WGS_EX2312012`.
- Hard filters only, **no VQSR**: `QD2`, `MQ40`, `RPRS-8`, `FS60`, `MQRankSum-12.5`, `LowQual`.
- Reference: `GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_maskedGRC_exclusions_v2_no_chr.fasta`.

> **Contig names are unprefixed** — `1`, `2`, …, `X`, `Y`, `M`. 2580 contigs including
> alt/random/decoy. Track 1 submissions must be **`chr`-prefixed**; see `challenge-spec.md`.

**Contents:**

| | |
|---|---|
| Records | 5,012,204 |
| PASS | 4,740,790 (94.6%) |
| SNV / indel / multiallelic | 4,080,038 / 865,306 / 66,860 |
| On alt/random/decoy contigs | 116,485 (must be dropped) |
| dbSNP-flagged (`DB`) | 4,408,823 (88.0%) — so ~600k novel |
| Mean sample DP | 45.1 (DP<10: 122,026; DP>200: 18,487) |
| Ti/Tv (PASS autosomal SNV) | **2.050** — normal for WGS |
| Genotypes present | `0/1` (3,047,077), `1/1` (1,898,267), `1/2` (66,860) |

> **There are no CNV, SV, or symbolic-allele records of any kind.** The file is a diploid
> germline SNV/indel call set. Mosaic aneuploidy — the defining feature of MVA — cannot
> appear in it. Any copy-number work must come from read depth (feat-005a).

Command:

```bash
zcat data/WGS_EX2312012_HGWCNDSX7.vcf.gz | awk -F'\t' '...'   # counts, FILTER, GT, DP, VAF hist
```

## 2. Sample characteristics

**Male.** chrX depth ratio **0.565** of the autosomal mean with heterozygosity collapsed to
8.1% (autosomes ~62%); chrY present. Already public — the challenge page's own image
alt-text describes the child as "himself".

**No runs of homozygosity detected by this coarse screen.** A 1 Mb scan for runs of ≥3 consecutive bins
with het fraction below 15% of the genome-wide value returned **zero runs**. Per-bin het
fraction is unimodal around 0.65 across 2,709 informative bins.

> This screen does not exclude consanguinity, shorter ROH or homozygous causes and
> does not establish phase. The challenge's public compound-pair answer-key statement
> motivates that competition model (`challenge-spec.md` §3), not a particular pair.

Command:

```bash
zcat data/WGS_EX2312012_HGWCNDSX7.vcf.gz | awk -F'\t' '...'   # 1 Mb het-fraction bins, ROH runs
```

## 3. Preliminary aneuploidy screen — superseded by feat-005a

10 Mb bins, PASS biallelic SNVs, DP band 20–90, measuring depth ratio vs the genome mean and
mean |BAF − 0.5| over heterozygous sites.

**Positive control:** chrX comes out at ratio 0.565 with het collapse. The method detects
real copy-number change.

**Result:** no autosome shows the ~1.5 depth ratio or split BAF band of a full or high-level
trisomy. But the residual signal is **dominated by a GC/mappability-correlated gradient** —
chr16, 17, 19, 20, 21 and 22 all rise together in depth ratio, het%, and BAF deviation.

| chrom | DP ratio | het % | mean BAF dev | het:hom |
|---|---|---|---|---|
| genome typical | ~1.00 | ~62 | ~0.068 | ~1.60 |
| 19 | 1.038 | 66.0 | 0.0721 | 1.94 |
| 22 | 1.049 | 67.0 | 0.0869 | 2.03 |
| **20** | **1.039** | **70.4** | **0.0905** | **2.38** |
| X (control) | 0.565 | 8.1 | — | 0.09 |

In this preliminary screen, chr20 was the largest outlier on every column. It could exclude
high-level aneuploidy but could not separate genuine low-level mosaic gain from GC bias —
the confounder moved both quantities the same way.
Bin-level outliers are additionally dominated by centromeric and segmental-duplication
regions (chr9:40–50 Mb, chr1:120–130 Mb, chr17:20–30 Mb), which is the expected artefact
pattern.

**Resolution (2026-09-03):** feat-005a re-aligned all lanes and used 100 kb bins,
leave-one-chromosome-out GC correction, a Umap mappability mask and an independent BAF
arm. Chr20 returns to baseline and is not supported; chr22 has a small depth-only shift;
chr19 retains concordant depth and BAF evidence consistent with low-level mosaic gain.
This is a screening result, not clinical confirmation. Full methods, aggregate intervals
and limitations are in `copy-number-screen.md`.

## 4. FASTQ

8 files, 79.5 GB gzipped.

- Illumina NovaSeq, instrument `A01973`, run 164, flowcell `HGWCNDSX7`, lanes 1–4, sample `S16`.
- **2 × 149 bp** paired-end, Phred+33.
- One library: index `GTGACGGAGC+NGGACCGCCA` on L001/L002/L004. **L003 R1 shows
  `GTGACGGAGA`** — differs in the final base; check whether that is a one-off first-read
  artefact or a systematic index difference before treating the lanes as one library.
- Compression ratio 4.83× (`L001_R1`: 10.47 GB → **50.60 GB**). Full set ≈ **385 GB**
  uncompressed.
- `zcat` of a single file took **6m56s single-threaded** — decompressing all 8 is ~1 h serial,
  before any alignment. `pigz` is not installed.

Commands:

```bash
for f in data/*.fastq.gz; do zcat "$f" | head -1; done
zcat data/WGS_EX2312012_HGWCNDSX7_S16_L001_R1_001.fastq.gz | wc -c    # 50,600,579,174
```

## 5. Phenotype document

`data/Challenge_Clinical_Phenotype_1.docx` — processed locally; protected wording was not
copied into tracked output. Only standardized IDs and reviewed broad categories are kept.

- 380 words, 51 paragraphs, 1 table, no images.
- **Carries 8 embedded `HP:#######` IDs.** Consistent with the official rules, which state
  phenotypic data is provided "as standardized HPO terms". Reviewed categorical context
  assigns seven terms to PROBAND01 and one (`HP:0200067`) to parental/family history.
- Keyword probe returns **false** for: `karyotype`, `aneuploid`, `mosaic`, `trisomy`, `OMIM`,
  `exome`, `variant`, `VUS`, `negative`, `microcephaly`, `BUB1B`, `CEP57`, `TRIP13`.

> Consequence: **we are given a multi-system phenotype with no prior genetic workup and no
> candidate gene.** Rank the complete pattern across malignancy, renal, growth, muscle and
> perinatal domains, retaining reproductive family history as separate mechanistic context.
> The search stays genome-wide; do not collapse it onto the three known MVA genes. See
> `phenotype.md` and `prior-knowledge.md`.

Command: `uv run python scripts/extract_hpo.py` with stdlib `zipfile` + `re` over
`word/document.xml`; it emits only permitted HPO labels and reviewed categorical context.

## 6. Compute environment (2026-08-28)

- At profiling time, no bioinformatics tooling was installed. **Feat-003 completed this
  prerequisite on 2026-09-02** with a pinned repository-local toolchain and offline
  annotation resources; see `notes/toolchain.md` and `tools/versions.tsv`.
- Outbound network reachable: Ensembl FTP, gnomAD GCS, UCSC goldenPath, `purl.obolibrary.org`,
  GitHub, Hugging Face. Annotation resources can be fetched.
- **Box is contended**: load average 109 on 64 cores; GPUs 0/1/2 (A100 80 GB) at 100% with
  other users' jobs, GPU 3 is a T400, only GPU 4 free. 3.3 TB free on `/mnt/md0` (92% full).
  Recheck live conditions before every large run rather than treating this snapshot as
  current capacity.
