"""Opt-in browser matrix: no runtime JS or CSS dependency introduced.

Requires developer-only Playwright + browsers:
  python3 tests/browser_matrix.py --browsers chromium firefox webkit
  PLAYWRIGHT_CHROMIUM_EXECUTABLE=/usr/bin/chromium-browser python3 ...
Run on a machine with the native browser dependencies installed. A missing
browser is reported as BLOCKED and never counted as PASS.
"""
import argparse
from pathlib import Path
import os
import shutil
import sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "docs/index.html", "examples/console.html",
         "examples/resources.html", "examples/pricing.html",
         "docs/console-kit.html")


def assert_page(browser, name: str, viewport: int) -> None:
    context = browser.new_context(viewport={"width": viewport, "height": 820},
                                  reduced_motion="reduce")
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda err: errors.append(str(err)))
    url = (ROOT / name).as_uri()
    response = page.goto(url, wait_until="load")
    assert response is not None and response.ok, (url, response and response.status)
    assert page.locator("script").count() == 0, name
    assert page.get_by_role("main").count() == 1, name
    assert page.locator('link[rel="stylesheet"]').count() >= 1
    css = page.locator("body").evaluate("e => getComputedStyle(e).getPropertyValue('--cy-accent').trim()")
    assert css in ("#76e7f7", "#f1b574"), (name, css)
    overflow = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    assert overflow <= 1, (name, viewport, overflow)
    assert not errors, (name, errors)
    if name == "docs/index.html" and viewport == 1280:
        button = page.get_by_role("button", name="OPEN COMMAND")
        button.focus()
        outline = button.evaluate("e => getComputedStyle(e).outlineStyle")
        assert outline != "none", outline
        page.keyboard.press("Enter")
        popover = page.locator("#command-popover")
        assert popover.evaluate('e => e.matches(":popover-open")'), "popover cannot open"
        page.keyboard.press("Escape")
        assert not popover.evaluate('e => e.matches(":popover-open")'), "popover cannot dismiss"
        details = page.locator("#components details").first
        details.locator("summary").click()
        assert details.evaluate("e => e.open"), "disclosure cannot open"
    if name == "examples/resources.html":
        assert page.get_by_role("search").count() == 1
        assert page.get_by_role("table").count() == 1
        assert page.get_by_role("textbox", name="SEARCH BY NAME").count() == 1
    context.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browsers", nargs="+",
                        choices=("chromium", "firefox", "webkit"),
                        default=("chromium", "firefox", "webkit"))
    args = parser.parse_args()
    with sync_playwright() as p:
        failed = 0
        for name in args.browsers:
            kwargs = {"headless": True}
            if name == "chromium":
                exe = (os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
                       or shutil.which("chromium") or shutil.which("chromium-browser"))
                if exe:
                    kwargs["executable_path"] = exe
                    kwargs["args"] = ["--no-sandbox"]
            try:
                browser = getattr(p, name).launch(**kwargs)
            except Exception as exc:
                failed += 1
                print(f"BLOCKED {name}: {str(exc).splitlines()[0]}", flush=True)
                continue
            try:
                for path in PAGES:
                    for width in (320, 390, 1280):
                        assert_page(browser, path, width)
                print(f"PASS {name}: {len(PAGES)} pages × 3 viewports + keyboard/popover checks",
                      flush=True)
            except Exception as exc:
                failed += 1
                print(f"FAIL {name}: {type(exc).__name__} {exc}", flush=True)
            finally:
                browser.close()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
