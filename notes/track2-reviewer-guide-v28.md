# Track 2 v28 reviewer guide

Start with [the report](track2-report-v28.md), [nine slides](track2-slides-v28.html)
and [330-word script](track2-pitch-v28.md). All integrate the completed v27 protein
background and expression-specificity results. The [current state](track2-current.json)
points to the PDF, methods workbook, plain transcript and recording-materials ZIP.

```bash
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/track2_public_review_v28.py
uv run --no-project python scripts/check_track2_falsification_v27.py
uv run python scripts/track2_release_v28.py verify results/feat009/jvv7_track2_research_v28
uv run python scripts/track2_bundle_v28.py verify
```

The first three commands use tracked public files and standard-library CPU code;
they need no subject data, credentials, network, GPU, weights or archived runs.
Strict release/bundle verification also checks local exports and historical packages.
The isolated check is `uv run python scripts/audit_track2_harness.py`. Its Python
audit guards test dependency isolation, not operating-system sandbox security.

The combined check retains 42 claim records across four registers, eleven unchanged
drug dispositions and frozen v19/v21/v23/v25/v27 findings. These are not 42 studies.
HT29 retains retrieval ranks 2–5 across five post-hoc views; MCF7 BUB1B drug reversal
weakens from 7 to 1,184 while MTOR stays first. Projection can remove real biology;
competing targets contribute to its fit. Protein-score backgrounds limit negative-sign
interpretation while preserving favorable matched N→K evidence. Failed controls and
query QC remain visible. Numerical consistency does not establish functional rescue.

The [v27 reproduction guide](track2-falsification-reproduction-v27.md) covers original
archive verification and analysis. Earlier routes remain in the [v26 guide](track2-reviewer-guide-v26.md).
All earlier bound sources/releases are preserved. New inference was completed in v27;
this integration did not rerun it. No owned GPU jobs remain.

See [readiness](track2-owner-readiness-v28.md) for outstanding provider/distribution,
video/runtime/hosting, live-portal and receipt items. All clinical margins remain null.
