"""Public CSS-first navigation and loading-state component contracts."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class GalleryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = set()
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.anchors.add(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))


class PracticalComponents(unittest.TestCase):
    def test_navigation_primitives_are_in_core_with_native_states(self):
        css = (ROOT / 'src/components/patterns.css').read_text()
        for selector in ('.syn-breadcrumbs', '.syn-pagination', '.syn-page-link',
                         '.syn-page-link[aria-current="page"]'):
            with self.subTest(selector=selector):
                self.assertIn(selector, css)
        self.assertIn('min-height: 2.75rem', css)
        self.assertIn('border-inline-start', css)
        self.assertIn('.syn-root :where(:focus-visible)', (ROOT / 'src/base.css').read_text())

    def test_loading_skeleton_is_static_and_accessible_example(self):
        css = (ROOT / 'src/components/patterns.css').read_text()
        self.assertIn('.syn-skeleton', css)
        self.assertIn('.syn-skeleton--short', css)
        self.assertNotIn('animation:', css)
        gallery = (ROOT / 'docs/index.html').read_text()
        self.assertIn('class="syn-skeleton" aria-hidden="true"', gallery)
        self.assertIn('class="syn-skeleton syn-skeleton--short" aria-hidden="true"', gallery)
        self.assertIn('Loading preview', gallery)
        self.assertNotIn('<script', gallery.lower())

    def test_gallery_navigation_resolves_to_real_anchors(self):
        gallery = (ROOT / 'docs/index.html').read_text()
        self.assertIn('class="syn-breadcrumbs" aria-label="Breadcrumb"', gallery)
        self.assertIn('class="syn-pagination" aria-label="Gallery sections"', gallery)
        self.assertIn('aria-current="page"', gallery)
        parsed = GalleryParser()
        parsed.feed(gallery)
        for href in parsed.links:
            if href.startswith('#') and len(href) > 1:
                self.assertIn(href[1:], parsed.anchors, href)

    def test_public_guides_link_to_existing_local_files(self):
        for relative in ('README.md', 'docs/distribution.md', 'docs/components.md',
                         'docs/recipes.md', 'RELEASE_CHECKS.md'):
            with self.subTest(document=relative):
                path = ROOT / relative
                for href in re.findall(r'\]\(([^\s\)]+)', path.read_text()):
                    if href.startswith(('https:', 'http:', 'mailto:', '#')):
                        continue
                    target = href.split('#', 1)[0]
                    if target:
                        self.assertTrue((path.parent / target).exists(), f'{relative}: {href}')


if __name__ == '__main__':
    unittest.main()
