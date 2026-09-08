# Track 1 submission preparation (feat-008)

Status on 2026-09-08: owner AI disclosure completed; v4 rebuild pending. No submission has been uploaded
by this workflow and no official score or remaining-attempt count is claimed.
The selected account from the local authenticated HF identity is `jvv7`; an empty
display name uses that username. Never print the token or complete identity response.

## Contract correction and unresolved owner decisions

The [official upload source](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/1c761cc23d90aebe6a011fd5b0b99517df42408c/tabs/submit_track1.py)
requires CSV, report (`.md` or `.pdf`) and a GitHub URL. It permits private repositories
during the competition, with public visibility required when the competition ends.
The earlier inference that the portal requires public visibility immediately was wrong.
The owner's stricter public-first policy remains active in AGENTS.md and the package
configuration until explicitly changed. Neither publication nor sharing retired objects
is safe while GitHub still serves those objects. The prepared Support request is unsent.

The official AI-use instructions require provider, plan/tier and data-handling setting.
The owner confirmed OpenAI/Codex **API tier** on 2026-09-06 and, on 2026-09-08,
confirmed that data is not used to train the provider's models and no other AI providers
were used. These owner attestations complete `notes/track1-submission-config.json`.
They are not independently verified account settings and do not imply zero retention,
a retention duration, or permission to transmit prohibited subject data.

Verified public source revision: `1c761cc23d90aebe6a011fd5b0b99517df42408c`.
Upload source SHA-256: `685a3b6d57ef3a1c49a8be47845b10d77cb576ed2d30b5a90879b09707659b86`.
The live preflight checks both the Space HEAD and this upload-code hash, failing closed
on changed/unavailable rules. It never downloads private ground truth.

## Reproducible local package

```bash
uv run python scripts/prepare_track1_package.py --self-check
uv run python scripts/track1_submission.py --self-check
# Commit reviewed code, template and config first; build requires a clean tree.
uv run python scripts/prepare_track1_package.py build --name jvv7_genomewide_mva_v3
uv run python scripts/prepare_track1_package.py verify results/feat008/jvv7_genomewide_mva_v3
uv run python scripts/test_track1_package.py results/feat008/jvv7_genomewide_mva_v3
# Push the reviewed commits before this live check:
uv run python scripts/prepare_track1_package.py preflight results/feat008/jvv7_genomewide_mva_v3
```

Build refuses to overwrite an existing package. Changed evidence, code or disclosure
requires a reviewed commit and a new package name. The manifest hashes the CSV, report,
local-check JSON, relevant source files and local evidence inputs. Verification repeats
the exact schema, identity, ranking and reference-normalization checks, regenerates the
report against the CSV/config, verifies committed source provenance and scans both
deliverables for prohibited content without printing matching source text.

The ten pairs preserve the reviewed baseline: one pair per gene, BUB1B first, with
lower-ranked alternatives explicitly weaker. No trans phase is asserted. The report
explains HPO/family separation, methods, targeted recall, CN/BAF screening limitations,
uncalibrated EPCRs and the ClinVar population-frequency caveat. The local 100 rank points
and 1.0 F-max use assumed row-1 truth, not the private answer key.

## Actual upload procedure — not yet executed

1. Resolve the owner disclosure fields and public-first policy. If it stays public-first,
   finish feat-007's remote purge and publication gates before uploading.
2. Commit configuration/report changes, create a new package, verify, push and run a
   fresh live preflight. Use only the exact CSV/report named in its manifest.
3. In the authenticated official portal, confirm identity `jvv7`, current quota and
   remaining attempts. No local score test consumes a submission; the real upload does.
4. Submit the paired files and configured GitHub URL once. Do not retry blindly after
   a timeout: inspect authenticated submission history first to avoid spending two slots.
5. Preserve the returned submission identifier, timestamp, official scores and quota in
   a local receipt; hash the submitted files again. Record only permitted derived facts
   in tracked notes. Do not claim success without a receipt/history confirmation.
6. Mark feat-008 done only after successful upload and receipt verification. Changing
   either deliverable after upload requires an explicit task from the owner.

The script intentionally does not automate uploads or pretend that live quota is known.
It can produce an offline-valid draft while required owner inputs remain unresolved;
such a draft is **not submission-ready**.

## Review corrections

