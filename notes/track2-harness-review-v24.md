# V24 integrated presentation and harness

The current harness and presentation are v24. Drug evidence/biological validation stay
v21, transcriptome research v19 and RNAi research v23. `notes/track2-current.json`
routes every current artifact; the public entry point is `scripts/check_track2_harness.py`.

New versioned review, render, export, release, bundle and regression files cover the
nine-slide deck, 342-word narration, exact transcript, matched disclosure, eleven methods
answers and 227-word abstract. The public checker calls both frozen research checkers
and pins the RNAi audit hash. Tests reject removal of reused-experiment limits, favorable
HT29 evidence, finite-reference sensitivity, missing BUB1B CRISPR evidence and required
controls. Original drug and readiness guards remain.

The release inherits v22 rather than assuming a nonexistent v23 presentation snapshot.
It preserves all 433 v22-bound inputs and binds the v23 audit's 22 public inputs plus
the audit itself. Earlier snapshots retain their original verifiers. The mutable
current pointers and combined harness stay outside historical release manifests;
the versioned public reviewer provides the fixed release check.

Offline Chrome exports nine slides and a nine-page report. Source/renderer/exporter
hashes, geometry, contrast and document template/answer integrity are checked. The
recording ZIP includes the new materials and frozen research supplements. It does not
record, upload or certify eligibility. Workbook appearance was not visually rendered.

The isolated-copy checks exercise Python audit guards for network, processes, protected
paths, credentials, external files and writes. They need no project environment, Git
history, subject inputs or GPU. This verifies runtime dependencies, not operating-system
sandbox security or biology. Final execution results are in progress.md session 64.
