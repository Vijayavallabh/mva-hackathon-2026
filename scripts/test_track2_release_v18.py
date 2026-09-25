from copy import deepcopy
import json
import unittest
import track2_release_v18 as release


class V18ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.audits = [json.loads((release.ROOT/f'notes/{n}').read_text()) for n in
                      ['track2-v18-render-audit.json','track2-v18-documents-audit.json','track2-public-review-v18.json']]

    def test_current_presentation_and_exports(self):
        r = release.scientific_checks()
        self.assertEqual((r['slides'], r['narration_words'], r['exports']['report_pages']), (8,334,6))

    def test_changed_export_sources_rejected(self):
        for index, key in [(0,'source_sha256'),(0,'renderer_sha256'),(2,'script_sha256')]:
            a=deepcopy(self.audits); a[index][key]='0'*64
            with self.subTest(key=key),self.assertRaises(ValueError):release.audit_checks(*a)

    def test_truncated_methods_or_modified_template_rejected(self):
        for key,value in [('answer_cells',['B9']),('official_questions_unchanged',False),
                          ('track1_values_and_cell_styles_preserved',False),('abstract_words',501),('upload_ready',True)]:
            a=deepcopy(self.audits);a[1]['export'][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):release.audit_checks(*a)

    def test_clipping_and_false_isolation_rejected(self):
        a=deepcopy(self.audits);a[0]['slides'][0]['outside']=['clipped']
        with self.assertRaises(ValueError):release.audit_checks(*a)
        a=deepcopy(self.audits);a[2]['project_environment_used']=True
        with self.assertRaises(ValueError):release.audit_checks(*a)

    def test_all_earlier_inputs_and_names_protected(self):
        self.assertTrue(release.historical.INPUTS <= release.INPUTS)
        for n in range(1,18):
            with self.subTest(n=n),self.assertRaises(ValueError):
                release.location(release.ROOT/f'results/feat009/jvv7_track2_research_v{n}')

    def test_manifest_never_attests_unknown_terms_or_delivery(self):
        m={key:None for key in release.FIELDS}
        m.update(schema_version=18,created_utc='2026-09-24T00:00:00+00:00',phase='unconfirmed',
                 upload_ready=False,upload_performed=False,provider_settings_verified=False,licensing_scope_resolved=False)
        release.manifest_checks(m)
        for key in ['upload_ready','upload_performed','provider_settings_verified','licensing_scope_resolved']:
            changed=deepcopy(m);changed[key]=True
            with self.subTest(key=key),self.assertRaises(ValueError):release.manifest_checks(changed)


if __name__ == '__main__': unittest.main()
