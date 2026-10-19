# Reproduce the completed optical comparison

This study uses unrelated public Funk HeLa data, Dataverse DOI
[10.7910/DVN/VYKTI5](https://doi.org/10.7910/DVN/VYKTI5), version 2.0, CC BY 4.0.
No challenge source record, clinical narrative, API key or gated file is required.
The source DOI, version, per-file hashes and executed code/environment hashes are
retained in the review archive. [Results and interpretation](track2-optical-v36.md)
separate original tests, amendments, exploratory controls and biological limits.

## Review retained evidence on a CPU

```bash
uv run --no-project python scripts/check_track2_optical_v36.py
uv run --no-project python scripts/track2_public_review_v36.py
uv run --no-project python scripts/check_track2_harness.py
```

These commands use public tracked records and the standard library, without source
matrices, model weights, network or GPUs. They check declared evidence and file
identity; they do not rerun inference or establish biology.

The local archive lives at `results/feat009/optical-v36/optical-v36-review.tar.gz`;
its adjacent `manifest.json` binds every member. It contains review JSON, source
manifests, execution receipts, scripts, logs and the pinned environment. Source
parquet, prepared matrices and checkpoints remain on the owner host. This is not
a complete raw-data or model-binary archive. Replay into a new output path:

```bash
uv run python scripts/track2_optical_archive_review_v36.py results/feat009/optical-v36/optical-v36-review.tar.gz results/feat009/optical-v36/manifest.json --output results/feat009/optical-v36/replay-new.json
uv run scripts/track2_optical_workbook_v36.py results/feat009/optical-v33/coverage/sources/genes.xlsx results/feat009/optical-v36/results.json --output results/feat009/optical-v36/workbook-new.json
```

The workbook is public `https://vesuvius.wi.mit.edu/genes.xlsx`. Its retained hash
is in the workbook receipt. It represents the same originating experiment;
matching it is a representation check, not an independent biological replication.
Archive replay recomputes guide ranks to gene/macro MRR using `math.fsum`, then
reuses the registered paired-bootstrap implementation. The latter is reproduction,
not a separately written statistical algorithm. It retains all six real/shuffled
comparisons per arm and post-hoc plate-only/within-plate metrics.

The tracked result uses whitespace-only compact JSON to stay below the repository's
5,000,000-byte blob limit: 4,709,908 bytes instead of 10,728,780. The
[encoding receipt](track2-optical-public-encoding-v36.json) binds both hashes.
The public checker reconstructs the original analysis bytes and requires their
hash to match the original workbook receipt. No measurement or decision changes.
The oversized release candidate, all 812 bound inputs and its ZIP remain in
`results/feat009/v36-size-gate-rejected-20261019/`. Reproduce the encoding into new paths:

```bash
uv run --no-project python scripts/track2_optical_public_pack_v36.py results/feat009/optical-v36/results.json results/feat009/optical-v36/public-new.json --receipt results/feat009/optical-v36/encoding-new.json
```

## Heavy reproduction and preserved execution

All work ran under `/home/prachh/v/mva-track2-optical-20261019-v33` on
`PrakashDGX_H2`, using `/home/prachh/v/bin/uv`, the root's isolated environment,
locked `uv.lock`, and eight owner-authorized H100s. Use a **new root beneath
`/home/prachh/v`** for a fresh reproduction. Do not overwrite completed outputs,
restart finished supervisors or modify scripts registered by an active job.
Set TMPDIR/cache locations under the chosen root. The remote scripts enforce
storage/free-space and worker-completion gates; inspect available resources first.
Long jobs use `nohup` with their logs under that root.

The executed sequence is recorded by the supervisor registrations and terminal
receipts, rather than inferred from a successful launch:

1. Download both complete public exports and verify all advertised checksums.
   Original `track2_optical_fetch_v33.py` and registered plans define source scope.
2. Exclude the four absolute image centroids with `track2_optical_prepare_v35.py`.
   The mitotic equivalence replay must reproduce every retained value, identity,
   guide count, feature sum and mean. Original v33 fits remain excluded.
3. For interphase, use `track2_optical_prepare_v36.py` for the legitimate empty
   shard. Its wrapper preserves nonempty v35 processing and archived partial work;
   all 3,027 shard receipts remain. The failed v35 attempt is retained.
4. Run `track2_optical_independent_v35.py` for independent CPU reductions of all
   40 fixed query guides in each arm. Run `track2_optical_run_v35.py` for each
   arm's four real and four shuffled 3,000-step fits; never use the old v33 model.
5. Run `track2_optical_audit_v35.py`, `track2_optical_plate_run_v35.py` and
   `track2_optical_plate_summary_v35.py`
   for each arm. Plate coverage varies; a pooled-trained encoder is not an
   unseen-acquisition test. Preserve missing query states.
6. `track2_optical_median_v35.py` computes complete featurewise guide medians
   with eight workers per arm, combining all source rows for each guide. Verify
   all 40 named query guides against CPU float64 medians. Do not average shard
   medians. `track2_optical_secondary_v35.py` adds the matched cross-arm fraction,
   exactly matched sampled-cell mean and two median preprocessing views.
7. `track2_optical_plate_control_v36.py` tests plate-only and same-plate full
   profiles under its explicitly post-hoc plan. It cannot replace the original
   gain gate or establish unseen-batch generalization.
8. `track2_optical_package_v36.py` requires successful terminal receipts and all
   declared workers. It checks source/output hashes and creates a new review
   archive. `track2_optical_finalize_v36.py` serializes the final controls and
   packaging; it never terminates another user's work.

The exact executable names/options, seed configurations and environment are in
archive `scripts/`, `pyproject.toml`, `uv.lock` and `outputs/*/registration.json`.
The original, correction, secondary, median and post-hoc plate plans are tracked
separately. The 128-cell cap, feature clipping, fixed gene split and coverage
thresholds did not change in response to favorable query ranks. All seeds and
controls remain. Full-cell and capped-cell comparisons answer different questions.

## Limits and retention

Source preparation and export checking include CPU/I/O work; eight-GPU use does
not mean continuous saturation. Seeds, guide profiles and resampled genes are not
new biological experiments. The trained MLP is a purpose-built benchmark, not a
claim to a state-of-the-art foundation model. No clinical or drug decision changed.
The remote root and all caches fall within the November 23 deletion/confirmation
scope in [deletion plan v2](deletion-plan-v2.md). No deletion was performed here.
