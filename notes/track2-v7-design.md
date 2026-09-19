# Track 2 v7: visual refinement

2026-09-19. Feat-009, baseline `b83c3d2`. The owner requested a more aesthetic
presentation. This is a visual revision of the five-slide v6 story. Use the
unchanged v6 report and 297-word narration, v5 validation and v4 evidence ledger.
All historical sources and packages remain preserved.

## Plan before implementation

V6's condensed bold headings dominate every slide, and the same title/diagram/note
placement gives unlike evidence the same visual weight. Replace that uniformity
with calmer typography, stronger grouping and deliberate variations in composition.

- Paper `#f6f7fb`: a cool neutral canvas.
- Ink `#241d32`: main text.
- Plum `#634285`: the proposed drug and published estimate.
- Mist `#eae3f2`: contextual grouping, not efficacy.
- Teal `#17666c`: functional endpoints.
- Night `#30203e`: the closing decision slide, with white text.

Use locally installed Liberation Serif regular for display titles, with Nimbus
Sans for scientific labels, citations and body text. Headings are 54-72 px; all
slide labels and citations remain at least 24 px. The scientific chart remains
numerically identical, with its logarithmic axis, point/interval and null reference.
No remote font, image service, new scientific source or model provider is needed.

```text
Cover      [large serif question        | two separate objectives]
Rationale  [two-line title]
           [mouse evidence] ... gap ... [conditional experiment]
Trial      [title / regimen]
           [            published estimate and interval         ]
Experiment [two-line title]
           [matched treatment matrix   | complete fate follow-up]
Decision   [large serif title]
           [four required conditions   | further preclinical work]
```

The right-hand cover graphic makes the two biological objectives legible; it is
not a decorative cell image. Rounded grouping surfaces denote experimental context.
Open circles in the treatment matrix denote planned groups, never success rates.
The final connectors require all criteria; they do not imply completed validation.

Pre-build critique: a serif font alone would be cosmetic. Recompose the figure
groups, give the conditional step its own clear visual space, and reduce the
cover's visual competition. Retain a quiet white evidence slide so the published
confidence interval remains the focus. No gradients, shadows, stock illustrations,
animation or repeated decorative cards.

## Presentation and preservation

Use `notes/track2-slides-v7.html` with `notes/track2-pitch-v6.md`; narration and
scientific order are unchanged. The v6 pitch's historical links still identify
its original deck. For this visual edition, open the v7 HTML or exported PDF.
Runtime remains unmeasured; neither is a recording or hosted pitch.

## Final visual review

All five final PDF pages were rasterized and inspected. The larger regular serif
titles, curved objective connectors, softly grouped comparisons and quieter
annotations make the evidence hierarchy easier to follow. No new illustration
of a biological result was added. The first render flagged overlapping title
line boxes; increasing line height resolved them. The PDF showed the browser's
serif fallback, so the final CSS explicitly names the rendered Liberation Serif.
The final PDF embeds its fonts and can be presented without font installation.

Final artifacts: `results/feat009/v7-slide-review-verified-20260919/` contains the
five-page PDF, five screen PNGs, five PDF rasterizations, a contact sheet and the
renderer provenance. All five 1280-by-720 slides have zero detected text overlap
or boundary violations, minimum 24 px text and a passing 640 px viewport check.
The PDF is 960 by 540 points per page, with no JavaScript. The weakest checked
text/background contrast is 5.11:1 (muted text on mist); the other checked pairs
range from 5.32:1 to 15.13:1. This is a bounded layout/contrast review, not a claim
of comprehensive accessibility certification or owner aesthetic approval.

Every slide's displayed word sequence and citation links match v6, including the
scientific caveats and AI disclosure. The deck remains 301 words; the inherited
narration remains 297 words. The v6 plot-coordinate validator checks the unchanged
ARST1431 HR/interval, log axis, null line, labels and primary DOI. The report,
narration, validation and scientific ledger were not edited.

Final deck SHA-256:
`25607c6f2ffda140c7c3482490e002f926149556efc7e65d99e64332117fc026`.

```bash
uv run python scripts/track2_release_v7.py check-deck
uv run node scripts/render_track2_slides_v7.mjs v7-slide-review-verified-20260919
uv run pdftoppm -png -scale-to 1280 results/feat009/v7-slide-review-verified-20260919/track2-slides-v7.pdf results/feat009/v7-slide-review-verified-20260919/pdf-slide
uv run pdfinfo results/feat009/v7-slide-review-verified-20260919/track2-slides-v7.pdf
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
# 429 tests pass, including 8 new synthetic snapshot-preservation tests.
```

The v7 release adapter checks the unchanged v6 release, which recursively verifies
v1-v5. Its snapshot copies the v7 deck/use note plus the unchanged v6 report/pitch,
v5 validation and v4 evidence. Tests cover wording drift, hostile markup, plotted
coordinates, immutable destinations, forged hashes, readiness claims, history/input
drift and symlinks. No historical release implementation was changed. Final build
results and publication checks are recorded in `progress.md` after this note is
frozen. This review was performed by the main agent; no independent reviewer or
additional model provider was used. Scientific and submission gates are unchanged.
