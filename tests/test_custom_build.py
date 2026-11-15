"""Selective CSS builds preserve deterministic, dependency-free defaults."""
from pathlib import Path
import subprocess
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CustomBuild(unittest.TestCase):
    def build(self, *options):
        return subprocess.run([sys.executable, "scripts/build.py", *options],
                              cwd=ROOT, text=True, capture_output=True)

    def test_select_components_modules_and_themes(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "custom.css"
            process = self.build("--components", "buttons,forms",
                                 "--modules", "semantic,presets",
                                 "--themes", "corporate", "--output", str(target))
            self.assertEqual(process.returncode, 0, process.stderr)
            css = target.read_text()
            self.assertIn(".syn-button", css)
            self.assertIn(".syn-input", css)
            self.assertNotIn(".syn-table-wrap", css)
            self.assertIn('@layer syn.semantic {', css)
            self.assertIn('@layer syn.tokens {', css)
            self.assertIn('data-syn-theme="corporate"', css)
            self.assertIn('data-syn-theme="grid"', css)  # default fallback
            self.assertNotIn('data-syn-theme="noir"', css)
            self.assertNotIn("syn-scanlines", css)

    def test_scan_infers_modules_without_mistaking_dynamic_variants_for_missing_css(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            (directory / "template.html").write_text(
                '<main class="syn-root" data-syn-theme="corporate">'
                '<button class="syn-button syn-button--primary">OK</button></main>')
            output = directory / "result.css"
            process = self.build("--scan", str(directory / "template.html"),
                                 "--themes", "corporate", "--output", str(output))
            self.assertEqual(process.returncode, 0, process.stderr)
            css = output.read_text()
            self.assertIn(".syn-button--danger", css)  # retain entire component and states
            self.assertNotIn(".syn-table-wrap", css)
            self.assertNotIn(".syn-input", css)

    def test_unknown_or_malformed_arguments_fail_without_writing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "bad.css"
            for options in (("--components", "buttons,unknown"),
                            ("--themes", "imaginary"),
                            ("--modules", "../secrets"),
                            ("--scan", "not-a-real-file")):
                with self.subTest(options=options):
                    process = self.build(*options, "--output", str(target))
                    self.assertNotEqual(process.returncode, 0)
                    self.assertFalse(target.exists())

    def test_optional_module_css_is_scoped_to_syntyr_root(self):
        sources = [* (ROOT / "src/components").glob("*.css")]
        sources += [ROOT / "src" / name for name in
                    ("semantic.css", "recipes.css", "geometry.css",
                     "effects.css", "application.css")]
        for source in sources:
            with self.subTest(source=source.name):
                self.assertIn(":where(.syn-root", source.read_text())

    def test_nested_theme_aliases_resolve_at_palette_boundary(self):
        tokens = (ROOT / "src/tokens.css").read_text()
        for theme in ("noir", "studio", "industrial", "terminal",
                      "corporate", "minimal"):
            start = tokens.index(f'.syn-root[data-syn-theme="{theme}"]')
            declarations = tokens[start:tokens.index("}", start)]
            self.assertIn("--syn-focus-ring: var(--syn-accent);", declarations)
            self.assertIn("--syn-link: var(--syn-accent);", declarations)
            self.assertIn("--syn-border-subtle:", declarations)
            self.assertIn("--syn-accent-soft: color-mix(", declarations)

    def test_custom_build_reports_sources_and_bytes_without_limits(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "out.css"
            report = Path(directory) / "report.json"
            command = self.build("--components", "buttons", "--output", str(target),
                                 "--report", str(report))
            self.assertEqual(command.returncode, 0, command.stderr)
            data = json.loads(report.read_text())
            self.assertEqual(data["included_sources"],
                             ["tokens.css", "base.css", "components/buttons.css"])
            self.assertEqual(data["raw_bytes"], target.stat().st_size)
            self.assertGreater(data["gzip_bytes"], 0)
            self.assertNotIn("budget", data)

    def test_no_hard_css_size_limits_in_active_contracts(self):
        for test in ("test_contract.py", "test_release_contract.py",
                     "test_alpha5_integration.py"):
            source = (ROOT / "tests" / test).read_text()
            self.assertNotIn("test_size_budgets", source)
            self.assertNotIn("test_stable_gzip_budgets", source)
            self.assertNotIn("assertLessEqual(len(gzip.compress", source)
        self.assertNotIn("compressed size budgets",
                         (ROOT / "ARCHITECTURE.md").read_text())


if __name__ == "__main__":
    unittest.main()
