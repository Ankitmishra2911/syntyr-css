# Syntyr CSS distribution

Syntyr CSS is MIT-licensed. No NPM install, JavaScript runtime, fonts,
icons, Sass compiler or CSS framework is required to use the distributed CSS.

## Recommended: self-host a versioned stylesheet

1. Download the asset from the [GitHub release](https://github.com/dporkka/syntyr-css/releases/tag/v0.3.0-alpha.4), or copy the matching file from the tag.
2. Put `syntyr.core.css` in your application's static CSS directory.
3. Load it normally:

```html
<link rel="stylesheet" href="/css/syntyr.core.css">
<section class="syn-root" data-syn-theme="grid">
  <button class="syn-button syn-button--primary">Initialize</button>
</section>
```

The stylesheet's path is *your* path; mount or copy the file there.
The above works with Go templates, plain HTML, Astro, HTMX, React and other
renderers. Add `syn-page` to the root only if you want full-page min-height.

## Optional themes and semantic HTML

Grid, Noir and Studio ship in the **same** core stylesheet; set
`data-syn-theme="grid"` or `data-syn-theme="noir"` or `data-syn-theme="studio"` on the scoped root.
You can nest differently themed elements.

The unreleased alpha.5 candidate adds Industrial, Terminal, Corporate and Minimal using the same scoped `data-syn-theme` contract. The published alpha.4 release includes Grid, Noir and Studio only.

Load `syntyr.semantic.css` after core **only** if you want automatic semantic
element styles within `.syn-semantic`. For static glows and decorative grid
effects, load `syntyr.effects.css` after core. SaaS, business and terminal layouts
are opt-in via `syntyr.recipes.css`. Optional frame geometry is in `syntyr.geometry.css`.
The alpha.5 candidate additionally provides `syntyr.utilities.css` for opt-in layout, spacing and visually-hidden helpers.

`syntyr.css` bundles core and effects. `syntyr.all.css` bundles the original
modules while still requiring `.syn-semantic` to opt into semantic element styles.
The new optional `syntyr.presets.css` and `syntyr.application.css` are separate
from this bundle, preserving its established size budget.
Avoid loading these bundles alongside their component files: that duplicates CSS.

## Pinned CDN for prototyping

```html
<link rel="stylesheet"
      href="https://syntyr-css.pages.dev/v/0.3.0-alpha.4/syntyr.core.css">
```

The first-party Cloudflare CDN serves frozen, checksum-verified CSS releases
from a global edge network. Unversioned `/dist/` URLs can change with builds;
pin `/v/<version>/` instead. The documentation's optional theme editor
has JavaScript, but the library CSS and consumer sites do not require it.
For production applications, copying the versioned CSS to your own origin
usually avoids an additional hostname connection.

## Release artifacts and guarantees

The published alpha.4 release contains seven SYNTYR CSS distributions. The
unreleased alpha.5 candidate contains ten SYNTYR distributions, including
optional utilities, presets and application stylesheets, plus the terminal ANSI palette JSON, this
guide, the MIT license, and README. No retired compatibility aliases are shipped. The ZIP is created deterministically using only
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

The `syn-` selectors, `--syn-` custom properties and `data-syn-` attributes are the only supported source API.
