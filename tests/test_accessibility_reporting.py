"""Regression checks for reproducible, actionable axe manual-review reports."""
from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('axe_audit', ROOT / 'tests/axe_audit.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class AuditReportingTests(unittest.TestCase):
    def test_normalizes_incomplete_nodes_with_selectors_and_summaries(self):
        data = {
            'violations': [],
            'incomplete': [{
                'id': 'color-contrast', 'impact': 'serious',
                'help': 'Elements must have sufficient color contrast',
                'nodes': [
                    {'target': ['.syn-root', 'a'], 'html': '<a>Read more</a>',
                     'failureSummary': 'Needs review', 'any': [], 'all': []},
                    {'target': ['.syn-panel'], 'html': '<div>Text</div>',
                     'failureSummary': None},
                ],
            }],
        }
        normalized = MODULE.normalize_findings('examples/themes.html', data)
        self.assertEqual(len(normalized['violations']), 0)
        self.assertEqual(len(normalized['incomplete']), 2)
        first = normalized['incomplete'][0]
        self.assertEqual(first['page'], 'examples/themes.html')
        self.assertEqual(first['rule'], 'color-contrast')
        self.assertEqual(first['selector'], ['.syn-root', 'a'])
        self.assertEqual(first['failure_summary'], 'Needs review')
        self.assertEqual(first['html'], '<a>Read more</a>')
        self.assertEqual(first['impact'], 'serious')

    def test_reports_confirmed_violations_separately(self):
        normalized = MODULE.normalize_findings('index.html', {
            'incomplete': [],
            'violations': [{'id': 'image-alt', 'impact': 'critical', 'help': 'Alternate text',
                            'nodes': [{'target': ['img'], 'html': '<img>', 'failureSummary': 'Missing alt'}]}],
        })
        self.assertEqual(len(normalized['violations']), 1)
        self.assertEqual(normalized['violations'][0]['rule'], 'image-alt')
        self.assertEqual(normalized['incomplete'], [])


if __name__ == '__main__':
    unittest.main()
