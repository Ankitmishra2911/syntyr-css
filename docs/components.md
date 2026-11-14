# Cyberline CSS component and token contract

Status: **experimental v0.3-alpha**, not yet released to a package registry. All CSS and markup are original to this repository; no upstream source code was copied.

## Loading and scoping

For the explicitly classed API (no automatic unclassed element styles):

```html
<link rel="stylesheet" href="cyberline.core.css">
<body class="cy-root cy-page" data-cy-theme="grid">
  <button class="cy-button cy-button--primary">Run</button>
</body>
```

For Pico-like semantic markup, add the optional file **after** core and mark the subtree:

```html
<link rel="stylesheet" href="cyberline.core.css">
<link rel="stylesheet" href="cyberline.semantic.css">
<section class="cy-semantic">
  <article>
    <label for="id">Operator <input id="id" name="id" required></label>
    <button>Continue</button>
  </article>
</section>
```

For optional effects, load `cyberline.effects.css`. `cyberline.css` is the legacy-compatible core + effects entry point. `cyberline.all.css` combines everything (semantic styling still requires `.cy-semantic`). `cy-root` should wrap any themed subtree; nested `data-cy-theme` overrides color tokens.

## Components

| Area | CSS API | Semantic alternative |
| --- | --- | --- |
| Buttons | `.cy-button`, `.cy-button--primary`, `.cy-button--outline`, `.cy-button--danger`, `.cy-button--small`, `.cy-button--ghost` | unclassed `button` |
| Panels | `.cy-panel`, `.cy-panel--cut` | unclassed `article` |
| Layout | `.cy-page` (viewport-height opt-in), `.cy-shell`, `.cy-header`, `.cy-grid`, `.cy-layout`, `.cy-inline`, `.cy-stack` | normal CSS layout |
| Typography | `.cy-logo`, `.cy-eyebrow`, `.cy-title`, `.cy-heading`, `.cy-lede`, `.cy-mono`, `.cy-caption`, `.cy-muted` | native heading/text |
| Status | `.cy-badge`, `.cy-alert`, `.cy-alert--danger`, `.cy-meter` on `progress` | native `progress` |
| Forms | `.cy-form`, `.cy-label`, `.cy-input`, `.cy-select`, `.cy-textarea`, `.cy-check`, `.cy-fieldset`, `.cy-help`, `.cy-error` | unclassed form controls |
| Overlays | `.cy-popover` on `[popover]`, `.cy-dialog` on `dialog`, `.cy-details` on `details` | browser defaults |
| Data | `.cy-table-wrap`, `.cy-table` | unclassed `table` |
| Effects (optional) | `.cy-grid-effect`, `.cy-glow`, `.cy-scanlines` | none |

Use native button `popovertarget="id"` to control a popover and `commandfor="id" command="show-modal"` to open a dialog in supporting browsers. This last native dialog invoker API has newer browser support; provide alternate ways to reach important content where needed. Do not build custom ARIA dialog/tab/combobox patterns unless they are tested and necessary.

## Theme tokens

| Token | Purpose |
| --- | --- |
| `--cy-bg`, `--cy-surface`, `--cy-surface-hi` | Background surfaces |
| `--cy-text`, `--cy-muted` | Foreground text |
| `--cy-accent`, `--cy-on-accent`, `--cy-accent-soft` | Accent and contrast |
| `--cy-frame`, `--cy-danger` | Borders and warning states |
| `--cy-font`, `--cy-mono` | System typography |
| `--cy-space-1` ... `--cy-space-5` | Spacing scale |
| `--cy-cut`, `--cy-radius`, `--cy-line`, `--cy-control-height` | Shape and layout |

Application CSS can override tokens:

```css
/* Unlayered CSS overrides the library's layered defaults. */
.my-surface { --cy-accent: #a9f890; }
```

## Accessibility and performance contracts

