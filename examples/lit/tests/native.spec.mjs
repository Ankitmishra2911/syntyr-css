import { test, expect } from "@playwright/test";

const nativePage = "/examples/web-components/index.html";
const serverPage = "/examples/web-components/ssr.html";

test.describe("native Custom Elements without JavaScript", () => {
  test.use({ javaScriptEnabled: false });

  test("retains readable light-DOM fallback without upgrade", async ({ page }) => {
    await page.goto(nativePage);
    await expect(page.locator("syn-demo-native-status [data-native-fallback]")).toBeVisible();
    await expect(page.locator("syn-demo-native-status [data-native-fallback]")).toContainText("Relay: online");
  });

  test("renders Declarative Shadow DOM server content without JavaScript", async ({ page }) => {
    await page.goto(serverPage);
    const element = page.locator("syn-demo-native-status");
    await expect(element.locator('[part="status"]')).toHaveText("Online");
    await expect(element.locator('[part="status"]')).toBeVisible();
    expect(await element.evaluate(host => Boolean(host.shadowRoot))).toBe(true);
  });
});

test("framework-free Custom Element upgrades and exposes native events", async ({ page }) => {
  await page.goto(nativePage);
  const element = page.locator("#native-status");
  const toggle = element.locator('[part="toggle"]');
  await expect(element.locator('[part="status"]')).toHaveText("Online");
  await expect(toggle).toHaveAttribute("aria-pressed", "true");
  await toggle.focus();
  await page.keyboard.press("Space");
  await expect(element.locator('[part="status"]')).toHaveText("Offline");
  await expect(toggle).toHaveAttribute("aria-pressed", "false");
  await expect(page.locator("#native-event-output")).toHaveText("Relay: offline");
  expect(await element.evaluate(host => host.shadowRoot?.querySelector('[part="panel"]') !== null)).toBe(true);
});

test("native Custom Element reflects external attributes and provides accessible busy state", async ({ page }) => {
  await page.goto(nativePage);
  const element = page.locator("#native-status");
  const panel = element.locator('[part="panel"]');
  const button = element.locator('[part="toggle"]');

  await element.evaluate(host => { host.setAttribute("service", "<img src=x onerror=alert(1)>"); host.busy = true; });
  await expect(element.locator('[part="title"]')).toHaveText("<img src=x onerror=alert(1)>");
  await expect(panel).toHaveAttribute("aria-busy", "true");
  await expect(button).toBeDisabled();
  await expect(element.locator('[part="status"]')).toHaveText("Updating status…");
  await element.evaluate(host => { host.busy = false; host.online = false; });
  await expect(button).toBeEnabled();
  await expect(element.locator('[part="status"]')).toHaveText("Offline");
  await expect(button).toHaveAttribute("aria-pressed", "false");
});

test("native Custom Element survives disconnect/reconnect without duplicate handlers", async ({ page }) => {
  await page.goto(nativePage);
  const element = page.locator("#native-status");
  await element.evaluate(host => {
    let count = 0;
    document.addEventListener("syn-demo-native-status-change", () => { count += 1; });
    window.__nativeEventCount = () => count;
    host.remove();
    document.querySelector("#native-container").append(host);
  });
  await element.locator('[part="toggle"]').click();
  await expect(element.locator('[part="status"]')).toHaveText("Offline");
  expect(await page.evaluate(() => window.__nativeEventCount())).toBe(1);
});

test("native Shadow DOM tokens update when nested Syntyr theme changes", async ({ page }) => {
  await page.goto(nativePage);
  const panel = page.locator("#native-status").locator('[part="panel"]');
  await expect(panel).toHaveCSS("border-top-style", "dashed");
  const before = await panel.evaluate(node => getComputedStyle(node).backgroundColor);
  await page.locator("#native-container").evaluate(node => { node.dataset.synTheme = "grid"; });
  await expect.poll(() => panel.evaluate(node => getComputedStyle(node).backgroundColor)).not.toBe(before);
});

test("Declarative Shadow DOM is reused on upgrade, not recreated", async ({ page }) => {
  await page.goto(serverPage);
  const element = page.locator("syn-demo-native-status");
  await expect(element.locator('[part="panel"]')).toHaveAttribute("data-server-rendered", "true");
  await element.locator('[part="toggle"]').click();
  await expect(element.locator('[part="status"]')).toHaveText("Offline");
  await expect(element.locator('[part="panel"]')).toHaveAttribute("data-server-rendered", "true");
});

test("native Custom Element retains keyboard focus and controls at narrow width and forced colors", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 640 });
  await page.emulateMedia({ forcedColors: "active" });
  await page.goto(nativePage);
  const button = page.locator("#native-status").locator('[part="toggle"]');
  await expect(button).toBeVisible();
  await button.focus();
  await expect(button).toHaveCSS("outline-style", "solid");
  await page.keyboard.press("Enter");
  await expect(page.locator("#native-status").locator('[part="status"]')).toHaveText("Offline");
});
