#!/usr/bin/env python3
"""Distinct-guide and separate-source arithmetic for plate sensitivity."""
import importlib.util
import unittest


@unittest.skipUnless(importlib.util.find_spec('torch'),'Run on the owner host')
class PlateRetrievalTests(unittest.TestCase):
    def test_same_guide_on_another_plate_is_excluded(self):
        import torch
        from track2_optical_plate_v35 import separate_retrieval
        q=torch.tensor([[1.,0.],[0.,1.],[1.,0.],[1.,0.]])
        r=q.clone()
        result=separate_retrieval(q,r,{'A':[0,1],'B':[2,3]},{'A':[0,1],'B':[2,3]})
        self.assertEqual(result['rows'][0]['own_score'],0.)
        self.assertEqual(result['rows'][0]['rank'],2.)

    def test_other_plate_values_are_used_for_reference(self):
        import torch
        from track2_optical_plate_v35 import separate_retrieval
        q=torch.tensor([[1.,0.],[1.,0.],[0.,1.],[0.,1.]])
        r=torch.tensor([[0.,1.],[0.,1.],[1.,0.],[1.,0.]])
        result=separate_retrieval(q,r,{'A':[0,1],'B':[2,3]},{'A':[0,1],'B':[2,3]})
        self.assertEqual({x['rank'] for x in result['rows']},{2.})

    def test_coverage_failure_is_missing_not_zero(self):
        import torch
        from track2_optical_plate_v35 import separate_retrieval
        result=separate_retrieval(torch.ones(2,2),torch.ones(2,2),{'A':[0,1]},{'A':[0,1]})
        self.assertEqual(result['status'],'insufficient_reference_genes')
        self.assertIsNone(result['macro_mrr'])


if __name__=='__main__':
    unittest.main()
