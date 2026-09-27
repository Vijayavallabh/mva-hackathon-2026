"""Numerical and interpretation regressions for the new public-data campaign."""
import unittest
import track2_transcriptome as t


class TranscriptomeTests(unittest.TestCase):
    def test_bh_known_example(self):
        self.assertEqual(t.bh([.01,.04,.03,.2]),[.04,.05333333333333334,.05333333333333334,.2])

    def test_bh_input_rejection(self):
        for values in [[float('nan')],[-.1],[1.1]]:
            with self.assertRaises(ValueError):t.bh(values)

    def test_splits_are_disjoint_complete_and_unordered(self):
        splits=t.half_splits(6)
        self.assertEqual(len(splits),10)
        observed=set()
        for a,b in splits:
            self.assertEqual(set(a)|set(b),set(range(6)))
            self.assertFalse(set(a)&set(b))
            observed.add(frozenset([frozenset(a),frozenset(b)]))
        self.assertEqual(len(observed),10)
        self.assertEqual(len(t.half_splits(3)),3)

    def test_qc_not_only_signature_strength(self):
        good=dict(distil_nsample=3,distil_cc_q75=.2,tas=.2)
        self.assertTrue(t.quality(good))
        for k in good:
            bad=good.copy();bad[k]=-666
            self.assertFalse(t.quality(bad))

    def test_rank_sign_and_ties(self):
        import numpy as np
        x=t.ranked([[1,1,2,4],[4,4,2,1]])
        np.testing.assert_allclose(x@x.T,[[1,-1],[-1,1]],atol=1e-12)

    def test_invalid_vector_rejected(self):
        for value in [[[1,1,1]],[[1,float('nan'),3]],[[1,float('inf'),3]]]:
            with self.assertRaises(ValueError):t.ranked(value)


if __name__=='__main__': unittest.main()
