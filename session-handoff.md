# Session handoff — Track 2 v17 presentation / v15 science

Updated 2026-09-24, session 56. Only feat-009 is active. Use
`notes/track2-current.json` for current artifacts/status. V17 updates the presentation,
report, exports and reviewer workflow against the live site and every public discussion.
V15 science retains all eleven v10 drug dispositions. Submitted Track 1 v4 and all
Track 2 v1–v16 inputs/releases remain immutable.

## Current materials

- `notes/track2-report-v17.md`: candidate-first hypothesis, balanced evidence, staged
  experiment, impact/innovation/reuse, eleven methods answers and full acknowledgement.
- `notes/track2-slides-v17.html`, `notes/track2-pitch-v17.md` and
  `notes/track2-transcript-v17.txt`: eight slides, seven SVG figures, 342 narration words.
  Planned timing is three minutes; actual runtime is unmeasured.
- `notes/track2-video-description-v17.md` matches report AI disclosure and acknowledgement.
- Seven-page report PDF, participant-named Markdown and filled original methods workbook:
  `results/feat009/v17-documents-final-20260924/`. B7–B17 filled, B17 249 words.
- Eight-slide PDF/PNGs: `results/feat009/v17-slide-review-release-20260924/`.
- Immutable research snapshot: `results/feat009/jvv7_track2_research_v17`.
  Recording-materials ZIP: `results/feat009/jvv7_track2_video_materials_v17.zip`.
- Public guidance: `notes/track2-reviewer-guide-v17.md`; concrete remaining delivery
  questions and unsent clarification text: `notes/track2-owner-readiness-v17.md`.

## Official and community findings

`notes/track2-official-requirements-review-20260924.md` independently checks ten public
resources at live revision aeeef5ad49f51204a7439352e59e9d310aee5e9e, including exact
live/source instructions, rubric, template and source hashes. Required: approved drug
hypothesis, participant-named PDF/Markdown report, GitHub URL, three-minute YouTube/Vimeo
video. Rubric: rigor 35%, impact 25%, innovation 25%, scalability 15%. No compulsory
wet-lab data or fixed slide count; no live Q&A. Three entries/latest-only; the workbook's
one-entry instruction is stale. Quota remains unqueried.

`notes/track2-community-review-20260924.md` covers all 24 public threads (12 closed),
68 latest visible comments, 86 events and three administrative screenshot attachments.
Thread 9 is absent from the public list; hidden/deleted/edit history was not sought.
No subject content was adopted or redistributed. Organizer guidance versus participant
suggestions is distinguished. Sep23 discussions were included: PDF methods accepted;
parental phase and aligned-read/library resources remain unanswered. Provider conditions
depend on actual terms/settings, not merely consumer/API labels. No contact or submission.

## Scientific position and falsification

No rescue-priority drug. Everolimus is an optional model-qualified mechanistic probe,
HCQ reserve; tumour killing is separate from non-cancer function. Phase, endogenous
allele effects, clinical exposure and meaningful assay margins remain unresolved.
No new model inference or wet-lab experiment occurred in this revision.

The v15 63-source ledger, validation plan and 19-claim register retain contrary evidence,
falsifiers, stop/reopening rules and next actions. Primary protein ordering passes 12/12,
but all-six-control separation fails 8/12 and 11/24 retained-control scores are negative.
That is post-hoc sensitivity, not clinical accuracy. D882A's secondary label is in main
text; the supplement remains independently unreviewed. All older failed controls remain.
Balnis supplemental ex vivo units conflict by 1,000-fold; neither value is a dose input.
Unknown evidence means hold; failed safety stops; all-pass permits preclinical review only.

The new narrative removes AF3/Atlas numerical outputs and figures from judge-facing
materials, retaining historical disclosure and notices. This is not a licence cure:
challenge CC BY scope for linked historical model outputs remains unresolved. Do not
change blanket licensing or claim eligibility on that basis.

## Verification and restart

```bash
./init.sh
uv run --no-project python scripts/track2_public_review_v17.py
uv run python scripts/check_track2_harness.py
uv run python scripts/track2_release_v17.py check
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
uv run python scripts/track2_release_v17.py verify results/feat009/jvv7_track2_research_v17
uv run python scripts/track2_bundle_v17.py verify
```

The public command passed in a clean copy without data/results/logs/.env/.git, with
network and protected-path access forbidden by an audit hook: 0.21 seconds, 37,376 KiB
maximum RSS on one local run. This is consistency, not biology or model throughput.
Historical release verification is separate and needs previous local snapshot folders.
Eight slide images are identical to visually reviewed previews; no text clipping or
overlap, 24px minimum, 640px viewport pass. All seven report pages visually reviewed.
Workbook round-trip checks preserve prompts and Track 1 template values/styles; its
appearance was not visually rendered. See the versioned audits and design note.

The separate agent reviewed requirements and an initial report, not final exports or
laboratory validity. Its relative-link finding was fixed. Exact final test counts,
init output, bundle/release hashes and publication/Git checks are in session 56 progress.

## Blockers

- Biological advancement: endogenous function, subject phase, model/branch qualification,
  tissue response, clinical exposure and prospectively justified assay margins missing.
- Balnis source units unresolved; secondary-control supplement and model dependence/
  cross-gene transfer/pretraining overlap remain limits. Prior retrieval failures remain
  recorded, not negative evidence. More correlated structures do not close these gaps.
- Delivery: Fireworks and earlier alignment-service handling remain unverified; OpenAI
  no-training is an owner attestation. Actual provider/credit terms need appropriate review.
- Distribution: linked-history CC BY scope versus historical AF3/non-AVI Atlas terms
  unresolved. A concrete clarification draft exists but has not been sent.
- Narration runtime, recording, hosted URL, owner/live portal checks and Track 2 receipt
  remain open. No remaining quota inferred. Do not call submission callbacks as tests.
- Track 1 owner-reported 100/F-max 1 retained; receipt/byte identity archive unverified.
  Never request another upload to resolve that administrative gap.

## Next actions and preservation

Rehearse and record the eight-slide pitch with the full acknowledgement visible inside
the three-minute runtime. Resolve provider/distribution questions and final portal checks
before submission. For research, qualify the endogenous non-cancer model and chosen
mechanistic branch; resolve source concentration ambiguity. Before any promotion, search
supporting and contrary primary evidence and update the relevant falsifier/reopening rule
in a new version. BindCraft2 remains deferred without a functional target/validation route.

Raw subject files/clinical narrative must stay on the original machine and out of hosted
context. No protected subject file was opened by this public research/export workflow;
local startup integrity programs may check local data. No family contact/re-identification.
Remote model folders under ~/v remain in the deletion inventory; no owned inference job
is pending from this cycle. Preserve all previews, failed requests and historical notices.
Keep the live retired-object purge guard for publication. Close: 2026-10-24 23:59 UTC;
deletion/confirmation: 2026-11-24. Commit intended changes, push origin, verify equality.
