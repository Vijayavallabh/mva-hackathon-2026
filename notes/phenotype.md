# Phenotype (feat-002)

The protected DOCX was processed locally. This tracked note contains only standardized HPO
IDs, public ontology labels, and reviewed categorical context—no clinical narrative, dates,
places, exact ages, measurements, or identifying free text.

## HPO terms

| HPO ID | Label | Applies to | Broad timing | Domain | Analysis role |
|---|---|---|---|---|---|
| `HP:0002859` | Rhabdomyosarcoma | proband | not specified | oncologic | proband phenotype |
| `HP:0000121` | Nephrocalcinosis | proband | congenital | renal | proband phenotype |
| `HP:0004322` | Short stature | proband | not specified | growth | proband phenotype |
| `HP:0001508` | Failure to thrive | proband | early life | growth and nutrition | proband phenotype |
| `HP:0003202` | Skeletal muscle atrophy | proband | not specified | neuromuscular | proband phenotype |
| `HP:0001622` | Premature birth | proband | perinatal | perinatal | proband phenotype |
| `HP:0001518` | Small for gestational age | proband | prenatal/perinatal | fetal growth | proband phenotype |
| `HP:0200067` | Recurrent spontaneous abortion | parental/family history | family history | reproductive | family-history signal |

Seven terms are proband phenotypes; the reproductive-loss term is parental/family history.
Keep the latter as mechanistic and inheritance context, but do not score it as an
abnormality observed in the proband.

The useful signal is the full multi-system constellation: malignancy, congenital renal
involvement, impaired growth and redacted development, adverse perinatal/fetal growth, and
parental reproductive loss. No individual term is diagnostic, and the context does not
establish whether the causal alleles were inherited or arose de novo.

## Method and provenance

The IDs were mechanically matched as `HP:` followed by seven digits in
`word/document.xml`. The script verifies that every ID has a populated Presentation/Notes
row, then applies the reviewed categorical mapping in `REVIEWED_CONTEXT`. Labels came from
the official [Human Phenotype Ontology OBO file](https://purl.obolibrary.org/obo/hp.obo).

- Ontology version: `hp/releases/2026-06-23`
- Local ontology SHA-256: `a5092cbdf605f568403cf7380d9173014015692433b2cc631bc5c1b053876b1b`
- Categorical context review recorded: `2026-09-02`
- Fetch ontology: `mkdir -p data/resources && curl --fail --location https://purl.obolibrary.org/obo/hp.obo --output data/resources/hp.obo`
- Reproduce: `uv run python scripts/extract_hpo.py`
- Data-free exercise: `uv run python scripts/extract_hpo.py --self-check`

## Scope of the search

The earlier structural keyword probe found no karyotype, prior genetic testing, or
candidate gene in the supplied material. The variant search therefore remains genome-wide;
known MVA genes are literature priors, not a hard shortlist.
