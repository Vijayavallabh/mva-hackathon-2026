# V23 combined harness integration

27 September 2026, session 63. Harness v23 adds the new public RNAi analysis to the
preserved v22 presentation, v21 drug/biological decision evidence and v19 campaign.
The entry point remains `uv run --no-project python scripts/check_track2_harness.py`.

The new checker verifies eight distinct GPU registrations, cell/space coverage,
1,536,619,950 pair comparisons, 5,843,968 conditional control evaluations, 2,364,754
orthogonal reference comparisons, reused RNAi experiments, missing seed coverage,
favorable HT29 evidence and the finite-reference counterweight. It binds code, plans,
results, report, figure, new claim register and qualification revisions to hashes.
No-result is not zero evidence. Results cannot promote phase, exposure, drug status,
biological validation or submission readiness.

Numerical unit checks cover tied ranks, nonfinite/constant input rejection, independent
gene/seed matching, diagonal exclusion and multiplicity. Evidence regressions reject
lost workers, missing-as-negative conversion, lost sensitivity findings, invented
independent experiments/BUB1B CRISPR data, changed counts, drug promotion and missing
falsifiers. The existing isolated-copy audit also exercises the new checker without
protected inputs or project dependencies. Actual final results are recorded in
session 63 of `progress.md`.

All 433 v22-bound inputs are checked for preservation; historical v22 and earlier
releases retain their own verifiers. New science is a separate addendum, not a
replacement of frozen presentation files. The v23 primary archive has its own
non-extracting verifier. A new archive would need a new destination and review.

The figure was visually inspected after correcting legend/footer overlap and a clipped
control range. The report does not convert pair counts to biological sample sizes,
wall time to GPU time, or a zero reference exceedance count to a probability of zero.
The work used CUDA matrix statistics, not new neural inference. GPU use was bursty.
No independent scientific reviewer or biological validation is claimed.
