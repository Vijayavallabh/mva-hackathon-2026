"""Extract public-safe phenotype features from the protected phenotype DOCX.

The protected clinical narrative is read locally but is never printed or written. The
program emits standardized HPO IDs plus reviewed, non-verbatim categorical context; it never
emits the Presentation or Notes cell text, numbers, ages, or measurements.

Run the real extraction from the repository root:

    uv run python scripts/extract_hpo.py

Run the synthetic, data-free exercise:

    uv run python scripts/extract_hpo.py --self-check
"""

from __future__ import annotations

import argparse
import hashlib
import re
import tempfile
import zipfile
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOCX = ROOT / "data" / "Challenge_Clinical_Phenotype_1.docx"
DEFAULT_ONTOLOGY = ROOT / "data" / "resources" / "hp.obo"
DEFAULT_OUTPUT = ROOT / "notes" / "phenotype.md"
HPO_SOURCE = "https://purl.obolibrary.org/obo/hp.obo"
CONTEXT_REVIEW_DATE = "2026-09-02"
HPO_ID = re.compile(rb"HP:\d{7}")
WORD_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WORD = {"w": WORD_NAMESPACE}
FORBIDDEN_QUANTITATIVE_DETAIL = re.compile(
    r"\d|\b(?:kg|kilogram\w*|gram\w*|cm|mm|week\w*|month\w*|year\w*)\b", re.I
)

class SubjectScope(StrEnum):
    """Whose phenotype or history a reviewed term describes."""

    PROBAND = "proband"
    FAMILY = "parental/family history"


@dataclass(frozen=True)
class PhenotypeContext:
    """Reviewed, non-verbatim context safe for the eventual public repository."""

    applies_to: SubjectScope
    broad_timing: str
    domain: str
    clinical_significance: str

    @property
    def analysis_role(self) -> str:
        return (
            "proband phenotype"
            if self.applies_to is SubjectScope.PROBAND
            else "family-history signal"
        )


# Curated from the protected Presentation/Notes column. Exact wording and quantitative
# details intentionally do not appear here. The extractor detects ID-set changes and empty
# context rows. A wording-only source change still requires a fresh human review.
REVIEWED_CONTEXT = {
    "HP:0002859": PhenotypeContext(
        SubjectScope.PROBAND,
        "not specified",
        "oncologic",
        "malignancy that prompted genomic investigation",
    ),
    "HP:0000121": PhenotypeContext(
        SubjectScope.PROBAND,
        "congenital",
        "renal",
        "congenital renal mineral deposition",
    ),
    "HP:0004322": PhenotypeContext(
        SubjectScope.PROBAND,
        "not specified",
        "growth",
        "stature markedly low relative to familial and age expectations",
    ),
    "HP:0001508": PhenotypeContext(
        SubjectScope.PROBAND,
        "early life",
        "growth and nutrition",
        "persistent early somatic growth and musculature impairment",
    ),
    "HP:0003202": PhenotypeContext(
        SubjectScope.PROBAND,
        "not specified",
        "neuromuscular",
        "diminished musculature accompanying poor overall growth",
    ),
    "HP:0001622": PhenotypeContext(
        SubjectScope.PROBAND,
        "perinatal",
        "perinatal",
        "substantial prematurity",
    ),
    "HP:0001518": PhenotypeContext(
        SubjectScope.PROBAND,
        "prenatal/perinatal",
        "fetal growth",
        "marked prenatal growth impairment with substantially reduced neonatal mass",
    ),
    "HP:0200067": PhenotypeContext(
        SubjectScope.FAMILY,
        "family history",
        "reproductive",
        "recurrent parental pregnancy loss preceding the proband",
    ),
}


def _read_document_xml(docx: Path) -> bytes:
    """Read the sole protected DOCX member used by both extraction stages."""
    with zipfile.ZipFile(docx) as archive:
        try:
            return archive.read("word/document.xml")
        except KeyError as error:
            raise ValueError("DOCX has no word/document.xml member") from error


def extract_hpo_ids(docx: Path) -> list[str]:
    """Return unique HPO IDs in document order without returning narrative text."""
    document_xml = _read_document_xml(docx)
    # Searching the XML bytes avoids storing or exposing the surrounding clinical text.
    found = (match.group().decode("ascii") for match in HPO_ID.finditer(document_xml))
    return list(dict.fromkeys(found))


