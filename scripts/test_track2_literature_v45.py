"""Regression tests for the targeted v45 falsification-literature addendum."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


class LiteratureV45Tests(unittest.TestCase):
    def setUp(self):
        self.note = Path("notes/track2-literature-v45.md").read_text()
        self.audit = json.loads(Path("notes/track2-literature-audit-v45.json").read_text())

    def test_checker_binds_searches_sources_and_boundaries(self):
        spec = importlib.util.spec_from_file_location("checker_v45", "scripts/check_track2_literature_v45.py")
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        result = checker.check()
        self.assertEqual((result["searches"], result["selected_sources"], result["public_receipts"]), (7, 4, 14))
        self.assertEqual(
            (result["subject_data_read"], result["drug_dispositions_changed"], result["biological_validation"],
             result["full_text_systematic_review"], result["new_gpu_campaign"]),
            (False, False, False, False, False),
        )

    def test_new_drug_records_cannot_be_promoted(self):
        d = self.audit["disposition_changes"]
        self.assertEqual(d["griseofulvin"], "not_promoted_tumour_killing_context_only")
        self.assertEqual(d["norlichexanthone"], "not_promoted_tumour_killing_context_only")
        self.assertEqual(d["vorinostat"], "unchanged_deprioritized_tumour_only")
        self.assertEqual(d["everolimus"], "unchanged_mechanistic_probe_only_on_hold")
        self.assertIsNone(d["rescue_priority"])
        self.assertEqual(d["phase"], "unconfirmed")

    def test_closed_access_reading_depth_is_honest(self):
        dois = {"10.1016/j.bioorg.2026.110130", "10.1016/j.compbiolchem.2026.109012"}
        for source in self.audit["selected_sources"]:
            if source["doi"] in dois:
                self.assertFalse(source["full_text_obtained"])
                self.assertIn("abstract", source["reading_depth"])

    def test_abstracts_contain_claimed_key_facts(self):
        norlich = Path("sources/public-literature-v45/pubmed-42330849-efetch.xml").read_text().lower()
        comp = Path("sources/public-literature-v45/pubmed-41895167-efetch.xml").read_text().lower()
        for phrase in ["mad1 and bubr1", "mad1-mad2 interaction", "norlichexanthone", "tpr"]:
            self.assertIn(phrase, norlich)
        for phrase in ["tpx2 and bub1b", "virtual-screening", "vorinostat", "breast cancer"]:
            self.assertIn(phrase, comp)

    def test_note_declares_no_new_gpu_campaign(self):
        normalized = " ".join(self.note.split()).lower()
        for phrase in [
            "not a systematic review",
            "it does **not** change any drug disposition",
            "do not run another gpu campaign",
            "no biological validation",
        ]:
            self.assertIn(phrase, normalized)
        for phrase in [
            "griseofulvin is promoted", "norlichexanthone is promoted", "vorinostat is reopened",
            "everolimus is promoted", "rescue priority is established",
        ]:
            self.assertNotIn(phrase, normalized)


if __name__ == "__main__":
    unittest.main()
