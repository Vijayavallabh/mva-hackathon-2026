import copy
import json
from pathlib import Path
import subprocess
import unittest
import track2_demo_v37 as demo
import track2_falsification_v21 as policy
import build_track2_demo_v37 as builder


class TeachingCases(unittest.TestCase):
    def setUp(self):
        self.definition=json.loads((demo.ROOT/'notes/track2-demo-cases-v37.json').read_text())
        self.current=json.loads((demo.ROOT/'notes/track2-decision-contract-v21.json').read_text())

    def test_fixed_cases_and_shortcut_ablation(self):
        result=demo.run()
        self.assertEqual((result['cases'],result['synthetic_cases'],result['current_decision']),(18,17,'HOLD'))
        self.assertEqual(result['shortcut_advances_rejected_by_policy'],{'benefit_only_advance':11,'benefit_and_viability_advance':9})
        self.assertFalse(result['clinical_validation'])

    def test_survivor_ratio_and_missingness_do_not_imply_benefit(self):
        r=demo.run();v,d=r['outcomes']['vehicle'],r['outcomes']['drug']
        self.assertLess(d['error_fraction'],v['error_fraction'])
        self.assertLess(d['observed_useful_fraction'],v['observed_useful_fraction'])
        self.assertAlmostEqual(r['missingness_difference_bounds'][0],-.25)
        self.assertAlmostEqual(r['missingness_difference_bounds'][1],-.10)
        self.assertFalse(r['missingness_bounds_are_confidence_intervals'])

    def test_absent_divisions_remain_missing(self):
        arm=dict(accurate_viable=0,erroneous_division=0,death=5,arrest=5,slippage=0,missing=0)
        self.assertIsNone(demo.denominator(arm)['error_fraction'])
        for value in [-1,True,1.5]:
            arm['death']=value
            with self.assertRaises(ValueError):demo.denominator(arm)

    def test_exact_embedded_sources(self):
        self.assertEqual(builder.rendered(),(demo.ROOT/'notes/track2-demo-v37.html').read_text())

    def test_javascript_matches_python_on_cases_and_perturbations(self):
        rows=demo.materialize(self.definition,self.current)
        records=[r['record'] for r in rows]
        base=self.definition['base_synthetic_record']
        for gate in policy.GATES:
            for state in ['unknown','fail']:
                r=copy.deepcopy(base);r['gates'][gate]=state;records.append(r)
        for target in ['benefit',*policy.HARMS]:
            for interval in [None,[-1,1],[2,2],[3,4],[-3,4]]:
                r=copy.deepcopy(base);e=r['benefit'] if target=='benefit' else r['harms'][target];e['interval']=interval;records.append(r)
            r=copy.deepcopy(base);e=r['benefit'] if target=='benefit' else r['harms'][target];e['margin']=None;records.append(r)
        for flag in [None,True,False]:
            r=copy.deepcopy(base);r['safety_stop_observed']=flag;records.append(r)
        code="require('./scripts/track2_demo_v37.js');let s='';process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>process.stdout.write(JSON.stringify(JSON.parse(s).map(Track2Demo.decide))));"
        out=subprocess.run(['node','-e',code],cwd=demo.ROOT,input=json.dumps(records),text=True,capture_output=True,check=True)
        self.assertEqual(json.loads(out.stdout),[policy.decide(r) for r in records])
        self.assertEqual(len(records),83)

    def test_browser_policy_rejects_invalid_records(self):
        base=self.definition['base_synthetic_record'];bad=[]
        for field,value in [('scope','patient_treatment'),('schema_version',99),('safety_stop_observed',1),('evidence_kind','not_measured')]:
            r=copy.deepcopy(base);r[field]=value;bad.append(r)
        for value in [True,'3',0,-1]:
            r=copy.deepcopy(base);r['benefit']['margin']=value;bad.append(r)
        for interval in [[5,3],[True,5],[1],[1,2,3]]:
            r=copy.deepcopy(base);r['benefit']['interval']=interval;bad.append(r)
        for r in bad:
            with self.assertRaises(ValueError):policy.decide(r)
        code="require('./scripts/track2_demo_v37.js');let s='';process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>process.stdout.write(JSON.stringify(JSON.parse(s).map(r=>{try{Track2Demo.decide(r);return false}catch{return true}}))));"
        out=subprocess.run(['node','-e',code],cwd=demo.ROOT,input=json.dumps(bad),text=True,capture_output=True,check=True)
        self.assertEqual(json.loads(out.stdout),[True]*len(bad))


if __name__=='__main__':unittest.main()
