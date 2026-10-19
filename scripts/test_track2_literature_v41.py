"""Regression tests for the public v41 literature-refresh provenance and scope limits."""
from copy import deepcopy
from pathlib import Path
import hashlib,json,tempfile,unittest
import check_track2_literature_v41 as checker


class LiteratureTests(unittest.TestCase):
    def setUp(self):
        self.note=(checker.ROOT/'notes/track2-literature-v41.md').read_text()
        self.audit=json.loads((checker.ROOT/'notes/track2-literature-audit-v41.json').read_text())

    def test_public_sources_and_counts_are_immutable(self):
        result=checker.check()
        self.assertEqual((result['searches'],result['selected_sources'],result['public_receipts']),(5,14,21))
        self.assertEqual(result["repository_bytes"],1670961)
        self.assertEqual((result['drug_dispositions_changed'],result['biological_validation'],
                          result['full_text_systematic_review']),(False,False,False))

    def test_receipt_hash_drift_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'sources').mkdir()
            for path in (checker.SOURCE_DIR).iterdir():
                if path.is_file():(root/'sources'/path.name).write_bytes(path.read_bytes())
            (root/'sources'/'pubmed-mva-bub1b-2025-2026-search.json').write_text('{}')
            result=checker.check.__globals__['require']
            # swap constants through a copied copy is harder; call public_path-like with patched digest by copying original module
            import importlib.util
            spec=importlib.util.spec_from_file_location('mutated',checker.__file__)
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            module.ROOT=root;module.SOURCE_DIR=root/'sources'
            with self.assertRaises(AssertionError):module.check()

    def test_selected_sources_must_include_new_bubr1_architecture_and_injury_papers(self):
        dois={x['doi'] for x in self.audit['selected_sources']}
        expected={'10.1038/s42003-026-10384-9','10.1093/nar/gkaf1517','10.1038/s41467-026-70521-0'}
        self.assertEqual(expected,dois&expected)

    def test_note_does_not_promote_a_drug_or_subject_identity(self):
        normalized=checker.re.sub(r'\s+',' ',self.note).lower()
        for phrase in ['proband01','wgs_ex2312012','everolimus is promoted','nad/sirt2 is promoted','hcq is reopened']:
            self.assertNotIn(phrase,normalized)

    def test_search_coverage_is_declared_not_exhaustive(self):
        self.assertIn('not exhaustive full-text systematic review',str(self.audit['limitations']).lower())


if __name__=='__main__':unittest.main()
