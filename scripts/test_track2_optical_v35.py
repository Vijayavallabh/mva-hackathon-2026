#!/usr/bin/env python3
"""Check the coordinate-leak correction without changing counts or sampling."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import track2_optical_prepare_v33 as old
import track2_optical_prepare_v35 as new


class OpticalCorrectionTests(unittest.TestCase):
    def test_centroids_are_excluded_but_shape_and_relative_displacement_remain(self):
        fields = ['nucleus_centroid_r','nucleus_centroid_c','cell_centroid_r','cell_centroid_c',
                  'nucleus_area','cell_area','nucleus_eccentricity',
                  'cell_dapi_mass_displacement','cell_dapi_center_mass_r']
        schema = pa.schema([(n,pa.float64()) for n in fields])
        self.assertEqual(new.phenotype_columns(schema),fields[4:8])
        self.assertEqual(set(old.phenotype_columns(schema))-set(new.phenotype_columns(schema)),set(fields[:4]))

    def test_corrected_preparation_preserves_cells_and_adds_plate_counts(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); source=root/'inputs/mitotic';source.mkdir(parents=True)
            jobs=[]
            for k in range(2):
                n=180
                frame=pd.DataFrame(dict(plate=['A']*90+['B']*90,well=['A1']*n,
                    tile=[k]*n,label=range(n),sgRNA_0=['ACGT']*n,gene_symbol_0=['BUB1B']*n,
                    group_0=['targeting']*n,nucleus_area=np.arange(n,dtype=float)/10,
                    cell_area=[np.nan]*20+[3.]*160,nucleus_centroid_r=np.arange(n,dtype=float)))
                p=source/f'part.{k}.parquet';pq.write_table(pa.Table.from_pandas(frame,preserve_index=False),p)
                jobs.append(dict(label=p.name,dataFile=dict(id=k,filesize=p.stat().st_size,
                    checksum=dict(value=hashlib.md5(p.read_bytes()).hexdigest()))))
            a=['nucleus_area','cell_area','nucleus_centroid_r']; b=a[:2]
            with contextlib.redirect_stdout(io.StringIO()):
                old.merge(root,'mitotic',a,[old.prepare_file((str(root),'mitotic',r,a)) for r in jobs])
                new.merge(root,'mitotic',b,[new.prepare_file((str(root),'mitotic',r,b)) for r in jobs])
            x=root/'prepared/mitotic';y=root/'prepared-v35/mitotic'
            self.assertEqual((x/'guides.json').read_bytes(),(y/'guides.json').read_bytes())
            pd.testing.assert_frame_equal(pq.read_table(x/'sample_meta.parquet').to_pandas(),
                                          pq.read_table(y/'sample_meta.parquet').to_pandas())
            np.testing.assert_array_equal(np.load(x/'sample_x.npy')[:,:2],np.load(y/'sample_x.npy'))
            with np.load(x/'full_profiles.npz') as first, np.load(y/'full_profiles.npz') as second:
                for key in ['sums','means','finite_counts']:
                    np.testing.assert_array_equal(first[key][:,:2],second[key])
            plates=json.loads((y/'guide_plates.json').read_text())
            self.assertEqual([(r['plate'],r['cells']) for r in plates],[('A',180),('B',180)])
            with np.load(y/'plate_profiles.npz') as stats:
                np.testing.assert_array_equal(stats['finite_counts'],[[180,140],[180,180]])
                self.assertEqual(stats['means'][0,1],3.)
            self.assertEqual(json.loads((y/'complete.json').read_text())['sampled_cells'],128)


if __name__=='__main__':
    unittest.main()
