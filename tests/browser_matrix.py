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
         "docs/console-kit.html", "examples/saas.html",
         "examples/business.html", "examples/terminal.html", "examples/geometry-terminal.html", "examples/geometry-terminal.html",
         "examples/vertigo-admin.html")


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
    assert css in ("#76e7f7", "#f1b574", "#2458c6"), (name, css)
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
    if name == "examples/geometry-terminal.html":
        frames = page.locator(".cy-frame")
        assert frames.count() == 5, "all five frame profiles must render"
        bevel = frames.first
        clip = bevel.evaluate("e => getComputedStyle(e, '::before').clipPath")
        assert clip.startswith("polygon("), (name, viewport, clip)
        fill = bevel.evaluate("e => getComputedStyle(e, '::after').backgroundColor")
        assert fill not in ("rgba(0, 0, 0, 0)", "transparent"), fill
        assert page.locator(".cy-terminal-error").count() == 1
        assert page.locator(".cy-terminal-warning").count() == 1
        numeric = page.locator(".cy-cell--numeric").first
        assert numeric.evaluate("e => getComputedStyle(e).textAlign") == "right"
        if viewport == 1280:
            panel_group = page.locator("#geometry .cy-grid")
            panel_group.evaluate("e => e.style.setProperty('--cy-frame-fill', '#225533')")
            inherited_fill = bevel.evaluate("e => getComputedStyle(e, '::after').backgroundColor")
            assert inherited_fill == "rgb(34, 85, 51)", inherited_fill

            page.evaluate("""() => {
                const controls = document.createElement('div');
                controls.innerHTML = '<button class="cy-button cy-button--primary" aria-disabled="true" id="cy-aria-disabled">ARIA disabled</button>'
                    + '<button class="cy-button cy-button--primary" disabled id="cy-native-disabled">Native disabled</button>';
                document.querySelector('main').append(controls);
            }""")
            aria_button = page.locator("#cy-aria-disabled")
            original_background = aria_button.evaluate("e => getComputedStyle(e).backgroundColor")
            aria_button.hover()
            assert aria_button.evaluate("e => getComputedStyle(e).backgroundColor") == original_background
            assert aria_button.evaluate("e => getComputedStyle(e).cursor") == "not-allowed"
            assert aria_button.evaluate("e => getComputedStyle(e).pointerEvents") != "none"
            native_button = page.locator("#cy-native-disabled")
            assert native_button.evaluate("e => getComputedStyle(e).cursor") == "not-allowed"

            page.emulate_media(forced_colors="active")
            assert bevel.evaluate("e => getComputedStyle(e).borderTopStyle") == "solid"
            assert bevel.evaluate("e => getComputedStyle(e, '::before').display") == "none"
    if name == "examples/vertigo-admin.html" and viewport == 1280:
        def styles():
            return page.evaluate("""() => {
                const card = document.querySelector('.cy-vertigo-admin .card');
                const button = document.querySelector('.cy-vertigo-admin button');
                function themeColor(token) {
                    const probe = document.createElement('span');
                    probe.style.backgroundColor = 'var(' + token + ')';
                    document.body.appendChild(probe);
                    const value = getComputedStyle(probe).backgroundColor;
                    probe.remove();
                    return value;
                }
                return {
                    cardBackground: getComputedStyle(card).backgroundColor,
                    surface: themeColor('--cy-surface'),
                    buttonBackground: getComputedStyle(button).backgroundColor,
                    accent: themeColor('--cy-accent')
                };
            }""")
        studio = styles()
        assert studio["cardBackground"] == studio["surface"], studio
        assert studio["buttonBackground"] == studio["accent"], studio
        page.locator("body").evaluate("e => e.setAttribute('data-cy-theme', 'noir')")
        noir = styles()
        assert noir["cardBackground"] == noir["surface"], noir
        assert noir["buttonBackground"] == noir["accent"], noir
        assert noir["accent"] != studio["accent"], "theme override was ignored"
        # Negative control: removing the optional adapter must remove its paint.
        page.locator('link[href="../integrations/vertigo/admin.css"]').evaluate("e => e.remove()")
        without_adapter = styles()
        assert without_adapter["cardBackground"] != without_adapter["surface"], (
            "adapter has no observable opt-in behavior"
        )
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
