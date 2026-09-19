# Track 2 v6: release and rendering standards review

2026-09-19 · feat-009 · baseline `17e9c66`

Scope: the new v6 release checker, synthetic tests and isolated local renderer.
Scientific fidelity is reviewed separately. This note does not certify clinical
validity, provider settings, video duration, an upload or the final slide design.

## Release and historical preservation

The new v6 release contains eight files and binds 65 inputs. It copies the current
report, pitch and HTML/SVG deck, three review/design notes, the unchanged v5
validation plan and the unchanged v4 evidence ledger. It does not create a new
validation plan with identical content. The public visual-basis note, new release
code/tests/renderer and all transitive v5 inputs are hash-bound.

The v6 verifier checks the actual v5 release, which recursively verifies v2-v4,
their sources and the earlier Track 1 preservation checks. V6 additionally checks
the seven v1 archived files against their historical manifest without applying
today's evidence decisions or source hashes to that earlier release. No historical
source or package is edited.
These checks establish local byte preservation, not independent identification of
the files previously uploaded by the owner.

The v4 evidence validator is reused directly. Phase remains unconfirmed, clinical
exposure margins remain null, everolimus is the sole conditional priority and HCQ
remains reserve. Provider training/retention fields cannot silently become verified.
Every new manifest retains `upload_ready: false`, no video URL and no upload action.

The snapshot destination must be a new direct child of `results/feat009` and cannot
be any v1-v5 historical destination. Existing directories, traversal and symlinked
paths are rejected. Source, copy and historical drift during a build prevent a
success manifest. Verification rejects changed inputs, mismatched copies, altered
history, shortened input lists, unexpected files, duplicate JSON keys, nonfinite
values and type-coerced readiness claims. Failed partial outputs are retained for
inspection rather than overwritten or silently reused.

## Static rendering and the published plot

V6 imports the frozen v5 HTML/SVG/CSS parser and subclasses it without changing
module globals. Its tag/attribute allowlists, restrictive CSP, balanced five-slide
structure, accessible vector labels and resource-loading restrictions are retained.
No historical parser needs editing to support this release.

One figure now represents published measurements: ARST1431 HR 0.86 with a 95%
confidence interval of 0.58-1.26. The other four figures are explanatory or proposed
schematics. The release scope and presentation summary make that distinction.
The v6 parser requires the identified plot on slide 3, a logarithmic 0.5-2 axis,
the three correctly positioned ticks, and point, interval and null-line positions
consistent with those values. Position tolerance is 0.1 SVG coordinate unit. It
also checks the published numeric labels and 297-evaluable population text in
slide content, the exact primary DOI link on slide 3, and the matching primary
source entry in the unchanged evidence ledger. Direct SVG transforms within the
plot are rejected so they cannot displace the checked coordinates.

These checks detect transcription, axis and source-map errors in this fixed figure.
They do not prove the source's scientific interpretation or all possible CSS
rendering behavior. The independent scientific review and rendered visual review
remain necessary; an accessible label or mathematically correct coordinate is not
a substitute for a legible graphic.

The renderer is the reviewed v5 implementation with v6 input, checker, temporary
profile and export names. It validates the fixed deck before browser startup,
compares the exact checked-byte hash, and renders a read-only copy inside an
isolated temporary profile. It uses a minimal environment, no project `.env`,
blocked network protocols, a nonworking proxy and disabled page scripts. Only
its owned Chrome process group is stopped. Profiles contain the public deck and
are retained for audit; unrelated profiles are untouched.

Five 1280-by-720 PNGs and `track2-slides-v6.pdf` are written exclusively to a new
review directory. Layout checks retain ordered slides, no text outside slide
bounds or overlapping text boxes, minimum computed font size 24 px, and a 640 px
view without horizontal overflow. Source and renderer hashes are checked after
capture. Preview exports remain outside the immutable package and are not a
recorded or hosted pitch.

## Executed checks and remaining review

```bash
uv run python scripts/test_track2_release_v6.py
# Ran 50 tests; OK. Synthetic temporary fixtures only.

uv run python scripts/test_track2_release_v5.py
# Ran 40 tests; OK. Earlier parser/release behavior preserved.

uv run node --check scripts/render_track2_slides_v6.mjs
# Exit 0.

uv run python scripts/track2_release_v5.py verify results/feat009/jvv7_track2_research_v5
# integrity_verified: true; eight files; historical v2/v3/v4 preserved.

uv run python -c 'import sys; sys.path.insert(0,"scripts"); import track2_release_v6 as r; print(r.history_checks())'
# Returns verified manifest hashes for v1, v2, v3, v4 and v5.

./init.sh
# no-data-in-git: ok
# self-check ok
# 84.99 GB in the local data directory
# COMPLETE: all files present at expected size
# local toolchain checks passed
# annotation resources ready
# === OK ===
```

The added synthetic cases reject a linear-axis point on the logarithmic plot,
incorrect interval endpoints or null placement, mismatched tick labels/positions,
nonfinite coordinates, displaced point/interval rows, direct or grouped SVG
transforms, missing plot identity, labels replaced by comments/descriptions,
unrelated DOI links and nonprimary or unrelated ledger mappings. Historical
checks now cover the archived v1 bytes and v5 as well as v2-v4. The inherited package/markup adversarial
tests continue to pass.

At the earlier checkpoint the final pitch and visual-basis source note were
missing. The resumed main agent supplied them and completed the final checks;
this addendum is an author verification, not a new independent standards review.

The real `check-deck` and renderer pass on the complete deck. Final render directory:
`results/feat009/v6-slide-review-final-20260919/`, source SHA-256
`2de0e16570ac2541e4a5faab4171240331dc26056f9781e0a9dea20ae2dce02d`.
All five PDF pages were rasterized and visually inspected. A label/connector
collision on slide 5 was fixed; automated text-box checks alone did not detect it.
Final geometry has zero text overlaps/boundary failures, minimum 24 px text and a
passing 640 px viewport check. The PDF is five pages, 16:9, without JavaScript.

The final Track 2 suite passes 421 tests, including the 50 new v6 tests. Core data,
Track 1 conformance and Track 2 evidence checks pass. Report sections 1-7, full
acknowledgement and source URL set match v5. The completed pitch has 297 narration
words; no timing or recorded-video check is claimed. The immutable package and
publication checks are recorded in the session progress entry after these notes
are frozen, so a package never needs to rewrite its own bound review inputs.
