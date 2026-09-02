# Phenotype (feat-002)

The protected DOCX was processed locally. This tracked note contains only the standardized
HPO IDs embedded in it and their public ontology labels—no clinical narrative, dates,
places, ages, or identifying free text.

## HPO terms

| HPO ID | Label |
|---|---|
| `HP:0002859` | Rhabdomyosarcoma |
| `HP:0000121` | Nephrocalcinosis |
| `HP:0004322` | Short stature |
| `HP:0001508` | Failure to thrive |
| `HP:0003202` | Skeletal muscle atrophy |
| `HP:0001622` | Premature birth |
| `HP:0001518` | Small for gestational age |
| `HP:0200067` | Recurrent spontaneous abortion |

## Method and provenance

The IDs were mechanically matched as `HP:` followed by seven digits in
`word/document.xml`; no phenotype was inferred from prose. Labels came from the official
[Human Phenotype Ontology OBO file](https://purl.obolibrary.org/obo/hp.obo).

- Ontology version: `hp/releases/2026-06-23`
- Local ontology SHA-256: `a5092cbdf605f568403cf7380d9173014015692433b2cc631bc5c1b053876b1b`
- Fetch ontology: `mkdir -p data/resources && curl --fail --location https://purl.obolibrary.org/obo/hp.obo --output data/resources/hp.obo`
- Reproduce: `uv run python scripts/extract_hpo.py`
- Data-free exercise: `uv run python scripts/extract_hpo.py --self-check`

## Scope of the search

The earlier structural keyword probe found no karyotype, prior genetic testing, or
candidate gene in the supplied material. The variant search therefore remains genome-wide;
known MVA genes are literature priors, not a hard shortlist.
