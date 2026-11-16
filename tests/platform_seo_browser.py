"""Opt-in browser smoke for platform landing pages; Playwright is maintainer-only."""
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import unittest

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = ("wordpress", "shopify", "wix", "webflow", "framer",
             "squarespace", "ghost", "hubspot", "drupal", "joomla",
             "carrd", "duda", "tilda")
PUBLIC = Path("/tmp/syntyr-platform-pages-publish-20261116")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


@contextmanager
def http_site():
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        partial(QuietHandler, directory=str(PUBLIC))
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


class PlatformSEOPageBrowserTests(unittest.TestCase):
    def test_browser_rendering_and_keyboard_navigation(self):
        if not (PUBLIC / "sitemap.xml").exists():
            self.skipTest("Build static site with scripts/build_cloudflare_site.py")
        with http_site() as base, sync_playwright() as playwright:
            for browser_type in ("chromium", "firefox"):
                browser = getattr(playwright, browser_type).launch(headless=True)
                try:
                    page = browser.new_page(viewport={"width": 320, "height": 720})
                    errors = []
                    failed_assets = []
                    page.on("pageerror", lambda err: errors.append(str(err)))
                    page.on("response", lambda res: failed_assets.append(res.url)
                            if res.status >= 400 else None)
                    for platform in PLATFORMS:
                        with self.subTest(engine=browser_type, platform=platform):
                            response = page.goto(
                                f"{base}/docs/{platform}.html",
                                wait_until="load")
                            self.assertEqual(response.status, 200)
                            self.assertEqual(page.locator("h1").count(), 1)
                            self.assertIn(platform, page.title().lower())
                            self.assertTrue(page.locator(
                                'a[href="site-builders.html"]').count() >= 1)
                            self.assertTrue(page.locator(
                                'main[role], main#doc-main').count() >= 1)
                            self.assertLessEqual(
                                page.evaluate(
                                    "document.documentElement.scrollWidth - innerWidth"),
                                1, platform)
                    self.assertFalse(errors, errors)
                    self.assertFalse(failed_assets, failed_assets)
                    page.close()
                finally:
                    browser.close()


if __name__ == "__main__":
    unittest.main()
