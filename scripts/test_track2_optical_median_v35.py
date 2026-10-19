#!/usr/bin/env python3
"""A guide spanning files must never be reduced as a mean of shard medians."""
import importlib.util
import unittest
import warnings
import numpy as np
from track2_optical_median_v35 import assignments,gpu_median


class AssignmentTests(unittest.TestCase):
    def test_shared_guides_keep_connected_files_together(self):
        files=[dict(guides={'A':1,'B':1},bytes=10),dict(guides={'B':1,'C':1},bytes=8),
               dict(guides={'C':1},bytes=9),dict(guides={'D':1},bytes=30)]
        jobs=assignments(files,workers=2)
        self.assertEqual(sorted(i for job in jobs for i in job),[0,1,2,3])
        self.assertTrue(any(set(job)=={0,1,2} for job in jobs))
        self.assertEqual(jobs,assignments(files,workers=2))

    def test_empty_workers_do_not_duplicate_work(self):
        jobs=assignments([dict(guides={'A':1},bytes=10)],workers=8)
        self.assertEqual(jobs,[[0],[],[],[],[],[],[],[]])


@unittest.skipUnless(importlib.util.find_spec('torch'),'Run in owner-hosted Torch environment')
class MedianArithmeticTests(unittest.TestCase):
    def test_even_odd_missing_and_all_missing_features(self):
        x=np.array([[1.,2.,np.nan,5.],[3.,4.,np.nan,np.nan],[9.,8.,np.nan,7.],
                    [10.,np.nan,np.nan,np.nan]],dtype=np.float32)
        median,finite=gpu_median(x,'cpu')
        np.testing.assert_allclose(median,[6.,4.,np.nan,6.],equal_nan=True)
        np.testing.assert_array_equal(finite,[4,3,0,2])

    def test_split_guide_needs_all_values(self):
        a=np.array([[0.],[0.],[0.]],dtype=np.float32);b=np.array([[10.]],dtype=np.float32)
        actual,_=gpu_median(np.concatenate([a,b]),'cpu')
        shard_a,_=gpu_median(a,'cpu');shard_b,_=gpu_median(b,'cpu')
        self.assertEqual(actual[0],0.)
        self.assertNotEqual(actual[0],(shard_a[0]+shard_b[0])/2)

    def test_random_float32_matches_cpu_float64(self):
        x=np.random.default_rng(3502).normal(size=(31,14)).astype(np.float32);x[::3,::2]=np.nan
        median,_=gpu_median(x,'cpu')
        np.testing.assert_allclose(median,np.nanmedian(x.astype(np.float64),axis=0),rtol=0,atol=2e-5)


if __name__=='__main__':unittest.main()
