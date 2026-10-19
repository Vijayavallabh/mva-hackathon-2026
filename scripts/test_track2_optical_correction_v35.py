#!/usr/bin/env python3
from copy import deepcopy
import json
import unittest
import check_track2_optical_correction_v35 as c


class OpticalClaimTests(unittest.TestCase):
    def test_verified_snapshot_passes(self):
        self.assertTrue(c.check()['passed'])

    def test_gain_or_bub1b_promotion_fails(self):
        r=json.loads((c.ROOT/'notes/track2-optical-mitotic-results-v35.json').read_text())
        for field,value in [('practical_gain_gate_passed',True),('joint_lower_bound_positive',True)]:
            altered=deepcopy(r);altered['real_gain'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):c.validate(altered)
        altered=deepcopy(r);altered['query_status']['BUB1B']['status']='evaluated'
        with self.assertRaises(ValueError):c.validate(altered)


if __name__=='__main__':
    unittest.main()
