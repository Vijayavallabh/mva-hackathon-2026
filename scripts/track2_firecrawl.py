#!/usr/bin/env python3
"""Bounded public-literature client for the owner's local Firecrawl MCP.

This is a real STDIO MCP connection, not a substitute REST implementation.
No subject files, credentials, global config changes, arbitrary URLs or shell input.
The local service can use externally hosted models; see the disclosure note.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import selectors
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENTRY = Path('/home/sports/.npm/_npx/12b05d58670d8359/node_modules/firecrawl-mcp/dist/index.js')
MAX_RESPONSE = 2_000_000
MAX_CALLS = 120
SCRIPT_BYTES = Path(__file__).read_bytes()
SCRIPT_SHA = hashlib.sha256(SCRIPT_BYTES).hexdigest()
PUBLIC_GENE = 'https://medlineplus.gov/genetics/gene/bub1b/'
JCI = 'https://www.jci.org/articles/view/126863'
QUERIES = [
    ('bubr1_rescue', 'BUBR1 BUB1B pharmacological rescue chromosome segregation rapamycin'),
    ('bubr1_stability', 'BUBR1 protein stability approved drug SIRT2 NAD rescue'),
    ('mva_treatment', '"mosaic variegated aneuploidy" treatment drug'),
    ('rapalog_negative', 'rhabdomyosarcoma everolimus temsirolimus randomized ARST1431 trial negative'),
    ('repurpose_rms', 'rhabdomyosarcoma drug repurposing mebendazole disulfiram statin digoxin'),
    ('rms_new', 'rhabdomyosarcoma approved drug repurposing 2025 2026'),
    ('normal_risk', 'aneuploidy normal cells mTOR inhibition chromosome instability rapamycin'),
    ('mtor_compensation', 'rhabdomyosarcoma everolimus resistance feedback IL17A secukinumab'),
    ('hcq_window', 'hydroxychloroquine rhabdomyosarcoma pharmacokinetics normal skeletal muscle'),
    ('rms_azole', 'posaconazole rhabdomyosarcoma hedgehog drug repurposing'),
    ('bubr1_correction', '"BubR1 allelic effects" correction retraction'),
    ('readthrough', 'BUB1B nonsense readthrough ataluren gentamicin rescue'),
]


def own_monitor_projection(value, ident):
    data = value.get('data', []) if isinstance(value, dict) else []
    if isinstance(data, dict):
        data = data.get('monitors', [])
    if not isinstance(data, list):
        raise ValueError('Invalid monitor list')
    return {'own_monitor_found': any(x.get('id') == ident for x in data if isinstance(x, dict))}


def data_of(result):
    return result['data'] if result.get('status') == 'ok' and isinstance(result.get('data'), dict) else {}


def research(client):
    for label, query in QUERIES:
        client.call('search_' + label, 'firecrawl_search', {'query': query, 'limit': 8})
    for label, query in [QUERIES[0], QUERIES[4], QUERIES[6], QUERIES[8]]:
        client.call('papers_' + label, 'firecrawl_research_search_papers', {'query': query, 'k': 12})
    for label, doi in [('bubr1', '10.1172/JCI126863'), ('rapalog', '10.1016/S1470-2045(24)00255-9')]:
        client.call('inspect_' + label, 'firecrawl_research_inspect_paper', {'paperId': 'doi:' + doi})
        for mode in ['citers', 'references']:
            client.call('related_' + label + '_' + mode, 'firecrawl_research_related_papers', {
                'seed_ids': ['doi:' + doi], 'intent': 'BUBR1 deficiency or rhabdomyosarcoma therapeutic rescue, negative trials, toxicity and mTOR',
                'mode': mode, 'rerank': True, 'k': 12})
    for label, doi, question in [
        ('bubr1', '10.1172/JCI126863', 'Which allele, tissue and genotype had mTORC1 activation, and was rapamycin or everolimus rescue experimentally tested?'),
        ('rapalog', '10.1016/S1470-2045(24)00255-9', 'What were the primary randomized comparison, hazard ratio, confidence interval and toxicity findings?'),
        ('secukinumab', '10.1158/1535-7163.MCT-23-0342', 'Which cell lines and xenografts were rhabdomyosarcoma versus other sarcomas? What dose, controls, response and normal-tissue safety were measured?'),
        ('north', '10.15252/embj.201386907', 'Which intervention increased BubR1 protein and which intervention extended mouse lifespan? Were these the same experiment?'),
    ]:
        client.call('read_' + label, 'firecrawl_research_read_paper', {'paperId': 'doi:' + doi, 'question': question, 'k': 8})
    client.call('github_reproducibility', 'firecrawl_research_search_github', {'query': 'rhabdomyosarcoma drug repurposing', 'k': 5})
    client.call('developer_provenance', 'firecrawl_developer_search', {'query': 'google-deepmind alphagenome variant scoring splice junction', 'k': 5})
    client.call('scrape_bubr1', 'firecrawl_scrape', {'url': JCI, 'formats': ['markdown', 'links'], 'onlyMainContent': True})
    client.call('scrape_correction', 'firecrawl_scrape', {'url': 'https://www.jci.org/articles/view/144781', 'formats': ['markdown'], 'onlyMainContent': True})


def followup(client):
    # Adaptive second pass: compound-specific queries after broad multi-compound noise.
    for name in ('pralatrexate', 'disulfiram', 'mebendazole', 'simvastatin', 'pyrvinium', 'posaconazole'):
        client.call('focused_' + name, 'firecrawl_search', {'query': 'rhabdomyosarcoma ' + name, 'limit': 6})
    for label, doi in [('pralatrexate', '10.1038/s41467-026-73749-y'),
                       ('disulfiram', '10.1002/ddr.70304'), ('statin', '10.3390/cancers16050853'),
                       ('sirt2_negative', '10.1111/acel.14027'), ('dimerizer', '10.1038/s41467-025-58185-8')]:
        client.call('inspect_' + label, 'firecrawl_research_inspect_paper', {'paperId': 'doi:' + doi})
        client.call('read_' + label, 'firecrawl_research_read_paper', {'paperId': 'doi:' + doi,
            'question': 'What was actually tested, in which models, with what controls, concentrations, survival or functional endpoints, and normal-cell toxicity? Distinguish drug identity, model subtype, cytostasis and rescue.', 'k': 6})
    client.call('scrape_pralatrexate', 'firecrawl_scrape', {'url': 'https://www.nature.com/articles/s41467-026-73749-y',
        'formats': ['markdown'], 'onlyMainContent': True})
    client.call('scrape_statin', 'firecrawl_scrape', {'url': 'https://www.mdpi.com/2072-6694/16/5/853',
        'formats': ['markdown'], 'onlyMainContent': True})


def capabilities(client):
    monitor_id = None
    interact_id = None
    try:
        search = data_of(client.call('scope_search', 'firecrawl_search', {
            'query': 'BUB1B mosaic variegated aneuploidy', 'limit': 5,
            'includeDomains': ['pubmed.ncbi.nlm.nih.gov', 'pmc.ncbi.nlm.nih.gov', 'nature.com']}))
        scrape = data_of(client.call('public_gene', 'firecrawl_scrape', {'url': PUBLIC_GENE,
            'formats': ['markdown', 'links', 'html'], 'onlyMainContent': True}))
        client.call('map_gene', 'firecrawl_map', {'url': 'https://medlineplus.gov/genetics/', 'search': 'BUB1B', 'limit': 5})
        crawl = data_of(client.call('crawl_gene', 'firecrawl_crawl', {'url': PUBLIC_GENE, 'limit': 1,
            'sitemap': 'skip', 'scrapeOptions': {'formats': ['markdown']}}, timeout=240))
        if crawl.get('id'):
            client.call('crawl_status', 'firecrawl_check_crawl_status', {'id': crawl['id']})
        if isinstance(scrape.get('html'), str) and len(scrape['html']) < MAX_RESPONSE:
            public_file = client.out / 'public-bub1b.html'
            # Only the HTML returned by the fixed public URL is eligible for local parse.
            public_file.write_text(scrape['html'])
            client.call('parse_public_gene', 'firecrawl_parse', {'filePath': str(public_file), 'formats': ['markdown', 'links']})
        web = search.get('data', {}).get('web', [])
        if search.get('id') and web:
            relevant = [x for x in web if 'bub1b' in (x.get('title', '') + x.get('description', '')).lower()]
            client.call('search_feedback', 'firecrawl_search_feedback', {'searchId': search['id'],
                'rating': 'good' if relevant else 'bad',
                'valuableSources': [{'url': x['url'], 'reason': 'Public BUB1B literature; discovery relevance only, not proof of drug response'} for x in relevant[:1]]})
        if scrape.get('metadata', {}).get('scrapeId'):
            client.call('scrape_feedback', 'firecrawl_feedback', {'endpoint': 'scrape',
                'jobId': scrape['metadata']['scrapeId'], 'rating': 'good' if 'BUB1B' in scrape.get('markdown', '') else 'bad',
                'url': PUBLIC_GENE, 'note': 'Public gene-page retrieval check, not scientific claim validation'})
        agent = data_of(client.call('agent_primary_audit', 'firecrawl_agent', {
            'urls': [JCI], 'prompt': 'Using only this public paper, identify the exact mouse allele and tissue with increased mTORC1 signaling. State whether rapamycin or everolimus was tested for rescue. Distinguish measured findings from hypotheses. Include the source URL. Do not infer patient treatment or efficacy.'}))
        if agent.get('id'):
            for i in range(12):
                result = data_of(client.call(f'agent_status_{i:02}', 'firecrawl_agent_status', {'id': agent['id']}))
                if result.get('status') in ('completed', 'failed', 'cancelled'):
                    break
                time.sleep(5)
        interact = data_of(client.call('interact_public_gene', 'firecrawl_interact', {
            'url': PUBLIC_GENE, 'code': 'agent-browser get title', 'language': 'bash', 'timeout': 30}, timeout=100))
        interact_id = interact.get('scrapeId')
        if interact_id:
            closed = client.call('interact_stop', 'firecrawl_interact_stop', {'scrapeId': interact_id})
            if closed['status'] == 'ok':
                interact_id = None
        monitor = data_of(client.call('monitor_create', 'firecrawl_monitor_create', {
            # The MCP advanced body REPLACES shorthand fields; it is not merged.
            'body': {'name': 'Track2 temporary public-source provenance check',
                     'targets': [{'type': 'scrape', 'urls': [PUBLIC_GENE]}],
                     'schedule': {'text': 'every day', 'timezone': 'UTC'},
                     'goal': 'Public BUB1B page baseline only, no efficacy claims',
                     'retentionDays': 2, 'judgeEnabled': False}}))
        monitor_id = monitor.get('data', {}).get('id')
        if monitor_id:
            client.call('monitor_list', 'firecrawl_monitor_list', {'limit': 100}, project=lambda x: own_monitor_projection(x, monitor_id))
            client.call('monitor_get', 'firecrawl_monitor_get', {'id': monitor_id})
            client.call('monitor_update', 'firecrawl_monitor_update', {'id': monitor_id, 'body': {'retentionDays': 2, 'name': 'Track2 temporary baseline; delete after check'}})
            run = data_of(client.call('monitor_run', 'firecrawl_monitor_run', {'id': monitor_id}))
            check_id = run.get('id') or run.get('data', {}).get('id')
            if check_id:
                for i in range(18):
                    check = data_of(client.call(f'monitor_check_{i:02}', 'firecrawl_monitor_check', {'id': monitor_id, 'checkId': check_id, 'limit': 5}))
                    if check.get('data', {}).get('status') in ('completed', 'partial', 'failed'):
                        break
                    time.sleep(5)
            client.call('monitor_checks', 'firecrawl_monitor_checks', {'id': monitor_id, 'limit': 5})
    finally:
        try:
            if interact_id:
                client.call('interact_cleanup', 'firecrawl_interact_stop', {'scrapeId': interact_id})
        finally:
            if monitor_id:
                result = client.call('monitor_delete', 'firecrawl_monitor_delete', {'id': monitor_id})
                client.manifest['temporary_monitor_deleted'] = data_of(result).get('success') is True
                client.manifest['deletion_semantics'] = 'soft deletion disables schedule, does not erase retained history'
            dump(client.out / 'manifest.json', client.manifest)


def now():
    return datetime.now(timezone.utc).isoformat()


def dump(path, value):
    # All destinations are in a new ignored run directory, never source datasets.
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    tmp.replace(path)


def child_env():
    return {'PATH': os.defpath, 'FIRECRAWL_API_URL': 'http://127.0.0.1:3002',
            'FIRECRAWL_SELF_HOSTED_DB_ENABLED': 'true',
            'FIRECRAWL_MCP_MAX_OUTPUT_CHARS': '400000', 'DO_NOT_TRACK': '1'}


def decode(response):
    if not isinstance(response, dict) or not isinstance(response.get('result'), dict):
        return {'status': 'tool_error', 'data': None}
    if response.get('error') or response.get('result', {}).get('isError'):
        return {'status': 'tool_error', 'data': None}
    result = response.get('result', {})
    if 'content' not in result:
        # All advertised tools in this deployment return MCP text blocks. Reject an
        # unsupported envelope rather than bypass error/truncation classification.
        return {'status': 'tool_error', 'data': None}
    if not isinstance(result['content'], list):
        return {'status': 'tool_error', 'data': None}
    if not all(isinstance(x, dict) and (x.get('type') != 'text' or isinstance(x.get('text'), str)) for x in result['content']):
        return {'status': 'tool_error', 'data': None}
    text = '\n'.join(x.get('text', '') for x in result['content'] if x.get('type') == 'text').strip()
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        value = text
    bad = (isinstance(value, dict) and (value.get('success') is False or value.get('error')
           or value.get('status') in ('failed', 'cancelled', 'error')))
    empty = value in ('', [], {}) or isinstance(value, str) and (
        '(no results)' in value or '(no full-text passages available' in value or '(paper not found)' in value)
    if isinstance(value, dict) and isinstance(value.get('data'), dict) and 'web' in value['data']:
        empty = not any(value['data'].get(k) for k in ('web', 'news', 'images'))
    if isinstance(value, dict) and not value.get('status') and any(value.get(k) == [] for k in ('data', 'papers', 'results')):
        empty = True
    truncated = (isinstance(value, str) and any(x in value.lower() for x in ('[truncated', 'output truncated', 'result truncated'))) or (
        isinstance(value, dict) and value.get('truncated') is True)
    return {'status': 'tool_error' if bad else 'empty' if empty else 'ok',
            'possible_truncation': bool(truncated), 'data': None if bad else value}


class MCP:
    def __init__(self, entry, out):
        if not entry.is_file() or entry.is_symlink() or entry.name != 'index.js':
            raise ValueError('Expected an existing local MCP index.js; no automatic installation')
        package_version = json.loads((entry.parent.parent / 'package.json').read_text())['version']
        self.out = out
        self.buffer = b''
        self.sequence = 0
        self.calls = []
        self.manifest = {'created_utc': now(), 'script_sha256': SCRIPT_SHA,
            'mcp_entry': str(entry), 'mcp_entry_sha256': hashlib.sha256(entry.read_bytes()).hexdigest(),
            'mcp_package_version': package_version,
            'api_url': 'http://127.0.0.1:3002', 'transport': 'stdio',
            'public_sources_only': True, 'project_env_loaded': False,
            'upstream_llm_possible': True, 'calls': self.calls}
        (out / 'executed-script.py').write_bytes(SCRIPT_BYTES)
        dump(out / 'manifest.json', self.manifest)
        self.tmp = tempfile.TemporaryDirectory(prefix='track2-firecrawl-')
        # Prepare metadata/artifacts before spawning, and clean up failed startup.
        try:
            self.proc = subprocess.Popen([shutil.which('node') or 'node', str(entry)],
                cwd=self.tmp.name, env=child_env(), stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, start_new_session=True)
            self.selector = selectors.DefaultSelector()
            self.selector.register(self.proc.stdout, selectors.EVENT_READ)
        except BaseException:
            if hasattr(self, 'proc'):
                self.proc.terminate()
                try:
                    self.proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.proc.kill()
                    self.proc.wait(timeout=5)
                self.proc.stdin.close()
                self.proc.stdout.close()
            if hasattr(self, 'selector'):
                self.selector.close()
            self.tmp.cleanup()
            raise

    def send(self, data, deadline):
        if isinstance(self.proc.stdin, io.BytesIO):
            self.proc.stdin.write(data)  # Offline tests; real transport always uses a pipe.
            return
        fd = self.proc.stdin.fileno()
        was_blocking = os.get_blocking(fd)
        os.set_blocking(fd, False)
        try:
            with selectors.DefaultSelector() as writer:
                writer.register(fd, selectors.EVENT_WRITE)
                while data:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0 or not writer.select(remaining):
                        raise TimeoutError('MCP stdin deadline exceeded')
                    try:
                        written = os.write(fd, data[:65536])
                        if written == 0:
                            raise RuntimeError('MCP stdin closed')
                        data = data[written:]
                    except BlockingIOError:
                        continue
        finally:
            os.set_blocking(fd, was_blocking)

    def rpc(self, method, params, timeout=180):
        self.sequence += 1
        ident = self.sequence
        if ident > MAX_CALLS:
            raise ValueError('Call budget exhausted')
        request = {'jsonrpc': '2.0', 'id': ident, 'method': method, 'params': params}
        deadline = time.monotonic() + timeout
        self.send((json.dumps(request) + '\n').encode(), deadline)
        received = 0
        while time.monotonic() < deadline:
            while b'\n' in self.buffer:
                line, self.buffer = self.buffer.split(b'\n', 1)
                if not line.strip():
                    continue
                response = json.loads(line)
                if response.get('id') == ident:
                    return response
            ready = self.selector.select(max(0, deadline - time.monotonic()))
            if not ready:
                break
            chunk = os.read(self.proc.stdout.fileno(), 65536)
            if not chunk:
                raise RuntimeError('MCP process closed stdout')
            received += len(chunk)
            if received > MAX_RESPONSE or len(self.buffer) + len(chunk) > MAX_RESPONSE:
                raise RuntimeError('MCP response exceeded byte budget')
            self.buffer += chunk
        raise TimeoutError('MCP response deadline exceeded; no automatic retry')

    def initialize(self):
        response = self.rpc('initialize', {'protocolVersion': '2025-06-18', 'capabilities': {},
            'clientInfo': {'name': 'track2-public-evidence', 'version': '1'}})
        if response.get('error'):
            raise RuntimeError('MCP initialization failed')
        dump(self.out / 'initialize.json', response)
        self.send(b'{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}\n', time.monotonic() + 10)
        listed = self.rpc('tools/list', {})
        self.tools = {x['name']: x for x in listed['result']['tools']}
        if len(self.tools) != len(listed['result']['tools']):
            raise ValueError('Duplicate advertised tool names')
        dump(self.out / 'tools.json', listed)
        self.manifest['advertised_tools'] = sorted(self.tools)
        dump(self.out / 'manifest.json', self.manifest)
        return self.tools

    def call(self, label, name, arguments, timeout=180, project=None):
        if name not in self.tools:
            raise ValueError('Tool not advertised')
        if not label.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Unsafe artifact label')
        item = {'label': label, 'tool': name, 'arguments': arguments, 'started_utc': now()}
        self.calls.append(item)
        dump(self.out / 'manifest.json', self.manifest)
        try:
            response = self.rpc('tools/call', {'name': name, 'arguments': arguments}, timeout)
            result = decode(response)
            # List endpoints can contain unrelated local users' monitors; never archive them.
            if project is not None and result['data'] is not None:
                result['data'] = project(result['data'])
            # Do not log server error messages: upstream error bodies can contain secrets.
            if result['status'] == 'tool_error':
                result['data'] = None
            dump(self.out / (label + '.json'), result)
            item['status'] = result['status']
            item['sha256'] = hashlib.sha256((self.out / (label + '.json')).read_bytes()).hexdigest()
        except (TimeoutError, RuntimeError, ValueError, OSError, TypeError, AttributeError) as exc:
            item['status'] = type(exc).__name__
            result = {'status': item['status'], 'data': None}
        item['ended_utc'] = now()
        dump(self.out / 'manifest.json', self.manifest)
        print(json.dumps({'label': label, 'tool': name, 'status': item['status']}), flush=True)
        return result

    def close(self):
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait(timeout=5)
        self.selector.close()
        self.proc.stdin.close()
        self.proc.stdout.close()
        self.tmp.cleanup()
        self.manifest['ended_utc'] = now()
        self.manifest['used_tools'] = sorted({x['tool'] for x in self.calls})
        dump(self.out / 'manifest.json', self.manifest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['discover', 'research', 'capabilities', 'followup'])
    parser.add_argument('output', type=Path)
    parser.add_argument('--entry', type=Path, default=DEFAULT_ENTRY)
    args = parser.parse_args()
    out = args.output.resolve()
    if not out.is_relative_to(ROOT / 'results/feat009'):
        raise ValueError('Output must be a new directory under results/feat009')
    out.mkdir(parents=True, exist_ok=False)
    client = MCP(args.entry, out)
    try:
        listed = client.initialize()
        print(json.dumps({'tools': sorted(listed), 'count': len(listed)}))
        if args.mode == 'research':
            research(client)
        elif args.mode == 'capabilities':
            capabilities(client)
        elif args.mode == 'followup':
            followup(client)
    finally:
        client.close()
    return 2 if any(x.get('status') != 'ok' for x in client.calls) else 0


if __name__ == '__main__':
    raise SystemExit(main())
