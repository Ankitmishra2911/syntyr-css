"""Opt-in minimalist framework ideas must not change Syntyr's zero-runtime contract."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MinimalistPatternsContract(unittest.TestCase):
    def test_system_palette_supports_nested_auto_with_native_color_scheme(self):
        css = (ROOT / "src/tokens.css").read_text()
        self.assertIn('.syn-root[data-syn-theme="auto"]', css)
        self.assertIn('.syn-root [data-syn-theme="auto"]', css)
        self.assertIn('color-scheme: light dark;', css)
        self.assertIn('light-dark(', css)
        self.assertIn('@supports (color: light-dark(', css)

    def test_intrinsic_layouts_and_fluid_tokens_are_recipes_only(self):
        css = (ROOT / "src/recipes.css").read_text()
        for fragment in (
            '.syn-sidebar', '.syn-switcher',
            '--syn-sidebar-width', '--syn-sidebar-content-min',
            '--syn-switcher-threshold',
            '--syn-type-display', '--syn-type-lede', '--syn-reading-width',
            '.syn-fluid-display', '.syn-fluid-lede', '.syn-reading',
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, css)
                self.assertIn(fragment, (ROOT / "dist/syntyr.recipes.css").read_text())
                self.assertNotIn(fragment, (ROOT / "dist/syntyr.core.css").read_text())
        self.assertIn('flex-wrap: wrap', css)
        self.assertIn('clamp(', css)
        self.assertIn('min(100%', css)

    def test_semantic_checkbox_and_radio_labels_are_inline_without_global_reset(self):
        css = (ROOT / "src/semantic.css").read_text()
        self.assertIn('label:not([class]):has(', css)
        self.assertIn('label[data-syn-semantic]:has(', css)
        self.assertIn('> input[type="checkbox"]', css)
        self.assertIn('> input[type="radio"]', css)
        self.assertIn('align-items: center;', css)
        self.assertIn('display: flex;', css)

    def test_real_html_example_uses_opt_in_css_and_accessible_controls(self):
        html = (ROOT / "examples/minimalist-patterns.html").read_text()
        for fragment in (
            'syntyr.core.css', 'syntyr.semantic.css', 'syntyr.recipes.css',
            'data-syn-theme="auto"', 'syn-semantic',
            'syn-sidebar', 'syn-switcher', 'syn-fluid-display',
            'type="checkbox"', 'for="email"', 'id="email"',
            'name="email"', 'type="submit"',
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, html)
        self.assertNotIn('<script', html)
        self.assertNotIn('onclick=', html)

    def test_distribution_has_no_new_runtime_or_build_dependency(self):
        src = (ROOT / "scripts/build.py").read_text()
        self.assertNotIn('npm ', src)
        self.assertIn("syntyr.recipes.css", src)
        self.assertIn("syntyr.semantic.css", src)


if __name__ == "__main__":
    unittest.main()
