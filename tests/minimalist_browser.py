"""Optional runtime verification of native auto palette and intrinsic layouts."""
import argparse
import os
import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = (ROOT / "examples/minimalist-patterns.html").as_uri()


def assert_minimalist(browser, engine):
    for color_scheme, expected_bg in (
        ("light", "rgb(245, 247, 251)"),
        ("dark", "rgb(8, 15, 25)"),
    ):
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            color_scheme=color_scheme,
            reduced_motion="reduce",
        )
        page = context.new_page()
        try:
            page.goto(EXAMPLE)
            background = page.locator("body").evaluate("(node) => getComputedStyle(node).backgroundColor")
            assert background == expected_bg, (engine, color_scheme, "auto background", background)

            tints = page.evaluate("""() => {
              const swatch = document.createElement('span');
              swatch.style.backgroundColor = 'var(--syn-accent-soft)';
              document.body.appendChild(swatch);
              const original = getComputedStyle(swatch).backgroundColor;
              document.body.style.setProperty('--syn-accent', '#ff0000');
              const overridden = getComputedStyle(swatch).backgroundColor;
              document.body.style.removeProperty('--syn-accent');
              swatch.remove();
              return [original, overridden];
            }""")
            assert tints[0] != tints[1] and '0, 0, 0, 0)' not in tints[0], (
                engine, color_scheme, 'soft accent does not track token override', tints)

            noir = page.locator('[data-syn-theme="noir"]').evaluate("(node) => getComputedStyle(node).getPropertyValue('--syn-bg').trim()")
            assert noir == "#0e0e12", (engine, color_scheme, "explicit nested theme", noir)

            checkbox_label = page.locator('label:has(> input[type="checkbox"])').evaluate(
                "(node) => getComputedStyle(node).display")
            text_label = page.locator('label[for="email"]').evaluate(
                "(node) => getComputedStyle(node).display")
            assert checkbox_label == "block" and text_label == "grid", (engine, checkbox_label, text_label)

            for choice in page.locator('input[type="checkbox"], input[type="radio"]').all():
                target = choice.bounding_box()
                assert target["width"] >= 24 and target["height"] >= 24, (
                    engine, "WCAG 2.2 target size", target)

            heading_size = page.locator(".syn-fluid-display").evaluate(
                "(node) => parseFloat(getComputedStyle(node).fontSize)")
            assert 32 <= heading_size <= 68, (engine, heading_size)

            def positions():
                sidebar = page.locator(".syn-sidebar > aside").bounding_box()
                content = page.locator(".syn-sidebar > section").bounding_box()
                cards = [node.bounding_box() for node in page.locator(".syn-switcher > article").all()]
                return sidebar, content, cards

            left, right, cards = positions()
            assert left["x"] + left["width"] <= right["x"] + 2, (engine, "sidebar is not two columns", left, right)
            assert max(abs(cards[0]["y"] - c["y"]) for c in cards) <= 2, (engine, "switcher not inline", cards)

            page.set_viewport_size({"width": 320, "height": 900})
            left, right, cards = positions()
            assert left["y"] + left["height"] <= right["y"] + 2, (engine, "sidebar not stacked", left, right)
            assert cards[0]["y"] < cards[1]["y"] < cards[2]["y"], (engine, "switcher not stacked", cards)
            # Small root text and mixed emphasized inline content must not shrink
            # the native control below 24 CSS px or prevent normal text wrapping.
            page.evaluate("""() => {
              document.documentElement.style.fontSize = '12px';
              const label = document.querySelector('label:has(> input[type="checkbox"])');
              label.insertAdjacentHTML('beforeend',
                ' Receive <strong>important</strong> account <strong>notifications</strong> from our service, including several long-form messages.');
            }""")
            for target in page.locator('input[type="checkbox"], input[type="radio"]').all():
                choice = target.bounding_box()
                assert choice["width"] >= 24 and choice["height"] >= 24, (
                    engine, color_scheme, choice)
            assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 1

            submit = page.get_by_role("button", name="Preview native submission")
            submit.focus()
            outline = submit.evaluate("(node) => getComputedStyle(node).outlineStyle")
            assert outline != "none", (engine, "missing keyboard focus")
            assert page.locator("script").count() == 0
        finally:
            context.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--browsers", nargs="+", choices=("chromium", "firefox", "webkit"),
                        default=("chromium", "firefox", "webkit"))
    args = parser.parse_args()
    failures = 0
    with sync_playwright() as playwright:
        for engine in args.browsers:
            try:
                kwargs = {"headless": True}
                if engine == "chromium":
                    executable = (os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
                                  or shutil.which("chromium") or shutil.which("chromium-browser"))
                    if executable:
                        kwargs.update(executable_path=executable, args=["--no-sandbox"])
                browser = getattr(playwright, engine).launch(**kwargs)
            except Exception as exc:
                failures += 1
                print(f"BLOCKED {engine}: {str(exc).splitlines()[0]}", flush=True)
                continue
            try:
                assert_minimalist(browser, engine)
                print(f"PASS {engine}: 2 palettes, nested theme, forms, fluid type, 2 layouts, mobile reflow", flush=True)
            except Exception as exc:
                failures += 1
                print(f"FAIL {engine}: {type(exc).__name__}: {exc}", flush=True)
            finally:
                browser.close()
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
