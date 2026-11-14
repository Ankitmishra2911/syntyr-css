"""Contracts for opt-in Syntyr density, geometry and operational presentation."""
from html.parser import HTMLParser
from pathlib import Path
import gzip
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DemoParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.classes = set()
        self.scripts = 0
        self.tables = 0
        self.headers = 0
        self.labels = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.classes.update(attributes.get("class", "").split())
        self.scripts += tag == "script"
        self.tables += tag == "table"
        self.headers += tag == "th"
        self.labels += tag == "label"


class CompositionApiTests(unittest.TestCase):
    def test_density_modes_are_scoped_and_preserve_existing_defaults(self):
        css = (ROOT / "src/presets.css").read_text()
        for mode in ("compact", "comfortable"):
            self.assertIn(f'data-syn-density="{mode}"', css)
        self.assertIn(".syn-root [data-syn-density=", css)
        for token in ("--syn-space-1", "--syn-space-5", "--syn-control-height",
                      "--syn-control-padding-block", "--syn-table-padding-block"):
            self.assertIn(token, css)
        self.assertIn("var(--syn-control-padding-block)", (ROOT / "src/components/forms.css").read_text())
        self.assertIn("var(--syn-table-padding-block)", (ROOT / "src/components/data.css").read_text())

    def test_geometry_overrides_inherit_across_nested_theme_boundaries(self):
        css = (ROOT / "src/presets.css").read_text()
        for name in ("precision", "industrial", "soft"):
            self.assertIn(f'data-syn-geometry="{name}"', css)
        self.assertIn("--syn-geometry-radius", css)
        self.assertIn("--syn-geometry-cut", css)
        css = (ROOT / "src/tokens.css").read_text()
        for theme in ("grid", "noir", "studio", "industrial", "terminal", "corporate", "minimal"):
            marker = f'.syn-root[data-syn-theme="{theme}"]'
            position = css.index(marker)
            declarations = css[css.index("{", position) + 1:css.index("}", position)]
            self.assertIn("var(--syn-geometry-radius,", declarations, theme)
            self.assertIn("var(--syn-geometry-cut,", declarations, theme)

    def test_semantic_tokens_are_theme_relative(self):
        css = (ROOT / "src/tokens.css").read_text()
        for token in ("--syn-focus-ring", "--syn-link", "--syn-border-subtle"):
            self.assertIn(token, css)
        self.assertIn("var(--syn-focus-ring)", (ROOT / "src/base.css").read_text())

    def test_operational_patterns_are_opt_in_but_publicly_shipped(self):
        from scripts.build import distributions
        from scripts.package_release import FILES
        definitions = distributions()
        self.assertEqual(definitions["syntyr.application.css"], ("application.css",))
        self.assertEqual(definitions["syntyr.presets.css"], ("presets.css",))
        self.assertNotIn("presets.css", definitions["syntyr.core.css"])
        self.assertNotIn("presets.css", definitions["syntyr.all.css"])
        self.assertIn("syntyr.presets.css", (ROOT / "README.md").read_text())
        self.assertNotIn("application.css", definitions["syntyr.core.css"])
        self.assertNotIn("application.css", definitions["syntyr.all.css"])
        self.assertIn("dist/syntyr.application.css", FILES)
        self.assertIn("dist/syntyr.presets.css", FILES)
        source = (ROOT / "src/application.css").read_text()
        for cls in (".syn-data-toolbar", ".syn-detail-list", ".syn-timeline",
                    ".syn-bulk-actions", ".syn-section-heading", ".syn-form-columns"):
            self.assertIn(cls, source)
        self.assertIn("@layer syn.application", source)
        self.assertNotIn("@import", source)
        self.assertEqual(source.strip(), (ROOT / "dist/syntyr.application.css").read_text().strip())

    def test_demo_exercises_theme_density_and_geometry_with_semantic_html(self):
        page = (ROOT / "examples/application-patterns.html").read_text()
        parser = DemoParser()
        parser.feed(page)
        for cls in ("syn-root", "syn-data-toolbar", "syn-detail-list", "syn-timeline"):
            self.assertIn(cls, parser.classes)
        for attr in ('data-syn-density="compact"', 'data-syn-geometry="precision"',
                     'data-syn-theme="studio"'):
            self.assertIn(attr, page)
        self.assertGreaterEqual(parser.tables, 1)
        self.assertGreaterEqual(parser.headers, 2)
        self.assertGreaterEqual(parser.labels, 1)
        self.assertEqual(parser.scripts, 0)
        self.assertIn("syntyr.application.css", page)
        self.assertIn("syntyr.presets.css", page)

    def test_new_bundle_preserves_existing_size_budgets(self):
        for name, limit in (("syntyr.core.css", 5120), ("syntyr.all.css", 8192)):
            data = (ROOT / "dist" / name).read_bytes()
            self.assertLessEqual(len(gzip.compress(data, mtime=0)), limit, name)


if __name__ == "__main__":
    unittest.main()
