#!/usr/bin/env python3
"""Offline public audit of v25 claims; no project dependencies or protected inputs."""
import csv
import hashlib
import io
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def require(ok,message):
    if not ok:raise ValueError(message)


def close(a,b):
    return math.isfinite(a) and math.isfinite(b) and abs(a-b)<=1e-12


def validate(result,summary,continuity,register,panel,report):
    require(result['version']==summary['version']==25 and result['complete'] and summary['complete'],'Incomplete or wrong campaign')
    runs=result['gpu_runs']
    require([r['registration']['shard'] for r in runs]==list(range(8)) and all(r['complete'] for r in runs),'Missing GPU worker')
    require(len({r['registration']['uuid'] for r in runs})==8,'GPU UUIDs not independent devices')
    require(all('H100' in r['registration']['device'] and r['registration']['tf32'] is False for r in runs),'Unreviewed numerical backend')
    totals={k:sum(r['comparisons'][k] for r in runs) for k in ['cross_batch','orthogonal','drug']}
    require(totals==result['comparisons']==summary['comparisons'],'Comparison count drift')
    require(sum(totals.values())==summary['total_comparisons']==2474445074,'Inflated compute count')
    cells=[c for r in runs for c in r['cells']]
    require(len(cells)==len({c['cell'] for c in cells})==19,'Cell coverage drift')
    require(sum(c['compound_profiles'] for c in cells)==summary['matched_compound_profiles']==285488,'Matched profile count drift')
    require(sum(c['compound_profiles']*c['crispr_genes'] for c in cells)==totals['drug'],'Drug matrix dimensions disagree')
    require(result['prepared']['bub1b_profiles']==31 and result['prepared']['bub1b_guides']==1,'Guide/profile confusion')
    require(summary['bub1b']['guides']==1 and summary['bub1b']['independent_guide_qualified_contexts']==0,'Unjustified guide qualification')
    require(summary['crispr_types']=={'trt_xpr':140945,'ctl_vector':1128,'ctl_untrt':828},'Controls confused with missing metadata')
    require(all(m['unannotated']==0 for m in result['prepared']['matrices']),'Unreviewed source join')
    require(not result['prepared']['bub1b_shared_replicate_pairs'] and result['prepared']['bub1b_with_old_shared_wells']==0,'Source-well reuse changed')
    cr=summary['bub1b']['cross_batch_records']
    require(len(cr)==30 and sum(r['top_one'] for r in cr)==2 and all(r['cell']=='HT29' for r in cr if r['top_one']),'Cross-batch result drift')
    orth=summary['bub1b']['orthogonal_records']
    require(len(orth)==20,'Missing unfavorable orthogonal result')
    ht=[r for r in orth if r['cell']=='HT29' and r['space']=='prime']
    require(len(ht)==2 and all(r['rnai_rank']==r['crispr_rank']==4 for r in ht),'Lost HT29 counterweight')
    require(all(r['correlation']<0 for r in orth if r['cell'] in ['MCF7','PC3']),'Lost discordant contexts')
    ev=summary['everolimus']
    require((ev['labelled_profiles'],ev['reference_matching_profiles'],ev['unresolved_identity_profiles'])==(628,271,357),'Compound identity pooling')
    require(ev['reference_matching_quality_passes']==82,'Source drug QC drift')
    b=[r for r in panel if r['gene']=='BUB1B' and r['compound_id']=='BRD-K13514097']
    q=[r for r in b if r['quality_pass']=='True']
    low=[r for r in q if float(r['dose'])<=.1]
    require(len(b)==15 and len(q)==5 and len(low)==3,'Favorable drug QC result lost')
    require(all(float(r['correlation'])<0 and int(r['query_quality_passes'])==0 for r in q),'Drug QC confused with query QC')
    require(all(float(r['exclude_BUB1B_correlation'])<0 and float(r['common_response_removed_correlation'])<0 for r in q),'Favorable sensitivity lost')
    mt=[r for r in panel if r['cell']=='MCF7' and r['gene']=='MTOR' and r['compound_id']=='BRD-K13514097' and float(r['dose'])==.1]
    require(len(mt)==1 and int(mt[0]['mimic_rank'])==1 and float(mt[0]['correlation'])>.28,'Lost MTOR favorable control')
    require(continuity['regrouped_profiles']==2 and continuity['exact_signature_matches']==0,'Changed-ID continuity lost')
    reused=[r for r in continuity['rows'] if r['shared_wells']]
    require({r['cell'] for r in reused}=={'A375','NPC'} and all(r['shared_wells']==3 and r['added_wells']==0 for r in reused),'False independent low-dose replication')
    require([r['id'] for r in register['claims']]==['R33','R34','R35','R36','R37'],'Incomplete claim challenges')
    for row in register['claims']:
        require(all(row.get(k) for k in ['support','challenge','falsifier','stop','reopen','next_action']),'Missing falsification action')
    for obj in [result,summary,register]:
        require(obj['drug_ranking_changed'] is False and obj['wet_lab_performed'] is False,'Unsupported biological promotion')
    require(summary['clinical_exposure_margin'] is None and register['rescue_priority'] is None,'Invented clinical margin/priority')
    require(all(r['maximum_numeric_error']<=2e-5 for r in runs),'Failed GPU validation')
    required=['one guide','0.3693','0.2836','regroup','not sustained saturation','2,474,445,074','Presentation v24 remains frozen']
    for phrase in required:require(phrase.lower() in report.lower(),'Lost report limitation/counterweight: '+phrase)
    return dict(passed=True,version=25,gpus=8,comparisons=sum(totals.values()),bub1b_profiles=31,bub1b_guides=1,
        matched_compound_profiles=285488,ht29_qualification_lead=True,independent_guide_qualified_contexts=0,
        drug_ranking_changed=False,biological_validation=False,new_neural_inference=False,claim_records=5)


