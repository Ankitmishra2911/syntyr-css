"""Public v0.2 API and commercial/open-core boundary, test-first."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]

class V02Contract(unittest.TestCase):
    def test_embedded_root_does_not_occupy_full_viewport(self):
        base = (ROOT / 'src/base.css').read_text()
        self.assertIn('.cy-page', base)
        self.assertNotIn('min-height: 100vh;', base)
        self.assertIn('min-height: 100svh;', base)

    def test_component_variants_have_documented_css(self):
        buttons = (ROOT / 'src/components/buttons.css').read_text()
        forms = (ROOT / 'src/components/forms.css').read_text()
        for component in ('.cy-button--danger', '.cy-button--outline', '.cy-button--small'):
            self.assertIn(component, buttons)
        for state in (':user-invalid', '[aria-invalid="true"]', '.cy-help', '.cy-error'):
            self.assertIn(state, forms)

    def test_semantic_layer_retains_opt_in_and_scoping(self):
        css = (ROOT / 'src/semantic.css').read_text()
        self.assertIn('.cy-semantic', css)
        self.assertIn(':where(input', css)
        self.assertIn('[aria-invalid="true"]', css)
        self.assertIn('input[type="range"]', css)

    def test_real_use_examples(self):
        for name in ('console.html', 'landing.html'):
            html = (ROOT / 'examples' / name).read_text()
            self.assertIn('cy-root cy-page', html)
            self.assertNotIn('<script', html)
            self.assertIn('cyberline.', html)

    def test_oss_and_paid_commercial_artifacts_separated(self):
        self.assertIn('MIT License', (ROOT / 'LICENSE').read_text())
        for name in ('strategy.md', 'premium-license-draft.md', 'validation-plan.md'):
            self.assertTrue((ROOT / 'business' / name).exists())
        self.assertIn('MIT', (ROOT / 'business' / 'strategy.md').read_text())

if __name__ == '__main__': unittest.main()
