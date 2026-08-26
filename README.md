# MVA Hackathon 2026 — private working repo

Entry for [Rare Disease, Real Kid: The MVA Hackathon 2026](https://sagebio-rare-disease-real-kid-mva-hackathon-2026.hf.space/).

**No subject data is in this repository and none ever will be.** See `AGENTS.md`
for the access terms this repo operates under and `notes/deletion-plan.md` for
the deletion obligation.

## Setup

```bash
./scripts/download_data.sh   # ~85 GB into data/, resumable
./init.sh                    # environment + integrity + safety gates
```

Requires: `uv`, and a Hugging Face login (`hf auth login`) on an account
approved for `SageBio/mva-hackathon-2026-data`.

## State

`feature_list.json` is the source of truth for what is done. `progress.md` is
the session log.
