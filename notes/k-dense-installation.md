# Project-local K-Dense BYOK

Owner-requested installation, 2026-09-13 IST, supporting feat-009. Upstream:
https://github.com/K-Dense-AI/k-dense-byok, revision
`2c613e38052f199526546191c8d8b98c1eb3b15e` (server version 0.10.0).
The clone and its dependencies are in ignored `tools/k-dense-byok/`.
No global npm package, shell-profile change or system package is required.
Existing Node 22.22.3, npm 11.17.0 and uv are used.

From this repository:

```bash
node scripts/k-dense.mjs
```

Open <http://localhost:3210>; backend: <http://localhost:8210>.
Both listeners bind to 127.0.0.1. Keep the terminal open; Ctrl+C stops both.
For a browser on another computer, forward both ports over SSH:

```bash
ssh -N -L 3210:127.0.0.1:3210 -L 8210:127.0.0.1:8210 USER@THIS_MACHINE
```

Then visit localhost:3210 on that computer. Configure your chosen provider in
Settings → API keys or Model providers. No key or subscription was copied from
the parent repository or the user's other applications; no inference was run.

Use the repository launcher above to preserve this installation's local scope.
It gives the app a minimal environment, without ambient provider credentials or
the parent `.env`. Pi auth/settings live in `tools/k-dense-byok/.local/pi-agent/`,
skills/npm/uv caches in `.cache/`, uv-managed Python downloads in `.local/python/`,
and app workspaces in `projects/`, all beneath that clone. Any app `.env` created
by Settings also stays in the ignored clone. Next.js telemetry is disabled.
The launcher refuses occupied ports and does not kill other services.

The app's project folder is **not an operating-system security sandbox**. Use
public literature and permitted derived summaries only. Do not import, attach,
symlink or direct a hosted agent to the source FASTQ/BAM/CRAM/VCF or phenotype
narrative. A local web app can still send prompts and tool results to hosted
providers. The repo's subject-data rules apply to all future use. Installing
this tool does not amend historical provider attestations or submission files.
Any future research use must record the actual providers and outputs used.
App workspace copies and chats are included in the existing deletion obligation.

Reproduce the install:

```bash
git clone https://github.com/K-Dense-AI/k-dense-byok.git tools/k-dense-byok
git -C tools/k-dense-byok checkout 2c613e38052f199526546191c8d8b98c1eb3b15e
node scripts/k-dense.mjs install
node scripts/k-dense.mjs check
```

`install` runs locked `npm ci` for both services, then the upstream `prep` to
seed an empty default workspace, scientific skills and uv environments.
`prep` can be run separately; `check` checks executables and upstream runtime
requirements without starting services. Ordinary start uses installed packages.
Upstream prep is best-effort: check its printed skills/venv results, since exit
success alone does not prove every optional download succeeded.

The existing project startup check needed one repair: GATK's launcher uses
`/usr/bin/env python`, which is absent in a fresh shell. `init.sh` now runs the
toolchain check with `uv run bash`, putting the existing project interpreter on
PATH. Tool versions, checksums and validation criteria are unchanged.

Validation and actual startup output are recorded in `progress.md`.
