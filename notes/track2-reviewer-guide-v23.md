# Combined Track 2 reviewer guide: v23 research / v22 presentation

Start with the [v23 RNAi addendum](track2-rnai-v23.md) and its
[qualification changes](track2-rnai-validation-v23.md). The eight-GPU analysis probes
seed and batch alternatives across the complete curated public RNAi matrix, retains
HT29's favorable signal, and exposes finite-reference sensitivity. Its five claim
challenges supplement the v21 register; no drug disposition changes.

The [current record](track2-current.json) keeps versions separate:

- Presentation/report, transcript, methods workbook and recording ZIP: **v22**, frozen.
- Drug evidence, biological validation and original 27-claim register: **v21**.
- Original transcriptome campaign: **v19**, frozen and integrated into v22.
- Seed-aware RNAi research, five additional claim challenges and combined harness: **v23**.

```bash
uv run --no-project python scripts/check_track2_harness.py
```

This public CPU check validates all four components, the fixed negative findings,
favorable counterweights, exact result counts, missing controls, finite-reference
sensitivity and preserved no-promotion status. It uses no subject input, data/results
folder, credentials, network, GPU, model weight or Git history. A passing result is
internal consistency, not biological qualification or upload eligibility.

For narrower checks:

```bash
uv run --no-project python scripts/check_track2_rnai_v23.py
uv run --no-project python scripts/check_track2_transcriptome.py
uv run --no-project python scripts/track2_public_review_v22.py
```

The [v22 guide](track2-reviewer-guide-v22.md) retains exact export/snapshot commands.
The v23 addendum is not inserted into the frozen v22 PDFs or recording ZIP. Its
primary 161-file archive is separate; full reproduction and archive verification are
in [the v23 report](track2-rnai-v23.md). Large public matrices stay on the owner host
with recorded hashes. Original GCTX CPU spotchecks validate arithmetic, not an
independent scientific review.

[Owner readiness](track2-owner-readiness-v22.md) remains applicable: a script is not
a recorded pitch; provider/distribution questions, video/hosting, live portal checks
and receipt remain open. No wet-lab work, clinical exposure margin or treatment efficacy
is established. Never infer remaining quota or resubmit Track 1 to resolve its receipt.
