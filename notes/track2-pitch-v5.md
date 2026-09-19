# Track 2: three-minute pitch

Participant jvv7, 2026-09-19. Research only; not a recorded video.
Trans phase remains unconfirmed. No efficacy or clinical exposure margin is established.

Use the [five-slide deck source](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-slides-v5.html) with the narration below; open the supplied HTML locally for presentation.
The [report](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v5.md) contains the evidence and full disclosure;
the [validation supplement](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation-v5.md) specifies the proposed tests.
The editable HTML and locally exported PDF contain conceptual figures, not experimental
results. Earlier pitch materials remain unchanged.

## Narration

### Slide 1 / 0:00-0:30 / Protect normal tissue

A cancer drug can kill a tumour while harming non-cancer cells that share its genetic
vulnerability. Our proposal tests both effects together. BUB1B is the genetic starting
point, but trans phase remains unconfirmed. We have not performed experiments or
demonstrated a treatment benefit. The drawings show what we propose to test.

### Slide 2 / 0:30-1:05 / Test the conditional lead

BUB1B encodes BUBR1, which helps control chromosome attachment and separation.
Everolimus merits testing only if a qualified model shows excessive mTORC1 activity.
The motivating mouse study used different alleles and did not test drug rescue.
In a randomized rhabdomyosarcoma trial, adding the related drug temsirolimus did not
demonstrate an event-free survival benefit. We are proposing a test of downstream
function; chromosome repair and cancer benefit remain unproven.

### Slide 3 / 1:05-1:35 / Separate the candidate branches

Hydroxychloroquine stays in reserve. Pralatrexate is a separate possibility for verified
fusion-positive rhabdomyosarcoma models, where recurrence and schedule-dependent
toxicity limit encouraging regression results. Other candidates face disputed mechanisms,
tissue-specific harm or unmatched exposure. Entinostat has a Chinese breast-cancer
approval, but no pediatric rhabdomyosarcoma indication. The report retains rejected
alternatives and checks model summaries against primary sources.

### Slide 4 / 1:35-2:15 / Follow every fate

Counting only survivors can make a harmful drug look helpful. We would enroll cells
before treatment and record accurate division, division errors, death, mitotic slippage
and no division, with tracking losses reported separately. We would then follow
daughter survival and tissue function. A lower fraction of abnormal surviving cells
cannot establish rescue. These branches describe proposed measurements, with no
assumed frequency or drug effect.

### Slide 5 / 2:15-3:00 / Run controlled validation

Start with independently engineered controls, including cis, trans and genetic correction.
Engineered phase does not resolve the child's phase. Qualify the defect and exposure,
randomize treatments, blind scoring and replicate across clones and days. Stop for
unacceptable normal-cell injury, unjustified exposure or benefit that fails to reproduce.
Efficacy and clinical exposure margins remain unknown; AlphaGenome predictions cannot
settle them. We disclose OpenAI, Google DeepMind and Fireworks-hosted GLM use.
Fireworks API credits are confirmed; training and retention settings remain unverified.
We thank the child, family and organizers. The next scientific step requires authorized
experimental validation. We propose no patient dosing.

## Recording and timing

The narration has 337 whitespace-separated words, or about 112.3 words per minute
over three minutes. This is a planning estimate. The slide timestamps are planned
allocations, not a measured performance. Count only
the narration paragraphs, excluding headings, to estimate pace. Rehearse at least three
times and measure the recording, including pauses and transitions. The full run must
fit the competition's three-minute requirement. Shorten wording if needed while
retaining the scientific limits and provider disclosure.

Open `track2-slides-v5.html` in a browser, use full-screen mode, and navigate with the
numbered links or Tab/Enter. The canvas is 1280 by 720 (16:9); small browser windows
scale the view. The PDF export is a convenient alternative for recording, not a video.
Render locally with:

```bash
node scripts/render_track2_slides_v5.mjs NEW-OUTPUT-NAME
```

Use a new lowercase, hyphenated output name. The renderer writes five PNG previews,
`track2-slides-v5.pdf` and `render.json` below `results/feat009/`. It refuses to overwrite
an existing directory. Check every slide at the intended recording size. Use only the
approved deck on screen; exclude terminals, credentials, raw data, protected narrative
and unrelated windows. No runtime, recording or hosted URL has been verified.

## Suggested video description

Research proposal by jvv7 for Rare Disease, Real Kid: The MVA Hackathon 2026.
No experiments performed or treatment recommended. Trans phase remains unconfirmed;
clinical efficacy and exposure margins are unestablished.

Report: https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v5.md

Code and provenance: https://github.com/Vijayavallabh/mva-hackathon-2026

AI assistance: OpenAI/Codex API tier, owner-attested no model training; Google DeepMind
AlphaGenome Atlas precomputed outputs and public downloads; Firecrawl self-hosted MCP
with Fireworks-hosted GLM, owner-confirmed API credits. Fireworks training/retention
remain unverified pending final disclosure confirmation. See the report for output
terms and the distinction between source evidence and model-generated proposals.
Slide design uses local SVG and browser rendering; no additional image-generation
provider was used.

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.

## Before submission

- Confirm that the report, narration and final recording agree. Any edits need a new snapshot.
- Verify Fireworks training/retention settings; credit billing does not establish them.
- Check actual runtime, speech clarity, slide legibility and acknowledgements.
- Host on YouTube/Vimeo and test playback in a signed-out browser.
- Check live rules, authenticated identity/quota and the final report filename.
- After authorized submission, archive the receipt, exact report hash and video URL.

## Panel questions

### Why everolimus despite negative tumour evidence?

The proposed test concerns a measured downstream functional abnormality. ARST1431 did
not demonstrate an event-free survival benefit from adding temsirolimus. Without the proposed pathway abnormality, or with
unacceptable injury to deficient-normal cells, this experiment would not advance.

### Why keep a short candidate list?

Additional drug names do not supply matched exposure or safety evidence. The decision
ledger records the alternatives and what evidence would justify reconsidering them.

### What does this proposal contribute?

It combines genotype-aware models, normal-cell protection and complete cell-fate
accounting in a testable design. It does not claim discovery of mTOR biology or a cure.

### Does the Track 1 score validate a treatment?

No. The owner-reported 100 rank points and F-max 1 do not establish phase, allele
function or response to any drug. The uploaded-byte receipt is not independently verified.

### Can a research proposal be submitted without wet-lab results?

It can describe the evidence and proposed tests honestly. Advancing toward treatment
requires experimental evidence and approvals that this project does not have.
