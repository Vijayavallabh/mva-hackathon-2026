# Current-state harness review

2026-09-21, session 54. Owner explicitly requested harness updates alongside the
new presentation. Main-agent author review; not an independent assessment.

The structural harness skill validator reported 100/100 before changes: instructions,
state, verification, scope and lifecycle each 5/5. Its “instructions” bottleneck
label was a tie, not evidence that any subsystem was worse. The score checks
artifact presence and wording; it missed concrete stale-state hazards:

- AGENTS described several historical reports as current and retained the withdrawn
  session 32 everolimus priority in an active-facts list.
- The 617-line handoff ended with older release commands; current transcript/release
  pointers could diverge across README, feature evidence and session notes.
- Startup checked data/toolchain integrity but not presentation versions, transcript
  alignment, model-control claims or unsupported delivery status.

The root now keeps contractual rules, current science, established Track 1 facts,
explicit verification, scope and lifecycle instructions. Historical session details
remain in progress.md and immutable Git revision bb82cd6; no raw data policy was
relaxed. Feat-009 evidence now summarizes current artifacts and routes to history.
The handoff distinguishes completed computation from biological and delivery gaps.

`notes/track2-current.json` is the single mutable artifact/status record. The new
`check_track2_harness.py` validates active-feature ownership, coherent versioned roles,
current routes, scientific/delivery state and actual presentation/model checks.
`init.sh` invokes it without GPU, SSH, keys or protected subject content. Newly
established biology or verified delivery status requires explicit evidence review
and a corresponding harness update, not editing a flag to bypass a check.

The v14 release binds its report, slides, transcript, source/results, runtime locks
and output terms. Historical v1–v13 are recursively verified. Mutable lifecycle
files are intentionally outside immutable scientific-release bindings, so future
handoff updates do not invalidate old packages. The renderer exports the required
AlphaFold3 terms and notice with the PDF.

Verification includes mutation tests for stale/mixed versions, false readiness,
lost acknowledgement/terms, altered trial numbers and model-claim boundaries.
Actual commands, test counts, fresh init output, visual review, publication audits
and Git verification are recorded in progress.md and track2-v14-design.md. A structural
score or passing software test is not experimental validation or clinical readiness.
