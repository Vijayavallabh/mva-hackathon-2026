"""Scientific failure cases for the new public CRISPR campaign."""
import unittest
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from track2_crispr_v25 import aggregate, normalize, quality, ranknorm


class CrisprNumerics(unittest.TestCase):
    def test_tied_and_reversed_profiles_match_scipy(self):
        a=np.array([1,1,2,3,5,5.])
        b=np.array([5,4,4,2,1,1.])
        self.assertAlmostEqual(float(ranknorm(a)@ranknorm(b)),spearmanr(a,b).statistic,places=12)

    def test_missing_and_constant_profiles_cannot_become_zero_evidence(self):
        for a in [np.ones(7),np.array([0,np.nan,1]),np.array([1,np.inf,2])]:
            with self.subTest(a=a),self.assertRaises(ValueError):ranknorm(a)

    def test_qc_codes_and_missing_metrics_are_not_truthy_passes(self):
        d=pd.DataFrame(dict(qc_pass=['1','2','1','1','1'],nsample=['3']*5,
                            cc_q75=['.2','.9','','-666','.9'],tas=['.2']*4+['.1']))
        self.assertEqual(quality(d).tolist(),[True,False,False,False,False])

    def test_three_batches_of_one_guide_remain_one_guide(self):
        d=pd.DataFrame(dict(cmap_name=['BUB1B']*3,pert_id=['same-guide']*3,
            batch=['a','b','c'],sig_id=['s1','s2','s3'],distil_ids=['r1|r2','r3|r4','r1|r5'],
            cell_mfc_name=['engineered']*3,qc_pass=['1']*3,nsample=['3']*3,
            cc_q75=['.4']*3,tas=['.4']*3))
        meta,values=aggregate(d,np.array([[1,2],[2,4],[3,6]]),['cmap_name'])
        self.assertEqual(meta.iloc[0].guide_ids,['same-guide'])
        self.assertEqual(meta.iloc[0].distil_ids,['r1','r2','r3','r4','r5'])
        np.testing.assert_allclose(values,[[2,4]])

    def test_equal_weight_means_use_original_row_indices(self):
        d=pd.DataFrame(dict(cmap_name=['A','B'],pert_id=['g1','g2'],batch=['a','a'],
            sig_id=['s1','s2'],distil_ids=['r1','r2'],cell_mfc_name=['cell']*2,
            qc_pass=['1']*2,nsample=['3']*2,cc_q75=['.4']*2,tas=['.4']*2),index=[2,0])
        meta,values=aggregate(d,np.array([[10,20],[99,99],[30,40]]),['cmap_name'])
        self.assertEqual(meta.cmap_name.tolist(),['A','B'])
        np.testing.assert_allclose(values,[[30,40],[10,20]])


if __name__=='__main__':unittest.main()