def check(root=ROOT):
    root=Path(root)
    audit=json.loads((root/'notes/track2-crispr-audit-v25.json').read_text())
    for relative,expected in audit['public_input_sha256'].items():
        p=Path(relative)
        require(not p.is_absolute() and '..' not in p.parts and p.parts[0] in ['notes','scripts'],'Unsafe audit path')
        require(not any((root/Path(*p.parts[:i])).is_symlink() for i in range(1,len(p.parts)+1)),'Symlinked input')
        require(hashlib.sha256((root/p).read_bytes()).hexdigest()==expected,'Changed bound input: '+relative)
    load=lambda stem:json.loads((root/f'notes/track2-crispr-{stem}-v25.json').read_text())
    result,summary,continuity,register=[load(s) for s in ['results','summary','continuity','register']]
    panel=list(csv.DictReader(io.StringIO((root/'notes/track2-crispr-everolimus-v25.tsv').read_text()),delimiter='\t'))
    verified=validate(result,summary,continuity,register,panel,(root/'notes/track2-crispr-v25.md').read_text())
    plan_hash=audit['public_input_sha256']['notes/track2-crispr-plan-v25.json']
    code_hash=audit['public_input_sha256']['scripts/track2_crispr_v25.py']
    require(result['plan_sha256']==summary['plan_sha256']==plan_hash and result['script_sha256']==code_hash,'Plan/code registration mismatch')
    require(all(r['registration']['plan_sha256']==plan_hash and r['registration']['script_sha256']==code_hash for r in result['gpu_runs']),'Worker drift')
    require(audit['numerical']['passed'] and audit['numerical']['direct_everolimus_count']==141 and audit['numerical']['maximum_error']<=2e-5,'Original-coordinate validation missing')
    require(audit['archive_verification']['passed'] and audit['archive_verification']['extracted'] is False,'Archive verification missing')
    require(len(load('source-manifest')['files'])==6 and all(r['etag_verified'] for r in load('source-manifest')['files']),'Unchecked source data')
    return verified


if __name__=='__main__':print(json.dumps(check(),indent=2))
