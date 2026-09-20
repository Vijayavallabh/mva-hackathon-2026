import unittest
import numpy as np
from track2_structure_analysis import aligned_distances


class StructureGeometryTests(unittest.TestCase):
    def setUp(self):
        self.xyz=np.array([[0.,0.,0.],[1.,0.,0.],[0.,2.,0.],[0.,0.,3.]])

    def test_rigid_translation_rotation_does_not_create_change(self):
        rotation=np.array([[0,-1,0],[1,0,0],[0,0,1]])
        distances=aligned_distances(self.xyz,self.xyz@rotation+np.array([5.,-2.,7.]))
        self.assertLess(max(distances),1e-12)

    def test_reflection_is_not_permitted_rotation(self):
        reflected=self.xyz.copy();reflected[:,0]*=-1
        self.assertGreater(max(aligned_distances(self.xyz,reflected)),0.1)

    def test_actual_deformation_retained(self):
        changed=self.xyz.copy();changed[0]+=[1,2,3]
        self.assertGreater(max(aligned_distances(self.xyz,changed)),0.1)

    def test_missing_coordinates_rejected(self):
        with self.assertRaises(ValueError):aligned_distances(self.xyz,self.xyz[:-1])

    def test_nan_rejected(self):
        changed=self.xyz.copy();changed[0,0]=np.nan
        with self.assertRaises(ValueError):aligned_distances(self.xyz,changed)


if __name__=='__main__':unittest.main()
