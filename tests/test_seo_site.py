"""SEO regression checks for the deployable Cloudflare Pages output."""
from __future__ import annotations

import json
import re
import unittest
from xml.etree import ElementTree

from scripts.build_cloudflare_site import SITE_URL, source_files


def meta(html: str, name: str) -> str:
    found = re.search(r'<meta\s+name="' + re.escape(name) + r'"\s+content="([^"]*)"', html)
    return found.group(1) if found else ""


def canonical(html: str) -> list[str]:
    return re.findall(r'<link\s+rel="canonical"\s+href="([^"]+)"', html)


class SEOOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.site = source_files()

    def test_sitemap_uses_200_status_urls_and_excludes_nonindexable_pages(self):
        xml = ElementTree.fromstring(self.site["sitemap.xml"])
        locs = [node.text for node in xml.findall("{*}url/{*}loc")]
        self.assertTrue(locs)
        self.assertEqual(len(locs), len(set(locs)))
        self.assertIn(SITE_URL + "/", locs)
        self.assertIn(SITE_URL + "/docs/catalog", locs)
        self.assertIn(SITE_URL + "/docs/", locs)
        self.assertNotIn(SITE_URL + "/404", locs)
        self.assertFalse(any(url.endswith(".html") or url.endswith(".md") for url in locs))
        self.assertEqual(self.site["robots.txt"].decode().count(SITE_URL + "/sitemap.xml"), 1)

    def test_every_indexable_html_has_exactly_one_clean_self_canonical(self):
        sitemap = ElementTree.fromstring(self.site["sitemap.xml"])
        listed = {node.text for node in sitemap.findall("{*}url/{*}loc")}
        for path, contents in self.site.items():
            if not path.endswith(".html"):
                continue
            html = contents.decode()
            urls = canonical(html)
            clean = ("/" if path == "index.html" else "/" + path[:-10]
                     if path.endswith("/index.html") else "/" + path[:-5])
            target = SITE_URL + clean
            if target in listed:
                self.assertEqual(urls, [target], path)
                self.assertNotIn("noindex", meta(html, "robots").lower(), path)
            else:
                self.assertIn("noindex", meta(html, "robots").lower(), path)
                self.assertNotIn(target, listed)

    def test_structured_data_identifies_software_and_docs_breadcrumbs(self):
        homepage = self.site["index.html"].decode()
        self.assertEqual(len(re.findall(r'application/ld\+json', homepage)), 1)
        home_data = json.loads(re.search(
            r'<script type="application/ld\+json">(.*?)</script>', homepage, re.S
        ).group(1))
        self.assertEqual(home_data["@type"], "SoftwareSourceCode")
        self.assertEqual(home_data["license"], "https://opensource.org/licenses/MIT")
        doc = self.site["docs/catalog.html"].decode()
        data = json.loads(re.search(
            r'<script type="application/ld\+json">(.*?)</script>', doc, re.S
        ).group(1))
        self.assertEqual(data["@type"], "BreadcrumbList")
        self.assertEqual(data["itemListElement"][-1]["item"], SITE_URL + "/docs/catalog")

    def test_human_navigation_points_to_html_and_robots_excludes_markdown(self):
        self.assertIn('href="components.html"', self.site["docs/catalog.html"].decode())
        self.assertIn('href="blocks-guide.html"', self.site["docs/blocks.html"].decode())
        headers = self.site["_headers"].decode()
        self.assertIn("/llms-full.txt\n  X-Robots-Tag: noindex", headers)
        self.assertIn("/docs/*.md\n  X-Robots-Tag: noindex", headers)

    def test_generated_guide_metadata_is_descriptive(self):
        for name in ("ai-quickstart", "components", "framework-integrations", "from-pico"):
            page = self.site[f"docs/{name}.html"].decode()
            description = meta(page, "description")
            self.assertGreaterEqual(len(description), 70, name)
            self.assertNotIn("complete illustrated HTML reference", description)
            self.assertLessEqual(len(description), 175)


if __name__ == "__main__":
    unittest.main()
