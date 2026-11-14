"""Ensure the optional browser and axe matrix include every publicly linked theme."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BrowserCoverageContract(unittest.TestCase):
    def test_new_theme_gallery_is_in_cross_engine_and_axe_audits(self):
        for script in ("browser_matrix.py", "axe_audit.py"):
            with self.subTest(script=script):
                source = (ROOT / "tests" / script).read_text(encoding="utf-8")
                self.assertIn('"examples/themes.html"', source)

    def test_theme_matrix_checks_all_six_palettes_and_color_schemes(self):
        source = (ROOT / "tests/browser_matrix.py").read_text(encoding="utf-8")
        for theme in ("grid", "noir", "industrial", "terminal", "corporate", "minimal"):
            self.assertIn(f'"{theme}"', source)
        self.assertIn('colorScheme', source)


if __name__ == "__main__":
    unittest.main()
