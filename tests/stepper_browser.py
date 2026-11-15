"""Focused real-browser contract for the native, zero-JS workflow stepper.

Developer-only: python3 tests/stepper_browser.py --browsers chromium firefox webkit
Install Playwright outside the Syntyr runtime; unavailable engines are BLOCKED.
"""
import argparse
import traceback
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = (ROOT / "examples/workflow-steps.html").as_uri()


def check(browser, width, scale):
    context = browser.new_context(viewport={"width": width, "height": 850}, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(EXAMPLE, wait_until="load")
        assert page.locator("script").count() == 0
        assert page.get_by_role("list", name="Workspace setup progress").count() == 1
        assert page.locator(".syn-steps").count() == 2
        assert page.locator('.syn-steps:not(.syn-steps--vertical) > [aria-current="step"]').count() == 1
        assert page.locator(".syn-steps--vertical > .syn-step").count() == 3

        page.evaluate("(scale) => document.documentElement.style.fontSize = (16 * scale) + 'px'", scale)
        metrics = page.locator(".syn-steps").first.evaluate("""e => {
          const parent = e.parentElement, cs = getComputedStyle(parent);
          const contentWidth = parent.getBoundingClientRect().width -
            parseFloat(cs.paddingInlineStart) - parseFloat(cs.paddingInlineEnd);
          const rem = parseFloat(getComputedStyle(document.documentElement).fontSize);
          return { flow: getComputedStyle(e).gridAutoFlow, expected: contentWidth >= 43 * rem ?
            'column' : 'row' };
        }""")
        assert metrics["flow"] == metrics["expected"], (width, scale, metrics)
        assert page.locator(".syn-steps--vertical").evaluate(
            "e => getComputedStyle(e).gridAutoFlow") == "row"
        assert page.locator(".syn-step").first.evaluate(
            "e => getComputedStyle(e, '::before').content") != "none"
        scroll = page.evaluate("""() => ({
            scroll: document.documentElement.scrollWidth,
            client: document.documentElement.clientWidth
        })""")
        assert scroll["scroll"] <= scroll["client"] + 1, (width, scale, scroll)
    finally:
        context.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--browsers", nargs="+", choices=["chromium", "firefox", "webkit"],
                        default=["chromium"])
    args = parser.parse_args()
    errors = []
    with sync_playwright() as playwright:
        for name in args.browsers:
            try:
                browser = getattr(playwright, name).launch(headless=True)
            except Exception as e:
                print(f"BLOCKED {name}: {e}")
                errors.append(name)
                continue
            try:
                for width, scale in ((320, 1), (390, 1), (768, 1), (1280, 1),
                                     (320, 2), (390, 2), (768, 2)):
                    check(browser, width, scale)
                print(f"PASS {name}: 7 viewport/text combinations")
            except Exception as e:
                errors.append(name)
                print(f"FAIL {name}: {traceback.format_exc()}")
            finally:
                browser.close()
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
