"""Opt-in real HTMX E2E tests. Never add HTMX to Syntyr's runtime.

Fetch a pinned HTMX 2.0.8 file as a developer-only test fixture:
  curl -fsSL https://unpkg.com/htmx.org@2.0.8/dist/htmx.min.js -o /tmp/syntyr-htmx.min.js
  HTMX_JS_PATH=/tmp/syntyr-htmx.min.js python3 tests/htmx_browser.py
Browser setup follows tests/browser_test.py (Playwright is dev-only).
"""
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import os
import shutil
import sys
import time
import unittest

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from examples.htmx_server import DemoHandler


class SlowDemoHandler(DemoHandler):
    def do_GET(self):
        if self.path.startswith("/customers/search"):
            time.sleep(0.3)
        super().do_GET()


class HtmxBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = os.environ.get("HTMX_JS_PATH", "")
        if not fixture or not Path(fixture).is_file():
            raise unittest.SkipTest("Set HTMX_JS_PATH to a local pinned HTMX 2.0.8 fixture")
        cls.htmx_js = Path(fixture)
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), SlowDemoHandler)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"
        cls.p = sync_playwright().start()
        executable = (os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
                      or shutil.which("chromium")
                      or shutil.which("chromium-browser"))
        launch = {"headless": True}
        if executable:
            launch.update(executable_path=executable, args=["--no-sandbox"])
        try:
            cls.browser = cls.p.chromium.launch(**launch)
        except Exception:
            cls.p.stop()
            cls.server.shutdown()
            cls.server.server_close()
            cls.thread.join(timeout=2)
            raise

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.p.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.page.route(
            "https://unpkg.com/htmx.org@2.0.8/dist/htmx.min.js",
            lambda route: route.fulfill(path=str(self.htmx_js), content_type="text/javascript"),
        )

    def tearDown(self):
        self.assertEqual(self.errors, [])
        self.context.close()

    def test_real_htmx_request_keeps_semantic_button_styled_and_swaps_results(self):
        self.page.goto(self.base + "/examples/htmx.html")
        self.page.wait_for_function("() => typeof window.htmx !== 'undefined'")
        button = self.page.locator("#search-button")
        height = button.evaluate("e => getComputedStyle(e).minHeight")
        self.assertEqual(height, "44px")
        self.page.locator("#query").fill("Acme")
        button.click()
        self.page.wait_for_function(
            "() => document.querySelector('#search-button').classList.contains('htmx-request')"
        )
        self.assertEqual(button.evaluate("e => getComputedStyle(e).minHeight"), height)
        self.assertNotEqual(button.locator(".htmx-indicator").evaluate(
            "e => getComputedStyle(e).display"), "none")
        self.page.get_by_text("Acme Corporation").wait_for()
        self.assertIn("1 customers", self.page.locator("#results").inner_text())
        self.assertFalse(button.evaluate("e => e.classList.contains('htmx-request')"))
        self.assertEqual(button.evaluate("e => getComputedStyle(e).minHeight"), height)
        self.assertEqual(self.page.locator("body").get_attribute("data-syn-theme"), "studio")

    def test_without_htmx_script_native_form_loads_complete_document(self):
        self.page.route(
            "https://unpkg.com/htmx.org@2.0.8/dist/htmx.min.js",
            lambda route: route.abort(),
        )
        self.page.goto(self.base + "/examples/htmx.html")
        self.page.locator("#query").fill("Northstar")
        self.page.locator("#search-button").click()
        self.page.wait_for_url("**/customers/search?q=Northstar")
        self.assertEqual(self.page.locator("h1").inner_text(), "Customer search")
        self.assertIn("Northstar Media", self.page.locator("#results").inner_text())


if __name__ == "__main__":
    unittest.main()
