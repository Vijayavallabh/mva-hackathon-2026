#!/usr/bin/env python3
"""The gain gate must fail on one weak seed or a stronger simple baseline."""
import unittest
import numpy as np
from track2_optical_audit_v35 import paired_gain


class PairedGainTests(unittest.TestCase):
    def test_constant_paired_gain_and_interval(self):
        out=paired_gain(np.full((2,20),.1),np.full((4,20),.15),repetitions=1024)
        self.assertTrue(out['practical_gain_gate_passed'])
        np.testing.assert_allclose(out['paired_95_percent_intervals'],np.full((4,2),.05))

    def test_one_bad_seed_blocks_gain(self):
        learned=np.full((4,20),.2);learned[3]=.11
        out=paired_gain(np.full((2,20),.1),learned,repetitions=1024)
        self.assertFalse(out['practical_gain_gate_passed'])
        self.assertFalse(out['all_seeds_exceed_002'])

    def test_strongest_simple_baseline_cannot_be_omitted(self):
        out=paired_gain(np.array([[.1]*20,[.3]*20]),np.full((4,20),.2),repetitions=1024)
        self.assertFalse(out['practical_gain_gate_passed'])
        self.assertLess(out['joint_minimum_seed_95_percent_interval'][1],0)

    def test_nonfinite_and_misaligned_matrices_fail(self):
        for base,learned in [(np.full((2,20),np.nan),np.ones((4,20))),
                             (np.ones((2,20)),np.ones((4,19))),
                             (np.ones((2,20)),np.ones((3,20)))]:
            with self.assertRaises(ValueError):
                paired_gain(base,learned,repetitions=100)


if __name__=='__main__':
    unittest.main()
