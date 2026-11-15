"""Humans get canonical HTML guides; AI clients keep the public Markdown sources."""
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

from scripts.build_cloudflare_site import source_files

ROOT = Path(__file__).resolve().parents[1]


class Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs).get('href', ''))


class DocumentationDeliveryTests(unittest.TestCase):
    def test_every_public_markdown_guide_has_a_human_html_counterpart(self):
        files = source_files()
        guides = sorted(name for name in files if name.startswith('docs/') and name.endswith('.md'))
        self.assertGreater(len(guides), 30)
        directory = files['docs/reference.html'].decode()
        for guide in guides:
            html = guide.removesuffix('.md') + '.html'
            self.assertIn(html, files, guide)
            page = files[html].decode()
            self.assertIn('<html lang="en">', page)
            self.assertIn('<main id="doc-main"', page)
            self.assertIn('<h1', page)
            self.assertIn(f'href="{Path(guide).name}"', page)
            self.assertIn(f'href="https://syntyr-css.pages.dev/{html}"', page)
            self.assertIn(f'href="{Path(html).name}"', directory)
            digest = hashlib.sha256(files[guide]).hexdigest()
            self.assertIn(f'content="{digest}"', page, html)
            self.assertNotIn('<script', page.lower())

    def test_markdown_table_code_and_links_are_real_html(self):
        files = source_files()
        page = files['docs/components.html'].decode()
        self.assertIn('<table>', page)
        self.assertIn('<pre><code', page)
        self.assertIn('href="visual-intensity.html"', page)
        self.assertNotIn('href="visual-intensity.md"', page)
        self.assertIn('id="loading-and-scoping"', page)
        self.assertIn('&lt;button', page)

    def test_human_navigation_targets_html_and_agent_sources_are_preserved(self):
        files = source_files()
        for name in ('docs/index.html', 'docs/guides.html', 'docs/reference.html'):
            self.assertIn(name, files)
            links = Anchors()
            links.feed(files[name].decode())
            self.assertFalse([url for url in links.links if re.search(r'\.md(?:$|[#?])', url)], name)
        self.assertIn(b'href="reference.html"', files['docs/guides.html'])
        self.assertIn(b'href="reference.html"', files['docs/index.html'])
        self.assertIn(b'docs/ai-quickstart.md', files['llms.txt'])
        self.assertIn('docs/ai-quickstart.md', files)
        self.assertIn('llms-full.txt', files)

    def test_indexing_and_content_discovery_favor_html_without_blocking_agents(self):
        files = source_files()
        headers = files['_headers'].decode()
        self.assertIn('/docs/*.md\n  X-Robots-Tag: noindex', headers)
        self.assertIn('/README.md\n  X-Robots-Tag: noindex', headers)
        # These paths must not match duplicate Content-Type rules.
        self.assertNotIn("\n/*.md\n", headers)
        self.assertIn('Sitemap: https://syntyr-css.pages.dev/sitemap.xml', files['robots.txt'].decode())
        sitemap = files['sitemap.xml'].decode()
        self.assertIn('https://syntyr-css.pages.dev/docs/components.html', sitemap)
        self.assertNotIn('https://syntyr-css.pages.dev/docs/components.md', sitemap)
        self.assertIn('https://syntyr-css.pages.dev/docs/reference.html', sitemap)


if __name__ == '__main__':
    unittest.main()
