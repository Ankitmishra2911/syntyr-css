"""Ensure the optional browser and axe matrix include every publicly linked theme."""
from pathlib import Path
from html.parser import HTMLParser
import unittest


class GenericAriaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.unscoped_labels = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "div" and any(key in attrs for key in ("aria-label", "aria-labelledby")) and "role" not in attrs:
            self.unscoped_labels.append((attrs.get("class", ""), attrs.get("aria-label", "")))


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

    def test_labeled_generic_containers_expose_a_semantic_role(self):
        pages = [ROOT / "index.html", *sorted((ROOT / "docs").glob("*.html")),
                 *sorted((ROOT / "examples").glob("*.html"))]
        for page in pages:
            with self.subTest(page=page.relative_to(ROOT)):
                parser = GenericAriaParser()
                parser.feed(page.read_text(encoding="utf-8"))
                self.assertEqual(parser.unscoped_labels, [], "add an appropriate role")


if __name__ == "__main__":
    unittest.main()
