# Optical validation correction — 19 October 2026

Public inputs: [Funk et al., Cell](https://doi.org/10.1016/j.cell.2022.10.017),
[Dataverse version 2.0](https://doi.org/10.7910/DVN/VYKTI5), CC BY 4.0.
The [source review](track2-optical-source-review-v33.md) records reading depth and
the fixed-cell and live-lineage limitations.

The original v33 selector retained four absolute image centroids:
`nucleus_centroid_r`, `nucleus_centroid_c`, `cell_centroid_r` and
`cell_centroid_c`. That contradicts the registered exclusion of absolute
coordinates. The v33 progress note's blanket statement that coordinates were
excluded is incorrect. Preserve those files and runs as historical records;
exclude the original fitted models from any gain claim.

The [correction amendment](track2-optical-amendment-v35.json) records discovery
after eight mitotic fits finished. One incidental learned MRR appeared in a log;
the full model/baseline comparison had not been inspected. This is a documented
implementation correction, not external preregistration or a fresh blinded study.

V35 removes only those four input features, leaving 1,064. The source clipping,
complete-guide counts, deterministic cell selection, gene splits, training
parameters and fixed query coverage thresholds remain unchanged. A full mitotic
replay must reproduce every retained sample value, sample identity, guide count,
feature sum and mean before corrected fitting. All four real-label seeds and
four shuffled controls are rerun. The original v33 outputs remain intact.

The revised preparation also saves complete per-guide/per-plate counts and
feature summaries. Plate-separated retrieval must use different acquisition
plates for query and reference. The pooled encoder has seen training-gene cells
from all plates, so this is not a fully unseen-acquisition test. Sparse query
coverage stays missing. The sampled-cell counts must accompany learned plate
profiles; they are smaller than the complete-cell baseline counts.

The basic-feature baseline's declared names match the source schema. Add explicit
size-only and within-profile-centered correlation comparisons. Compare every
learned seed against the strongest simple baseline. Paired resampling uses
held-out genes, recomputes the strongest baseline within each draw, and reports
both per-seed and minimum-over-seeds intervals. No cell-level pseudo-replication.

A suspected storage problem was checked rather than assumed: the 95 mitotic
shards contain 20,404 guide records in total, equal to the distinct-guide count.
The complete preparation occupies 8,063,718,534 bytes. Three downloaded interphase
shards contained 1, 8 and 5 guides. These observations support retaining sharded
preparation with a free-space guard; they do not establish the final footprint.

Commands on `PrakashDGX_H2`, rooted at
`/home/prachh/v/mva-track2-optical-20261019-v33`:

```bash
/home/prachh/v/bin/uv run --no-sync python scripts/track2_optical_prepare_v35.py . --arm mitotic --workers 8
/home/prachh/v/bin/uv run --no-sync python scripts/track2_optical_audit_v35.py . equivalence
/home/prachh/v/bin/uv run --no-sync python scripts/track2_optical_run_v35.py . --arm mitotic
```

Tests use `TMPDIR` beneath this remote root. The first remote test attempt hit
the free-space guard on the default temporary filesystem; no production job ran
from that attempt. All ten v35 preparation, mathematical and gain-gate tests
then passed with the authorized temporary directory.

## Corrected mitotic result

The [full replay](track2-optical-equivalence-v35.json) passed exactly for every
retained value, sample identity, count, sum and mean. All eight corrected fits
completed. [Independent CPU reductions](track2-optical-independent-mitotic-v35.json)
reproduced all 40 query-guide counts and finite-feature counts; feature sums agreed
within the fixed 1e-7 tolerance. These checks validate arithmetic and preservation.

The [mitotic comparison](track2-optical-mitotic-results-v35.json) contains all
eight baselines, four real-label seeds, four shuffled controls and query results.
It evaluates 950 held-out genes through 3,164 guide queries. The strongest simple
baseline is the full-profile cosine mean reciprocal rank (MRR), **0.047518**.

| Seed | Learned MRR | Gain over strongest baseline | Paired 95% interval |
|---|---:|---:|---:|
| 3301 | 0.055122 | 0.007603 | 0.000139 to 0.013516 |
| 3302 | 0.052096 | 0.004577 | −0.002101 to 0.009698 |
| 3303 | 0.050422 | 0.002904 | −0.003708 to 0.007969 |
| 3304 | 0.055476 | 0.007958 | 0.000613 to 0.013733 |

All four fail the fixed **0.02** practical gain requirement. Two paired intervals
include zero; the minimum-over-seeds interval is **−0.003855 to 0.007287**.
The 20,000 resamples use genes and reselect the strongest simple baseline within
each draw. These are dependent seed comparisons, not four biological replications.
Shuffled-control MRRs are 0.026842–0.033273. Real labels improve the point estimates,
but this does not satisfy the declared practical gain rule or qualify BUB1B biology.

A [local replay](track2-optical-local-replay-v35.json) verified the 118-file public
review archive, recomputed every method's gene and macro MRR from guide ranks,
and reproduced both real and shuffled paired intervals within 1e-12. Commands:

```bash
uv run python scripts/track2_optical_archive_review_v35.py results/feat009/optical-v35/mitotic/mitotic-v35-review.tar.gz results/feat009/optical-v35/mitotic/mitotic-v35-review-manifest.json --output results/feat009/optical-v35/local-replay-check.json
uv run --no-project python scripts/check_track2_optical_correction_v35.py
```

BUB1B, BUB1, MAD2L1, AURKB and PLK1 are missing for insufficient guide coverage.
CDC20, TTK, MTOR, RPTOR and RICTOR are evaluated; all eligible directions are retained.
Do not substitute their results for the missing BUB1B result. Adding the pending
mitotic-fraction baseline cannot turn this failed strongest-baseline gate into a pass.

All eight plate-sensitivity workers completed. The
[plate audit](track2-optical-plates-mitotic-v35.json) exposes another coverage limit:
each acquisition plate has only **0–2** eligible test/reference genes under the
20-cell, two-guide rule. None of the ten named query genes qualifies on any plate.
This cannot assess BUB1B plate robustness. The two-gene retrieval scores are retained
without interpreting them as confirmation or comparing them with the 950-gene pool.

The encoder uses at most 128 cells per guide while the full-profile baseline uses
all cells. The primary comparison tests practical performance; it does not isolate
representation quality from sample size. A separately declared
[secondary analysis](track2-optical-secondary-plan-v35.json) will add matched-sample
means after both exports complete. It cannot retroactively rescue this failed gate.

Interphase completion, cross-arm counts and integrated review remain pending.
The frozen v34 presentation is a progress snapshot and must be read with this
correction. No drug, phase, clinical-exposure or biological-validation decision changes.

## Consequence for the proposal

Keep the mitotic neural profile out of drug-ranking decisions. Retain the simple
full-profile comparator, and qualify interphase imaging independently. Before a
joint drug experiment, establish enough independent perturbation/restoration designs
and cells for the chosen endpoint. If coverage fails, revise collection or the assay
before treatment testing; preserve the failed coverage decision. Track enrolled
cells through division and daughter fate so loss of abnormal cells cannot masquerade
as functional recovery. These requirements refine the experiment; this public HeLa
analysis supplies neither non-cancer rescue nor selected-allele validation.
