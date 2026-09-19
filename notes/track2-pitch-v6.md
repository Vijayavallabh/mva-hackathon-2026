# Testing everolimus for tissue function in MVA

Participant jvv7, 2026-09-19. Research only; not a recorded video.
Trans phase remains unconfirmed. No efficacy or clinical exposure margin is established.

Use the [five-slide deck](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-slides-v6.html)
with this narration. The [report](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v6.md)
contains the evidence and full disclosure; the unchanged
[validation plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation-v5.md)
specifies the proposed tests. Slide 3 redraws published trial results. The other four
figures show objectives or proposed experiments, with no new experimental data.
All earlier pitch materials remain unchanged.

## Narration

### Slide 1 / 0:00-0:30 / The research question

Can everolimus improve tissue function in a BUB1B model of mosaic variegated aneuploidy?
BUB1B helps control chromosome segregation. Our selected variants provide a starting
point, but their phase and individual effects remain unresolved. We propose one
conditional experiment in non-cancer cells. Tumour control needs separate evidence.
We have performed no experiments.

### Slide 2 / 0:30-1:07 / Why test this pathway?

The clue comes from mouse muscle carrying different BubR1 alleles. One genotype
comparison showed increased phosphorylation of two mTORC1 targets. The study had
small blot groups, was not randomized or blinded, and did not test drug rescue.
First, establish whether excess mTORC1 activity exists in our model. Only then test
everolimus. Better function could reflect downstream mitigation; it would not by
itself establish chromosome repair.

### Slide 3 / 1:07-1:37 / What the trial limits

The tumour evidence warrants caution. In ARST1431, adding temsirolimus to chemotherapy
did not establish an event-free survival benefit among 297 evaluable participants.
The hazard ratio was 0.86, with a confidence interval spanning no difference.
That does not prove zero effect. It also does not test non-cancer everolimus rescue.
Each claim needs its own experiment.

### Slide 4 / 1:37-2:20 / What we would measure

Compare vehicle and everolimus in deficient and corrected models, including cis, trans,
single-allele and wild-type controls. Engineered phase cannot resolve the child's phase.
Randomize treatment, blind scoring, and prespecify a tissue-relevant function.
Follow every enrolled cell: record first division, errors, death, arrest and mitotic
slippage, then follow daughter survival separately. Report tracking loss.
Counting only survivors could make harmful treatment appear beneficial.

### Slide 5 / 2:20-3:00 / The decision

Advance preclinically only with functional benefit, acceptable deficient-normal safety,
justified exposure and replication across clones and days. Stop advancement if any
criterion fails or remains unresolved. Efficacy and clinical exposure margins remain
unknown. We disclose OpenAI, Google DeepMind and Fireworks-hosted GLM use; Fireworks
training and retention remain unverified. We thank the child, family and organizers.
This proposal requires authorized validation and makes no patient-dosing recommendation.

## Recording and timing

The narration has 297 whitespace-separated words: 51, 65, 54, 62 and 65 across the
five slides. That is 99 words per minute over three minutes, a planning estimate.
The slide timestamps are planned allocations, not measured runtime. Count only the
narration paragraphs, excluding headings, to estimate pace. Rehearse and measure the
complete recording with pauses and transitions against the three-minute requirement.

Open `track2-slides-v6.html` in a browser and navigate with the numbered links or
Tab/Enter. The canvas is 1280 by 720 (16:9); the PDF is an alternative for recording.
Render locally with:

```bash
uv run node scripts/render_track2_slides_v6.mjs NEW-OUTPUT-NAME
```

Use a new lowercase, hyphenated output name. Five PNGs, `track2-slides-v6.pdf` and
`render.json` are written below `results/feat009/`; existing directories are refused.
Check each slide at recording size. Keep the recording limited to the approved deck;
exclude credentials, protected data/narrative and unrelated windows. No runtime,
recording or hosted URL has been verified.

## Video description and acknowledgement

Testing everolimus for tissue function in MVA. A conditional preclinical proposal;
no demonstrated efficacy, confirmed trans phase or clinical exposure margin.

Report: https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v6.md

Code and provenance: https://github.com/Vijayavallabh/mva-hackathon-2026

AI assistance: OpenAI/Codex API tier, owner-attested no model training; Google DeepMind
AlphaGenome Atlas precomputed outputs and public downloads; Firecrawl self-hosted MCP
with Fireworks-hosted GLM, owner-confirmed API credits. Fireworks training/retention
remain unverified pending final disclosure confirmation. The report retains output
terms and separates source evidence from model proposals. Slide design and rendering
are local; no additional image-generation provider was used.

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.

## Before submission

- Confirm owner review and agreement between the report, narration and recording.
- Verify Fireworks training/retention settings; credit billing does not establish them.
- Measure runtime and check speech, slide legibility and acknowledgements.
- Host on YouTube/Vimeo and verify signed-out playback.
- Check live rules, authenticated identity/quota and public-repository/purge status.
- After authorized submission, archive the receipt, exact report hash and video URL.

Edits after bundling require a new snapshot. A script, deck or verified local package
is not a recording, upload or receipt.

## Panel questions

### Why everolimus?

It is the sole conditional research priority in the reviewed decision ledger. The
different-allele mouse finding motivates testing a pathway abnormality; it does not
demonstrate rescue. Without the abnormality, drug screening would not advance.

### Why leave other drugs out of the narration?

The report retains the full candidate assessment. HCQ remains reserve; pralatrexate
remains an optional fusion-positive RMS direction. Neither displaces this experiment.

### What would count as success?

Replicated, prespecified functional benefit with acceptable deficient-normal safety
and justified exposure would support further preclinical work. Pathway inhibition or
a smaller abnormal fraction among survivors would be insufficient.

### Does Track 1 establish a treatment?

No. The owner-reported leaderboard result cannot establish phase, allele function
or drug response. Receipt and uploaded-byte identity remain independently unverified.
