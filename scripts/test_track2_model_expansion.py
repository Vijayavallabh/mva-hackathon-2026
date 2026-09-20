import copy
import json
from pathlib import Path
import tempfile
import unittest
from track2_model_expansion import aggregate, MODELS


class ExpansionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.paths=[]
        plan=json.loads(Path('notes/track2-model-expansion-plan.json').read_text())
        for index,model in enumerate(MODELS):
            rows=[dict(window=w['name'],variant=v['variant'],group=v['group'],score=float(index))
                  for w in plan['windows'] for v in plan['controls']+[dict(variant='N1002K',group='candidate')]]
            p=Path(self.temp.name)/f'{model}.json'
            p.write_text(json.dumps(dict(model=model,plan_sha256='plan',script_sha256='script',rows=rows,
                                        gate={'pass':index!=2})))
            self.paths.append(p)

    def alter(self,index,fn):
        p=self.paths[index];x=json.loads(p.read_text());fn(x);p.write_text(json.dumps(x))

    def test_ensemble_includes_failed_control_checkpoint(self):
        result=aggregate(self.paths)
        self.assertEqual(result['esm1v_five_checkpoint_ensemble'][0]['mean'],2.0)
        self.assertEqual(len(result['models']),7)
        self.assertFalse(result['clinical_classification'])

    def test_missing_checkpoint_rejected(self):
        with self.assertRaises(ValueError): aggregate(self.paths[:-1])

    def test_repeated_checkpoint_rejected(self):
        with self.assertRaises(ValueError): aggregate(self.paths[:-1]+[self.paths[0]])

    def test_duplicate_score_not_silently_averaged(self):
        self.alter(2,lambda x:x['rows'].__setitem__(0,copy.deepcopy(x['rows'][1])))
        with self.assertRaises(ValueError): aggregate(self.paths)

    def test_missing_score_rejected(self):
        self.alter(2,lambda x:x['rows'].pop())
        with self.assertRaises(ValueError): aggregate(self.paths)

    def test_nonfinite_score_rejected(self):
        self.alter(2,lambda x:x['rows'][0].update(score=float('nan')))
        with self.assertRaises(ValueError): aggregate(self.paths)

    def test_changed_plan_rejected(self):
        self.alter(2,lambda x:x.update(plan_sha256='changed'))
        with self.assertRaises(ValueError): aggregate(self.paths)

    def test_changed_implementation_rejected(self):
        self.alter(2,lambda x:x.update(script_sha256='changed'))
        with self.assertRaises(ValueError): aggregate(self.paths)


if __name__=='__main__':unittest.main()
