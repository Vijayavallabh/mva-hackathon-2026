# Track 2 deadline refresh, version 44

20 October 2026, 15:34:56 UTC. This is an anonymous public-source refresh,
not a contact, authenticated account check or submission preflight. It checked
the live Space revision, all seven official files, and the public discussion
listing. It did not reread every discussion thread, private content, edit
history, authenticated quota, eligibility or provider settings.

The live Space revision remains `60e1c30e337ce6fe01813040dbe49979eb8c50aa`.
All seven official files remain hash-identical to the v42 capture: README,
config, about, rules, FAQ, submit_track2 and the methods workbook template.
The public discussion listing still contains 31 discussions, including the same
numbers, statuses and titles as the v42 capture; 16 are closed. The listing does
not expose comment bodies, so no thread-content reread is claimed. No new
organizer requirement was found.

Consequently the deadline remains **October 24, 23:59 UTC**; the pitch remains
at most **180 seconds** on YouTube/Vimeo; methods B9 remains required; B17
remains limited to 500 words; the rubric remains **35/25/25/15**; three entries
are allowed with only the latest reviewed; quota remains unknown; winners are
announced December 18; and deletion/confirmation remains due by **November 23**
to **cnb@sagebase.org**.

The current v43 report/deck/exports already meet these unchanged requirements.
No drug disposition, biological claim, recording state, provider setting,
hosting result or submission readiness changes. This refresh does not authorize
organizer contact or family contact.

## Reproduction

The exact live Space revision and discussion-listing requests are recorded in
`notes/track2-requirements-v44.json`. Historical receipts remain in
`sources/public-official-v42/`. Check this refresh with:

```bash
uv run --no-project python scripts/check_track2_requirements_v44.py
uv run --no-project python -m unittest scripts.test_track2_requirements_v44
```

This is public requirements provenance, not biological validation.
