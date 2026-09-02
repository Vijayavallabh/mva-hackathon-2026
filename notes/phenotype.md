# Phenotype (feat-002)

The protected DOCX was processed locally. This tracked note contains only standardized HPO
IDs, public ontology labels, and reviewed categorical context—no clinical narrative, dates,
places, exact ages, measurements, or identifying free text.

## HPO terms

| HPO ID | Label | Applies to | Broad timing | Domain | Clinical significance | Analysis role |
|---|---|---|---|---|---|---|
| `HP:0002859` | Rhabdomyosarcoma | proband | not specified | oncologic | malignancy that prompted genomic investigation | proband phenotype |
| `HP:0000121` | Nephrocalcinosis | proband | congenital | renal | congenital renal mineral deposition | proband phenotype |
| `HP:0004322` | Short stature | proband | not specified | growth | stature markedly low relative to familial and age expectations | proband phenotype |
| `HP:0001508` | Failure to thrive | proband | early life | growth and nutrition | persistent early somatic growth and musculature impairment | proband phenotype |
| `HP:0003202` | Skeletal muscle atrophy | proband | not specified | neuromuscular | diminished musculature accompanying poor overall growth | proband phenotype |
| `HP:0001622` | Premature birth | proband | perinatal | perinatal | substantial prematurity | proband phenotype |
| `HP:0001518` | Small for gestational age | proband | prenatal/perinatal | fetal growth | marked prenatal growth impairment with substantially reduced neonatal mass | proband phenotype |
| `HP:0200067` | Recurrent spontaneous abortion | parental/family history | family history | reproductive | recurrent parental pregnancy loss preceding the proband | family-history signal |

Seven terms are proband phenotypes; the reproductive-loss term is parental/family history.
Keep the latter as mechanistic and inheritance context, but do not score it as an
abnormality observed in the proband.

The useful signal is the full multi-system constellation: malignancy, congenital renal
involvement, impaired somatic and muscular development, adverse perinatal/fetal growth, and
parental reproductive loss. No individual term is diagnostic, and the context does not
establish whether the causal alleles were inherited or arose de novo.

This constellation—not any one row—was the clinical basis for genomic investigation.

## Interpretation policy

Use the cross-system pattern as the primary phenotype representation; never tune ranking
around one manifestation. The reproductive-history annotation is a clinically meaningful
input dimension rather than disposable metadata, while remaining scoped to family history.

For chromosome-instability syndromes, reproductive loss among relatives is compatible
with either inherited susceptibility or a newly arising causal event. Genomic evidence is
required to discriminate between those models; the family-history feature alone cannot.

## Method and provenance

The IDs were mechanically matched as `HP:` followed by seven digits in
`word/document.xml`. The script verifies that every ID has a populated Presentation/Notes
row, then applies the reviewed categorical mapping in `REVIEWED_CONTEXT`. Labels came from
the official [Human Phenotype Ontology OBO file](https://github.com/obophenotype/human-phenotype-ontology/releases/download/v2026-06-23/hp.obo).

- Ontology version: `hp/releases/2026-06-23`
- Local ontology SHA-256: `a5092cbdf605f568403cf7380d9173014015692433b2cc631bc5c1b053876b1b`
- Categorical context review recorded: `2026-09-02`
- Fetch ontology: `mkdir -p data/resources && curl --fail --location https://github.com/obophenotype/human-phenotype-ontology/releases/download/v2026-06-23/hp.obo --output data/resources/hp.obo`
- Reproduce: `uv run python scripts/extract_hpo.py`
- Data-free exercise: `uv run python scripts/extract_hpo.py --self-check`

## Scope of the search

The earlier structural keyword probe found no karyotype, prior genetic testing, or
candidate gene in the supplied material. The variant search therefore remains genome-wide;
known MVA genes are literature priors, not a hard shortlist.
