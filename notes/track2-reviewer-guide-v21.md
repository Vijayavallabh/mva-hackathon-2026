# Review the integrated Track 2 v21 materials

27 September 2026. Read the [report](track2-report-v21.md),
[eight-slide deck](track2-slides-v21.html) and [335-word narration](track2-pitch-v21.md).
The [plain transcript](track2-transcript-v21.txt) matches each slide. Two result slides
and the report's third section integrate the completed [v19 expression analysis](track2-transcriptome-v19.md).
The [artifact record](track2-current.json) lists the PDF, workbook, PNG and bundle paths.

## Public consistency checks

```bash
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/track2_public_review_v21.py
```

The first checks current routes and status; the second checks frozen v21 presentation
content, methods, narration, source records, v21 falsification and decision-contract checks and the hash-bound v19
campaign. Both run on a CPU without subject data, results folders, credentials, network,
SSH, model weights or GPUs. They check consistency, not efficacy or eligibility.

The dependency audit uses a temporary public-only copy and the uv interpreter's base
installation. Six probes test its Python audit guards. This is not an operating-system
sandbox assessment or a scientific replication:

```bash
uv run --no-project python scripts/audit_track2_harness.py
uv run --no-project python scripts/audit_track2_public_v21.py
```

## Rebuild exports in new directories

```bash
uv run node scripts/render_track2_slides_v21.mjs new-v21-slides
uv run scripts/track2_export_documents_v21.py new-v21-documents
uv run node scripts/render_track2_report_v21.mjs new-v21-documents
```

Renderers require Node/Chrome and use isolated offline profiles. The export uses the
original hash-verified methods workbook, preserves questions and the Track 1 sheet,
and fills B7-B17. The official template's stale one-entry text is preserved with a
comment explaining the reviewed three-entry rule. No formulas execute.

Exact local snapshot/bundle checks additionally require retained historical releases
and rendered outputs; they are intentionally separate from the public CPU check:

```bash
uv run python scripts/track2_release_v21.py verify results/feat009/jvv7_track2_research_v21
uv run python scripts/track2_bundle_v21.py verify
uv run --no-project python scripts/verify_track2_transcriptome_archive.py results/feat009/transcriptome-remote-v19/transcriptome-v19-audit.tar.gz
```

The recording ZIP contains the integrated report, methods, eight slides/PNGs, script,
transcript, disclosure, guides, the v21 falsification review/validation/contract/evidence
and the v19 narrative/figure/reproduction note. The
research snapshot binds the entire public campaign plus prior sources; the separate
457-file archive retains large computational outputs. See the
[execution record](track2-transcriptome-reproduction-v19.md) for full rerun instructions
and matrices omitted from that archive. Existing versions must not be overwritten.

## Findings and limits to keep together

- Primary query gates pass 0/14 under an uncalibrated operational filter. Post-hoc
  full filters pass 0/42, while HT29 retains a five-reagent adjusted-tail 0.042 result.
- Primary everolimus correlations are positive in 13/19 comparisons reusing fourteen
  profiles at 10 µM nominal culture concentration; correlation does not prove harm.
- Of 180 second-release everolimus-labelled profiles, 174 have unresolved stereo
  metadata. All six reference-matching 0.1 µM profiles fail specified drug QC.
- All eight H100s completed three waves, but kernels were bursty. Computational
  profile/comparison/resample counts are not independent biological experiments.

The v21 amendment preserves the v15 drug dispositions and adds sharper qualification requirements. Qualify endogenous
function and independent genetic controls, then test drug plus the deficit directly.
Keep all cell fates and sustained function; separate tumour killing from non-cancer
benefit. No drug earns rescue priority, phase and clinical margins remain unknown,
and no wet-lab result is claimed. The [readiness note](track2-owner-readiness-v21.md)
separates remaining video/provider/delivery work from biological qualification.
Requirements/community evidence is dated September 24-25; v21 does not claim a new
complete website/discussion audit.
