# Every enrolled cell: an offline research review kit

Open `notes/track2-demo-v37.html` in a browser, or run:

```bash
uv run --offline --no-project python scripts/track2_demo_v37.py
```

The command requires uv and an available Python 3.12+ interpreter, with no third-party
Python dependencies. The browser page is self-contained. No server, model weights,
GPU, API key or patient file is required. Links open public source pages only if you
choose to follow them. The demo itself sends no network requests.

## A two-minute walkthrough

1. Inspect the actual state: all biological measurements and margins are unresolved,
   so the decision is HOLD.
2. Compare the two invented 100-cell arms. A lower division-error percentage hides
   lower accurate viable output. Explore missing outcomes; the bounds are not
   sampling confidence intervals.
3. Select “Benefit with unacceptable recovery injury.” See why benefit cannot cancel
   injury. Then try “Nonsignificant injury is not proven safe” and “Drug and genetic
   deficit measured separately.”
4. Select the all-pass example. It permits preclinical review only. Download a case
   and inspect the exact assumptions, numbers and explanation.

## What the kit demonstrates

The fixed teaching set has 17 synthetic cases and the actual unmeasured state.
An intentionally incomplete benefit-only comparator advances 11 cases held or stopped
by the full policy; adding only viability still advances 9. This set was selected to
illustrate failure modes. It is not a held-out benchmark, a measure of diagnostic
accuracy, evidence of clinical safety or proof of superiority over other tools.
Python and JavaScript agree on 83 valid checks and reject 12 invalid records.

The original v21 decision policy is preserved. A case can be invalid, unresolved,
inconsistent with its tested branch, inconsistent with meaningful benefit, unsafe
for advancement, or ready for further preclinical review. The software validates
record shape and applies declared rules. It cannot establish that a user-supplied
assay, endpoint, interval, margin or gate declaration is scientifically justified.
Synthetic units and cutoffs must never be used in a real experiment.

From the full repository, build the compact ZIP with `uv run python scripts/track2_community_kit_v37.py build`.
It includes the page, cases, unchanged empty contract, Python policy/replay, this
guide and SHA-256 manifest. The full report and historical model outputs are not
dependencies of this small kit. From the full repository, verify it with the same script's `verify` command.
Inside an extracted kit, the Python replay and browser page work directly; the
packaging script is intentionally not a runtime dependency.

## Transfer and community contribution

Reusable: the schema, uncertainty states, audit trail, all-enrolled denominators,
explicit stop reasons and readable demonstration. Revalidate for a new context:
mechanism, model, tissue, functional endpoint, biological units, observation window,
exposure, benefit/injury margins and independent confirmation. Larger datasets do
not substitute for those steps.

The public repository and small kit lower the technical requirements for inspection.
They do not establish actual use, ease of use, community benefit or family endorsement.
No patient/family interviews or external usability study were performed. An authorized
future user study could measure whether researchers and patient advocates correctly
distinguish HOLD, invalid assays and scoped stopping decisions before and after
using the tool. No outreach is implied or performed.

The kit contains original project code and synthetic examples under CC BY 4.0,
with attribution to jvv7 and the repository. It does not contain AF3/Atlas outputs
or confer new rights to historical third-party materials. Distribution questions
for the full submission remain in [delivery readiness](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-owner-readiness-v37.md).

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.
