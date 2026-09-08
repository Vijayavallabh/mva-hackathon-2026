# Session handoff

**Last updated:** 2026-09-08, session 31. **Active feature: feat-009 Track 2.**
Owner explicitly authorized rigorous autonomous research with repeated skeptical review.
Scope and acceptance: `notes/track2-plan.md`; starting commit `21896c6`.

## Current scientific and competition state

- Owner confirms first Track 1 submission and reports **100 rank points / F-max 1**,
  leaderboard position **93**. Do not continue saying upload/score wholly unknown or
  ask for duplicate submission. Receipt and uploaded-byte identity have not been
  independently verified; feat-008 retains only this administrative archive requirement.
  Owner authorization explicitly permits Track 2 research despite that dependency.
- **Trans phase remains unconfirmed.** Feat-005b targeted recall, feat-005c fragment
  connectivity and feat-006b native phase audits supplied no linking evidence. No
  score, prediction or assumption of compound heterozygosity establishes phase.
- **The v4 CSV/report are immutable** in `results/feat008/jvv7_genomewide_mva_v4/`.
  Current hashes are checked by `uv run python scripts/track2_evidence.py track1`.
  Do not rebuild or overwrite them. Earlier v1/v2/v3 are historical, not upload choices.
- Feat-007 publication/purge is complete. Support ticket 4738585 and controlled
  authenticated/anonymous checks resolved it. Repo is public. Retain preflight guards,
  but do not recreate the old purge blocker or send another Support message.
- Owner-attested AI disclosure: OpenAI Codex API tier, no model training, no other
  AI providers. Not independently audited; does not imply zero retention. No new
  AI-provider service was used in Track 2 work.
- Public Track 2 code at `1c761cc23d90aebe6a011fd5b0b99517df42408c` allows **three
  entries, latest only reviewed**, not one. Detailed report, GitHub URL and a
  three-minute YouTube/Vimeo video URL are required. See `notes/track2-search.md`.

## Track 2 artifacts and evidence

- `notes/track2-report.md`: detailed research proposal, not a clinical treatment plan.
- `notes/track2-sources.json`: thirty source/claim/model/reading-depth records.
- `notes/track2-candidates.json`: twelve decisions; two conditional screens
  (everolimus and hydroxychloroquine), one temsirolimus benchmark, three
  deprioritizations, six exclusions. No established efficacy or measured exposure margin.
- `notes/track2-validation.md`: staged genotype/phase, RNA/protein, functional,
  matched-normal/tumour and exposure gates; randomization, blinding and replication.
  **No laboratory experiment was performed.** Genetic correction is a proposed
  positive control, not a drug or an observed rescue in this subject.
- `notes/track2-pitch.md`: approximately 401 spoken words with storyboard/timing;
  still a script, not a recorded/hosted pitch.
- `notes/track2-devils-advocate.md`: R0–R4 objections, corrections and review record.
- `scripts/track2_public_search.py`: fixed public-only queries and provenance.
- `scripts/track2_evidence.py`: offline ledger checks, qualitative rationale ablations,
  optional public source verification, draft-package build/verify, Track 1 hash guard.
- `scripts/test_track2_evidence.py`: adversarial unit/regression checks; no subject input.

Public caches are ignored under `results/feat009/`. The initial version-only Europe PMC
response produced an **invalid** search summary; it is not zero-hit evidence. The
expanded focused run retrieved 138/138, 404/404, 7/7, 12/12 and 5/5 overlapping hits,
with no failed requests. This is not full independent screening of every paper.
Final source-verification-v2 recorded 19/19 DOI/title matches and 11 official pages
retrieved, zero errors/review flags. Identifier checks do not establish scientific truth.

## Blockers and unresolved evidence

- **Track 2 delivery:** final recorded three-minute pitch, public playable URL,
  authenticated quota check and portal receipt remain outstanding. Do not equate a
  script or a locally built package with submission. Do not spoof authentication.
- **Track 1 archival check:** obtain the existing receipt when available, not another
  upload. This does not block literature, code or draft-report work.
- **Science:** exact-allele functional effects, phase, tumour context, pathway activity
  and exposure-supported normal/tumour margin remain unknown. The two conditional
  screens are experiments to falsify, not drugs recommended for the child.
- Do not seek family contact, acquire patient samples, order treatment, or transfer
  subject files to answer these questions. Authorized laboratory/material access would
  be required for future wet-lab work. No clinical dose is proposed.
- Preferred external search/image skill services lacked authentication; public web/API
  retrieval and local text schematics were used. No extra model provider was introduced.

## Resume and verify

```bash
./init.sh
uv run python scripts/track2_evidence.py check
uv run python scripts/test_track2_evidence.py
uv run python scripts/track2_evidence.py sensitivity
uv run python scripts/track2_evidence.py track1
```

Continue feat-009 only: address documented review findings, verify draft-package
integrity, refine the scientific/pitch delivery and prepare a hosted pitch. The current
review/test/commit record is appended to `progress.md` and the adversarial log.
Do not infer completion from the presence of a report draft.

## Retained earlier work and guardrails

Feat-001 through feat-007, including feat-005b/005c/006b, are complete. Baseline,
commands and limitations remain in `notes/data-profile.md`, `notes/vcf-triage.md`,
`notes/targeted-recall.md`, `notes/phase-connectivity.md`, and
`notes/track1-evidence-audit.md`. The coarse negative ROH screen does not exclude
consanguinity. The low-level chr19 copy-number screening signal is not a clinical
karyotype or drug-sensitivity assay. Family reproductive history is a separate input,
not an abnormality measured in the proband.

Earlier local manual-review items (not new causal findings): a heterozygous DELLY
event overlaps a padded TRIP13 window without orthogonal validation; an L003 read-index
difference has not been established as a systematic library difference. Do not emit
subject records to investigate either. No new phase data was generated in Track 2.

`data/`, `results/` and `logs/` stay ignored. Recovery mirrors/maps/bundles under
`results/feat007/` can retain obsolete history; never republish them. Deletion scope
includes caches, derived copies and retired Git objects/reflogs. Use uv only, local
toolchain pins and fresh `./init.sh`. Check shared hardware before any large job.

Commit intended changes, push configured origin, verify upstream equality and a clean
tree. Raw subject records/narrative never enter model context or external services;
permitted derived summaries and public literature do. Submission closes 2026-10-24
23:59 UTC; data deletion and confirmation are due by 2026-11-24.
