"""Contract for native disclosure navigation in a responsive workspace.

A folder navigation should remain plain links and <details>, not a fake ARIA tree.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
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

    def test_copyable_sidebar_recipe_has_a_separate_scoped_ancestor(self):
        guide = (ROOT / "docs/recipes.md").read_text(encoding="utf-8")
        snippet = guide.split("## Native disclosure navigation for workspaces", 1)[1].split("```html", 1)[1].split("```", 1)[0]
        self.assertIn('<div class="syn-root" data-syn-theme="studio">\n  <div class="syn-sidebar">', snippet)
        self.assertNotIn('class="syn-root syn-sidebar"', snippet)
        self.assertIn('<nav class="syn-tree-nav"', snippet)
        self.assertIn('<main id="workspace">', snippet)
        self.assertIn('</main>\n  </div>\n</div>', snippet)

    def test_workspace_navigation_targets_are_distinct_sections(self):
        content = EXAMPLE.read_text(encoding="utf-8")
        navigation = content.split('<nav class="syn-tree-nav"', 1)[1].split("</nav>", 1)[0]
        fragment_targets = re.findall(r'<a href="#([^"]+)"', navigation)
        self.assertEqual(len(fragment_targets), len(set(fragment_targets)),
                         "Each workspace navigation item needs its own destination")
        page = Elements()
        page.feed(content)
        for target in fragment_targets:
            self.assertIn(target, page.ids)

    def test_optional_recipe_preserves_focus_reflow_and_forced_colors(self):
        source = (ROOT / "src/recipes.css").read_text(encoding="utf-8")
        dist = (ROOT / "dist/syntyr.recipes.css").read_text(encoding="utf-8")
        for css in (source, dist):
            self.assertIn("syn-tree-nav", css)
            self.assertIn("min-block-size: 44px", css)
            self.assertIn(":focus-visible", css)
            self.assertIn("forced-colors: active", css)
        self.assertIn('href="../dist/syntyr.recipes.css"', EXAMPLE.read_text())

    def test_deeply_nested_lists_cap_visual_indentation_for_reflow(self):
        # Native disclosures remain structurally nested without spending
        # more horizontal space at each level of a deep navigation.
        cutoff = "&.syn-tree-nav " + " ".join([":is(ul, ol)"] * 5)
        for css in ("src/recipes.css", "dist/syntyr.recipes.css"):
            source = (ROOT / css).read_text(encoding="utf-8")
            self.assertIn(cutoff + " {", source)
            rule = source.split(cutoff + " {", 1)[1].split("}", 1)[0]
            self.assertIn("margin-inline-start: 0", rule)
            self.assertIn("padding-inline-start: 0", rule)
            self.assertIn("border-inline-start: 0", rule)

    def test_discoverability_and_static_site_contract(self):
        self.assertIn("native-disclosure-navigation.html", (ROOT / "README.md").read_text())
        self.assertIn("native-disclosure-navigation.html", (ROOT / "docs/recipes.md").read_text())
        self.assertIn("native-disclosure-navigation.html", (ROOT / "llms.txt").read_text())
        self.assertIn("native-disclosure-navigation.html",
                      (ROOT / "scripts/build_cloudflare_site.py").read_text())


if __name__ == "__main__":
    unittest.main()
