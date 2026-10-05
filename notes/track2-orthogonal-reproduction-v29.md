# Reproduce Track 2 v29

The calculations use public reference sequence, predicted domain structures and LINCS
expression resources. They require no subject files. All original records are preserved.

## Public review

```bash
uv run --no-project python scripts/check_track2_orthogonal_v29.py
uv run --no-project python scripts/check_track2_harness.py
```

These standard-library checks verify complete aggregate probability distributions,
control ordering, background ranks, 400 held-out expression fits, missing-query/QC
handling, source hashes and unchanged biological/delivery status. They do not rerun
neural inference or establish biological validity.

## Archived output and independent local recomputation

Archive: `results/feat009/orthogonal-v29/orthogonal-v29-audit.tar.gz`.

- SHA-256: `373d78784dabc003335813736f907348f7c90aaac510e242b0c917eff8e5280e`
- Bytes: **1,645,137,933**; **3,838 files**.
- Includes original per-draw probability/score arrays and fixed-site FASTAs, all
  held-out reference panels and fitted bases, 12 input CIFs, plans, metadata hashes,
  locks, executed scripts, worker logs, numerical controls and failed attempts.
- Excludes model weights, environment caches, large reused expression matrices,
  credentials and protected subject inputs.

Use new destinations:

```bash
uv run python scripts/archive_track2_orthogonal_v29.py verify \
  results/feat009/orthogonal-v29/orthogonal-v29-audit.tar.gz \
  results/feat009/v29-replay-archive
uv run python scripts/analyze_track2_orthogonal_v29.py \
  results/feat009/v29-replay-archive . results/feat009/v29-replay-analysis
uv run python scripts/summarize_track2_orthogonal_v29.py \
  results/feat009/v29-replay-archive results/feat009/v29-replay-analysis
```

Archive verification rejects duplicate, traversing, absolute, symlink and nonregular
members, limits total size, verifies every digest, and extracts only to a new directory.
The analyzer verifies every fixed residue in all 67,584 samples and rebuilds all
aggregate probabilities, control decisions and expression records. Compare the four
published scientific JSON/TSV outputs plus compute summary with `notes/`. Float formatting
may depend on NumPy version; the original remote and local comparison is recorded in
`track2-orthogonal-audit-v29.json`.
The public expression JSON uses compact formatting to meet the repository's blob-size
gate; the public TSV uses LF line endings. These formatting changes preserve all values.
Original remote and locally regenerated files remain available for byte comparisons.

`structural-draws-v29.tsv` is a regenerated convenience file for selected mutation
log-odds trajectories; all amino-acid probabilities for every draw remain in the archive.
No draw count is an independent biological sample size.

## Fresh owner-host execution

Original root: `/home/prachh/v/mva-track2-orthogonal-20261006-v29`.
Do not overwrite it. Create a new root under `~/v`, update `TASK_ROOT` in the setup and
launch scripts, and copy the public inputs under the names in the archive. The new
root's parent must still contain the existing `bin/uv`, or update that runner path.

Clone the toolkit with sparse paths `common` and `proteinmpnn` at
`f4f62fa6592ae4938d49b1757bea0cfeff9f468e`. Run
`setup_track2_orthogonal_v29.sh` through `nohup` into the new `logs/` folder. It installs
a separate uv project and pinned upstream ProteinMPNN, without system packages or
changes to historical environments. Python 3.11.5, torch 2.5.1+cu124, NumPy 1.26.4,
Biopython 1.84 and setuptools 68.1.2 are recorded in the model lock. Other resolved
dependencies are locked; this is not a claim that every package matches the toolkit's
full reference container lock.

The preparer verifies and reuses ESMFold2 CIFs from
`~/v/mva-track2-expanded-latest-20260921/` and expression matrices from
`~/v/mva-track2-crispr-20261001-v25/outputs/prepared/`.
The [earlier reproduction notes](track2-falsification-reproduction-v27.md) link their
public reconstruction routes. Archived CIFs can also be staged under the expected
source paths in a separate replay tree; preserve the supplied hashes and reference
identities. Expression execution uses the frozen v19 torch environment and its recorded
lock, not the ProteinMPNN environment.

```bash
nohup bash scripts/run_track2_orthogonal_v29.sh > logs/model-launch.log 2>&1 < /dev/null &
# After that wave finishes and all eight GPUs are free:
nohup bash scripts/run_track2_crossfit_v29.sh > logs/expression-launch.log 2>&1 < /dev/null &
```

Both launchers check GPU availability and stop on failure. No unrelated process is
terminated. In the original session, expression ran while the protein runtime dependency
was repaired, then the protein wave ran after expression completed. That scheduling
change does not alter either analysis plan. The successful model pilot compares
stock/exact outputs and checks a paired direct-conditional calculation before launching
eight workers. Source code is unchanged; setup/format/runtime failures remain archived.

Finish with `archive_track2_orthogonal_v29.py build` after both completion markers exist.
The archive binds original executed scripts; later public summary/checker scripts are
separately bound by the v29 audit. Retain all owned remote copies in the November 24
deletion scope. There is no recorded video or Track 2 submission from this workflow.
