#!/usr/bin/env node
// Project-local K-Dense entry point. No parent .env or ambient provider keys.
import fs from 'node:fs';
import path from 'node:path';
import net from 'node:net';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const app = path.join(root, 'tools/k-dense-byok');
const mode = process.argv[2] ?? 'start';
if (!['start', 'install', 'check', 'prep'].includes(mode) || process.argv.length > 3) {
  console.error('Usage: node scripts/k-dense.mjs [start|install|check|prep]');
  process.exit(2);
}
if (!fs.existsSync(path.join(app, 'package.json'))) {
  console.error('Clone K-Dense into tools/k-dense-byok first; see notes/k-dense-installation.md.');
  process.exit(1);
}
process.umask(0o077);
const env = Object.fromEntries(['HOME', 'PATH', 'TERM', 'LANG'].filter(k => process.env[k]).map(k => [k, process.env[k]]));
for (const [key, relative] of Object.entries({
  PI_CODING_AGENT_DIR: '.local/pi-agent',
  KADY_PI_AGENT_DIR: '.local/pi-agent',
  KADY_SKILLS_CACHE_DIR: '.cache/skills',
  KADY_PROJECTS_ROOT: 'projects',
  XDG_CACHE_HOME: '.cache',
  XDG_CONFIG_HOME: '.local/config',
  XDG_DATA_HOME: '.local/share',
  XDG_STATE_HOME: '.local/state',
  npm_config_cache: '.cache/npm',
  UV_CACHE_DIR: '.cache/uv',
  UV_PYTHON_INSTALL_DIR: '.local/python',
  UV_TOOL_DIR: '.local/uv-tools',
  UV_TOOL_BIN_DIR: '.local/bin',
  TMPDIR: '.cache/tmp',
})) {
  env[key] = path.join(app, relative);
  fs.mkdirSync(env[key], { recursive: true });
}
Object.assign(env, {
  KADY_HOST: '127.0.0.1', KADY_PORT: '8210', KADY_FRONTEND_PORT: '3210',
  NEXT_PUBLIC_ADK_API_URL: 'http://localhost:8210',
  NEXT_TELEMETRY_DISABLED: '1', DO_NOT_TRACK: '1',
});
const children = [];
let stopping = false;
function launch(command, args, dir, detached = false) {
  const child = spawn(command, args, { cwd: path.join(app, dir), env, stdio: 'inherit', detached });
  child.on('error', error => { console.error(error.message); shutdown(1); });
  return child;
}
function run(command, args, dir = '') {
  return new Promise((resolve, reject) => {
    const child = launch(command, args, dir);
    child.on('error', reject);
    child.on('exit', code => code === 0 ? resolve() : reject(new Error(`${command} exited ${code}`)));
  });
}
function shutdown(code) {
  if (stopping) return;
  stopping = true;
  for (const child of children) {
    try { process.kill(-child.pid, 'SIGTERM'); } catch {}
  }
  setTimeout(() => {
    for (const child of children) {
      try { process.kill(-child.pid, 'SIGKILL'); } catch {}
    }
    process.exit(code);
  }, 2500);
}
try {
  if (mode === 'install') {
    for (const dir of ['server', 'web']) await run('npm', ['ci', '--no-audit', '--no-fund'], dir);
    await run('npm', ['run', 'prep'], 'server');
  } else if (mode === 'prep') {
    await run('npm', ['run', 'prep'], 'server');
  } else if (mode === 'check') {
    for (const file of ['server/node_modules/.bin/tsx', 'web/node_modules/.bin/next']) {
      fs.accessSync(path.join(app, file), fs.constants.X_OK);
    }
    await run('node', ['start.mjs', '--check']);
    console.log('Project-local dependencies present; UI port 3210, backend port 8210.');
  } else {
    // Refuse occupied ports; never terminate another application's listener.
    for (const port of [3210, 8210]) {
      await new Promise((resolve, reject) => {
        const probe = net.createServer();
        probe.once('error', reject);
        probe.listen(port, '127.0.0.1', () => probe.close(resolve));
      });
    }
    for (const signal of ['SIGINT', 'SIGTERM', 'SIGHUP']) process.on(signal, () => shutdown(0));
    children.push(launch('npm', ['run', 'start'], 'server', true));
    children.push(launch('npm', ['run', 'dev', '--', '--hostname', '127.0.0.1', '--port', '3210'], 'web', true));
    for (const child of children) child.on('exit', code => { if (!stopping) shutdown(code || 1); });
    console.log('K-Dense starting: http://localhost:3210 — Ctrl+C stops both services.');
  }
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
