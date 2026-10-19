"""A new presentation must preserve history and cannot invent recording evidence."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import unittest
import track2_release_v39 as release


class ReleaseTests(unittest.TestCase):
    def manifest(self):
        return dict(schema_version=39, created_utc=datetime.now(timezone.utc).isoformat(),
                    files={}, input_hashes={}, historical_v37_manifest='0'*64,
                    optical_audit_sha256=release.optical.AUDIT_SHA256, presentation={},
                    upload_ready=False, upload_performed=False, video_url=None,
                    provider_settings_verified=False, licensing_scope_resolved=False,
                    phase='unconfirmed', clinical_exposure_margin=None)

    def test_metadata_and_historical_input_preservation(self):
        release.manifest_checks(self.manifest())
        self.assertTrue(release.historical.INPUTS <= release.INPUTS)
        self.assertIn('notes/track2-demo-v37.html', release.FILES.values())
        self.assertIn('notes/track2-qualification-amendment-v39.md', release.FILES.values())

    def test_delivery_or_scientific_promotion_rejected(self):
        for key, value in [('upload_ready', True), ('upload_performed', True),
                           ('provider_settings_verified', True), ('licensing_scope_resolved', True),
                           ('phase', 'trans'), ('clinical_exposure_margin', 10),
                           ('video_url', 'https://example.org/unrecorded')]:
            record = self.manifest(); record[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                release.manifest_checks(record)

    def test_historical_directories_protected(self):
        for version in [19, 21, 29, 31, 32, 34, 35, 36, 37, 38]:
            with self.subTest(version=version), self.assertRaises(ValueError):
                release.location(release.ROOT / f'results/feat009/jvv7_track2_research_v{version}')

    def test_recording_audit_rejects_hidden_cues_missing_inputs_or_false_completion(self):
        audit = json.loads((release.ROOT / 'notes/track2-prompter-audit-v39.json').read_text())
        release.recording_checks(audit)
        changes = []
        missing = deepcopy(audit); missing['public_input_sha256'].pop('notes/track2-pitch-v39.md')
        changes.append(missing)
        hidden = deepcopy(audit); hidden['browser_checks']['checks']['mobileCues'][1]['top'] = 0
        changes.append(hidden)
        for field in ['recording_created', 'runtime_measured', 'independent_review']:
            altered = deepcopy(audit); altered[field] = True; changes.append(altered)
        for altered in changes:
            with self.assertRaises(ValueError):
                release.recording_checks(altered)


if __name__ == '__main__':
    unittest.main()
