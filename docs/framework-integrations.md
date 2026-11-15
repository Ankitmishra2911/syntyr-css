# Syntyr CSS integration guide: HTMX and common frontend stacks

Syntyr is a **CSS presentation layer**, not a state manager, request client, or component runtime.
It has no JavaScript initialization, no required build tool, and no runtime dependency.
Every example uses the same `syn-` classes, CSS tokens and standard HTML.

## Choose one styling mode

1. **Explicit classes (recommended for apps):** load `syntyr.core.css`, use
   `.syn-root` on a stable ancestor, then `.syn-button`, `.syn-panel`, `.syn-input`, etc.
2. **Optional semantic HTML:** additionally load `syntyr.semantic.css` after core and
   add `.syn-semantic` to a scoped ancestor. Unclassed HTML receives semantic styles.
   For an element that an interaction framework will add classes to, opt it in once
   with `data-syn-semantic`. This preserves semantic styling while host-managed
   classes such as `htmx-request` are added and removed.

```html
<section class="syn-root syn-semantic" data-syn-theme="studio">
  <button data-syn-semantic hx-get="/status" hx-target="#status">Check status</button>
  <div id="status" aria-live="polite"></div>
</section>
```

**Host isolation:** Loading the CSS alone does not style a `.syn-button`,
`.syn-panel`, or other Syntyr class outside `.syn-root`. Existing host UI
components and CSS retain their presentation. Put `.syn-root` on the actual
Syntyr subtree (or on the component itself); do not assume a globally
scoped component class creates its own theme root. Syntyr uses native CSS
nesting for this boundary, so test embedding in each target browser.

The marker is only considered **inside** `.syn-semantic`, so it does not style
elements elsewhere. Do not put it on elements styled by a separate component
library unless you explicitly want Syntyr semantic styling there. Prefer
`.syn-button` for already-classed controls. The marker does **not** make the
control stateful, disabled, or accessible by itself.

## HTMX: progressive enhancement

A complete example with a real stdlib Python HTTP server is at:
[examples/htmx.html](https://github.com/dporkka/syntyr-css/blob/main/examples/htmx.html),
[examples/htmx_server.py](https://github.com/dporkka/syntyr-css/blob/main/examples/htmx_server.py), and
[examples/htmx.css](https://github.com/dporkka/syntyr-css/blob/main/examples/htmx.css).
These links lead to source files, not a live Cloudflare demonstration.

From the repository root:

```sh
python3 examples/htmx_server.py
# open http://127.0.0.1:8765/examples/htmx.html
```

The optional demo loads **pinned HTMX 2.0.8** from a third-party CDN. The CSS
library doesn't load HTMX automatically. Production applications should
self-host the pinned HTMX asset for control over performance, integrity, and CSP.

The search form uses a real `action` and `method=get`. When HTMX sends
`HX-Request: true`, the server returns only the result fragment. Ordinary
navigation gets a complete HTML document. The server emits `Vary: HX-Request`
to keep caches from mixing the representations, and escapes user-controlled
query text before inserting it in HTML.

For best results:

- Put `.syn-root` and `data-syn-theme` **outside** the swapped element.
- Swap the narrowest stable target (normally `innerHTML` inside a results container).
- Give labels and inputs stable IDs; preserve native form submission as a fallback.
- Use the framework's `hx-indicator` and `hx-disabled-elt` when appropriate;
  `aria-busy` does **not** block duplicate submissions by itself.
- Do not create a permanent Syntyr HTMX runtime or register Syntyr lifecycle events.
- For strict CSP, use `includeIndicatorStyles: false` and an external stylesheet.
  The demo shows this pattern with a small **application-owned** `htmx.css`.
- Test initial document, request state, swapped fragment, form fallback, and
  failure paths in an actual browser.

The demo server intentionally exposes only four static assets and one GET route,
listens on localhost, and is **not** included in the Cloudflare static-site build.
A static host cannot serve its dynamic search endpoint without a backend.

## Alpine.js

Use native attributes for real state, and Syntyr classes for presentation:

```html
<div class="syn-root" x-data="{ selected: false }">
  <button class="syn-button" type="button"
          :aria-pressed="String(selected)" @click="selected = !selected">
    Toggle details
  </button>
</div>
```

Mount Alpine once in the host app. For `x-cloak`, define a tiny application
rule `[x-cloak] { display: none !important; }` before Alpine initializes.
Syntyr doesn't manage Alpine state.

## Datastar

Bind standard `aria-*`, `data-syn-state`, and class attributes to Datastar
signals. Style the resulting HTML as ordinary DOM. Keep the Syntyr theme root
outside morph targets, and let Datastar own request and signal behavior.
No Syntyr Datastar plugin is needed.

## React / Next.js

```jsx
import "./syntyr.core.css";

export function StatusCard({ status }) {
  return (
    <section className="syn-root" data-syn-theme="studio">
      <article className="syn-panel">
        <h2 className="syn-heading">Operations</h2>
        <p>{status}</p>
      </article>
    </section>
  );
}
```

Import CSS once from the app entry point (or root layout, as supported by
the framework). No Syntyr provider, hooks, hydration, or dependency on React.

## Vue / Nuxt and Svelte / SvelteKit

Import the same CSS once. Bind native classes, `aria-*`, and
`data-syn-state` using each framework's built-in template syntax.
Do not wrap simple visual classes in additional runtime components unless the
application benefits from reusable semantic component boundaries.

## Astro, Hugo, Zola, Django, Rails, Go/templ and Rust templates

Serve `syntyr.core.css` as a normal static asset. Write HTML partials
with real headings, forms and links. Optional interactive islands can use
HTMX, Alpine, Datastar, React or native browser elements without changing
Syntyr's HTML/CSS contract. In Rails, Hotwire/Turbo updates have the same
theme-root and swap-boundary considerations as HTMX.

## Existing Tailwind or component-library applications

- Syntyr's `.syn-root` scope and `@layer syn.*` layers limit unintended
  interference, but Tailwind Preflight can still change global element defaults.
- Prefer explicit Syntyr classes. Apply `.syn-semantic` only to designated
  regions, not to a whole React/Headless UI component tree.
- Override public `--syn-*` tokens in application CSS; avoid copying or
  rebuilding utility frameworks inside Syntyr.
- Test cascade ordering, focus rings, dark/light color schemes, zoom and
  third-party components after integration.

## Performance and compatibility contract

- CSS bytes are tracked by `python3 scripts/asset_report.py` with optional JSON baseline comparisons; no arbitrary gzip release gate.
- Syntyr runtime JS: **zero**. HTMX/Alpine/React are host-app dependencies.
- Self-host assets on the app's own origin when practical; pin external CDN
  versions. Don't load both `syntyr.all.css` and its constituent stylesheets.
- Use Playwright or equivalent browser automation to verify dynamic class
  changes, HTMX fragments, responsiveness and accessibility.
- Avoid large DOM swaps, expensive decorative effects on scrolling tables,
  and unnecessary hydration. Measure actual page LCP, CLS and INP.
