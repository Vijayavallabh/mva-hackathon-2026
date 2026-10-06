# Track 2 v32 harness review

The current artifact record, AGENTS, README, feature evidence and handoff route
presentation and harness v32 to the completed v31 Perturb-seq evidence. Earlier
v19/v21/v23/v25/v27/v29 records and all presentation releases remain frozen.
The drug ledger and decision contract remain v21. There are 52 claim records across
six registers, with eleven unchanged drug dispositions.

The combined standard-library reviewer needs public notes/scripts only. It verifies
the pinned v31 audit, all source hashes, complete query states, calculation counts,
missing controls, guide identity, no promotion and displayed numbers. The new release
includes all v30 inputs plus v31 evidence and v32 presentation inputs. Strict release
verification separately checks the historical local snapshots and exported artifacts.
The recording ZIP is a collection of materials, not a recording or receipt.

Adversarial tests cover altered correlation/rank displays, omitted control or guide
limitations, loss of previous control failures, safety-gate relabeling, stale routes,
false completion/clinical claims, incomplete methods and changed exports. The public
isolation audit forbids network, subprocesses, protected paths, credentials, writes
and arbitrary external reads through Python audit guards. This tests dependency
isolation, not operating-system sandbox security or biological correctness.

Run `uv run --no-project python scripts/check_track2_harness.py` for the combined
review; `uv run python scripts/audit_track2_harness.py` repeats it in a temporary
public-only copy. Versioned presentation checks use `scripts/track2_public_review_v32.py`.
Final execution outcomes and fresh `./init.sh` output are recorded in progress.md,
session 71. No independent reviewer or new hosted biological-model provider was used.
