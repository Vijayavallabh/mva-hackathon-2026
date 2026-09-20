#!/usr/bin/env python3
"""Model-comparison v14 snapshot, preserving every historical input and release."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import track2_release_v13 as historical
previous = historical.previous
from track2_release_v7 import Content

ROOT=previous.ROOT
require=previous.require
digest=previous.digest
FILES = {k:v for k,v in historical.FILES.items() if not any(tag in k for tag in ('report_v13', 'slides_v13', 'pitch_v13', 'video-description-v13'))}
FILES.update({'AlphaFold3-Output-Terms.md': 'notes/alphafold3-output-terms.md',
 'Legally-Binding-Terms-of-Use.txt': 'notes/alphafold3-Legally-Binding-Terms-of-Use.txt',
 'alphafold3-results.json': 'notes/track2-alphafold3-results.json',
 'esm3-structure-results.json': 'notes/track2-esm3-structure-results.json',
 'esmfold2-msa-results.json': 'notes/track2-esmfold2-msa-results.json',
 'esmfold2-single-results.json': 'notes/track2-esmfold2-single-results.json',
 'evo2-20b-results.json': 'notes/track2-evo2-20b-results.json',
 'jvv7_track2_pitch_v14.md': 'notes/track2-pitch-v14.md',
 'jvv7_track2_report_v14.md': 'notes/track2-report-v14.md',
 'jvv7_track2_slides_v14.html': 'notes/track2-slides-v14.html',
 'jvv7_track2_transcript_v14.txt': 'notes/track2-transcript-v14.txt',
 'latest-model-audit.json': 'notes/track2-latest-model-audit.json',
 'latest-model-plan.json': 'notes/track2-latest-model-plan.json',
 'latest-model-provenance.json': 'notes/track2-latest-model-provenance.json',
 'latest-model-source-audit.json': 'notes/track2-latest-model-source-audit.json',
 'latest-models.md': 'notes/track2-latest-models.md',
 'latest-protein-results.json': 'notes/track2-latest-protein-results.json',
 'video-description-v14.md': 'notes/track2-video-description-v14.md'})
FILES['presentation-review-v14.json']='notes/track2-v14-render-audit.json'
INPUTS = historical.INPUTS | set(FILES.values()) | {
 'notes/track2-v14-design.md',
 'scripts/render_track2_slides_v14.mjs',
 'scripts/run_track2_latest_fold2_msa.py',
 'scripts/run_track2_latest_setup.sh',
 'scripts/test_track2_latest_analysis.py',
 'scripts/test_track2_release_v14.py',
 'scripts/track2_evo2_20b_comparison.py',
 'scripts/track2_latest_af3.py',
 'scripts/track2_latest_af3.uv.lock',
 'scripts/track2_latest_af3_environment.toml',
 'scripts/track2_latest_analysis.py',
 'scripts/track2_latest_archive.py',
 'scripts/track2_latest_archive_initial.py',
 'scripts/track2_latest_esm.uv.lock',
 'scripts/track2_latest_esm_environment.toml',
 'scripts/track2_latest_jobs.py',
 'scripts/track2_latest_jobs_initial.py',
 'scripts/track2_latest_protein.py',
 'scripts/track2_latest_protein_ccd_fix.py',
 'scripts/track2_latest_protein_initial.py',
 'scripts/track2_latest_publish_results.py',
 'scripts/track2_latest_resources.py',
 'scripts/track2_latest_resources_retry.py',
 'scripts/track2_latest_verify_archive.py',
 'scripts/track2_release_v14.py',
}
FIELDS={'schema_version','created_utc','files','input_hashes','historical_v13_manifest',
 'presentation','upload_ready','upload_performed','video_url','provider_settings_verified',
 'phase','clinical_exposure_margin'}

class DeckParser(previous.static.DeckParser):
 def validate(self):
  require(not self.stack and self.html_count==1,'incomplete HTML')
  require(self.csp_count==1,'restrictive CSP required')
  require(self.sections==[f'slide-{i}' for i in range(1,10)],'nine ordered slides required')
  require(self.svg_count==8 and self.section_vectors==[1]*8+[0],'eight figures plus acknowledgement required')

def presentation_checks(deck):
 parser=DeckParser();parser.feed(deck);parser.close();parser.validate()
 c=Content();c.feed(deck);slides=[' '.join(x).lower() for x in c.sections]
 for n,phrases in previous.REQUIRED.items():
  idx=n-1 if n==1 else n+1
  for phrase in phrases:
   phrase=phrase.replace('no experiments performed','no wet-lab experiments').replace('fireworks training/retention unverified','fireworks and alignment-service policies unverified')
   require(phrase in slides[idx],f'missing scientific boundary on slide {idx+1}: {phrase}')
 for phrase in ['earlier esm','seven checkpoints','disagreement + failed controls','all four pass the fixed gate',
                'negative n1002k scores in all three windows','esm3-open 1.4b','84 scores','small engineered-control set',
                'no clinical classification or drug ranking']:
  require(phrase in slides[1],f'missing sequence qualification: {phrase}')
 for phrase in ['192 new structures','alphafold3 / esmfold2','impaired controls also fold',
                '7.10–9.10 å','evo2 20b','auroc 0.920','100 comparisons',
                'brca1 benchmark does not validate bub1b','endogenous rna, protein and cell function',
                'alphafold3-derived summaries / interpretation modified','alphafold3 output terms','terms notice']:
  require(phrase in slides[2],f'missing structural/DNA qualification: {phrase}')
 for link in ['https://doi.org/10.1038/s41586-024-07487-w',
              'https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphafold3-output-terms.md',
              'https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphafold3-Legally-Binding-Terms-of-Use.txt']:
  require(link in c.links,'missing AF3 citation/terms link')
 old=(ROOT/'notes/track2-slides-v12.html').read_text()
 pattern=r'<svg id="arst1431-plot".*?</svg>'
 require(re.findall(pattern,deck,re.S)==re.findall(pattern,old,re.S),'randomized trial plot changed')
 require(previous.normalized(previous.acknowledgement()).lower() in slides[8],'full acknowledgement required')
 require('https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v14.md' in c.links,'current disclosure link required')
 require(previous.previous.previous.REMOVED_LINE not in slides[0],'removed cover line restored')
 return dict(slides=9,vector_figures=8,visible_words=[len(x) for x in c.sections])

def check_deck():
 p=ROOT/'notes/track2-slides-v14.html';data=p.read_bytes()
 return dict(static_deck_verified=True,source_sha256=hashlib.sha256(data).hexdigest(),**presentation_checks(data.decode()))

def scientific_checks():
 deck=check_deck();report=(ROOT/'notes/track2-report-v14.md').read_text()
 require('Computational evidence supports\nthe missense allele' not in report,'unqualified missense claim restored')
 for phrase in ['older model disagreement','failed experimental-control','clinical exposure','phase','ColabFold','Evo2']:
  require(phrase.lower() in report.lower(),f'missing report qualification/disclosure: {phrase}')
 pitch=(ROOT/'notes/track2-pitch-v14.md').read_text()
 spoken=pitch.split('## Narration\n')[1].split('## Recording notes')[0]
 require(re.findall(r'### Slide (\d+) /',spoken)==list('123456789'),'nine aligned narration sections required')
 counts=[len(x.split()) for x in re.split(r'### Slide [^\n]+\n',spoken)[1:]]
 require(310<=sum(counts)<=375,'three-minute planning word budget exceeded')
 require(f'Narration contains {sum(counts)} whitespace-separated words' in pitch,'word count drift')
 for phrase in ['whole blood is not free tissue','phase remain unconfirmed','no rescue priority, clinical margin or wet-lab result',
                'fail selected controls','not validate bub1b','small fixed control challenge','alphafold3 output terms']:
  require(phrase in ' '.join(pitch.lower().split()),f'missing narration boundary: {phrase}')
 transcript='Track 2 v14 — read-aloud transcript\nRead the paragraphs; headings and times are cues, not narration.\n\n'
 for header,paragraph in re.findall(r'### Slide ([^\n]+)\n\n(.*?)(?=\n\n###|\Z)',spoken.strip(),re.S):
  transcript+='Slide '+header.replace(' / ',' | ')+'\n'+paragraph.strip()+'\n\n'
 require((ROOT/'notes/track2-transcript-v14.txt').read_text()==transcript,'plain transcript drift')
 old_report=(ROOT/'notes/track2-report-v13.md').read_text()
 require(report.split('## 2. Test the mechanism before the drug')[1].split('## 8. Reproducibility')[0]==old_report.split('## 2. Test the mechanism before the drug')[1].split('## 8. Reproducibility')[0],'unchanged drug science drift')
 model_evidence_checks()
 review=json.loads((ROOT/'notes/track2-v14-render-audit.json').read_text())
 require(review['source_sha256']==deck['source_sha256'],'audited deck hash drift')
 require(review['renderer_sha256']==digest(ROOT/'scripts/render_track2_slides_v14.mjs'),'audited renderer hash drift')
 require(len(review['slides'])==9 and all(not x['outside'] and not x['overlaps'] and x['min_font_px']>=24 for x in review['slides']),'visual geometry failed')
 require(review['files']['AlphaFold3-Output-Terms.md']==digest(ROOT/'notes/alphafold3-output-terms.md'),'rendered terms drift')
 require(review['files']['Legally-Binding-Terms-of-Use.txt']==digest(ROOT/'notes/alphafold3-Legally-Binding-Terms-of-Use.txt'),'rendered notice drift')
 for name in ['track2-report-v14.md' ,'track2-video-description-v14.md']:
  text=(ROOT/'notes'/name).read_text()
  require(previous.normalized(text.split('## Acknowledgement\n')[1])==previous.normalized(previous.acknowledgement()),'acknowledgement changed')
 return dict(**deck,narration_words=sum(counts),words_per_slide=counts,runtime_measured=False)

def model_evidence_checks():
 from track2_latest_analysis import sequence_check
 from track2_evo2_comparison import functional_gate
 plan=json.loads((ROOT/'notes/track2-latest-model-plan.json').read_text())
 provenance=json.loads((ROOT/'notes/track2-latest-model-provenance.json').read_text())
 archived=provenance['archive_manifest']['files']
 proteins=json.loads((ROOT/'notes/track2-latest-protein-results.json').read_text())['models']
 require(len(proteins)==4 and sum(len(x['rows']) for x in proteins.values())==84,'protein matrix incomplete')
 for label,result in proteins.items():
  encoded=(json.dumps(result,indent=2,allow_nan=False)+'\n').encode()
  require(hashlib.sha256(encoded).hexdigest()==archived[f'outputs/{label}/summary.json']['sha256'],'protein output binding drift')
  checked=sequence_check(result,plan)
  require(checked['gate']['pass'] and all(r['score']<0 for r in checked['candidate']),'new-model slide claim does not match scores')
 total=0
 for name in ['alphafold3','esm3-structure','esmfold2-single','esmfold2-msa']:
  result=json.loads((ROOT/f'notes/track2-{name}-results.json').read_text())
  total+=result['structures']
  require(len(result['records'])==result['structures'],'structure matrix incomplete')
 require(total==192,'structure count drift')
 esm3=json.loads((ROOT/'notes/track2-esm3-structure-results.json').read_text())
 require([round(x,2) for x in esm3['ranges']['WT']['CA_rmsd_range_angstrom']]==[7.10,9.10],'displayed WT variability drift')
 evo=json.loads((ROOT/'notes/track2-evo2-20b-results.json').read_text())
 require(digest(ROOT/'notes/track2-evo2-20b-results.json')==archived['outputs/Evo2-20B/summary.json']['sha256'],'Evo output binding drift')
 require(len(evo['benchmark'])==96 and len(evo['candidate_scores'])==4,'Evo matrix incomplete')
 require(evo['numerical_gate']['pass'] and evo['benchmark_gate']['pass_gate'],'Evo qualification drift')
 require(evo['benchmark_gate']==functional_gate(evo['benchmark']),'Evo gate recomputation mismatch')
 require(round(evo['benchmark_gate']['auroc_negative_delta'],3)==0.920,'displayed AUROC drift')
 require(not evo['clinical_classification'] and not evo['drug_ranking_changed'] and not evo['phase_resolved'],'unsupported promotion')
 audit=json.loads((ROOT/'notes/track2-latest-model-audit.json').read_text())
 require(audit['passed'] is True and audit['clinical_validation'] is False,'model audit claim drift')
 require(audit['plan_sha256']==digest(ROOT/'notes/track2-latest-model-plan.json'),'plan binding drift')
 require(audit['analysis_sha256']==digest(ROOT/'scripts/track2_latest_analysis.py'),'analysis binding drift')
 for name in ['track2-report-v14.md','track2-video-description-v14.md']:
  text=(ROOT/'notes'/name).read_text()
  for phrase in ['AlphaFold3 Output Terms','Legally','modifications','10.1038/s41586-024-07487-w','Fireworks','unverified']:
   require(phrase in text,'missing output terms/provider disclosure')
 return dict(protein_scores=84,structures=192,dna_comparisons=100)

def inputs():return {s:digest(ROOT/s) for s in sorted(INPUTS)}
def history():
 p=ROOT/'results/feat009/jvv7_track2_research_v13'
 require(historical.verify(p)['integrity_verified'],'v13/historical verification failed')
 return digest(p/'manifest.json')
def location(path):
 path=previous.checked_path(path)
 require(path.parent==ROOT/'results/feat009' and re.fullmatch(r'[a-z0-9][a-z0-9_-]*',path.name),'invalid snapshot path')
 require(path.name not in {f'jvv7_track2_research_v{i}' for i in range(1,14)},'historical snapshot protected')
 return path

def build(path):
 path=location(path);require(not path.exists(),'use a new output directory')
 checks=scientific_checks();bound=inputs();old=history();path.mkdir()
 for name,source in FILES.items():shutil.copyfile(ROOT/source,path/name)
 manifest=dict(schema_version=14,created_utc=datetime.now(timezone.utc).isoformat(),
  files={name:digest(path/name) for name in FILES},input_hashes=bound,historical_v13_manifest=old,
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
 require(m['schema_version']==14 and m['input_hashes']==inputs(),'input/schema drift')
 require(set(m['files'])==set(FILES) and {p.name for p in path.iterdir()}==set(FILES)|{'manifest.json'},'unexpected file set')
 for name,source in FILES.items():require(digest(path/name)==m['files'][name]==m['input_hashes'][source],'output drift')
 require(m['historical_v13_manifest']==history(),'historical drift')
 require(m['presentation']==scientific_checks(),'presentation drift')
 require(all(m[k] is False for k in ['upload_ready','upload_performed','provider_settings_verified']),'readiness changed')
 require(m['video_url'] is None and m['clinical_exposure_margin'] is None and m['phase']=='unconfirmed','scientific status changed')
 return dict(integrity_verified=True,files=len(FILES),bound_inputs=len(INPUTS),historical_v1_through_v13_preserved=True,upload_ready=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['check-deck','check','build','verify']);p.add_argument('output',type=Path,nargs='?');a=p.parse_args()
 if a.command in ['build','verify']:
  if a.output is None:p.error('new output directory required')
  result={'build':build,'verify':verify}[a.command](a.output)
 else:
  if a.output is not None:p.error('check takes no output')
  result={'check':scientific_checks,'check-deck':check_deck}[a.command]()
 print(json.dumps(result,indent=2))
