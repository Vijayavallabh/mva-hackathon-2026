"""Historical v41 harness tests are superseded; run the v43 test module.

The current state intentionally moved to v43.  Keeping this generic name active
would test v41 against current files and fail misleadingly.
"""
import unittest


class HistoricalHarnessTests(unittest.TestCase):
    def test_current_harness_is_checked_by_versioned_v43_test(self):
        from pathlib import Path
        self.assertTrue(Path("scripts/test_track2_harness_v43.py").is_file())


if __name__ == "__main__":
    unittest.main()
