"""Regression coverage for PR20's root scoping, presets, and safe builds."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReviewRegressions(unittest.TestCase):
    def build(self, *args):
        return subprocess.run([sys.executable, "scripts/build.py", *args],
                              cwd=ROOT, capture_output=True, text=True)

    def test_semantic_mode_works_on_root_and_descendant_container(self):
        css = (ROOT / "src/semantic.css").read_text()
        self.assertIn(".syn-root.syn-semantic", css)
        self.assertIn(".syn-root .syn-semantic", css)
        self.assertIn("button:not([class])", css)

    def test_root_can_itself_be_a_region_for_container_queries(self):
        css = (ROOT / "src/components/patterns.css").read_text()
        self.assertIn("&.syn-region", css)
        self.assertIn("container-type: inline-size", css)

    def test_geometry_presets_recompute_inherited_radius_and_cut_aliases(self):
        css = (ROOT / "src/presets.css").read_text()
        for name in ("precision", "industrial", "soft"):
            with self.subTest(geometry=name):
                selector = re.search(
                    r':where\([^{}]*data-syn-geometry="' + name + r'"[^{}]*\)\s*\{([^{}]*)\}', css)
                self.assertIsNotNone(selector)
                declarations = selector.group(1)
                self.assertIn("--syn-radius: var(--syn-geometry-radius)", declarations)
                self.assertIn("--syn-cut: var(--syn-geometry-cut)", declarations)

    def test_css_output_and_report_cannot_replace_each_other(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "generated.css"
            p = self.build("--components", "buttons", "--output", str(target),
                           "--report", str(target))
            self.assertNotEqual(p.returncode, 0, p.stdout)
            self.assertFalse(target.exists())

    def test_report_cannot_replace_checked_in_distribution(self):
        dist = ROOT / "dist" / "syntyr.core.css"
        before = dist.read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "generated.css"
            p = self.build("--components", "buttons", "--output", str(target),
                           "--report", str(dist))
            self.assertNotEqual(p.returncode, 0, p.stdout)
            self.assertFalse(target.exists())
            self.assertEqual(dist.read_bytes(), before)

    def test_no_fixed_gzip_ceiling_in_remaining_contracts(self):
        for path in ("tests/test_visual_v04_contract.py",
                     "tests/test_v03_contract.py"):
            with self.subTest(path=path):
                content = (ROOT / path).read_text()
                self.assertNotRegex(content, r"assertLessEqual\([^\n]*gzip")
                self.assertNotIn("8 * 1024", content)
                self.assertNotIn("5 * 1024", content)

    def test_scan_excludes_ignored_tree_content(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / "templates").mkdir()
            (path / "templates" / "index.html").write_text(
                '<main class="syn-root"><button class="syn-button">Go</button></main>')
            (path / "node_modules").mkdir()
            (path / "node_modules" / "file.html").write_text(
                '<table class="syn-table"><tr><td>Not used</td></tr></table>')
            output = path / "app.css"
            p = self.build("--scan", str(path), "--output", str(output))
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn(".syn-button", output.read_text())
            self.assertNotIn(".syn-table-wrap", output.read_text())


if __name__ == "__main__":
    unittest.main()
