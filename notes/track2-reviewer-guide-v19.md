# Track 2: review the presentation and completed research together

27 September 2026. Start with the [v18 report](track2-report-v18.md) and the
[v19 public transcriptome addendum](track2-transcriptome-v19.md). The report presents
the conditional everolimus experiment; the addendum adds completed public-data
falsification and stricter model/compound qualification requirements. The v18 report,
eight-slide deck and 334-word narration remain preserved, and do not contain the
later transcriptome analysis. There is no combined v19 submission package or recorded
pitch. [Current artifact paths](track2-current.json) distinguish these roles.

## One public review command

```bash
uv run --no-project python scripts/check_track2_harness.py
```

The standard-library check now covers both the v18 presentation and v19 research.
It verifies the current routes, scientific/delivery status, frozen campaign hashes,
complete result checks, numerical counts, failed filters and the limited favourable
HT29 result. It needs no subject files, `data/`, `results/`, `.env`, Git history,
network, SSH, GPU, model weights or local historical archives. It does not recalculate
all expression scores, verify eligibility, establish efficacy or submit an entry.

To repeat the dependency audit from a working Git checkout:

```bash
uv run --no-project python scripts/audit_track2_harness.py
```

The audit helper uses the Git file list to stage a temporary public-only copy. Its
child review uses the uv interpreter's base installation, without the project virtual
environment or Git history. Six explicit probes confirm the Python audit hook blocks
network access, new processes, protected files, credentials, outside files and writes.
This is a dependency audit, not an operating-system sandbox assessment.

The following commands remain available for narrower or historical checks:

| Command | Scope |
|---|---|
| `uv run --no-project python scripts/track2_public_review_v18.py` | Frozen v18 presentation, methods and prior evidence |
| `uv run --no-project python scripts/check_track2_transcriptome.py` | Frozen v19 campaign consistency and bound public artifacts |
| `uv run python scripts/track2_release_v18.py verify results/feat009/jvv7_track2_research_v18` | Exact-byte v18 snapshot and retained earlier local releases |
| `uv run --no-project python scripts/verify_track2_transcriptome_archive.py results/feat009/transcriptome-remote-v19/transcriptome-v19-audit.tar.gz` | The retained 457-file public-data archive |
| `./init.sh` | Local environment, protected-data gate, dataset/toolchain resources and the combined harness |

## Read the result with its limits

- Fourteen BUB1B contexts fail the full primary operational query filter. This is
  an uncalibrated screening requirement, not proof of biological unreliability.
- The post-hoc full filters pass 0/42. HT29 has a five-reagent projected adjusted
  tail of approximately 0.042 and fails the declared six-reagent minimum. Retain this
  partial positive; do not replace the primary analysis or erase the counterweight.
- Everolimus has 13 positive raw correlations in 19 primary comparisons, which reuse
  fourteen drug profiles. Positive correlation is not proof of harm.
- Of 180 second-release everolimus-labelled profiles, 174 have unresolved stereo
  metadata; the six reference-matching profiles fail the specified drug QC. Do not
  merge their identifiers or claim a qualified low-dose response.
- All eight H100s completed three waves, but utilization was bursty. The 312,438
  compound profiles, 12,185,082 comparisons and 560,000 resamples are not independent
  biological experiments. No new neural-model inference or wet-lab work ran.

The [v15 claim register](track2-falsification-register-v15.json) and
[validation plan](track2-validation-v15.md) remain in force alongside the addendum's
revised requirements: qualify endogenous function and on-target perturbation, verify
chemical identity, then measure joint treatment and functional endpoints. No drug
earns rescue priority. Everolimus remains an optional qualified mechanistic probe;
HCQ is reserve. Phase and clinical exposure margins remain unresolved.

## Reproduce or prepare a later package

The [v18 guide](track2-reviewer-guide-v18.md) retains report/workbook/slide export
commands and historical notices. The [v19 execution record](track2-transcriptome-reproduction-v19.md)
documents GEO sources, plans, environment, CUDA commands, full score/null arrays,
archive omissions and a new-directory requirement. Neither workflow should overwrite
the retained v1–v18 releases or v19 campaign inputs.

For future presentation integration, create a new version of the report, slides,
narration, disclosure/methods exports and release manifest. Do not edit v18 in place or
describe its recording bundle as including v19. Provider handling, distribution scope,
recording/hosting, final live portal checks and the receipt remain in the
[updated readiness note](track2-owner-readiness-v19.md). The current rules evidence is
dated September 24–25; this harness update did not recheck the website or discussions.
