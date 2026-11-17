/* Optional live browser regression for the catalog-to-playground workflow. */
'use strict';
const assert = require('node:assert/strict');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');

const root = path.resolve(__dirname, '..');
const gallery = pathToFileURL(path.join(root, 'docs/catalog.html')).href;

(async () => {
  const executablePath = process.env.SYNTYR_CHROMIUM_EXECUTABLE;
  const browser = await chromium.launch({headless: true, ...(executablePath ? {executablePath} : {})});
  try {
    for (const width of [390, 1280]) {
      const page = await browser.newPage({viewport: {width, height: 850}});
      const errors = [];
      page.on('pageerror', error => errors.push(String(error)));
      await page.goto(gallery, {waitUntil: 'load'});
      const editLinks = page.locator('.catalog-edit');
      const cards = await page.locator('.catalog-card').count();
      assert.ok(cards >= 8);
      assert.equal(await editLinks.count(), cards);
      await editLinks.first().click();
      assert.ok(page.url().includes('#component=catalog-buttons-title'));
      const frame = page.frameLocator('#playground-preview');
      await frame.locator('.syn-button--primary').first().waitFor();
      assert.equal(await page.locator('#playground-example').inputValue(), 'catalog-buttons-title');
      assert.equal(await page.locator('#playground-reference-module').innerText(), 'syntyr.core.css');
      assert.ok((await page.locator('#playground-markup').inputValue()).includes('syn-button--primary'));

      await page.locator('#playground-search').fill('breadcrumb');
      assert.ok((await page.locator('#playground-search-status').innerText()).includes('1 of'));
      await page.locator('#playground-example').selectOption('catalog-breadcrumbs-title');
      await frame.locator('.syn-breadcrumbs').first().waitFor();
      assert.ok((await page.locator('#playground-reference-description').innerText()).length > 5);

      await page.locator('#playground-example').selectOption('actions');
      await frame.locator('.syn-panel').first().waitFor();
      await page.locator('#playground-panel-radius').evaluate(el => {
        el.value = '22';
        el.dispatchEvent(new Event('input', {bubbles: true}));
      });
      await page.waitForFunction(() => {
        const frame = document.querySelector('#playground-preview');
        const panel = frame?.contentDocument?.querySelector('.syn-panel');
        return panel && getComputedStyle(panel).borderTopLeftRadius === '22px';
      });
      assert.equal(await page.locator('#playground-panel-radius-value').innerText(), '22px');
      await page.locator('#playground-viewport').selectOption('390');
      assert.ok(await page.locator('#playground-preview').evaluate(el => el.getBoundingClientRect().width <= 391));
      await page.locator('#playground-theme').selectOption('grid');
      await frame.locator('body[data-syn-theme="grid"]').waitFor();

      await page.locator('#playground-markup').fill(
        '<p id="sandbox-check">Safe</p><script>parent.document.body.dataset.injected="yes"</script>'
      );
      await frame.locator('#sandbox-check').waitFor();
      assert.equal(await page.locator('body').getAttribute('data-injected'), null);
      assert.equal(errors.length, 0, errors.join('\n'));
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
      assert.equal(overflow, false, `Horizontal overflow at ${width}px`);
      console.log(`PASS chromium ${width}px gallery link / search / tokens / width / sandbox`);
      await page.close();
    }
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
