# Track 2 public literature addendum, version 43

20 October 2026. This addendum reports a targeted contrary-evidence search across
PubMed and OpenAlex, not a new exhaustive systematic review. It reads one
open-access full text and the PubMed record for the highest-impact paper found.
No protected subject data was accessed, and this search does not change any drug
disposition. Everolimus remains a mechanistic probe on HOLD; HCQ remains reserve;
no NAD/SIRT2 intervention is promoted; no clinical exposure margin, no rescue
priority and no phase result is established.

## Searches

The PubMed search combined mTOR/rapamycin/everolimus/sirolimus terms with
BUB1B/BUBR1/spindle checkpoint/aneuploidy and date limits 2020-2026. It found
the [Besson et al. eLife paper](https://doi.org/10.7554/eLife.108275)
(PMID 42223017), which
directly links TORC1 downregulation to improved chromosome segregation. An
OpenAlex title/abstract search for TORC1 and chromosome segregation from 2020
found 13 records, dominated by that paper and its public review/response records.
A separate targeted PubMed search confirmed no everolimus-specific chromosome-
segregation rescue report. The targeted search did not establish absence of all
related studies; it is not a systematic review.

The 2025 checkpoint-architecture evidence is consistent with [Sethi et al.](https://doi.org/10.1038/s41467-025-59970-1):
kinetochores accelerate mitotic checkpoint complex assembly at near-physiological protein
concentrations. A separate PubMed query combining BUB1B/BUBR1/spindle checkpoint/aneuploidy with
mTOR/rapamycin/everolimus/sirolimus for 2025-2026 yielded 13 records. Besson
et al. was not in that set because PubMed's supplementary-concept translation did
not map the title field exactly; that omission is why complementary searches and
OpenAlex were needed. Search receipts are preserved in
`sources/public-literature-v43/`.

## What Besson et al. actually shows

[Besson et al.](https://doi.org/10.7554/eLife.108275) (eLife, June 2026) studied **fission yeast**, not mammalian MVA.
In `mis4-G1487D`, a cohesin-loader mutant, TORC1 downregulation by rapamycin or
genetic hypomorphic alleles improved growth, increased cohesin binding to
chromosomal sites, and reduced anaphases with lagging DNA. Rapamycin (200 ng/mL)
during one cell-cycle doubling reduced lagging-DNA anaphases. The effect was
weaker than the genetic TORC1 mutant, and rapamycin and genetic TORC1 reduction
are not equivalent. In wild-type fission yeast, reduced TORC1 activity also
increased cohesin binding and chromosome transmission fidelity. The paper did
not test everolimus, BUB1B/BUBR1, a human cell, a constitutional MVA model,
useful non-cancer daughter output/recovery, injury, clinical exposure, or rescue.

The paper is mechanistically relevant because it links TORC1 activity to
chromosome segregation fidelity in a cohesin-loader context. It does not provide
a new target-organ rationale or human exposure basis. Because everolimus is an
approved mTORC1 inhibitor, the paper increases the plausibility that mTORC1
modulation could directly affect chromosome segregation rather than only downstream
sarcopenia. That is not evidence of benefit. TORC1 inhibition can also cause G1
arrest, alter autophagy, reduce output, and in other contexts impair cell survival.
The existing all-enrolled-cell useful-output and injury rules remain mandatory.

## Consequence for the proposal

1. Add a direct TORC1 activity check to the existing mTOR branch prerequisite:
   measure p70 S6 kinase and 4EBP1 phosphorylation in the engineered hTERT-RPE1
   comparator alongside BUBR1 protein, not only downstream organ or tissue markers.
2. Add a mitotic-specific chromosome-segregation endpoint: lagging DNA/anaphase
   bridges, all-enrolled daughter fate, and later useful output/recovery. This is
   not a ratio-only endpoint.
3. Keep everolimus on HOLD. It may only enter the joint-treatment factorial if
   the engineered deficit is reproducible and BUBR1 restoration is attributable.
   A valid negative in that model would close the tested claim in that model; it
   would not prove universal inefficacy.
4. Do not treat yeast evidence as evidence for everolimus. Rapamycin and
   everolimus are not interchangeable; even in fission yeast, rapamycin was weaker
   than genetic TORC1 reduction and partially inhibits TORC1.
5. If the model qualifies, test both everolimus and its matched vehicle, with
   dose/engagement measured in the same culture. A modest segregation improvement
   without preserved useful output, recovery, and injury margins would not advance
   the route.

## Falsification/stop rule

| Claim to test | Support needed | Falsifier / stopping condition | Next discriminating action |
|---|---|---|---|
| Reduced mTORC1 activity improves segregation in a BUB1B-deficient human context | mTORC1 activity marker falls after everolimus; lagging DNA falls; useful output and recovery are preserved; BUBR1 restoration effect is independently attributable | No mTORC1 engagement; no segregation improvement; or improved segregation with reduced useful output/increased injury | Test mTORC1 engagement and all-enrolled fate in the engineered hTERT-RPE1 comparator |
| TORC1 modulation is relevant outside yeast | Reproducible species/tissue-specific effect on segregation and useful output | Human RPE1 shows no segregation/output benefit at tolerated, verified exposure | Do not advance this branch without fresh non-cancer context evidence |
| Everolimus is the right perturbation | Engagement, exposure, and safety margins are measured and acceptable | mTORC1 engagement without segregation benefit, or unacceptable injury | Stop the everolimus branch; do not substitute sirolimus or NAD/SIRT2 without a new test |

## Boundaries

This is public literature evidence only. It does not validate a drug, dose,
clinical margin, therapeutic window, or biological assay. It does not use subject
data, subject phenotype text, or the subject VCF. No wet-lab experiment,
provider account verification, or submission readiness claim follows.
