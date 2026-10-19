"""An empty public export shard must not drop or alter neighboring observations."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import track2_optical_prepare_v35 as core
import track2_optical_prepare_v36 as repair


class EmptyShardTests(unittest.TestCase):
    def test_empty_shard_preserved_and_merge_identical_to_nonempty_data(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'inputs/interphase';source.mkdir(parents=True)
            frame=pd.DataFrame(dict(plate=['A','A'],well=['A1','A1'],tile=[1,1],label=[1,2],
                gene_symbol_0=['BUB1B']*2,group_0=['targeting']*2,sgRNA_0=['ACGT']*2,
                cell_area=[2.,4.],nucleus_area=[1.,np.nan]))
            jobs=[]
            for i,data in enumerate([frame,frame.iloc[:0]]):
                p=source/f'part.{i}.parquet';pq.write_table(pa.Table.from_pandas(data,preserve_index=False),p)
                row=dict(label=p.name,dataFile=dict(id=i,filesize=p.stat().st_size,
                    checksum=dict(value=hashlib.md5(p.read_bytes()).hexdigest())))
                jobs.append((str(root),'interphase',row,['cell_area','nucleus_area']))
            partial=root/'prepared-v35/interphase/shards/1';partial.mkdir(parents=True)
            (partial/'failed-stage.txt').write_text('preserve this incomplete output')
            with patch.object(core,'MIN_FREE_BYTES',0),patch.object(repair,'MIN_FREE_BYTES',0):
                receipts=[repair.prepare_file(j) for j in jobs]
                self.assertEqual(repair.prepare_file(jobs[1]),receipts[1])
                with contextlib.redirect_stdout(io.StringIO()):
                    core.merge(root,'interphase',jobs[0][3],receipts)
            target=root/'prepared-v35/interphase'
            self.assertTrue((root/'outputs/preparation-v36-preserved/interphase/1/failed-stage.txt').is_file())
            self.assertEqual(receipts[1]['cells'],0)
            with np.load(target/'full_profiles.npz') as a:
                np.testing.assert_array_equal(a['sums'],[[6.,1.]])
                np.testing.assert_array_equal(a['finite_counts'],[[2,1]])
            done=json.loads((target/'complete.json').read_text())
            self.assertEqual((done['cells'],done['guides'],done['sampled_cells']),(2,1,2))
            np.testing.assert_array_equal(np.load(target/'shards/1/sample_x.npy').shape,(0,2))


if __name__=='__main__':unittest.main()
