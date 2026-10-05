# V29 qualification amendments

Use with `track2-validation-v21.md`, the v23/v25/v27 qualification notes and
`track2-orthogonal-v29.md`. Eleven drug dispositions remain unchanged.

1. **Control labels attach to an endpoint and experiment.** Preserve the 2012 D882N/A
   comparison but do not call either a universally functional or clinically benign
   control. The 2019 CENP-E phosphorylation result and 2020 KARD-S676 result must accompany
   future interpretation. A control that retains abundance may still fail a distinct
   molecular or cellular function. Resolve the relevant assay response before using it
   to qualify an endogenous candidate result.
2. **Separate structural compatibility from function.** ProteinMPNN fails the expanded
   control ordering in all 24 comparisons. Its candidate score therefore cannot open
   a protein-stabilizer branch, determine pathogenicity, or prioritize a drug. Report
   WT- and mutant-backbone results together. Neither a stable score nor a favorable
   predicted fold supplies abundance, localization, binding, catalytic or segregation
   measurements.
3. **Keep HT29 as an attribution lead.** Agreement survives exclusion of evaluated genes
   from projection fitting and removal of failed CRISPR profiles. It still comes from
   one guide in a tumour context. Require an independent guide or non-cutting perturbation,
   restoration, measured depletion, and growth/viability/editing controls. Then establish
   the relevant deficit in a non-cancer model before extrapolating functional benefit.
4. **Missing qualified queries stay missing.** MCF7 drug QC and MTOR mimicry cannot qualify
   BUB1B. No passing MCF7 BUB1B query exists in this dataset. Do not zero-fill it, carry
   forward an all-profile estimate as QC-qualified, or combine it with HT29 as a joint
   response. Recover new qualified same-model perturbation evidence before reopening.
5. **Retain the competing explanations.** Component removal may erase true biology;
   persistence may reflect a shared pathway rather than target specificity. Compare
   relevant checkpoint/mitotic controls, use independently qualified perturbations, and
   measure all cell fates. Expression reversal, reduced proliferation and tumour killing
   are not evidence of safer divisions in non-cancer tissue.
6. **Judge computational controls at their actual scope.** One stock/exact pilot and one
   direct API comparison are numerical checks. Four related checkpoints, six predicted
   backbones, repeated gene partitions and 67,584 fixed-site samples are not independent
   biological replicates. Keep failed runtime attempts, all outcomes and fixed input hashes.

The catalytic disagreement requires discriminating biology, not a vote between papers
or model families. Assess endogenous abundance and localization alongside KARD/PP2A
recruitment and direct chromosome-attachment/segregation outcomes; use catalytic or
CENP-E assays only for the specific mechanism they test. Claims of rescue still require
qualified joint treatment, justified exposure and benefit/injury margins, independent
confirmation, and the existing safety-first stop rules.
