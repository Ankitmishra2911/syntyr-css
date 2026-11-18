"""Opt-in browser tests for accessibility regressions in shipped examples.

Runs against the actual CSS without adding runtime dependencies. Example:
  python tests/accessibility_regression_browser.py --browsers chromium firefox
"""
import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check(browser, engine):
    # All shipping palettes, including focus/filled states. Test 2x/4x root text
    # enlargement rather than claiming to emulate browser-UI zoom.
    for theme in ('studio', 'grid', 'noir', 'industrial', 'terminal', 'corporate', 'minimal'):
        for size in (32, 64):
            page = browser.new_page(viewport={"width": 320, "height": 800})
            try:
                page.goto((ROOT / "examples/native-recipes.html").as_uri())
                page.locator('.syn-root').first.evaluate("(root, theme) => root.setAttribute('data-syn-theme', theme)", theme)
                page.evaluate("size => { document.documentElement.style.fontSize = size + 'px' }", size)
                field = page.locator('#example-email')
                label = page.locator('label[for="example-email"]')

                def check_layout(state):
                    layout = label.evaluate('''label => {
                        const field = document.querySelector('#example-email');
                        const l = label.getBoundingClientRect();
                        const f = field.getBoundingClientRect();
                        return {
                            readable: label.scrollWidth <= label.clientWidth + 1,
                            stackedAbove: l.bottom <= f.top + 1,
                            fieldOverflow: field.parentElement.scrollWidth > field.parentElement.clientWidth + 1
                        };
                    }''')
                    assert layout['readable'], f"{engine} {theme} {size}px {state}: clipped label: {layout}"
                    assert layout['stackedAbove'], f"{engine} {theme} {size}px {state}: overlap: {layout}"
                    assert not layout['fieldOverflow'], f"{engine} {theme} {size}px {state}: overflow: {layout}"

                check_layout('empty')
                field.focus()
                check_layout('focused')
                field.fill('dev@example.com')
                check_layout('filled')
            finally:
                page.close()

    # Wide layouts should retain the opt-in floating effect.
    page = browser.new_page(viewport={"width": 1100, "height": 820})
    try:
        page.goto((ROOT / 'examples/native-recipes.html').as_uri())
        label = page.locator('label[for="example-email"]')
        field = page.locator('#example-email')
        field.fill('dev@example.com')
        assert label.evaluate('e => getComputedStyle(e).transform') != 'none', (
            f"{engine}: floating enhancement unexpectedly disabled on wide fields")
        page.locator('body').evaluate("e => e.setAttribute('dir', 'rtl')")
        field.fill('')
        field.blur()
        before = label.bounding_box()
        field.fill('dev@example.com')
        after = label.bounding_box()
        right_before = before['x'] + before['width']
        right_after = after['x'] + after['width']
        assert abs(right_before - right_after) <= 2, (
            f"{engine}: RTL floating label must shrink toward inline-start, "
            f"not move away from its right edge", before, after)
    finally:
        page.close()

    page = browser.new_page(viewport={"width": 320, "height": 800})
    try:
        page.goto((ROOT / "examples/resources.html").as_uri())
        table = page.locator('.syn-table-wrap.resource-table')
        assert table.count() == 1
        attrs = table.evaluate('''e => ({
            hasOverflow: e.scrollWidth > e.clientWidth + 2,
            name: e.getAttribute('aria-label'),
            role: e.getAttribute('role'),
            tabindex: e.getAttribute('tabindex')
        })''')
        assert attrs['hasOverflow'], f"{engine}: expected overflow for keyboard scroll test: {attrs}"
        assert attrs['role'] == 'region' and attrs['name'] and attrs['tabindex'] == '0', (
            f"{engine}: scrolling table lacks explicit keyboard/region semantics: {attrs}")
        table.focus()
        assert table.evaluate('e => document.activeElement === e'), f"{engine}: table cannot receive focus"
        page.keyboard.press('ArrowRight')
        page.wait_for_function("document.querySelector('.resource-table').scrollLeft > 0", timeout=2000)
    finally:
        page.close()

    for path, selectors in [
        ('index.html', ['.site-brand', '.site-nav a', '.site-tertiary-link',
                        '.site-showcase-card > .site-secondary-link', '.site-footer a']),
        ('docs/index.html', ['.docs-header .syn-logo', '.docs-flagship-links a', 'footer.syn-header a']),
    ]:
        page = browser.new_page(viewport={"width": 1280, "height": 820})
        try:
            page.goto((ROOT / path).as_uri())
            for selector in selectors:
                matches = page.locator(selector)
                assert matches.count(), f"{engine}: missing tested target {selector} on {path}"
                for idx in range(matches.count()):
                    height = matches.nth(idx).bounding_box()['height']
                    assert height >= 24, f"{engine}: undersized {path} {selector} [{idx}]: {height}px"
        finally:
            page.close()
    # Browser forced-colors *emulation* is useful regression coverage, but it
    # does not stand in for a native OS high-contrast screen-reader review.
    for path, selector in (
        ('docs/blocks.html', '.syn-block-asset--dot-field > span'),
        ('docs/blocks.html', '.syn-block-asset--diagonal > span'),
        ('examples/flagship-grid.html', '.flagship-lede'),
    ):
        page = browser.new_page(viewport={"width": 390, "height": 820},
                                forced_colors='active', reduced_motion='reduce')
        try:
            page.goto((ROOT / path).as_uri())
            assert page.evaluate("matchMedia('(forced-colors: active)').matches"), (
                f"{engine}: forced-colors emulation not applied")
            assert page.get_by_role('main').count() == 1, path
            target = page.locator(selector)
            assert target.is_visible(), f"{engine}: forced-colors target hidden: {path} {selector}"
            colors = target.evaluate('''e => ({foreground: getComputedStyle(e).color,
                background: getComputedStyle(e).backgroundColor})''')
            assert colors['foreground'] != colors['background'], (
                f"{engine}: forced-colors collapsed text and background: {path} {colors}")
            if path == 'docs/blocks.html':
                beam = page.locator('.syn-block-asset--beam')
                assert beam.evaluate("e => getComputedStyle(e).animationDuration") == '0s', (
                    f"{engine}: reduced-motion beam animation still active")
        finally:
            page.close()

    print(f"{engine}: floating labels, keyboard-scrollable table, and site link targets, forced-color emulation passed")


def main():
    from playwright.sync_api import sync_playwright
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browsers', nargs='+', choices=('chromium', 'firefox', 'webkit'),
                        default=['chromium', 'firefox'])
    args = parser.parse_args()
    with sync_playwright() as playwright:
        for engine in args.browsers:
            options = {"headless": True}
            if engine == "webkit" and os.environ.get("SYNTYR_WEBKIT_EXECUTABLE"):
                options["executable_path"] = os.environ["SYNTYR_WEBKIT_EXECUTABLE"]
            browser = getattr(playwright, engine).launch(**options)
            try:
                check(browser, engine)
            finally:
                browser.close()


if __name__ == '__main__':
    main()