def _cell_text(cell: ElementTree.Element) -> str:
    """Join Word text runs for local classification; callers must not emit the result."""
    return "".join(node.text or "" for node in cell.findall(".//w:t", WORD)).strip()


def _word_ngrams(text: str, size: int = 3) -> set[tuple[str, ...]]:
    """Return normalized word n-grams for private in-memory disclosure checks."""
    words = re.findall(r"[a-z]+", text.casefold())
    return {tuple(words[index : index + size]) for index in range(len(words) - size + 1)}


def validate_context_rows(
    docx: Path, contexts: Mapping[str, PhenotypeContext]
) -> set[str]:
    """Validate populated rows and summaries without returning protected source text."""
    root = ElementTree.fromstring(_read_document_xml(docx))
    tables = root.findall(".//w:tbl", WORD)
    if len(tables) != 1:
        raise ValueError("expected exactly one phenotype table")
    rows = tables[0].findall("./w:tr", WORD)
    if not rows:
        raise ValueError("phenotype table has no rows")

    header_cells = rows[0].findall("./w:tc", WORD)
    headers = [_cell_text(cell).casefold() for cell in header_cells]
    context_indices = [
        index
        for index, header in enumerate(headers)
        if "present" in header and "note" in header
    ]
    feature_indices = [
        index
        for index, header in enumerate(headers)
        if "clinical" in header and "feature" in header
    ]
    if len(context_indices) != 1:
        raise ValueError("phenotype table lacks one combined Presentation/Notes column")
    if len(feature_indices) != 1:
        raise ValueError("phenotype table lacks one Clinical Feature column")
    context_index = context_indices[0]
    protected_indices = (feature_indices[0], context_index)

    populated: set[str] = set()
    for row_number, row in enumerate(rows[1:], 1):
        cells = row.findall("./w:tc", WORD)
        if context_index >= len(cells):
            raise ValueError("phenotype table row has too few columns")
        row_ids = HPO_ID.findall(" ".join(_cell_text(cell) for cell in cells).encode())
        source_texts = [_cell_text(cells[index]) for index in protected_indices]
        if row_ids and not source_texts[-1]:
            raise ValueError(f"phenotype table row {row_number} has empty context")
        for raw_id in row_ids:
            hpo_id = raw_id.decode("ascii")
            populated.add(hpo_id)
            context = contexts.get(hpo_id)
            if context is None:
                continue
            summary = " ".join(
                (context.broad_timing, context.domain, context.clinical_significance)
            )
            if FORBIDDEN_QUANTITATIVE_DETAIL.search(summary):
                raise ValueError(f"reviewed context contains quantitative detail: {hpo_id}")
            source_ngrams = set().union(*(_word_ngrams(text) for text in source_texts))
            if source_ngrams & _word_ngrams(summary):
                raise ValueError(f"reviewed context overlaps protected wording: {hpo_id}")
    return populated


def _finish_obo_term(fields: dict[str, object], labels: dict[str, str]) -> None:
    """Add one non-obsolete OBO term and its alternate IDs to ``labels``."""
    term_id = fields.get("id")
    name = fields.get("name")
    if not isinstance(term_id, str) or not isinstance(name, str):
        return
    if fields.get("is_obsolete") == "true":
        return
    labels[term_id] = name
    for alt_id in fields.get("alt_ids", []):
        if isinstance(alt_id, str):
            labels[alt_id] = name


