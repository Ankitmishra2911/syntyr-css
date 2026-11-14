# Syntyr performance and design guidance

Syntyr is a scoped, CSS-first visual library with no runtime JavaScript, no
fonts downloaded by default, and no required package manager. Optimize
**real browser behavior** rather than targeting an arbitrary gzip byte count.

## Inspect stylesheet sizes without blocking releases

```sh
python3 scripts/build.py --check
python3 scripts/asset_report.py
python3 scripts/asset_report.py --json > /tmp/syntyr-sizes.json
python3 scripts/asset_report.py --baseline /tmp/syntyr-sizes.json
```

The report shows deterministic raw and gzip transfer sizes for every actual
distribution. A prior JSON report can be supplied to show signed size deltas.
Both increasing and decreasing sizes are diagnostic: **there is no 5 KiB or
8 KiB pass/fail limit**. A useful feature should not fail merely because of
compressed bytes. Instead, investigate surprising jumps and measure real
LCP, CLS, INP, style recalculation, and paint cost in production-shaped pages.

Start with `syntyr.core.css` alone. Add `syntyr.recipes.css`,
`syntyr.semantic.css`, or effects only when the application uses them.
Do not include both `syntyr.all.css` and its individual modules. Prefer
same-origin, cacheable stylesheets to an extra CDN hostname in most apps.

## Zero-JS visual accents

Optional recipes add depth and a stronger visual hierarchy without extra DOM,
canvas, web fonts or animations:

```html
<link rel="stylesheet" href="/css/syntyr.core.css">
<link rel="stylesheet" href="/css/syntyr.recipes.css">
<section class="syn-root syn-region" data-syn-theme="studio">
  <article class="syn-app-card syn-surface--accent syn-surface--lift">
    <label class="syn-label" for="search">Find an account</label>
    <input class="syn-input" id="search" name="q" type="search">
  </article>
</section>
```

- `syn-surface--accent` adds a token-colored inset top rule and subtle surface
  tint. It can be used on panels, cards and other bordered surfaces.
- `syn-surface--lift` adds a modest hover/focus treatment on capable pointers,
  without transforms or persistent `will-change`. Use sparingly, mainly where
  cards contain interactive elements. It does not make a card clickable.
- The visual system adapts to any of the seven theme palettes; forced-colors
  mode uses a visible border instead of relying on shadows.
- These are optional recipes, **not baseline component appearance changes**.

The original Grid/Noir aesthetic can remain technical; Studio/Corporate/Minimal
should feel restrained. Use typography hierarchy, consistent spacing and
purposeful accent color before adding glow, gradients or large shadows.

## Opt-in long-page render deferral

```html
<!-- Only below-the-fold sections of sufficiently long, dense pages. -->
<section class="syn-defer-section" style="--syn-defer-size: 42rem">
  <h2>Archive</h2>
  <!-- expensive table, logs or reporting visuals -->
</section>
```

`syn-defer-section` applies `content-visibility: auto` with a tunable
`contain-intrinsic-size` placeholder. The browser can skip layout and paint
for offscreen content until needed; actual benefit depends on DOM structure
and the browser. Printing restores full visibility. Choose an approximate
intrinsic block size based on actual content to reduce layout shifts.

**Do not** indiscriminately defer the hero/LCP content, small pages, open
dialogs, active focus targets, or containers whose height is critical to
navigation. It isn't virtualization and doesn't reduce network/DOM memory.
Measure on real pages before adopting it broadly.

## Developer-experience contract

- Native HTML first. Use existing `syn-*` classes and `--syn-*` tokens.
- Respect focus rings, disabled states, form semantics, reduced motion,
  color contrast, and forced colors.
- Keep framework-specific request/DOM logic in HTMX/React/Alpine/etc., not CSS.
- Use committed deterministic CSS; the stdlib Python build is for maintainers.
- Test actual browser rendering and zoom, not only compressed file size.

See [framework integrations](framework-integrations.md),
[theme customization](theme-customization.md) and
[component contract](components.md).
