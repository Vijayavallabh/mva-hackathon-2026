#!/usr/bin/env python3
"""Cross-arm alignment and fixed-cell sampling controls cannot create evidence."""
import unittest
import numpy as np
import pandas as pd
from track2_optical_secondary_v35 import matched_fraction,sampled_means


class SecondaryTests(unittest.TestCase):
    def rows(self):
        return [dict(guide='A',gene='BUB1B',group='targeting',cells=20),
                dict(guide='B',gene='MTOR',group='targeting',cells=10)]

    def test_matching_uses_sequence_not_row_order(self):
        a=self.rows();b=[dict(a[1],cells=90),dict(a[0],cells=80)]
        values,records=matched_fraction(a,b,'mitotic')
        np.testing.assert_allclose(values[:,0],[.2,.1])
        self.assertEqual([r['interphase_cells'] for r in records],[80,90])
        inverse,_=matched_fraction(b,a,'interphase')
        np.testing.assert_allclose(inverse[:,0],[.1,.2])

    def test_missing_other_arm_is_explicit_zero_observed_not_missing_target(self):
        a=self.rows();values,records=matched_fraction(a,a[:1],'interphase')
        self.assertEqual(values[1,0],0.)
        self.assertTrue(records[1]['other_arm_zero_observed'])
        self.assertEqual(records[1]['interphase_cells'],10)

    def test_conflicting_gene_and_duplicate_guides_fail(self):
        a=self.rows()
        with self.assertRaisesRegex(ValueError,'Conflicting'):
            matched_fraction(a,[dict(a[0],gene='WRONG')],'mitotic')
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            matched_fraction(a,a+[a[0]],'mitotic')

    def test_fixed_sample_mean_and_missing_features_survive_guide_reordering(self):
        a=self.rows()
        meta=pd.DataFrame(dict(sgRNA_0=['B','A','B','A'],gene_symbol_0=['MTOR','BUB1B','MTOR','BUB1B']))
        x=np.array([[2.,np.nan],[4.,2.],[6.,np.nan],[8.,4.]],dtype=np.float32)
        means,finite,counts=sampled_means(x,meta,a)
        np.testing.assert_allclose(means,[[6.,3.],[4.,np.nan]],equal_nan=True)
        np.testing.assert_array_equal(finite,[[2,2],[2,0]])
        np.testing.assert_array_equal(counts,[2,2])

    def test_changed_sample_attribution_or_clipping_fails(self):
        a=self.rows();meta=pd.DataFrame(dict(sgRNA_0=['A','B'],gene_symbol_0=['BUB1B','MTOR']))
        with self.assertRaisesRegex(ValueError,'clipping'):
            sampled_means(np.array([[11.,0.],[1.,1.]]),meta,a)
        meta.loc[0,'gene_symbol_0']='WRONG'
        with self.assertRaisesRegex(ValueError,'attribution'):
            sampled_means(np.ones((2,2)),meta,a)


if __name__=='__main__':unittest.main()
