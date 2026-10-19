# Work directed at the Track 2 rubric

19 October 2026. Feat-009 only. Author assessment, not a judge score or estimated
chance of winning. V36 and earlier bound inputs remain immutable.

The official overview asks whether the variant mechanism supports the drug (35%),
what independent validation could contribute to MVA understanding or diagnosis
(25%), whether the method/tool is creative (25%), and whether it can realistically
transfer to other people, diseases or datasets (15%). The separate Innovation Prize
recognizes creativity, community impact or patient-centered design independently of
placement. There is no live Q&A: the report, repository and three-minute video must
answer foreseeable objections themselves.

Sources: [overview](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/60e1c30e337ce6fe01813040dbe49979eb8c50aa/tabs/about.py),
[rules](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/60e1c30e337ce6fe01813040dbe49979eb8c50aa/tabs/rules.py),
[announcement 28](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/28).

## Priority and acceptance criteria

| Criterion | Main weakness in v36 | Work and acceptance criterion |
|---|---|---|
| Rigor | Many controls, but the pair-to-drug link remains indirect and the two pathway branches compete for attention. | Make the evidence chain explicit; choose excess mTOR-associated activity with impaired function as the first qualification question. Retain flux as a separately locked alternative, never a post-hoc explanation. Preserve all negative and favorable controls. |
| Potential impact | A long account of failed models obscures what a positive or negative biological result would add. | Give a staged laboratory handoff, concrete functional readouts, stop conditions and the information each stage provides. Separate diagnostic research utility from treatment efficacy. State patient-burden assumptions and absent family co-design. |
| Innovation | The decision contract is executable but difficult for a non-programmer to inspect. | Build a self-contained interactive research review demo with the actual unknown state, explicit synthetic examples, inspectable reasons and downloadable records. Compare defined shortcuts on a deliberately selected teaching set, without claiming clinical validation or general superiority. |
| Scalability | Review is CPU-only, but a reviewer must navigate many files and historic versions. | Supply a small offline kit, one-command replay, a schema and a transfer checklist. Measure the local replay time/size and distinguish those observations from biological cost or cross-disease validity. |
| Innovation Prize | Patient-centered intent is described, but practical design choices are hard to see. | Demonstrate all-enrolled outcomes, injury overriding benefit, accessible plain-language explanations and no patient-data requirement for the demo. Include an honest community-use plan with no invented users or endorsements. |
| Delivery | The required video and several owner/provider questions remain open. | Produce a polished nine-slide deck, concise narration, recording guide and a judge navigation page. Keep video/hosting/receipt fields unknown until real evidence exists. |

## Boundaries and falsification

No new model run is justified merely by compute availability. The completed eight-H100
campaign already found that neural imaging models miss the required gain. Preserve
the favorable simple BUB1B signal and its method/plate sensitivity. The next causal
drug evidence requires joint intervention in a qualified biological model.

The demo's numerical values are invented teaching fixtures. Its margins must never
be copied into an experiment or interpreted as clinical cutoffs. Expected decisions
are author-specified before replay; matching them proves implementation behavior,
not the scientific correctness of the policy. Shortcut comparisons use the same
fixtures and are deliberately incomplete, not competitive clinical products.

Do not claim new biological efficacy, calibrated diagnostic classification, family
consultation, external adoption, specialist review, laboratory readiness or award
likelihood. No family/organizer contact, upload, system installation or agreement
acceptance is part of this work. Preserve the unconfirmed phase, null clinical
exposure margins, optional everolimus probe and HCQ reserve.

## Design direction

The demo opens with the actual unresolved research decision, followed by a two-arm
cell-outcome diagram and selectable teaching cases. Use ice #f2f7f8, ink #142c3c,
deep teal #123a40, mint #d8eee5, iris #48419d and rust #8a392a. Ubuntu/system sans
supports offline reading. A large cell-outcome comparison is the visual focus;
avoid dashboard cards, decorative gradients and score-like claims of efficacy.
Use visible keyboard focus, native controls, text plus color, responsive layout,
no automatic animation and no external assets, analytics or network requests.

The scientific-slides/frontend-design skills guide rendering and visual review;
scientific-critical-thinking, humanizer and no-ai-slop guide the argument and prose.
