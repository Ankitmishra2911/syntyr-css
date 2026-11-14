# MIT-licensed composition recipes

These original Syntyr recipes are free to copy, edit, commercialize, and distribute under MIT. No Tailwind Plus source or premium assets were copied. For live examples see [the gallery](index.html), the [Grid console](../examples/console.html), and the [Noir pricing layout](../examples/pricing.html).

## 1. Responsive telemetry cards

The `.cy-region` element establishes a **named inline-size container**. Unlike media queries, the cards respond to the width of the enclosing widget/sidebar. This is a native browser feature; no JavaScript observer is needed.

```html
<section class="cy-root cy-region" data-cy-theme="grid" aria-label="Network telemetry">
  <div class="cy-stats">
    <article class="cy-stat"><span class="cy-stat-label">UPTIME</span><p class="cy-stat-value">99.8%</p></article>
    <article class="cy-stat"><span class="cy-stat-label">NODES</span><p class="cy-stat-value">24</p></article>
    <article class="cy-stat"><span class="cy-stat-label">ALERTS</span><p class="cy-stat-value">02</p></article>
  </div>
</section>
```

## 2. Accessible empty state

```html
<section class="cy-empty" aria-labelledby="empty-heading">
  <p class="cy-eyebrow">QUEUE / EMPTY</p>
  <h2 id="empty-heading">No pending actions</h2>
  <p class="cy-muted">New items appear here once submitted.</p>
  <a class="cy-button cy-button--primary" href="/new">Create an item</a>
</section>
```

This is a *visual composition*, not a live queue implementation. Preserve real links, meaningful labels, and server-side behavior.

## 3. Three-card pricing display

```html
<section class="cy-root cy-region" data-cy-theme="noir" aria-label="Illustrative plans">
  <div class="cy-pricing">
    <article class="cy-price-card">
      <h2>Personal</h2>
      <p class="cy-price-value">$19<small> / month</small></p>
      <ul class="cy-feature-list"><li>One project</li><li>Basic support</li></ul>
      <a class="cy-button" href="/contact">Contact us</a>
    </article>
    <article class="cy-price-card" data-cy-featured>
      <h2>Studio</h2>
      <p class="cy-price-value">$49<small> / month</small></p>
      <ul class="cy-feature-list"><li>Unlimited projects</li><li>Team seats</li></ul>
      <a class="cy-button cy-button--primary" href="/contact">Contact us</a>
    </article>
    <article class="cy-price-card">
      <h2>Enterprise</h2>
      <p class="cy-price-value">Custom</p>
      <ul class="cy-feature-list"><li>Security review</li><li>Dedicated support</li></ul>
      <a class="cy-button" href="/contact">Contact us</a>
    </article>
  </div>
</section>
```

## 4. Stateful native button (host controlled)

```html
<button type="button" class="cy-button" aria-pressed="true">Grid view</button>
<button type="button" class="cy-button" aria-busy="true">Syncing status</button>
```

`aria-pressed="true"` conveys a real toggle state to accessibility APIs; set it only when a toggle actually is pressed. `aria-busy` signals that updates are in progress; it **does not** disable a button or create loading logic. The UI state must come from your application/server. If a state is only decorative, use `data-cy-state="active"` instead of misusing ARIA.

## Token-only custom theme

```css
/* Unlayered application CSS intentionally overrides Syntyr's layered tokens. */
.cy-root[data-cy-theme="custom"] {
  --cy-bg: #0b1019;
  --cy-surface: #192333;
  --cy-accent: #82f9d1;
  --cy-on-accent: #09120e;
  --cy-text: #eefbf7;
  --cy-muted: #bbd4ce;
  --cy-frame: #496b68;
}
```

For custom themes, test *every* textual token pairing and important state for WCAG contrast. The example overrides only a subset of the available color tokens and is not an accessibility certification.

## Reusing recipes across stacks

- **Go / templ, PHP, Django, Rust templates:** Make recipes server-rendered partials and pass content as arguments.
- **HTMX / Datastar:** Use the same classes on server-returned fragments. Their JavaScript, if chosen, is outside the CSS library.
- **React / Vue / Astro:** Wrap the exact markup in framework components only when the host application calls for it.

Favor stable component classes and CSS variables over copying long lists of generated utilities. See [contract](components.md) and [Tailwind research](tailwind-research.md).
