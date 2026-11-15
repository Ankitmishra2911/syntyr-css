"""Published commercial research must describe real deliverables, never imply a sale."""
import json
import re
import unittest
from pathlib import Path

from scripts.build_cloudflare_site import source_files

ROOT = Path(__file__).resolve().parents[1]


class CommercialOfferCatalogTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / 'metadata/commercial-offers.json').read_text())
        self.html = (ROOT / 'docs/products.html').read_text()

    def test_valid_machine_readable_offers_are_consistent_with_public_page(self):
        self.assertEqual(self.catalog['schema_version'], 1)
        products = self.catalog['products']
        self.assertEqual([p['id'] for p in products], ['core', 'console-kit', 'pro', 'studio', 'agency'])
        for product in products:
            with self.subTest(product=product['id']):
                self.assertIn(product['status'], {'available', 'research'})
                self.assertIn(f'data-product-id="{product["id"]}"', self.html)
                card = re.search(r'<article\b[^>]*data-product-id="' + re.escape(product['id']) + r'"[^>]*>(.*?)</article>', self.html, re.S)
                self.assertIsNotNone(card)
                self.assertIn(product['name'], card.group(1))
                self.assertIn(product['display_price'], card.group(1))
                self.assertIn(product['license_status'], {'MIT', 'draft-not-operative'})
                self.assertNotIn('checkout_url', product)
                if product['status'] == 'research':
                    self.assertFalse(product.get('deliverable_ready', False))
                    self.assertEqual(product['license_status'], 'draft-not-operative')
                else:
                    self.assertEqual(product['id'], 'core')
                    self.assertTrue(product['deliverable_ready'])
                    self.assertEqual(product['license_status'], 'MIT')

    def test_roadmap_is_clearly_not_a_storefront_or_payment_form(self):
        self.assertIn('NOT FOR SALE', self.html)
        self.assertIn('proposed', self.html.lower())
        self.assertIn('MIT', self.html)
        self.assertIn('no payment', self.html.lower())
        self.assertNotRegex(self.html.lower(), r'href=["\'](?:/checkout|https?://checkout\.)')
        self.assertNotIn('<form ', self.html)
        self.assertNotIn('application/ld+json', self.html)  # no fake buyable offers in search results

    def test_public_build_publishes_only_marketing_copy_and_manifest(self):
        published = source_files()
        self.assertIn('docs/products.html', published)
        self.assertIn('metadata/commercial-offers.json', published)
        self.assertNotIn('business/premium-license-draft.md', published)
        self.assertFalse(any(path.startswith(('private/', 'business/', 'premium/')) for path in published))

    def test_details_urls_resolve_to_published_product_pages(self):
        from urllib.parse import urljoin, urlsplit, unquote
        published = source_files()
        catalog_url = 'https://syntyr-css.pages.dev/metadata/commercial-offers.json'
        expected = {
            'core': 'docs/distribution.html',
            'console-kit': 'docs/console-kit.html',
            'pro': 'docs/products.html',
            'studio': 'docs/products.html',
            'agency': 'docs/products.html',
        }
        for product in self.catalog['products']:
            with self.subTest(product=product['id']):
                url = urlsplit(urljoin(catalog_url, product['details_url']))
                self.assertEqual(url.scheme, 'https')
                self.assertEqual(url.hostname, 'syntyr-css.pages.dev')
                self.assertFalse(url.query or url.fragment)
                published_path = unquote(url.path).lstrip('/')
                self.assertEqual(published_path, expected[product['id']])
                self.assertIn(published_path, published)

    def test_mobile_navigation_has_native_no_javascript_disclosure(self):
        self.assertIn('<details class="site-mobile-menu">', self.html)
        self.assertIn('<summary>Menu</summary>', self.html)
        self.assertIn('aria-label="Mobile product navigation"', self.html)

    def test_research_asks_buyers_about_specific_products_without_private_data(self):
        form = (ROOT / '.github/ISSUE_TEMPLATE/commercial-product-feedback.yml').read_text()
        for tier in ('Console Kit', 'Syntyr Pro', 'Syntyr Studio', 'Syntyr Agency'):
            self.assertIn(tier, form)
        self.assertIn('No sales or preorders', form)
        self.assertIn('Do not share', form)
        self.assertIn('price-point', form)
        self.assertIn('current-project', form)
        self.assertIn('commercial-product-feedback.yml', self.html)

    def test_discoverability_for_humans_and_agents(self):
        self.assertIn('docs/products.html', (ROOT / 'index.html').read_text())
        self.assertIn('products.html', (ROOT / 'docs/index.html').read_text())
        self.assertIn('metadata/commercial-offers.json', (ROOT / 'llms.txt').read_text())
        self.assertIn('products.html', (ROOT / 'docs/console-kit.html').read_text())


if __name__ == '__main__':
    unittest.main()
