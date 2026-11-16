"""Optional real-browser smoke for the server-rendered Syntyr OOH workspace.

Requires developer-installed Playwright browsers; never used by consumers.
Run: /path/to/playwright-python tests/operations_workspace_server_browser.py
"""
from pathlib import Path
import argparse
import sys
import threading

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))
from operations_workspace_server import create_server


def run(browser_name: str = "chromium", screenshot_dir: Path | None = None,
        axe_file: Path | None = None):
    from playwright.sync_api import sync_playwright

    server = create_server(port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}"
    try:
        with sync_playwright() as playwright:
            browser = getattr(playwright, browser_name).launch(headless=True)
            try:
                for width in (320, 390, 1280):
                    context = browser.new_context(viewport={"width": width, "height": 900},
                                                  bypass_csp=bool(axe_file))
                    page = context.new_page()
                    page.goto(url, wait_until="domcontentloaded")
                    page.locator("h1").wait_for()
                    assert page.locator("h1").count() == 1
                    assert page.locator(".syn-ops-record").count() == 6
                    assert page.locator("script").count() == 0
                    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"), f"Root overflow at {width}px"
                    assert page.locator(".syn-ops-marker").count() == 6
                    if axe_file:
                        page.add_script_tag(path=str(axe_file.resolve()))
                        audit = page.evaluate("""async () => axe.run(document, {
                            runOnly: {type: 'tag', values: [
                                'wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'
                            ]}
                        })""")
                        violations = [item["id"] for item in audit["violations"]]
                        incomplete = [item["id"] for item in audit["incomplete"]]
                        assert not violations, f"axe violations at {width}px: {violations}"
                        if incomplete:
                            print(f"MANUAL REVIEW {browser_name} {width}px: axe incomplete {incomplete}")

                    # Real native form submission; no client-side state manager.
                    page.locator("#filter-query").fill("east")
                    page.locator("#filter-status").select_option("available")
                    page.locator("#filter-type").select_option("static")
                    page.get_by_role("button", name="Apply filters").click()
                    page.wait_for_url("**/?query=east&status=available&type=static")
                    assert page.locator(".syn-ops-record").count() == 2
                    assert page.locator(".syn-ops-marker").count() == 2
                    page.get_by_role("link", name="View asset details").last.click()
                    page.wait_for_url("**selected=EV-035#selection")
                    assert page.locator("#selection").get_by_text("East Vista").count() == 1
                    assert page.locator(".syn-ops-record[data-syn-selected='true']").count() == 1
                    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")

                    # No-result state remains accessible and has no stale selection.
                    page.locator("#filter-query").fill("missing asset")
                    page.get_by_role("button", name="Apply filters").click()
                    assert page.get_by_text("No assets match your filters").count() == 1
                    assert page.locator("#selection").count() == 0

                    if screenshot_dir:
                        screenshot_dir.mkdir(parents=True, exist_ok=True)
                        page.goto(url)
                        page.screenshot(path=str(screenshot_dir / f"{browser_name}-{width}.png"), full_page=True)
                    context.close()
                    print(f"PASS {browser_name} at {width}px: native filtering, selection, empty state, no overflow")
            finally:
                browser.close()
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", choices=("chromium", "firefox", "webkit"), default="chromium")
    parser.add_argument("--screenshots", type=Path)
    parser.add_argument("--axe-file", type=Path, help="Optional local axe-core JS for WCAG smoke checks")
    args = parser.parse_args()
    if args.axe_file and not args.axe_file.is_file():
        parser.error(f"Missing axe-core file: {args.axe_file}")
    run(args.browser, args.screenshots, args.axe_file)
