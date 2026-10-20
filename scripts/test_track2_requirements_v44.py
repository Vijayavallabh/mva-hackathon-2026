"""Regression tests for the anonymous live v44 deadline refresh."""
import json
import tempfile
import importlib.util
import unittest
from pathlib import Path


class RequirementsV44Tests(unittest.TestCase):
    def setUp(self):
        self.audit = json.loads(Path("notes/track2-requirements-v44.json").read_text())
        self.review = Path("notes/track2-requirements-review-v44.md").read_text()

    def test_current_state_is_preserved(self):
        spec = importlib.util.spec_from_file_location('checker_v44', 'scripts/check_track2_requirements_v44.py')
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        result = checker.check()
        self.assertEqual(
            (result["official_sources"], result["public_threads"], result["closed_threads"]),
            (7, 31, 16),
        )
        self.assertEqual(
            (result["requirements_changed"], result["anonymous_get_only"], result["upload_ready"]),
            (False, True, False),
        )

    def test_all_seven_official_files_are_bound_by_hash(self):
        expected = {
            "README.md", "config.py", "tabs/about.py", "tabs/rules.py",
            "tabs/faq.py", "tabs/submit_track2.py",
            "static/templates/methods_description_form.xlsx",
        }
        self.assertEqual({x["name"] for x in self.audit["official_sources"]}, expected)
        self.assertTrue(all(x["http_status"] == 200 and x["unchanged"] for x in self.audit["official_sources"]))

    def test_listing_is_checked_without_false_full_thread_reread(self):
        listing = self.audit["discussion_listing"]
        self.assertEqual(listing["count"], 31)
        self.assertEqual(listing["closed_count"], 16)
        self.assertEqual(listing["visible_comment_counts_not_reread"], True)
        self.assertEqual(listing["new_organizer_requirement_found"], False)

    def test_core_deadline_and_rubric_are_unchanged(self):
        r = self.audit["unchanged_requirements"]
        self.assertEqual(r["deadline_utc"], "2026-10-24T23:59:00Z")
        self.assertEqual(r["video_duration_seconds"], 180)
        self.assertEqual(r["rubric_weights"], {"scientific_rigor": 35, "potential_impact": 25, "innovation": 25, "scalability": 15})
        self.assertIsNone(r["quota_remaining"])
        self.assertEqual(r["data_deletion_deadline"], "2026-11-23")
        self.assertEqual(r["data_deletion_confirmation_email"], "cnb@sagebase.org")

    def test_no_false_readiness_or_biology_claim(self):
        normalized = " ".join(self.review.split()).lower()
        for phrase in ["quota is known", "upload is ready", "provider settings are verified", "establishes biological validation", "clinical safety recommendation", "submission was performed"]:
            self.assertNotIn(phrase, normalized)
        self.assertFalse(self.audit["provider_settings_verified"])
        self.assertFalse(self.audit["upload_ready"])

    def test_mutated_timestamp_or_requirement_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "notes").mkdir(parents=True)
            for name in ["track2-requirements-v44.json", "track2-requirements-review-v44.md"]:
                (root / "notes" / name).write_bytes(Path("notes", name).read_bytes())
            audit = json.loads((root / "notes/track2-requirements-v44.json").read_text())
            audit["retrieved_utc"] = "2026-10-24T00:00:00Z"
            (root / "notes/track2-requirements-v44.json").write_text(json.dumps(audit))
            spec = importlib.util.spec_from_file_location("mutated", "scripts/check_track2_requirements_v44.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.ROOT = root
            module.AUDIT = root / "notes/track2-requirements-v44.json"
            module.REVIEW = root / "notes/track2-requirements-review-v44.md"
            with self.assertRaises(AssertionError):
                module.check()


if __name__ == "__main__":
    unittest.main()
