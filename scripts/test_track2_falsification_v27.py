"""Numerical and archive boundaries for the v27 falsification campaign."""
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
import numpy as np
from analyze_track2_falsification_v27 import distribution
from archive_track2_falsification_v27 import verify
from track2_saturation_v27 import jobs
from track2_specificity_v27 import ranks, unit


class AnalysisBoundaries(unittest.TestCase):
    def test_shards_cover_each_coordinate_once(self):
        plan=json.loads(Path('notes/track2-saturation-plan-v27.json').read_text())
        for shard in range(0,8,2):
            a={(w['name'],p) for w,p in jobs(plan,shard)}
            b={(w['name'],p) for w,p in jobs(plan,shard+1)}
            self.assertFalse(a&b);self.assertEqual(len(a|b),2368)
        for bad in [-1,8,True]:
            with self.assertRaises(ValueError):jobs(plan,bad)

    def test_negative_is_not_rare_and_inclusive_ties(self):
        d=distribution([-4.,-2.,-2.,-.1,1.],-2.)
        self.assertEqual(d['negative_fraction'],.8)
        self.assertEqual(d['at_or_below_candidate_fraction'],.6)
        self.assertEqual(d['n'],5)

    def test_empty_or_nonfinite_background_rejected(self):
        for v in [[],[float('nan')],[float('inf')]]:
            with self.assertRaises(ValueError):distribution(v,0.)

    def test_rank_correlation_ties_and_anticorrelation(self):
        x=np.array([[2.,2.,5.,9.],[9.,9.,5.,2.]])
        z=ranks(x)
        self.assertAlmostEqual(float(z[0]@z[1]),-1.)
        np.testing.assert_allclose(z.sum(1),0.,atol=1e-12)

    def test_zero_residual_cannot_become_zero_evidence(self):
        with self.assertRaises(ValueError):unit(np.zeros((2,4)))

    def test_projection_removes_only_selected_directions(self):
        q=np.array([[1.,0.,0.]]).T
        z=np.array([[3.,4.,5.]])
        r=unit(z-(z@q)@q.T)
        self.assertAlmostEqual(float((r@q)[0,0]),0.)
        self.assertAlmostEqual(float(np.linalg.norm(r)),1.)
        self.assertAlmostEqual(float(r[0,1]/r[0,2]),.8)

    def test_tar_traversal_and_links_rejected_before_write(self):
        for name,kind in [('../escape',tarfile.REGTYPE),('/absolute',tarfile.REGTYPE),('link',tarfile.SYMTYPE)]:
            with tempfile.TemporaryDirectory() as d:
                root=Path(d);archive=root/'bad.tar.gz'
                with tarfile.open(archive,'w:gz') as tar:
                    member=tarfile.TarInfo(name);member.type=kind;member.size=0
                    tar.addfile(member,io.BytesIO(b''))
                with self.assertRaises(ValueError):verify(archive,root/'out')
                self.assertFalse((root/'out').exists())


if __name__=='__main__':unittest.main()
