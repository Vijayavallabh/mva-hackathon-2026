# Review the integrated Track 2 v26 proposal

Start with the [report](track2-report-v26.md), [nine slides](track2-slides-v26.html)
and [read-aloud transcript](track2-transcript-v26.txt). The [current artifact record](track2-current.json)
gives the PDF, workbook, immutable snapshot and recording-materials ZIP paths.

The proposal tests an optional everolimus mechanism after model qualification.
HT29's RNAi/CRISPR agreement strengthens an assay-development lead, with one guide,
one failed-QC batch and tumour-context limits. MCF7 has favorable drug/MTOR connections
but a failed BUB1B query that disagrees with RNAi. Different cells and separate
perturbations cannot establish joint rescue. No rescue-priority drug is supported.

```bash
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/track2_public_review_v26.py
```

Both checks use public files and the standard library without subject data, results,
credentials, network, GPUs or historical local snapshots. They verify internal
consistency, including 37 claim records, the three expression campaigns, slide/script
alignment and fixed scientific/delivery status. A passing check does not establish
biological efficacy or submission eligibility. The combined check additionally binds
current routing and the report/slide/workbook export audits.

The source analyses remain unchanged:

- [v19 transcriptomics](track2-transcriptome-v19.md): uncalibrated query filters,
  five-reagent HT29 exception and older compound identity/QC findings.
- [v23 RNAi](track2-rnai-v23.md): seed effects, six-reagent PRIME finding and
  finite-reference sensitivity on reused experiments.
- [v25 CRISPR](track2-crispr-v25.md): new BUB1B coverage, single-guide limitation,
  bidirectional retrieval, failed model/drug checks and source-well continuity.
- [v21 validation](track2-validation-v21.md), [v23 controls](track2-rnai-validation-v23.md)
  and [v25 controls](track2-crispr-validation-v25.md): independent perturbation and
  restoration, editing stress, joint functional response, fate, injury and exposure.

The full research archives retain numerical outputs, provenance and failed attempts.
GPU use was brief; no new model inference or biological validation is claimed.
The [integration review](track2-v26-integration-review.md) documents presentation scope
and the [readiness note](track2-owner-readiness-v26.md) lists remaining delivery items.

```bash
uv run python scripts/track2_release_v26.py verify results/feat009/jvv7_track2_research_v26
uv run python scripts/track2_bundle_v26.py verify
```

These stricter local commands also require retained historical releases and exported
files. The ZIP contains recording/review materials; it is not a recorded video.
