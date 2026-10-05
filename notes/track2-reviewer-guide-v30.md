# Track 2 v30 reviewer guide

Start with [the report](track2-report-v30.md), [nine slides](track2-slides-v30.html)
and [326-word script](track2-pitch-v30.md). All integrate the completed
[v29 structural and held-out expression results](track2-orthogonal-v29.md).
The [current state](track2-current.json) points to the PDF, methods workbook,
plain transcript and recording-materials ZIP.

```bash
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/track2_public_review_v30.py
uv run --no-project python scripts/check_track2_orthogonal_v29.py
uv run python scripts/track2_release_v30.py verify results/feat009/jvv7_track2_research_v30
uv run python scripts/track2_bundle_v30.py verify
```

The first three commands use public files and standard-library CPU code; they need
no subject data, credentials, network, GPU, weights or archived runs. Strict release
and bundle verification also checks local exports and historical packages. The
isolated check is `uv run python scripts/audit_track2_harness.py`. Its Python audit
guards test dependency isolation, not operating-system sandbox security.

The combined check retains 47 claim records across five registers, eleven unchanged
drug dispositions and frozen v19/v21/v23/v25/v27/v29 findings. These are not 47 studies.
ProteinMPNN control ordering passes 1/24 primary and 0/24 expanded comparisons.
Four related checkpoint sets and repeated backbones do not independently establish
function. D882N control interpretation depends on the measured endpoint; the
catalytic disagreement remains unresolved.

HT29 PRIME agreement survives CRISPR QC restriction and symmetric held-out fitting.
Its adjusted correlation spans 0.1223-0.1371. RNAi ranks 1-6 and CRISPR ranks 1-3
use 715-781 and 276-340 reference genes respectively. These dependent partition
ranges are not confidence intervals; ranks are not comparable with prior full panels.
One guide, RNAi uncertainty and tumour context still limit the assay lead. MCF7
has no qualified BUB1B query after QC restriction. Its all-profile drug reversal
weakens while MTOR remains first. No joint functional rescue was measured.

The [v29 reproduction guide](track2-orthogonal-reproduction-v29.md) describes the
3,838-file archive and complete local reanalysis. Earlier routes remain in the
[v28 guide](track2-reviewer-guide-v28.md). All earlier bound sources and releases
are preserved. No inference was rerun for this presentation update. No owned GPU
jobs remain.

The [October 6 requirements refresh](track2-requirements-review-v30.md) covers
26 public threads and 79 visible comments by comparison with the earlier review.
Twelve new or edited comments were reread; there was no independent reviewer.
See [readiness](track2-owner-readiness-v30.md) for provider/distribution,
video/runtime/hosting, portal and receipt items. All clinical margins remain null.
