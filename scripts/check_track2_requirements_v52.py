#!/usr/bin/env python3
"""Verify the anonymous v52 official-source and latest-thread refresh."""
import json
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'notes/track2-requirements-v52.json'
SOURCE=ROOT/'sources/public-official-v52'
def require(c,m):
 if not c: raise ValueError(m)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check():
 require(AUDIT.is_file(),'Missing v52 audit')
 a=json.loads(AUDIT.read_text())
 require(a['schema_version']==52 and a['anonymous_get_only'] and a['provider_settings_verified'] is False,'Audit scope drift')
 require(a['official_files']['tabs-submit_track2.py']==digest(SOURCE/'tabs-submit_track2.py')=='f48d576ab052df34527222b7693f956e15e5376ef68eddedcf0c4f04736bf65c','Submit form drift')
 for n,sha in a['official_files'].items():require(sha==digest(SOURCE/n),'Official receipt drift: '+n)
 require(a['discussion_listing']['count']==32 and a['discussion_listing']['closed_count']==16,'Discussion listing drift')
 require(sorted(a['discussion_listing']['numbers'])==list(range(1,9))+list(range(10,34)),'Missing discussion number')
 require(a['material_changes']['official_submission_files_unchanged'] and a['material_changes']['rubric_unchanged'],'False material-change claim')
 require(a['material_changes']['new_organizer_requirement_found'] is False,'False new requirement claim')
 for phrase in ['thread 33 is an open readme/sdk update pull request','thread 32 contains an organizer reply permitting a written report that','thread 31 documents a synapse alternative']:
  require(phrase in (ROOT/'notes/track2-requirements-review-v52.md').read_text().lower(),'Review boundary missing: '+phrase)
 return {'passed':True,'version':52,'official_files':len(a['official_files']),'discussions':a['discussion_listing']['count'],'new_organizer_requirement_found':False,'provider_settings_verified':False,'upload_ready':False}
if __name__=='__main__':print(json.dumps(check(),indent=2))
