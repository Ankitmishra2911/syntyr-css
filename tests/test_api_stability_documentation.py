"""The public prerelease stability contract must travel with the distributions."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ApiStabilityDocumentation(unittest.TestCase):
    def test_api_contract_is_linked_from_readme_and_architecture(self):
        self.assertTrue((ROOT / 'docs/api-stability.md').is_file())
        self.assertIn('docs/api-stability.md', (ROOT / 'README.md').read_text())
        self.assertIn('docs/api-stability.md', (ROOT / 'ARCHITECTURE.md').read_text())

    def test_api_contract_is_published_and_packaged(self):
        from scripts.package_release import FILES
        from scripts.build_cloudflare_site import source_files
        self.assertIn('docs/api-stability.md', FILES)
        self.assertIn('docs/api-stability.md', source_files())


if __name__ == '__main__':
    unittest.main()
