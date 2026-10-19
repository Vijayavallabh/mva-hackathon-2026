# Remaining work that could improve the Track 2 entry

19 October 2026. Review addendum only: the presentation and release remain v37.
This is an author/agent assessment, not independent review, a judge score or an
estimated probability of winning. The owner asked whether useful work was exhausted.
It is not. Software correctness and a complete research package do not establish
competitive strength.

## What the evidence supports

The submission has a traceable scientific record, explicit counterevidence, a
conditional experimental proposal and a working offline demonstration. Its largest
scientific weakness remains the indirect link from the retained variants to the
proposed drug. Its innovation and community-use claims have not been tested with
unfamiliar users or compared systematically with existing methods.

The official rubric allocates 35% to rigor, 25% to potential impact, 25% to innovation
and 15% to scalability. Impact includes what independent validation could contribute
to MVA understanding or diagnosis. The separate Innovation Prize can recognize
creativity, community impact or patient-centered design; actual adoption is not a
stated prerequisite. Four official files were freshly retrieved and remain identical
to v37. [Overview](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/60e1c30e337ce6fe01813040dbe49979eb8c50aa/tabs/about.py),
[rules](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/60e1c30e337ce6fe01813040dbe49979eb8c50aa/tabs/rules.py).

## Priority order

| Priority | Remaining weakness | Concrete work and completion evidence |
|---|---|---|
| 1. Submission access | A required recorded/hosted pitch is still absent; provider/distribution and live-delivery questions remain. | Record in the owner's voice, measure the export, verify access and exact files, resolve the existing questions and retain the actual receipt. A rehearsal or script cannot satisfy these steps. |
| 2. Drug rationale | Being a testable probe does not establish that everolimus is the strongest therapeutic candidate. The current favorable mechanistic bridge is indirect. | Challenge everolimus against the NAD/SIRT2 route and mechanism qualification before drug testing under the same evidence requirements. Obtain an outside critique of the first qualification experiment. Change priority if stronger evidence warrants it. See the [comparison](track2-candidate-comparison-v38.md). |
| 3. Innovation | Reusable rules, rejection gates and CPU-only execution are not sufficient evidence of novelty. | Compare specific capabilities with existing public methods; identify what our implementation adds and what it does not. Document the result without a superiority claim unsupported by a fair comparison. |
| 4. Reviewer comprehension | The deck is visually readable, but comprehension within three minutes is unmeasured. Slides 5 and 6 carry substantial technical detail. | Have an unfamiliar reader summarize the proposal after one timed viewing. Check the drug, hypothesis, observed result, synthetic example and next experiment. Revise the pitch based on actual misunderstandings. |
| 5. Demonstrated reuse | An isolated replay establishes portability; it does not establish ease of use or transfer to another biological setting. | Have an unfamiliar person open the demo and explain HOLD, injury and all-pass outcomes without coaching. A second public case would need a fixed scope and separately adjudicated applicability; do not relabel selected examples as held-out validation. |

The order is an assessment of practical value before the deadline, not an estimated
increase in award probability. More GPU inference is justified only if a specific
result could change the biological decision and the required controls are available.

## A concrete challenge to the novelty argument

Another public Track 2 project describes a reusable pipeline with direction checks,
rejection rules and controls. Its README alone shows that these broad ideas are
already present in the field. We inspected its methods description, not its patient
case, full report or executable behavior. Its reported performance and registration
timing were not independently verified. This is evidence against a broad novelty
claim, not evidence that its submission is better than ours.
[Public methods README, pinned revision](https://github.com/swoopeagle/mva-hackathon-methods/blob/c21dd5a79cbb59959fbb6b6ea420375fe799649c/README.md).

Our more specific contribution is the integration of audited BUB1B evidence,
all-enrolled outcome accounting, missingness, separate invalid/unknown/injury states,
and a staged joint-intervention proposal. These component methods are established.
Their usefulness and distinctiveness still need assessment; calling them a unique
platform or a clinically validated decision system would be unsupported.

The current 17 synthetic cases were selected to illustrate failure modes. The
benefit-only and benefit-plus-viability comparators are intentionally incomplete.
Their failures are educational examples, not a fair contest against another complete
tool. A larger number of such cases would not by itself fix that limitation.

## Presentation review

All nine final PNGs were reviewed in sequence; the PDF was not used as a substitute
for visual inspection. The existing render audit counts 707 visible words including
headings, sources and acknowledgement. The narration has 368 words. Neither count
measures what a reviewer can understand during the allotted video.

- Slides 1–3 state a conditional drug experiment, but introduce the drug, variant
  mechanism, two branches and several technical prerequisites quickly. The second
  branch may distract from the first qualification question; test this with a viewer.
- Slide 4 makes the denominator problem concrete. Preserve its synthetic label.
- Slides 5 and 6 contain 92 and 97 visible words, allocated 19 and 20 seconds. Model
  names, retrieval metrics, biological controls and clinical counterevidence compete
  for attention. Prioritize the decision each finding changes; the report can retain
  full numerical detail. This is a comprehension concern, not a measured failure.
- Slides 7 and 8 explain the tool and transfer, but do not demonstrate external use.
- Slide 9 preserves the required acknowledgement. Any shortened pitch must preserve
  attribution and the distinction between a proposed experiment and observed efficacy.

A scientifically sound negative result can be valuable. It still needs a clear
explanation of what another researcher can now do differently. A long inventory of
failed models cannot substitute for that explanation or for the drug rationale.

## Outside review and owner preparation

The owner says they can arrange a reviewer and identifies as a bioengineering
undergraduate. Their technical review and presentation are valuable contributions;
review by the entry's author is not independent. A faculty mentor or researcher with
relevant chromosome-biology, experimental-pharmacology or cell-assay expertise can
review a bounded part of the proposal and state the limits of that expertise. A
clinical review would separately address translational assumptions. Neither type
of feedback is biological validation or family endorsement.

The [review packet](track2-external-review-packet-v38.md) is ready for the owner to
share. No reviewer has been contacted, no feedback received and no endorsement
claimed. The packet includes a separate self-rehearsal checklist for the owner.

## Sources, commands and preservation

Fresh anonymous source receipts and the public comparator README are retained in
`results/feat009/competitive-reassessment-20261019/`. The official HTML parser in the
web tool could not retrieve several pages; direct anonymous HTTP requests returned
200 and matched the stored v37 hashes. No new discussion census is claimed.

Bounded searches covered BUB1B/Asn1002Lys, BubR1/SIRT2/NAD, the primary mouse paper,
and public MVA Track 2 methods. These are not an exhaustive novelty or literature
review. The JCI article was accessible; several PMC/PubMed full-page requests were
blocked or incomplete. Indexed primary abstracts and the existing adjudications
were used with those limits. Another participant's causal probability was not used
as evidence. No private competitor material was accessed, and competitor code was
not executed. No protected subject data was sent to a search or external service.

Reproduce the local word counts from `notes/track2-v37-render-audit.json` and review
`results/feat009/v37-slides-final-b-20261019/slide-1.png` through `slide-9.png`.
Verify the preserved release with:

```bash
uv run --no-project python scripts/track2_release_v37.py verify results/feat009/jvv7_track2_research_v37
uv run --no-project python scripts/check_track2_harness.py
```

No drug ranking, exposure margin, phase, biological-validation flag or v37 bound
input changes in this addendum. These findings identify remaining work; they do not
establish that it has already been completed.
