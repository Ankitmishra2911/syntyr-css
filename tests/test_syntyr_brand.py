"""Brand migration contract: SYNTYR public identity with non-breaking legacy paths."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
MODULES = ('core', 'semantic', 'effects', 'recipes', 'utilities', 'all')


class SyntyrBrandTests(unittest.TestCase):
    def test_public_site_uses_syntyr_brand(self):
        for rel in ('index.html', 'docs/index.html', 'docs/console-kit.html'):
            with self.subTest(page=rel):
                contents = (ROOT / rel).read_text(encoding='utf-8')
                self.assertIn('SYNTYR', contents)
                self.assertNotIn('CYBERLINE', contents)
                self.assertNotIn('Cyberline', contents)

    def test_primary_css_paths_and_legacy_aliases_remain_identical(self):
        for name in ('syntyr.css', 'cyberline.css') + tuple(
            f'{prefix}.{module}.css' for prefix in ('syntyr', 'cyberline') for module in MODULES
        ):
            with self.subTest(name=name):
                self.assertTrue((ROOT / 'dist' / name).is_file())
        for module in ('',) + MODULES:
            suffix = f'.{module}' if module else ''
            with self.subTest(module=module):
                self.assertEqual(
                    (ROOT / 'dist' / f'syntyr{suffix}.css').read_bytes(),
                    (ROOT / 'dist' / f'cyberline{suffix}.css').read_bytes(),
                )
        result = subprocess.run([sys.executable, 'scripts/build.py', '--check'],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_all_published_css_outputs_are_checked_into_git(self):
        # A developer's global gitignore must not silently drop new dist files.
        output = subprocess.run(['git', 'ls-files', '--', 'dist/'], cwd=ROOT,
                                capture_output=True, text=True, check=True)
        tracked = set(output.stdout.splitlines())
        expected = {f'dist/{prefix}{suffix}.css'
                    for prefix in ('syntyr', 'cyberline')
                    for suffix in ('', '.core', '.semantic', '.effects', '.recipes', '.all')}
        self.assertTrue(expected <= tracked,
                        'Missing from Git: ' + ', '.join(sorted(expected - tracked)))

    def test_release_uses_new_name_and_preserves_compatibility_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / 'release.zip'
            result = subprocess.run(
                [sys.executable, 'scripts/package_release.py', str(archive)],
                cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with ZipFile(archive) as zip_file:
                names = set(zip_file.namelist())
                prefix = 'syntyr-css-0.3.0-alpha.4/'
                self.assertIn(prefix + 'README.md', names)
                for basename in ('syntyr', 'cyberline'):
                    for module in ('',) + MODULES:
                        suffix = f'.{module}' if module else ''
                        self.assertIn(prefix + f'dist/{basename}{suffix}.css', names)

    def test_docs_explain_legacy_classes_and_paths(self):
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        migration = (ROOT / 'docs/brand-migration.md').read_text(encoding='utf-8')
        self.assertTrue(readme.startswith('# SYNTYR'))
        self.assertIn('dporkka/syntyr-css', readme)
        self.assertIn('cy-root', readme)
        self.assertIn('cyberline.core.css', migration)
        self.assertIn('syntyr.core.css', migration)
        self.assertIn('cy-', migration)


if __name__ == '__main__':
    unittest.main()
