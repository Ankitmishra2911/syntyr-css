"""Portable CMS starter: no CMS or JavaScript dependency at render time."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts import render_cms_starter as cms

ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "examples/cms-starter"


class CmsStarterTests(unittest.TestCase):
    def sample(self):
        return json.loads((STARTER / "content/pages/home.json").read_text(encoding="utf-8"))

    def test_sample_renders_native_syntyr_html_and_static_styles(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp)
            cms.build(STARTER, destination, ROOT / "dist")
            html = (destination / "index.html").read_text(encoding="utf-8")
            self.assertIn('<main id="content"', html)
            self.assertIn('class="syn-site-hero"', html)
            self.assertIn('class="syn-feature-grid"', html)
            self.assertIn('class="syn-pricing"', html)
            self.assertIn("<details", html)
            self.assertIn('<script src=', (destination / "admin/index.html").read_text(encoding="utf-8"))
            self.assertTrue((destination / "css/syntyr.core.css").is_file())
            self.assertTrue((destination / "css/syntyr.recipes.css").is_file())
            self.assertTrue((destination / "admin/config.yml").is_file())
            self.assertNotIn("sveltia-cms.js", html)

    def test_untrusted_text_is_escaped_not_emitted_as_markup(self):
        page = self.sample()
        page["sections"][0]["heading"] = '<img src=x onerror="alert(1)">'
        html = cms.render_document(page)
        self.assertIn("&lt;img src=x onerror=&quot;alert(1)&quot;&gt;", html)
        self.assertNotIn('<img src=x', html)

    def test_dangerous_or_protocol_relative_urls_are_rejected(self):
        for url in ("javascript:alert(1)", "data:text/html,bad", "//evil.example/", "/\\evil.com", "https://evil.test/\nmalformed"):
            with self.subTest(url=url):
                page = self.sample()
                page["sections"][0]["button"]["url"] = url
                with self.assertRaises(ValueError):
                    cms.render_document(page)

    def test_unknown_block_types_are_rejected(self):
        page = self.sample()
        page["sections"].append({"type": "html", "body": '<script>alert(1)</script>'})
        with self.assertRaisesRegex(ValueError, "type"):
            cms.render_document(page)

    def test_missing_nested_fields_are_rejected(self):
        page = self.sample()
        del page["sections"][0]["button"]["url"]
        with self.assertRaises(ValueError):
            cms.render_document(page)

    def test_unexpected_fields_and_themes_are_rejected(self):
        page = self.sample()
        page["sections"][0]["unsafeHtml"] = "<b>bad</b>"
        with self.assertRaises(ValueError):
            cms.render_document(page)
        page = self.sample()
        page["theme"] = 'studio" onload="alert(1)'
        with self.assertRaises(ValueError):
            cms.render_document(page)

    def test_schema_and_editors_declare_same_section_types(self):
        schema = json.loads((STARTER / "blocks.schema.json").read_text(encoding="utf-8"))
        types = {section["properties"]["type"]["const"] for section in schema["$defs"]["section"]["oneOf"]}
        self.assertEqual(types, {"hero", "features", "pricing", "faq", "cta"})
        sveltia = (STARTER / "admin/config.yml").read_text(encoding="utf-8")
        pages = (STARTER / ".pages.yml").read_text(encoding="utf-8")
        for section_type in types:
            with self.subTest(section_type=section_type):
                self.assertIn(f"- name: {section_type}\n", sveltia)
                self.assertIn(f"- name: {section_type}\n", pages)
        self.assertIn("blockKey: type", pages)
        self.assertIn("typeKey: type", sveltia)
        self.assertIn("content/pages/home.json", pages)
        self.assertIn("content/pages/home.json", sveltia)

    def test_malformed_section_and_theme_are_rejected_cleanly(self):
        for field, value in (("theme", []), ("theme", {})):
            page = self.sample()
            page[field] = value
            with self.assertRaises(ValueError):
                cms.render_document(page)
        page = self.sample()
        page["sections"][1]["type"] = {"nested": "invalid"}
        with self.assertRaises(ValueError):
            cms.render_document(page)

    def test_render_does_not_mutate_data(self):
        page = self.sample()
        before = deepcopy(page)
        cms.render_document(page)
        self.assertEqual(page, before)


if __name__ == "__main__":
    unittest.main()
