# Phenotype (feat-002)

The protected DOCX was processed locally. This tracked note contains only the standardized
HPO IDs embedded in it, their public ontology labels, and broad lexical context signals—no
clinical narrative, dates, places, ages, measurements, or identifying free text.

## HPO terms

| HPO ID | Label | Presentation/Notes signals |
|---|---|---|
| `HP:0002859` | Rhabdomyosarcoma | no broad signal |
| `HP:0000121` | Nephrocalcinosis | perinatal timing |
| `HP:0004322` | Short stature | family context |
| `HP:0001508` | Failure to thrive | no broad signal |
| `HP:0003202` | Skeletal muscle atrophy | no broad signal |
| `HP:0001622` | Premature birth | prenatal timing, perinatal timing, quantitative detail |
| `HP:0001518` | Small for gestational age | perinatal timing, quantitative detail |
| `HP:0200067` | Recurrent spontaneous abortion | proband context, family context, prenatal timing, perinatal timing, longitudinal detail |

The signal columns are conservative keyword matches, not clinical interpretation. “No
broad signal” means none of the fixed categories matched; it does not mean the cell was
empty or uninformative. Exact wording and quantitative values remain protected locally.
Mixed proband/family signals are deliberately left unresolved and must not be converted
into phenotype-ranking weights without authorized local human review.

## Method and provenance

The IDs were mechanically matched as `HP:` followed by seven digits in
`word/document.xml`. The combined Presentation/Notes column was reduced to a fixed
vocabulary covering subject context, broad timing, and information type. Labels came from
the official [Human Phenotype Ontology OBO file](https://purl.obolibrary.org/obo/hp.obo).

- Ontology version: `hp/releases/2026-06-23`
- Local ontology SHA-256: `a5092cbdf605f568403cf7380d9173014015692433b2cc631bc5c1b053876b1b`
- Fetch ontology: `mkdir -p data/resources && curl --fail --location https://purl.obolibrary.org/obo/hp.obo --output data/resources/hp.obo`
- Reproduce: `uv run python scripts/extract_hpo.py`
- Data-free exercise: `uv run python scripts/extract_hpo.py --self-check`

## Scope of the search

The earlier structural keyword probe found no karyotype, prior genetic testing, or
candidate gene in the supplied material. The variant search therefore remains genome-wide;
known MVA genes are literature priors, not a hard shortlist.
