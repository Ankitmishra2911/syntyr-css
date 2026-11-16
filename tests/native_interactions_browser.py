"""Optional cross-browser smoke test for script-free native interaction recipes.

Run with developer-installed Playwright:
    python3 tests/native_interactions_browser.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "examples/native-interactions.html").as_uri()
GROUP = 'details[name="native-interaction-faq"]'


def check(browser_type, engine, width, forced_colors=False):
    browser = browser_type.launch(headless=True)
    try:
        context = browser.new_context(
            viewport={"width": width, "height": 540 if width == 360 else 800},
            java_script_enabled=False,
            reduced_motion="reduce",
            forced_colors="active" if forced_colors else "none",
        )
        page = context.new_page()
        page.goto(URL, wait_until="domcontentloaded")
        assert page.locator("script").count() == 0
        group = page.locator(GROUP)
        assert group.count() == 3
        assert group.evaluate_all("els => els.filter(el => el.open).length") == 1
        group.nth(1).locator("summary").click()
        assert group.nth(1).get_attribute("open") is not None
        assert group.nth(0).get_attribute("open") is None
        group.nth(2).locator("summary").focus()
        page.keyboard.press("Enter")
        assert group.nth(2).get_attribute("open") is not None
        assert group.nth(1).get_attribute("open") is None

        # Invoker commands work without a framework or any inline script.
        page.get_by_role("button", name="Review a confirmation").click()
        dialog = page.locator("#native-interaction-confirm")
        assert dialog.is_visible(), (engine, "dialog did not open")
        assert dialog.evaluate("el => el.matches(':modal')")
        bounds = dialog.bounding_box()
        assert bounds is not None
        assert bounds["x"] >= -1 and bounds["x"] + bounds["width"] <= width + 1, bounds
        # Enlarged root text and short viewports must not push modal controls
        # outside the browser's bounded scrollable top layer.
        page.evaluate("document.documentElement.style.fontSize = '200%'")
        enlarged = dialog.bounding_box()
        assert enlarged["x"] >= -1 and enlarged["x"] + enlarged["width"] <= width + 1, enlarged
        assert enlarged["height"] <= page.viewport_size["height"] + 1, enlarged
        page.evaluate("document.documentElement.style.fontSize = ''")
        assert dialog.evaluate("el => getComputedStyle(el).overflowY") == "auto"
        dialog.get_by_role("button", name="Cancel").click()
        assert not dialog.is_visible(), (engine, "dialog did not close")
        page.get_by_role("button", name="Review a confirmation").click()
        page.keyboard.press("Escape")
        assert not dialog.is_visible(), (engine, "Escape did not close dialog")

        cities = page.locator("#native-interaction-city")
        assert cities.get_attribute("list") == "native-interaction-cities"
        cities.fill("Custom City")
        assert cities.input_value() == "Custom City"
        select = page.locator("#native-interaction-market")
        select.select_option("br")
        assert select.input_value() == "br"
        meter = page.locator("#native-interaction-capacity")
        assert meter.evaluate("el => el.value") == 68
        assert page.locator("#native-interaction-result").inner_text() == "42 available locations"

        # A static site can demonstrate native GET navigation without pretending
        # to return application-owned filtered results.
        query = page.locator("#native-interaction-query")
        query.fill("billboard & lighting")
        page.get_by_role("button", name="Search", exact=True).click()
        assert "q=billboard+%26+lighting" in page.url, page.url
        assert page.locator("main").is_visible()
        if forced_colors:
            assert page.evaluate("matchMedia('(forced-colors: active)').matches")
        print(f"PASS {engine} width={width} forced_colors={forced_colors}")
    finally:
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        for engine in ("chromium", "firefox"):
            for width in (320, 360, 1280):
                check(getattr(playwright, engine), engine, width, forced_colors=False)
        check(playwright.chromium, "chromium", 360, forced_colors=True)
