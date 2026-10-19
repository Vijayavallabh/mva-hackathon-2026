# Empty interphase shard: preparation repair

19 October 2026. The v35 interphase preparation stopped at 12:50:09 UTC before
any interphase model fit. The downloaded public export contains 3,027 parquet
shards plus two metadata files. Footer inspection found one empty shard,
`part.3.parquet`, Dataverse file 6421679 (684,563 bytes). The other completed
preparation receipts cover 2,378 shards and 24,409,280 cells at the failure audit.
These are partial progress counts, not the final study population.

The failure was `ValueError: need at least one array to concatenate`. The source
file has zero rows; the implementation assumed at least one guide. V36 writes
correctly typed zero-row summaries and verifies source size, checksum and footer.
It does not manufacture a zero phenotype, add a guide or drop a subject observation.
Nonempty shards continue through the unchanged v35 code. Completed shards are
hash-checked; incomplete outputs move into a preserved failure directory before
repair. No feature, threshold, split, cell sample, fit or scoring policy changes.

`track2_optical_prepare_v36.py` calls the existing v35 merge and adds the repair
code hash, all source-shard receipt hashes and empty-file identity to the final
preparation receipt. The original failed supervisor, log and script remain intact.
The replacement supervisor uses a new `interphase-v36-pipeline` directory, retaining
the v35 model/audit/plate workers and output naming. The secondary-controls
supervisor waits for this replacement's successful terminal receipt.

A regression combines an empty shard with a nonempty shard, verifies exact sums,
finite counts and sample counts, checks idempotent receipt verification and retains
the incomplete artifact. Remote tests use TMPDIR under the authorized v root.
An earlier broad remote test invocation used the default temporary filesystem and
failed its free-space guard; it launched no secondary supervisor. That operational
failure is preserved in `logs/test-controls-v35.log` and is not a scientific result.
