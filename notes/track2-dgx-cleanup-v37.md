# Owner-authorized DGX cleanup

19 October 2026. The owner requested deletion of unwanted DGX files. The cleanup
was restricted to reproducible uv installer caches in four completed MVA project
roots under `/home/prachh/v`: pilot-20260920, expanded-20260920,
orthogonal-20261006-v29 and optical-20261019-v33 (each prefixed `mva-track2-`).
No scientific input, output, checkpoint, model weight, log, environment, managed
Python interpreter, shared cache or unrelated project was deleted.

`scripts/track2_dgx_cleanup_v37.py` first checked exact directories, symlinks and
open/mapped files. Retained symlinks into a target cache or detected active users
would reject the cleanup. It invoked `uv cache clean --cache-dir` on each allowlisted
cache; all four exited 0. Cache directory totals fell by 36,565,536,768 allocated
bytes (about 34.05 GiB). Those totals included hard links into retained environments.
The package manager reported about 2.5 GiB plus small metadata removals, not 34 GiB
of newly free filesystem space. Concurrent unrelated work prevents attributing the
filesystem free-space change solely to this cleanup.

Plan and execution receipts are retained locally at
`results/feat009/dgx-cleanup-v37-plan.json` and `dgx-cleanup-v37-receipt.json`.
The first environment smoke command omitted the executable after `uv run` and was
rejected as syntax; a corrected explicit-environment import check is recorded in
`dgx-cleanup-v37-python-check.txt`. This was not an environment or scientific failure.
The final optical completion receipt remains present. Reinstallation can recreate
installer caches; the computational record and reproducibility inputs are preserved.

This maintenance is separate from the mandatory November 23 challenge-data deletion.
It does not satisfy or claim completion of that requirement; no confirmation email
was sent. No unrelated job was stopped.
