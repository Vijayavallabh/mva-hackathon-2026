# Track 2: official website review and v12 alignment

2026-09-19, session 49, baseline `6d33184`; feat-009. The owner requested a review
of the challenge website and any necessary changes. This is an author requirements
review, not an organizer endorsement, account audit or submission.

## Sources actually reviewed

Read the running site's public Gradio configuration, including About-page HTML,
Track 2 instructions, FAQ and rules, alongside the public source at revision
`1c761cc23d90aebe6a011fd5b0b99517df42408c`. The anonymous Space API still resolves
to that revision; this is a live recheck, not a newly changed code release. The
text-only browser could see only the Gradio shell, so the public `/config` response
supplied the content of the live components. No login, quota callback, upload or
submit callback was invoked.

Sources: [challenge website](https://sagebio-rare-disease-real-kid-mva-hackathon-2026.hf.space/),
[About/rubric](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/1c761cc23d90aebe6a011fd5b0b99517df42408c/tabs/about.py),
[rules](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/1c761cc23d90aebe6a011fd5b0b99517df42408c/tabs/rules.py),
[submission instructions](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/1c761cc23d90aebe6a011fd5b0b99517df42408c/tabs/submit_track2.py),
[methods template](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/resolve/1c761cc23d90aebe6a011fd5b0b99517df42408c/static/templates/methods_description_form.xlsx).
The template's Track 2 sheet, cells A7–A17, was read as XML without executing macros,
formulas or foreign Python. The workbook was not modified.

Reviewed the public community index and relevant threads: organizer
[LLM/data clarification #2](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/2),
[approved-drug/combination clarification #5](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/5),
[updates #10](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/10)
and [dataset citation clarification #13](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/13).
Other participants' speculation is not an official requirement or biological evidence.
Rechecked the [June 2026 everolimus label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2),
indications and section 12.1, solely to support existing approval/target wording.

## Findings and changes

| Website requirement or criterion | Finding in v11/current report | V12 disposition |
|---|---|---|
| Existing market-approved medication with a variant-to-mechanism rationale | The report explains approval and allele limits, but the pitch names only the gene and drug. | Add stop-gain/missense context, uncertain allele function/phase, mTORC1 target and approved-for-other-indications status to slide 1 and narration. This is a downstream hypothesis, not gene repair or proven MVA efficacy. |
| Scientific rigor, 35% | Falsification, model transfer, safety, exposure and all-cell fate accounting are already prominent. | Retain them and the exact ARST1431 estimate. No candidate promotion or new biological claim. |
| Potential impact, 25% | Little explicit pitch explanation of what validation would teach about MVA. | State the conditional value: distinguish useful functional modulation from harm and identify what merits further study. No clinical benefit estimate or diagnostic claim. |
| Innovation, 25% | The creative contribution is buried among controls. | Make genotype/phase-aware comparisons and first-event/daughter-fate accounting explicit; no claim of first-ever novelty. |
| Scalability, 15% | Open code is linked, but transfer conditions are mostly unstated in the pitch. | Explain reuse of code, evidence schema and decision rules, with fresh model, exposure and safety qualification for each genotype/context. No automatic efficacy transfer. |
| Recommended methods answers; AI disclosure required | Much is scattered in the long report; automation/curation and data-source scope are not template-indexed. | Add an eleven-field methods appendix and an abstract below 500 words, including unmeasured time/cost rather than inventing estimates. |
| Required acknowledgement in public communications | Exact text is in the report; standalone slides have only thanks and a link. | Add a full acknowledgement end slide and ready-to-copy video description containing the complete acknowledgement and provider disclosure. |
| Three-minute recorded YouTube/Vimeo pitch, report and GitHub URL | PDF/script are not a recorded video; no hosted URL or receipt exists. | Budget the end slide inside three minutes. Keep recording/hosting and owner/live checks open. |

The About page explicitly treats entries as hypotheses for investigation. Keeping
everolimus as an optional mechanistic probe is compatible with that scope; there is
no requirement to claim demonstrated efficacy. The proposal still needs a plausible
mechanistic bridge, and the panel may reasonably find the indirect evidence weak.
This review cannot assign a score or guarantee eligibility/selection.

## Ambiguities and limits

- The workbook still mentions one final Track 2 entry. The live instructions,
  configuration, specific FAQ and organizer announcement #10 consistently specify
  three entries with only the latest reviewed. Use one designated team submitter;
  this does not verify remaining quota or imply a need to resubmit.
- The About timeline lists October 24–November 24 for judging, while rules,
  instructions and FAQ describe roughly two to three months. Do not promise an
  announcement date. Close remains October 24 at 23:59 UTC.
- Organizer clarification #13 says the later-publication dataset-reference rule is
  not an additional Track 2 report requirement now. Do not manufacture a dataset DOI
  or block this report on an unavailable formatted reference.
- The methods template answers are voluntary except the AI disclosure field. The
  written report, GitHub URL and recorded pitch remain required. No exact required
  slide count or compulsory wet-lab results were found in the inspected materials.
- Organizer data-processing guidance does not relax this repository's stricter
  raw-data, contact, publication or deletion instructions. Provider settings remain
  explicitly unresolved; credit-based usage is not a data-policy audit. No new
  provider or gated payload was used for this website review.

## Reproduction and provenance

```bash
uv run python scripts/track2_challenge_review.py results/feat009/new-challenge-review
```

Actual output: `results/feat009/challenge-review-live-v1/`. Nine sources returned
successfully, plus the public Space metadata request. `manifest.json` binds revision,
URLs, timestamps, response bytes and executed-script hash. Selected community API
records use `/api/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/{2,5,10,13}`;
their separate `community-manifest.json` records URLs and hashes. These are anonymous
GETs. Raw Gradio config stays local; no leaderboard contents were used as evidence.

Key SHA-256 values:

- About: `1867b07f24d987fbb728c756c2d2bc4ab5f302d7c7804f53fe7b6a8b4c83ae43`
- Rules: `dccb3740f6301b8629c704c375739e23391d19dee62513587ee461d6c8637f8f`
- Track 2 instructions: `f48d576ab052df34527222b7693f956e15e5376ef68eddedcf0c4f04736bf65c`
- Methods workbook: `61aab080a2868a3b724e76692b83c24812112e305cd3a8b03f8f91a6b2414441`
- Live config: `8fc846d7969c8280c6ad55a3379c167d5f7d2d17baf31aa1c118875756b690f2`

Web-tool parsing failed for some raw-code pages and discussion #13; direct public
source/API retrieval succeeded. These are access-path differences, not missing
rules or negative evidence. Current science remains the v10 ledger and validation;
all historical bound inputs are preserved. Presentation checks follow.


## Presentation design and author verification

Continue the reviewed scientific-slides/frontend-design direction: pale paper, plum
and teal, serif question headings, large explanatory diagrams and source footers.
Keep slides 2–5 and the published ARST1431 plot intact; strengthen the first page's
mechanism/approval explanation and replace the closing page with the three judged
contributions plus the advancement rule. The acknowledgement receives a seventh,
text-only page so its complete wording stays legible. It is not another evidence
figure or additional spoken scientific claim.

Rendered with the existing isolated, network-blocked browser workflow:

```bash
uv run python scripts/track2_release_v12.py check-deck
uv run python scripts/track2_release_v12.py check
uv run node scripts/render_track2_slides_v12.mjs v12-slide-review-first-20260919
uv run pdftoppm -png -scale-to 1280 results/feat009/v12-slide-review-first-20260919/track2-slides-v12.pdf results/feat009/v12-slide-review-first-20260919/pdf-page
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
```

All seven PDF pages were individually inspected after rendering. No text overlap
or clipping was detected or observed. The minimum rendered text is 24 px, the
640 px view passes, and the unchanged text palette retains checked contrast of at
least 5.43:1. There are six SVG figures: five conceptual diagrams and one unchanged
published-data redraw; page 7 is deliberately text only. Visible word counts are
57/78/67/60/72/95/105, including footers and the acknowledgement. The seven-page PDF
is 960 × 540 points per page, tagged and without JavaScript. Narration is 338 words
(50/47/53/39/53/74/22), with planned transitions and end slide inside three minutes;
actual runtime remains unmeasured.

The new release checks preserve report sections 1–6 byte-for-byte relative to v10,
check all eleven template answers and the 228-word abstract, and require the full
acknowledgement in the report, visible slide and video description. Ten new tests
exercise omission/tampering, script alignment, scientific limits, plot preservation,
immutable snapshots and input/copy integrity. All 489 Track 2 tests pass. These
checks are author verification, not independent scientific review, regulatory
approval, a score prediction or a recording. No new experiment, selected-pair
response, phase, clinical exposure margin or provider-policy assurance is claimed.
