"""Contracts for the next public, MIT-licensed Cyberline UX/market-validation iteration."""
from pathlib import Path
from html.parser import HTMLParser
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.descriptions = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "meta" and values.get("name") == "description":
            self.descriptions.append(values.get("content", ""))


class V04Contract(unittest.TestCase):
    def test_original_resource_index_is_a_free_reusable_example(self):
        page = (ROOT / "examples/resources.html").read_text(encoding="utf-8")
        for fragment in ('cy-root cy-page', 'data-cy-theme="noir"', 'method="get"',
                         "aria-labelledby", 'scope="col"', "<caption", "cy-table-wrap",
                         "cy-input", "cy-select", "MIT", "ILLUSTRATIVE"):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, page)
        self.assertNotIn("<script", page.lower())
        self.assertNotIn("stripe", page.lower())

    def test_theme_customization_guide_is_copy_pasteable(self):
        guide = (ROOT / "docs/theme-customization.md").read_text(encoding="utf-8")
        for token in ("--cy-accent", "--cy-on-accent", "--cy-bg", "--cy-surface",
                      "data-cy-theme", "cy-root", "cy-semantic", "prefers-reduced-motion"):
            self.assertIn(token, guide)
        self.assertIn(chr(96)*3 + "css", guide)
        self.assertIn(chr(96)*3 + "html", guide)
        self.assertIn("contrast", guide.lower())

    def test_site_gallery_links_to_new_demo_and_guide(self):
        page = (ROOT / "docs/index.html").read_text(encoding="utf-8")
        self.assertIn('href="../examples/resources.html"', page)
        self.assertIn("theme-customization.md", page)
        metadata = MetadataParser()
        metadata.feed(page)
        self.assertEqual(len(metadata.descriptions), 1, "one non-conflicting SEO meta description")
        self.assertIn('role="group" aria-label="Grid palette"', page)
        self.assertIn('role="group" aria-label="Noir palette"', page)

    def test_commercial_preview_is_truthful_and_not_a_checkout(self):
        page = (ROOT / "docs/console-kit.html").read_text(encoding="utf-8")
        self.assertIn("$59", page)
        self.assertIn("concept", page.lower())
        self.assertIn("not available", page.lower())
        self.assertIn("MIT", page)
        self.assertNotIn("<script", page.lower())
        self.assertNotIn("checkout", page.lower())
        self.assertIn("github.com/dporkka/cyberline-css/issues/new", page)


if __name__ == "__main__":
    unittest.main()
