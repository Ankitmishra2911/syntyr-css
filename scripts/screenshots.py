"""Create development previews with an optional Chromium/Playwright install.

CI sandboxes may block navigation, so the same local CSS is injected inline.
"""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT/'docs/index.html').read_text(encoding='utf-8')
css = (ROOT/'dist/cyberline.all.css').read_text(encoding='utf-8')
doc_css = (ROOT/'docs/docs.css').read_text(encoding='utf-8')
html = html.replace('<link rel="stylesheet" href="../dist/cyberline.all.css">', f'<style>{css}</style>')
html = html.replace('<link rel="stylesheet" href="docs.css">', f'<style>{doc_css}</style>')
with sync_playwright() as p:
    options = {'headless': True}
    if os.path.exists('/usr/bin/chromium'):
        options['executable_path'] = '/usr/bin/chromium'
        options['args'] = ['--no-sandbox']
    browser = p.chromium.launch(**options)
    for name, width, height in [('desktop', 1365, 900), ('mobile', 390, 844)]:
        page = browser.new_page(viewport={'width': width, 'height': height}, device_scale_factor=1, reduced_motion='reduce')
        page.set_content(html)
        path = ROOT/'previews'/f'{name}.png'
        page.screenshot(path=str(path), full_page=True)
        print(f'WROTE {path} ({path.stat().st_size} bytes)')
        page.close()
    browser.close()
