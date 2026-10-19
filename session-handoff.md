# Session handoff: corrected optical validation v35; interphase pipeline active

Only **feat-009** is active. Presentation/harness v34 remain the latest immutable
release. Current routes in `notes/track2-current.json` add the mandatory v35
correction and failed mitotic comparison. Read `notes/track2-optical-correction-v35.md`
before using the old presentation. Do not edit any v33/v34 bound file.
The current presentation files are `notes/track2-report-v34.md`,
`notes/track2-slides-v34.html`, `notes/track2-pitch-v34.md` and
`notes/track2-transcript-v34.txt`; use them with the correction above.
The combined reviewer entry points remain `scripts/track2_public_review_v34.py`,
`notes/track2-reviewer-guide-v34.md` and the original assay-qualification report
`notes/track2-transcriptome-v19.md` alongside later research addenda.

## Completed this session

- Found four absolute centroid columns in the original 1,068 v33 features. This
  violated the registered policy. Preserve and exclude those original fits from
  gain claims; the v33 blanket coordinate-exclusion statement is superseded.
- V35 preparation retains 1,064 features. Exact full mitotic replay verifies all
  retained sample identities/values, complete guide counts, sums and means.
- Eight corrected 3,000-step fits completed on eight H100s: real seeds 3301–3304
  plus four shuffled controls. Source clipping, sample cap, gene split and model
  settings are unchanged; no query-driven tuning.
- The practical gain gate fails across 950 held-out genes/3,164 guide queries.
  Strongest simple baseline MRR 0.047518; real models 0.050422–0.055476. Gains
  0.002904–0.007958 fall short of 0.02; two paired intervals and the joint interval
  include zero. Shuffled controls 0.026842–0.033273. All outputs are retained.
- Independent CPU `math.fsum` reductions verify all 40 guides in the ten queries.
- Eight plate-sensitivity workers completed. Each plate has only 0–2 eligible
  test/reference genes. None of the ten queries qualifies on any plate. Do not
  interpret the two-gene scores as confirmation or compare them to the 950-gene pool.
  Weighted plate embeddings agree with pooled embeddings within 5.087e-7.
- BUB1B counts remain 11/15/11/25; only one meets 20 cells, while two guides are
  required. Missing evidence is not a negative biological effect.
- No rescue-priority drug, phase, exposure, wet-lab or clinical update.

Recheck locally:

```bash
uv run --no-project python scripts/check_track2_optical_correction_v35.py
uv run --no-project python scripts/check_track2_harness.py
uv run python scripts/track2_release_v34.py verify results/feat009/jvv7_track2_research_v34
```

The local review archive is `results/feat009/optical-v35/mitotic/mitotic-v35-review.tar.gz`:
118 files, 14,235,350 bytes, SHA-256
`5ac610082576059c8fccf132308c723873df90ca76ca4a069abe9aa3cd3a88e6`.
It contains public JSON review records, script/environment provenance and source
manifests. Checkpoints and prepared numeric arrays remain on the owner host; this
is not an archive of the entire raw public dataset or model binaries.

## Live owner-hosted work — do not duplicate

Host `PrakashDGX_H2`; root `/home/prachh/v/mva-track2-optical-20261019-v33`.
All processing/caches stay under that root, using `/home/prachh/v/bin/uv` and the
existing isolated environment. No protected subject data was transferred.

At 12:21 UTC, 2,018/3,029 files (214,264,876,807 bytes) were downloaded without
reported errors; free space was 388,122,353,664 bytes. This is a historical status,
not current completion. The pipeline Python PID is **546535**.

The original interphase downloader Python PID is **4156734**. A separate
`track2_optical_finish_v35.py` supervisor waits for its complete checksum-bound
manifest. It then runs, sequentially:

1. Corrected interphase preparation with eight CPU workers.
2. Independent CPU query reductions.
3. Four real and four shuffled fits on eight idle H100s.
4. Fixed gene-level comparison against all eight within-arm baselines.
5. Eight plate-sensitivity workers.

It refuses partial coverage, changed registered scripts, occupied GPUs after a
bounded wait, storage over 450 GB or free space below 128 GiB. It never restarts
the downloader, stops another process or overwrites an existing wave. Do not
modify its registered scripts while this pipeline is active. The plain v33 model
must never be used for the interphase arm.

