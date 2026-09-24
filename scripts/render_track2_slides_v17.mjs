#!/usr/bin/env node
// Local-only preview of the fixed public-safe v17 deck. No project env or subject inputs.
// Node >=22 and installed Chrome; output must be a new direct feat009 child directory.
import { spawn, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { once } from 'node:events';
import { readFile, writeFile, mkdir, mkdtemp, lstat } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(root, 'notes/track2-slides-v17.html');
const rendererPath = fileURLToPath(import.meta.url);
const outputName = process.argv[2];
if (process.argv.length !== 3 || !/^[a-z][a-z0-9-]+$/.test(outputName ?? '')) {
  throw new Error('Usage: node scripts/render_track2_slides_v17.mjs NEW-OUTPUT-NAME');
}
const outputRoot = path.join(root, 'results/feat009');
for (const target of [root, path.join(root, 'results'), outputRoot,
  path.join(root, 'notes'), path.join(root, 'scripts'), source, rendererPath,
  path.join(root, 'scripts/track2_public_review_v17.py')]) {
  if ((await lstat(target)).isSymbolicLink()) throw new Error('Symlinked input/output parent');
}
if (!(await lstat(source)).isFile() || !(await lstat(rendererPath)).isFile())
  throw new Error('Deck and renderer must be regular files');
const validation = spawnSync('/home/sports/.local/bin/uv',
  ['run', '--offline', '--no-project', 'python', '-c', 'import sys,json;sys.path.insert(0,"scripts");import track2_public_review_v17 as r;print(json.dumps(r.check_deck()))'],
  { cwd: root, env: { PATH: '/usr/bin:/bin', LANG: 'C.UTF-8', UV_OFFLINE: '1' },
    encoding: 'utf8', timeout: 30000, maxBuffer: 1024 * 1024 });
if (validation.error || validation.status !== 0)
  throw new Error(`Static deck validation failed before browser launch: ${validation.stderr || validation.error}`);
const sourceBytes = await readFile(source);
const rendererBytes = await readFile(rendererPath);
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const checked = JSON.parse(validation.stdout);
if (checked.static_deck_verified !== true || checked.source_sha256 !== hash(sourceBytes))
  throw new Error('Deck changed after static validation');
const output = path.join(outputRoot, outputName);
await mkdir(output); // exclusive: never overwrite a review or release
const profile = await mkdtemp(path.join(tmpdir(), 'mva-v17-render-'));
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
  await page('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
  await page('Page.enable');
  await page('Network.enable');
  await page('Network.setBlockedURLs', { urls: ['http://*', 'https://*', 'ws://*', 'wss://*'] });
  await page('Emulation.setScriptExecutionDisabled', { value: true });
  const navigation = await page('Page.navigate', { url: pathToFileURL(renderSource).href });
  if (navigation.errorText) throw new Error('Local deck navigation failed');
  let complete = false;
  for (let attempt = 0; attempt < 50; attempt++) {
    const check = await page('Runtime.evaluate', { expression: "document.readyState === 'complete' && document.querySelectorAll('section.slide').length === 8", returnByValue: true });
    if (check.result.value === true) { complete = true; break; }
    await delay(100);
  }
  if (!complete) throw new Error('Deck did not load eight slides');
  const geometry = await page('Runtime.evaluate', {
    expression: `Array.from(document.querySelectorAll('section.slide')).map(section => {
      const rect = section.getBoundingClientRect();
      const walker = document.createTreeWalker(section, NodeFilter.SHOW_TEXT);
      const outside = []; const textBoxes = []; const fontSizes = []; let words = 0; let node;
      while (node = walker.nextNode()) {
        if (!node.textContent.trim()) continue;
        const range = document.createRange(); range.selectNodeContents(node);
        const boxes = [...range.getClientRects()].filter(box => box.width > 0 && box.height > 0);
        if (boxes.length) {
          words += node.textContent.trim().split(/\\s+/).length;
          fontSizes.push(parseFloat(getComputedStyle(node.parentElement).fontSize));
        }
        for (const box of boxes) {
          textBoxes.push({text:node.textContent.trim().slice(0,80),left:box.left,right:box.right,top:box.top,bottom:box.bottom});
          if (box.left < rect.left || box.right > rect.right || box.top < rect.top || box.bottom > rect.bottom)
            outside.push(node.textContent.trim().slice(0, 80));
        }
      }
      const overlaps = [];
      for (let a=0; a<textBoxes.length; a++) for(let b=a+1; b<textBoxes.length; b++){
        const x=textBoxes[a], y=textBoxes[b];
        if (Math.min(x.right,y.right)-Math.max(x.left,y.left)>2 &&
            Math.min(x.bottom,y.bottom)-Math.max(x.top,y.top)>2)
          overlaps.push([x.text,y.text]);
      }
      return {id:section.id,x:rect.x + scrollX,y:rect.y + scrollY,width:rect.width,height:rect.height,
        outside,overlaps,visible_words:words,min_font_px:Math.min(...fontSizes),
        svg_figures:section.querySelectorAll('svg[role="img"]').length};
    })`, returnByValue: true,
  });
  if (geometry.exceptionDetails) throw new Error('Layout inspection failed');
  const slides = geometry.result.value;
  const files = {};
  for (const [index, slide] of slides.entries()) {
    if (slide.id !== `slide-${index + 1}` || slide.width !== 1280 || slide.height !== 720 || slide.outside.length || slide.overlaps.length || slide.min_font_px < 24 || slide.svg_figures !== (index < 7 ? 1 : 0))
      throw new Error(`Unexpected layout in slide ${index + 1}: ${JSON.stringify(slide)}`);
    const capture = await page('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
      clip: { x: slide.x, y: slide.y, width: slide.width, height: slide.height, scale: 1 } });
    const bytes = Buffer.from(capture.data, 'base64');
    const name = `${slide.id}.png`;
    await writeFile(path.join(output, name), bytes, { flag: 'wx' });
    files[name] = hash(bytes);
  }
  await page('Emulation.setDeviceMetricsOverride', { width: 640, height: 720, deviceScaleFactor: 1, mobile: false });
  const narrowCheck = await page('Runtime.evaluate', { expression:
    "({width:document.querySelector('section.slide').getBoundingClientRect().width,scrollWidth:document.documentElement.scrollWidth})",
    returnByValue: true });
  const narrow = narrowCheck.result.value;
  if (narrowCheck.exceptionDetails || Math.abs(narrow.width - 640) > 1 || narrow.scrollWidth > 641)
    throw new Error(`Narrow-screen layout failed: ${JSON.stringify(narrow)}`);
  await page('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
  // Print the same local source with page-size CSS; no web assets or narration.
  await page('Emulation.setEmulatedMedia', { media: 'print' });
  const pdf = await page('Page.printToPDF', { printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: false, marginTop: 0, marginBottom: 0, marginLeft: 0, marginRight: 0 });
  const pdfBytes = Buffer.from(pdf.data, 'base64');
  await writeFile(path.join(output, 'track2-slides-v17.pdf'), pdfBytes, { flag: 'wx' });
  files['track2-slides-v17.pdf'] = hash(pdfBytes);
  if (hash(await readFile(source)) !== hash(sourceBytes)) throw new Error('Deck changed during rendering');
  if (hash(await readFile(rendererPath)) !== hash(rendererBytes)) throw new Error('Renderer changed during execution');
  const manifest = { source: 'notes/track2-slides-v17.html', source_sha256: hash(sourceBytes),
    renderer_sha256: hash(rendererBytes),
    browser: await call('Browser.getVersion'), slides, narrow_screen: narrow, files,
    temporary_profile: { path: profile, retained: true, contents: 'isolated public-deck browser profile; no login or subject input' },
    limits: 'Geometry and screenshots are preview checks, not recording, runtime validation, scientific validity or upload readiness.' };
  await writeFile(path.join(output, 'render.json'), JSON.stringify(manifest, null, 2) + '\n', { flag: 'wx' });
  console.log(JSON.stringify({ output, slides: slides.length, text_outside_slides: 0, text_overlaps: 0, visible_words: slides.map(s => s.visible_words), source_sha256: manifest.source_sha256 }));
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
