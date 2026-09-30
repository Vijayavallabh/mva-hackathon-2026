"""Reject material scientific overstatements in the v25 public evidence."""
from copy import deepcopy
import csv
import io
import json
import unittest
from pathlib import Path
import check_track2_crispr_v25 as checker


class PublicCrisprChecks(unittest.TestCase):
    def setUp(self):
        root=checker.ROOT
        self.args=[json.loads((root/f'notes/track2-crispr-{s}-v25.json').read_text()) for s in ['results','summary','continuity','register']]
        self.args += [list(csv.DictReader(io.StringIO((root/'notes/track2-crispr-everolimus-v25.tsv').read_text()),delimiter='\t')),
                      (root/'notes/track2-crispr-v25.md').read_text()]

    def test_public_check(self):self.assertTrue(checker.check()['passed'])

    def test_profiles_are_not_guides(self):
        self.args[1]['bub1b']['guides']=31
        with self.assertRaisesRegex(ValueError,'guide qualification'):checker.validate(*self.args)

    def test_more_scores_cannot_become_more_evidence(self):
        self.args[1]['total_comparisons']+=1
        with self.assertRaisesRegex(ValueError,'compute count'):checker.validate(*self.args)

    def test_favorable_ht29_cannot_disappear(self):
        self.args[1]['bub1b']['orthogonal_records']=[r for r in self.args[1]['bub1b']['orthogonal_records'] if r['cell']!='HT29']
        with self.assertRaises(ValueError):checker.validate(*self.args)

    def test_discordant_contexts_cannot_be_flipped(self):
        row=next(r for r in self.args[1]['bub1b']['orthogonal_records'] if r['cell']=='MCF7')
        row['correlation']=.2
        with self.assertRaisesRegex(ValueError,'discordant'):checker.validate(*self.args)

    def test_drug_qc_does_not_qualify_query(self):
        for r in self.args[4]:
            if r['gene']=='BUB1B' and r['compound_id']=='BRD-K13514097' and r['quality_pass']=='True':r['query_quality_passes']='1'
        with self.assertRaisesRegex(ValueError,'query QC'):checker.validate(*self.args)

    def test_regrouped_wells_are_not_independent_replication(self):
        self.args[2]['regrouped_profiles']=0
        with self.assertRaisesRegex(ValueError,'continuity'):checker.validate(*self.args)

    def test_safety_and_exposure_cannot_be_promoted(self):
        for i,key,value in [(1,'clinical_exposure_margin',2),(3,'rescue_priority','everolimus'),(0,'wet_lab_performed',True)]:
            a=deepcopy(self.args);a[i][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):checker.validate(*a)

    def test_sampling_cannot_be_called_saturation(self):
        self.args[-1]=self.args[-1].replace('not sustained saturation','sustained saturation')
        with self.assertRaisesRegex(ValueError,'limitation'):checker.validate(*self.args)


if __name__=='__main__':unittest.main()
