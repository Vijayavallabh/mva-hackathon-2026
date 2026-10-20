#!/usr/bin/env node
// Local-only preview of the fixed public-safe v36 deck. No project env or subject inputs.
// Node >=22 and installed Chrome; output must be a new direct feat009 child directory.
import { spawn, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { once } from 'node:events';
import { readFile, writeFile, mkdir, mkdtemp, lstat } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const kind=process.argv[3]??'demo';
if(!['demo','prompter'].includes(kind))throw new Error('Unknown interactive');
const source = path.join(root, `notes/track2-${kind==='demo'?'demo-v37':'teleprompter-v46'}.html`);
const rendererPath = fileURLToPath(import.meta.url);
const outputName = process.argv[2];
if (![3,4].includes(process.argv.length) || !/^[a-z][a-z0-9-]+$/.test(outputName ?? '')) {
  throw new Error('Usage: node scripts/review_track2_interactive_v46.mjs NEW-OUTPUT-NAME [demo|prompter]');
}
const outputRoot = path.join(root, 'results/feat009');
for (const target of [root, path.join(root, 'results'), outputRoot,
  path.join(root, 'notes'), path.join(root, 'scripts'), source, rendererPath,
  path.join(root, 'scripts/build_track2_demo_v37.py')]) {
  if ((await lstat(target)).isSymbolicLink()) throw new Error('Symlinked input/output parent');
}
if (!(await lstat(source)).isFile() || !(await lstat(rendererPath)).isFile())
  throw new Error('Deck and renderer must be regular files');
const sourceBytes=await readFile(source),rendererBytes=await readFile(rendererPath);
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const buildScript=kind==='demo'?'build_track2_demo_v37.py':'build_track2_recording_v46.py';
const validation=spawnSync('/home/sports/.local/bin/uv',['run','--offline','--no-project','python','scripts/'+buildScript,'--check'],{cwd:root,env:{PATH:'/usr/bin:/bin',LANG:'C.UTF-8'},encoding:'utf8',timeout:30000});
if(validation.status!==0)throw new Error('Generated input check failed: '+validation.stderr);
const output = path.join(outputRoot, outputName);
await mkdir(output); // exclusive: never overwrite a review or release
const profile = await mkdtemp(path.join(tmpdir(), 'mva-v40-interactive-'));
const renderSource = path.join(profile, 'interactive.html');
await writeFile(renderSource, sourceBytes, { flag: 'wx', mode: 0o444 });
const browser = spawn('/usr/bin/google-chrome', [
  '--headless', '--disable-gpu', '--disable-background-networking', '--no-first-run',
  '--no-default-browser-check', '--hide-scrollbars', '--host-resolver-rules=MAP * ~NOTFOUND',
  '--proxy-server=http://127.0.0.1:9', '--proxy-bypass-list=<-loopback>',
  '--remote-debugging-port=0', '--remote-debugging-address=127.0.0.1',
  `--user-data-dir=${profile}`, 'about:blank',
], { cwd: profile, env: { PATH: '/usr/bin:/bin', LANG: 'C.UTF-8' }, stdio: 'ignore', detached: true });
let spawnError;
browser.on('error', error => { spawnError = error; });
let socket;
let transportError;
let nextId = 0;
const pending = new Map();
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
const call = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
  if (transportError) { reject(transportError); return; }
  if (socket?.readyState !== WebSocket.OPEN) { reject(new Error('CDP connection is not open')); return; }
  const id = ++nextId;
  const timer = setTimeout(() => { pending.delete(id); reject(new Error(`CDP timeout: ${method}`)); }, 15000);
  pending.set(id, { resolve, reject, timer });
  socket.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));
});
try {
  let active;
  for (let attempt = 0; attempt < 100; attempt++) {
    if (spawnError) throw spawnError;
    if (browser.exitCode !== null) throw new Error('Chrome exited before local debugging was ready');
    try { active = await readFile(path.join(profile, 'DevToolsActivePort'), 'utf8'); break; }
    catch (error) { if (error.code !== 'ENOENT') throw error; }
    await delay(100);
  }
  if (!active) throw new Error('Chrome startup timed out');
  const [port, endpoint] = active.trim().split('\n');
  if (!/^\d{1,5}$/.test(port) || +port < 1 || +port > 65535 ||
      !/^\/devtools\/browser\/[a-z0-9-]+$/.test(endpoint)) throw new Error('Invalid local endpoint');
  socket = new WebSocket(`ws://127.0.0.1:${port}${endpoint}`);
  await Promise.race([once(socket, 'open'), delay(10000).then(() => { throw new Error('CDP connection timeout'); })]);
  const failTransport = error => {
    transportError = error;
    for (const request of pending.values()) { clearTimeout(request.timer); request.reject(error); }
    pending.clear();
  };
  socket.addEventListener('error', () => failTransport(new Error('Local CDP transport failed')));
  socket.addEventListener('close', () => failTransport(new Error('Local CDP transport closed')));
  socket.addEventListener('message', event => {
    let message;
    try { message = JSON.parse(event.data); }
    catch { failTransport(new Error('Invalid local CDP response')); return; }
    if (!message || typeof message !== 'object' || Array.isArray(message)) {
      failTransport(new Error('Invalid local CDP response shape')); return;
    }
    const request = pending.get(message.id);
    if (!request) return;
    pending.delete(message.id); clearTimeout(request.timer);
    if (message.error) request.reject(new Error(message.error.message));
    else request.resolve(message.result);
  });
  const { targetId } = await call('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await call('Target.attachToTarget', { targetId, flatten: true });
  const page = (method, params) => call(method, params, sessionId);

  await page('Emulation.setDeviceMetricsOverride',{width:1280,height:900,deviceScaleFactor:1,mobile:false});
  await page('Page.enable');await page('Network.enable');
  await page('Network.setBlockedURLs',{urls:['http://*','https://*','ws://*','wss://*']});
  const nav=await page('Page.navigate',{url:pathToFileURL(renderSource).href});
  if(nav.errorText)throw new Error(nav.errorText);
  const evaluate=async expression=>{const r=await page('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
  for(let i=0;i<50;i++){if(await evaluate("document.readyState==='complete'"))break;await delay(100);}
  const files={},checks={};
  async function shot(name){const r=await page('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});const b=Buffer.from(r.data,'base64');await writeFile(path.join(output,name),b,{flag:'wx'});files[name]=hash(b);}
  await shot('desktop.png');
  if(kind==='demo'){
    checks.current=await evaluate("({decision:document.getElementById('decision').dataset.decision,cells:document.querySelectorAll('.cells i').length,cases:document.getElementById('case-select').options.length})");
    if(checks.current.decision!=='HOLD'||checks.current.cells!==200||checks.current.cases!==18)throw new Error('Current demo state differs');
    checks.cases=await evaluate("JSON.parse(document.getElementById('case-data').textContent).cases.map(c=>{const s=document.getElementById('case-select');s.value=c.id;s.dispatchEvent(new Event('change'));return {id:c.id,decision:document.getElementById('decision').dataset.decision,expected:c.expected}})");
    if(checks.cases.some(c=>c.decision!==c.expected))throw new Error('Browser case mismatch');
    await evaluate("document.getElementById('case-select').value='injury';document.getElementById('case-select').dispatchEvent(new Event('change'));document.getElementById('cases').scrollIntoView();true");
    await shot('injury-case.png');
    await evaluate("document.getElementById('reset').click();true");
    checks.reset=await evaluate("document.getElementById('decision').dataset.decision==='HOLD'&&document.activeElement.id==='case-select'");
    if(!checks.reset)throw new Error('Reset/focus failed');
    checks.download=await evaluate("(()=>{let saved;const prior=URL.createObjectURL;URL.createObjectURL=b=>{saved=b;return prior(b)};document.getElementById('download').click();URL.createObjectURL=prior;return saved.text().then(t=>JSON.parse(t))})()");
    if(checks.download.case_id!=='current'||checks.download.decision.clinical_recommendation!==false)throw new Error('Download record differs');
  }else{
    checks.timing=await evaluate("[0,18,40,63,87,106,126,149,168,180].map(t=>{Track2Pitch.seek(t);return {seconds:t,slide:Track2Pitch.state().slide}})");
    if(checks.timing.map(x=>x.slide).join(',')!=='1,2,3,4,5,6,7,8,9,9')throw new Error('Slide timing differs');
    await evaluate('Track2Pitch.seek(0);true');
    await page('Input.dispatchKeyEvent',{type:'keyDown',key:' ',code:'Space',windowsVirtualKeyCode:32});
    await delay(250);
    await page('Input.dispatchKeyEvent',{type:'keyDown',key:' ',code:'Space',windowsVirtualKeyCode:32});
    checks.keyboard=await evaluate('Track2Pitch.state()');
    if(checks.keyboard.running||checks.keyboard.elapsed<=0)throw new Error('Keyboard pause failed');
  }
  const metrics=()=>evaluate("({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,buttons:[...document.querySelectorAll('button')].map(x=>({text:x.textContent,height:x.getBoundingClientRect().height})),labelledControls:[...document.querySelectorAll('select,input')].every(x=>document.querySelector('label[for=\"'+x.id+'\"]')),networkResources:performance.getEntriesByType('resource').filter(x=>/^https?:/.test(x.name)).length})");
  async function cueVisibility(){
    const rows=await evaluate("[0,18,40,63,87,106,126,149,168].map(t=>{Track2Pitch.seek(t);return {seconds:t,top:document.querySelector('article.active').getBoundingClientRect().top,headerBottom:document.querySelector('header').getBoundingClientRect().bottom}})");
    if(rows.some(r=>r.top<r.headerBottom))throw new Error('Active cue hidden by sticky header');
    return rows;
  }
  checks.desktop=await metrics();
  if(kind==='prompter')checks.desktopCues=await cueVisibility();
  await page('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:false});
  await evaluate('scrollTo(0,0);true');checks.mobile=await metrics();
  if(kind==='prompter'){checks.mobileCues=await cueVisibility();await evaluate('Track2Pitch.seek(18);true');await shot('mobile-cue-2.png');await evaluate('Track2Pitch.seek(0);scrollTo(0,0);true');}
  await shot('mobile.png');
  if([checks.desktop,checks.mobile].some(m=>m.scrollWidth>m.width||m.networkResources!==0||!m.labelledControls||m.buttons.some(b=>b.height<44)))throw new Error('Responsive/control/network check failed');
  if(hash(await readFile(source))!==hash(sourceBytes))throw new Error('Interactive changed during review');
  const audit={passed:true,kind,source_sha256:hash(sourceBytes),renderer_sha256:hash(rendererBytes),checks,files,browser:await call('Browser.getVersion'),network_blocked:true,independent_review:false,formal_accessibility_audit:false,clinical_validation:false};
  await writeFile(path.join(output,'audit.json'),JSON.stringify(audit,null,2)+'\n',{flag:'wx'});
  console.log(JSON.stringify({passed:true,kind,output,files:Object.keys(files)}));
} finally {
  for (const request of pending.values()) { clearTimeout(request.timer); request.reject(new Error('Renderer closing')); }
  pending.clear();
  if (socket) socket.close();
  if (Number.isInteger(browser.pid) && browser.pid > 0) {
    const signalGroup = signal => {
      try { process.kill(-browser.pid, signal); return true; }
      catch (error) { if (error.code === 'ESRCH') return false; throw error; }
    };
    signalGroup('SIGTERM');
    for (let i = 0; i < 30 && signalGroup(0); i++) await delay(100);
    if (signalGroup(0)) signalGroup('SIGKILL');
    for (let i = 0; i < 30 && browser.exitCode === null && browser.signalCode === null; i++) await delay(100);
    if (browser.exitCode === null && browser.signalCode === null) throw new Error('Owned Chrome did not exit');
  }
  // Temporary public-page-only profile retained for audit; no unrelated profile touched.
}
