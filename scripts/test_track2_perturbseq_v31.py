#!/usr/bin/env python3
"""Regression guards for stratified independence and public HDF5 decoding."""
import unittest
from copy import deepcopy
import json
from pathlib import Path
import numpy as np
from track2_perturbseq_v31 import stratified_half
from check_track2_perturbseq_v31 import validate_results


class Splits(unittest.TestCase):
    def test_strata_are_balanced_and_all_cells_accounted_for(self):
        strata=np.repeat(np.arange(50),np.arange(1,51))
        side=stratified_half(strata,np.random.default_rng(123))
        self.assertEqual(set(side),{0,1})
        for s in np.unique(strata):
            counts=np.bincount(side[strata==s],minlength=2)
            self.assertLessEqual(abs(int(counts[0])-int(counts[1])),1)
        self.assertEqual(len(side),len(strata))

    def test_singletons_are_not_all_in_one_half(self):
        side=stratified_half(np.arange(1000),np.random.default_rng(31))
        self.assertTrue(400<int(side.sum())<600)

    def test_seed_replays_and_partitions_change(self):
        strata=np.repeat(np.arange(10),50)
        a=stratified_half(strata,np.random.default_rng(8))
        b=stratified_half(strata,np.random.default_rng(8))
        c=stratified_half(strata,np.random.default_rng(9))
        np.testing.assert_array_equal(a,b)
        self.assertFalse(np.array_equal(a,c))

    def test_ordering_does_not_make_contiguous_halves(self):
        strata=np.zeros(1000,dtype=int)
        side=stratified_half(strata,np.random.default_rng(11))
        self.assertTrue(200<int(side[:500].sum())<300)
        self.assertEqual(int(side.sum()),500)


class EvidenceGuards(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((Path(__file__).resolve().parents[1]/'notes/track2-perturbseq-results-v31.json').read_text())

    def test_complete_results_pass(self):
        self.assertEqual(validate_results(self.data)['gpu_correlations'],27628823832)

    def test_cannot_promote_rescue_or_confidence(self):
        for key in ['biological_validation','drug_ranking_changed','phase_confirmed',
                    'conditional_ranges_are_biological_confidence_intervals','neural_model_inference']:
            j=deepcopy(self.data);j[key]=True
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'promotion'):validate_results(j)

    def test_cannot_drop_an_unfavorable_query(self):
        self.data['split_results']=[r for r in self.data['split_results'] if r['gene']!='BUB1B']
        with self.assertRaisesRegex(ValueError,'Incomplete'):validate_results(self.data)

    def test_absence_cannot_become_zero(self):
        self.data['missing_queries']['rpe1'].remove('RICTOR')
        with self.assertRaisesRegex(ValueError,'Missing query'):validate_results(self.data)

    def test_core_controls_cannot_be_called_independent(self):
        self.data['all_controls_sensitivity']='replicated with independent controls'
        with self.assertRaisesRegex(ValueError,'selected-control'):validate_results(self.data)

    def test_denominator_and_range_are_checked(self):
        self.data['split_results'][0]['forward_rank']['maximum']=100000
        with self.assertRaisesRegex(ValueError,'denominator'):validate_results(self.data)

    def test_false_replication_count_rejected(self):
        self.data['query_metadata']['rpe1']['query_metadata'][0]['guide_pairs']*=2
        with self.assertRaisesRegex(ValueError,'False guide replication'):validate_results(self.data)

    def test_workload_is_derived_not_accepted_as_a_claim(self):
        self.data['compute']['gpu_correlations']+=1
        with self.assertRaisesRegex(ValueError,'workload'):validate_results(self.data)

    def test_null_tail_resolution_is_checked(self):
        self.data['null_results'][0]['descriptive_tail']=0
        with self.assertRaisesRegex(ValueError,'null arithmetic'):validate_results(self.data)

    def test_partition_influence_cannot_become_independent_validation(self):
        self.data['partition_sensitivity'][0]['reference_includes_retained_cells']=False
        with self.assertRaisesRegex(ValueError,'held-out'):validate_results(self.data)


if __name__=='__main__':unittest.main()
