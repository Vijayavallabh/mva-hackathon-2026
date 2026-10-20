"""Historical v43 harness tests are superseded; run the v47 test module.

The current state intentionally moved to v47. Keeping this generic name active would test
v43 against current files and fail misleadingly.
"""
import unittest
from pathlib import Path


class HistoricalHarnessTests(unittest.TestCase):
    def test_current_harness_is_checked_by_versioned_v47_test(self):
        self.assertTrue(Path("scripts/test_track2_harness_v47.py").is_file())


if __name__ == "__main__":
    unittest.main()
