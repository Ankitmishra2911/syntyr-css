# MIT-licensed composition recipes

These original Syntyr recipes are free to copy, edit, commercialize, and distribute under MIT. No Tailwind Plus source or premium assets were copied. For live examples see [the gallery](index.html), the [Grid console](../examples/console.html), and the [Noir pricing layout](../examples/pricing.html).

## 1. Responsive telemetry cards

The `.syn-region` element establishes a **named inline-size container**. Unlike media queries, the cards respond to the width of the enclosing widget/sidebar. This is a native browser feature; no JavaScript observer is needed.

```html
<section class="syn-root syn-region" data-syn-theme="grid" aria-label="Network telemetry">
  <div class="syn-stats">
    <article class="syn-stat"><span class="syn-stat-label">UPTIME</span><p class="syn-stat-value">99.8%</p></article>
    <article class="syn-stat"><span class="syn-stat-label">NODES</span><p class="syn-stat-value">24</p></article>
    <article class="syn-stat"><span class="syn-stat-label">ALERTS</span><p class="syn-stat-value">02</p></article>
  </div>
</section>
```

## 2. Accessible empty state

```html
<section class="syn-empty" aria-labelledby="empty-heading">
  <p class="syn-eyebrow">QUEUE / EMPTY</p>
  <h2 id="empty-heading">No pending actions</h2>
  <p class="syn-muted">New items appear here once submitted.</p>
  <a class="syn-button syn-button--primary" href="/new">Create an item</a>
</section>
```

This is a *visual composition*, not a live queue implementation. Preserve real links, meaningful labels, and server-side behavior.

## 3. Three-card pricing display

```html
<section class="syn-root syn-region" data-syn-theme="noir" aria-label="Illustrative plans">
  <div class="syn-pricing">
    <article class="syn-price-card">
      <h2>Personal</h2>
      <p class="syn-price-value">$19<small> / month</small></p>
      <ul class="syn-feature-list"><li>One project</li><li>Basic support</li></ul>
      <a class="syn-button" href="/contact">Contact us</a>
    </article>
    <article class="syn-price-card" data-syn-featured>
      <h2>Studio</h2>
      <p class="syn-price-value">$49<small> / month</small></p>
      <ul class="syn-feature-list"><li>Unlimited projects</li><li>Team seats</li></ul>
      <a class="syn-button syn-button--primary" href="/contact">Contact us</a>
    </article>
    <article class="syn-price-card">
      <h2>Enterprise</h2>
      <p class="syn-price-value">Custom</p>
      <ul class="syn-feature-list"><li>Security review</li><li>Dedicated support</li></ul>
      <a class="syn-button" href="/contact">Contact us</a>
    </article>
  </div>
</section>
```

## 4. Stateful native button (host controlled)

```html
<button type="button" class="syn-button" aria-pressed="true">Grid view</button>
<button type="button" class="syn-button" aria-busy="true">Syncing status</button>
```

`aria-pressed="true"` conveys a real toggle state to accessibility APIs; set it only when a toggle actually is pressed. `aria-busy` signals that updates are in progress; it **does not** disable a button or create loading logic. The UI state must come from your application/server. If a state is only decorative, use `data-syn-state="active"` instead of misusing ARIA.

## Token-only custom theme

```css
/* Unlayered application CSS intentionally overrides Syntyr's layered tokens. */
.syn-root[data-syn-theme="custom"] {
  --syn-bg: #0b1019;
  --syn-surface: #192333;
  --syn-accent: #82f9d1;
  --syn-on-accent: #09120e;
  --syn-text: #eefbf7;
  --syn-muted: #bbd4ce;
  --syn-frame: #496b68;
}
```

For custom themes, test *every* textual token pairing and important state for WCAG contrast. The example overrides only a subset of the available color tokens and is not an accessibility certification.

## Reusing recipes across stacks

- **Go / templ, PHP, Django, Rust templates:** Make recipes server-rendered partials and pass content as arguments.
- **HTMX / Datastar:** Use the same classes on server-returned fragments. Their JavaScript, if chosen, is outside the CSS library.
- **React / Vue / Astro:** Wrap the exact markup in framework components only when the host application calls for it.

