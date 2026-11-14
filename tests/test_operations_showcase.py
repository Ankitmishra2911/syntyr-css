"""Contracts for the static, reusable SYNTYR operations dashboard example."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/operations-console.html"


class LinksAndIds(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.fragments = []
        self.remote_assets = []
        self.scripts = []
        self.headings = []
        self.mains = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("href", "").startswith("#"):
            self.fragments.append(a["href"][1:])
        if tag in ("script", "iframe"):
            self.scripts.append(tag)
        if tag in ("img", "link", "script"):
            src = a.get("src", a.get("href", ""))
            if src.startswith(("http:", "https:", "//")):
                self.remote_assets.append(src)
        if tag == "main":
            self.mains += 1
        if tag == "h1":
            self.headings.append(tag)


class OperationsExampleContract(unittest.TestCase):
    def test_dashboard_is_complete_and_no_js(self):
        source = EXAMPLE.read_text()
        for name in ("cy-app-shell", "cy-app-rail", "cy-app-nav", "cy-workspace",
                     "cy-kpi-grid", "cy-frame--bracket", "cy-frame--bevel",
                     "cy-terminal", "cy-status--success", "cy-status--warning",
                     "cy-cell--numeric", "<progress", "<details", "<summary",
                     "ops-scroll-hint", 'tabindex="0"', "<table", "<caption", 'scope="col"', 'href="#main"',
                     '<main id="main"'):
            with self.subTest(name=name):
                self.assertIn(name, source)
        self.assertIn("ILLUSTRATIVE", source)
        self.assertIn('role="group" aria-label="Static sample command output"', source)
        self.assertNotIn("<script", source.lower())
        self.assertNotIn("onclick=", source.lower())

    def test_navigation_semantics_and_local_assets(self):
        parser = LinksAndIds()
        parser.feed(EXAMPLE.read_text())
        self.assertEqual(parser.mains, 1)
        self.assertEqual(len(parser.headings), 1)
        self.assertEqual(parser.scripts, [])
        self.assertEqual(parser.remote_assets, [])
        self.assertTrue(set(parser.fragments) <= parser.ids, (set(parser.fragments) - parser.ids))
        for css in ("../dist/syntyr.core.css", "../dist/syntyr.recipes.css",
                    "../dist/syntyr.geometry.css"):
            self.assertIn(css, EXAMPLE.read_text())

    def test_example_event_times_explicitly_use_utc(self):
        times = re.findall(r'<time datetime="([^"]+)"', EXAMPLE.read_text())
        self.assertEqual(len(times), 3)
        self.assertTrue(all(value.endswith("Z") for value in times), times)

    def test_example_is_in_gallery_and_browser_audits(self):
        self.assertIn("operations-console.html", (ROOT / "docs/index.html").read_text())
        self.assertIn("operations-console.html", (ROOT / "README.md").read_text())
        for script in ("tests/browser_matrix.py", "tests/reflow_test.py", "tests/axe_audit.py"):
            with self.subTest(script=script):
                self.assertIn('"examples/operations-console.html"', (ROOT / script).read_text())


if __name__ == "__main__":
    unittest.main()
