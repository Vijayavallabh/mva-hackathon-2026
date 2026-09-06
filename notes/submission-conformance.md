# Track 1 local scorer and submission conformance

## Outcome

Feat-006 is complete. The organizers' public `evaluation.py` is vendored byte-for-byte at
Hugging Face Space revision `1c761cc23d90aebe6a011fd5b0b99517df42408c` with SHA-256
`6d18b581e65a45e1ccc120071d588e740c2e42e983ff50704c60a40232b19180`.
The official CSV template from the same revision is tracked with normalized LF line endings;
its fields and example rows are unchanged.

The local draft contains ten distinct compound-pair hypotheses from the completed feat-004
ranking. It passes the exact official schema plus stricter submission-readiness checks:

- `proband_id` is exactly `PROBAND01` on every row.
- Every chromosome is `chr`-prefixed even though the local VCF/reference are unprefixed.
- There are exactly ten rows, no duplicate hypothesis, and ten finite, strictly distinct
  EPCR values in descending file order.
- Both alleles of each pair are complete, uppercase, non-identical DNA alleles.
- All 20 alleles agree with the exact local GRCh38 reference and remain unchanged after
  `bcftools norm`; indels are therefore minimal and left-aligned in the submitted form.
- The unmodified official loader accepts the draft and the official scoring function runs.

The draft EPCR sequence (0.95 down to 0.50) is a deterministic rank-preserving placeholder,
not a calibrated probability model. Absolute EPCR magnitudes do not change rank points and,
provided values remain distinct and ordered, do not change which prediction sets the F-max
sweep evaluates. Calibration should be revisited with the final biological ranking.

## Reproduce

```bash
uv run python scripts/track1_submission.py --self-check
uv run python scripts/track1_submission.py build
uv run python scripts/track1_submission.py check
```

The build writes `results/feat006/track1_candidate.csv`; the check writes
`results/feat006/track1_candidate.check.json`. Both stay local under the gitignored results
tree. The JSON report records SHA-256 values for both the exact checked CSV and the vendored
scorer, so a later CSV edit cannot be mistaken for the file that passed. The self-check
also verifies the pinned scorer and tracked template checksums, valid construction, exact
official score behavior, full and
partial-match rank points, and rejection of a wrong proband ID, unprefixed contig, duplicate
EPCR, incomplete second allele, eleven rows, and a non-left-aligned indel.

## What the local score means

The real draft was scored under the explicit hypothetical assumption that submitted row 1
is the causal pair. Under that assumption the official scorer returns rank points 100,
F-max 1.0 at EPCR 0.95, and one prediction row at the maximizing threshold. This is the
expected plumbing test for a correctly placed exact answer.

The private answer key was not downloaded or inferred by this step. Consequently this is
not a true challenge score and is not biological confirmation. In particular, the leading
BUB1B pair is still supported only as an unphased compound-heterozygous hypothesis; trans
phase remains unconfirmed. No Track 1 submission has been spent.

Feat-008 packages this checked ranking with a revision-bound report and a hash manifest;
see `notes/track1-submission.md`. Offline validity alone is insufficient for upload: owner
AI-account disclosures, local visibility policy and authenticated portal quota must also
be resolved. No official competition score is represented by the hypothetical test.

## Pinned public provenance

- Space: `SageBio/rare-disease-real-kid-mva-hackathon-2026`
- Revision resolved with:
  `git ls-remote https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026.git HEAD`
- Vendored scorer source path: `evaluation.py`
- Vendored template source path: `static/templates/track1_submission_template.csv`

The wrapper deliberately does not modify the scorer. Local safety rules live in
`scripts/track1_submission.py`, keeping upstream behavior auditable separately from our
stricter readiness policy.
