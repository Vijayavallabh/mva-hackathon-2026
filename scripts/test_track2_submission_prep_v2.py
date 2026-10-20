"""Regression tests for the owner-facing Track 2 submission-prep checklist."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


class SubmissionPrepTests(unittest.TestCase):
    def setUp(self):
        self.note = Path("notes/track2-submission-prep-v2.md").read_text()
        self.state = json.loads(Path("notes/track2-current.json").read_text())

    def test_checker_binds_exact_materials_and_false_submission_state(self):
        spec = importlib.util.spec_from_file_location("prep_v1", "scripts/check_track2_submission_prep_v2.py")
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        result = checker.check()
        self.assertEqual(result["version"], 2)
        self.assertGreater(result["report_pdf_bytes"], 0)
        self.assertGreater(result["report_md_bytes"], 0)
        self.assertEqual(
            (result["video_recorded"], result["video_url"], result["upload_ready"], result["upload_performed"]),
            (False, None, False, False),
        )

    def test_official_form_behavior_is_reflected(self):
        normalized = " ".join(self.note.split()).lower()
        for phrase in [
            "github repo url",
            "pitch video url",
            "report file",
            "notes for judges",
            "either the pdf or markdown version, not both",
            "username or team name in the report filename",
            "team / display name",
        ]:
            self.assertIn(phrase, normalized)

    def test_exact_portal_values_are_not_invented(self):
        normalized = " ".join(self.note.split()).lower()
        self.assertIn("https://github.com/vijayavallabh/mva-hackathon-2026", normalized)
        self.assertIn("owner to choose", normalized)
        self.assertIn("absent", normalized)
        for phrase in [
            "quota is known",
            "submission has been received",
            "biological validation is established",
            "prize eligibility is established",
            "provider settings are verified",
        ]:
            self.assertNotIn(phrase, normalized)

    def test_receipt_hash_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for relative in ["notes", "results/feat009/v47-documents-final-20261020-3",
                             "results/feat009/v47-slides-final-20261020-1", "sources/public-official-v42"]:
                (root / relative).mkdir(parents=True, exist_ok=True)
            for name in ["track2-submission-prep-v2.md", "track2-current.json", "track2-submission-materials-v1.json"]:
                (root / "notes" / name).write_bytes(Path("notes", name).read_bytes())
            (root / "sources/public-official-v42/tabs-submit_track2.py").write_bytes(
                Path("sources/public-official-v42/tabs-submit_track2.py").read_bytes())
            for name in ["jvv7_track2_report_v47.pdf", "jvv7_track2_report_v47.md",
                         "jvv7_track2_methods_v47.xlsx"]:
                source = Path("results/feat009/v47-documents-final-20261020-3", name)
                (root / "results/feat009/v47-documents-final-20261020-3" / name).write_bytes(source.read_bytes())
            slide = Path("results/feat009/v47-slides-final-20261020-1/track2-slides-v47.pdf")
            (root / "results/feat009/v47-slides-final-20261020-1/track2-slides-v47.pdf").write_bytes(slide.read_bytes())
            materials = json.loads((root / "notes/track2-submission-materials-v1.json").read_text())
            materials["report_pdf"]["sha256"] = "0" * 64
            (root / "notes/track2-submission-materials-v1.json").write_text(json.dumps(materials))
            spec = importlib.util.spec_from_file_location("mutated", "scripts/check_track2_submission_prep_v2.py")
            checker = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(checker)
            checker.ROOT = root
            checker.CHECKLIST = root / "notes/track2-submission-prep-v2.md"
            checker.CURRENT = root / "notes/track2-current.json"
            checker.MATERIALS = root / "notes/track2-submission-materials-v1.json"
            checker.OFFICIAL = root / "sources/public-official-v42/tabs-submit_track2.py"
            with self.assertRaises(AssertionError):
                checker.check()

if __name__ == "__main__":
    unittest.main()