The first local package (`v1`) is superseded, not an uploaded deliverable. Independent
specification and standards review identified a stale-upstream check, an upload-policy
dependency in the public-repository purge check, and imprecise missing-AF wording.
The revised preflight queries the actual configured origin branch and always requires
the purge gate when visibility is PUBLIC. Unknown visibility fails closed. Tests cover
18 policy/visibility/purge combinations, a moved remote despite matching cached refs,
an unavailable remote, and payload/manifest corruption. Named evidence paths replaced
positional dependencies. The report now states the actual +1 default for missing AF.

## Historical v2 result and live blocker

Package: `results/feat008/jvv7_genomewide_mva_v2/`, built at code revision
`c5bc2e0` (full SHA in its manifest). The CSV contains 10 ranked pairs and 20 alleles
that pass exact reference normalization. SHA-256:

- CSV: `a1f9315e223a07914589ce6884a66702b80e587ec5b7ad67f2ca1213f6caa225`
- Report: `e4df63305f7cdb3e3e6deb97a8366f859e6a08fa0dc58caefe0c33eb27d7a98f`

The live preflight run after pushing returned exit 1, with the three missing disclosure
fields and failed remote purge as blockers. The official contract and live origin checks
passed. **Unexpectedly, GitHub reported PUBLIC**, confirmed by a separate query at about
17:44 UTC on 2026-09-06; all 13 retired blobs remained retrievable with zero unknown
errors and a successful control. This session performed no visibility change. The owner
was asked to authorize restoration to PRIVATE. The object checker did not print blob
contents, and no submission was attempted.

### Standards review

The independent review found a conditional purge-gate violation and a low-priority
positional-evidence naming issue. Both were corrected in `c5bc2e0`; re-review identified
no residual standards violations or material heuristic findings.

### Specification review

The independent review found stale cached-upstream verification, conditional publication
safety and inaccurate missing-AF wording. All three were corrected in `c5bc2e0`;
re-review identified no residual specification issues. The actual upload and owner
inputs remain explicitly unfinished.

Review totals: Standards 2 findings resolved; Specification 3 findings resolved (the
purge issue appears in both axes). No remaining finding in either reviewed axis.

## Owner clarification (2026-09-06)

The owner confirmed that they deliberately made the repository public and that Codex
uses API tier. The configuration records the tier verbatim in meaning; it does not infer
account-specific retention, training or data-sharing settings. Two disclosure fields
remain unresolved: `ai_data_handling_setting` and `other_ai_providers`.

The PUBLIC state is therefore explained, not an unexplained repository change. It does
not establish that GitHub purged the retired objects or clear the confidentiality gate.
The most recent remote check still found all 13 retrievable. No visibility change or
upload is performed in response to this clarification.

The v2 package above is a historical validated draft bound to the previous configuration.
Its hashes remain unchanged, but verification against the updated configuration must
reject it. A refreshed v3 draft is documented below. After completing the remaining
disclosure, commit the configuration and build a new package name (next: v4); never edit
the old deliverables in place.

## Historical v3 draft (2026-09-06)

Built `results/feat008/jvv7_genomewide_mva_v3/` from `cdfb444` with the owner-confirmed
API-tier disclosure. This refresh changes the report, not the ranked candidates or
scientific interpretation. Trans phase remains unconfirmed. The CSV SHA-256 is unchanged:
`a1f9315e223a07914589ce6884a66702b80e587ec5b7ad67f2ca1213f6caa225`.
The report SHA-256 is
`eb836b42dc8b10c3dc010384edd124bd8e3c02a738a9106e097c887de42d421f`.

Build, offline verification and package regression pass: 10 pairs, 20 normalized alleles,
18 publication-policy cases, three live-upstream cases, portable copying and nine
corruption rejections. The real preflight exits 1 with exactly these blockers:

- API account data-handling disclosure remains unconfirmed.
- Other AI providers used remain unconfirmed.
- The independent retired-object purge gate still fails.

The live repository is PUBLIC; the pinned official upload contract and origin
synchronization checks pass. No submission was attempted, quota remains unqueried, and
there is no official score or receipt. Repeatedly rebuilding an unchanged draft cannot
resolve these blockers: the next material work requires the missing owner disclosures
and resolution of the retained-object exposure. The request to ignore that gate was not
implemented because it conflicts with the non-negotiable data-access rules.
