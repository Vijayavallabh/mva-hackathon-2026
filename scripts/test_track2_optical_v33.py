#!/usr/bin/env python3
"""Regression checks for optical follow-up identity, sampling and provenance."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from track2_optical_prepare_v33 import (QUERIES, cell_hashes, gene_split, merge,
                                      phenotype_columns, prepare_file, sample_indices)


class OpticalPreparationTests(unittest.TestCase):
    def source(self, root, file_id, first, count, guide='ACGT', gene='BUB1B', missing=False):
        path = root / 'inputs/mitotic' / f'part.{file_id}.parquet'
        path.parent.mkdir(parents=True, exist_ok=True)
        data = dict(plate=['plateA']*count, well=['A1']*count, tile=[1]*count,
                    label=list(range(first, first+count)), gene_symbol_0=[gene]*count,
                    group_0=['targeting']*count, sgRNA_0=[guide]*count,
                    nucleus_area=np.arange(first, first+count, dtype=float)/100,
                    cell_area=np.full(count, np.nan if missing else 3.0))
        pq.write_table(pa.table(data), path)
        raw = path.read_bytes()
        row = dict(label=path.name, dataFile=dict(id=file_id, filesize=len(raw),
                   checksum=dict(value=hashlib.md5(raw).hexdigest())))
        return row

    def test_identity_columns_and_absolute_coordinates_cannot_enter_model(self):
        names = ['cell_area', 'nucleus_dapi_mean', 'gene_symbol_0', 'cell_0', 'plate',
                 'cell_i', 'nucleus_bounds_0', 'cell_dapi_center_mass_r',
                 'nucleus_dapi_max_location_c', 'class_predict_0', 'nucleus_dapi_mass_displacement']
        schema = pa.schema([(n, pa.float64()) for n in names])
        self.assertEqual(phenotype_columns(schema), ['cell_area', 'nucleus_dapi_mean',
                                                    'nucleus_dapi_mass_displacement'])

    def test_all_queries_are_held_out(self):
        self.assertEqual({gene_split(g) for g in QUERIES}, {'test'})
        self.assertEqual(gene_split('EXAMPLE'), gene_split('EXAMPLE'))

    def test_sampling_is_order_invariant_and_uses_full_identity(self):
        frame = pd.DataFrame(dict(plate=['a']*200, well=['a']*200, tile=[1]*200, label=range(200)))
        full, rank = cell_hashes(frame)
        shuffled = frame.sample(frac=1, random_state=9)
        full2, rank2 = cell_hashes(shuffled)
        self.assertEqual(set(full[sample_indices(rank)].tobytes()[i:i+16] for i in range(0,128*16,16)),
                         set(full2[sample_indices(rank2)].tobytes()[i:i+16] for i in range(0,128*16,16)))
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            cell_hashes(pd.concat([frame, frame.iloc[:1]], ignore_index=True))

    def test_full_counts_survive_sample_cap_and_cross_shard_merge(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            features = ['nucleus_area', 'cell_area']
            rows = [self.source(root, 1, 0, 180), self.source(root, 2, 180, 170)]
            receipts = [prepare_file((str(root), 'mitotic', r, features)) for r in rows]
            merge(root, 'mitotic', features, receipts)
            dest = root / 'prepared/mitotic'
            guides = json.loads((dest / 'guides.json').read_text())
            self.assertEqual(guides[0]['cells'], 350)
            self.assertEqual(np.load(dest / 'sample_x.npy').shape, (128, 2))
            values = np.load(dest / 'full_profiles.npz')
            np.testing.assert_allclose(values['means'][0], [1.745, 3.0], atol=1e-7)
            np.testing.assert_array_equal(values['finite_counts'][0], [350, 350])

    def test_missing_input_feature_remains_missing_in_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row = self.source(root, 1, 0, 30, missing=True)
            r = prepare_file((str(root), 'mitotic', row, ['nucleus_area', 'cell_area']))
            p = root / 'prepared/mitotic/shards/1/summary.npz'
            values = np.load(p)
            self.assertEqual(values['finite_counts'][0,1], 0)
            self.assertEqual(r['cells'], 30)

    def test_source_and_cached_output_tampering_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row = self.source(root, 1, 0, 30)
            job = (str(root), 'mitotic', row, ['nucleus_area', 'cell_area'])
            prepare_file(job)
            p = root / 'prepared/mitotic/shards/1/guides.json'
            p.write_text('[]')
            with self.assertRaisesRegex(ValueError, 'Prepared shard changed'):
                prepare_file(job)

    def test_duplicate_identity_across_shards_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            features = ['nucleus_area', 'cell_area']
            rows = [self.source(root, 1, 0, 30), self.source(root, 2, 29, 30, guide='TGCA')]
            receipts = [prepare_file((str(root), 'mitotic', r, features)) for r in rows]
            with self.assertRaisesRegex(ValueError, 'Duplicate full cell identity across'):
                merge(root, 'mitotic', features, receipts)


if __name__ == '__main__':
    unittest.main()
