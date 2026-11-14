# Cyberline CSS distribution

Cyberline CSS is MIT-licensed. No NPM install, JavaScript runtime, fonts,
icons, Sass compiler or CSS framework is required to use the distributed CSS.

## Recommended: self-host a versioned stylesheet

1. Download the asset from the [GitHub release](https://github.com/dporkka/cyberline-css/releases/tag/v0.3.0-alpha.2), or copy the matching file from the tag.
2. Put `cyberline.core.css` in your application's static CSS directory.
3. Load it normally:

```html
<link rel="stylesheet" href="/css/cyberline.core.css">
<section class="cy-root" data-cy-theme="grid">
  <button class="cy-button cy-button--primary">Initialize</button>
</section>
```

The stylesheet's path is *your* path; mount or copy the file there.
The above works with Go templates, plain HTML, Astro, HTMX, React and other
renderers. Add `cy-page` to the root only if you want full-page min-height.

## Optional themes and semantic HTML

Grid, Noir and Studio ship in the **same** core stylesheet; set
`data-cy-theme="grid"` or `data-cy-theme="noir"` or `data-cy-theme="studio"` on the scoped root.
You can nest differently themed elements.

Load `cyberline.semantic.css` after core **only** if you want automatic semantic
element styles within `.cy-semantic`. For static glows and decorative grid
effects, load `cyberline.effects.css` after core. SaaS, business and terminal layouts
are opt-in via `cyberline.recipes.css`. Advanced geometry is opt-in via `cyberline.geometry.css` (load after core; use either it or the all-in-one bundle).

`cyberline.css` bundles core and effects. `cyberline.all.css` bundles all modules
while still requiring `.cy-semantic` to opt into semantic element styles.
Avoid loading these bundles alongside their component files: that duplicates CSS.

## Pinned CDN for prototyping

```html
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/gh/dporkka/cyberline-css@v0.3.0-alpha.2/dist/cyberline.core.css">
```

This is an *external* CDN (jsDelivr), not a Cyberline runtime dependency.
Pin a specific tag rather than using `@latest` or a moving branch.
For production reliability, self-host your copy and control cache headers.

## Release artifacts and guarantees

The development-branch ZIP now includes the optional geometry stylesheet along with the other CSS distributions and terminal
ANSI palette JSON, this guide, the MIT
license, and the README. The ZIP is created deterministically using only
Python's standard library:

```sh
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v
python3 scripts/package_release.py
```

Both visual themes and all essential components are MIT-licensed. Commercial
premium templates, if introduced, will be independently authored and sold
separately. This v0.3 alpha is **not** a v1 production compatibility guarantee;
cross-browser and full accessibility audits are still release gates.
