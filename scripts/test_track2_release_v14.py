import json
from pathlib import Path
import unittest
from unittest.mock import patch
import track2_release_v14 as release


class IntegratedPresentationTests(unittest.TestCase):
    def setUp(self):
        self.deck=(release.ROOT/'notes/track2-slides-v14.html').read_text()

    def test_aligned_presentation_and_plain_transcript(self):
        checked=release.scientific_checks()
        self.assertEqual((checked['slides'],checked['narration_words']), (9,336))
        self.assertFalse(checked['runtime_measured'])

    def test_critical_claim_removals_are_rejected(self):
        for old in ['All four pass the fixed gate','Disagreement + failed controls',
                    'small engineered-control set','Impaired controls also fold',
                    'BRCA1 benchmark does not validate BUB1B',
                    'AlphaFold3-derived summaries / interpretation modified',
                    'No wet-lab experiments.']:
            with self.subTest(old=old), self.assertRaises(ValueError):
                release.presentation_checks(self.deck.replace(old,'Removed'))

    def test_terms_links_and_citation_required(self):
        for link in ['https://doi.org/10.1038/s41586-024-07487-w',
                     'https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphafold3-output-terms.md',
                     'https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphafold3-Legally-Binding-Terms-of-Use.txt']:
            with self.subTest(link=link),self.assertRaises(ValueError):
                release.presentation_checks(self.deck.replace(link,'https://example.org'))

    def test_trial_estimate_preserved(self):
        with self.assertRaises(ValueError):
            release.presentation_checks(self.deck.replace('HR 0.86','HR 0.20'))

    def test_complete_acknowledgement_required(self):
        with self.assertRaises(ValueError):
            release.presentation_checks(self.deck.replace('We acknowledge their trust in making this Hackathon possible.','Thanks.'))

    def test_active_content_rejected(self):
        with self.assertRaises(ValueError):
            release.presentation_checks(self.deck.replace('</head>','<script>alert(1)</script></head>'))

    def test_all_historical_paths_protected(self):
        for version in range(1,14):
            with self.subTest(version=version),self.assertRaises(ValueError):
                release.location(release.ROOT/f'results/feat009/jvv7_track2_research_v{version}')

    def test_transcript_drift_rejected(self):
        original=Path.read_text
        def modified(path,*args,**kwargs):
            text=original(path,*args,**kwargs)
            return text+'Extra speech.' if path.name=='track2-transcript-v14.txt' else text
        with patch.object(Path,'read_text',modified),self.assertRaisesRegex(ValueError,'transcript drift'):
            release.scientific_checks()

    def test_model_promotion_rejected(self):
        original=Path.read_text
        def modified(path,*args,**kwargs):
            text=original(path,*args,**kwargs)
            if path.name=='track2-latest-model-audit.json':
                data=json.loads(text);data['clinical_validation']=True;return json.dumps(data)
            return text
        with patch.object(Path,'read_text',modified),self.assertRaisesRegex(ValueError,'audit claim drift'):
            release.model_evidence_checks()

    def test_altered_sequence_score_rejected(self):
        original=Path.read_text
        def modified(path,*args,**kwargs):
            text=original(path,*args,**kwargs)
            if path.name=='track2-latest-protein-results.json':
                data=json.loads(text)
                data['models']['ESMC-300M-score']['rows'][0]['score']+=1
                return json.dumps(data)
            return text
        with patch.object(Path,'read_text',modified),self.assertRaisesRegex(ValueError,'binding drift'):
            release.model_evidence_checks()

    def test_terms_and_all_campaigns_packaged(self):
        for name in ['AlphaFold3-Output-Terms.md','Legally-Binding-Terms-of-Use.txt',
                     'esm-results.json','latest-protein-results.json','evo2-20b-results.json',
                     'evo2-40b-results.json','jvv7_track2_transcript_v14.txt']:
            self.assertIn(name,release.FILES)


if __name__=='__main__':unittest.main()
