import unittest
from copy import deepcopy
import csv
import io
import json
from pathlib import Path
import tarfile
import tempfile
from track2_crossfit_v29 import split_genes
from check_track2_orthogonal_v29 import validate_structural, validate_expression
from archive_track2_orthogonal_v29 import verify

ROOT=Path(__file__).resolve().parents[1]


class HeldOutTargetTests(unittest.TestCase):
    def test_train_and_reference_genes_disjoint_in_both_modalities(self):
        modalities=[['BUB1B','MTOR']+[f'G{i}' for i in range(70)],
                    ['BUB1B','MTOR']+[f'G{i}' for i in range(15,100)]]
        for seed in [17,41,73,101]:
            for fold in range(5):
                training,evaluation=set(),set()
                for names in modalities:
                    tr,ev=split_genes(names,seed,fold,['BUB1B','MTOR'])
                    training.update(names[i] for i in tr)
                    evaluation.update(names[i] for i in ev)
                    self.assertTrue({0,1}.issubset(ev))
                self.assertFalse(training&evaluation)

    def test_reference_coverage_exactly_once_per_partition(self):
        names=['BUB1B','MTOR']+[f'G{i}' for i in range(100)]
        for seed in [17,41,73,101]:
            seen=[]
            for fold in range(5):
                _,ev=split_genes(names,seed,fold,['BUB1B','MTOR'])
                seen.extend(names[i] for i in ev if i>1)
            self.assertEqual(sorted(seen),sorted(names[2:]))

    def test_gene_split_independent_of_modality_row_order(self):
        names=['BUB1B','MTOR','A','B','C','D']
        for fold in range(5):
            _,one=split_genes(names,17,fold,['BUB1B','MTOR'])
            reverse=names[::-1];_,two=split_genes(reverse,17,fold,['BUB1B','MTOR'])
            self.assertEqual({names[i] for i in one},{reverse[i] for i in two})


class PublishedEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        read=lambda name:json.loads((ROOT/'notes'/name).read_text())
        cls.sp=read('track2-structural-plan-v29.json');cls.ep=read('track2-crossfit-plan-v29.json')
        cls.s=read('track2-structural-results-v29.json');cls.e=read('track2-crossfit-results-v29.json')
        with (ROOT/'notes/track2-structural-probabilities-v29.tsv').open() as f:cls.rows=list(csv.DictReader(f,delimiter='\t'))

    def test_complete_published_records_pass(self):
        validate_structural(self.sp,self.s,self.rows);validate_expression(self.ep,self.e)

    def test_missing_amino_acid_or_context_rejected(self):
        for rows in [self.rows[:-1],self.rows[:-20]]:
            with self.subTest(length=len(rows)),self.assertRaises(ValueError):validate_structural(self.sp,self.s,rows)

    def test_failed_controls_cannot_be_promoted(self):
        result=deepcopy(self.s);result['comparisons'][0]['primary_controls_pass']=True
        with self.assertRaisesRegex(ValueError,'Primary gate'):validate_structural(self.sp,result,self.rows)
        result=deepcopy(self.s);result['expanded_controls_pass']=24
        with self.assertRaises(ValueError):validate_structural(self.sp,result,self.rows)

    def test_candidate_score_must_match_probabilities(self):
        result=deepcopy(self.s);result['comparisons'][0]['candidate_log_odds']=0.
        with self.assertRaisesRegex(ValueError,'Candidate drift'):validate_structural(self.sp,result,self.rows)

    def test_biological_promotion_rejected(self):
        for field in ['functional_validation','drug_ranking_changed']:
            result=deepcopy(self.s);result[field]=True
            with self.subTest(field=field),self.assertRaises(ValueError):validate_structural(self.sp,result,self.rows)

    def test_missing_qc_query_cannot_be_zero_filled(self):
        result=deepcopy(self.e)
        row=next(r for r in result['records'] if r['cell']=='MCF7' and r['quality']=='crispr_quality_pass_only')
        rep=row['folds'][0]['representations']['all978']
        rep['missing']=[r for r in rep['missing'] if r['gene']!='BUB1B']
        rep['queries'].append(dict(gene='BUB1B',correlation=0.,rnai_rank=1,crispr_rank=1,crispr_profiles=1,crispr_quality_pass=1))
        with self.assertRaisesRegex(ValueError,'Missing MCF7 query fabricated'):validate_expression(self.ep,result)

    def test_failed_quality_cannot_enter_passing_only_view(self):
        result=deepcopy(self.e)
        row=next(r for r in result['records'] if r['quality']=='crispr_quality_pass_only')
        row['folds'][0]['representations']['all978']['queries'][0]['crispr_quality_pass']=0
        with self.assertRaisesRegex(ValueError,'QC leakage'):validate_expression(self.ep,result)

    def test_rank_requires_its_own_reference_denominator(self):
        result=deepcopy(self.e);view=result['records'][0]['folds'][0]['representations']['all978']
        view['queries'][0]['crispr_rank']=view['crispr_reference_genes']+1
        with self.assertRaisesRegex(ValueError,'Rank denominator'):validate_expression(self.ep,result)

    def test_missing_or_leaking_fold_rejected(self):
        result=deepcopy(self.e);result['records'][0]['folds'][0]['train_test_disjoint']=False
        with self.assertRaisesRegex(ValueError,'Projection validity'):validate_expression(self.ep,result)
        result=deepcopy(self.e);result['records'][0]['folds'].pop()
        with self.assertRaisesRegex(ValueError,'Fold coverage'):validate_expression(self.ep,result)


class ArchiveBoundaryTests(unittest.TestCase):
    def test_traversal_duplicate_and_symlink_members_rejected(self):
        cases=[('traversal',['../escape'],False),('duplicate',['inputs/a','inputs/a'],False),('symlink',['inputs/a'],True)]
        for label,names,symlink in cases:
            with self.subTest(label=label),tempfile.TemporaryDirectory() as temp:
                root=Path(temp);archive=root/'bad.tar.gz'
                with tarfile.open(archive,'w:gz') as tar:
                    for name in names:
                        info=tarfile.TarInfo(name)
                        if symlink:info.type=tarfile.SYMTYPE;info.linkname='/etc/passwd';tar.addfile(info)
                        else:info.size=1;tar.addfile(info,io.BytesIO(b'x'))
                with self.assertRaises(ValueError):verify(archive,root/'out')
                self.assertFalse((root/'out').exists())


if __name__=='__main__':unittest.main()
