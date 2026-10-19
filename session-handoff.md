# Session handoff: Track 2 v34 materials and pending v33 optical research

19 October 2026 IST, session 72. Only feat-009 is active. Use
`notes/track2-current.json`, `scripts/check_track2_harness.py` and
`notes/track2-reviewer-guide-v34.md`. Presentation/harness v34 retain completed
v19/v21/v23/v25/v27/v29/v31 findings and explicitly pending v33 model validation.
The original expression record remains `notes/track2-transcriptome-v19.md`.

The owner emphasized announcement 28 and competitive delivery. Follow
`notes/track2-competition-strategy-v34.md`: prioritize supported mechanism, functional
impact, a demonstrable reusable method and the recording/submission deadline.
Track 1 recognition is separate from Track 2 panel prizes.

## Current deliverables

`notes/track2-report-v34.md`, `notes/track2-slides-v34.html`,
`notes/track2-pitch-v34.md`, `notes/track2-transcript-v34.txt` and video description
are synchronized. Nine slides, 336 narration words and eleven methods fields with
an abstract of 356 words. The optical slide displays verified guide counts and
missing coverage; detailed drug matching remains in the report. Runtime is unmeasured.
Export/snapshot/ZIP paths are in the current state. Preserve every older bound file.

```bash
./init.sh
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/check_track2_optical_progress_v33.py
uv run python scripts/audit_track2_harness.py
uv run python scripts/track2_release_v34.py verify results/feat009/jvv7_track2_research_v34
uv run python scripts/track2_bundle_v34.py verify
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
```

Final verification and real fresh-shell init output are in progress.md session 72.
These checks verify consistency; no biological or clinical validation is inferred.

## Live research state and restart path

The broader GPU research goal remains active. Remote root:
`/home/prachh/v/mva-track2-optical-20261019-v33` on `PrakashDGX_H2`.
All public data, processes, environment and caches remain under `v`. No raw subject
data or clinical narrative was transferred. Local GPU discovery fails with an NVML
library/driver mismatch; do not change the shared host's drivers.

Mitotic download/preparation completed: 97 verified files, 838,224 cells,
20,404 guide labels and 1,068 features. BUB1B counts 11/15/11/25 leave one guide
meeting the unchanged 20-cell minimum. Two guides are required; retrieval remains
missing, not zero. HeLa lacks functional p53 and is not a non-cancer allele model.
The complete interphase preparation must independently verify workbook coverage.

A two-step smoke run passed and is excluded. The eight full mitotic workers finished
successfully at 11:45:58 UTC; their supervisor receipt records eight zero exits.
This is later than the frozen v34 launch snapshot. Full metrics have not yet received
the planned aggregate, plate-sensitivity and independent validation. Do not call
completed fitting a gain. Original worker PIDs 126288-126295 are terminal and may
be reused by the system; never signal them without checking process identity.

The interphase downloader remains live. At 11:54:20 UTC it had verified 925/3,029
files (98,748,257,467/321,585,666,869 bytes), with no reported errors. Read
`outputs/download-interphase-status.json`, inspect the matching process and check
free disk before taking action. Earlier SSH session timeouts do not imply job failure.
Do not duplicate the download or overwrite output directories. No interphase model
wave has launched. The downloader Python PID was 4156734 at that check; verify
process identity before using it. Disk had 489 GiB free, above the 128 GiB floor.

Remote inspection:

```bash
ssh PrakashDGX_H2 'cd /home/prachh/v/mva-track2-optical-20261019-v33 && cat outputs/download-interphase-status.json && cat outputs/wave-mitotic/finished.json'
```

Use `scripts/track2_optical_fetch_v33.py`, `track2_optical_prepare_v33.py`,
`track2_optical_model_v33.py` and `track2_optical_run_v33.py`. The copied remote
`pyproject.toml` and `uv.lock` are retained as versioned public environment files.
Run through `/home/prachh/v/bin/uv`, with caches under the campaign root. Keep all
long tasks under nohup with logs. The supervisor requires eight idle GPUs and never
stops existing jobs. Read the fixed plan, separate amendment and
`notes/track2-optical-progress-v33.md` before continuing.

Next: finish the interphase download, verify receipts, prepare that arm and launch
its registered four real/four shuffled workers. Implement/validate held-out-plate
sensitivity, cross-arm count controls, independent CPU summaries and the paired
held-out-gene baseline comparison. Preserve every failure and missing query state.
Use a new evidence version for validated findings; v34 is a progress snapshot.
Carbon was reviewed and deferred as irrelevant to functional rescue. The unchanged
Anthropic toolkit has already run ProteinMPNN in v29; its failed controls remain.

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
