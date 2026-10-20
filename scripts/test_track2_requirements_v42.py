"""Regression tests for the bounded anonymous v42 requirements refresh."""
import unittest
from copy import deepcopy
from pathlib import Path
import json,tempfile,importlib.util
import check_track2_requirements_v42 as checker


class RequirementsTests(unittest.TestCase):
    def setUp(self):
        self.audit=json.loads((checker.ROOT/'notes/track2-requirements-v42.json').read_text())

    def test_current_public_state_is_preserved(self):
        result=checker.check()
        self.assertEqual((result['official_sources'],result['public_threads'],result['visible_comments'],result['closed_threads']),(7,31,89,16))
        self.assertEqual((result['requirements_changed'],result['anonymous_get_only'],result['upload_ready']),(False,True,False))

    def test_official_hashes_and_thread_hashes_are_bound(self):
        for source in self.audit['official_sources']:
            if 'receipt' not in source: continue
            path=checker.ROOT/source['receipt']
            self.assertEqual(checker.digest(path),source['sha256'])
        for thread in self.audit['community']['threads']:
            path=checker.ROOT/thread['receipt']
            self.assertEqual(checker.digest(path),thread['sha256'])

    def test_thread_32_permission_is_not_a_requirement_change(self):
        thread=next(x for x in self.audit['community']['threads'] if x['num']==32)
        self.assertEqual(thread['visible_comments'],3)
        self.assertEqual(self.audit['material_changes']['new_thread_32_pitch_video_published_example'],True)
        self.assertIn('no script rewrite is mandated before recording', (checker.ROOT/'notes/track2-requirements-review-v42.md').read_text().lower())

    def test_github_synapse_alternative_does_not_change_our_selected_route(self):
        thread=next(x for x in self.audit['community']['threads'] if x['num']==31)
        self.assertEqual(thread['visible_comments'],2)
        self.assertIn('public github remains our selected route', (checker.ROOT/'notes/track2-requirements-review-v42.md').read_text().lower())

    def test_thread_29_routing_and_thread_26_metadata_are_scoped(self):
        self.assertEqual(self.audit['material_changes']['thread_29_participant_correction_irb_consent_routing'],True)
        self.assertEqual(self.audit['material_changes']['thread_26_hash_only_reaction_metadata_change'],True)

    def test_receipt_or_hash_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name);(root/'notes').mkdir();(root/'sources').mkdir()
            for source in self.audit['official_sources']:
                if 'receipt' not in source: continue
                src=checker.ROOT/source['receipt'];dest=root/source['receipt'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(src.read_bytes())
            for thread in self.audit['community']['threads']:
                src=checker.ROOT/thread['receipt'];dest=root/thread['receipt'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(src.read_bytes())
            listing=checker.ROOT/self.audit['community']['listing_receipt'];dest=root/self.audit['community']['listing_receipt'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(listing.read_bytes())
            for path in [checker.AUDIT,checker.REVIEW,checker.BASELINE]:
                dest=root/path.relative_to(checker.ROOT);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(path.read_bytes())
            spec=importlib.util.spec_from_file_location('mutated',checker.__file__);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            module.ROOT=root;module.AUDIT=root/'notes/track2-requirements-v42.json';module.REVIEW=root/'notes/track2-requirements-review-v42.md';module.BASELINE=root/'notes/track2-requirements-v39.json';module.RECEIPTS=root/'sources/public-official-v42'
            altered=(root/'sources/public-official-v42/index-0.json').read_text();(root/'sources/public-official-v42/index-0.json').write_text(altered+' drift')
            with self.assertRaises((AssertionError, json.JSONDecodeError)):module.check()


if __name__=='__main__':unittest.main()
