#!/usr/bin/env python3
"""Model-comparison v13 snapshot, preserving every historical input and release."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import track2_release_v12 as previous
from track2_release_v7 import Content

ROOT=previous.ROOT
require=previous.require
digest=previous.digest
FILES={
 'jvv7_track2_report_v13.md':'notes/track2-report-v13.md',
 'jvv7_track2_slides_v13.html':'notes/track2-slides-v13.html',
 'jvv7_track2_pitch_v13.md':'notes/track2-pitch-v13.md',
 'video-description-v13.md':'notes/track2-video-description-v13.md',
 'model-comparison.md':'notes/track2-model-expansion.md',
 'esm-results.json':'notes/track2-esm-expanded-results.json',
 'boltz-single-results.json':'notes/track2-boltz-single-summary.json',
 'boltz-msa-results.json':'notes/track2-boltz-msa-summary.json',
 'alphafold-results.json':'notes/track2-alphafold-results.json',
 'evo2-7b-results.json':'notes/track2-evo2-7b-results.json',
 'protein-reanalysis-audit.json':'notes/track2-protein-model-audit.json',
 'validation-v10.md':'notes/track2-validation-v10.md',
 'evidence-v10.json':'notes/track2-evidence-v10.json',
 'evo2-40b-results.json':'notes/track2-evo2-40b-results.json',
 'evo2-result-audit.json':'notes/track2-evo2-result-audit.json',
 'model-provenance.json':'notes/track2-model-provenance.json',
 'protein-model-plan.json':'notes/track2-model-expansion-plan.json',
 'shared-msa-plan.json':'notes/track2-structure-msa-plan.json',
 'alphafold-plan.json':'notes/track2-alphafold-plan.json',
 'evo2-plan.json':'notes/track2-evo2-plan.json',
 'evo2-runtime-amendment.md':'notes/track2-evo2-runtime-amendment.md',
 'evo2-memory-amendment.json':'notes/track2-evo2-memory-amendment.json',
 'experimental-coordinate-audit.json':'notes/track2-structure-reference-audit.json',
}
# Fixed catalogue: snapshot binds all model methods, results and presentation inputs.
INPUTS=previous.INPUTS | set(FILES.values()) | {
 'scripts/track2_evo2_long_context.py',
 'scripts/run_track2_evo2_long_context.sh',
 'notes/track2-alphafold-plan.json',
 'notes/track2-alphafold-results.json',
 'notes/track2-boltz-msa-summary.json',
 'notes/track2-boltz-single-summary.json',
 'notes/track2-esm-expanded-results.json',
 'notes/track2-esm-pilot-plan.json',
 'notes/track2-esm-pilot-results.json',
 'notes/track2-esm-pilot.md',
 'notes/track2-evo2-40b-results.json',
 'notes/track2-evo2-7b-results.json',
 'notes/track2-evo2-plan.json',
 'notes/track2-evo2-result-audit.json',
 'notes/track2-evo2-runtime-amendment.md',
 'notes/track2-model-expansion-plan.json',
 'notes/track2-model-expansion.md',
 'notes/track2-model-provenance.json',
 'notes/track2-pitch-v13.md',
 'notes/track2-protein-model-audit.json',
 'notes/track2-report-v13.md',
 'notes/track2-slides-v13.html',
 'notes/track2-structure-msa-plan.json',
 'notes/track2-structure-reference-audit.json',
 'notes/track2-v13-design.md',
 'notes/track2-video-description-v13.md',
 'scripts/render_track2_slides_v13.mjs',
 'scripts/run_track2_esm_pilot.sh',
 'scripts/run_track2_evo2_cublas_retry.sh',
 'scripts/run_track2_evo2_fp8_flash_retry.sh',
 'scripts/run_track2_evo2_fp8_setup.sh',
 'scripts/run_track2_evo2_model.py',
 'scripts/run_track2_evo2_setup.sh',
 'scripts/run_track2_model_expansion.py',
 'scripts/test_track2_esm_pilot.py',
 'scripts/test_track2_evo2_comparison.py',
 'scripts/test_track2_evo2_result_audit.py',
 'scripts/test_track2_model_expansion.py',
 'scripts/test_track2_release_v13.py',
 'scripts/test_track2_structure_analysis.py',
 'scripts/track2_alphafold.uv.lock',
 'scripts/track2_alphafold_analysis.py',
 'scripts/track2_alphafold_comparison.py',
 'scripts/track2_alphafold_environment.toml',
 'scripts/track2_boltz.uv.lock',
 'scripts/track2_boltz_comparison.py',
 'scripts/track2_boltz_environment.toml',
 'scripts/track2_boltz_msa.py',
 'scripts/track2_esm_environment.toml',
 'scripts/track2_esm_loader_resources.py',
 'scripts/track2_esm_pilot.py',
 'scripts/track2_esm_pilot.uv.lock',
 'scripts/track2_esm_remote_env.sh',
 'scripts/track2_evo2.uv.lock',
 'scripts/track2_evo2_bootstrap_environment.toml',
 'scripts/track2_evo2_comparison.py',
 'scripts/track2_evo2_cublas.uv.lock',
 'scripts/track2_evo2_cublas_environment.toml',
 'scripts/track2_evo2_environment.toml',
 'scripts/track2_evo2_fp8.uv.lock',
 'scripts/track2_evo2_fp8_bootstrap_environment.toml',
 'scripts/track2_evo2_fp8_environment.toml',
 'scripts/track2_evo2_resources.py',
 'scripts/track2_evo2_result_audit.py',
 'scripts/track2_expansion_env.sh',
 'scripts/track2_model_expansion.py',
 'scripts/track2_model_result_audit.py',
 'scripts/track2_release_v13.py',
 'scripts/track2_structure_analysis.py',
 'scripts/track2_structure_reference_audit.py',
}
FIELDS={'schema_version','created_utc','files','input_hashes','historical_v12_manifest',
 'presentation','upload_ready','upload_performed','video_url','provider_settings_verified',
 'phase','clinical_exposure_margin'}

class DeckParser(previous.static.DeckParser):
 def validate(self):
  require(not self.stack and self.html_count==1,'incomplete HTML')
  require(self.csp_count==1,'restrictive CSP required')
  require(self.sections==[f'slide-{i}' for i in range(1,9)],'eight ordered slides required')
  require(self.svg_count==7 and self.section_vectors==[1]*7+[0],'seven figures plus acknowledgement required')

def presentation_checks(deck):
 parser=DeckParser();parser.feed(deck);parser.close();parser.validate()
 c=Content();c.feed(deck);slides=[' '.join(x).lower() for x in c.sections]
 for n,phrases in previous.REQUIRED.items():
  idx=n-1 if n==1 else n
  for phrase in phrases:
   phrase=phrase.replace('no experiments performed','no wet-lab experiments').replace('fireworks training/retention unverified','fireworks and alignment-service policies unverified')
   require(phrase in slides[idx],f'missing scientific boundary on slide {idx+1}: {phrase}')
 for phrase in ['seven esm checkpoints','48 boltz / 120 alphafold2','impaired controls also fold',
                'brca1 benchmark does not validate bub1b','endogenous rna, protein and cell function']:
  require(phrase in slides[1],f'missing model qualification: {phrase}')
 old=(ROOT/'notes/track2-slides-v12.html').read_text()
 pattern=r'<svg id="arst1431-plot".*?</svg>'
 require(re.findall(pattern,deck,re.S)==re.findall(pattern,old,re.S),'randomized trial plot changed')
 require(previous.normalized(previous.acknowledgement()).lower() in slides[7],'full acknowledgement required')
 require('https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v13.md' in c.links,'current disclosure link required')
 require(previous.previous.previous.REMOVED_LINE not in slides[0],'removed cover line restored')
 return dict(slides=8,vector_figures=7,visible_words=[len(x) for x in c.sections])

def check_deck():
 p=ROOT/'notes/track2-slides-v13.html';data=p.read_bytes()
 return dict(static_deck_verified=True,source_sha256=hashlib.sha256(data).hexdigest(),**presentation_checks(data.decode()))

def scientific_checks():
 deck=check_deck();report=(ROOT/'notes/track2-report-v13.md').read_text()
 require('Computational evidence supports\nthe missense allele' not in report,'unqualified missense claim restored')
 for phrase in ['discordant','failed experimental-control','clinical exposure','phase','ColabFold','Evo2']:
  require(phrase.lower() in report.lower(),f'missing report qualification/disclosure: {phrase}')
 pitch=(ROOT/'notes/track2-pitch-v13.md').read_text()
 spoken=pitch.split('## Narration\n')[1].split('## Recording notes')[0]
 require(re.findall(r'### Slide (\d+) /',spoken)==list('12345678'),'eight aligned narration sections required')
 counts=[len(x.split()) for x in re.split(r'### Slide [^\n]+\n',spoken)[1:]]
 require(310<=sum(counts)<=375,'three-minute planning word budget exceeded')
 require(f'Narration contains {sum(counts)} whitespace-separated words' in pitch,'word count drift')
 for phrase in ['whole blood is not free tissue','phase remain unconfirmed','no wet-lab experiment',
                'failed controls','not validate bub1b']:
  require(phrase in pitch.lower(),f'missing narration boundary: {phrase}')
 for name in ['track2-report-v13.md','track2-video-description-v13.md']:
  text=(ROOT/'notes'/name).read_text()
  require(previous.normalized(text.split('## Acknowledgement\n')[1])==previous.normalized(previous.acknowledgement()),'acknowledgement changed')
 return dict(**deck,narration_words=sum(counts),words_per_slide=counts,runtime_measured=False)

def inputs():return {s:digest(ROOT/s) for s in sorted(INPUTS)}
def history():
 p=ROOT/'results/feat009/jvv7_track2_research_v12'
 require(previous.verify(p)['integrity_verified'],'v12/historical verification failed')
 return digest(p/'manifest.json')
def location(path):
 path=previous.checked_path(path)
 require(path.parent==ROOT/'results/feat009' and re.fullmatch(r'[a-z0-9][a-z0-9_-]*',path.name),'invalid snapshot path')
 require(path.name not in {f'jvv7_track2_research_v{i}' for i in range(1,13)},'historical snapshot protected')
 return path

def build(path):
 path=location(path);require(not path.exists(),'use a new output directory')
 checks=scientific_checks();bound=inputs();old=history();path.mkdir()
 for name,source in FILES.items():shutil.copyfile(ROOT/source,path/name)
 manifest=dict(schema_version=13,created_utc=datetime.now(timezone.utc).isoformat(),
  files={name:digest(path/name) for name in FILES},input_hashes=bound,historical_v12_manifest=old,
  presentation=checks,upload_ready=False,upload_performed=False,video_url=None,
  provider_settings_verified=False,phase='unconfirmed',clinical_exposure_margin=None)
 require(inputs()==bound and history()==old,'input drift during copy')
 (path/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 return verify(path)

def verify(path):
 path=location(path);m=json.loads((path/'manifest.json').read_text())
 previous.foundation.exact_keys(m,FIELDS,'manifest')
 timestamp=datetime.fromisoformat(m['created_utc'])
 require(timestamp.tzinfo is not None and timestamp.utcoffset().total_seconds()==0,'UTC timestamp required')
 require(m['schema_version']==13 and m['input_hashes']==inputs(),'input/schema drift')
 require(set(m['files'])==set(FILES) and {p.name for p in path.iterdir()}==set(FILES)|{'manifest.json'},'unexpected file set')
 for name,source in FILES.items():require(digest(path/name)==m['files'][name]==m['input_hashes'][source],'output drift')
 require(m['historical_v12_manifest']==history(),'historical drift')
 require(m['presentation']==scientific_checks(),'presentation drift')
 require(all(m[k] is False for k in ['upload_ready','upload_performed','provider_settings_verified']),'readiness changed')
 require(m['video_url'] is None and m['clinical_exposure_margin'] is None and m['phase']=='unconfirmed','scientific status changed')
 return dict(integrity_verified=True,files=len(FILES),bound_inputs=len(INPUTS),historical_v1_through_v12_preserved=True,upload_ready=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['check-deck','check','build','verify']);p.add_argument('output',type=Path,nargs='?');a=p.parse_args()
 if a.command in ['build','verify']:
  if a.output is None:p.error('new output directory required')
  result={'build':build,'verify':verify}[a.command](a.output)
 else:
  if a.output is not None:p.error('check takes no output')
  result={'check':scientific_checks,'check-deck':check_deck}[a.command]()
 print(json.dumps(result,indent=2))
