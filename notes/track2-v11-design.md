# Track 2 v11: present the falsification findings

2026-09-19, session 48; baseline `5d0a344`. Feat-009. The owner requested updated
slides and narration relevant to the completed v10 research. The report, validation
plan, ledger and cycle-1 review remain v10 and unchanged. This presentation does not
add evidence, promote a candidate or modify earlier snapshots.

## Design before implementation

Use six slides for a three-minute pitch: question, conflicting evidence, separate
hypotheses, tumour boundary, proposed experiment, and advancement criteria. The
extra slide gives the v10 hypothesis revision room without crowding the evidence.
Narration will target roughly 340–365 words; actual runtime must be rehearsed.

Retain the established paper `#f6f7fb`, ink `#241d32`, plum `#634285`, mist
`#eae3f2`, teal `#17666c` and night `#30203e` palette. Liberation Serif carries
the question/headlines; Nimbus Sans carries scientific labels, at least 24 px.
Keep the chromosome schematic, use study-to-outcome rows for conflicting findings,
two separate hypothesis branches, the exact published ARST1431 plot, cell-fate
tracking, and four joined advancement requirements. Arrows show the proposed
comparison or a source-specific observation, never an assumed clinical response.

```text
1  [question / non-cancer function          | chromosome-control schematic]
2  [compound + model] --------------------- [reported outcome + limitation]
3             [qualify model and prespecify]
              /                           \
       [A: excess mTOR]           [B: flux + regenerative deficit]
4  [tumour boundary / original published HR and confidence interval]
5  [graded exposure + recovery | complete cell-fate and function accounting]
6  [function / safety / exposure / replication] -> [further preclinical work]
```

Brief review: preserve the user's chosen visual identity and removed cover line.
Do not introduce more decorative cards or a large search-count statistic. The
scientific change is the story. Move the trial from slide 3 to slide 4 without
changing its SVG, estimates, labels, source or interpretation. Keep time allocations
as rehearsal guidance, not measured video runtime. No new image/model provider is
needed for these exact, editable vector diagrams.

## Source and claim mapping

Slide 1 uses established BUB1B/BUBR1 context. Slide 2 pairs Joseph's selected muscle-
mass findings with Ge's regeneration risk and Goutas's BUBR1-loss concern. These are
different compounds/models and do not establish selected-pair benefit or harm.
Slide 3 explains the v10 protocol's A/B distinction, motivated by Balnis's hypercapnia
results; the supplementary dose/schedule gap remains unresolved. Slide 4 retains
Gupta/ARST1431 exactly. Slides 5–6 translate the v10 validation plan: graded exposure,
regeneration/recovery, first-event and daughter-fate records, delayed normal-tissue
injury and justified exposure. Naddaf and van Erp support the linked safety/exposure
qualifications; neither establishes pediatric risk or free tissue concentration.

The already-adjudicated v10 report, ledger and cycle review are the evidence basis.
A bounded public-page recheck reached the Balnis primary article; the Joseph PMC
page presented a browser challenge and Ge's PubMed page returned no parsed text.
Existing archived primary sections/abstracts remain the basis for those statements.
No new full-paper or independent review is claimed. The research-lookup guidance
informed source selection; the available web tool and existing public archives were
used rather than adding Parallel/OpenRouter providers. Scientific-slides and the
installed frontend-design guidance inform the visual and timing review.

## Final author review and use

Inspected all six rasterized PDF pages from the first render. The final pass added
a report/source/disclosure link on slide 6; slides 1–5 are pixel-identical to the
inspected first version, and the final page 6 was inspected again. There is no text
overlap or clipping. Minimum font size is 24 px, checked text-palette contrast is
at least 5.43:1, and the 640 px view has no horizontal overflow. The PDF has six
960 × 540 pt pages, embedded fonts and no JavaScript. An overview is available
beside the PDF. The figures are readable at reduced size; dense methodological
detail remains in the full validation plan.

The six slides contain 410 visible words (44/78/67/60/72/89), including citations
and disclosure. Narration contains 358 words (42/61/66/46/65/78), approximately
119 words/minute over three minutes; timestamps allocate 22/30/32/23/34/39 seconds.
Timing remains unmeasured. The final script explicitly pauses advancement for
unexplained BUBR1 loss and retains HCQ reserve, phase/exposure uncertainty, absence
of experiments and provider limits. The slide-6 source link and narration source
map connect the brief safety/exposure wording to the detailed v10 evidence.

The exact ARST1431 SVG is unchanged from v10 and moves to slide 4. Other diagrams
are source-specific summaries or proposed comparisons; none represents new data.
Current science remains the 52-source/11-decision v10 ledger. This is author content
and visual review, not independent scientific review, a measured read-through,
clinical validation or a recorded presentation.

```bash
uv run python scripts/track2_release_v11.py check
uv run python scripts/track2_release_v11.py check-deck
uv run node scripts/render_track2_slides_v11.mjs v11-slide-review-final-20260919
uv run pdftoppm -png -scale-to 1280 results/feat009/v11-slide-review-final-20260919/track2-slides-v11.pdf results/feat009/v11-slide-review-final-20260919/pdf-page
uv run pdfinfo results/feat009/v11-slide-review-final-20260919/track2-slides-v11.pdf
uv run pdffonts results/feat009/v11-slide-review-final-20260919/track2-slides-v11.pdf
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
uv run python scripts/track2_release_v11.py build results/feat009/jvv7_track2_research_v11
uv run python scripts/track2_release_v11.py verify results/feat009/jvv7_track2_research_v11
```

All 479 Track 2 tests pass, including eight new presentation/preservation tests.
The static renderer retains the isolated offline browser and input-hash checks.
The v11 snapshot binds the presentation to unchanged v10 scientific files and
recursively preserves v1–v10. New checks reject lost hypothesis/model qualifications,
missing cell-fate/safety limits, changed narration boundaries or slide order,
changed plot geometry, active markup, restored cover wording, source/copy drift,
historical-output reuse, symlinks and invented readiness. These are content and
integrity checks, not proof of biological validity.

Exports: `results/feat009/v11-slide-review-final-20260919/`. Deck SHA-256:
`fbdfbd447c949482ca015b5b2a90e025e2a6dbd8ec21c5f780ccc01513999cf2`.
Use `notes/track2-pitch-v11.md` for reading; its headings and recording notes are
not spoken. Full acknowledgement and AI disclosure remain in the v10 report.
Rehearsal, recording/hosting, provider verification, owner/live checks and receipt
remain outstanding. No new model provider, subject analysis, drug decision,
experiment, phase/exposure conclusion or upload was introduced.