def parse_obo(ontology: Path) -> tuple[dict[str, str], dict[str, str]]:
    """Return HPO ID-to-label mappings and public ontology header metadata."""
    labels: dict[str, str] = {}
    metadata: dict[str, str] = {}
    fields: dict[str, object] | None = None

    with ontology.open(encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            if line == "[Term]":
                if fields is not None:
                    _finish_obo_term(fields, labels)
                fields = {"alt_ids": []}
                continue
            if line.startswith("["):
                if fields is not None:
                    _finish_obo_term(fields, labels)
                fields = None
                continue
            if ": " not in line:
                continue

            key, value = line.split(": ", 1)
            if fields is None:
                if key in {"format-version", "data-version", "ontology"}:
                    metadata[key] = value
            elif key == "alt_id":
                alt_ids = fields["alt_ids"]
                assert isinstance(alt_ids, list)
                alt_ids.append(value)
            elif key in {"id", "name", "is_obsolete"}:
                fields[key] = value

    if fields is not None:
        _finish_obo_term(fields, labels)
    return labels, metadata


def sha256(path: Path) -> str:
    """Calculate a resource checksum without loading the whole file into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def render_markdown(
    ids: Iterable[str],
    labels: dict[str, str],
    contexts: Mapping[str, PhenotypeContext],
    metadata: dict[str, str],
    digest: str,
) -> str:
    """Build the public-safe phenotype note without protected cell text."""
    rows = []
    for hpo_id in ids:
        try:
            label = labels[hpo_id]
        except KeyError as error:
            raise ValueError(f"HPO ID is absent or obsolete in hp.obo: {hpo_id}") from error
        try:
            context = contexts[hpo_id]
        except KeyError as error:
            raise ValueError(f"HPO ID lacks reviewed context: {hpo_id}") from error
        rows.append(
            f"| `{hpo_id}` | {label} | {context.applies_to} | "
            f"{context.broad_timing} | {context.domain} | "
            f"{context.clinical_significance} | {context.analysis_role} |"
        )

    table = "\n".join(rows)
    data_version = metadata.get("data-version", "not declared")
    return f"""# Phenotype (feat-002)

The protected DOCX was processed locally. This tracked note contains only standardized HPO
IDs, public ontology labels, and reviewed categorical context—no clinical narrative, dates,
places, exact ages, measurements, or identifying free text.

## HPO terms

| HPO ID | Label | Applies to | Broad timing | Domain | Clinical significance | Analysis role |
|---|---|---|---|---|---|---|
{table}

Seven terms are proband phenotypes; the reproductive-loss term is parental/family history.
Keep the latter as mechanistic and inheritance context, but do not score it as an
abnormality observed in the proband.

The useful signal is the full multi-system constellation: malignancy, congenital renal
involvement, impaired somatic and muscular development, adverse perinatal/fetal growth, and
parental reproductive loss. No individual term is diagnostic, and the context does not
establish whether the causal alleles were inherited or arose de novo.

This constellation—not any one row—was the clinical basis for genomic investigation.

## Method and provenance

The IDs were mechanically matched as `HP:` followed by seven digits in
`word/document.xml`. The script verifies that every ID has a populated Presentation/Notes
row, then applies the reviewed categorical mapping in `REVIEWED_CONTEXT`. Labels came from
the official [Human Phenotype Ontology OBO file]({HPO_SOURCE}).

- Ontology version: `{data_version}`
- Local ontology SHA-256: `{digest}`
- Categorical context review recorded: `{CONTEXT_REVIEW_DATE}`
- Fetch ontology: `mkdir -p data/resources && curl --fail --location {HPO_SOURCE} --output data/resources/hp.obo`
- Reproduce: `uv run python scripts/extract_hpo.py`
- Data-free exercise: `uv run python scripts/extract_hpo.py --self-check`

## Scope of the search

The earlier structural keyword probe found no karyotype, prior genetic testing, or
candidate gene in the supplied material. The variant search therefore remains genome-wide;
known MVA genes are literature priors, not a hard shortlist.
"""


def run(
    docx: Path,
    ontology: Path,
    output: Path,
    contexts: Mapping[str, PhenotypeContext] = REVIEWED_CONTEXT,
) -> list[str]:
    """Extract IDs, resolve labels, and write the safe derived-output note."""
    ids = extract_hpo_ids(docx)
    if not ids:
        raise ValueError("no embedded HPO IDs found")
    populated_context = validate_context_rows(docx, contexts)
    missing_rows = [hpo_id for hpo_id in ids if hpo_id not in populated_context]
    if missing_rows:
        raise ValueError(f"HPO IDs have no populated Presentation/Notes row: {missing_rows}")
    missing_review = [hpo_id for hpo_id in ids if hpo_id not in contexts]
    stale_review = [hpo_id for hpo_id in contexts if hpo_id not in ids]
    if missing_review or stale_review:
        raise ValueError(
            f"reviewed context does not match document IDs: "
            f"missing={missing_review}, stale={stale_review}"
        )
    labels, metadata = parse_obo(ontology)
    output.write_text(render_markdown(ids, labels, contexts, metadata, sha256(ontology)))
    return ids


def self_check() -> None:
    """Exercise extraction, deduplication, label lookup, and disclosure boundaries."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        docx = root / "synthetic.docx"
        ontology = root / "hp.obo"
        output = root / "phenotype.md"

        xml = f"""<w:document xmlns:w="{WORD_NAMESPACE}"><w:body><w:tbl>
<w:tr><w:tc><w:p><w:r><w:t>Clinical Feature</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:r><w:t>HPO ID</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:r><w:t>Clinical Presentations / Notes</w:t></w:r></w:p></w:tc></w:tr>
<w:tr><w:tc><w:p><w:r><w:t>Example one</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:r><w:t>HP:0000001</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:r><w:t>The child was diagnosed after birth; private measurement was 12 cm at 37 weeks on 2026-01-01 and treated surgically</w:t></w:r></w:p></w:tc></w:tr>
<w:tr><w:tc><w:p><w:r><w:t>Example two</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:r><w:t>HP:0000002</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:r><w:t>Private family pregnancy history was recurrent</w:t></w:r></w:p></w:tc></w:tr>
</w:tbl></w:body></w:document>"""
        with zipfile.ZipFile(docx, "w") as archive:
            archive.writestr("word/document.xml", xml)
        ontology.write_text(
            "format-version: 1.2\n"
            "data-version: synthetic/test\n\n"
            "[Term]\n"
            "id: HP:0000001\n"
            "name: Synthetic term one\n\n"
            "[Term]\n"
            "id: HP:0000002\n"
            "name: Synthetic term two\n"
        )

        synthetic_context = {
            "HP:0000001": PhenotypeContext(
                SubjectScope.PROBAND,
                "congenital",
                "renal",
                "synthetic renal context",
            ),
            "HP:0000002": PhenotypeContext(
                SubjectScope.FAMILY,
                "family history",
                "reproductive",
                "synthetic family context",
            ),
        }
        ids = run(docx, ontology, output, synthetic_context)
        rendered = output.read_text()
        assert ids == ["HP:0000001", "HP:0000002"]
        assert "Synthetic term one" in rendered
        assert "Synthetic term two" in rendered
        assert "Private measurement" not in rendered
        assert "Private pregnancy" not in rendered
        assert "12 cm" not in rendered
        assert "37 weeks" not in rendered
        assert "2026-01-01" not in rendered
        assert "diagnosed after birth" not in rendered
        assert "congenital" in rendered
        assert "parental/family history" in rendered

        unsafe_quantitative = dict(synthetic_context)
        unsafe_quantitative["HP:0000001"] = PhenotypeContext(
            SubjectScope.PROBAND,
            "congenital",
            "renal",
            "quantified as 37 units",
        )
        try:
            run(docx, ontology, output, unsafe_quantitative)
        except ValueError as error:
            assert "quantitative detail" in str(error)
        else:
            raise AssertionError("quantitative context was not rejected")

        unsafe_overlap = dict(synthetic_context)
        unsafe_overlap["HP:0000001"] = PhenotypeContext(
            SubjectScope.PROBAND,
            "congenital",
            "renal",
            "the child was diagnosed after birth private measurement",
        )
        try:
            run(docx, ontology, output, unsafe_overlap)
        except ValueError as error:
            assert "overlaps protected wording" in str(error)
        else:
            raise AssertionError("verbatim context was not rejected")
    print("self-check ok: IDs and reviewed context resolved; protected text not emitted")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract HPO IDs and reviewed context without exposing narrative."
    )
    parser.add_argument("--docx", type=Path, default=DEFAULT_DOCX)
    parser.add_argument("--ontology", type=Path, default=DEFAULT_ONTOLOGY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--self-check", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    if arguments.self_check:
        self_check()
    else:
        extracted = run(arguments.docx, arguments.ontology, arguments.output)
        print(f"wrote {arguments.output} with {len(extracted)} HPO terms")
