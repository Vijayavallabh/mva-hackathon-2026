# Track 2 v6: story and visual rebuild

2026-09-19. Active feature: feat-009. The owner rejected both the v5 story and
its design. V5 and every earlier bound source remain unchanged.

## Design brief

The panel should understand one proposal in three minutes: test everolimus for
non-cancer tissue function only after a BUB1B model demonstrates the relevant
pathway abnormality. The talk must explain the rationale, the evidence against
overclaiming, and the experiment that determines whether to continue.

The previous deck resembled an assay worksheet. Its generic cell illustrations
and candidate list did not explain why this particular experiment deserved a test.
Reducing the word count did not solve that problem.

## Plan before implementation

Color tokens: aubergine `#342044` for the opening and conclusion; white `#ffffff`
for evidence; ink `#241b2d`; plum `#70418a` for the proposed intervention;
teal `#006b70` for normal-tissue function; pale lavender `#eee8f3` for grouping.
These colors encode subject and experiment, not success probabilities. No gradients,
shadows, stock cell cartoons or decorative scientific images.

Typography: locally installed Nimbus Sans Narrow for the large, compact titles;
Nimbus Sans for body, figure labels and numerical evidence. Titles 58-76 px, body
28-34 px, citations and limits at least 24 px. The display face gives more room to
the figures without turning every title into three lines.

Layouts vary with the content. Reading order stays left aligned. The cover sets
out the two biological objectives; the second slide separates a published finding
from a proposed test; the third gives the published confidence interval most of
the canvas; the fourth shows the controlled comparison; the last connects the
advance criteria to a research decision.

```text
1  [research question                 | BUB1B + two objectives]
2  [mouse observation]  transfer gap  [pair-specific experiment]
3  [trial / population]
   [             hazard ratio and confidence interval        ]
4  [matched treatment matrix         | complete fate follow-up]
5  [criteria                         | next research decision]
```

Pre-build critique: a title plus three identical cards would repeat v5's problem.
The revised plan uses an evidence comparison and an actual trial plot, with no
ranked-drug catalogue slide. The cover's two branches are objectives, not an image
of a patient, a measurement or a claim of dual drug benefit. The concluding diagram
must not imply that pathway inhibition alone qualifies as functional rescue.

## Scientific and editorial boundaries

The humanizer and no-ai-slop passes remove formulaic opening disclaimers and
repetitive candidate lists from the narration, while retaining the essential
limits visibly and the detailed qualifications in the report and notes. They do
not remove the full disclosure, acknowledgements or contrary evidence.

The research-lookup workflow reuses the reviewed ledger and checks public primary
sources through built-in web access. No Parallel, OpenRouter or image-generation
provider is invoked. The PDF skill is used for local export review; slides are
rasterized and visually inspected. Figures remain editable local SVG.

Only the ARST1431 plot represents measured published results. All other diagrams
show proposed comparisons or objectives. There are no new experiment results,
patient-level disclosures, estimates of efficacy, phase claims or clinical margins.

## Review record

The initial work left a first render and pre-final reviewer notes. On continuation,
the main agent completed the narration and inspected all five screen previews and
all five pages rasterized from the final PDF. The slide-5 "All required" label
crossed the brace in the first render; moving it clear of the connector fixed the
collision. Text-only geometry had not detected that defect.

Final render: `results/feat009/v6-slide-review-final-20260919/`. The deck has 301
visible words across five slides (49/64/61/60/67), four conceptual SVG figures and
one redrawn published result. The 297-word narration follows the same sequence.
V5's 288-word deck remains preserved; this revision prioritizes a coherent
experiment and legible evidence rather than another word-count reduction.

Automated checks report five 1280-by-720 slides, no text-box overlaps or boundary
violations, minimum computed text size 24 px, and no horizontal overflow at 640 px.
The exported PDF has five 960-by-540-point pages (16:9). The PDF omits navigation.
All pages were rasterized with `uv run pdftoppm -png -scale-to 1280` and inspected.
The standalone public trial plot also has Matplotlib SVG/PDF exports, reproduced
by the command in `sources/research_track2_v6_visual_basis.md`.

Final deck SHA-256:
`2de0e16570ac2541e4a5faab4171240331dc26056f9781e0a9dea20ae2dce02d`.
These checks establish the reviewed rendering, not owner aesthetic approval or a
recording. The final content/visual pass was performed by the resumed main agent;
no new independent reviewer or external model provider was used.
