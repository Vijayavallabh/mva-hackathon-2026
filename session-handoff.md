# Session handoff

**Last updated:** 2026-09-08, session 32. **Active feature: feat-009 Track 2.**
The user requested rigorous final scientific/exposure review. Baseline `1a97a0e`;
review specification and findings: `notes/track2-final-review.md`.
The previous session's equal-priority HCQ nomination is superseded.

## Current scientific and competition state

- The owner reports first Track 1 submission: **100 rank points / F-max 1**, leaderboard
  position **93**. Independent receipt/uploaded-byte archival remains the sole feat-008
  administrative blocker, not a reason to resubmit or block authorized Track 2 research.
- **Trans phase remains unconfirmed.** No new genetic/phase experiment occurred here.
- Preserve `results/feat008/jvv7_genomewide_mva_v4/` byte-for-byte. Check with
  `uv run python scripts/track2_evidence.py track1`; current-file identity does not
  independently verify the uploaded bytes.
- Feat-007 purge/publication is complete; repo public; Support ticket 4738585. Do not
  recreate the old purge blocker, change visibility or contact Support/family.
- Owner-attested AI disclosure: OpenAI/Codex API tier, no model training and no other
  providers. This is not an account audit or zero-retention claim. No extra provider used.
- Public Track 2 code permits **three entries, latest only reviewed**. Report, GitHub URL
  and a three-minute YouTube/Vimeo URL are required; no Track 2 upload has occurred.

## Final review outcome and artifacts

- **Everolimus: one conditional, phenotype-first research priority.** Measure mTORC1
  excess before screening; require functional benefit, exposure and deficient-normal safety.
- **HCQ: reserve/deprioritized**, not an equal-priority lead. Closest compound-level
  adult everolimus/HCQ trial is included with its positive single-arm endpoint and limitations.
  No pediatric RMS or genotype-specific therapeutic window follows.
- Twelve candidates: one conditional screen, one temsirolimus benchmark, four
  deprioritizations and six exclusions. No established clinical efficacy.
- `notes/track2-report.md`: research draft 2; `track2-final-review.md`: extended
  scientific, PK/PD, negative/positive evidence and horizon review.
- `notes/track2-sources.json`: **53 curated sources**, 40 DOI-bearing papers/notices,
  eleven official pages and two chemical-property records. Selected text/abstract reading,
  not complete reading of all search results.
- `notes/track2-exposure.json`: eight public-study/label observations, with parent/salt,
  matrix, binding, timing, endpoint and population retained. All clinical margins null.
  `scripts/track2_exposure.py` converts units, not clinical doses or therapeutic margins.
- `track2-validation.md`: proposed assays only; measured exposure, reporter controls,
  matched deficient-normal assessment, RMS comparator and combination-antagonism gates.
- `track2-pitch.md`: about 408 spoken words / 136 words per minute; not a recording.
- `track2-devils-advocate.md`: separate standards/spec findings and revision record.

## Reproducibility and review evidence

Supplementary public search: twelve fixed sets, **941 distinct source/ID records**, no
failed/truncated queries in `results/feat009/final-review-search-v2-20260908/`. This is
not 941 screened studies, complete literature or a duplicate systematic review.
One DOI has MED/PPR records; related studies/versions are not independent replications.

The 23-article XML attempt in `final-review-fulltexts-v2-20260908/` returned eleven usable
articles and twelve HTTP 404s, explicitly recorded. All eleven usable bodies pass the
tightened substantive-text validator. Browser/abstract reading depth remains explicit.

`source-verification-v5/` is the current 53-source identity/provenance run; older v4
verified 52 sources and must not be called the current source-ledger hash.
Full DOI/title and chemical-identity checks are separate from claim validity.

Independent review of `893dbd2` identified three standards/validation defects and one
specification omission (Haas 2019). Fixes bind analyte/form/mass to source metadata, reject
per-record invented margins, reject empty article bodies, and include the actual drug
combination trial. Both independent rechecks report all findings resolved; no new material
issue was identified in their bounded reviews. Final checks are in progress/adversarial notes.
Current suites: **63 evidence/package tests + 44 exposure/retrieval tests = 107**.

## Blockers and unresolved evidence

- **Delivery:** final recorded three-minute pitch, public playable URL, final owner review,
  live rule/disclosure and authenticated quota checks, and portal submission/receipt.
  Do not equate a script or locally verified bundle with an uploaded entry.
- **Science:** exact-allele effects, phase, current tumour/clinical context, pathway activity
  and a measured normal/tumour exposure window remain unknown. No wet-lab work performed.
  Literature review cannot establish these facts or authorize clinical treatment.
- **Track 1:** independently archive the existing receipt if supplied; do not upload again.
- No subject-file transfer, sample acquisition, treatment/procurement, family contact or
  extra AI provider is authorized. Preferred research/image skill services lack credentials;
  public sources/local tables were used instead.
- These scientific limits do not prevent an honest research proposal, but must not be
  concealed or presented as completed experiments.

## Resume and verify

```bash
./init.sh
uv run python scripts/track2_evidence.py check
uv run python scripts/test_track2_evidence.py
uv run python scripts/test_track2_review.py
uv run python scripts/track2_exposure.py
uv run python scripts/track2_evidence.py sensitivity
uv run python scripts/track2_evidence.py track1
```

Continue feat-009 only. The original `jvv7_track2_research_v1/` is preserved (seven file
hashes checked). `jvv7_track2_research_v2-review/` is the pre-independent-fix snapshot;
do not submit it. The final reviewed research bundle is
`results/feat009/jvv7_track2_research_v2/`; report SHA-256
`6685a1f25b7e8da6e69bab57bf5bdb855dce0e22095d80c9f1a02ea80d37ed72`.
Run `uv run python scripts/track2_evidence.py verify results/feat009/jvv7_track2_research_v2`.
V2 verification enforces ten files and current input hashes;
any later input change requires a new directory. Integrity is not clinical validity.

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
