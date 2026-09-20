"""Check coordinate conversion and fail-closed pilot decisions without model weights."""
import copy
import unittest

from track2_esm_pilot import control_gate, parse_variant, token_position


class PilotTests(unittest.TestCase):
    def test_reference_coordinates(self):
        self.assertEqual(parse_variant("D3N", "ACDE"), ("D", 3, "N"))

    def test_wrong_reference_rejected(self):
        with self.assertRaises(ValueError):
            parse_variant("N3K", "ACDE")

    def test_non_substitutions_rejected(self):
        for value in ("D3*", "D3D", "D03N", "D0N", "D30N", "D3NN"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_variant(value, "ACDE")

    def test_bos_and_window_offsets(self):
        self.assertEqual(token_position(1002, 1, 1022), 1002)
        self.assertEqual(token_position(1002, 29, 1050), 974)
        self.assertEqual(token_position(1002, 721, 1044), 282)
        self.assertEqual(token_position(29, 29, 1050), 1)
        self.assertEqual(token_position(1050, 29, 1050), 1022)

    def test_silent_truncation_rejected(self):
        for values in ((1002, 1, 1050), (28, 29, 1050), (1051, 29, 1050)):
            with self.assertRaises(ValueError):
                token_position(*values)

    @staticmethod
    def rows():
        return [{"window": w, "group": g, "score": s}
                for w in ("a", "b", "c")
                for g, s in (("primary_retained", -1), ("primary_impaired", -2),
                             ("primary_impaired", -3), ("primary_impaired", -4),
                             ("secondary_retained", -100))]

    def test_direction_and_secondary_exclusion(self):
        gate = control_gate(self.rows())
        self.assertTrue(gate["pass"])
        self.assertEqual(gate["windows"]["a"]["retained_minus_highest_impaired"], 1)

    def test_one_failed_window_stops(self):
        rows = self.rows()
        rows[0]["score"] = -5
        self.assertFalse(control_gate(rows)["pass"])

    def test_ties_do_not_pass(self):
        rows = self.rows()
        rows[0]["score"] = -2
        self.assertFalse(control_gate(rows)["pass"])

    def test_missing_control_or_window_stops(self):
        for rows in (self.rows()[1:], self.rows()[5:]):
            with self.assertRaises(ValueError):
                control_gate(rows)

    def test_nonfinite_scores_rejected(self):
        for value in (float("nan"), float("inf"), -float("inf")):
            rows = copy.deepcopy(self.rows())
            rows[1]["score"] = value
            with self.assertRaises(ValueError):
                control_gate(rows)


if __name__ == "__main__":
    unittest.main()
