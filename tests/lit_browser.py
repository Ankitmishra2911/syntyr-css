"""Optional real-browser coverage for the bundled Syntyr + Lit sample.

Build the isolated example first:
  cd examples/lit && npm ci && npm run build && cd ../..
Then (with Python Playwright and browsers installed):
  python3 tests/lit_browser.py --browsers chromium,firefox,webkit
No third-party runtime network requests; Lit is not part of Syntyr core.
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import shutil
import sys
from threading import Thread

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "examples/lit/dist/demo.js"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def run_checks(browser, name, url):
    nojs = browser.new_context(java_script_enabled=False)
    try:
        page = nojs.new_page()
        page.goto(url, wait_until="load")
        fallbacks = page.locator("[data-lit-fallback]")
        assert fallbacks.count() == 2, (name, "missing no-JS fallback")
        assert all(fallbacks.nth(i).is_visible() for i in range(2)), (name, "hidden fallback")
        assert "Online" in fallbacks.first.inner_text()
    finally:
        nojs.close()

    context = browser.new_context(viewport={"width": 1200, "height": 800},
                                  reduced_motion="reduce")
    try:
        page = context.new_page()
        errors = []
        external_requests = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("request", lambda request: (
            external_requests.append(request.url)
            if not request.url.startswith(url.split("/examples/")[0] + "/") else None
        ))
        page.goto(url, wait_until="load")
        light = page.locator("syn-demo-status-panel")
        light.locator(".syn-panel .syn-status").wait_for()
        assert light.locator("[data-lit-fallback]").count() == 0, (name, "duplicate fallback")
        assert light.get_attribute("online") == "", (name, "online attribute not reflected")
        assert light.locator(".syn-status--success").inner_text() == "Online"
        assert light.locator(".syn-panel").evaluate(
            "e => getComputedStyle(e).position") == "relative", (name, "light DOM unstyled")

        light_button = light.get_by_role("button")
        light_button.click()
        assert light.get_attribute("online") is None, (name, "light reflected state")
        assert light.locator(".syn-status--warning").inner_text() == "Offline"
        assert "North hub: offline" in page.locator("#event-output").inner_text()
        light.evaluate("e => e.busy = true")
        assert light_button.is_disabled(), (name, "disabled state")
        light.evaluate("e => e.busy = false")
        light_button.focus()
        page.keyboard.press("Enter")
        assert light.get_attribute("online") == "", (name, "keyboard activation")

        shadow = page.locator("syn-demo-shadow-signal")
        shadow_button = shadow.locator("button[part='toggle']")
        shadow_button.wait_for()
        assert shadow.evaluate("e => e.shadowRoot !== null"), (name, "no shadow root")
        assert shadow.locator("[part='panel']").count() == 1
        assert shadow_button.get_attribute("aria-pressed") == "true"
        shadow_button.focus()
        page.keyboard.press("Enter")
        assert shadow_button.get_attribute("aria-pressed") == "false"
        assert shadow.get_attribute("active") is None, (name, "shadow reflected state")
        assert "composed shadow event" in page.locator("#event-output").inner_text()
        assert shadow.locator("[part='panel']").evaluate(
            "e => getComputedStyle(e).borderTopStyle") == "dashed", (name, "::part style")

        panel = shadow.locator("[part='panel']")
        before = panel.evaluate("e => getComputedStyle(e).backgroundColor")
        page.locator('section[data-syn-theme="noir"]').evaluate(
            "e => e.dataset.synTheme = 'grid'")
        after = panel.evaluate("e => getComputedStyle(e).backgroundColor")
        assert before != after, (name, "shadow did not inherit nested theme", before, after)
        assert shadow.evaluate(
            "e => getComputedStyle(e).getPropertyValue('--syn-accent').trim()"
        ), (name, "missing inherited token")

        assert not errors, (name, "runtime errors", errors)
        assert not external_requests, (name, "unexpected external requests", external_requests)
    finally:
        context.close()


def run_framework_checks(browser, name, base_url):
    """Exercise real React 19 custom events and real HTMX host replacement."""
    react_url = base_url + "/examples/lit/react-interop.html"
    htmx_url = base_url + "/examples/lit/htmx-interop.html"
    nojs = browser.new_context(java_script_enabled=False)
    try:
        page = nojs.new_page()
        page.goto(react_url)
        assert page.locator("[data-nojs-fallback]").is_visible(), (name, "React no-JS fallback")
        page.goto(htmx_url)
        assert page.locator("#htmx-result [data-lit-fallback]").is_visible(), (name, "HTMX fallback")
        page.get_by_role("button", name="Load relay status").click()
        assert "/examples/lit/htmx-result.html" in page.url, (name, "native GET navigation")
        assert page.locator("#htmx-result [data-lit-fallback]").is_visible(), (name, "GET response")
    finally:
        nojs.close()

    context = browser.new_context()
    try:
        page = context.new_page()
        errors = []
        external_requests = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("request", lambda request: (
            external_requests.append(request.url)
            if not request.url.startswith(base_url + "/") else None
        ))
        page.goto(react_url)
        react_custom = page.locator("#react-root syn-demo-status-panel")
        react_custom.get_by_role("button", name="Mark offline").click()
        page.get_by_text("React customer hub: offline (React 19 handler)",
                         exact=True).wait_for(timeout=5000)
        assert react_custom.locator(".syn-status--warning").count() == 1

        page.goto(htmx_url)
        original = page.locator("#htmx-result syn-demo-status-panel")
        original.locator(".syn-status--warning").wait_for()
        original.evaluate("e => e.dataset.testOld = 'yes'")
        page.get_by_role("button", name="Load relay status").click()
        replaced = page.locator("#htmx-result syn-demo-status-panel")
        replaced.locator(".syn-status--success").wait_for()
        assert page.url == htmx_url, (name, "HTMX did not intercept GET")
        assert replaced.get_attribute("data-test-old") is None, (name, "old host not replaced")
        assert replaced.locator("[data-lit-fallback]").count() == 0, (
            name, "new Lit host not upgraded")
        replaced.get_by_role("button", name="Mark offline").click()
        assert "HTMX relay: offline" in page.locator("#htmx-event-output").inner_text(), (
            name, "custom event after HTMX swap")
        assert not errors, (name, "framework runtime errors", errors)
        assert not external_requests, (name, "unexpected external requests", external_requests)
    finally:
        context.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browsers", default="chromium,firefox,webkit",
                        help="Comma-separated browser engines (chromium,firefox,webkit)")
    args = parser.parse_args()
    browsers = [item.strip() for item in args.browsers.split(",") if item.strip()]
    if not browsers or any(item not in {"chromium", "firefox", "webkit"} for item in browsers):
        parser.error("Choose chromium,firefox,webkit (comma-separated)")
    if not BUNDLE.is_file():
        print("BLOCKED: build the optional Lit example with npm ci && npm run build first")
        return 1
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("BLOCKED: install developer-only Python Playwright")
        return 1
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    url = f"http://127.0.0.1:{server.server_port}/examples/lit/index.html"
    failures = 0
    try:
        with sync_playwright() as playwright:
            for name in browsers:
                launch = {"headless": True}
                if name == "chromium":
                    executable = (os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
                                  or shutil.which("chromium")
                                  or shutil.which("chromium-browser"))
                    if executable:
                        launch.update(executable_path=executable, args=["--no-sandbox"])
                try:
                    browser = getattr(playwright, name).launch(**launch)
                except Exception as error:
                    print(f"BLOCKED {name}: {str(error).splitlines()[0]}")
                    failures += 1
                    continue
                try:
                    run_checks(browser, name, url)
                    run_framework_checks(browser, name, url.split("/examples/")[0])
                    print(f"PASS {name}: Lit, React 19, HTMX, native GET fallback, themes and events")
                except Exception as error:
                    print(f"FAIL {name}: {type(error).__name__}: {error}")
                    failures += 1
                finally:
                    browser.close()
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=3)
    return int(failures != 0)


if __name__ == "__main__":
    sys.exit(main())
