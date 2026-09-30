# Track 2 v27 reviewer guide

Use `notes/track2-current.json`. Presentation v26 stays frozen; the current research
addendum is [v27](track2-falsification-v27.md), with four complete protein score matrices,
all transcriptome sensitivities and five new claim challenges. Read it alongside the
v26 presentation until a new presentation version integrates the findings.

```bash
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/check_track2_falsification_v27.py
```

The combined check covers v26 presentation, v21 decisions, frozen v19/v23/v25 research
and v27 additions. All 42 claim records are retained; they are not 42 studies. V27 has
9,472 masked distributions, 179,968 substitution scores and 918,999,010 expression
comparisons. These counts do not measure biological independence or efficacy.

The [reproduction note](track2-falsification-reproduction-v27.md) gives original archive
verification and reanalysis commands. The [earlier guide](track2-reviewer-guide-v26.md)
gives strict presentation/release checks and prior research routes. Old inputs must
remain unchanged. Public checking uses standard-library CPU code and needs no subject
files, network, credentials, GPU or retained archives. Numerical consistency does not
establish biology, eligibility, clinical safety or submission readiness.

The [current readiness note](track2-owner-readiness-v27.md) retains delivery and scientific
gaps. No rescue drug, phase confirmation, clinical margin, wet-lab experiment, recorded
video or Track 2 receipt is established by this research.
