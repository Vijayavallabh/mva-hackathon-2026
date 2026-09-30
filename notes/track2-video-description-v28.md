# Track 2 v28: video description

Testing everolimus for useful cell function in BUB1B-associated MVA. An approved-drug
research hypothesis with model qualification, direct functional testing and explicit
stopping rules. Everolimus remains an optional probe; no rescue-priority drug is supported.

Participant: jvv7. This file accompanies the nine-slide deck and 330-word narration.
The three-minute schedule is a rehearsal plan; no recording, hosting or measured
runtime is established.

Report: https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v28.md

## Sources and review

- [Protein backgrounds, HT29 robustness and weaker MCF7 reversal](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-v27.md)
- [Five additional protein/specificity challenges](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-register-v27.json)

- [Falsification review and 27-claim register](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-review-v21.md)
- [Complete public expression results](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-transcriptome-v19.md)
- [RNAi seed controls, HT29 counterweight and finite-reference sensitivity](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-rnai-v23.md)
- [New CRISPR findings, one-guide limits and source-well continuity](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-crispr-v25.md)
- [Five additional CRISPR claim challenges](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-crispr-register-v25.json)
- [Five additional RNAi claim challenges](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-rnai-register-v23.json)
- [RAPA-EX-01 primary human trial](https://doi.org/10.1002/jcsm.70274)
- [Young-rat muscle study](https://doi.org/10.1371/journal.pone.0312859)
- [PoWeR female-mouse study](https://doi.org/10.1111/acel.70183)
- [Validation plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation-v21.md)

HT29 retains retrieval ranks 2–5 under stronger sensitivity tests, with one-guide and
QC limits. MCF7 BUB1B reversal falls from rank 7 to 1,184; MTOR stays first. Different cells do not establish a
joint rescue result; reaggregated wells do not establish independent replication.
The human/animal findings are indirect for everolimus in MVA. Invalid assays and
imprecise results cannot establish biological failure or safety. Subject phase and
clinical exposure margins remain unknown. Tumour killing and non-cancer rescue need
separate tests. The report contains additional primary sources and limitations.

## AI provider, plan and handling

OpenAI Codex/API was used for code, literature
research, synthesis, editorial work and agent reviews. The owner attests no training on
content; this is not an independent account or zero-retention audit. Firecrawl's local
bridge previously used Fireworks-hosted GLM on owner-confirmed API credits for public
literature; training/retention settings remain unverified. Local retrieval is not proof
of local inference. Google DeepMind AlphaGenome Atlas supplied precomputed API/download
outputs, not on-demand inference; its output/service terms remain applicable. Owner-hosted
research used ESM-1v/ESM-2, ESMC 300M/600M/6B, ESM3-open 1.4B, Boltz-2, AlphaFold2,
AlphaFold3, ESMFold2 and Evo2 7B/20B/40B with public references and permitted derived
substitutions. Earlier ColabFold alignment search received only public wild-type protein;
service training/retention policies remain unverified. The public LINCS, RNAi and CRISPR campaigns used all eight owner-host H100s for statistical reanalysis,
not new neural-model inference, with brief, bursty kernels. Only public NIH/Broad data and
code were transferred under the owner's `~/v` folder. The v21 research used public literature searches and local decision-logic checks.
The v23 follow-up used public RNAi/CRISPR matrices, CUDA statistics and local numerical
checks. The v25 follow-up used public LINCS2020 CRISPR and compound matrices,
source-well audits and original-coordinate numerical checks. The v27 follow-up added
local ESMC/ESM3 protein inference and expression sensitivity analyses on all eight H100s.
The Anthropic uplifting-biomolecular-modeling toolkit was reviewed at pinned revision
`f4f62fa6592ae4938d49b1757bea0cfeff9f468e` through five documents; it was not installed
or executed. Established local FP32 runtimes were retained. No new hosted provider was
added. This v28 integration used local editing and offline rendering, with no additional
neural inference or repeat of the September 24 full requirements/community audit. Raw subject reads, VCF records and clinical
narrative stay local. Unknown settings are not silently attested. Historical AF3-derived
materials retain [AlphaFold3 Output Terms](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphafold3-output-terms.md), the
[Legally Binding Terms of Use notice](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphafold3-Legally-Binding-Terms-of-Use.txt),
modifications disclosure and [Abramson citation](https://doi.org/10.1038/s41586-024-07487-w).

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.
