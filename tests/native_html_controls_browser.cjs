/* Developer-only native HTML/browser regression: NODE_PATH points to local Playwright. */
'use strict';
const assert = require('node:assert/strict');
const path = require('node:path');
const { chromium, firefox, webkit } = require('playwright');
const base = path.resolve(__dirname, '../examples/native-elements.html');
const engine = process.env.SYNTYR_BROWSER || 'chromium';
const executables = {
  chromium: process.env.SYNTYR_CHROMIUM_EXECUTABLE,
  firefox: process.env.SYNTYR_FIREFOX_EXECUTABLE,
  webkit: process.env.SYNTYR_WEBKIT_EXECUTABLE,
};
if (!(engine in executables)) throw new Error('Unsupported browser: ' + engine);
(async () => {
  const browser = await {chromium, firefox, webkit}[engine].launch({
    headless: true, ...(executables[engine] ? {executablePath: executables[engine]} : {}),
  });
  try {
    for (const width of [320, 390, 768]) {
      const page = await browser.newPage({ viewport: {width, height: 800}, reducedMotion: 'reduce' });
      await page.goto('file://' + base);
      assert.equal(await page.locator('script').count(), 0, 'No runtime JS');
      for (const fontSize of ['100%', '200%', '400%']) {
        await page.evaluate(s => document.documentElement.style.fontSize = s, fontSize);
        const metric = await page.evaluate(() => ({
          page: document.documentElement.scrollWidth,
          viewport: document.documentElement.clientWidth,
          file: document.querySelector('#design-file').getBoundingClientRect().right,
        }));
        assert.ok(metric.page <= metric.viewport + 1,
          `${engine}: horizontal overflow at width=${width}, root font=${fontSize}: ${JSON.stringify(metric)}`);
      }
      await page.evaluate(() => document.documentElement.style.fontSize = '');
      const suggestions = page.locator('#native-location');
      assert.equal(await suggestions.getAttribute('list'), 'native-location-list');
      assert.equal(await page.locator('#native-location-list option').count(), 3);
      await suggestions.fill('Central district');
      assert.equal(await suggestions.inputValue(), 'Central district');
      const details = page.locator('details[name="native-review-sections"]');
      assert.equal(await details.count(), 2);
      await details.nth(0).locator('summary').focus();
      await page.keyboard.press('Enter');
      assert.equal(await details.nth(0).getAttribute('open'), '');
      await details.nth(1).locator('summary').focus();
      await page.keyboard.press('Enter');
      assert.equal(await details.nth(1).getAttribute('open'), '');
      // Exclusive-open details[name] is progressive: older engines may leave both open.
      assert.equal(await page.locator('button[commandfor="sample-dialog"]').count(), 1);
      await page.close();
    }
    console.log(engine + ': native HTML input, keyboard, disclosure, 320/390/768 reflow PASS');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
