# Syntyr CSS distribution

Syntyr CSS is MIT-licensed. No NPM install, JavaScript runtime, fonts,
icons, Sass compiler or CSS framework is required to use the distributed CSS.

## Recommended: self-host a versioned stylesheet

1. Download the asset from the [GitHub release](https://github.com/dporkka/syntyr-css/releases/tag/v0.3.0-alpha.3), or copy the matching file from the tag.
2. Put `syntyr.core.css` in your application's static CSS directory.
3. Load it normally:

```html
<link rel="stylesheet" href="/css/syntyr.core.css">
<section class="cy-root" data-cy-theme="grid">
  <button class="cy-button cy-button--primary">Initialize</button>
</section>
```

The stylesheet's path is *your* path; mount or copy the file there.
The above works with Go templates, plain HTML, Astro, HTMX, React and other
renderers. Add `cy-page` to the root only if you want full-page min-height.

## Optional themes and semantic HTML

The published alpha.3 core includes Grid, Noir and Studio. The unreleased
alpha.4 source also offers Industrial, Terminal, Corporate and Minimal. Set
`data-cy-theme` on the scoped root or a nested region; all seven preserve
the same component API. The published alpha.3 tag does **not** contain the four new themes.

Load `syntyr.semantic.css` after core **only** if you want automatic semantic
element styles within `.cy-semantic`. For static glows and decorative grid
effects, load `syntyr.effects.css` after core. SaaS, business and terminal layouts
are opt-in via `syntyr.recipes.css`. Layout and spacing helpers are
opt-in via `syntyr.utilities.css` (legacy alias `cyberline.utilities.css`).

`syntyr.css` bundles core and effects. `syntyr.all.css` bundles all modules
while still requiring `.cy-semantic` to opt into semantic element styles.
Avoid loading these bundles alongside their component files: that duplicates CSS.

## Pinned CDN for prototyping

```html
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/gh/dporkka/syntyr-css@v0.3.0-alpha.3/dist/syntyr.core.css">
```

This is an *external* CDN (jsDelivr), not a SYNTYR runtime dependency.
Pin a specific tag rather than using `@latest` or a moving branch.
For production reliability, self-host your copy and control cache headers.

## Release artifacts and guarantees

The prospective alpha.4 ZIP contains seven SYNTYR CSS distributions plus seven
byte-identical legacy Cyberline compatibility files, the terminal ANSI palette
JSON, this guide and the MIT
license, and the README. The ZIP is created deterministically using only
Python's standard library:

```sh
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v
python3 scripts/package_release.py
```

All seven development-branch palettes and essential components are MIT-licensed. Commercial
premium templates, if introduced, will be independently authored and sold
separately. This v0.3 alpha is **not** a v1 production compatibility guarantee;
cross-browser and full accessibility audits are still release gates.

For existing Cyberline integration paths and the unchanged `cy-` selectors, see [brand migration](brand-migration.md).
