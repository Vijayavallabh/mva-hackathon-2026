#!/usr/bin/env node
// Local-only preview of the prepared public-safe v18 report. No project env or subject inputs.
// Node >=22 and installed Chrome; output must be the prepared document directory; PDFs are never overwritten.
import { spawn, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { once } from 'node:events';
import { readFile, writeFile, mkdir, mkdtemp, lstat } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const outputName = process.argv[2];
if (process.argv.length !== 3 || !/^[a-z][a-z0-9-]+$/.test(outputName ?? ''))
  throw new Error('Usage: node scripts/render_track2_report_v18.mjs EXISTING-DOCUMENT-OUTPUT-NAME');
const output = path.join(root, 'results/feat009', outputName);
const source = path.join(output, 'jvv7_track2_report_v18.html');
const rendererPath = fileURLToPath(import.meta.url);
const outputRoot = path.join(root, 'results/feat009');
for (const target of [root, path.join(root, 'results'), outputRoot,
  path.join(root, 'notes'), path.join(root, 'scripts'), source, rendererPath,
  path.join(root, 'scripts/track2_public_review_v18.py')]) {
  if ((await lstat(target)).isSymbolicLink()) throw new Error('Symlinked input/output parent');
}
if (!(await lstat(source)).isFile() || !(await lstat(rendererPath)).isFile())
  throw new Error('Deck and renderer must be regular files');
const sourceBytes = await readFile(source);
const rendererBytes = await readFile(rendererPath);
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const documents = JSON.parse(await readFile(path.join(output, 'documents.json'), 'utf8'));
if (documents.files['jvv7_track2_report_v18.html'] !== hash(sourceBytes) ||
    documents.report_sha256 !== hash(await readFile(path.join(root,'notes/track2-report-v18.md'))))
  throw new Error('Prepared report/source hash mismatch');
if (/<(?:script|iframe|img|object|embed)\b/i.test(sourceBytes.toString('utf8')))
  throw new Error('Active or remote report element');
const profile = await mkdtemp(path.join(tmpdir(), 'mva-v18-render-'));
const renderSource = path.join(profile, 'deck.html');
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
  await page('Emulation.setDeviceMetricsOverride', { width: 665, height: 940, deviceScaleFactor: 1, mobile: false });
  await page('Page.enable');
  await page('Network.enable');
  await page('Network.setBlockedURLs', { urls: ['http://*', 'https://*', 'ws://*', 'wss://*'] });
  await page('Emulation.setScriptExecutionDisabled', { value: true });
  const navigation = await page('Page.navigate', { url: pathToFileURL(renderSource).href });
  if (navigation.errorText) throw new Error('Local deck navigation failed');
  let complete = false;
  for (let attempt = 0; attempt < 50; attempt++) {
    const check = await page('Runtime.evaluate', { expression: "document.readyState === 'complete' && document.querySelectorAll('main h1').length === 1", returnByValue: true });
    if (check.result.value === true) { complete = true; break; }
    await delay(100);
  }
  if (!complete) throw new Error('Report did not load');
  const inspect = await page('Runtime.evaluate', { expression:
    "({width:document.documentElement.clientWidth,scrollWidth:document.documentElement.scrollWidth,links:document.querySelectorAll('a[href]').length,headings:document.querySelectorAll('h2').length,tables:document.querySelectorAll('table').length})",
    returnByValue:true });
  if (inspect.exceptionDetails || inspect.result.value.scrollWidth > 666)
    throw new Error('Report horizontal overflow');
  const geometry = inspect.result.value;
  const files = {};
  // Print the same local source with page-size CSS; no web assets or narration.
  await page('Emulation.setEmulatedMedia', { media: 'print' });
  const pdf = await page('Page.printToPDF', { printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="width:100%;font-family:Arial;font-size:8px;color:#655b70;padding:0 48px;display:flex;justify-content:space-between"><span>jvv7 · Track 2 v18 · Research hypothesis</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>'  });
  const pdfBytes = Buffer.from(pdf.data, 'base64');
  await writeFile(path.join(output, 'jvv7_track2_report_v18.pdf'), pdfBytes, { flag: 'wx' });
  files['jvv7_track2_report_v18.pdf'] = hash(pdfBytes);
  if (hash(await readFile(source)) !== hash(sourceBytes)) throw new Error('Deck changed during rendering');
  if (hash(await readFile(rendererPath)) !== hash(rendererBytes)) throw new Error('Renderer changed during execution');
  const manifest = {source:'notes/track2-report-v18.md', source_sha256:documents.report_sha256,
    html_sha256:hash(sourceBytes), renderer_sha256:hash(rendererBytes),
    exporter_sha256:documents.script_sha256, browser:await call('Browser.getVersion'),
    geometry, files, limits:'PDF export and geometry; no scientific, licensing, recording or upload certification.'};
  await writeFile(path.join(output,'report-render.json'),JSON.stringify(manifest,null,2)+'\n',{flag:'wx'});
  console.log(JSON.stringify({output,pdf:'jvv7_track2_report_v18.pdf',geometry,source_sha256:documents.report_sha256}));

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
