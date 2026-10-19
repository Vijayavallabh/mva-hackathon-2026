import unittest
import numpy as np
from track2_optical_plate_control_v36 import plate_vectors


class PlateMetadataTests(unittest.TestCase):
    def test_proportions_single_plate_and_complete_count_conservation(self):
        rows=[dict(guide='g1',cells=10),dict(guide='g2',cells=20)]
        parts=[dict(guide='g2',plate='B',cells=15),dict(guide='g1',plate='A',cells=10),dict(guide='g2',plate='A',cells=5)]
        values,single,plates=plate_vectors(rows,parts)
        np.testing.assert_array_equal(values,[[1.,0.],[.25,.75]])
        self.assertEqual(single,['A',None]);self.assertEqual(plates,['A','B'])

    def test_duplicate_or_missing_cells_fail(self):
        rows=[dict(guide='g1',cells=10)];part=dict(guide='g1',plate='A',cells=5)
        for values in [[part],[part,part]]:
            with self.subTest(values=values),self.assertRaises(ValueError):plate_vectors(rows,values)


if __name__=='__main__':unittest.main()
