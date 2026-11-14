"""Integration contract: seven SYNTYR themes coexist with frames and showcase."""
from pathlib import Path
import gzip
import ast
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE_TYPES = ("core", "semantic", "recipes", "effects", "geometry", "utilities", "", "all")


class SevenThemeIntegrationContract(unittest.TestCase):
    def test_every_feature_is_shipped_in_both_stable_namespaces(self):
        from scripts.build import distributions
        packages = distributions()
        for module in BUNDLE_TYPES:
            suffix = f".{module}" if module else ""
            syntyr = f"syntyr{suffix}.css"
            cyberline = f"cyberline{suffix}.css"
            with self.subTest(module=module):
                self.assertIn(syntyr, packages)
                self.assertEqual(packages[syntyr], packages[cyberline])
                self.assertEqual((ROOT / "dist" / syntyr).read_bytes(),
                                 (ROOT / "dist" / cyberline).read_bytes())
        self.assertIn("geometry.css", packages["syntyr.all.css"])
        self.assertIn("utilities.css", packages["syntyr.all.css"])
        self.assertNotIn("geometry.css", packages["syntyr.core.css"])
        self.assertNotIn("utilities.css", packages["syntyr.core.css"])
        self.assertIn("@layer cy.tokens, cy.base, cy.components, cy.semantic, cy.recipes, cy.geometry, cy.effects;",
                      (ROOT / "dist/syntyr.core.css").read_text()[:400])

    def test_syntyr_release_package_carries_both_optional_modules(self):
        from scripts.package_release import FILES
        for basename in ("syntyr.geometry.css", "cyberline.geometry.css",
                         "syntyr.utilities.css", "cyberline.utilities.css"):
            with self.subTest(basename=basename):
                self.assertIn("dist/" + basename, FILES)
        self.assertEqual((ROOT / "VERSION").read_text().strip(), "0.3.0-alpha.4")

    def test_all_three_feature_galleries_remain_discoverable(self):
        html = (ROOT / "docs/index.html").read_text()
        for item in ("examples/themes.html", "examples/geometry-terminal.html",
                     "examples/operations-console.html"):
            with self.subTest(item=item):
                self.assertIn(item.rsplit("/", 1)[1], html)
        for item in ("themes.html", "geometry-terminal.html", "operations-console.html"):
            with self.subTest(item=item):
                self.assertTrue((ROOT / "examples" / item).exists())

    def test_browser_accepts_all_seven_root_theme_accents(self):
        content = (ROOT / "tests/browser_matrix.py").read_text()
        from test_v05_contract import THEMES, theme_rules
        tokens = (ROOT / "src/tokens.css").read_text()
        assertion = content.split("assert css in (", 1)[1].split("), (name, css)", 1)[0]
        for theme in THEMES:
            with self.subTest(theme=theme):
                self.assertIn('"' + theme_rules(tokens, theme)["--cy-accent"] + '"', assertion)

    def test_browser_suite_covers_each_page_once(self):
        groups = []
        for script in ("browser_matrix.py", "reflow_test.py", "axe_audit.py"):
            module = ast.parse((ROOT / "tests" / script).read_text())
            assignment = next(n for n in module.body if isinstance(n, ast.Assign)
                              and any(isinstance(t, ast.Name) and t.id == "PAGES" for t in n.targets))
            groups.append(ast.literal_eval(assignment.value))
        for group in groups:
            self.assertEqual(len(group), len(set(group)), "duplicate page in browser matrix")
            for basename in ("themes.html", "geometry-terminal.html", "operations-console.html"):
                self.assertEqual(sum(p.endswith("/" + basename) for p in group), 1)

    def test_distribution_stays_within_existing_gzip_budgets(self):
        self.assertLessEqual(len(gzip.compress((ROOT / "dist/syntyr.core.css").read_bytes(), mtime=0)), 5 * 1024)
        self.assertLessEqual(len(gzip.compress((ROOT / "dist/syntyr.css").read_bytes(), mtime=0)), 5 * 1024)
        self.assertLessEqual(len(gzip.compress((ROOT / "dist/syntyr.all.css").read_bytes(), mtime=0)), 8 * 1024)


if __name__ == "__main__":
    unittest.main()
