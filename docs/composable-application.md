# Composable Syntyr themes and application surfaces (unreleased candidate)

Syntyr separates color, density, geometry and operational UI patterns.
These are original, MIT-licensed CSS features. They do not require JavaScript,
Node, Sass, font downloads or an application build step.

## Installation

Copy the current candidate's generated files into your own static assets:

```html
<link rel="stylesheet" href="/css/syntyr.core.css">
<link rel="stylesheet" href="/css/syntyr.recipes.css">
<link rel="stylesheet" href="/css/syntyr.presets.css">
<link rel="stylesheet" href="/css/syntyr.application.css">
```

`syntyr.presets.css` provides density and geometry attributes;
`syntyr.application.css` provides optional operational presentation.
Neither is included in `syntyr.all.css` or `syntyr.css`; load only the modules needed for your application. They are included in the candidate release ZIP and the
unversioned Cloudflare site output, not the immutable alpha.4 URL.

## Independent axes

```html
<section class="syn-root syn-region"
         data-syn-theme="studio"
         data-syn-density="compact"
         data-syn-geometry="precision">
  <article class="syn-panel" data-syn-theme="noir">
    Nested Noir keeps compact spacing and precision geometry.
  </article>
  <article class="syn-panel" data-syn-density="comfortable"
           data-syn-geometry="soft">
    Only this panel opts into larger spacing and soft corners.
  </article>
</section>
```

Themes: `grid`, `noir`, `studio`, `industrial`, `terminal`,
`corporate`, `minimal`.

Density: default (omit attribute), `compact` or `comfortable`.
The compact control minimum is 36 CSS px at the default root size, which
can fall below touch-friendly guidelines; use the default or comfortable
setting on touch-first experiences. A theme does not silently alter density.

Geometry: default (omit attribute), `precision`, `industrial` or `soft`.
Presets influence public radius/cut tokens and the optional frame module.
The presets can inherit across a nested color-theme boundary because
palette defaults defer to inherited geometry overrides.

The core exposes these new theme-relative aliases:
`--syn-link`, `--syn-focus-ring`, `--syn-border-subtle`.
They resolve against local palette tokens and can be overridden by host CSS.

## Operational presentation classes

- `.syn-data-toolbar` and `.syn-filter-group`: wrapping toolbar presentation.
- `.syn-section-heading`: heading/action alignment.
- `.syn-table--striped` and `.syn-table--dense`: table presentation;
  compose with existing `.syn-table`.
- `.syn-bulk-actions`: bulk-action surface. A real application supplies
  selection state, permissions and actions.
- `.syn-detail-list`: semantic definition lists; place each `dt`/`dd`
  pair inside a `div`.
- `.syn-timeline`: ordered list of audit events; use actual `time` elements.
- `.syn-form-columns`: responsive form grid inside a `.syn-region`.

See [the static application patterns demo](../examples/application-patterns.html).
All data in that demo is synthetic, and no buttons pretend to mutate state.

Syntyr intentionally does not implement search, sorting, selection,
authentication, validation, paging or server operations. Wire those
functions into your host application and preserve semantic controls.
For tables, use captions, column/row headers, and a named horizontal
scroll area where overflow is required. Do not use disabled styling as
security enforcement.

## Compatibility and verification

The public `syn-` namespace is unchanged. Without the optional sheets,
existing theme palettes, spacing and geometry keep their prior appearance.

Run:

```sh
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v
python3 tests/browser_matrix.py --browsers chromium firefox webkit
python3 tests/reflow_test.py --browsers chromium firefox webkit
```

The last two commands require optional Playwright developer tooling and
available browser binaries; tests do not certify screen-reader accessibility.
