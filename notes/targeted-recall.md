# Targeted realignment and missed-allele screen — feat-005b

## Purpose and scope

This optional feature was explicitly activated on 2026-09-03. Its purpose is to test
whether the original diploid germline VCF omitted a relevant SNV, indel or structural
allele near genes that survived the genome-wide feat-004 ranking. It is not an aneuploidy
analysis; the corrected depth/BAF screen remains feat-005a.

The interval builder takes every distinct gene represented in
`results/feat004/all_candidate_models.tsv` and forces inclusion of the three established
MVA genes BUB1B, CEP57 and TRIP13. Ensembl 116 gene bodies receive 20 kb flanks and are
merged. The resulting 187-gene target comprises 184 intervals and 25,332,670 bases. This
keeps all 185 genes that survived the first-pass candidate models rather than collapsing
the analysis to BUB1B, while acknowledging that the re-call is hypothesis-directed rather
than a second unrestricted whole-genome interpretation.

## Design

All four paired FASTQ lanes are aligned once to the exact validated unprefixed GRCh38
reference. Mate information is repaired, alignments are coordinate-sorted, and duplicates
are marked and removed. The resulting full alignment stays under gitignored
`results/feat005b/`; retaining it permits consistent SNV/indel, structural-variant and
phasing analyses without a third FASTQ pass.

The downstream evidence streams are deliberately complementary:

1. GATK HaplotypeCaller re-calls conventional diploid SNVs and indels in the padded gene
   windows.
2. GATK Mutect2 runs in single-sample tumor-only mode over the same windows. Mutect2 uses
   local haplotype assembly and supports detection of somatic mosaicism, but without a
   matched normal or panel of normals its novel calls are a sensitive screen, not somatic
   truth. F1R2 orientation priors and FilterMutectCalls are applied.
3. A second interval set gives every candidate gene 1 Mb flanks (144 merged intervals,
   340,005,156 bases). `samtools view --fetch-pairs` retains complete read pairs whenever
   either mate touches those regions, and DELLY 2.1.0 screens the resulting target-enriched
   BAM for deletions, insertions, duplications, inversions and breakends. Because DELLY's
   germline filter assumes a cohort, this single-sample analysis instead retains discovery
   PASS sites at DELLY's default site-quality threshold, QUAL >= 300, before testing overlap
   with the 20 kb gene windows.
4. WhatsHap 2.8 attempts read-backed phasing across the complete padded BUB1B locus. The
   leading pair is called trans or cis only if both biallelic heterozygotes
   are phased in the same phase set. Separate phase sets, missing calls or an unphased
   genotype leave trans phase unconfirmed.

HaplotypeCaller and Mutect2 PASS calls are normalized against the exact reference and
subtracted from the already normalized source VCF by exact allele identity. Novel calls
are annotated offline with VEP 116 and its pinned gnomAD fields. The review table retains
rare or frequency-absent coding/splice candidates; it remains local because it contains
subject-level variant records.

No BQSR is applied: the installed bundle does not contain a reference-matched, pinned set
of known-sites resources, and silently mixing reference builds would be worse than stating
this limitation. The source data are high-depth WGS, and both callers use
their own base and mapping-quality models.

## Reproduce

```bash
./scripts/run_targeted_recall.sh --self-check
mkdir -p logs
nohup setsid env \
  MVA_RECALL_ALIGN_THREADS=32 \
  MVA_RECALL_SORT_THREADS=8 \
  MVA_RECALL_DECOMP_THREADS=4 \
  MVA_RECALL_CALL_THREADS=8 \
  ./scripts/run_targeted_recall.sh \
  >> logs/feat005b-targeted-recall.log 2>&1 </dev/null &
```

The 2026-09-03 resource snapshot found 64 physical cores, 446 GB available RAM and 3.65 TB
free disk at 91% filesystem use; live load average was 13.4. Alignment is therefore capped
at 32 threads, sorting at eight threads with 4 GB per thread, and calling at eight threads.
GPU availability does not materially accelerate this BWA/GATK/DELLY workflow.

The pipeline validates all inputs and pinned tools before reading FASTQ, verifies mate-lane
pairing, uses input/code/tool-bound stage signatures, runs `samtools quickcheck`, records
flagstat/stats, and can resume at intervals, alignment, small-call, structural-call and
phase checkpoints.

## Outputs and privacy

All subject-level outputs stay in `results/feat005b/`, including the BAM, VCF/BCF files,
phased VCF, novel-candidate table and target-SV table. `summary.json` contains aggregates
and the categorical phase result. Only reviewed aggregate findings and permitted submitted
candidate conclusions are copied into tracked notes. No subject read, alignment or VCF
record is sent to a remote service.

## Result

The all-lane alignment retained 934,025,028 primary nonduplicate reads; 99.55% mapped and
98.27% were properly paired. HaplotypeCaller emitted 53,865 normalized accepted alleles in
the 25.3 Mb target. Exact subtraction against the feat-004 normalized PASS baseline left
2,374 annotated HaplotypeCaller calls and 541 Mutect2 calls, with 270 exact alleles seen by
both callers. The offline rarity and coding/splice filter retained 24 rows across 12 genes.
None adds an allele in BUB1B, CEP57 or TRIP13, and none is supported by both callers. The
rows are concentrated in polymorphic or mapping-sensitive loci including MUC4, HLA/KIR,
PKD1 and TAS2R31. A Mutect2-only CUL7 missense is retained for secondary manual review
because of CUL7's growth biology, but its near-homozygous allele fraction and lack of
HaplotypeCaller support do not justify promoting it over the existing BUB1B pair.

DELLY generated 7,123 raw target-enriched candidates. Applying discovery PASS plus
QUAL >= 300 retained 1,500; 167 overlap a 20 kb candidate-gene window. No retained event
overlaps the BUB1B or CEP57 window. One overlaps the padded TRIP13 window and remains a
local manual-review item, not a confirmed structural allele; the single-sample targeted
screen has no orthogonal SV validation and its numerous window overlaps show that PASS and
site quality alone are not sufficient for pathogenic interpretation.

Within the 100,154-base padded BUB1B locus, WhatsHap found 56 usable heterozygous variants
and 432 reads covering at least two variants. It created local phase blocks, but both
leading alleles remained unphased and had no shared phase-set identifier. Therefore
**trans phase remains unconfirmed**. Feat-005b does not change the Track 1 ordering: BUB1B
remains the leading candidate pair, with phase and the missense allele's classification as
the main unresolved biological questions.

The aggregate counts above are reproduced by the main command plus:

```bash
tools/install/bin/samtools flagstat results/feat005b/all-lanes.markdup.bam
tools/install/bin/bcftools view -H results/feat005b/delly.raw.bcf | wc -l
tools/install/bin/bcftools view -H results/feat005b/delly.pass.bcf | wc -l
uv run python scripts/analyze_targeted_recall.py \
  --hc-vep results/feat005b/haplotypecaller.novel.vep.vcf.gz \
  --mutect-vep results/feat005b/mutect2.novel.vep.vcf.gz \
  --delly results/feat005b/delly.pass.bcf \
  --manifest results/feat005b/targets.json \
  --phased results/feat005b/target-source.phased.vcf.gz \
  --candidates results/feat004/candidate_models.tsv \
  --novel-candidates results/feat005b/novel-candidates.tsv \
  --target-svs results/feat005b/target-svs.tsv \
  --summary results/feat005b/summary.json
```
