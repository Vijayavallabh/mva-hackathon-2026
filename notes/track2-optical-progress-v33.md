# Public optical phenotypes: research status, 19 October 2026

This is an in-progress study, not a validated model result. The question is whether
independent imaging features and guide designs can improve BUB1B assay qualification
beyond the weak target specificity in the completed expression analyses.

The [fixed plan](track2-optical-plan-v33.json) and
[separate amendment](track2-optical-amendment-v33.json) precede full model fitting.
They specify held-out genes, four seeds, shuffled training controls and comparisons
with cell abundance, basic morphology, full profiles and PCA whitening. The ten
query genes never enter training or checkpoint selection. The numerical gain rule
is an engineering criterion; passing it cannot establish drug response or rescue.

## Verified preparation

The public Funk et al. dataset, Harvard Dataverse version 2.0,
[10.7910/DVN/VYKTI5](https://doi.org/10.7910/DVN/VYKTI5), is CC BY 4.0.
All 97 mitotic files passed provider size/MD5 and local SHA-256 checks.
Preparation retained 838,224 cells, 20,404 guide labels and 1,068 numerical features.
Deterministic sampling retains at most 128 cells per guide; full counts and feature
sums remain available. Source normalization is reused. Coordinate and identifier
columns are excluded from learning. These are unrelated public HeLa cells, not
subject data or the selected alleles. HeLa lacks functional p53.

BUB1B mitotic guide counts are **11, 15, 11 and 25**. Only one guide meets the
fixed 20-cell minimum; evaluation needs at least two. BUB1B mitotic retrieval is
therefore **missing for insufficient guide coverage**, not zero or evidence against
BUB1B biology. The original workbook's interphase counts are 859, 1,219, 839 and
1,435; complete interphase preparation must independently check them.

## Compute and outstanding validation

The remote root is `/home/prachh/v/mva-track2-optical-20261019-v33`. An isolated
environment and all caches remain there. Eleven preparation/retrieval tests passed
on the owner host. A separate two-step GPU smoke run completed; its metrics are
excluded from scientific interpretation. At 11:43 UTC, eight mitotic workers were
launched: real-label seeds 3301-3304 on GPUs 0-3 and the four matched shuffled controls
on GPUs 4-7. The interphase download was still in progress. These launch records do
not establish completion, sustained utilization or improvement over baseline.

The public [status snapshot](track2-optical-status-v33.json) binds preparation and
launch receipts. Live status is under `outputs/wave-mitotic/` and
`outputs/download-interphase-status.json` on the host. Do not restart an existing
wave merely because an SSH call timed out. The supervisor records worker exits and
GPU utilization. Read current status before allocating devices.

Full-model aggregation, held-out-plate sensitivity, cross-arm count controls,
independent CPU checks and the baseline gain assessment remain unfinished. The
interphase arm must finish download/preparation before its registered eight-worker
wave. Keep the original thresholds after observing missing coverage. Record failures
and weak results with the same detail as favorable ones.

Morphology can reflect abundance, size, DNA content, stress or survivor selection.
The source live-cell sub-screen excludes incomplete tracks and combines some fate
classes; it cannot supply our required all-enrolled daughter-survival endpoint.
Independent perturbation/restoration and direct joint treatment remain necessary.
[Source review](track2-optical-source-review-v33.md).

No rescue-priority drug, phase, clinical margin or biological validation is added.
The [November 23 deletion plan](deletion-plan-v2.md) includes this remote root and
its caches. No protected reads, VCF records or clinical narrative were transferred.
