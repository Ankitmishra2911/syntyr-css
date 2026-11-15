"""Opt-in data-workspace styling contracts; no runtime framework dependency."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class DataGridContract(unittest.TestCase):
    def test_opt_in_module_and_zero_js_delivery(self):
        from scripts.build import distributions
        self.assertEqual(distributions()["syntyr.data-grid.css"], ("data-grid.css",))
        self.assertNotIn("data-grid.css", distributions()["syntyr.core.css"])
        self.assertTrue((ROOT / "dist/syntyr.data-grid.css").is_file())
        css = (ROOT / "src/data-grid.css").read_text()
        self.assertIn("@layer syn.components", css)
        self.assertIn(".syn-root", css)
        self.assertIn(".syn-data-grid", css)
        self.assertNotIn("javascript:", css)

    def test_accessible_cell_states_and_density(self):
        css = (ROOT / "src/data-grid.css").read_text()
        for state in ('[aria-selected="true"]', '[aria-invalid="true"]',
                      '[aria-readonly="true"]', '[data-syn-dirty="true"]',
                      ':focus-visible', 'forced-colors: active'):
            with self.subTest(state=state):
                self.assertIn(state, css)
        self.assertIn('data-syn-density="compact"', css)
        self.assertIn("font-variant-numeric: tabular-nums", css)
        self.assertIn(".syn-data-grid__header-row", css)

    def test_static_html_example_is_self_contained(self):
        example = (ROOT / "examples/data-grid.html").read_text()
        self.assertIn("syntyr.data-grid.css", example)
        self.assertIn("syn-data-grid", example)
        self.assertIn('role="grid"', example)
        self.assertIn('role="row" aria-rowindex="1" class="syn-data-grid__header-row"', example)
        self.assertNotIn("<script", example.lower())

if __name__ == "__main__":
    unittest.main()
