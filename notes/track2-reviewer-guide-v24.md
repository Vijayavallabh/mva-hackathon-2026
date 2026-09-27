# Track 2 v24 reviewer guide

The [report](track2-report-v24.md), [nine slides](track2-slides-v24.html),
[342-word narration](track2-pitch-v24.md), [plain transcript](track2-transcript-v24.txt)
and [video description](track2-video-description-v24.md) integrate the completed
v19 expression campaign and v23 RNAi analysis. The [current record](track2-current.json)
lists the PDF, methods workbook, snapshot and recording-materials ZIP.

Start with the RNAi section and slide 4. They retain seed-associated similarity,
the favorable six-reagent HT29 PRIME result and its finite-reference sensitivity.
The v19 five-reagent HT29 finding is a separate result. Both analyses reuse public
experiments; no independent BUB1B experiment or drug benefit is established.
The [qualification addendum](track2-rnai-validation-v23.md) specifies the resulting
controls. Drug/biological decisions remain v21; all clinical margins remain null.

## Public consistency checks

```bash
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/track2_public_review_v24.py
uv run --no-project python scripts/check_track2_rnai_v23.py
uv run --no-project python scripts/check_track2_transcriptome.py
```

The first command checks current routes, versions, scientific boundaries and export
provenance. The second checks the versioned presentation, report/methods/disclosure,
exact narration alignment, both frozen research campaigns, and the 27+5 claim records.
The last two inspect each research campaign separately. These use public CPU inputs
without subject files, data/results folders, credentials, network, GPUs, model weights
or Git history. Passing verifies internal consistency, not biology or eligibility.

The isolated runtime audit copies public files and blocks network, process launch,
protected paths, credentials, unrelated external paths and writes through Python audit
hooks. This is a dependency check, not an operating-system security boundary:

```bash
uv run --no-project python scripts/audit_track2_harness.py --output NEW-AUDIT.json
```

## Exports and immutable releases

```bash
uv run node scripts/render_track2_slides_v24.mjs NEW-SLIDE-DIRECTORY
uv run scripts/track2_export_documents_v24.py NEW-DOCUMENT-DIRECTORY
uv run node scripts/render_track2_report_v24.mjs NEW-DOCUMENT-DIRECTORY
uv run python scripts/track2_release_v24.py verify results/feat009/jvv7_track2_research_v24
uv run python scripts/track2_bundle_v24.py verify
```

Use new directory names for rendering/export. Renderers run isolated offline Chrome
on fixed local content. The methods export uses the pinned official workbook, fills
B7-B17, preserves its questions and Track 1 styles, and comments on the stale quota
instruction. B9 exactly matches the video description; B17 is 227 words.
The workbook is a review artifact; the report is the PDF/Markdown submission format.

The release binds all earlier v22 inputs and the frozen v23 audit's public inputs.
Its verifier also checks the retained local historical snapshots, so it requires
`results/` unlike the public checker. Earlier versions are never overwritten.
The recording ZIP includes the new presentation plus the v19 narrative/figure/guide,
v21 decision materials and v23 narrative/figure/qualification/register/sensitivity.
It is not a recorded video or receipt.

Full research reproduction and large-array archive verification remain documented in
[the v19 guide](track2-transcriptome-reproduction-v19.md) and
[the v23 report](track2-rnai-v23.md). The v23 archive has 161 files; omitted large arrays
remain hash-inventoried on the owner host. Numerical spotchecks verify arithmetic,
not independent scientific review.

[Owner readiness](track2-owner-readiness-v24.md) lists the remaining video, provider,
distribution, live-portal and receipt work. Requirements/community coverage remains
the dated September 24-25 review. Never infer quota or resubmit Track 1 to resolve its
administrative receipt gap.
