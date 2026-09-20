import unittest
from track2_evo2_comparison import rc,functional_gate


class Evo2ScoreTests(unittest.TestCase):
    def rows(self,loss,retained):
        return [dict(id=str(i),group='LOF' if i<48 else 'FUNC',
                     delta_mean_strands=loss if i<48 else retained) for i in range(96)]

    def test_reverse_complement_round_trip(self):
        sequence='AAAACGTTG';self.assertEqual(rc(rc(sequence)),sequence)
        self.assertEqual(rc('AAGC'),'GCTT')

    def test_ambiguous_reference_rejected(self):
        with self.assertRaises(ValueError):rc('ACNT')

    def test_correct_score_direction(self):
        result=functional_gate(self.rows(-2.,-1.))
        self.assertEqual(result['auroc_negative_delta'],1.)
        self.assertTrue(result['pass_gate'])

    def test_reversed_direction_cannot_pass(self):
        result=functional_gate(self.rows(-1.,-2.))
        self.assertEqual(result['auroc_negative_delta'],0.)
        self.assertFalse(result['pass_gate'])

    def test_ties_not_counted_as_success(self):
        result=functional_gate(self.rows(-1.,-1.))
        self.assertEqual(result['auroc_negative_delta'],0.5)
        self.assertFalse(result['pass_gate'])

    def test_incomplete_benchmark_rejected(self):
        with self.assertRaises(ValueError):functional_gate(self.rows(-2.,-1.)[:-1])

    def test_duplicate_id_rejected(self):
        rows=self.rows(-2.,-1.);rows[1]['id']=rows[0]['id']
        with self.assertRaises(ValueError):functional_gate(rows)

    def test_nonfinite_rejected(self):
        rows=self.rows(-2.,-1.);rows[0]['delta_mean_strands']=float('nan')
        with self.assertRaises(ValueError):functional_gate(rows)


if __name__=='__main__':unittest.main()