Favor stable component classes and CSS variables over copying long lists of generated utilities. See [contract](components.md) and [Tailwind research](tailwind-research.md).

## Accessible navigation and loading placeholders

Breadcrumbs use a real ordered list inside a labeled navigation landmark. The separator is a CSS border rather than spoken punctuation:

```html
<nav class="syn-breadcrumbs" aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><span aria-current="page">Reports</span></li>
  </ol>
</nav>
```

Page controls are **real links**, not inert buttons. Match the selected page to the actual URL, and label any symbol-only links:

```html
<nav class="syn-pagination" aria-label="Results pages">
  <a class="syn-page-link" href="?page=1">1</a>
  <a class="syn-page-link" href="?page=2" aria-current="page">2</a>
  <a class="syn-page-link" href="?page=3">3</a>
</nav>
```

Skeletons are deliberately static. Hide the visual placeholder from assistive technology and announce loading outside it with application-owned state. Do not leave an infinite loading message or use fake progress values:

```html
<section aria-busy="true" aria-label="Reports">
  <p role="status">Loading reports…</p>
  <span class="syn-skeleton" aria-hidden="true"></span>
  <span class="syn-skeleton syn-skeleton--short" aria-hidden="true"></span>
</section>
```

When loading finishes, the application replaces the placeholders with content and clears `aria-busy`. The CSS library does not implement fetching or state changes.

## Server-rendered SaaS filter and settings patterns

The [SaaS workflow demonstration](../examples/saas-workflows.html) shows how to combine standard HTML search forms, a table, navigation landmarks, native settings disclosures and no-JavaScript placeholders. The page's data is illustrative and **is not filtered**; the following behavior belongs to the host application:

- Parse and validate `query`, `status`, `owner` and `page` on the server, apply authorization before filtering, paginate the results, and escape all rendered user input.
- Preserve submitted form values and `aria-current` based on the actual result page, and emit a truthful result count plus empty-state or error message.
- Persist preferences in the server's settings endpoint, with CSRF protection for changes; the static demo intentionally has no save button.
- When using HTMX, Datastar or another enhancement layer, keep GET filters, ordinary links and form labels working without client-side JavaScript.

The scoped `examples/saas-workflows.css` stylesheet contains layout glue only and is **not** added to the distributed core or all-in-one bundle.


## Intrinsic responsive layouts (optional recipes CSS)

Load `syntyr.core.css` plus `syntyr.recipes.css`. The layout primitives are
scoped to `.syn-root` and require no JavaScript, framework or viewport media
queries. Their children are ordinary semantic HTML.

```html
<section class="syn-root">
  <div class="syn-sidebar" style="--syn-sidebar-width: 14rem">
    <aside>Navigation or filters</aside>
    <main>Main content</main>
  </div>
  <div class="syn-switcher" style="--syn-switcher-threshold: 42rem">
    <article>First card</article>
    <article>Second card</article>
    <article>Third card</article>
  </div>
</section>
```

`.syn-sidebar` expects **exactly two** direct children: sidebar first,
content second. Defaults: sidebar 16rem, content minimum 28rem (capped at
100% of available width). In narrow containers they stack, and neither
child is forced wider than the container by the layout primitive. Content
with long unbreakable text should still use appropriate wrapping.

`.syn-switcher` treats all direct children uniformly. Above the 40rem
default threshold they share a row; below it every child stacks. Override
`--syn-switcher-threshold` per instance. This differs from `.syn-grid`,
which can display different numbers of columns at intermediate widths.

Use opt-in fluid type classes `.syn-fluid-display`, `.syn-fluid-lede` and
`.syn-reading`. The CSS custom properties `--syn-fluid-display-size`,
`--syn-type-lede` and `--syn-reading-width` can be overridden in plain
application CSS. Keep real document headings and reading order.

See [the working minimalist demo](../examples/minimalist-patterns.html).
