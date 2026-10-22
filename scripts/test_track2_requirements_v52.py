"""Regression checks for the anonymous v52 requirements refresh."""
import json
import unittest
from pathlib import Path
import check_track2_requirements_v52 as checker

class RequirementsTests(unittest.TestCase):
 def test_refresh_passes_and_adds_no_requirement(self):
  result=checker.check()
  self.assertEqual((result['version'],result['discussions'],result['new_organizer_requirement_found']),(52,32,False))
  self.assertFalse(result['provider_settings_verified'])
  self.assertFalse(result['upload_ready'])

 def test_latest_thread_is_non_submission_pr(self):
  raw=json.loads(Path('sources/public-official-v52/discussion-33.json').read_text())
  self.assertEqual(raw['title'],'Update README.md')
  self.assertTrue(raw['isPullRequest'])
  self.assertEqual(raw['events'][1]['data']['oid'],'7b9e5bc54181edbaeeee641986caf9585ecb74dd')

 def test_thread_32_permits_challenge_case_report(self):
  raw=json.loads(Path('sources/public-official-v52/discussion-32.json').read_text())
  organizer=[e for e in raw['events'] if e.get('author',{}).get('isOrgMember') and e.get('type')=='comment']
  self.assertIn('acceptable for the written report to cover the challenge case',organizer[-1]['data']['latest']['raw'])
if __name__=='__main__':unittest.main()
