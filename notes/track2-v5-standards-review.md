# Track 2 v5: release and rendering standards review

2026-09-19 · feat-009 · baseline `13c8b46`

Scope: the new v5 release checker, its synthetic tests and the main editor's new
renderer. The other review covers scientific and editorial fidelity. This note
does not certify clinical validity, account settings, video runtime or upload
readiness.

## Implementation and review findings

The v5 package is a separate, compact snapshot with eight files: the current
report, pitch, self-contained HTML/SVG deck, validation plan, unchanged v4 evidence
ledger and three review notes. Historical reports are not mixed into the current
upload choice. The manifest binds 55 inputs: these sources, the new code/tests/renderer,
the visual-basis source note and all transitive v4 inputs. No older bound file
needs to change for this refresh.

`scripts/track2_release_v5.py` uses the existing v4 scientific-ledger validator.
It retains the fixed 11 candidate decisions, unresolved phase, unknown exposure
margins and unverified Fireworks training/retention settings. Its historical
check verifies v4, which recursively verifies v2/v3 and Track 1 preservation.
That is local byte preservation, not independent verification of uploaded bytes.
All releases remain research drafts with `upload_ready: false`, no video URL and
no upload operation.

The new vector policy is intentionally narrow. Each of five ordered slides must
contain a labelled static SVG. Tags and attributes are allowlisted. Script,
embedded documents, images, external fonts, SVG references, animation, filters,
foreign objects, event attributes and resource-loading CSS are rejected. The
deck must retain exactly one restrictive content-security policy. Citation links
can be internal anchors or credential-free HTTPS URLs; the renderer does not
follow them. Print and narrow-screen layout rules are allowed. This policy is
a constrained authoring check, not a general-purpose HTML sanitizer.

One material renderer hardening issue was raised during review: blocking HTTP
does not stop an edited deck from trying to load a local file. The main editor
fixed it by running the static checker before browser startup, comparing the
checker result with the exact source-byte hash, and rendering those bytes from
a read-only snapshot in the isolated temporary profile. The source and renderer
are checked again for drift after capture. Input/parent symlinks and nonregular
deck/renderer files are rejected. The static checker reads its payload once and
hashes the exact bytes it parsed.

The renderer uses a minimal environment, no project `.env`, an isolated browser
profile, blocked network protocols, a nonworking proxy and disabled page script
execution. It starts and stops only its owned Chrome process group. It writes
new PNG/PDF previews exclusively; it never overwrites an existing review folder.
The browser profile contains only the public deck and is retained for audit.
The PDF is a preview/export, not a video or a scientific result. Preview files
and their rendering manifest remain outside the immutable submission package.

The release checker rejects lexical traversal, output paths outside a direct
`results/feat009` child, old release destinations, input/output symlinks,
existing destinations, unknown files, duplicate JSON keys, nonfinite numbers,
unsupported fields and type-coerced readiness claims. Copies and sources must
match; input or historical drift during copying prevents a success manifest.
Failed partial outputs are not automatically deleted or silently reused.
Hash checks detect drift; they are not signatures or protection against a
hostile process with the same filesystem permissions.

Some release/path logic is repeated in the new module. This is deliberate:
extracting it from the hash-bound earlier scripts would invalidate the preserved
snapshots. Existing validation functions are reused where their fixed behavior
fits the new release; no generalized packaging framework was introduced.

No remaining material standards issue was found in the reviewed implementation.
Visual and PDF-page inspection still belongs to the separate design review.

## Executed checks

```bash
uv run python scripts/test_track2_release_v5.py
# Ran 40 tests; OK. Synthetic temporary fixtures only.

uv run python scripts/test_track2_release_v4.py
# Ran 72 tests; OK. Existing bound validator remains unchanged.

uv run python scripts/track2_release_v5.py check-deck
# static_deck_verified: true; five slides; five conceptual vector figures.

uv run python scripts/track2_release_v4.py verify results/feat009/jvv7_track2_research_v4
# integrity_verified: true; historical_v2_preserved/historical_v3_preserved: true.
```

Test logs are `logs/track2-v5-release-tests.log` and
`logs/track2-v5-prior-release-tests.log`. The v5 tests exercise adversarial
markup/CSS, inaccessible or missing vectors, ordering/balance/CSP violations,
link injection, path and symlink attacks, source/copy/history drift, scientific
promotion, manifest tampering and Python boolean/integer/float coercion. They
also verify the fixed pre-render deck check and exact source-byte hash.

The preserved v4 report SHA-256 remains
`79d962cb2723c3fa73c3591f6c3749eddd08d859edcecb7a9631ae424d31dc8a`;
its deck SHA-256 remains
`30110964d8e09f83d49307b9f22e74d54ce9da4a18fcf6eb159c30dc02d576d8`.
Final v5 package verification, fresh `./init.sh`, disclosure/history audits and
commit/push status are recorded by the main editor in the session handoff and
progress log. This note does not claim those later steps have already passed.
