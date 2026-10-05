# Track 2 v29: structural controls and fair expression comparisons

6 October 2026 IST. Completed on all eight owner-host H100s, using public resources
under `~/v/mva-track2-orthogonal-20261006-v29`. Read this addendum with the preserved
v28 report and presentation. Drug decisions remain unchanged.

**The new calculations strengthen HT29 as an assay-development lead and weaken any
attempt to infer allele function from protein-model scores.** They do not establish a
rescue-priority drug. Everolimus remains an optional, model-qualified mechanistic probe;
HCQ remains reserve. Endogenous allele effects, phase and clinical exposure margins
remain unknown.

## What changed

| Question | Completed test | Consequence |
|---|---|---|
| Does structural compatibility discriminate known control endpoints? | ProteinMPNN separates the historical primary controls in **1/24** weight/backbone comparisons; the expanded panel passes **0/24**. | Structural likelihood cannot qualify N1002K function. |
| Is N1002K's structural score stable to the input backbone? | WT-backbone mean log odds range **−5.696 to −5.389**; mutant-predicted backbones give **−2.780 to +0.463**. | Keep backbone conditioning explicit; selecting the favorable structure would distort the conclusion. |
| Does HT29 agreement survive fair adjustment and QC restriction? | PRIME RNAi/CRISPR correlation is **0.3500** after retaining only passing CRISPR profiles; mean-plus-ten-PC residual correlations remain **0.1223–0.1371**. | Preserve HT29 for attribution/assay development, with independent-guide and non-cancer-model gates intact. |
| Is the MCF7 drug connection robust? | BUB1B reversal attenuates under held-out adjustment, and no MCF7 BUB1B CRISPR query survives QC. MTOR matching remains first. | Drug target engagement and deficit rescue remain different claims. |

Complete numerical records are in `track2-structural-results-v29.json`,
`track2-structural-probabilities-v29.tsv` and `track2-crossfit-results-v29.json`.
`track2-orthogonal-summary-v29.json` derives the compact ranges. These are computational
comparisons of reused public resources, not new biological experiments.

## Structural evidence: stronger candidate score, failed functional calibration

The fixed plan evaluated four related ProteinMPNN checkpoints on six existing
ESMFold2 WT domain backbones: single-sequence and shared-MSA predictions, three seeds
each. Twenty-one positions include all 17 asparagines in residues 721–1044 and the
historical control sites. Every other residue was fixed to the public WT sequence.
Each context retained 128 samples of the upstream decoding policy and its amino-acid
probabilities. Another 24 contexts scored position 1002 on mutant-predicted backbones.
The total is **528 contexts and 67,584 fixed-site samples**, with 10,560 aggregate
site/amino-acid records. No therapeutic sequence was selected from those samples.

N1002K has the lowest mean log odds among the 17 N→K substitutions on every WT
backbone/checkpoint combination. That is favorable candidate-specific evidence within
this representation. It is **not** a pathogenicity probability or measured destabilization.
The same scorer usually fails to place all historical impaired controls below D882N,
and never separates the expanded impaired/retained panel. All outcomes are retained;
we do not select the one passing primary comparison.

Mutant-predicted backbones substantially change the score, including positive values.
This sensitivity does not prove that either backbone is biologically correct or that
the substitution is harmless. Predicted geometry conditions the model's preferences.
An isolated domain omits cellular partners, dynamics and regulation; checkpoint and
backbone repetitions are dependent, and training overlap remains unresolved.

