/* Offline educational view of the unchanged v21 research decision policy. */
'use strict';
(() => {
  const gates=['assay_valid','model_qualified','branch_eligible','plan_locked','compound_identity','joint_drug_deficit','randomized_blinded','experimental_units_valid','all_enrolled_accounted','independent_confirmation','exposure_bridge','mechanism_interpretable','scope_qualified'];
  const harms=['division_capacity','chromosome_fidelity','viability','regeneration','recovery'];
  const check=(x,m)=>{if(!x)throw new Error(m);};
  const keys=(x,k)=>x&&typeof x==='object'&&!Array.isArray(x)&&Object.keys(x).sort().join('|')===[...k].sort().join('|');
  const numeric=x=>typeof x==='number'&&Number.isFinite(x);
  function endpoint(x){
    check(keys(x,['unit','interval','margin']),'Wrong endpoint fields');
    check(typeof x.unit==='string'&&x.unit.trim(),'Endpoint unit missing');
    check(x.margin===null||(numeric(x.margin)&&x.margin>0),'Invalid or unjustified margin');
    check(x.interval===null||(Array.isArray(x.interval)&&x.interval.length===2&&x.interval.every(numeric)&&x.interval[0]<=x.interval[1]),'Invalid uncertainty interval');
    return [x.interval,x.margin];
  }
  function decide(r){
    check(keys(r,['schema_version','scope','gates','benefit','harms','safety_stop_observed','evidence_kind']),'Wrong decision fields');
    check(r.schema_version===21,'Wrong decision schema');
    check(r.scope==='qualified_non_cancer_model','Out-of-scope decision request');
    check(['not_measured','synthetic','reviewed_confirmation'].includes(r.evidence_kind),'Unknown evidence kind');
    check(keys(r.gates,gates)&&Object.values(r.gates).every(x=>['pass','fail','unknown'].includes(x)),'Missing or invalid gate');
    check(keys(r.harms,harms),'Missing injury endpoint');
    const [b,d]=endpoint(r.benefit), hs=Object.values(r.harms).map(endpoint),g=r.gates;
    check(r.safety_stop_observed===null||typeof r.safety_stop_observed==='boolean','Invalid stop flag');
    if(r.evidence_kind==='not_measured')check(b===null&&d===null&&hs.every(([i,m])=>i===null&&m===null)&&Object.values(g).every(x=>x==='unknown')&&r.safety_stop_observed===null,'Unmeasured evidence cannot contain passes or numerical results');
    const out=(decision,reason)=>({clinical_recommendation:false,scope:r.scope,evidence_kind:r.evidence_kind,decision,reason});
    if(r.safety_stop_observed===true)return out('STOP_SAFETY_REVIEW','Observed safety trigger; attribution requires review');
    if(g.assay_valid==='fail')return out('INVALID_HOLD','Failed assay/control cannot refute a biological hypothesis');
    if(g.assay_valid==='pass'&&hs.some(([i,m])=>i!==null&&m!==null&&i[0]>m))return out('STOP_SAFETY_REVIEW','Injury exceeds its prespecified bound in the tested context');
    if(g.plan_locked==='fail')return out('INVALID_HOLD','Post-hoc changes cannot serve as locked confirmation');
    if(g.assay_valid==='pass'&&['model_qualified','branch_eligible'].some(k=>g[k]==='fail'))return out('STOP_BRANCH','Qualified test rejects this model/branch prerequisite only');
    if(Object.values(g).some(x=>x!=='pass'))return out('HOLD','Prerequisites unresolved or failed; no transfer from another branch');
    if(r.safety_stop_observed===null)return out('HOLD','Safety-trigger assessment missing');
    if(b!==null&&d!==null&&b[1]<d)return out('STOP_TESTED_BENEFIT','Interval excludes the prespecified meaningful benefit; not universal inefficacy');
    if(b===null||d===null||hs.some(([i,m])=>i===null||m===null))return out('HOLD','Measurements or independently justified margins missing');
    if(b[0]<=d||hs.some(([i,m])=>i[1]>=m))return out('HOLD','Insufficient precision for benefit or noninferiority; nonsignificance is not safety');
    return out('PRECLINICAL_REVIEW_ONLY','All scoped criteria met; specialist review and additional scope qualification remain');
  }
  function materialize(data,current){return data.cases.map(c=>{
    const record=structuredClone(c.evidence==='current'?current:data.base_synthetic_record);
    Object.entries(c.patch).forEach(([p,v])=>{const k=p.split('.');let t=record;k.slice(0,-1).forEach(x=>t=t[x]);check(Object.hasOwn(t,k.at(-1)),'Unknown teaching-case field');t[k.at(-1)]=structuredClone(v);});
    return {case:c,record};
  });}
  function denominator(arm){
    check(keys(arm,['accurate_viable','erroneous_division','death','arrest','slippage','missing'])&&Object.values(arm).every(x=>Number.isInteger(x)&&x>=0),'Nonnegative integer outcome counts required');
    const n=Object.values(arm).reduce((a,b)=>a+b,0),d=arm.accurate_viable+arm.erroneous_division;
    check(n>0,'At least one enrolled cell required');
    return {enrolled:n,completed_divisions:d,error_fraction:d?arm.erroneous_division/d:null,observed_useful_fraction:arm.accurate_viable/n,missingness_bounds:[arm.accurate_viable/n,(arm.accurate_viable+arm.missing)/n],confidence_interval:false};
  }
  globalThis.Track2Demo={decide,materialize,denominator};
  if(typeof document==='undefined')return;
  const data=JSON.parse(document.getElementById('case-data').textContent),current=JSON.parse(document.getElementById('current-data').textContent);
  const rows=materialize(data,current),select=document.getElementById('case-select');
  const el=(tag,text)=>{const e=document.createElement(tag);e.textContent=text;return e;};
  const human=x=>x.replaceAll('_',' ');
  const labels={HOLD:'Hold advancement',INVALID_HOLD:'Invalid assay or plan: hold inference',STOP_SAFETY_REVIEW:'Stop advancement; review injury',STOP_BRANCH:'Stop this branch',STOP_TESTED_BENEFIT:'Stop the tested benefit claim',PRECLINICAL_REVIEW_ONLY:'Preclinical review only'};
  rows.forEach(({case:c})=>{const o=el('option',c.title);o.value=c.id;select.append(o);});
  let selected;
  function render(){
    selected=rows.find(x=>x.case.id===select.value);const r=selected.record,d=decide(r);
    document.getElementById('kind').textContent=r.evidence_kind==='not_measured'?'Actual research state: unmeasured':'Invented teaching case: synthetic';
    const decision=document.getElementById('decision');decision.textContent=labels[d.decision];decision.dataset.decision=d.decision;decision.dataset.state=d.decision.startsWith('STOP')?'stop':d.decision.startsWith('PRECLINICAL')?'review':'hold';
    document.getElementById('reason').textContent=selected.case.explanation;
    document.getElementById('policy-reason').textContent=d.reason;
    const body=document.getElementById('gate-rows');body.replaceChildren();
    Object.entries(r.gates).forEach(([name,value])=>{const tr=el('tr','');tr.append(el('td',human(name)),el('td',value));body.append(tr);});
    const evidence=document.getElementById('endpoint-rows');evidence.replaceChildren();
    [['benefit',r.benefit],...Object.entries(r.harms)].forEach(([name,v])=>{const tr=el('tr','');tr.append(el('td',human(name)),el('td',v.interval===null?'Unmeasured':v.interval.join(' to ')),el('td',v.margin===null?'Unjustified':String(v.margin)));evidence.append(tr);});
    document.getElementById('record').textContent=JSON.stringify({input:r,output:d},null,2);
  }
  select.addEventListener('change',render);render();
  document.getElementById('reset').addEventListener('click',()=>{select.value='current';render();select.focus();});
  document.getElementById('download').addEventListener('click',()=>{
    const body={notice:data.purpose,case_id:selected.case.id,record:selected.record,decision:decide(selected.record)};
    const u=URL.createObjectURL(new Blob([JSON.stringify(body,null,2)+'\n'],{type:'application/json'}));
    const a=document.createElement('a');a.href=u;a.download='research-teaching-'+selected.case.id+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);
  });
  for(const [name,arm]of Object.entries(data.denominator_example).filter(([n])=>['vehicle','drug'].includes(n))){
    const grid=document.getElementById(name+'-cells');
    Object.entries(arm).forEach(([category,count])=>{for(let n=0;n<count;n++){const cell=el('i','');cell.className=category;cell.setAttribute('aria-hidden','true');grid.append(cell);}});
  }
  function recover(){
    const v=Number(document.getElementById('recover-vehicle').value),d=Number(document.getElementById('recover-drug').value);
    document.getElementById('recovery-result').textContent=`If ${v} missing vehicle and ${d} missing drug outcomes were useful, output would be ${60+v}/100 versus ${40+d}/100. Difference: ${40+d-60-v} percentage points.`;
  }
  ['recover-vehicle','recover-drug'].forEach(id=>document.getElementById(id).addEventListener('input',recover));recover();
})();
