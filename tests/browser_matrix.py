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
         "docs/console-kit.html", "examples/themes.html")


def assert_page(browser, name: str, viewport: int) -> None:
    context = browser.new_context(viewport={"width": viewport, "height": 820},
                                  reduced_motion="reduce")
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda err: errors.append(str(err)))
    url = (ROOT / name).as_uri()
    response = page.goto(url, wait_until="load")
    assert page.url == url, (url, page.url)
    assert response is None or response.ok, (url, response.status)
    assert page.locator("script").count() == 0, name
    assert page.get_by_role("main").count() == 1, name
    assert page.locator('link[rel="stylesheet"]').count() >= 1
    css = page.locator("body").evaluate("e => getComputedStyle(e).getPropertyValue('--cy-accent').trim()")
    assert css in ("#76e7f7", "#f1b574", "#313a45"), (name, css)
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
        assert page.get_by_role("searchbox", name="SEARCH BY NAME").count() == 1
    if name == "examples/themes.html":
        expected = {
            "grid": ("#76e7f7", "dark"),
            "noir": ("#f1b574", "dark"),
            "industrial": ("#ffb36b", "dark"),
            "terminal": ("#65e8a0", "dark"),
            "corporate": ("#155ac8", "light"),
            "minimal": ("#313a45", "light"),
        }
        assert page.locator(".theme-tile").count() == len(expected)
        for theme, (accent, scheme) in expected.items():
            tile = page.locator(f'.theme-tile[data-cy-theme="{theme}"]')
            assert tile.count() == 1, theme
            values = tile.evaluate("""e => ({
                accent: getComputedStyle(e).getPropertyValue('--cy-accent').trim(),
                colorScheme: getComputedStyle(e).colorScheme
            })""")
            assert values["accent"] == accent, (theme, values)
            assert values["colorScheme"] == scheme, (theme, values)
            button = tile.locator(".cy-button--primary")
            assert button.is_visible(), (theme, "primary button hidden")
        if viewport == 1280:
            nested = page.evaluate("""() => {
                function create(parent, name, classes) {
                    const node = document.createElement('section');
                    node.className = classes;
                    node.dataset.cyTheme = name;
                    node.innerHTML = '<h3>Nested theme heading</h3>';
                    parent.append(node);
                    const style = getComputedStyle(node);
                    return {
                        text: getComputedStyle(node.querySelector('h3')).color,
                        colorScheme: style.colorScheme,
                        radius: style.getPropertyValue('--cy-radius').trim(),
                        cut: style.getPropertyValue('--cy-cut').trim()
                    };
                }
                const grid = document.querySelector('.theme-tile[data-cy-theme="grid"]');
                const corporate = document.querySelector('.theme-tile[data-cy-theme="corporate"]');
                const terminal = document.querySelector('.theme-tile[data-cy-theme="terminal"]');
                const lightInDark = create(grid, 'corporate', 'cy-price-card');
                const darkInLight = create(corporate, 'grid', 'cy-price-card');
                const gridInTerminal = create(terminal, 'grid', 'cy-panel cy-panel--cut');
                const flex = document.createElement('div');
                flex.className = 'cy-u-flex cy-u-between cy-u-center';
                corporate.append(flex);
                return {lightInDark, darkInLight, gridInTerminal,
                        justify: getComputedStyle(flex).justifyContent,
                        align: getComputedStyle(flex).alignItems};
            }""")
            assert nested["lightInDark"]["text"] == "rgb(24, 39, 60)", nested
            assert nested["lightInDark"]["colorScheme"] == "light", nested
            assert nested["darkInLight"]["text"] == "rgb(237, 249, 255)", nested
            assert nested["darkInLight"]["colorScheme"] == "dark", nested
            assert nested["gridInTerminal"]["radius"] == ".25rem", nested
            assert nested["gridInTerminal"]["cut"] == ".9rem", nested
            assert nested["justify"] == "space-between", nested
            assert nested["align"] == "center", nested
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
                        try:
                            assert_page(browser, path, width)
                        except Exception as exc:
                            raise AssertionError(f"{path} viewport {width}: {exc}") from exc
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