- Actual semantic HTML and associated labels; use `button` for actions and `a` for navigation.
- Visible `:focus-visible` outline; do not remove it with theme overrides.
- Contrast target: WCAG 2.2 AA for text; manually verify any customized tokens.
- Honor user preferences: `prefers-reduced-motion`, `forced-colors`; effects opt-in and static.
- Avoid relying on color alone for state; use labels or icons with text alternatives.
- Core CSS gzip limit: 5 KiB; full bundle gzip limit: 8 KiB; runtime JS: 0 bytes.
- Browser coverage: current Chromium, Firefox and WebKit. The included automated browser suite runs Chromium when installed and can be extended to other engines.
- Do not automatically treat the demo or contract tests as an accessibility certification: test screen readers, 200%/400% zoom, form errors, contrast, and actual products separately.

## Distribution behavior

The repository contains **no `package.json`**, Node runtime requirement, or bundling dependency. A standard Python 3 build script creates deterministic concatenated CSS and validates exact committed outputs:

```sh
python3 scripts/build.py
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v
```

## Licensing and provenance

MIT; this version is original work, not a fork or copy of Pico CSS, Chota or Open Props. If future work ports code from an upstream library, preserve that project's copyright and MIT notices and document the relevant files in `THIRD_PARTY_NOTICES.md`.


## Embedded versus full-page usage

`cy-root` provides a bounded styling context. Add `cy-page` **only for full-page experiences**. This separation prevents an embedded themed widget from unexpectedly forcing a viewport-height section.

```html
<section class="cy-root" data-cy-theme="noir">
  <div class="cy-panel">This can be embedded inside an existing application.</div>
</section>
```

For invalid form controls, associate error text through native labeling and `aria-describedby`, and set `aria-invalid="true"` for server-provided errors. `cy-error` changes text color; do not rely on color alone to communicate invalid state.

```html
<label class="cy-label" for="email">Email</label>
<input class="cy-input" id="email" type="email" aria-invalid="true" aria-describedby="email-error">
<p class="cy-error" id="email-error">Enter a valid email address.</p>
```

## v0.3 compositional patterns (no build step)

The following are ordinary CSS classes in `cyberline.core.css`:

| Class | Purpose |
| --- | --- |
| `.cy-region` | Named `cy-region` inline-size container for independent widget responsiveness |
| `.cy-split` | Stacked by default; two columns at container width >=43rem |
| `.cy-stats` | One/two/three columns at container widths <31rem, >=31rem, >=55rem |
| `.cy-stat`, `.cy-stat-label`, `.cy-stat-value` | Semantic telemetry card presentation |
| `.cy-empty` | Centered dashed-outline empty-state composition |
| `.cy-pricing`, `.cy-price-card` | One column until 43rem, then three equal columns |
| `.cy-price-card[data-cy-featured]` | Opt-in highlighted plan, purely visual, no ARIA claim |
| `.cy-price-value`, `.cy-feature-list` | Pricing typography and list styles |
| `.cy-toolbar` | Wrapping flex toolbar |

Attach `.cy-region` **on an ancestor** of the patterns. A region element isn't its own query container descendant; without a region ancestor the patterns remain readable one-column layouts. Nest separate regions for independently sized widgets. The `cy-region` name prevents unrelated page containers from changing their layouts.

Button state: `.cy-button[aria-pressed="true"]` is a pressed **toggle button**; `[data-cy-state="active"]` is decoration/host state; `[aria-busy="true"]` expresses in-progress updates but does not actually disable interactions. State changes and form handling are application responsibilities.

Additional inherited tokens: `--cy-ease`, `--cy-duration-fast`, `--cy-success`, `--cy-warning`. Extend themes with unlayered `.cy-root[data-cy-theme="custom"] { --cy-accent: ... }` CSS. Test contrast for your own values.

See [theme customization and token overrides](theme-customization.md), [MIT composition recipes](recipes.md) and [Tailwind architectural research](tailwind-research.md).
