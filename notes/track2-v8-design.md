# Track 2 v8: a more specific scientific visual story

2026-09-19. Feat-009. Baseline `333abd1`. The owner explicitly requested removal
of the cover line “Research only. Trans phase unconfirmed. No experiments performed.”
and a more aesthetic, relevant deck. That line is removed from the new cover.
The report and narration still state the actual evidence limits; no new scientific
certainty or completed experiment is implied by this presentation edit.

## Design before implementation

V7 improved typography but still relied on abstract objectives and text containers.
V8 gives each slide a subject-specific diagram: chromosome control, conditional
pathway testing, the published trial interval, cell-fate accounting and the
criteria for further preclinical work. These are explanatory/proposed schematics
except for the unchanged published ARST1431 estimate.

Retain the calm palette: paper `#f6f7fb`, ink `#241d32`, plum `#634285`, mist
`#eae3f2`, teal `#17666c`, and night `#30203e`. Use Liberation Serif regular for
56-74 px display titles and Nimbus Sans for labels/body. Keep all projected slide
text at least 24 px. Rounded shapes depict a cell, target or experimental grouping;
they should not become a repeated set of decorative cards.

```text
1  [research question                 | chromosome-control schematic]
2  [limited mouse observation] ... gap ... [conditional pathway test]
3  [tumour-trial question / published HR and confidence interval]
4  [model comparisons | enrolled cell -> division and other fates]
5  [function / safety / exposure / replication]
   [             all required for the next experiment           ]
```

The cover illustration must not resemble observed subject data, an assay result
or a claimed drug effect. Spindle lines and chromosomes explain the gene-level
context; they do not represent the selected variants' measured function. The
pathway diagram must put phenotype qualification before drug testing. The fate
diagram must distinguish first division from daughter survival and preserve
death, arrest, slippage and tracking loss. Four advancement conditions are not a
sequence or four successes, so use a joining bracket rather than numbered steps
or checkmarks. Prioritize meaningful relationships over ornament.

## Evidence and use

Use the unchanged `notes/track2-report-v6.md`, `track2-pitch-v6.md` (297 narration
words), `track2-validation-v5.md` and `track2-evidence-v4.json`. The five spoken
sections still follow the same question/rationale/trial/experiment/decision order.
The v6 pitch retains historical deck links; open `track2-slides-v8.html` or the v8
PDF for this presentation. No new narration timing or recorded video is claimed.

The existing report and selected primary sections of
[Sieben et al.](https://www.jci.org/articles/view/126863) support BUBR1's chromosome
attachment/checkpoint roles and the different-allele muscle phosphoprotein finding.
This is a bounded source recheck, not a new full-paper review. The figures do not
claim everolimus repairs chromosome segregation or demonstrates tissue rescue.
The ARST1431 redraw retains its existing primary citation, population and exact
HR/95% CI. The unchanged validation plan supplies proposed models and fate endpoints.

## Final author review and reproduction

All five PDF pages were inspected at 1280 px after local browser rendering and
PDF rasterization. The cover now explains the gene-level context; slide 2 shows
the uncertain mouse-to-model transfer and conditional pathway test; slide 4 records
all enrolled-cell outcomes separately from daughter survival. The final bracket
joins four advancement requirements without implying achieved outcomes. The plot
retains the published point/interval on its original logarithmic axis.

The deck has 313 visible words (39/70/60/68/76), four conceptual figures and one
published-data plot. Minimum slide text is 24 px; the conservative text-palette
contrast check is at least 5.11:1. Rendering reports zero outside-slide text and
zero text overlaps; the 640 px view has no horizontal overflow. PDF export has
five 960 × 540 pt pages, embedded fonts and no JavaScript. Links and SVG accessible
labels remain available. This is an author review, not an independent scientific
review, audience readability study, narration timing or completed experiment.

```bash
uv run python scripts/track2_release_v8.py check-deck
uv run node scripts/render_track2_slides_v8.mjs v8-slide-review-final-20260919
uv run pdftoppm -png -scale-to 1280 results/feat009/v8-slide-review-final-20260919/track2-slides-v8.pdf results/feat009/v8-slide-review-final-20260919/pdf-page
uv run pdfinfo results/feat009/v8-slide-review-final-20260919/track2-slides-v8.pdf
uv run pdffonts results/feat009/v8-slide-review-final-20260919/track2-slides-v8.pdf
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
uv run python scripts/track2_release_v8.py build results/feat009/jvv7_track2_research_v8
uv run python scripts/track2_release_v8.py verify results/feat009/jvv7_track2_research_v8
```

Final PDF, page previews and overview are under
`results/feat009/v8-slide-review-final-20260919/`. The renderer records source,
code and export hashes in `render.json`. Deck SHA-256:
`93804595099b9422e4eede96d73b6fe80cebe7b877b25dfcd301c6fd242f655e`.

The v8 adapter permits the requested wording revision while requiring the
scientific qualifications and source links, validates the static SVG and published
plot geometry, and recursively verifies the untouched v1-v7 packages. Regression
coverage includes rejection of restored cover wording, removed evidence limits,
active markup, inaccurate plot geometry, historical-output reuse, source/copy
changes, symlinks and changes to readiness or scientific state. Test fixtures use
this public deck and synthetic package contents; no subject inputs are read.

The five-page deck is ready for the owner's presentation review. The unchanged
v6 narration still requires rehearsal and recording; hosting, provider-account
settings, final owner/live submission checks and receipt remain outstanding.
No new model provider, source data processing, phase/efficacy/exposure evidence,
recording or upload was introduced. Preserve every earlier snapshot and bound input.
