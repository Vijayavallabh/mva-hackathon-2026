# Session handoff

**Last updated:** 2026-09-21 IST, session 54. **Active feature: feat-009 Track 2.**

## Current artifacts

Read `notes/track2-current.json` first. Current presentation/report revision is **v14**;
drug science is **v10**. Use:

- `notes/track2-report-v14.md`: both model campaigns, methods and expanded disclosure.
- `notes/track2-slides-v14.html`: nine slides; exact trial plot and full acknowledgement.
- `notes/track2-pitch-v14.md` and `notes/track2-transcript-v14.txt`: nine aligned paragraphs,
  336 narration words; timings are allocations, actual runtime unmeasured.
- `notes/track2-video-description-v14.md`: full acknowledgement, provider disclosure,
  AlphaFold3 terms, modification notice and paper citation.
- `notes/track2-v14-design.md`: source/visual review and export directory.
- `scripts/track2_release_v14.py` and `scripts/render_track2_slides_v14.mjs`: current
  release/render entry points; never overwrite a prior snapshot.

The recording-materials bundle is
`results/feat009/jvv7_track2_video_materials_v14.zip`: PDF/HTML slides, nine PNGs,
transcript, report, video description, terms and a checksum manifest. The verified
research snapshot is `results/feat009/jvv7_track2_research_v14` (38 files/234 bound
inputs; all v1–v13 preserved). These are materials for recording, not a hosted video.

## Scientific state to preserve

No drug earns rescue priority. Everolimus is an optional qualified mechanistic probe;
HCQ is reserve. V10's separately qualified A/B hypotheses and functional benefit,
injury, regeneration, recovery, exposure and replication gates remain unchanged.
Neither hypothesis is established for the selected pair. Trans phase and clinical
exposure margins are unresolved; no wet-lab experiment has been performed.

The newer-model follow-up is complete: ESMC 300M/600M/6B and ESM3-open 1.4B produce
84 scores and pass the small fixed control challenge; N1002K is negative in every
window. This strengthens computational motivation to test it. Earlier ESM disagreement
and failed controls remain relevant. AlphaFold3 120, ESM3 24 and ESMFold2 48 structures
retain confident impaired controls and WT sampling variability. Evo2 20B completes
100 comparisons, passes strict numerical gates and has BRCA1 AUROC 0.9201389.
BRCA1 transfer, pretraining overlap and correlated model evidence constrain conclusions.
No score, confident fold or model agreement establishes function or drug rescue.

See `notes/track2-latest-models.md`, fixed plan, complete matrices and provenance.
All 685 archive member hashes pass; 686 files including manifest. Local reanalysis
agrees with remote scores/gates, with maximum coordinate difference 1.43e-14. Retain
failed download/runtime attempts, first-GPU-filter omission, CCD cache correction,
inherited plan prose and the false environment-without-mutation flag correction.
AlphaFold3 Output Terms, mandatory notice, modifications and citation must accompany
all derived findings, including exported decks. No new GPU inference was needed for
this integration; no owned GPU process is pending.

Validation: 562 Track 2 tests pass; eight targeted harness tests pass again after
final bundle-path checks. Fresh no-argument init passes with its new step 7; the
standalone current-harness check also passes after the last edit. Live PUBLIC/purge
checks pass and the staged disclosure audit has zero findings. Actual output and
final Git commands are in progress.md.

## Next steps

1. Rehearse the nine-slide transcript to measure runtime, including transitions and
   the full acknowledgement page; record and host the three-minute video.
2. Integrate any later evidence through a new version, preserving falsification,
   failed controls and all earlier bound inputs. Update the current-artifact record,
   report, slides, transcript, release checks and handoff together.
3. Before any submission, resolve owner/provider disclosure, perform live authenticated
   identity/rules/quota checks, review the complete artifact bundle and archive the receipt.
   A successful local build is not submission readiness or permission to invent a URL.

## Blockers and unresolved evidence

- Endogenous allele function, phase, tumour context, tissue response and clinical
  exposure are unestablished. No laboratory qualification or efficacy/safety result.
- Fireworks and external alignment-service training/retention policies remain unverified.
  OpenAI no-training is an owner attestation; self-hosted Firecrawl previously used
  Fireworks-hosted GLM. See current report section 9 for all providers/output terms.
- Narration runtime, recording, hosting, owner/live checks and Track 2 receipt remain open.
- Track 1 first-attempt 100 / F-max 1 is owner-reported; receipt and uploaded-byte identity
  remain unverified. Do not ask for another upload; preserve submitted v4. This
  administrative blocker does not block authorized Track 2 research.
- Local NVML mismatch remains a historical operational issue; check actual hardware
  before new compute. Completed owner-hosted models are not blocked by it.

## Restart and verification

```bash
./init.sh
cat notes/track2-current.json
uv run python scripts/check_track2_harness.py
uv run python scripts/track2_release_v14.py check
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
uv run python scripts/track2_release_v14.py verify results/feat009/jvv7_track2_research_v14
```

The startup check uses public files only and requires no GPU, SSH, key or protected
subject content. It detects mixed artifact versions, stale handoff pointers and
unsupported scientific/delivery promotion. The structural harness skill score alone
was insufficient: it returned 100/100 even while old/current wording conflicted.
See `notes/track2-harness-review-v14.md`; actual validation and init output are in
`progress.md`. Do not conflate software checks with biological validation.

## Preservation and data boundary

All prior v1–v13 packages and their bound files are immutable; Track 1 v4 is preserved.
Older session details live in `progress.md` and the prior harness at Git revision
`bb82cd6` (`git show bb82cd6:AGENTS.md` and `git show bb82cd6:session-handoff.md`).
Data facts/commands remain in the referenced research notes. Do not revive historical
candidate priorities, failed access blockers or current-version labels from those records.

Raw subject reads/VCF subsets/clinical narrative never leave the original machine.
No family contact or re-identification. Remote public-reference/model work is under
`~/v/mva-track2-pilot-20260920/`, `~/v/mva-track2-expanded-20260920/` and
`~/v/mva-track2-expanded-latest-20260921/`; all are in the deletion inventory.
Recovery Git bundles may retain obsolete history; never republish them. Keep the
live purge guard for preflight. Close 2026-10-24 23:59 UTC; deletion/confirmation due
2026-11-24. Commit intended changes, push configured origin and verify a clean tree
and upstream equality at session end.
