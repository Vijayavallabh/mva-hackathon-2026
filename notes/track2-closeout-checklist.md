# Track 2 post-submission close-out checklist

20 October 2026. This is a preparation note for feat-010. It does not authorize deletion
before the required date and does not claim that submission, hosting, review, receipt
archiving or deletion has occurred. Use it only after Track 2 submission is complete and
the owner has decided that no further reproduction or urgent post-submission response is
needed. Preserve all immutable snapshots, bound inputs and earlier releases until then.

## Non-negotiable order

1. Confirm Track 2 submission was actually completed by the owner.
2. Archive exact uploaded bytes, URLs and the authenticated submission receipt.
3. Perform a final authenticated portal/identity/quota check.
4. Decide whether any judge question, clarification or appeal requires reproduction.
5. Only then begin deletion, with the inventory below and per-root verification.
6. After all copies are verified removed, send one truthful confirmation email.

Deadline: delete and confirm to cnb@sagebase.org by 23 November 2026.
That supersedes every frozen historical November 24 note or recipient.

## Pre-deletion gate

- [ ] Owner confirms final submission and receipt are archived outside the deletion scope.
- [ ] Uploaded report, workbook, slides, methods workbook, video URL and receipt are saved.
- [ ] Any judge response window or requested clarification is resolved or explicitly closed.
- [ ] No pending process references any root below (check on each host, not only this one).
- [ ] No owner-requested reproduction or close-out analysis is still planned.
- [ ] Unrelated owner files are separated from project data by explicit inventory.
- [ ] A separate copy of any material the owner is legally permitted to retain has been made
      only after checking challenge publication/retention terms and AF3/Atlas output terms.

## Local inventory

Delete only after the gate above is fully checked and each item is inventoried:

- `data/`
- `results/`
- `logs/`
- dataset caches and subject-bearing intermediates
- recovery bundles
- local copies of public inputs used only for this challenge
- local model/caches retained solely for this campaign

The tracked public repository, notes and permitted derived summaries remain governed by
the organizers' publication terms. Do not delete the GitHub history before the owner has
confirmed whether public code and derived outputs remain permitted or required.

## Other-host inventory

These roots are explicitly in the deletion scope. Sizes were checked on 20 October 2026.
All completed campaigns had already passed local archive verification at that time; that
verification does not authorize earlier deletion.

- `PrakashDGX_H2:/home/prachh/v/mva-track2-pilot-20260920` (about 16 GiB)
- `PrakashDGX_H2:/home/prachh/v/mva-track2-expanded-20260920` (about 257 GiB)
- `PrakashDGX_H2:/home/prachh/v/mva-track2-expanded-latest-20260921` (about 120 GiB)
- `PrakashDGX_H2:/home/prachh/v/mva-track2-transcriptome-20260927` (about 62 GiB)
- `PrakashDGX_H2:/home/prachh/v/mva-track2-rnai-20260927-v23` (about 16 GiB)
- `PrakashDGX_H2:/home/prachh/v/mva-track2-crispr-20261001-v25` (about 51 GiB)
- `PrakashDGX_H2:/home/prachh/v/mva-track2-falsification-20261001-v27` (about 136 MiB)
- `PrakashDGX_H2:/home/prachh/v/mva-track2-orthogonal-20261006-v29` (about 11 GiB)
- `PrakashDGX_H2:/home/prachh/v/mva-track2-perturbseq-20261007-v31` (about 31 GiB)
- `PrakashDGX_H2:/home/prachh/v/mva-track2-optical-20261019-v33` (about 368 GiB)

Related other-host caches and project-only environments under those roots are included.
Do not use a broad wildcard that could touch unrelated owner projects. Delete by the
exact enumerated root after a fresh `ps`/open-file check and a fresh size/path inventory.

## Verification commands before deletion

Run these on the relevant host, not only from memory:

```bash
# Local repository state
git status --short
git branch -vv
git log --oneline -5

# Other-host active processes and inventory
ssh PrakashDGX_H2 'ps -eo user,pid,etime,cmd | grep -E "mva-track2" | grep -v grep || true'
ssh PrakashDGX_H2 'find /home/prachh/v -maxdepth 1 -type d -name "mva-track2-*" -printf "%p\n" | sort'
ssh PrakashDGX_H2 'du -sh /home/prachh/v/mva-track2-* 2>/dev/null'
```

If any process is active, stop and resolve it. Do not kill another owner's job. If an
expected root is missing or an unexpected root appears, inventory it before proceeding.

## Per-root deletion procedure

For each root, in this order:

1. Confirm the exact absolute path and that it is an `mva-track2-*` directory.
2. Check for active processes/open files using that root.
3. Record its byte size and file count before deletion.
4. Delete only that root with `rm -rf --one-file-system -- <exact-path>`.
5. Verify the path no longer exists.
6. Record the completed deletion in the close-out log below.

Do not batch all roots into one command until the first few have been verified. If
deletion is interrupted, re-inventory before retrying.

## Post-deletion verification

After all local and remote roots are removed:

- [ ] Each enumerated local path is absent.
- [ ] Each enumerated other-host path is absent.
- [ ] No `mva-track2-*` project root remains on PrakashDGX_H2.
- [ ] No source FASTQ, BAM/CRAM, VCF or phenotype document remains outside the tracked
      permitted summaries.
- [ ] Dataset caches and recovery bundles are absent.
- [ ] The public repository contains only code and permitted derived summaries.
- [ ] Record the final disk-free state on the other host.

Only after every verification passes, send the truthful confirmation email to
cnb@sagebase.org. Do not send it earlier or based on an incomplete deletion.

## Close-out log

Record each deletion only after it is verified. Do not prefill this table.

| Host | Path | Pre-deletion size | Verified absent | Date/time (UTC) | Operator |
|---|---|---|---|---|---|
| local | `data/` | | | | |
| local | `results/` | | | | |
| local | `logs/` | | | | |
| PrakashDGX_H2 | `mva-track2-pilot-20260920` | | | | |
| PrakashDGX_H2 | `mva-track2-expanded-20260920` | | | | |
| PrakashDGX_H2 | `mva-track2-expanded-latest-20260921` | | | | |
| PrakashDGX_H2 | `mva-track2-transcriptome-20260927` | | | | |
| PrakashDGX_H2 | `mva-track2-rnai-20260927-v23` | | | | |
| PrakashDGX_H2 | `mva-track2-crispr-20261001-v25` | | | | |
| PrakashDGX_H2 | `mva-track2-falsification-20261001-v27` | | | | |
| PrakashDGX_H2 | `mva-track2-orthogonal-20261006-v29` | | | | |
| PrakashDGX_H2 | `mva-track2-perturbseq-20261007-v31` | | | | |
| PrakashDGX_H2 | `mva-track2-optical-20261019-v33` | | | | |

Email sent: not yet.

## What this checklist does not do

- It does not authorize contacting the family or MVA Society.
- It does not authorize organizer contact before the required confirmation email.
- It does not establish biological validation, submission readiness or prize eligibility.
- It does not change any drug disposition, claim, presentation version or bound artifact.
- It does not permit deleting unrelated owner work or other projects on the shared host.
- It does not resolve the challenge publication/retention or AF3/Atlas output terms.