Authoritative status:

```bash
ssh PrakashDGX_H2 'cd /home/prachh/v/mva-track2-optical-20261019-v33 && cat outputs/download-interphase-status.json && cat outputs/interphase-v35-pipeline/status.json'
```

Pipeline registration/status/terminal files: `outputs/interphase-v35-pipeline/`.
Log: `logs/interphase-v35-pipeline.log`. Completed corrected mitotic paths are
`prepared-v35/mitotic`, `models-v35/mitotic-*`, `plate-v35/mitotic-*`,
`outputs/wave-v35-mitotic` and `outputs/wave-plates-v35-mitotic`. Old `prepared/`,
`models/` and `outputs/wave-mitotic` remain preserved historical work.

If a tool call times out, inspect process identity and these receipts before
considering a restart. A pending download is not a blocker while independent work
is possible; the overall research goal remains active.

## Next bounded work

- Continue from the active pipeline; inspect its failed/finished receipt and every
  worker return code. Verify complete interphase BUB1B counts independently against
  the source workbook's 859/1219/839/1435; do not assume agreement.
- Run `track2_optical_plate_summary_v35.py . --arm interphase` after plate completion.
  The pipeline does not invoke this final condensation step.
- Implement the already-declared cross-arm mitotic-fraction control and the
  exploratory matched-128-cell mean diagnostic in
  `notes/track2-optical-secondary-plan-v35.json`. The latter was declared after
  mitotic results but before interphase fitting. It cannot rescue the failed
  primary mitotic gate. Preserve original primary metrics and all seeds.
- Validate all gains against the strongest simple baseline, not just a favorable
  comparator. Query specificity, reference-cohort sizes, plate coverage, sampling
  information and HeLa/p53 limitations must remain explicit.
- Audit the full evidence, bind retained records and update the research summary,
  falsification decisions and harness. Then integrate finished findings into a new
  presentation/report/transcript version and render/inspect it. Preserve v34.
- Carbon was reviewed and deferred as irrelevant to functional rescue. The
  unchanged Anthropic toolkit already ran extensive ProteinMPNN inference in v29;
  failed functional controls remain. Do not rerun unrelated models to force gain.

## Official requirements and blockers

- The October 19 source refresh covers seven files at revision
  `60e1c30e337ce6fe01813040dbe49979eb8c50aa` and 29 public threads/83 visible comments.
  Four changed/new comments were reread. Unchanged text retains previous review.
  No independent reviewer, account, quota, live-rendering or receipt check occurred.
- Submission remains **October 24, 23:59 UTC**. The active deletion/confirmation
  deadline is **November 23**, recipient **cnb@sagebase.org**. Use
  `notes/deletion-plan-v2.md`; old frozen dates and addresses are superseded.
  Feat-010 remains not started; no deletion or email occurred.
- No rescue-priority drug. Everolimus remains an optional model-qualified probe;
  HCQ reserve. Phase, endogenous effects and clinical exposure margins remain unknown.
  Independent perturbation/restoration, non-cancer function and joint drug treatment
  are still missing. No computational score supplies those measurements.
- Keep invalid assays, imprecision, futility and safety failure distinct. Unknown
  evidence means HOLD; safety failure overrides benefit. All-pass allows preclinical
  review only. Tumour killing requires separate deficient-normal controls.
- Balnis ex vivo units conflict by 1,000-fold; both values remain quarantined.
- Fireworks/earlier alignment-service handling and linked AF3/non-AVI Atlas versus
  challenge CC BY scope remain unresolved. OpenAI no-training is owner attestation.
- Recording, measured runtime, hosting, owner/live-portal checks and Track 2 receipt
  remain open. Three entries, latest only reviewed; quota unknown. No upload occurred.
- Preserve submitted Track 1 v4. Owner-reported 100/F-max 1 is an attestation; its
  receipt/byte verification is separate. Do not request another upload.

No family contact or re-identification. Keep the purge guard, commit intended changes,
push configured origin and verify upstream equality. The overall research goal is
not complete merely because this presentation update is complete.
