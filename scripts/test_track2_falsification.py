"""Offline public/synthetic checks for the bounded research transports."""
import copy
import json
import unittest
from unittest.mock import patch

import track2_falsification_search as search
import track2_falsification_sources as sources


class FalsificationTransportTests(unittest.TestCase):
    def setUp(self):
        self.call = {'label': 'public_test', 'claim': 'F2', 'tool': 'firecrawl_search',
                     'arguments': {'query': 'BUBR1 rapamycin', 'limit': 8}}

    def test_all_fixed_plans_validate_without_network(self):
        for mode in ('discovery', 'followup', 'primary', 'closure'):
            plan = json.loads((search.ROOT / f'notes/track2-falsification-{mode}-20260919.json').read_text())
            self.assertTrue(search.validate(plan))
        for suffix in ('', '-supplement'):
            plan = json.loads((search.ROOT / f'notes/track2-falsification-records{suffix}-20260919.json').read_text())
            self.assertTrue(sources.validate(plan['records']))

    def test_persistent_or_model_jobs_are_rejected(self):
        for tool in ('firecrawl_agent', 'firecrawl_monitor_create', 'firecrawl_interact', 'firecrawl_feedback'):
            call = dict(self.call, tool=tool)
            with self.assertRaises(ValueError): search.validate({'calls': [call]})

    def test_search_cannot_smuggle_scrape_actions_or_unbounded_output(self):
        for key, value in [('scrapeOptions', {'actions': ['executeJavascript']}), ('limit', 10000)]:
            call = copy.deepcopy(self.call); call['arguments'][key] = value
            with self.assertRaises(ValueError): search.validate({'calls': [call]})

    def test_duplicate_labels_and_budget_rejected(self):
        for calls in ([self.call, self.call], [], [self.call] * 76):
            with self.assertRaises(ValueError): search.validate({'calls': calls})

    def test_scrape_allowlist_and_plain_format(self):
        call = dict(self.call, tool='firecrawl_scrape', arguments={
            'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC123/',
            'formats': ['markdown'], 'onlyMainContent': True})
        self.assertTrue(search.validate({'calls': [call]}))
        for url in ('file:///data/example', 'http://127.0.0.1/',
                    'https://pmc.ncbi.nlm.nih.gov.evil.example/',
                    'https://user:password@pmc.ncbi.nlm.nih.gov/'):
            bad = copy.deepcopy(call); bad['arguments']['url'] = url
            with self.assertRaises(ValueError): search.validate({'calls': [bad]})
        call['arguments']['formats'] = ['summary']
        with self.assertRaises(ValueError): search.validate({'calls': [call]})

    def test_structured_records_reject_private_or_arbitrary_urls(self):
        for url in ('file:///data/example', 'https://example.org/', 'http://127.0.0.1/',
                    'https://www.ebi.ac.uk/private/account'):
            with self.assertRaises(ValueError):
                sources.validate([{'id': 'record', 'url': url, 'format': 'json'}])

    def test_primary_identity_mismatch_cannot_pass_as_requested_study(self):
        record = {'expected_pmcid': 'PMC2793064'}
        sources.check_identity(record, {'resultList': {'result': [{'pmcid': 'PMC2793064'}]}})
        for hits in ([], [{'pmcid': 'PMC2861805'}], [{'pmcid': 'PMC2793064'}] * 2):
            with self.assertRaisesRegex(ValueError, 'identity mismatch'):
                sources.check_identity(record, {'resultList': {'result': hits}})

    def test_worker_always_closes_its_client(self):
        with patch.object(search, 'MCP') as client, patch.object(search.Path, 'mkdir'):
            client.return_value.initialize.side_effect = RuntimeError('synthetic startup failure')
            with self.assertRaises(RuntimeError): search.worker(None, search.Path('synthetic'), [])
            client.return_value.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
