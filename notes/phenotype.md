# Phenotype (feat-002 — not started)

Source: `data/Challenge_Clinical_Phenotype_1.docx` (gitignored, 380 words).

The official rules state phenotypic data is provided "as standardized HPO terms", and a
structural probe confirms the document carries **8 embedded `HP:#######` IDs**. So this is
mechanical ID extraction, not narrative-to-HPO inference.

Keep this file free of anything that could re-identify the child or the family: **HPO term
IDs and labels only** — no narrative quotes, no dates, no places, no ages, no free text
lifted from the document. That boundary is what `AGENTS.md` rule 1 permits to be shared,
and this file is bound for a public repository (feat-007).

## HPO terms

_(to fill — feat-002: `scripts/extract_hpo.py` pulls the `HP:` IDs from `word/document.xml`
with stdlib `zipfile`, resolves labels against `hp.obo` from feat-003)_

| HPO ID | Label |
|---|---|
| _(to fill)_ | |

## What the document does not contain

Verified by keyword probe, all **absent**: `karyotype`, `aneuploid`, `mosaic`, `trisomy`,
`OMIM`, `exome`, `variant`, `VUS`, `negative`, `microcephaly`, `BUB1B`, `CEP57`, `TRIP13`.

There is **no prior genetic workup, no karyotype result and no candidate gene** in the
material we were given. The variant search must stay genome-wide — see
`prior-knowledge.md`.
