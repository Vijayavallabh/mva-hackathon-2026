# Track 2 v18 visual redesign

25 September 2026. Aesthetic revision of the eight-slide pitch, using the
scientific-slides and locally pinned frontend-design skills. The scientific ledger
remains v15, the official-source review remains v17; the report/methods are revised to v18, and the pitch is rewritten to 334 spoken words for Track 2. The official website was rechecked after the owner requested competition framing;
no new biomedical inference or model provider was used. Figures are editable, locally rendered SVG, not generated images.

## Design plan, before implementation

Audience: a scientific judging panel watching a three-minute video without live Q&A.
The job is to make the qualified hypothesis, balanced evidence, decisive experiment
and falsification rules understandable at a glance.

Tokens: ice `#F7FAFC`, ink `#142C3C`, deep teal `#123A40`, evergreen `#176359`,
mint `#D8EEE5`, iris `#48419D`. White and pale iris are supporting surfaces.
Ubuntu Medium carries the headlines; Ubuntu Regular carry body and diagram
labels. Numbers use tabular alignment. The PDF embeds the installed fonts; HTML
falls back to sans-serif if Ubuntu is unavailable. No remote font dependency.

Composition alternatives considered:

```text
Repeated panels (rejected)             Figure-led sequence (chosen)
[ heading                 ]           [ question      | spindle    ]
[ box ] [ box ] [ box     ]           [ genotype ------< branches  ]
[ citation                ]           [ study context | evidence   ]
                                      [ staged experiment -------- ]
                                      [ completed    | all cells   ]
                                      [ evidence     > decision    ]
```

The first option repeats v17's card rhythm. The second gives each scientific idea
its own shape. Dark opening/decision/closing slides punctuate bright analytical
slides. The memorable image is a large, explicitly conceptual mitotic spindle;
other surfaces stay quiet. Curves in the cover echo the branching logic later.
Left alignment, wide margins, short text lines and direct labels take priority.

Critique before building: a dark field plus a bright accent could become a generic
technology pitch. The revision therefore uses a specific mitosis schematic, botanical
mint rather than neon, humanist type rather than futuristic labels, and white
analytical pages. No decorative gradients, glass cards, random particles, or model
structure imagery. No disease outcome is represented as measured data.

## Planned slide treatments

1. Large question and mitotic spindle; candidate and uncertainty remain visible.
2. An actual fork separates the two unqualified mechanism hypotheses.
3. Three evidence rows preserve positive findings, opposing findings and trial uncertainty.
4. A staged horizontal route separates qualification, probing and confirmation.
5. Common-scale bars expose the synthetic denominator trap, with explicit arm labels.
6. Three large decision rows distinguish unknown evidence, failed safety and all-pass.
7. A connected genotype/fate/rules diagram explains the reusable contribution.
8. A quiet closing with the complete acknowledgement, not a decorative thank-you page.

## Review record

Rendering, geometry, PDF review, exact output hashes and any corrections are recorded
below after implementation and in `track2-v18-render-audit.json`.


## Final review

- Eight 1280×720 slides and seven SVG figures; 549 visible words.
  Minimum text 24px; no reported text overlap or clipping. The 640px viewport passes.
  Checked text contrast is at least 5.26:1. Ubuntu fonts
  are embedded in the PDF; the few fallback symbols are embedded too.
- All eight final screenshot/PDF pages reviewed. The initial cover line-height was
  increased after geometry detected overlapping text ranges. Visual inspection found
  an overlong mechanism label and misaligned fork; both were corrected.
- After the owner's competition-framing request, the cover names the repurposing
  proposal, candidate choice appears earlier, and the conclusion identifies impact
  and the next experiment. The new 334-word script matches eight slides.
- The report is 2,119 words versus 2,910 (27.18% shorter), with a 166-word abstract.
  Six A4 pages, all inspected; evidence columns rebalanced. Its full provider
  disclosure, acknowledgement and 27 unique citation targets are preserved.
- All synthetic bars use the same 400px 0–100% track; values are unchanged.
  The depiction is labelled synthetic, with explicit control/treated denominators.
- The final source/renderer/output hashes are in the render/document audits. The
  public reviewer also passes in an isolated copy without data, results, logs, .env
  or .git, with network and protected-path access blocked: 0.315 seconds on one run.
  This measures consistency checking only. No biological or eligibility claim follows.
