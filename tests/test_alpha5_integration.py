"""Alpha.5 integration contracts: SYNTYR-only seven themes and optional utilities."""
from pathlib import Path
import ast
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Alpha5Integration(unittest.TestCase):
    def test_only_syntyr_distributions_and_complete_optional_modules(self):
        from scripts.build import distributions
        definitions = distributions()
        expected = {f"syntyr{suffix}.css" for suffix in
                    ("", ".core", ".semantic", ".recipes", ".effects",
                     ".geometry", ".utilities", ".all")}
        self.assertEqual(set(definitions), expected)
        for filename in expected:
            self.assertEqual(
                (ROOT / "dist" / filename).read_text(),
                "\n".join((ROOT / "src" / part).read_text().strip()
                          for part in definitions[filename]) + "\n",
                filename)
        self.assertIn("geometry.css", definitions["syntyr.all.css"])
        self.assertIn("utilities.css", definitions["syntyr.all.css"])
        self.assertNotIn("utilities.css", definitions["syntyr.core.css"])
        self.assertNotIn("geometry.css", definitions["syntyr.core.css"])

    def test_core_and_optional_artifacts_are_nonempty(self):
        for suffix in (".core", "", ".all"):
            with self.subTest(suffix=suffix):
                self.assertGreater((ROOT / "dist" / f"syntyr{suffix}.css").stat().st_size, 0)

    def test_all_demos_are_covered_once_by_all_browser_suites(self):
        pages = ("themes.html", "geometry-terminal.html", "operations-console.html")
        for script in ("browser_matrix.py", "reflow_test.py", "axe_audit.py"):
            module = ast.parse((ROOT / "tests" / script).read_text())
            assignment = next(
                node for node in module.body
                if isinstance(node, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "PAGES" for t in node.targets))
            entries = ast.literal_eval(assignment.value)
            self.assertEqual(len(entries), len(set(entries)), script)
            for page in pages:
                self.assertEqual(entries.count("examples/" + page), 1, (script, page))

    def test_alpha5_is_unpublished_and_does_not_replace_alpha4_release_links(self):
        self.assertEqual((ROOT / "VERSION").read_text().strip(), "0.3.0-alpha.5")
        text = (ROOT / "README.md").read_text()
        self.assertIn("examples/themes.html", text)
        self.assertIn("examples/operations-console.html", text)
        self.assertIn("dist/syntyr.utilities.css", text)
        self.assertIn("v0.3.0-alpha.4", text)
        from scripts.package_release import FILES
        self.assertIn("dist/syntyr.utilities.css", FILES)


if __name__ == "__main__":
    unittest.main()
