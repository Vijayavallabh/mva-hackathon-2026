"""Snapshot metadata cannot relax delivery gates or target historical directories."""
from copy import deepcopy
from datetime import datetime,timezone
import unittest
import track2_release_v36 as release


class ReleaseTests(unittest.TestCase):
    def manifest(self):
        return dict(schema_version=36,created_utc=datetime.now(timezone.utc).isoformat(),
            files={},input_hashes={},historical_v34_manifest='0'*64,
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
        for version in [19,21,29,31,32,33,34,35]:
            with self.subTest(version=version),self.assertRaises(ValueError):
                release.location(release.ROOT/f'results/feat009/jvv7_track2_research_v{version}')

    def test_outside_snapshot_root_rejected(self):
        with self.assertRaises(ValueError):release.location(release.ROOT/'notes/replacement')


if __name__=='__main__':unittest.main()
