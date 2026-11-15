# Optional Syntyr + Lit example

This is **not** a Syntyr runtime dependency or part of the Cloudflare static-site
allowlist. It demonstrates two independent Web Component styling strategies:

- **Light DOM**: Lit renders normal Syntyr classes into the page. The standard
  `syntyr.core.css` stylesheet applies without copying it into a Shadow Root.
- **Shadow DOM**: Lit keeps its default shadow boundary. Local `static styles`
  consume inherited `--syn-*` custom properties and expose `::part()` hooks.

## Run locally

From this directory, with Node.js and npm available:

```sh
npm ci
npm run build
cd ../..
python3 -m http.server 8765 --bind 127.0.0.1
# Open http://127.0.0.1:8765/examples/lit/index.html
```

The page uses a local bundled module and the repository's built CSS. The lockfile
pins the opt-in example dependencies. There is no runtime network request to a
third-party CDN. Run `python3 scripts/build.py` at repository root if CSS
artifacts need regeneration.

To run browser coverage after building:

```sh
python3 tests/lit_browser.py --browsers chromium,firefox,webkit
```

Requires a separate developer installation of Python Playwright and its browsers.
Unavailable engines fail visibly rather than being counted as passing.

The HTML includes static fallback markup for both components. Without JavaScript,
this remains readable; enhanced buttons intentionally operate on **local demo
state only**. The real application must own persistence and authorization.

See [the Lit integration guide](../../docs/lit-integration.md) and
[component-authoring contract](../../docs/component-authoring.md).
