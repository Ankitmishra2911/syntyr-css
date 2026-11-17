/* Optional maintainer-only Playwright test; not part of Syntyr CSS runtime. */
'use strict';
const assert = require('node:assert/strict');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium, firefox, webkit} = require('playwright');
const catalog = pathToFileURL(path.resolve(__dirname, '../docs/catalog.html')).href;
const engines = {chromium, firefox, webkit};

(async () => {
  const names = process.argv.slice(2).length ? process.argv.slice(2) : ['chromium'];
  for (const name of names) {
    if (!engines[name]) throw Error(`Unknown browser ${name}`);
    const custom = {
      chromium: process.env.SYNTYR_CHROMIUM_EXECUTABLE,
      firefox: process.env.SYNTYR_FIREFOX_EXECUTABLE,
      webkit: process.env.SYNTYR_WEBKIT_EXECUTABLE,
    }[name];
    const browser = await engines[name].launch({headless: true, ...(custom ? {executablePath: custom} : {})});
    try {
      for (const width of [390, 1280]) {
        const page = await browser.newPage({viewport: {width, height: 800}});
        await page.goto(catalog, {waitUntil: 'load'});
        await page.waitForFunction(() => document.getElementById('catalog-controls').hidden === false);
        const total = await page.locator('.catalog-card').count();
        assert.ok(total >= 27);
        assert.equal(await page.locator('.catalog-card:not([hidden])').count(), total);
        assert.equal(await page.locator('.catalog-copy:not([hidden])').count(), total);
        await page.locator('#catalog-category').selectOption('media');
        assert.equal(await page.locator('.catalog-card:not([hidden])').count(), 1);
        await page.locator('#catalog-search').fill('image');
        assert.equal(await page.locator('.catalog-card:not([hidden])').count(), 1);
        await page.locator('#catalog-search').fill('buttons');
        assert.equal(await page.locator('.catalog-card:not([hidden])').count(), 0);
        await page.locator('#catalog-category').selectOption('all');
        await page.locator('#catalog-search').fill('');
        await page.locator('#catalog-theme').selectOption('noir');
        assert.equal(await page.locator('body').getAttribute('data-syn-theme'), 'noir');
        await page.locator('#catalog-preview-size').selectOption('compact');
        assert.equal(await page.locator('#catalog-items').getAttribute('data-catalog-preview'), 'compact');
        const previewWidth = await page.locator('.catalog-preview').first().evaluate(el => el.getBoundingClientRect().width);
        assert.ok(previewWidth <= 23 * 16 + 1, 'Compact preview should not exceed 23rem');
        await page.locator('#catalog-search').fill('table');
        assert.equal(await page.locator('.catalog-card:not([hidden])').count(), 1);
        assert.equal(await page.locator('#catalog-results').innerText(), 'Showing 1 of ' + total + ' examples.');
        await page.locator('#catalog-search').fill('no-such-component');
        assert.equal(await page.locator('.catalog-card:not([hidden])').count(), 0);
        assert.equal(await page.locator('#catalog-empty').isVisible(), true);
        await page.locator('#catalog-search').fill('buttons');
        assert.equal(await page.locator('.catalog-card:not([hidden])').count(), 1);
        await page.evaluate(() => {
          Object.defineProperty(navigator, 'clipboard', {
            configurable: true, value: {writeText: async (value) => { window.__catalogCopied = value; }}
          });
        });
        await page.locator('.catalog-card:not([hidden]) [data-catalog-copy]').click();
        const copied = await page.evaluate(() => window.__catalogCopied);
        assert.ok(copied.includes('syn-button--primary'));
        assert.equal(await page.locator('#catalog-results').innerText(), 'Buttons HTML copied.');
        await page.evaluate(() => Object.defineProperty(navigator, 'clipboard', {configurable: true, value: undefined}));
        await page.locator('.catalog-card:not([hidden]) [data-catalog-copy]').click();
        assert.equal(await page.locator('.catalog-card:not([hidden]) .catalog-code-details').evaluate(el => el.open), true);
        assert.ok((await page.evaluate(() => window.getSelection()?.toString() || '')).includes('syn-button--primary'));
        assert.equal(await page.locator('#catalog-results').innerText(), 'HTML selected. Use your keyboard to copy it.');
        const dimensions = await page.evaluate(() => ({scroll: document.documentElement.scrollWidth, inner: window.innerWidth}));
        assert.ok(dimensions.scroll <= dimensions.inner + 1, `Unexpected horizontal overflow at ${width}: ${JSON.stringify(dimensions)}`);
        await page.close();

        const noJs = await browser.newContext({viewport: {width, height: 800}, javaScriptEnabled: false});
        const noJsPage = await noJs.newPage();
        await noJsPage.goto(catalog, {waitUntil: 'load'});
        assert.equal(await noJsPage.locator('.catalog-card:not([hidden])').count(), total);
        assert.equal(await noJsPage.locator('.catalog-source code').count(), total);
        assert.equal(await noJsPage.locator('#catalog-controls').isVisible(), false);
        assert.equal(await noJsPage.locator('[data-catalog-copy]:visible').count(), 0);
        await noJs.close();
        process.stdout.write(`${name} ${width}px: search, clipboard, empty state, reflow and no-JS pass\n`);
      }
    } finally { await browser.close(); }
  }
})().catch((error) => { console.error(error); process.exitCode = 1; });