The endpoint labels themselves require care. The 2012 reconstitution study supports
D882N/A as retained controls for its measured stability and mitotic endpoints.
[Suijkerbuijk et al.](https://doi.org/10.1016/j.devcel.2012.03.009)
The 2019 study reports that D882N retains stability but loses CENP-E phosphorylation;
this challenges a universal “functional” label without directly repeating every earlier
segregation assay. [Huang et al.](https://doi.org/10.1038/s41422-019-0178-z)
The 2020 study retains D882N/A stability and KARD-S676 signals and supports a scaffolding
role, while leaving activity under other conditions open.
[Gama Braga et al.](https://doi.org/10.1016/j.celrep.2020.108397)
We preserve the fixed 2012 ordering for reproducibility and label it endpoint-specific.
We do not relabel controls after seeing model scores or claim to resolve the catalytic
controversy computationally.

## Expression evidence: evaluated genes excluded from fitting

V27 excluded selected query genes from projection fitting, but competing reference
genes could remain in the fit. V29 fixes that asymmetry. For each fold, both modalities
exclude all query genes and all evaluated reference genes before fitting the pooled
mean direction and up to ten principal components. References are assigned by a
deterministic gene-symbol hash shared across modalities. Four partitions, five folds,
five cells, two RNAi representations and two CRISPR-quality views produce **400 fits**
and **820,147,416 correlation comparisons**.

The views use all 978 features or remove the fitted mean plus one, three or ten PCs.
All ordinary reference genes are evaluated once per partition. The same experiments
recur across partitions, and the ten query genes recur in every fold. The resulting
ranges are sensitivity ranges, **not confidence intervals**. Removing shared components
can remove real biology and is not causal adjustment. CRISPR QC restriction does not
establish RNAi potency or resolve seed effects.

HT29 retains positive PRIME agreement in all views. After restricting CRISPR to its
passing profile, residual ten-PC ranks are **1–6 among 715–781 RNAi reference genes**
and **1–3 among 276–340 CRISPR reference genes** across the 20 partitions. The broader
three-PC sensitivity reaches RNAi rank 7. These smaller held-out denominators must not
be compared directly with v27's full-panel ranks. One BUB1B guide still underlies the
CRISPR evidence. Failed-batch records remain in the all-profile arm.

The held-out benchmark also improves in aggregate after projection. For HT29's
QC-restricted PRIME arm, first-place RNAi retrieval rises from 5.67% to 7.48%, and
first-place CRISPR retrieval from 7.38% to 9.10%. These percentages describe repeated
reference-gene retrieval records, not independent experimental successes or causal
specificity. The full benchmark and other eight query genes are retained.

For reference-matching MCF7 everolimus at **0.1 µM nominal culture exposure**, BUB1B
correlation changes from −0.2144 to −0.0335…−0.0259 after mean-plus-ten-PC removal.
Its within-fold reversal rank changes from 1–3 to 204–308 among 787–920 references.
MTOR mimicry remains first, including in the QC-restricted CRISPR arm. Every MCF7
BUB1B query fails the specified QC: the QC-restricted result is **missing**, not zero,
negative evidence of rescue, or something that passing drug QC can repair. No
HT29-plus-MCF7 composite rescue claim is supported.

## What the toolkit actually did

We executed the pinned [Anthropic ProteinMPNN optimization kit](https://github.com/anthropics/uplifting-biomolecular-modeling/tree/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/proteinmpnn)
in `exact` mode with pinned upstream source and recorded checkpoint hashes. The
four checkpoint sets are variants of one model family. The stock/exact pilot produced
identical sequence bytes and probability/score arrays. A separate paired upstream
sampling/direct-conditional check differed by at most **1.79×10⁻⁷** in probability.
That control forced the queried site last; production retained the upstream random
ordering policy. These checks establish bounded software agreement, not biology.

Setup failures are preserved: the configuration flag belongs to the shell wrapper,
the upstream fixed-position file requires one JSON object per line, and Triton needed
the pinned setuptools runtime dependency. Upstream model code was not altered.
The kit's own pinned-weight list covers its default checkpoints; the extra 010/030
weights are pinned here through the upstream commit and recorded SHA-256 values.
No general speedup or whole-campaign bitwise-equivalence claim is made from one pilot.

All eight model workers and all eight expression workers finished. Device monitoring
and worker timings are in `track2-orthogonal-compute-v29.json`; sampled utilization
is distinct from continuous saturation. No raw subject file, source VCF record or
clinical narrative was transferred. No additional hosted model provider was used.
The remote folder remains in the November 24 deletion scope.

## Next discriminating evidence

Clinical counterevidence also remains relevant. [ARST1431](https://www.sciencedirect.com/science/article/pii/S1470204524002559)
did not demonstrate an event-free-survival benefit from adding temsirolimus to its
rhabdomyosarcoma regimen. This limits extrapolation from mTOR matching to efficacy;
it did not test everolimus for MVA functional rescue. The [official everolimus label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=5aaf2fb7-93f6-40d6-941a-9583a3794ce7)
retains infection, pneumonitis, renal and marrow risks. Its distribution and binding
data do not establish an unbound tissue margin from nominal culture exposure.
Scaffolding/PP2A recruitment remains a competing mechanism to test; HCQ gains no
priority by elimination. These source checks preserve the existing gates.

Use the existing v21 biological decision contract plus
`track2-orthogonal-validation-v29.md`. Qualify independent perturbation/restoration,
abundance, kinetochore recruitment and first-division/daughter outcomes before joint
drug testing. The control conflict adds a requirement to specify which endpoint a
control validates and to separate stability, scaffolding and catalytic readouts.
No protein or expression score substitutes for this work. Unknown evidence remains
HOLD; a safety failure overrides apparent benefit; all-pass permits preclinical
review only. No wet-lab result or clinical recommendation follows from this campaign.
