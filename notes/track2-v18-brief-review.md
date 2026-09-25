# Track 2 pitch framing against the official brief

25 September 2026. Owner-requested recheck of the challenge website after the visual
redesign and concise report edit. Anonymous retrieval; no login or portal actions.

The live Space remains at `aeeef5ad49f51204a7439352e59e9d310aee5e9e`. Overview, FAQ,
rules, Track 2 submission instructions, config and README match the September 24
source hashes. The live submission instruction component 40 matches the pinned source
after trimming. The complete runtime config hash differs, so only the checked component
is called an exact live/source match. Retrieval hashes and timestamps are in
`track2-v18-brief-audit.json`; public cache is `results/feat009/v18-brief-review-20260925/`.
Foreign source was parsed/read, not executed. Web-tool failures are not evidence of
missing pages: anonymous direct GETs returned HTTP 200. Discussions were not re-enumerated;
the complete September 24 review remains separately dated.

## What the panel is evaluating

The task is to nominate an existing approved medicine for investigation, connect it to
the disrupted biology, and explain the reasoning in a three-minute video. Completed
efficacy is not required. The rubric weighs mechanism/candidate support at 35%, potential
contribution to MVA understanding if validated at 25%, a creative method/angle at 25%,
and realistic transfer beyond this case at 15%. These are judging criteria, not scores
assigned to our entry.

Sources: [official overview](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/about.py),
[submission instructions](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/submit_track2.py),
[FAQ](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/faq.py).

## Resulting pitch

| Slides | What judges can assess |
|---|---|
| 1 | Everolimus is the explicit approved-drug proposal, qualified for investigation. |
| 2 | BUB1B/BUBR1 biology, unknown allele effects/phase and the two conditional downstream branches. |
| 3 | Candidate rationale and contrary evidence in original contexts; HCQ remains reserve. |
| 4 | The concrete qualification, blinded probe and independent confirmation plan. |
| 5 | The methodological contribution: measuring every enrolled cell to avoid false rescue. |
| 6 | Benefit, safety and exposure rules that make the proposal falsifiable. |
| 7 | Conditional impact, realistic reuse and the next experiment. |
| 8 | Full required acknowledgement. |

The 334-word narration leads with the repurposing proposal. The redesigned visuals
support the candidate/mechanism argument; software-audit details stay in the report
and reviewer guide. No candidate is promoted to rescue priority, and no biological
measurement, clinical efficacy or predicted judging score is added.
