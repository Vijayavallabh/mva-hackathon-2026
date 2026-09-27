# Track 2 harness integration review

27 September 2026, session 59. Harness version 19 combines presentation version 18,
drug-disposition ledger version 15 and research addendum version 19. The versions name
different artifacts; none implies a newer approved treatment or a submitted entry.

## Observed gap and correction

The previous main harness checked v18 and ignored `research_addendum`. Four mutation
checks were accepted: deleting the addendum, routing its report into `data/`, inflating
the GPU count to 80 and claiming fourteen primary query passes. The separate v19
checker existed, but the main command and v18-only reviewer guides did not provide a
complete current review. Baseline evidence is retained locally in
`results/feat009/harness-sync-baseline-gaps-20260927.json`.

`scripts/check_track2_harness.py` now requires the completed addendum and exact public
routes, checks the frozen v19 audit/hash inventory, invokes both preserved scientific
checks and derives summary counts from the completed outputs. It retains the HT29
partial positive and rejects changes to failed query/QC counts, compound identities,
GPU coverage or drug dispositions. Public file resolution rejects symlinks and paths
outside the checkout. The `results/` archive route is recorded but never opened by the
public checker.

`notes/track2-current.json` distinguishes the combined reviewer/readiness routes from
the frozen v18 artifact routes. The new reviewer and readiness notes cover both
presentation and research. AGENTS, README, feature state, handoff and `init.sh` use the
combined command; startup no longer repeats the full v19 check separately. The original
v18 guides, all 316 v18-bound inputs, the v19 campaign and its manifest stay byte-identical.

## Verification scope

The harness-creator structural audit reports **5/5 in each subsystem**: instructions,
state, verification, scope and lifecycle (100/100 overall). All scores tie, so there
is no meaningful lowest-scoring subsystem. Its tie-break label “instructions” does
not establish a cause. The concrete false passes identify verification/routing as the
actual gap. Structural scores alone missed that gap and do not measure research quality.

Regression checks cover the demonstrated false passes, stale review links, count/QC
drift, incomplete follow-up coverage, erased favourable evidence, missing bound inputs
and unsafe paths. An isolated public checkout runs the combined command with network,
process launching and protected-path access denied by an audit hook. It supplies no
project environment, raw data, results, `.env`, Git history, SSH or model weights.
The reproducible command is `uv run --no-project python scripts/audit_track2_harness.py`;
the outer helper uses Git only to stage public files, and the isolated child self-tests
six blocked operations before review. This does not claim operating-system isolation.
Exact output, final test counts, 346 preserved-input hashes, fresh `./init.sh` output
and publication checks are recorded in session 59 of `progress.md`.

This is a same-agent implementation and verification review, not independent scientific
review. No inference, expression reanalysis, new literature evidence, wet-lab work,
provider change, submission or external message occurred. All clinical, licensing,
provider and delivery uncertainties remain open.
