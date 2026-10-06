# Track 2 v31: a detectable BUB1B response is not a specific disease surrogate

**Decision:** the new non-cancer RPE1 evidence supports a measurable response to
BUB1B depletion, but does not qualify a BUB1B-specific rescue model. Keep RPE1 as a
candidate comparator for functional qualification. Do not promote a drug or infer a
shared response across cell types. This adds a direct challenge to the earlier
tumour-cell expression results; it does not invalidate every BUB1B perturbation model.

All eight H100s on the owner host completed the public-data campaign under
`~/v/mva-track2-perturbseq-20261007-v31`. There were **27,628,823,832 CUDA correlation
comparisons** and **2,048 split repetitions**, plus 13,421,574 CPU cross-cell comparisons.
These are dependent calculations, not independent experiments. Timed CUDA matrix
products summed to 6.476 seconds; worker wall times were 40–59 seconds. GPU use was
bursty, not sustained saturation. No new neural-model inference was performed.

## What was tested

We reanalyzed public [Replogle et al. CRISPRi data](https://doi.org/10.1016/j.cell.2022.05.013):
247,914 retained RPE1 cells and 310,385 K562 essential-screen cells. RPE1 is a
non-cancer, hTERT-immortalized retinal epithelial line; it is not the child's tissue.
The source differs from earlier LINCS experiments. **Both cell types use one shared
BUB1B paired-guide construct**, containing 106 RPE1 and 141 K562 cells. Neither two
guides in one construct nor hundreds of cells constitute independent perturbation designs.

The [plan](track2-perturbseq-plan-v31.json) was fixed before inspecting target expression
effects. A documented [amendment](track2-perturbseq-amendment-v31.json) removed a false
sensitivity: all retained non-targeting cells were already provider-selected core
controls. An unselected-control comparison is unavailable in this export. Four seed
blocks per cell replaced the duplicate control views, with 1,024 random splits per cell.

Common features were selected using control cells alone. Expression used log1p CP10k
with the original full-library UMI denominator and same-batch control centering.
Random halves used disjoint control cells. We retained all ten prespecified queries,
all reference constructs and three feature views. [Methods](track2-perturbseq-methods-v31.md)
describe the null, partition influence and source-count CPU checks.

## Results that change interpretation

After excluding the ten prespecified query genes (nine present in the selected matrix),
the remaining measured features number 4,852.
The narrower cell-cycle sensitivity retains 4,773 features.

| Test | RPE1 | K562 essential |
|---|---:|---:|
| BUB1B target/control CP10k ratio, matched by batch | 0.0487 | 0.0962 |
| BUB1B split-half median correlation, query transcripts removed | 0.6572 | 0.1197 |
| Median BUB1B retrieval rank, first direction | 171.5 / 2,154 | 323.5 / 2,077 |
| Median rank, reverse direction | 183 / 2,154 | 320 / 2,077 |
| First-direction BUB1B top-10 retrievals | 0 / 1,024 | 1 / 1,024 |
| MTOR median split-half correlation, same view | 0.8044 | 0.5928 |
| MTOR median retrieval rank, both directions | 1 | 1 |

The RPE1 BUB1B response is sizeable and internally repeatable, but many other
essential-gene responses resemble its held-out cells more closely. K562 BUB1B
split-half agreement is much weaker despite substantial target-transcript suppression.
Removing query and cell-cycle genes leaves median correlations of 0.6290 and 0.1166;
it does not produce distinctive BUB1B retrieval. MTOR's stronger behavior shows that
the dataset can support a repeatable expression response, while providing no validation
of the BUB1B query or drug efficacy.

**Cross-cell transfer is weak for BUB1B.** With query transcripts removed, its RPE1–K562
correlation is **0.1043**. Its corresponding ranks are **980/2,077** and **386/2,154**.
MTOR's correlation is **0.5836**, with ranks **1/2,077** and **2/2,154**. The cell types,
sampling days and CRISPRi effectors differ, so disagreement cannot be assigned to a
single cause. It does not support treating these expression signatures as interchangeable.

Both BUB1B expression-change norms exceeded all 1,024 batch-matched pseudo-perturbation
draws from the selected controls. This establishes only detectability relative to that
finite conditional reference. It does not establish target specificity, calibrated FDR
or biological rescue. The control-selection gap may make the reference optimistic.

The authors' RNA-derived BUB1B CNV scores are retained separately: 23.4426 in RPE1 and
8.6757 in K562. These are published expression-based estimates, not newly measured DNA
copy number, a karyotype, or evidence about the child. No cell-cycle occupancy labels
were available in the downloaded cell metadata; gene removal is a sensitivity analysis.

RICTOR has no perturbation cells in either export. RPE1 CDC20 and AURKB lack the
prespecified 30-cell coverage for retrieval. RPTOR has 30 RPE1 cells, but its transcript
is absent from the exported measured-gene matrix. Preserve these distinct missing-data
states; do not replace them with negative effects or zero scores.

## Consequences for the solution

1. **Require functional attribution before drug matching.** Add independent BUB1B
   suppression and an appropriate restoration comparison; measure protein, division
   errors, daughter survival and later non-cancer function. A strong expression shift
   alone does not meet this requirement.
2. **Keep perturbation detectability separate from specificity.** Report both even
   when one is favorable. No post-hoc top-10 threshold was used to declare biological
   success or failure.
3. **Measure pathway direction in the actual qualified model.** Tumour BUB1B–mTOR
   findings and non-cancer depletion can have different implications. MTOR knockdown,
   everolimus treatment and joint treatment of a BUB1B deficit are separate experiments.
4. **Retain safety and exposure gates.** The refreshed literature contains both
   contrary mechanistic evidence and context-specific favorable findings. The
   [source review](track2-perturbseq-source-review-v31.md) translates them into
   endpoint and interpretation requirements without transferring clinical results
   across diseases.

Everolimus remains an optional, model-qualified mechanistic probe; HCQ remains reserve.
There is no rescue-priority drug, confirmed trans phase, clinical exposure margin or
new wet-lab result. This work does not establish a treatment for the child. All earlier
findings and dispositions remain in force, including v29's failed protein controls and
HT29's limited assay evidence. Presentation v30 remains frozen and predates this addendum.

## Audit trail

- [Complete public results](track2-perturbseq-results-v31.json): all ten query states,
  split distributions, conditional null summaries, both cross-cell rank directions,
  partition sensitivities, source summaries and full-panel context.
- [Source searches](track2-perturbseq-sources-v31.json) and
  [source review](track2-perturbseq-source-review-v31.md): 98 returned titles screened,
  selected abstracts/passages read, unavailable full texts and failed requests explicit.
- Exact plans, executed scripts, original matrices of full-profile comparisons,
  all per-repeat query records and logs are retained in the v31 audit archive.
- CPU FP64 reconstruction from original counts agreed within 2.83×10⁻⁶ for checked
  query profiles; correlation-dot-product checks were within 4.50×10⁻⁷. Passing numerical
  checks establish arithmetic agreement, not biology.

All inputs were public. No raw subject data or clinical narrative left the original
machine. No new hosted biological-model provider, family contact, submission or video
recording occurred. The remote folder and its caches remain in the **24 November 2026**
deletion scope. Existing provider, licensing and delivery gaps remain open.
