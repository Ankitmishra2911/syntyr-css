"""Contract checks for the optional Nulang integration example."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "nulang-web"


class NulangWebExampleTests(unittest.TestCase):
    def test_css_preparation_copies_the_canonical_asset(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run(
                [sys.executable, str(EXAMPLE / "prepare.py"), temporary],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                (Path(temporary) / "syntyr.core.css").read_bytes(),
                (ROOT / "dist" / "syntyr.core.css").read_bytes(),
            )

    def test_page_exercises_standard_html_and_syntyr_without_js(self):
        source = (EXAMPLE / "src" / "main.nula").read_text()
        self.assertIn('route "GET" "/" -> home', source)
        self.assertIn('route "GET" "/status" -> status', source)
        for contract in ("syn-root", "syn-panel", "syn-button", "syn-table", "data-syn-theme", "/syntyr.core.css"):
            with self.subTest(contract=contract):
                self.assertIn(contract, source)
        self.assertNotIn('raw(', source)
        self.assertNotIn('javascript:', source)

    def test_static_assets_are_served_from_example_directory(self):
        manifest = (EXAMPLE / "Nulang.toml").read_text()
        self.assertIn('static_dir = "static"', manifest)
        self.assertIn('output_dir = "dist"', manifest)


if __name__ == "__main__":
    unittest.main()
