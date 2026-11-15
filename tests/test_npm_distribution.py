"""CSS-only npm distribution is optional, complete and release-safe."""
import json
from pathlib import Path
import unittest

from scripts.build import distributions

ROOT = Path(__file__).resolve().parents[1]


class NpmDistributionContract(unittest.TestCase):
    def setUp(self):
        self.package = json.loads((ROOT / 'package.json').read_text(encoding='utf-8'))

    def test_public_css_only_package_metadata(self):
        self.assertEqual(self.package['name'], '@syntyr/css')
        self.assertEqual(self.package['version'], (ROOT / 'VERSION').read_text().strip())
        self.assertEqual(self.package['license'], 'MIT')
        self.assertFalse(self.package.get('private', False))
        self.assertEqual(self.package['style'], './dist/syntyr.core.css')
        self.assertEqual(self.package['exports']['.'], './dist/syntyr.core.css')
        self.assertIn('**/*.css', self.package['sideEffects'])
        self.assertNotIn('main', self.package)
        for field in ('dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies', 'bin'):
            self.assertNotIn(field, self.package, field)

    def test_every_distribution_is_explicitly_exported(self):
        expected = {
            ('./syntyr.css' if name == 'syntyr.css' else './' + name.removeprefix('syntyr.')): './dist/' + name
            for name in distributions()
        }
        self.assertEqual({key: value for key, value in self.package['exports'].items() if key != '.'}, expected)
        for relative in expected.values():
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative.removeprefix('./')).is_file())

    def test_allowlisted_release_files_are_css_and_docs_only(self):
        self.assertEqual(set(self.package['files']), {'dist/', 'README.md', 'LICENSE'})
        self.assertIn('publishConfig', self.package)
        self.assertEqual(self.package['publishConfig']['access'], 'public')
        self.assertTrue((ROOT / 'docs/package-managers.md').is_file())


if __name__ == '__main__':
    unittest.main()
