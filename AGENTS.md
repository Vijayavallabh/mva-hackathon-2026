# AGENTS.md

Private working repo for **Rare Disease, Real Kid: The MVA Hackathon 2026**
(Sage Bionetworks / MVA Society). Single-subject WGS of a child with Mosaic
Variegated Aneuploidy. Two tracks: variant prediction (auto-scored) and drug
repurposing (panel-judged). Close: **24 Oct 2026 23:59 UTC**.

## Non-negotiable rules

These come from the signed data-access terms, not from style preference.

1. **No subject data leaves this machine.** Never commit, upload, paste, or
   send any FASTQ/BAM/VCF/phenotype content anywhere — including into a model
   prompt hosted by a third party, an issue, or a public repo. `data/`,
   `results/` and `logs/` are gitignored and a pre-commit hook enforces it.
2. **No re-identification, no contacting the family or the MVA Society.**
3. **Delete everything by 24 Nov 2026** (30 days after close), then email
   RarediseaserealkidMVAhackathon2026@synapse.org to confirm. See `notes/deletion-plan.md`.
4. **Embargo**: code and derived outputs may be shared publicly at any time;
   manuscripts using the dataset may not be submitted until organizers publish
   their summary report.

If a task appears to require breaking one of these, stop and ask.

## Startup workflow

```bash
./init.sh          # env + data integrity + no-data-in-git gate
cat feature_list.json    # pick exactly ONE unfinished feature
git log --oneline -5
```

Test command (the only automated test in the repo):
`uv run python scripts/verify_data.py --self-check`

## Environment

**uv only.** No conda, no pip, no system python.
- add a dep: `uv add <pkg>` (never `pip install`)
- run anything: `uv run <cmd>`
- Bioinformatics binaries that are not pip-installable (bcftools, samtools,
  bwa-mem2) go in `tools/` via `scripts/get_tools.sh`; record the version there.

Hardware: this box has 5x A100 80GB + 1x T400. `PrakashDGX_H2` (6x H100) is
reachable over SSH for heavier jobs but the data stays here unless the user
says otherwise.

## Layout

```
data/       85 GB gated dataset (gitignored, never committed)
scripts/    download, tooling, pipeline entry points
results/    all derived output (gitignored — contains subject genotypes)
notes/      tracked markdown: findings, hypotheses, deletion plan
```

## Working rules

- One feature at a time from `feature_list.json`; update `status` + `evidence`
  in the same commit as the work.
- Every claim about the genome needs the command that produced it recorded in
  `notes/` — the submission must be reproducible from this repo alone.
- Long GPU/CPU jobs: `nohup` into `logs/`, never block the session.
- Don't claim done without running `./init.sh` and pasting real output.

## Definition of done (per feature)

- [ ] Behavior implemented
- [ ] `./init.sh` passes, output recorded
- [ ] `evidence` field in `feature_list.json` names the artifact and command
- [ ] `notes/` updated if a scientific claim changed

## Scope boundary

In scope: everything under `scripts/`, `notes/`, and the harness files.
Out of scope without asking: touching other repos under
`/mnt/md0/IITM/BackUp/Home/vijayavallabh/`, installing system packages,
pushing to any remote other than `origin`, and any change to the two
submission deliverables after they have been uploaded.

## End of session

1. Update `progress.md` (append a dated section) and `feature_list.json` status/evidence.
2. Record blockers in `session-handoff.md` under Blockers.
3. Commit — the pre-commit hook runs the no-data gate for you.
4. Clean restart path: `./init.sh` must pass from a fresh shell with no
   arguments and no manual setup. If it does not, fix that before ending.
