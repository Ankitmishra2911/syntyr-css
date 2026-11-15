"""Tests for opt-in, zero-JS presentation and rendering recipes."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RenderingRecipes(unittest.TestCase):
    def test_optional_render_deferral_respects_print_and_intrinsic_size(self):
        css = (ROOT / "src/recipes.css").read_text(encoding="utf-8")
        core = (ROOT / "dist/syntyr.core.css").read_text(encoding="utf-8")
        self.assertIn(".syn-defer-section", css)
        self.assertIn("content-visibility: auto", css)
        self.assertIn("contain-intrinsic-size: auto var(--syn-defer-size, 36rem)", css)
        self.assertIn("@media print", css)
        self.assertIn("content-visibility: visible", css)
        self.assertNotIn(".syn-defer-section", core)

    def test_visual_modifiers_are_opt_in_and_use_theme_tokens(self):
        css = (ROOT / "src/recipes.css").read_text(encoding="utf-8")
        self.assertIn(".syn-surface--accent", css)
        self.assertIn(".syn-surface--lift", css)
        self.assertIn("var(--syn-accent)", css)
        self.assertIn("@media (hover: hover)", css)
        self.assertIn("prefers-reduced-motion: reduce", css)

    def test_real_example_uses_opt_in_visual_recipes(self):
        html = (ROOT / "examples/saas-workflows.html").read_text(encoding="utf-8")
        self.assertIn("syn-surface--accent", html)
        self.assertIn("syn-surface--lift", html)


if __name__ == "__main__":
    unittest.main()
