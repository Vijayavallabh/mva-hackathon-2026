# Track 2 v5: editorial and visual review

2026-09-19, feat-009, baseline `13c8b46`. The owner requested skill discovery and
installation, humanizer/no-ai-slop editing, and a more visual, less text-heavy deck.
This revision covers the current Track 2 report, validation supplement, pitch and
slides. Uploaded Track 1 files and all historical Track 2 sources/packages stay intact.
The evidence ledger remains v4: this is a communication revision, not new science.

## Skills and installation

Used `find-skills` and the local `skill-installer` to inspect the skills.sh leaderboard,
search `slide design`, and check the curated OpenAI list. The CLI search returned
slide-specific options, including `nexu-io/open-design@slides` (2.6K displayed installs)
and `figma/mcp-server-guide@figma-use-slides` (1.4K). Neither was needed for a standalone
local HTML deck. These are observed directory counts, not quality/security guarantees.

Selected [Anthropic frontend-design](https://github.com/anthropics/skills/tree/34040c9c568585f6929bedeaad110ad08f079624/skills/frontend-design)
for typography, deliberate visual structure and screenshot critique. The skills.sh
leaderboard displayed 901.4K installs; the GitHub API returned 177,113 repository stars.
Reviewed the instruction file before use. Installed at a pinned revision with the
existing installer; no package scripts, hosted inference or extra model provider:

```bash
uv run python .codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo anthropics/skills --ref 34040c9c568585f6929bedeaad110ad08f079624 \
  --path skills/frontend-design --dest .codex/skills
```

The installed skill and Apache-2.0 licence are local ignored files; this command is
the reinstall record. The skill becomes discoverable on the next turn and its
instructions were read directly for this revision.

Also used existing `scientific-slides` and its visual-review workflow, `humanizer`,
`no-ai-slop` and its evaluation checklist, `research-lookup` for source reuse/checking,
and `pdf` for the printable local export. Optional image-generation backends were not
used. The diagrams are editable SVG written locally; no synthetic patient likeness,
photomicrograph, drug-response curve or invented experimental measurement appears.

## Design plan before implementation

Audience: a scientific competition panel watching a three-minute research proposal.
Job: make the normal-tissue safety requirement and the conditional experiment clear.

Palette: paper white `#ffffff`, ink `#173042`, cobalt `#2549a3`, deep teal `#00675b`,
amber-brown `#885500`, pale blue `#edf3fa`. Color identifies context and is always
paired with labels; it never encodes an unmeasured effect size.
Typography: locally installed DejaVu Sans with sans-serif fallback; 48-64 px headings,
26-32 px diagram labels, 24 px citations/limits. No external font requests.
Layout: 16:9, 1280 by 720, fixed presentation canvas with stepped scaling on
small screens. No automatic animation or remote dependencies.

Compared layouts:

```text
Rejected: [ title ]                 Chosen: [ short claim             ]
          [ card ][ card ][ card ]          [ large explanatory figure ]
          [ paragraphs / caveats ]         [ local caveat / citation  ]
```

Repeated cards were already the main weakness of v4. Replace them with a paired-cell
concept, a conditional pathway, a two-branch candidate map, a cell-fate tree and a
proposed validation route. Each figure carries a relationship, not decoration.
Use the report and spoken script for the qualifications that cannot fit legibly on
screen. Keep decisive caveats visible: research only, unconfirmed phase, indirect
mouse evidence, unknown exposure and unverified Fireworks data handling.

## Review record

The humanizer draft/audit/revision pass and no-ai-slop self-evaluation produced plainer
report and validation prose, direct spoken narration and shorter slide labels. The
independent [editorial review](track2-v5-editorial-review.md) records preservation of
quantities, citations, candidate decisions and the exact acknowledgement. It also
identified wording that could trade normal-cell injury against benefit; the final deck
instead stops for unacceptable injury and restricts advancement to preclinical work.

Measured slide text, including headers, citations and page numbers but excluding
navigation, SVG accessibility descriptions and HTML metadata:

| Version | Slide 1 | Slide 2 | Slide 3 | Slide 4 | Slide 5 | Total |
|---|---:|---:|---:|---:|---:|---:|
| v4 | 65 | 93 | 77 | 99 | 76 | 410 |
| v5 | 40 | 67 | 54 | 54 | 73 | 288 |

That is 122 fewer words, a 29.8% reduction. Counts use whitespace-separated text
within each slide section; SVG titles are excluded. The browser's visible-text counts
agree for v5. The 337-word narration plans about 112.3 words/minute; its runtime has
not been measured. This is a shorter deck, not a compressed evidence record.

Final visual artifact directory:
`results/feat009/v5-slide-review-scaled-20260919/`.
It contains five 1280 by 720 screenshots, a five-page 16:9 PDF, rendering metadata
and PDF raster previews. The final source SHA-256 is
`3333e5f6cd1da1d1a4f618b6ffdb6b38946264bafce8f6c8472c86c737f26203`.
All five PDF pages were converted to PNG and visually inspected; the footer was also
checked in enlarged crops. No clipped text, missing figures or harmful overlaps remain.
The source uses at least 24 px text within slides. The minimum conservative palette
contrast across tested text/background pairs is 5.62:1; colors also have text labels.
These checks do not establish universal accessibility, projector or video performance.

```bash
node scripts/render_track2_slides_v5.mjs v5-slide-review-scaled-20260919
pdftoppm -scale-to-x 1280 -scale-to-y 720 -png \
  results/feat009/v5-slide-review-scaled-20260919/track2-slides-v5.pdf \
  results/feat009/v5-slide-review-scaled-20260919/pdf-slide
pdfinfo results/feat009/v5-slide-review-scaled-20260919/track2-slides-v5.pdf
```

The renderer reports five figures, no out-of-slide text and no detected text-box
overlap. A 640 px viewport check gives a 640 px slide and document width. A continuous
CSS scaling attempt failed in the installed Chrome; fixed scaling breakpoints replace
it. Earlier diagnostic folders are retained and are not the final deliverables.
Other fixes during inspection: increase title line spacing, shorten an overflowing
heading, keep page numbers together and move browser navigation away from the footer.
The PDF omits navigation. No animation, narration, recording or video hosting occurred.

The renderer validates static markup before launching Chrome, hashes the checked
content and renders a read-only copy in an isolated profile. Its minimal environment,
disabled script execution, network blocking and restrictive CSP prevent the deck from
loading external assets. See the [standards review](track2-v5-standards-review.md).
Only public-safe sources and permitted derived content enter the deliverables.

## Handoff

Use the v5 report for the next owner review, with the matching deck and narration.
The immutable bundle contains current materials and the unchanged v4 evidence ledger;
the PDF is a separately hashed render export. Prior Track 1 and Track 2 files remain
unchanged. All scientific limits and provider/video/live-submission gates remain.
Skill installation is reproducible from the pinned command above and does not add an
AI inference provider to the disclosure.
