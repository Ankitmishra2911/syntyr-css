/* Docs-only progressive enhancement; Syntyr CSS ships with zero runtime JavaScript. */
(() => {
  "use strict";
  const examples = {
    metrics: `<section class="syn-region">
  <h2 class="syn-heading">System telemetry</h2>
  <div class="syn-stats">
    <article class="syn-stat"><span class="syn-stat-label">USERS</span><p class="syn-stat-value">2,840</p></article>
    <article class="syn-stat"><span class="syn-stat-label">UPTIME</span><p class="syn-stat-value">99.9%</p></article>
    <article class="syn-stat"><span class="syn-stat-label">ALERTS</span><p class="syn-stat-value">02</p></article>
  </div>
</section>`,
    actions: `<section class="syn-panel" style="--syn-panel-radius: .75rem; --syn-panel-padding: 1.5rem">
  <h2 class="syn-heading">Deployment ready</h2>
  <p class="syn-muted">Scoped tokens customize this panel without a new component class.</p>
  <div class="syn-inline syn-u-wrap">
    <button class="syn-button syn-button--primary">Deploy</button>
    <button class="syn-button syn-button--outline">Preview</button>
    <button class="syn-button syn-button--ghost">Cancel</button>
  </div>
</section>`,
    form: `<form class="syn-panel syn-form" action="#" method="get">
  <h2 class="syn-heading">Create workspace</h2>
  <label class="syn-label" for="workspace-name">WORKSPACE NAME</label>
  <input id="workspace-name" class="syn-input syn-u-w-full" name="workspace" required placeholder="Example Studio">
  <label class="syn-check"><input type="checkbox" required> I accept the terms</label>
  <button class="syn-button syn-button--primary" type="submit">Create</button>
  <p class="syn-muted">Preview only; forms cannot submit in this frame.</p>
</form>`,
    cards: `<section class="syn-grid">
  <article class="syn-panel" style="--syn-panel-padding: 1.5rem; --syn-panel-radius: .65rem">
    <span class="syn-badge">ANALYTICS</span>
    <h2 class="syn-heading">Discover patterns</h2>
    <p class="syn-muted">Readable content and restrained color.</p>
    <a class="syn-button syn-button--primary" href="#details">Explore</a>
  </article>
  <article class="syn-panel" style="--syn-panel-padding: 1.5rem; --syn-panel-radius: .65rem">
    <span class="syn-badge">WORKFLOWS</span>
    <h2 class="syn-heading">Move faster</h2>
    <p class="syn-muted">Reusable visual language in ordinary HTML.</p>
    <a class="syn-button" href="#details">Learn more</a>
  </article>
</section>`
  };
  const example = document.getElementById("playground-example");
  const theme = document.getElementById("playground-theme");
  const markup = document.getElementById("playground-markup");
  const preview = document.getElementById("playground-preview");
  const status = document.getElementById("playground-status");
  const renderButton = document.getElementById("playground-render");
  const copyButton = document.getElementById("playground-copy");
  let framePending = false;

  function render() {
    // No script or form permissions, even if an editor pastes arbitrary markup.
    // allow-same-origin permits Syntyr's *local* stylesheet to load; it does
    // not permit script execution without allow-scripts.
    const shell = `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self' 'unsafe-inline'; img-src data:; base-uri 'none'; form-action 'none'">
<link rel="stylesheet" href="../dist/syntyr.all.css">
<style>html,body{min-height:100%;} body.syn-root{margin:0;padding:1.5rem;} *,*::before,*::after{box-sizing:border-box;}</style>
</head><body class="syn-root syn-page" data-syn-theme="${theme.value}">${markup.value}</body></html>`;
    preview.srcdoc = shell;
    status.textContent = `Preview updated: ${theme.options[theme.selectedIndex].text} theme.`;
  }

  function scheduleRender() {
    if (framePending) return;
    framePending = true;
    requestAnimationFrame(() => { framePending = false; render(); });
  }

  function loadExample() {
    markup.value = examples[example.value] || examples.metrics;
    scheduleRender();
  }

  example.addEventListener("change", loadExample);
  theme.addEventListener("change", scheduleRender);
  markup.addEventListener("input", scheduleRender);
  renderButton.addEventListener("click", render);
  copyButton.addEventListener("click", async () => {
    try {
      if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText(markup.value);
      status.textContent = "HTML copied.";
    } catch (_error) {
      markup.focus();
      markup.select();
      status.textContent = "HTML selected. Copy it with your keyboard.";
    }
  });
  loadExample();
})();
