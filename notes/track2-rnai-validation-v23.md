# Qualification changes from the v23 RNAi analysis

This supplements [v21 validation](track2-validation-v21.md). It does not qualify an
assay, promote a drug or replace the v21 biological decision contract. All clinical
margins and experimental measurements remain unknown.

| Claim under challenge | New evidence | Change to the next discriminating experiment |
|---|---|---|
| Different reagent IDs imply independent target evidence | All ten BUB1B reagents have distinct deposited 6-mer and 7-mer seeds. Alternative mature products and potency were not measured. | Record reagent sequence, annotated/alternative seeds and target engagement separately. Distinct annotations meet the metadata check only. |
| Reproducible RNAi expression mainly reflects BUB1B | In each expression representation, 45/54 evaluable BUB1B reagent-context records correlate more with unrelated same-seed reagents than with same-target peers. | Include different-target, same-seed controls alongside independent perturbation/rescue controls. Randomize assay plates and preserve batch and replicate IDs. A coherent signature alone cannot pass on-target qualification. |
| The failed earlier filter rules out usable BUB1B biology | HT29's processed profile has positive excess coherence against the fixed batch reference; raw and processed results differ. | Retain HT29 as a candidate for independent target/function qualification. Do not call this tumour line a non-cancer MVA model or transfer its result to the child. Preserve the v19 failed filter and its partial positive. |
| An extreme tail in a small reference set is strong confirmation | Exact seed-reference sets can contain only 4–40 combinations. Finite-reference sensitivity removes all five primary threshold crossings. | Set null coverage, matching, multiplicity and missing-control rules before scoring; inspect effect size and precision. Zero exceedances must not be described as zero error probability. Require independent confirmation before advancing. |
| A useful RNAi/CRISPR benchmark validates BUB1B or everolimus | Other-gene agreement is recoverable, including MTOR, but this panel contains no BUB1B CRISPR data or joint drug/deficit observations. | Use orthogonal BUB1B perturbation and restoration in the intended model, with measured endogenous protein/function. Validate MTOR target engagement separately from functional benefit. |

The proposed joint-treatment study still needs qualified deficit and rescue controls,
a relevant non-cancer tissue model, first-division and daughter-fate measurements,
function, recovery and injury endpoints. Compare drug-plus-deficit with both deficit
alone and drug alone. Keep tumour killing separate and include deficient normal tissue
in that branch. Exposure matching must be justified independently; expression scores
cannot set a dose or exposure margin.

Stopping rules remain: invalid assay → hold inference; insufficient precision → hold
advancement; qualified evidence excluding meaningful benefit → stop the scoped claim;
failed safety → stop and review injury. Even all requirements passing permits only
further preclinical review. Unknown seed coverage is not an unfavorable result, and
an unfavorable expression score is not proof of biological harm.
