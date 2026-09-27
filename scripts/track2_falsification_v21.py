#!/usr/bin/env python3
"""Review the v21 falsification amendment and exercise proposed decision logic.

This is a research-planning checker, never a treatment or automated dose selector.
All numeric examples are synthetic; actual model results and margins remain null.
"""
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GATES=('assay_valid','model_qualified','branch_eligible','plan_locked','compound_identity',
       'joint_drug_deficit','randomized_blinded','experimental_units_valid',
       'all_enrolled_accounted','independent_confirmation','exposure_bridge',
       'mechanism_interpretable','scope_qualified')
HARMS=('division_capacity','chromosome_fidelity','viability','regeneration','recovery')
STATES={'pass','fail','unknown'}

def require(ok,message):
    if not ok: raise ValueError(message)

def numeric(x):
    return type(x) in (int,float) and math.isfinite(x)

def endpoint(value):
    require(set(value)=={'unit','interval','margin'},'Wrong endpoint fields')
    require(isinstance(value['unit'],str) and value['unit'].strip(),'Endpoint unit missing')
    margin=value['margin']; interval=value['interval']
    require(margin is None or (numeric(margin) and margin>0),'Invalid or unjustified margin')
    if interval is not None:
        require(type(interval) is list and len(interval)==2 and all(numeric(x) for x in interval)
                and interval[0]<=interval[1],'Invalid uncertainty interval')
    return interval,margin

def decide(record):
    require(set(record)=={'schema_version','scope','gates','benefit','harms','safety_stop_observed','evidence_kind'},'Wrong decision fields')
    require(record['schema_version']==21,'Wrong decision schema')
    require(record['scope']=='qualified_non_cancer_model','Out-of-scope decision request')
    require(record['evidence_kind'] in {'not_measured','synthetic','reviewed_confirmation'},'Unknown evidence kind')
    gates=record['gates']
    require(set(gates)==set(GATES) and all(type(x) is str and x in STATES for x in gates.values()),'Missing or invalid gate')
    require(set(record['harms'])==set(HARMS),'Missing injury endpoint')
    benefit,delta=endpoint(record['benefit'])
    harms={k:endpoint(v) for k,v in record['harms'].items()}
    require(record['safety_stop_observed'] is None or type(record['safety_stop_observed']) is bool,'Invalid stop flag')
    if record['evidence_kind']=='not_measured':
        require(benefit is None and delta is None and all(i is None and m is None for i,m in harms.values())
                and all(x=='unknown' for x in gates.values()) and record['safety_stop_observed'] is None,
                'Unmeasured evidence cannot contain passes or numerical results')
    result=dict(clinical_recommendation=False,scope=record['scope'],evidence_kind=record['evidence_kind'])
    def out(decision,reason): return result|dict(decision=decision,reason=reason)
    # A flagged adverse event stops advancement pending review even if attribution is unresolved.
    if record['safety_stop_observed'] is True:
        return out('STOP_SAFETY_REVIEW','Observed safety trigger; attribution requires review')
    if gates['assay_valid']=='fail':
        return out('INVALID_HOLD','Failed assay/control cannot refute a biological hypothesis')
    if gates['assay_valid']=='pass' and any(interval is not None and margin is not None and interval[0]>margin for interval,margin in harms.values()):
        return out('STOP_SAFETY_REVIEW','Injury exceeds its prespecified bound in the tested context')
    if gates['plan_locked']=='fail':
        return out('INVALID_HOLD','Post-hoc changes cannot serve as locked confirmation')
    if gates['assay_valid']=='pass' and any(gates[g]=='fail' for g in ('model_qualified','branch_eligible')):
        return out('STOP_BRANCH','Qualified test rejects this model/branch prerequisite only')
    if any(x!='pass' for x in gates.values()):
        return out('HOLD','Prerequisites unresolved or failed; no transfer from another branch')
    if record['safety_stop_observed'] is None:
        return out('HOLD','Safety-trigger assessment missing')
    if benefit is not None and delta is not None and benefit[1]<delta:
        return out('STOP_TESTED_BENEFIT','Interval excludes the prespecified meaningful benefit; not universal inefficacy')
    if benefit is None or delta is None or any(i is None or m is None for i,m in harms.values()):
        return out('HOLD','Measurements or independently justified margins missing')
    if benefit[0]<=delta or any(i[1]>=m for i,m in harms.values()):
        return out('HOLD','Insufficient precision for benefit or noninferiority; nonsignificance is not safety')
    return out('PRECLINICAL_REVIEW_ONLY','All scoped criteria met; specialist review and additional scope qualification remain')

def validate_register(register, baseline):
    require(register['schema_version']==21 and register['clinical_recommendation'] is False,
            'Unsupported register scope')
    claims=register['claims']
    ids={c['id'] for c in claims}
    require(ids>={c['id'] for c in baseline['claims']},'Baseline claim omitted')
    require(len(ids)==len(claims)==27,'Duplicate/missing claim')
    for c in claims:
        for field in ('claim','support','challenge','falsifier','stop_rule','reopen_rule','v21_action','state','evidence_refs'):
            require(c.get(field),'Missing falsification field: '+c['id']+' / '+field)
        require(set(c.get('depends_on',[]))<=ids and set(c.get('eligible_branch_any_of',[]))<=ids,
                'Unknown claim dependency')
        require(c['state'] in {'unresolved','inference_rejected','bounded_evidence'},'Unsupported claim promotion')
    require(register['rescue_priority'] is None and register['phase']=='unconfirmed' and register['clinical_exposure_margin'] is None,'Scientific promotion')
    require(register['advancement_gates']==baseline['advancement_gates'],
            'Unmeasured advancement gates changed')
    return len(claims)

def validate_evidence(decisions, old):
    require(decisions['schema_version']==21 and decisions['disposition_change'] is False and
            decisions['rescue_priority'] is None and decisions['clinical_exposure_margin'] is None and
            decisions['phase']=='unconfirmed','Unsupported evidence promotion')
    require(decisions['baseline']=='notes/track2-evidence-v15.json','Baseline route lost')
    require(decisions['decisions']==old['decisions'],'Drug dispositions changed')
    sources=decisions['additional_sources']
    ids={s['id'] for s in sources}
    require(len(ids)==len(sources)==12,'Duplicate or missing source adjudication')
    require(not ids & {s['id'] for s in old['sources']},'Baseline source ID reused')
    for s in sources:
        require(all(s.get(k) for k in ('id','url','reading_depth','finding','limit','decision')),'Incomplete source adjudication')
    return len(sources)

def check():
    register=json.loads((ROOT/'notes/track2-falsification-register-v21.json').read_text())
    baseline=json.loads((ROOT/'notes/track2-falsification-register-v15.json').read_text())
    count=validate_register(register,baseline)
    decisions=json.loads((ROOT/'notes/track2-evidence-v21.json').read_text())
    old=json.loads((ROOT/'notes/track2-evidence-v15.json').read_text())
    sources=validate_evidence(decisions,old)
    plan=json.loads((ROOT/'notes/track2-decision-contract-v21.json').read_text())
    actual=decide(plan)
    require(actual['decision']=='HOLD' and plan['evidence_kind']=='not_measured','Actual evidence promoted')
    return dict(passed=True,claims=count,additional_source_records=sources,
                current_decision=actual,drug_dispositions_changed=False,biological_validation=False)

if __name__=='__main__': print(json.dumps(check(),indent=2))
