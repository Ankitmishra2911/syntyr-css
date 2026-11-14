"""Release contract for the modular, zero-runtime-dependency Syntyr package."""
from pathlib import Path
import gzip
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'

class ReleaseContract(unittest.TestCase):
    def test_modular_source_tree_and_distributions(self):
        for rel in (
            'src/components/layout.css', 'src/components/typography.css',
            'src/components/buttons.css', 'src/components/forms.css',
            'src/components/overlays.css', 'src/components/data.css',
            'src/semantic.css', 'src/effects.css',
            'dist/syntyr.core.css', 'dist/syntyr.semantic.css',
            'dist/syntyr.effects.css', 'dist/syntyr.all.css',
            'dist/syntyr.css',
        ):
            with self.subTest(rel=rel):
                self.assertTrue((ROOT / rel).is_file(), f'Missing {rel}')

    def test_semantic_is_opt_in(self):
        core = (DIST / 'syntyr.core.css').read_text()
        semantic = (DIST / 'syntyr.semantic.css').read_text()
        self.assertNotIn('syn-semantic', core)
        for tag in ('button', 'input', 'select', 'textarea', 'table', 'article', 'details'):
            with self.subTest(tag=tag):
                self.assertIn(f'{tag}:not([class])' if tag in ('select', 'textarea') else f':where({tag}', semantic)
        self.assertIn('.syn-semantic', semantic)
        self.assertIn('@layer syn.semantic', semantic)

    def test_themes_and_accessibility_hooks(self):
        all_css = (DIST / 'syntyr.all.css').read_text()
        for term in ('[data-syn-theme="grid"]', '[data-syn-theme="noir"]',
                     'prefers-reduced-motion', 'forced-colors', ':focus-visible',
                     '.syn-button--ghost', '.syn-alert', 'min(', 'color-mix('):
            with self.subTest(term=term):
                self.assertIn(term, all_css)

    def test_size_budgets(self):
        core = gzip.compress((DIST / 'syntyr.core.css').read_bytes(), mtime=0)
        all_css = gzip.compress((DIST / 'syntyr.all.css').read_bytes(), mtime=0)
        self.assertLessEqual(len(core), 5 * 1024, f'core gzip {len(core)} bytes')
        self.assertLessEqual(len(all_css), 8 * 1024, f'all gzip {len(all_css)} bytes')

    def test_build_is_reproducible(self):
        proc = subprocess.run([sys.executable, 'scripts/build.py', '--check'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_gallery_and_docs(self):
        self.assertTrue((ROOT/'docs/index.html').is_file())
        self.assertTrue((ROOT/'docs/components.md').is_file())
        gallery = (ROOT/'docs/index.html').read_text()
        self.assertIn('syn-semantic', gallery)
        self.assertIn('data-syn-theme="grid"', gallery)
        self.assertIn('data-syn-theme="noir"', gallery)
        self.assertNotIn('<script', gallery)

if __name__ == '__main__':
    unittest.main()
