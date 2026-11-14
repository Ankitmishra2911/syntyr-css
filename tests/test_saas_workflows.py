"""Contract for copyable, server-ready SaaS workflow markup without framework JS."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.ids = set()
        self.labels = set()
        self.form_methods = []
        self.search_landmarks = 0
        self.tables = 0
        self.scripts = 0
        self.links = []
        self.names = []
        self.current_pages = 0
    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get('id'): self.ids.add(attrs['id'])
        if tag == 'label' and attrs.get('for'): self.labels.add(attrs['for'])
        if tag == 'form': self.form_methods.append(attrs.get('method'))
        if tag == 'search' or attrs.get('role') == 'search': self.search_landmarks += 1
        if tag == 'table': self.tables += 1
        if tag == 'script': self.scripts += 1
        if tag == 'a': self.links.append(attrs.get('href',''))
        if tag in {'input','select','textarea'} and attrs.get('name'): self.names.append(attrs['name'])
        if attrs.get('aria-current') == 'page': self.current_pages += 1


class SaaSWorkflows(unittest.TestCase):
    def test_server_ready_search_filter_settings_markup(self):
        page = (ROOT / 'examples/saas-workflows.html').read_text()
        html = Markup(); html.feed(page)
        self.assertEqual(html.scripts, 0, 'example must not require runtime JavaScript')
        self.assertEqual(html.search_landmarks, 1)
        self.assertEqual(html.tables, 1)
        self.assertIn('get', html.form_methods)
        self.assertEqual(html.current_pages, 3, "one current item per navigation landmark")
        self.assertTrue({'query','status','owner'} <= set(html.names))
        self.assertTrue({'query','status','owner','main','records','preferences','results'} <= html.ids)
        self.assertTrue({'query','status','owner'} <= html.labels)
        self.assertIn('server', page.lower())
        self.assertIn('illustrative', page.lower())
        self.assertIn('aria-describedby', page)
        self.assertIn('class="syn-breadcrumbs workflow-breadcrumbs"', page)
        self.assertIn('class="syn-pagination workflow-pagination"', page)
        self.assertIn('syn-app-shell', page)
        self.assertIn('syn-skeleton', page)
        self.assertIn('syn-table-wrap', page)
        self.assertIn('role="group" aria-label="Loading preview"', page)
        self.assertIn('id="dense"', page)
        self.assertIn('Email notifications (requires server)', page)
        self.assertIn('href="#main"', page)
        for href in html.links:
            if href.startswith('#') and len(href)>1:
                self.assertIn(href[1:], html.ids)

    def test_example_uses_only_local_css(self):
        page = (ROOT / 'examples/saas-workflows.html').read_text()
        for href in ('../dist/syntyr.core.css','../dist/syntyr.recipes.css','saas-workflows.css'):
            self.assertIn('href="' + href + '"', page)
            self.assertTrue((ROOT / 'examples'/href).exists())
        scoped = (ROOT / 'examples/saas-workflows.css').read_text()
        self.assertIn('.workflow-', scoped)
        self.assertNotIn('@keyframes', scoped)
        self.assertNotIn('animation:', scoped)

    def test_gallery_and_cloudflare_publisher_include_complete_example(self):
        self.assertIn('examples/saas-workflows.html', (ROOT / 'README.md').read_text())
        self.assertIn('saas-workflows.html', (ROOT / 'docs/index.html').read_text())
        self.assertIn('saas-workflows.html', (ROOT / 'scripts/build_cloudflare_site.py').read_text())
        self.assertIn('saas-workflows.css', (ROOT / 'scripts/build_cloudflare_site.py').read_text())


if __name__=='__main__':
    unittest.main()
