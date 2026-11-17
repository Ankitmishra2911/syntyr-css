"""Optional browser smoke test for Syntyr's local-only visual page composer.

Run from repository root: python3 tests/page_builder_browser.py
"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import threading
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, *_args):
        pass


def verify(browser, base_url, width):
    context = browser.new_context(viewport={"width": width, "height": 900}, accept_downloads=True)
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.goto(base_url + "/docs/page-builder.html", wait_until="load")
    preview = page.frame_locator("#builder-preview")
    preview.locator(".syn-stage h1").wait_for()
    expect(preview.locator(".syn-stage h1")).to_have_text("Build your next website visually.")
    assert page.locator("#builder-outline > li").count() == 3

    page.locator('[data-block-type="quote"]').click()
    assert page.locator("#builder-outline > li").count() == 4
    page.locator("#builder-inspector [data-field='quote']").fill("Testimonial from browser smoke test")
    expect(preview.locator("blockquote p")).to_have_text("Testimonial from browser smoke test")

    page.locator("#builder-undo").click()
    expect(preview.locator("blockquote p")).not_to_have_text("Testimonial from browser smoke test")
    page.locator("#builder-redo").click()
    expect(preview.locator("blockquote p")).to_have_text("Testimonial from browser smoke test")
    page.locator('#builder-outline [data-index="3"] [data-action="up"]').click()
    assert page.locator('#builder-outline [data-index="2"] [data-action="select"]').get_attribute("aria-label").startswith("Edit Testimonial")
    page.locator('#builder-outline [data-index="2"] [data-action="down"]').click()

    page.locator("#builder-theme").select_option("grid")
    expect(preview.locator("body")).to_have_attribute("data-syn-theme", "grid")
    for preset, pixels in (("desktop", 1200), ("tablet", 760), ("mobile", 390)):
        page.locator("#builder-viewport").select_option(preset)
        expect(page.locator("#builder-viewport-frame")).to_have_class(
            "builder-viewport builder-viewport--" + preset
        )
        assert preview.locator("body").evaluate("() => innerWidth") == pixels

    page.locator('[data-block-type="faq"]').click()
    expect(page.locator("#builder-outline > li")).to_have_count(5)
    preview.locator("details summary").first.click()
    expect(preview.locator("details").first).to_have_attribute("open", "")
    expect(preview.locator("details p").first).to_be_visible()
    page.locator("#builder-undo").click()
    expect(page.locator("#builder-outline > li")).to_have_count(4)
    page.locator("#builder-redo").click()
    expect(page.locator("#builder-outline > li")).to_have_count(5)
    page.locator('#builder-outline [data-index="4"] [data-action="up"]').click()
    expect(page.locator('#builder-outline [data-index="3"] [data-action="up"]')).to_be_focused()

    # Some remote headless browsers cancel file downloads at the OS boundary.
    # Capture the actual Blob payload without mocking the builder's export code.
    page.evaluate("""() => {
        const original = URL.createObjectURL.bind(URL);
        URL.createObjectURL = (blob) => {
            window.__lastBuilderBlob = blob;
            return original(blob);
        };
    }""")
    with page.expect_download() as download_info:
        page.locator("#builder-export-html").click()
    assert download_info.value.suggested_filename == "index.html"
    html = page.evaluate("async () => await window.__lastBuilderBlob.text()")
    assert 'href="syntyr.all.css"' in html
    assert "Testimonial from browser smoke test" in html
    assert "<script" not in html

    with page.expect_download() as download_info:
        page.locator("#builder-export-json").click()
    assert download_info.value.suggested_filename == "syntyr-page.json"
    data = json.loads(page.evaluate("async () => await window.__lastBuilderBlob.text()"))
    assert data["schema"] == "syntyr.page.v1"
    assert data["theme"] == "grid"
    assert data["blocks"][-1]["type"] == "quote"

    project_bytes = json.dumps(data).encode()
    page.locator("#builder-import").set_input_files({
        "name": "page.json", "mimeType": "application/json", "buffer": project_bytes,
    })
    expect(page.locator("#builder-status")).to_contain_text("Project opened.")
    expect(page.locator("#builder-outline > li")).to_have_count(5)
    page.locator("#builder-import").set_input_files({
        "name": "bad.json", "mimeType": "application/json", "buffer": b'{"schema":"invalid"}',
    })
    expect(page.locator("#builder-status")).to_contain_text("Cannot open project")
    expect(page.locator("#builder-outline > li")).to_have_count(5)

    invalid = json.loads(json.dumps(data))
    invalid["blocks"][0]["type"] = ["hero"]
    page.locator("#builder-import").set_input_files({
        "name": "invalid-type.json", "mimeType": "application/json",
        "buffer": json.dumps(invalid).encode(),
    })
    expect(page.locator("#builder-status")).to_contain_text("Cannot open project")
    expect(page.locator("#builder-outline > li")).to_have_count(5)

    assert page.locator("body").evaluate("e => e.scrollWidth <= innerWidth + 1")
    assert not errors, errors
    context.close()


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                for width in (390, 1280):
                    verify(browser, "http://127.0.0.1:" + str(server.server_port), width)
                    print("PASS visual builder chromium", width)
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
