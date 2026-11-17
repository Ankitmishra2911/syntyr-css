"""Contract for native disclosure navigation in a responsive workspace.

A folder navigation should remain plain links and <details>, not a fake ARIA tree.
"""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/native-disclosure-navigation.html"


class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag in {"a", "link"}:
            self.links.append(attrs.get("href", ""))


class NativeDisclosureNavigationTest(unittest.TestCase):
    def test_navigation_has_native_keyboard_and_current_page_semantics(self):
        self.assertTrue(EXAMPLE.is_file(), "Missing native disclosure navigation demo")
        content = EXAMPLE.read_text(encoding="utf-8")
        page = Elements()
        page.feed(content)
        navs = [attrs for tag, attrs in page.tags if tag == "nav" and attrs.get("aria-label")]
        self.assertTrue(navs)
        self.assertGreaterEqual(sum(tag == "details" for tag, _ in page.tags), 2)
        self.assertGreaterEqual(sum(tag == "summary" for tag, _ in page.tags), 2)
        self.assertEqual(sum(attrs.get("aria-current") == "page" for _, attrs in page.tags), 1)
        self.assertFalse(any(tag == "script" for tag, _ in page.tags))
        self.assertNotIn('role="tree"', content)
        self.assertNotIn('role="treeitem"', content)
        self.assertTrue(any("syn-sidebar" in attrs.get("class", "") for _, attrs in page.tags))
        self.assertTrue(any("syn-tree-nav" in attrs.get("class", "") for _, attrs in page.tags))
        for href in page.links:
            if href.startswith("#") and len(href) > 1:
                self.assertIn(href[1:], page.ids)
        self.assertIn("no JavaScript", content)
        self.assertIn("not an ARIA tree", content)

    def test_optional_recipe_preserves_focus_reflow_and_forced_colors(self):
        source = (ROOT / "src/recipes.css").read_text(encoding="utf-8")
        dist = (ROOT / "dist/syntyr.recipes.css").read_text(encoding="utf-8")
        for css in (source, dist):
            self.assertIn("syn-tree-nav", css)
            self.assertIn("min-block-size: 44px", css)
            self.assertIn(":focus-visible", css)
            self.assertIn("forced-colors: active", css)
        self.assertIn('href="../dist/syntyr.recipes.css"', EXAMPLE.read_text())

    def test_discoverability_and_static_site_contract(self):
        self.assertIn("native-disclosure-navigation.html", (ROOT / "README.md").read_text())
        self.assertIn("native-disclosure-navigation.html", (ROOT / "docs/recipes.md").read_text())
        self.assertIn("native-disclosure-navigation.html", (ROOT / "llms.txt").read_text())
        self.assertIn("native-disclosure-navigation.html",
                      (ROOT / "scripts/build_cloudflare_site.py").read_text())


if __name__ == "__main__":
    unittest.main()
