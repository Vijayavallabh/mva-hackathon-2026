"""Regression tests for the v43 targeted contrary-evidence literature addendum."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


class LiteratureV43Tests(unittest.TestCase):
    def setUp(self):
        self.note = Path("notes/track2-literature-v43.md").read_text()
        self.audit = json.loads(Path("notes/track2-literature-audit-v43.json").read_text())

    def test_checker_covers_searches_sources_and_boundaries(self):
        spec = importlib.util.spec_from_file_location("checker_v43", "scripts/check_track2_literature_v43.py")
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        result = checker.check()
        self.assertEqual(
            (result["searches"], result["selected_sources"], result["public_receipts"]),
            (3, 2, 5),
        )
        self.assertEqual(
            (
                result["subject_data_read"],
                result["drug_dispositions_changed"],
                result["biological_validation"],
                result["full_text_systematic_review"],
            ),
            (False, False, False, False),
        )

    def test_dispositions_are_unchanged(self):
        d = self.audit["disposition_changes"]
        self.assertEqual(d["everolimus"], "unchanged_mechanistic_probe_only_on_hold")
        self.assertEqual(d["hydroxychloroquine"], "unchanged_reserve")
        self.assertEqual(d["nad_sirt2"], "unchanged_not_promoted")
        self.assertIsNone(d["rescue_priority"])
        self.assertIsNone(d["clinical_exposure_margin"])
        self.assertEqual(d["phase"], "unconfirmed")

    def test_fulltext_scope_is_yeast_and_excludes_human_drug_terms(self):
        source = Path("sources/public-literature-v43/elife-108275-fulltext.xml").read_text().lower()
        self.assertIn("mis4-g1487d", source)
        self.assertIn("200 ng/ml", source)
        self.assertIn("rapamycin only partially inhibits torc1 activity", source)
        for term in ["everolimus", "sirolimus", "bub1b", "htert-rpe1"]:
            self.assertNotIn(term, source)

    def test_hash_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "notes").mkdir(parents=True)
            (root / "sources/public-literature-v43").mkdir(parents=True)
            for path in Path("notes").glob("track2-literature-v43*"):
                (root / "notes" / path.name).write_bytes(path.read_bytes())
            for path in Path("sources/public-literature-v43").iterdir():
                (root / "sources/public-literature-v43" / path.name).write_bytes(path.read_bytes())
            spec = importlib.util.spec_from_file_location("mutated", "scripts/check_track2_literature_v43.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.ROOT = root
            module.SOURCE_DIR = root / "sources/public-literature-v43"
            target = module.SOURCE_DIR / "elife-108275-fulltext.xml"
            original = target.read_bytes()
            target.write_bytes(original.replace(b"mis4-G1487D", b"mutated-G0000D", 1))
            with self.assertRaises(AssertionError):
                module.check()

    def test_note_declares_limitations_without_promoting_a_drug(self):
        normalized = " ".join(self.note.split()).lower()
        for phrase in [
            "not a new exhaustive systematic review",
            "does not change any drug disposition",
            "no rescue priority",
            "not a systematic review",
        ]:
            self.assertIn(phrase, normalized)
        for phrase in [
            "everolimus is promoted",
            "nad/sirt2 is promoted",
            "hcq is reopened",
            "clinical exposure margin is established",
            "phase is confirmed",
        ]:
            self.assertNotIn(phrase, normalized)


if __name__ == "__main__":
    unittest.main()
