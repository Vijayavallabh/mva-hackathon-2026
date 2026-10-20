# Session handoff: v41 literature-integrated presentation and harness

20 October 2026, session 81. Only **feat-009** remains active for delivery and
unresolved biological qualification. The v41 revision preserves the frozen v40
qualification sequence, synthetic-arm labels, 367-word own-voice narration and
recording metrics while adding the current public literature refresh. Use
`notes/track2-current.json`, `notes/track2-report-v41.md`,
`notes/track2-slides-v41.html`, `notes/track2-pitch-v40.md` and
`notes/track2-transcript-v40.txt`. The combined entry point is
`scripts/check_track2_harness.py`; start with
`notes/track2-reviewer-guide-v41.md` and `notes/track2-owner-readiness-v41.md`.
The literature chain is `notes/track2-literature-v41.md`,
`notes/track2-literature-audit-v41.json` and
`scripts/check_track2_literature_v41.py`.
The v19 `notes/track2-transcriptome-v19.md` and all later completed research are
preserved. The drug ledger/base contract remain v21; the demo and community kit
remain v37. All bound releases through v39 and the v38 review addendum are frozen.

## What changed after the owner's rehearsal

Read `notes/track2-rehearsal-adjudication-v39.md`,
`notes/track2-candidate-comparison-v39.md` and
`notes/track2-qualification-amendment-v39.md`. First qualify endogenous BUB1B
function and independently controlled restoration in proposed engineered hTERT-RPE1.
The comparator is immortalized, has weak retained expression specificity, and is
not an available patient line or a muscle/renal surrogate. Availability, clone
feasibility and functional qualification remain unconfirmed. No biological work
is promised before the submission deadline.

Everolimus is a conditional worked example on HOLD for unmeasured prerequisites.
The mTOR mouse signal is heterozygous BubR1+/X753 skeletal muscle, with sarcopenia
relevance, not demonstrated compound-pair rescue. North's genetic SIRT2 survival
benefit was male biased and distinct from NMN abundance or niacin findings. Mouse
K243 corresponds to human K250; favorable oocyte results coexist with harmful
somatic checkpoint/tumor findings. No generic K243R rescue control, allele-agnostic
rescue or new drug priority follows. SIRT2 is not a BUBR1-specific restoration.
Use product-specific Afinitor/Zortress labeling. Unknown evidence remains HOLD;
valid precise negatives close only the tested claim/context. Injury overrides benefit.

The owner can arrange a reviewer and is a bioengineering undergraduate. Use
`notes/track2-external-review-packet-v42.md`. The supplied rehearsal and AI-assisted
adjudication are not the independent review being arranged. No reviewer contact,
feedback or endorsement is established. The v38 competitive-review caveats remain,
including unverified competitor performance and the limits of broad novelty claims.

## Current materials

V40 contains nine slides, eight vector figures, 367 narration words, a ten-page
report, 334-word abstract, all eleven methods answers, transcript, video description
and an own-voice teleprompter. The frozen v37 demo still has 17 synthetic cases and
the actual unmeasured HOLD state. Its rules demonstrate software behavior, not
biological or clinical validity. The v40 small-kit guide points to that existing kit.

Frozen v40 exports remain `results/feat009/v40-slides-final-20261020` and
`results/feat009/v40-documents-final-20261020`; the final teleprompter browser receipt
remains under `results/feat009/v40-prompter-final-20261020`. Current v41 exports are
`results/feat009/v41-slides-final-20261020-3` and
`results/feat009/v41-documents-final-20261020-8`; no measured recording is claimed. The header continues to respect wrapped mobile controls. A shared narration parser
checks the transcript, prompter, guide and metrics JSON: 367 words in 180 allocated
seconds, or 122.3 planned words/minute. These are not measured video times. Earlier draft exports and
interim audit receipts remain in ignored results. Local conversation exports are
ignored and are not publication artifacts. Actual final checks are in progress.md.

## Completed research

Read `notes/track2-optical-v36.md` and its reproduction/audit/results records.
Both public exports completed: 838,224 mitotic and 31,046,046 interphase cells.
Sixteen corrected 3,000-step real/shuffled fits, sixteen plate workers and sixteen
complete-guide median workers finished on all eight H100s. Twelve baseline methods
per arm remain, with their original, registered and exploratory timing.

- Both practical neural-gain gates fail. Full means are strongest: MRR 0.047518
  mitotic and 0.234113 interphase. Interphase neural MRR is 0.143636-0.148017.
- Equal-cap interphase means score 0.093093, below the neural models. This supports
  an exploratory representation benefit under the cap, not a full-data gain.
- Full interphase BUB1B ranks 1/3/3/2 among 994 genes are favorable. The fourth guide
  varies strongly with aggregation, model and plate; cross-plate ranks reach 520.
  Treat this as an assay-development lead, not qualified non-cancer rescue.
- BUB1B mitotic counts remain 11/15/11/25. Only one guide qualifies; two are required.
  Missing is not zero, a normal phenotype or disproof of biology.
- Post-hoc plate proportions do not reproduce the favorable pooled ranks, but do
  not rule out batch effects. The exclusive-single-plate control has zero eligible
  genes and remains unavailable. Pooled-trained encoders are not unseen-batch tests.
- Original centroid-contaminated fits stay excluded. The legitimate empty shard
  exposed a preserved v35 failure; v36 repairs it without changing nonempty processing.
