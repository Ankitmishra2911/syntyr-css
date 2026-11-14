"""v0.3 portable composition API, commercial boundary and no-build contract."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class V03Contract(unittest.TestCase):
    def test_modular_container_patterns_are_shipped(self):
        source = (ROOT / 'src/components/patterns.css').read_text()
        self.assertIn('.syn-region', source)
        self.assertIn('container-name: syn-region', source)
        self.assertIn('@container syn-region (min-width:', source)
        for item in ('.syn-split', '.syn-stats', '.syn-stat', '.syn-empty', '.syn-pricing', '.syn-price-card'):
            with self.subTest(item=item):
                self.assertIn(item, source)
        self.assertIn('components/patterns.css', (ROOT / 'scripts/build.py').read_text())
        self.assertIn('.syn-pricing', (ROOT / 'dist/syntyr.core.css').read_text())

    def test_accessible_state_styles_and_explicit_tokens(self):
        buttons = (ROOT / 'src/components/buttons.css').read_text()
        tokens = (ROOT / 'src/tokens.css').read_text()
        for item in ('[aria-pressed="true"]', '[data-syn-state="active"]', '[aria-busy="true"]'):
            self.assertIn(item, buttons)
        for token in ('--syn-ease:', '--syn-duration-fast:', '--syn-success:', '--syn-warning:'):
            self.assertIn(token, tokens)

    def test_free_original_recipes_and_marketing_example(self):
        for rel in ('docs/recipes.md', 'docs/tailwind-research.md', 'examples/pricing.html', 'business/console-kit-spec.md'):
            with self.subTest(rel=rel):
                self.assertTrue((ROOT / rel).is_file())
        gallery = (ROOT / 'docs/index.html').read_text()
        self.assertIn('id="recipes"', gallery)
        self.assertIn('class="syn-region"', gallery)
        self.assertIn('syn-price-card', gallery)
        self.assertIn('examples/pricing.html', gallery)
        self.assertNotIn('<script', gallery)
        pricing = (ROOT / 'examples/pricing.html').read_text()
        self.assertIn('syn-pricing', pricing)
        self.assertNotIn('<script', pricing)
        self.assertIn('MIT', pricing)

    def test_license_and_bundle_constraints(self):
        self.assertIn('MIT License', (ROOT / 'LICENSE').read_text())
        self.assertNotIn('tailwindcss', (ROOT / 'dist/syntyr.core.css').read_text().lower())
        self.assertFalse((ROOT / 'node_modules').exists())
        from scripts.asset_report import measure_distributions
        sizes = measure_distributions(ROOT / 'dist')
        self.assertIn('syntyr.core.css', sizes)
        self.assertIn('syntyr.all.css', sizes)

if __name__ == '__main__': unittest.main()
