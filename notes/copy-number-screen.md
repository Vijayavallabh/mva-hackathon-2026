# GC-corrected copy-number and BAF screen — feat-005a

Completed locally on 2026-09-03. This note contains aggregate derived results only: no
subject reads, genotypes or variant positions.

## Question and result

The preliminary 10 Mb VCF screen could not distinguish low-level mosaic gain from a
GC/mappability artefact on chromosomes 19, 20 and 22. The corrected screen resolves those
signals as follows:

| chromosome | corrected depth ratio (95% CI) | BAF excess variance (95% CI) | interpretation |
|---|---:|---:|---|
| 19 | 1.02163 (1.01803–1.02669) | 0.000423 (0.000222–0.000778) | joint depth and BAF support for low-level mosaic gain |
| 20 | 1.00110 (0.99620–1.00580) | 0.000094 (−0.000107–0.000393) | no gain after correction |
| 22 | 1.00872 (1.00123–1.01557) | 0.000223 (−0.000117–0.000917) | small depth shift without BAF support; not jointly supported |

The stricter mappability sensitivity analysis (≥0.95 rather than ≥0.90) gives the same
three conclusions. For chromosome 19 its depth ratio is 1.02161 (95% CI
1.01785–1.02653), and its BAF excess interval remains above zero
(0.000204–0.000605).

The two simple chromosome 19 effect-size conversions differ: depth suggests about 4.3%
and BAF about 7.8–8.5% mosaic fraction. Treat this as a broad approximately 4–9% screening
range, not a calibrated estimate. The concordant directions and threshold sensitivity make
the signal credible, but a single-subject WGS screen without matched controls is not a
clinical karyotype and does not prove mosaic trisomy 19.

This copy-number result is independent of small-variant phase. In particular, it **does not
show that the two leading BUB1B alleles are in trans**; trans phase remains unconfirmed.

## Method

The pipeline builds fixed 100 kb primary-contig bins from the exact masked GRCh38 no-alt +
hs38d1 reference and annotates each bin with reference GC, callable A/C/G/T fraction and
the pinned Umap k=100 multi-read mappability track. It streams all four paired FASTQ lanes
through BWA-MEM2, mate fixing, coordinate sorting and duplicate removal. Only primary,
nonduplicate, QC-passing alignments with MAPQ ≥30 contribute aligned reference bases;
intermediate BAM data is not retained.

Analysis retains autosomal bins with A/C/G/T fraction ≥0.95 and mappability ≥0.90. Each
target chromosome is corrected against a 0.5%-GC median curve learned from the other 21
autosomes, with linear interpolation and normalization against those other autosomes.
Depth intervals use a deterministic 2,000-replicate, chromosome-stratified 1 Mb block
bootstrap. Every replicate resamples the target and background blocks and refits both the
GC curve and its normalization, propagating spatial correlation and correction-model
uncertainty within this sample.

The BAF arm uses PASS biallelic heterozygous SNVs with DP 20–90, GQ ≥30 and at least five
reads supporting each allele, restricted to the same eligible bins. Its statistic is
`(BAF − 0.5)^2 − 0.25/depth`, first aggregated within 100 kb bins. Its deterministic
2,000-replicate bootstrap resamples contiguous 1 Mb blocks, stratifies the background by
chromosome, excludes the target chromosome from the background, and jointly refits the
target-versus-background contrast. A gain is called supported only when the depth
interval's lower bound is above 1.01 and the BAF-excess interval's lower bound is above
zero. The entire analysis is repeated at mappability ≥0.95 as a sensitivity check.

At the primary threshold, 25,883 autosomal depth bins, 2,110,700 high-quality heterozygous
SNVs and 25,767 populated 100 kb BAF bins were eligible. Alignment accounting was
938,213,206 input SAM records, 868,096,455 accepted records and 127,162,165,520 accepted
aligned bases; exclusions
were 8,413,170 flag failures, 55,867,998 MAPQ failures and 5,835,583 nonprimary-contig
records.

## Reproduction

The mappability asset, source URL and SHA-256 are pinned in `tools/resources.tsv`. The
resource installer verifies it locally along with the reference and annotation bundle.

```bash
./scripts/get_resources.sh --check
./scripts/run_copy_number_screen.sh --self-check
MVA_ALIGN_THREADS=40 MVA_SORT_THREADS=8 MVA_DECOMP_THREADS=2 \
  ./scripts/run_copy_number_screen.sh
```

The first complete run was launched under `nohup` because alignment is long-running:

```bash
MVA_ALIGN_THREADS=40 MVA_SORT_THREADS=8 MVA_DECOMP_THREADS=2 \
  nohup setsid -f ./scripts/run_copy_number_screen.sh \
  > logs/feat005a-copy-number.log 2>&1
```

Generated per-bin counts, BAF observations and summaries remain under the gitignored
`results/feat005a/` directory because they derive from subject-level data. The tracked code
and this aggregate report are sufficient to regenerate them from the gated inputs.

## Limitations

- This is one tissue, one subject and no matched control cohort; chromosome-specific
  residual technical bias remains possible.
- Joint block-bootstrap intervals include within-sample spatial, GC-model and baseline
  variation, but not between-sample laboratory or population variation.
- Bulk blood WGS may miss tissue-restricted or very-low-level mosaicism.
- The approximate mosaic fractions are model-based screening summaries, not clinical
  confirmation. Cytogenetic testing or an orthogonal copy-number assay would be required.
- Copy-number evidence cannot establish inheritance, pathogenicity or trans phase for the
  candidate small variants.
