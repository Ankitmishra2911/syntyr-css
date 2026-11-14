"""v0.3 portable composition API, commercial boundary and no-build contract."""
from pathlib import Path
import gzip
import unittest

ROOT = Path(__file__).resolve().parents[1]

class V03Contract(unittest.TestCase):
    def test_modular_container_patterns_are_shipped(self):
        source = (ROOT / 'src/components/patterns.css').read_text()
        self.assertIn('.cy-region', source)
        self.assertIn('container-name: cy-region', source)
        self.assertIn('@container cy-region (min-width:', source)
        for item in ('.cy-split', '.cy-stats', '.cy-stat', '.cy-empty', '.cy-pricing', '.cy-price-card'):
            with self.subTest(item=item):
                self.assertIn(item, source)
        self.assertIn('components/patterns.css', (ROOT / 'scripts/build.py').read_text())
        self.assertIn('.cy-pricing', (ROOT / 'dist/cyberline.core.css').read_text())

    def test_accessible_state_styles_and_explicit_tokens(self):
        buttons = (ROOT / 'src/components/buttons.css').read_text()
        tokens = (ROOT / 'src/tokens.css').read_text()
        for item in ('[aria-pressed="true"]', '[data-cy-state="active"]', '[aria-busy="true"]'):
            self.assertIn(item, buttons)
        for token in ('--cy-ease:', '--cy-duration-fast:', '--cy-success:', '--cy-warning:'):
            self.assertIn(token, tokens)

    def test_free_original_recipes_and_marketing_example(self):
        for rel in ('docs/recipes.md', 'docs/tailwind-research.md', 'examples/pricing.html', 'business/console-kit-spec.md'):
            with self.subTest(rel=rel):
                self.assertTrue((ROOT / rel).is_file())
        gallery = (ROOT / 'docs/index.html').read_text()
        self.assertIn('id="recipes"', gallery)
        self.assertIn('class="cy-region"', gallery)
        self.assertIn('cy-price-card', gallery)
        self.assertIn('examples/pricing.html', gallery)
        self.assertNotIn('<script', gallery)
        pricing = (ROOT / 'examples/pricing.html').read_text()
        self.assertIn('cy-pricing', pricing)
        self.assertNotIn('<script', pricing)
        self.assertIn('MIT', pricing)

    def test_license_and_bundle_constraints(self):
        self.assertIn('MIT License', (ROOT / 'LICENSE').read_text())
        self.assertNotIn('tailwindcss', (ROOT / 'dist/cyberline.core.css').read_text().lower())
        self.assertFalse((ROOT / 'node_modules').exists())
        self.assertLessEqual(len(gzip.compress((ROOT / 'dist/cyberline.core.css').read_bytes(), mtime=0)), 5 * 1024)
        self.assertLessEqual(len(gzip.compress((ROOT / 'dist/cyberline.all.css').read_bytes(), mtime=0)), 8 * 1024)

if __name__ == '__main__': unittest.main()