- Independent CPU reductions, all 40 query-guide medians per arm, workbook counts,
  archive hashes and local rank/MRR/paired-interval replay pass. Replay reuses the
  registered bootstrap implementation; no independent statistical algorithm is claimed.
- Six new falsification records bring the total to 58 across seven registers.
  No drug, phase, exposure, wet-lab or clinical claim changes.

## Remote state: finished, do not restart

Host `PrakashDGX_H2`; root `/home/prachh/v/mva-track2-optical-20261019-v33`.
All work, cache and temporary files stayed under the owner's `v` folder, using
`/home/prachh/v/bin/uv` and the isolated pinned environment. No protected subject
input was transferred. All owned campaign stages have successful terminal receipts:

- `outputs/interphase-v36-pipeline/finished.json`, 13:09:25 UTC.
- `outputs/secondary-v35-pipeline/finished.json`, 13:26:31 UTC.
- `outputs/finalize-v36-pipeline/finished.json`, 13:28:06 UTC.

The old `outputs/interphase-v35-pipeline/failed.json` is historical, not an active
failure. Preserve original scripts, registrations, partial-output archive, fitted
checkpoints and prepared arrays. Do not restart the downloader or supervisors.

Local review archive: `results/feat009/optical-v36/optical-v36-review.tar.gz`,
3,535 files / 81,058,361 bytes, SHA-256
`a1e366c5c931a626c446c17de4d77fd15384e5c5730cd45e2f11c04f7d40ab8d`.
This contains public review records, code and provenance; source parquet, checkpoints
and prepared numeric matrices remain remote. Local replay covers twelve paired
comparisons, 480 evaluated cross-plate metrics and both post-hoc plate-only metrics.
The remote roots remain in the November 23 deletion scope. At the owner's request,
four uv installer caches from completed MVA jobs were removed after dependency
and open-file checks. Approximately 2.5 GiB was removed by uv; 34 GiB of cache
directory allocation largely shared hard-linked storage with retained environments.
Results, source data, models, checkpoints and unrelated projects were preserved.
See `notes/track2-dgx-cleanup-v37.md`; environment imports passed after cleanup.

## Checks and reproduction

```bash
./init.sh
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/track2_public_review_v41.py
uv run --no-project python scripts/check_track2_literature_v41.py
uv run --no-project python scripts/check_track2_optical_v36.py
uv run python scripts/audit_track2_harness.py
uv run python scripts/track2_release_v41.py verify results/feat009/jvv7_track2_research_v41-verified27
uv run python scripts/track2_bundle_v41.py verify
uv run --no-project python scripts/track2_community_kit_v37.py verify
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
```

Public checks need no subject files, GPU, keys, network or historical local snapshots.
Strict release verification also checks retained local exports/archives. New snapshots
must use unused directories; never edit old bound inputs to make a new check pass.
Python audit hooks check dependency isolation, not operating-system security.

## Blockers and next actions

- Arrange actual outside review through the owner; preserve feedback and the reviewed
  version, then adjudicate objections. Uncoached pitch/demo comprehension is unmeasured.
- Record the 367-word pitch in the owner's own voice, measure the full exported video
  including acknowledgement and transitions, and host on YouTube/Vimeo. Script cue
  allocations total 180 seconds but are not a measured recording. No video or URL exists.
- Resolve existing provider/distribution questions. OpenAI no-training is an owner
  attestation; Fireworks and earlier alignment-service handling remain unverified.
  Historical AF3/non-AVI Atlas terms versus challenge CC BY scope remain unresolved.
  Preserve the notices and existing unsent clarification; no organizer contact is authorized.
- Before delivery, review exact files, team identity, live rules/quota, public GitHub
  and video access. Three entries are allowed; only the latest is judged. Quota is
  unknown. Archive uploaded bytes and the receipt after actual submission.
- Scientific advancement needs independent endogenous perturbation/restoration,
  qualified non-cancer function, joint treatment, exposure and injury measurements.
  No rescue-priority drug, confirmed phase, clinical margin or wet-lab result exists.
  Everolimus remains an optional probe; HCQ remains reserve. Balnis units stay quarantined.
- Preserve submitted Track 1 v4. Owner-reported 100/F-max 1 is separate from the missing
  receipt/byte audit; do not upload again to fix that administrative gap.
- The October 20 v42 anonymous refresh found the seven official files unchanged at
  `60e1c30e337ce6fe01813040dbe49979eb8c50aa`, but public discussion now has 31 threads,
  89 visible comments and 16 closed threads. Thread 32 permits a clearly labeled
  published-paper example in the pitch; the current non-genomic 367-word script remains
  compliant. Thread 31 documents a Synapse alternative; thread 29 reinforces IRB/consent
  routing. This is still not an authenticated account/quota check.
  Submit by **October 24, 23:59 UTC**. Delete all scoped local/remote data and confirm
  to **cnb@sagebase.org by November 23**, under `notes/deletion-plan-v2.md`. Feat-010
  has not started. Cache cleanup did not satisfy this obligation. No email/upload occurred.

One bounded public-source literature search was added in v41, and one anonymous
official/community refresh was added in v42; no GPU campaign, remote job, wet-lab
result or additional hosted model provider was run. The v39/v40 scientific
adjudications remain authoritative. V41 changes readout design, not drug disposition;
v42 changes delivery options, not requirements. The next decisive evidence remains
biological, not more model agreement.
