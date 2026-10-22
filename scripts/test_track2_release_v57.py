"""A v43 literature-integrated presentation must preserve history and evidence boundaries."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import unittest
import track2_release_v57 as release
import check_track2_literature_v45 as literature


class ReleaseTests(unittest.TestCase):
    def manifest(self):
        return dict(schema_version=47, created_utc=datetime.now(timezone.utc).isoformat(),
                    files={}, input_hashes={}, historical_v40_manifest='0'*64,
                    optical_audit_sha256=release.optical.AUDIT_SHA256, presentation={},
                    upload_ready=False, upload_performed=False, video_url=None,
                    provider_settings_verified=False, licensing_scope_resolved=False,
                    phase='unconfirmed', clinical_exposure_margin=None)

    def test_v40_inputs_and_literature_addendum_are_bound(self):
        release.manifest_checks(self.manifest())
        self.assertTrue(release.historical.INPUTS <= release.INPUTS)
        self.assertIn('notes/track2-literature-v45.md', release.FILES.values())
        self.assertIn('notes/track2-literature-audit-v45.json', release.FILES.values())
        self.assertIn('scripts/check_track2_literature_v45.py', release.INPUTS)
        audit=json.loads((release.ROOT/'notes/track2-literature-audit-v45.json').read_text())
        self.assertTrue(all(source['receipt'] in release.INPUTS
                            for source in audit['selected_sources'] if source['receipt']))
        self.assertIn('notes/track2-report-v57.md', release.FILES.values())
        self.assertIn('notes/track2-slides-v57.html', release.FILES.values())

    def test_delivery_or_scientific_promotion_rejected(self):
        for key, value in [('upload_ready', True), ('upload_performed', True),
                           ('provider_settings_verified', True), ('licensing_scope_resolved', True),
                           ('phase', 'trans'), ('clinical_exposure_margin', 10),
                           ('video_url', 'https://example.org/unrecorded')]:
            record=self.manifest();record[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):
                release.manifest_checks(record)

    def test_historical_directories_including_v40_protected(self):
        for version in [19,21,29,31,32,34,35,36,37,38,39,40]:
            with self.subTest(version=version),self.assertRaises(ValueError):
                release.location(release.ROOT/f'results/feat009/jvv7_track2_research_v{version}')

    def test_v43_checks_preserve_literature_boundaries(self):
        result=release.scientific_checks()
        self.assertEqual(result['presentation_version'],57)
        self.assertEqual(result['literature_v45'],
                         {'passed':True,'version':45,'searches':7,'selected_sources':4,
                          'public_receipts':14,'repository_bytes':94130,
                          'subject_data_read':False,'drug_dispositions_changed':False,
                          'biological_validation':False,'full_text_systematic_review':False,'new_gpu_campaign':False})
        self.assertEqual(result['exports']['render_pdf_pages'],9)
        self.assertEqual(result['exports']['report_pdf_title'],'jvv7 · Track 2 report v57')
        self.assertGreaterEqual(result['exports']['minimum_checked_text_contrast'],4.5)
        self.assertFalse(result['exports']['independent_visual_review'])
        self.assertFalse(result['recording']['runtime_measured'])

    def test_literature_scope_promotion_rejected(self):
        audit=release.ROOT/'notes/track2-literature-audit-v45.json'
        original=audit.read_text()
        changes=[]
        record=json.loads(original);record['disposition_changes']['everolimus']='promoted';changes.append(record)
        record=json.loads(original);record['biological_validation']=True;changes.append(record)
        record=json.loads(original);record['full_text_systematic_review']=True;changes.append(record)
        record=json.loads(original);record['selected_sources']=[];changes.append(record)
        try:
            for altered in changes:
                audit.write_text(json.dumps(altered,indent=2))
                with self.assertRaises(AssertionError):literature.check()
        finally:
            audit.write_text(original)


if __name__=='__main__':unittest.main()
