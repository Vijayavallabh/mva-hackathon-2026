# Track 2 v29 reviewer guide

Read [the new research addendum](track2-orthogonal-v29.md) before interpreting the
preserved [v28 report](track2-report-v28.md), [slides](track2-slides-v28.html) and
[script](track2-pitch-v28.md). The [current state](track2-current.json) uses harness v29
and presentation v28. It does not claim the new findings are already incorporated
into the frozen slide/report exports.

```bash
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/check_track2_orthogonal_v29.py
uv run python scripts/audit_track2_harness.py
uv run python scripts/track2_release_v28.py verify results/feat009/jvv7_track2_research_v28
```

The first two use only tracked public files and standard-library CPU code. The third
checks the combined reviewer in a temporary public copy with Python audit guards;
it is a dependency check, not operating-system security certification. The fourth
checks the unchanged presentation and retained historical archives.

The v29 audit binds new code, fixed plans, results, contrary source review and five
additional falsification claims. All 47 claim records remain available; these are not
47 studies. Failed structural controls, mutant-backbone sensitivity, the D882N endpoint
conflict, fair held-out expression comparisons and absent QC-qualified MCF7 queries
must remain visible. See [qualification changes](track2-orthogonal-validation-v29.md)
and [archive/reproduction](track2-orthogonal-reproduction-v29.md).

The original [v19 transcriptome findings](track2-transcriptome-v19.md), v21 drug
decisions and v23/v25/v27 research remain immutable. HT29 is an assay-development
lead; no rescue-priority drug, confirmed phase or clinical margin is established.
Numerical consistency is not biological validation.

All eight H100s completed the new model and statistical waves; the Anthropic toolkit
was executed for ProteinMPNN. No owned inference job remains. Video, provider,
distribution, portal and receipt gaps remain in [readiness](track2-owner-readiness-v28.md).
Official rules/discussions were last reviewed September 24–25, not during this cycle.
