# Optical morphology: a favorable assay lead, with failed practical neural gain

19 October 2026. Completed public HeLa computation on eight owner-host H100s.
The retained BUB1B interphase mean profiles rank their own target 1, 3, 3 and 2
among 994 genes. This is a useful assay-development lead, with substantial guide,
aggregation and acquisition sensitivity. Neither arm passes the fixed practical
neural-gain rule. No drug, endogenous-allele, phase or clinical-exposure claim changes.

Public sources: [Funk et al., Cell](https://doi.org/10.1016/j.cell.2022.10.017),
[Dataverse version 2.0](https://doi.org/10.7910/DVN/VYKTI5), CC BY 4.0, and the
[public gene workbook](https://vesuvius.wi.mit.edu/genes.xlsx).
[Source review](track2-optical-source-review-v33.md),
[targeted methods/fate reread](track2-optical-interpretation-v35.md),
[complete results](track2-optical-results-v36.json),
[reproduction](track2-optical-reproduction-v36.md).

## What changed and what stayed fixed

The original v33 selector retained four absolute image centroids despite its
exclusion policy. Those eight mitotic fits are retained but excluded from gain
claims. A separately documented correction removes exactly four features, leaving
1,064. Full mitotic replay reproduced every retained sample value/identity, count,
sum and mean. The correction follows completed original fits and one incidental
logged MRR; it is not a fresh blinded or externally preregistered study.

Interphase processing then encountered a legitimate zero-row public shard,
Dataverse file 6421679. The preserved v35 failure is an implementation error, not
bad source data. V36 handles the empty shard with typed zero-length outputs,
preserves nonempty v35 processing, moves partial work aside and retains all 3,027
shard receipts. The repaired pipeline completed at 13:09:25 UTC; secondary controls
completed at 13:26:31 and final packaging at 13:28:06. Nothing was silently dropped.
[Correction](track2-optical-correction-v35.md), [empty-shard repair](track2-optical-empty-shard-v36.md).

The four real-label and four shuffled-label seeds per arm (3301-3304) each ran
3,000 steps with fixed splits, best validation checkpoint selection and no query
genes in fitting. A 512/256/128 GELU encoder uses 32-cell bags, 128 genes per step,
cross-guide InfoNCE, temperature 0.1, AdamW learning rate 0.0003 and weight decay
0.01. Source features are clipped to ±10, complete-guide summaries retained and
at most 128 cells per guide selected by a feature-independent identity hash.
Training-gene preprocessing, deterministic settings, BF16 autocast/FP32 parameters
and scores, and disabled TF32 are recorded in code. This is a purpose-built neural
benchmark, not a claim to a current state-of-the-art foundation model.

Evaluation requires at least 20 source cells per guide and two guides per gene;
training requires three. Query genes were fixed in advance. Own-target references
exclude the query guide; other target centroids use their eligible guides. Reference
guide counts differ. Exact ties receive average ranks. Macro MRR averages within
gene first; held-out genes, not cells, are the paired-bootstrap units. The practical
rule requires **every real seed** to gain at least 0.02 over the strongest simple
baseline, all paired lower bounds above zero, and a positive lower bound for the
minimum-over-seeds gain. Every draw reselects the strongest baseline.

## Complete cohorts and comparisons

| Arm | Complete cells | Sampled cells | Guide designs | Gene labels | Test genes |
|---|---:|---:|---:|---:|---:|
| mitotic | 838,224 | 832,846 | 20,404 | 5,050 | 950 |
| interphase | 31,046,046 | 2,609,447 | 20,445 | 5,050 | 994 |

Both exports completed without download errors: 97 mitotic files / 8,399,967,217
bytes and 3,029 interphase files / 321,585,666,869 bytes. The 2 metadata files in each
export are not counted as cell shards. Sixteen corrected fits, sixteen cross-plate
workers and sixteen complete-median workers all exited successfully. CPU/I/O stages
and brief GPU kernels mean these counts do not imply continuous saturation.

| Baseline | Mitotic macro MRR | Interphase macro MRR |
|---|---:|---:|
| basic_morphology | 0.017211631 | 0.086002829 |
| full_correlation | 0.047292179 | 0.233360551 |
| full_profile | 0.047518181 | 0.234112788 |
| guide_abundance | 0.014492086 | 0.010641173 |
| pca_whiten_128 | 0.040710371 | 0.197374188 |
| pca_whiten_256 | 0.034248714 | 0.180754152 |
| pca_whiten_64 | 0.046838199 | 0.213897730 |
| size_only | 0.009781271 | 0.018735922 |
| mitotic_fraction | 0.014026103 | 0.014829963 |
| matched_sample_mean | 0.047441097 | 0.093092657 |
| full_median_shared_preprocessing | 0.036678891 | 0.198041789 |
| full_median_training_preprocessing | 0.044255592 | 0.227001174 |

The original eight within-arm methods remain separate from the registered ninth
cross-arm fraction control. Matched-sample means and both complete-median views
were declared after mitotic results and before interphase fitting; they are
exploratory. Medians combine every source cell for each guide, never averages of
shard medians. The median-only preprocessing uses training genes and the original
feature mask; the shared view uses mean-derived scaling. Gene references still
average guide profiles, so this is not the source authors' complete median/PHATE
pipeline. All declarations and original comparisons remain intact.

| Arm / seed | Learned MRR | Shuffled MRR | Gain vs strongest original baseline | Original paired 95% interval |
|---|---:|---:|---:|---|
| mitotic / 3301 | 0.055121613 | 0.033272772 | 0.007603432 | 0.000138502 to 0.013516055 |
| mitotic / 3302 | 0.052095504 | 0.030085872 | 0.004577323 | -0.002100682 to 0.009697764 |
| mitotic / 3303 | 0.050421767 | 0.026842244 | 0.002903586 | -0.003707667 to 0.007969004 |
| mitotic / 3304 | 0.055476497 | 0.030544013 | 0.007958316 | 0.000613493 to 0.013732737 |
| interphase / 3301 | 0.143635847 | 0.056392886 | -0.090476941 | -0.103267489 to -0.078082234 |
| interphase / 3302 | 0.145884895 | 0.057045967 | -0.088227893 | -0.100780413 to -0.076206435 |
| interphase / 3303 | 0.148016742 | 0.061061330 | -0.086096046 | -0.099402267 to -0.073204234 |
| interphase / 3304 | 0.147027011 | 0.055548878 | -0.087085777 | -0.100216577 to -0.074562914 |

Mitotic: the registered nine-baseline joint interval is -0.003854558 to 0.007287330; the expanded twelve-baseline interval is -0.003886346 to 0.007251042. Both gates fail.

Interphase: the registered nine-baseline joint interval is -0.103595389 to -0.078746402; the expanded twelve-baseline interval is -0.103595389 to -0.078746402. Both gates fail.

The interphase neural models **do outperform the exactly matched 128-cell mean**
(0.093093) on point MRR. They still underperform full means (0.234113) and full
medians with training-median scaling (0.227001). Thus the result rejects a practical
full-data gain, not all representation benefit. The equal-information observation
is exploratory and does not replace the original strongest-baseline comparison.
Repeated seeds and bootstraps are dependent computational comparisons, not biological
replications or probabilities of efficacy.

## The favorable BUB1B result and its weaknesses

BUB1B interphase counts are 859/1,219/839/1,435; independent source reductions and
the separately distributed public workbook agree exactly. Mitotic counts are
11/15/11/25: only one guide reaches 20 cells, where two are required. BUB1B, BUB1,
MAD2L1, AURKB and PLK1 therefore have missing mitotic retrieval. Missing is not zero
and does not demonstrate a normal or abnormal biological effect.

| Interphase method | BUB1B guide ranks, in fixed guide order |
|---|---|
| full_profile | 1 / 3 / 3 / 2 |
| full_correlation | 1 / 3 / 3 / 2 |
| basic_morphology | 2 / 3 / 3 / 7 |
| size_only | 62 / 188 / 134 / 722 |
| guide_abundance | 240 / 399 / 253 / 783 |
| mitotic_fraction | 5 / 5 / 5 / 153 |
| matched_sample_mean | 1 / 3 / 4 / 8 |
| full_median_shared_preprocessing | 1 / 3 / 3 / 836 |
| full_median_training_preprocessing | 1 / 3 / 3 / 9 |
| learned seed 3301 | 1 / 3 / 3 / 780 |
| learned seed 3302 | 1 / 3 / 3 / 788 |
| learned seed 3303 | 1 / 3 / 4 / 776 |
| learned seed 3304 | 1 / 3 / 2 / 770 |
| shuffled seed 3301 | 2 / 2 / 464 / 191 |
| shuffled seed 3302 | 42 / 1 / 8 / 900 |
| shuffled seed 3303 | 1 / 4 / 7 / 475.5 |
| shuffled seed 3304 | 1 / 6 / 10 / 929 |

The full-mean best matches are BUB1B, MAD2L1, TTK and TTK. Shared checkpoint biology
is a plausible explanation; the signal is not uniquely BUB1B-specific. The fourth
guide changes from rank 2 under full means to 836 under shared-scale medians, 9 under
training-median scaling and 770-788 across real neural seeds. Three strong guides
cannot erase that disagreement. Guide efficacy, mixed cell states, off-target effects
and preprocessing are alternatives, not established explanations. Reused cells and
shuffled-label matches also preclude treating apparently strong directions as new
independent confirmations.

All ten queries remain visible. These are full-mean MRRs, not a comparison between
biologically interchangeable endpoints:

| Query | Mitotic MRR | Interphase MRR |
|---|---:|---:|
| BUB1B | missing | 0.541667 |
| BUB1 | missing | 0.265811 |
| MAD2L1 | missing | 0.375254 |
| CDC20 | 0.093750 | 0.002678 |
| TTK | 0.142857 | 0.253333 |
| AURKB | missing | 0.751712 |
| PLK1 | missing | 0.013451 |
| MTOR | 0.003630 | 0.875000 |
| RPTOR | 0.027818 | 0.625000 |
| RICTOR | 0.028204 | 0.660714 |

## Acquisition and class-selection alternatives

The registered cross-plate analysis separates query and reference plates and
excludes the own query guide from its target reference. The encoder and scaling
still use other training-gene cells from all plates; this is not an unseen-batch
training test. Full-cell and sampled-cell counts accompany every query. Interphase
BUB1B has four evaluated directions on every plate; results vary materially:

| Query plate | Reference genes | Full-mean BUB1B guide ranks |
|---|---:|---|
| 20200202_6W-LaC024A | 994 | 4 / 4 / 12 / 2 |
| 20200202_6W-LaC024B | 994 | 5 / 3 / 1 / 5 |
| 20200202_6W-LaC024C | 994 | 1 / 3 / 2 / 3 |
| 20200202_6W-LaC024D | 992 | 4 / 3 / 7 / 430 |
| 20200202_6W-LaC024E | 993 | 1 / 3 / 1 / 110 |
| 20200202_6W-LaC024F | 994 | 10 / 1 / 2 / 520 |
| 20200206_6W-LaC025A | 993 | 48 / 3 / 40 / 460 |
| 20200206_6W-LaC025B | 991 | 2 / 4 / 1 / 11 |

Changing reference cohorts prevent interpreting raw pooled-versus-plate MRR as a
gain. All seeds, shuffled workers and six methods per plate remain in the archive.
Mitotic plates have 0-2 eligible reference genes; none of the ten named queries
qualifies. Those scores cannot establish BUB1B acquisition robustness.

A **post-hoc** plate-only control was fixed after seeing favorable pooled BUB1B
ranks, before median/secondary scores. Plate proportions alone yield BUB1B ranks
138/907/397/119 and macro MRR 0.008337 in interphase. They do not reproduce the
favorable morphology ranks, but cannot exclude phenotype-specific batch effects.
The same plan's restriction to guides observed exclusively on one plate produces
zero eligible genes on every plate in both arms. It supplies no within-plate
validation; preserve the unsuccessful control design. It is separate from the
completed query-versus-other-plates analysis above and cannot change original gates.

Complete exports permit exact-guide mitotic/(mitotic+interphase) fractions. BUB1B's
fraction ranks 5/5/5/153 in interphase, not its 1/3/3/2 full morphology ranks. Those
are observed composition measurements, not viability. The source classifier uses
morphology and source normalization is within class. Entry, exit, cell loss and
classification can change the fraction; BUB1B-specific classifier error is unknown.
Fixed-cell HeLa images, transformed and lacking functional p53, cannot establish
all-enrolled daughter survival, useful non-cancer function, selected-allele effects
or joint drug response. Selected Cohen-Sharir results show relative sensitivities
can reverse at prolonged assessment; they do not test everolimus rescue.

## Numerical evidence and retained failures

Mitotic: independent CPU reductions cover all 40 named query guides, with maximum feature-sum error 0. Forty CPU/GPU median checks have maximum error 2.384185791e-07; secondary float64/float32 cosine error is 2.384185795e-07.

Interphase: independent CPU reductions cover all 40 named query guides, with maximum feature-sum error 2.273736754e-13. Forty CPU/GPU median checks have maximum error 5.960464478e-08; secondary float64/float32 cosine error is 2.3841858e-07.

The local archive replay verifies every member hash, recomputes rank-to-gene and
macro MRR with `math.fsum`, and reproduces all six original/registered/exploratory
real/shuffled paired comparisons per arm within 1e-12. It also rechecks all evaluated
cross-plate and post-hoc rank metrics. Interval replay reuses the registered
bootstrap routine and is not an independent statistical implementation. The
[replay receipt](track2-optical-local-replay-v36.json),
[workbook receipt](track2-optical-workbook-v36.json) and
[bound audit](track2-optical-audit-v36.json) record exact provenance.

The 3,535-file archive is 81,058,361 bytes, SHA-256
`a1e366c5c931a626c446c17de4d77fd15384e5c5730cd45e2f11c04f7d40ab8d`.
It includes public review records, code, provenance and failed attempts; source
parquet, checkpoints and prepared numeric matrices remain on the owner host.
A remote test invocation first hit the default temporary filesystem's space guard;
using the authorized root's TMPDIR passed 35 tests, followed by two plate-control
tests. That operational failure is retained. Successful arithmetic checks and
execution are not independent scientific or biological review.

## Decision and what would overturn it

Keep simple morphology as a candidate assay readout; do not promote the neural
model or everolimus from these retrieval results. Resolve guide disagreement with
independent perturbation/restoration and endogenous function. Distribute independent
designs across acquisition batches; qualify coverage before testing transfer. In
an intended non-cancer model, measure useful lineage function and all enrolled cell
fates through justified follow-up and recovery, then test drug plus deficit against
each alone. Prespecify independent confirmation and benefit/injury/exposure gates.

The [six falsification records](track2-optical-register-v36.json) and
[validation changes](track2-optical-validation-v36.md) make these consequences
executable/reviewable alongside the unchanged v21 decision contract. A new model
comparison would need an independently specified gain test and external-context
validation. Drug advancement additionally needs qualified joint-treatment evidence.
No rescue-priority drug, confirmed phase, clinical exposure margin, wet-lab result,
recording or submission receipt is supplied by this computation.
