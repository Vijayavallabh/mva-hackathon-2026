import itertools
import unittest
import numpy as np
from scipy.stats import spearmanr
from track2_rnai_v23 import ranknorm, valid_draws, valid_seed, pair_mean, bh

class RNAiNumerics(unittest.TestCase):
    def test_tied_spearman(self):
        x=np.array([[1,1,2,5,6],[6,4,4,1,0]],float)
        self.assertAlmostEqual(float(ranknorm(x)[0]@ranknorm(x)[1]),spearmanr(*x).statistic,places=14)

    def test_bad_vectors_rejected(self):
        for x in [[1,1,1],[1,float('nan'),3],[1,float('inf'),3]]:
            with self.subTest(x=x),self.assertRaises(ValueError):ranknorm([x])

    def test_independent_target_and_seed_constraints(self):
        genes=np.array(['A','A','B','C']);seeds=np.array(['AAA','BBB','AAA','CCC'])
        draws=np.array([[0,1],[0,2],[0,3]])
        self.assertEqual(valid_draws(draws,genes).tolist(),[False,True,True])
        self.assertEqual(valid_draws(draws,genes,seeds).tolist(),[False,False,True])

    def test_mean_pair_excludes_diagonal(self):
        m=np.array([[99,.1,.4],[.1,99,.7],[.4,.7,99]])
        self.assertAlmostEqual(pair_mean(m,np.array([[0,1,2]]))[0],.4)
        self.assertAlmostEqual(pair_mean(m,np.array([[2,0]]))[0],.4)

    def test_seed_missing_rejected(self):
        self.assertTrue(valid_seed('ACGTAC',6))
        for s in ['-666','ACGNAC','ACGTA','']:
            self.assertFalse(valid_seed(s,6))

    def test_BH_keeps_missing_family_members(self):
        self.assertAlmostEqual(bh([.001]+[1]*35)[0],.036)
        np.testing.assert_allclose(bh([.8,.1,.2]),[.8,.3,.3],rtol=0,atol=1e-15)

if __name__=='__main__':unittest.main()
