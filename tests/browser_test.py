"""Opt-in Playwright browser smoke and interaction tests against real Chromium.

Run: python3 tests/browser_test.py
Browser infrastructure is developer-only, never a Cyberline runtime dependency.
"""
from pathlib import Path
import os
import shutil
import unittest

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
# Inlining local CSS avoids network/file:// navigation blocked by some hardened CI browsers.

class BrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = sync_playwright().start()
        kwargs = dict(headless=True)
        executable = (os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE')
                      or shutil.which('chromium')
                      or shutil.which('chromium-browser'))
        if executable:
            kwargs['executable_path'] = executable
            kwargs['args'] = ['--no-sandbox']
        cls.browser = cls.p.chromium.launch(**kwargs)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.p.stop()

    def setUp(self):
        self.context = self.browser.new_context(viewport={'width': 1280, 'height': 900}, device_scale_factor=1)
        self.page = self.context.new_page()
        self.errors = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        html = (ROOT / 'docs/index.html').read_text(encoding='utf-8')
        css = (ROOT / 'dist/cyberline.all.css').read_text(encoding='utf-8')
        docs_css = (ROOT / 'docs/docs.css').read_text(encoding='utf-8')
        html = html.replace('<link rel="stylesheet" href="../dist/cyberline.all.css">', f'<style>{css}</style>')
        html = html.replace('<link rel="stylesheet" href="docs.css">', f'<style>{docs_css}</style>')
        self.page.set_content(html, wait_until='load')

    def tearDown(self):
        self.assertFalse(self.errors, self.errors)
        self.context.close()

    def test_theme_tokens_are_applied_and_nested(self):
        root = self.page.locator('body')
        grid = self.page.locator('#themes [data-cy-theme="grid"]')
        noir = self.page.locator('#themes [data-cy-theme="noir"]')
        self.assertEqual(root.evaluate("e => getComputedStyle(e).getPropertyValue('--cy-accent').trim()"), '#76e7f7')
        self.assertEqual(grid.evaluate("e => getComputedStyle(e).getPropertyValue('--cy-accent').trim()"), '#76e7f7')
        self.assertEqual(noir.evaluate("e => getComputedStyle(e).getPropertyValue('--cy-accent').trim()"), '#f1b574')
        self.assertEqual(grid.locator('.cy-panel').count(), 0) # this panel *is* the theme root

    def test_semantic_mode_is_scoped_and_styled(self):
        semantic_button = self.page.locator('#semantic .cy-semantic button')
        self.assertEqual(semantic_button.count(), 1)
        self.assertEqual(semantic_button.evaluate('e => getComputedStyle(e).minHeight'), '44px')
        semantic_article = self.page.locator('#semantic .cy-semantic article')
        self.assertEqual(semantic_article.evaluate('e => getComputedStyle(e).backgroundColor'), 'rgb(17, 31, 44)')
        self.page.evaluate("""() => {
          const b = document.createElement('button');
          b.id = 'unstyled-external';
          b.textContent = 'Outside';
          document.body.appendChild(b);
        }""")
        external = self.page.locator('#unstyled-external')
        self.assertNotEqual(external.evaluate('e => getComputedStyle(e).minHeight'), '44px')

    def test_semantic_mode_leaves_range_input_native(self):
        self.page.evaluate("""() => {
          const range = document.createElement('input');
          range.id = 'range-audit';
          range.type = 'range';
          document.querySelector('.cy-semantic article').appendChild(range);
        }""")
        range_border = self.page.locator('#range-audit').evaluate('e => getComputedStyle(e).borderTopWidth')
        self.assertEqual(range_border, '0px')

    def test_embedded_root_does_not_force_viewport_height(self):
        self.page.evaluate("""() => {
          const section = document.createElement('section');
          section.id = 'embedded-root';
          section.className = 'cy-root';
          section.innerHTML = '<span>Small widget</span>';
          document.body.appendChild(section);
        }""")
        min_height = self.page.locator('#embedded-root').evaluate('e => getComputedStyle(e).minHeight')
        self.assertNotEqual(min_height, '900px')

    def test_popover_opens_and_escape_dismisses(self):
        popover = self.page.locator('#command-popover')
        self.assertFalse(popover.evaluate('e => e.matches(":popover-open")'))
        self.page.get_by_role('button', name='OPEN COMMAND').click()
        self.assertTrue(popover.evaluate('e => e.matches(":popover-open")'))
        self.page.keyboard.press('Escape')
        self.assertFalse(popover.evaluate('e => e.matches(":popover-open")'))

    def test_invoker_dialog_opens_and_closes(self):
        dialog = self.page.locator('#diagnostic-dialog')
        self.page.get_by_role('button', name='OPEN DIALOG').click()
        self.assertTrue(dialog.evaluate('e => e.open'))
        self.assertTrue(dialog.evaluate('e => e.matches(":modal")'))
        self.page.get_by_role('button', name='ACKNOWLEDGE').click()
        self.assertFalse(dialog.evaluate('e => e.open'))

    def test_disclosure_and_keyboard_focus(self):
        disclosure = self.page.locator('#components details').first
        self.assertFalse(disclosure.evaluate('e => e.open'))
        disclosure.locator('summary').click()
        self.assertTrue(disclosure.evaluate('e => e.open'))
        self.page.keyboard.press('Tab')
        # Focus styles should never be set to none by the framework.
        focus_color = self.page.locator(':focus').evaluate('e => getComputedStyle(e).outlineStyle')
        self.assertNotEqual(focus_color, 'none')

    def test_mobile_has_no_document_horizontal_overflow(self):
        self.page.set_viewport_size({'width': 375, 'height': 812})
        values = self.page.evaluate('() => ({sw:document.documentElement.scrollWidth, cw:document.documentElement.clientWidth})')
        self.assertLessEqual(values['sw'], values['cw'] + 1, values)

    def test_reduced_motion_disables_transitions(self):
        self.page.emulate_media(reduced_motion='reduce')
        duration = self.page.locator('.cy-button--primary').first.evaluate('e => getComputedStyle(e).transitionDuration')
        self.assertIn(duration, ('0s', '0s, 0s, 0s'), duration)

    def test_container_query_cards_adapt_to_parent_not_viewport(self):
        region = self.page.locator('#recipes .cy-region').first
        stats = region.locator('.cy-stats')
        def columns():
            return len(stats.evaluate('e => getComputedStyle(e).gridTemplateColumns').split())
        region.evaluate('e => e.style.width = "380px"')
        self.assertEqual(columns(), 1)
        region.evaluate('e => e.style.width = "550px"')
        self.assertEqual(columns(), 2)
        region.evaluate('e => e.style.width = "950px"')
        self.assertEqual(columns(), 3)

    def test_attribute_variants_preserve_semantics(self):
        self.page.emulate_media(reduced_motion='reduce')
        self.page.evaluate("""() => {
          const button = document.createElement('button');
          button.id = 'v03-state';
          button.className = 'cy-button';
          button.textContent = 'Toggle';
          document.querySelector('#recipes').appendChild(button);
        }""")
        b = self.page.locator('#v03-state')
        base = b.evaluate('e => getComputedStyle(e).color')
        b.evaluate('e => e.setAttribute("aria-pressed", "true")')
        pressed = b.evaluate('e => getComputedStyle(e).color')
        self.assertNotEqual(base, pressed)
        self.assertEqual(b.get_attribute('aria-pressed'), 'true')
        b.evaluate('e => e.setAttribute("aria-busy", "true")')
        self.assertEqual(b.evaluate('e => getComputedStyle(e).cursor'), 'progress')

    def test_unlayered_host_theme_overrides_token(self):
        self.page.add_style_tag(content='.cy-root[data-cy-theme="grid"] { --cy-accent: #99ffcc; }')
        self.assertEqual(self.page.locator('body').evaluate(
            'e => getComputedStyle(e).getPropertyValue("--cy-accent").trim()'), '#99ffcc')

    def test_noir_pricing_example_is_responsive_and_local(self):
        html = (ROOT / 'examples/pricing.html').read_text(encoding='utf-8')
        core = (ROOT / 'dist/cyberline.core.css').read_text(encoding='utf-8')
        effects = (ROOT / 'dist/cyberline.effects.css').read_text(encoding='utf-8')
        html = html.replace('<link rel="stylesheet" href="../dist/cyberline.core.css">', f'<style>{core}</style>')
        html = html.replace('<link rel="stylesheet" href="../dist/cyberline.effects.css">', f'<style>{effects}</style>')
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.page.set_content(html)
        pricing = self.page.locator('.cy-pricing')
        self.assertEqual(len(pricing.evaluate('e => getComputedStyle(e).gridTemplateColumns').split()), 1)
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 391)
        self.page.set_viewport_size({'width': 1280, 'height': 900})
        self.assertEqual(len(pricing.evaluate('e => getComputedStyle(e).gridTemplateColumns').split()), 3)
        self.assertEqual(self.page.locator('.cy-price-card').count(), 3)

    def test_forced_colors_still_has_visible_control_border(self):
        self.page.emulate_media(forced_colors='active')
        color = self.page.get_by_role('button', name='OPEN COMMAND').evaluate('e => getComputedStyle(e).borderTopStyle')
        self.assertEqual(color, 'solid')

if __name__ == '__main__':
    unittest.main(verbosity=2)
