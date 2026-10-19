#!/usr/bin/env python3
"""CPU mathematical checks, executed in the owner-hosted Torch environment."""
import importlib.util
import unittest


@unittest.skipUnless(importlib.util.find_spec('torch'), 'Run in the v35 remote Torch environment')
class OpticalModelTests(unittest.TestCase):
    def test_query_guide_is_excluded_from_own_reference(self):
        import torch
        from track2_optical_model_v35 import retrieve
        vectors=torch.tensor([[1.,0.],[0.,1.],[1.,0.],[1.,0.]])
        out=retrieve(vectors,{'A':[0,1],'B':[2,3]})
        self.assertEqual(out['rows'][0]['own_score'],0.)
        self.assertEqual(out['rows'][0]['rank'],2.)

    def test_identical_vectors_receive_average_ranks(self):
        import torch
        from track2_optical_model_v35 import retrieve
        out=retrieve(torch.ones((6,2)),{'A':[0,1],'B':[2,3],'C':[4,5]})
        self.assertEqual({r['rank'] for r in out['rows']},{2.})
        self.assertEqual(out['macro_mrr'],0.5)

    def test_insufficient_guides_and_controls_are_not_scored_as_negative(self):
        from track2_optical_model_v35 import eligible_groups
        rows=[dict(gene='BUB1B',split='test',cells=n) for n in [11,15,11,25]]
        rows += [dict(gene='MTOR',split='test',cells=30)]*2
        rows += [dict(gene='nontargeting_0',split='test',cells=100)]*2
        out=eligible_groups(rows,'test')
        self.assertEqual(set(out),{'MTOR'})

    def test_nonfinite_score_stops_analysis(self):
        import torch
        from track2_optical_model_v35 import retrieve
        with self.assertRaisesRegex(ValueError,'Nonfinite'):
            retrieve(torch.tensor([[float('nan'),1.],[1.,1.],[0.,1.],[1.,0.]]),{'A':[0,1],'B':[2,3]})


if __name__ == '__main__':
    unittest.main()
