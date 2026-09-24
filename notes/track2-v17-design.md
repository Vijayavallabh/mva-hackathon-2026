# Track 2 v17 presentation and document review

24 September 2026. Presentation v17 retains scientific ledger/validation v15:
63 sources, eleven unchanged dispositions, nineteen falsifiable claims. No new
inference, experiment, phase evidence, clinical margin or candidate promotion.

## What changed and why

The live rubric gives scientific rigor 35%, impact 25%, innovation 25% and scalability
15%. The report now opens with the approved-drug hypothesis and the next experiment,
then connects mechanism, positive and contrary evidence, qualification, useful function,
injury and exposure. A separate section explains the contribution and practical reuse.
It does not claim a comparative rescue ranking or predict a prize. The numerical model
inventory remains in technical history; it no longer dominates the three-minute pitch.

All 24 publicly listed discussions, 68 latest visible comments, 86 events and three
administrative screenshot attachments were reviewed. See the complete thread table in
`track2-community-review-20260924.md`. The official source/live-component comparison is
pinned to aeeef5ad49f51204a7439352e59e9d310aee5e9e. Template questions are preserved,
including the historical one-entry instruction with a comment explaining the live rule.
The PDF/Markdown report answers all eleven methods questions and includes the required
AI disclosure, full acknowledgement and a 249-word abstract.

## Visual and document checks

- Eight 1280×720 slides, seven purpose-built SVG figures, 578 visible words, minimum
  24px text. Geometry reports no text outside slides or overlapping text; 640px viewport
  has no horizontal scroll. All eight screen exports and PDF pages were reviewed;
  the synthetic-denominator and stopping-rule slides were also inspected at full size.
- A common 400px scale represents 0–100% in both synthetic bar panels. Values are
  20/80 versus 5/45 abnormal completed divisions and 60/100 versus 40/100 useful output.
  They are labelled synthetic, not data. No chart implies a measured drug response.
- Final slide exports are byte-identical to the visually reviewed first exports;
  subsequent changes only added decision-label IDs for stronger semantic tests.
  Exact hashes, geometry, contrast checks and browser version are in the render audit.
- The final report PDF is seven A4 pages with 11pt body type, repeated table headings,
  absolute public evidence links and a complete acknowledgement on page seven. All pages
  were inspected; table page two and final page seven were checked individually. The
  initial eight-page preview was revised to avoid an almost empty final page and retained.
- The original workbook is hash-pinned. All B7–B17 values round-trip correctly; official
  questions and Track 1 template values/cell styles are unchanged. No formulas, formula
  errors, macros or external workbook links. Workbook appearance was not visually rendered.
- Narration has 342 whitespace-separated words across eight matched sections:
  44/43/47/47/47/42/49/23. Three-minute allocations are planning cues; no runtime
  measurement, recording or hosted video is claimed.

See `track2-v17-render-audit.json` and `track2-v17-documents-audit.json` for source,
renderer, exporter and output hashes. Rendering was deterministic HTML/SVG with isolated
network-blocked Chrome, not image-model generation or a new provider.

## Independent review and concrete corrections

A separate research agent reviewed the official pages/template and then the initial
v17 report against those requirements. See
`track2-official-requirements-review-20260924.md` and
`track2-v17-requirements-check.md`. That review prompted replacement of ten relative
report links with absolute public links. Root verified the final document export and
matched workbook answers. The separate agent did not review the final PDF, workbook
appearance, secondary-control supplement or laboratory science. Its initial report
hash is historical, not falsely presented as the final source hash.

A mutation test found that deleting a main stopping-rule label could pass because the
same phrase appeared in a footer. The final checker now verifies the six specific
decision-row labels, so the footer cannot mask a missing stop rule. Thirteen new public
review regressions exercise coverage, false quota/readiness, missing disclosures,
abstract length, trial uncertainty, synthetic denominators and unsafe remote resources.

## Public reproducibility and limits

`uv run --no-project python scripts/track2_public_review_v17.py` passed in an isolated
copy of 367 nonignored public files with no data, results, logs, .env or .git directories.
An audit hook rejected network calls and attempts to read the prohibited directories;
the project environment was not used. One local run took 0.21 seconds and 37,376 KiB
maximum RSS. This is a consistency-check resource measurement, not inference speed,
experimental throughput, end-to-end cost or biological validation. The exact record is
`track2-public-review-v17.json`. Full historical integrity remains a separate operation
that requires retained local release folders.

The judge-facing materials omit AF3/Atlas numerical outputs and derived figures but
disclose historical use. Omission does not settle the linked repository's licensing
scope. No blanket relicence, provider attestation or upload readiness is asserted.
The concrete remaining question and recording/portal steps are in
`track2-owner-readiness-v17.md`; its clarification text has not been sent.
