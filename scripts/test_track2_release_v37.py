"""Snapshot metadata cannot relax delivery gates or target historical directories."""
from copy import deepcopy
import json
from datetime import datetime,timezone
import unittest
import track2_release_v37 as release


class ReleaseTests(unittest.TestCase):
    def manifest(self):
        return dict(schema_version=37,created_utc=datetime.now(timezone.utc).isoformat(),
            files={},input_hashes={},historical_v36_manifest='0'*64,
            optical_audit_sha256=release.optical.AUDIT_SHA256,presentation={},
            upload_ready=False,upload_performed=False,video_url=None,
            provider_settings_verified=False,licensing_scope_resolved=False,
            phase='unconfirmed',clinical_exposure_margin=None)

    def test_conservative_metadata(self):
        release.manifest_checks(self.manifest())

    def test_readiness_promotion_rejected(self):
        for key in ['upload_ready','upload_performed','provider_settings_verified','licensing_scope_resolved']:
            m=self.manifest();m[key]=True
            with self.subTest(key=key),self.assertRaises(ValueError):release.manifest_checks(m)

    def test_historical_locations_protected(self):
        for version in [19,21,29,31,32,33,34,35,36]:
            with self.subTest(version=version),self.assertRaises(ValueError):
                release.location(release.ROOT/f'results/feat009/jvv7_track2_research_v{version}')

    def test_outside_snapshot_root_rejected(self):
        with self.assertRaises(ValueError):release.location(release.ROOT/'notes/replacement')


class InteractiveReceiptTests(unittest.TestCase):
    def setUp(self):
        self.audit=json.loads((release.ROOT/'notes/track2-demo-audit-v37.json').read_text())

    def test_audit_dependencies_do_not_bind_mutable_current_routes(self):
        mutable={'scripts/check_track2_harness.py','scripts/audit_track2_harness.py',
                 'notes/track2-current.json','AGENTS.md','README.md','session-handoff.md','feature_list.json'}
        self.assertFalse(mutable & set(self.audit['public_input_sha256']))
        self.assertIn('scripts/audit_track2_public_v37.py',self.audit['public_input_sha256'])

    def test_receipts_pass(self):
        self.assertFalse(release.interactive_checks(self.audit)['clinical_validation'])

    def test_missing_bound_source_rejected(self):
        self.audit['public_input_sha256'].pop('scripts/track2_falsification_v21.py')
        with self.assertRaisesRegex(ValueError,'omits required'):release.interactive_checks(self.audit)

    def test_synthetic_pass_cannot_become_clinical_or_recorded(self):
        for field in ['clinical_validation','recording_created','external_adoption_measured','policy_validity_established']:
            a=deepcopy(self.audit);a[field]=True
            with self.subTest(field=field),self.assertRaises(ValueError):release.interactive_checks(a)

    def test_missing_cue_or_unsafe_download_rejected(self):
        a=deepcopy(self.audit);a['browser_checks']['prompter']['checks']['timing'].pop()
        with self.assertRaisesRegex(ValueError,'cue drift'):release.interactive_checks(a)
        a=deepcopy(self.audit);a['browser_checks']['demo']['checks']['download']['decision']['clinical_recommendation']=True
        with self.assertRaisesRegex(ValueError,'Clinical demo'):release.interactive_checks(a)

if __name__=='__main__':unittest.main()
