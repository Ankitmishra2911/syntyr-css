# Hosting SYNTYR on Cloudflare

SYNTYR is a static website and CSS library. It does not need a server,
database, JavaScript runtime, Node install, NPM install, or a CDN SDK.

## Reproducible, allowlisted output

From the repository root:

```sh
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v
python3 scripts/build_cloudflare_site.py
python3 scripts/build_cloudflare_site.py --check
```

The generated `.cloudflare-public/` directory is the **only** directory
that may be published. Never deploy the repository root: it contains tests,
scripts, experiments, and business planning material.

The site retains relative HTML links, component examples, Markdown guides,
terminal palette JSON, and public CSS assets. The optional documentation-only theme editor has its
own small JavaScript file; consuming apps and other demos require none.

## Cloudflare hosting

Preferred for new deployments: Cloudflare Workers Static Assets. A simple
existing Cloudflare Pages project also serves these files globally without a
Worker runtime; use Pages when its Git integration is already in place.

For a Git-connected static deployment, use:

- Repository: `dporkka/syntyr-css`, production branch `main`
- Build command: `python3 scripts/build.py --check && python3 -m unittest discover -s tests -q && python3 scripts/build_cloudflare_site.py`
- Output directory: `.cloudflare-public`
- Project root: repository root
- No server-side functions and no install command

Cloudflare Pages project: `syntyr-css`, configured for `main` and the
`.cloudflare-public` output, with hostname `syntyr-css.pages.dev`. This
project uses Git-connected builds, and its live production deployment was
verified with HTTP 200 responses for public pages/assets and HTTP 404 for
non-public paths. Cloudflare builds run the Python test suite as a release gate.

Configure a custom domain only after DNS and trademark/name clearance.
Keep the existing GitHub Pages site as a rollback until production checks pass.

## Immutable stylesheets for the live documentation site

The Cloudflare publish builder rewrites its **own HTML stylesheet links**
to content-addressed `/_assets/css/<sha256>.css` copies. Cloudflare serves
these with `Cache-Control: public, max-age=31536000, immutable`, so
repeat visits avoid unnecessary stylesheet revalidation. A change to any
CSS asset changes the hash and the generated HTML reference in the same
deployment. The original source HTML files are **not** edited.

The regular `/dist/*` preview and download URLs remain available,
mutable and revalidated (`max-age=0, must-revalidate`); never mark
unversioned preview CSS immutable. Frozen public `/v/<version>/*`
releases remain byte-for-byte unchanged. Third-party applications should
still self-host or pin versioned assets, rather than copy the hashed
documentation-only URLs.

The builder recognizes local linked stylesheet files that are included
in the public allowlist. It rejects CSS containing unresolved `@import`
or `url()` dependencies rather than silently moving it to a different
relative path. If a new CSS file needs relative assets, explicitly add
and test a relocation strategy before publishing.

## CSS CDN URLs

Unversioned CSS: `/dist/syntyr.core.css` for previews and quick starts.

Frozen CSS: `/v/0.3.0-alpha.4/syntyr.core.css` for pinned consumers.
Every version under `site-releases/` is copied to `/v/<version>/`.
Published snapshots have SHA-256 hashes in `site-releases/manifest.json`.
Do not modify, reuse, or delete a published version; release a new version.
The build refuses mismatched hashes, and the `_headers` file marks only
`/v/*` assets as immutable.

**Self-host CSS in the consuming application's own origin when possible.**
A separate CDN hostname can cost an additional DNS lookup, connection, and
TLS negotiation even when Cloudflare serves it from a nearby edge.

## HTTP validation after deploy

```sh
BASE=https://<your-cloudflare-site>
curl -fsSI "$BASE/"
curl -fsSI "$BASE/docs/"
curl -fsSI "$BASE/dist/syntyr.core.css"
curl -fsSI "$BASE/v/0.3.0-alpha.4/syntyr.core.css"
curl -fsS -o /dev/null -w '%{http_code}\n' "$BASE/business/strategy.md"
```

Expected: HTML and CSS 200; internal business document 404. The published
root `404.html` is required: without it, Cloudflare Pages serves unknown
paths as an SPA fallback with HTTP 200.
Check MIME types (`text/html`, `text/css`), Cache-Control,
`cf-cache-status` where present, and gzip/Brotli transfer behavior.

Cloudflare routing may normalize trailing-slash URLs. Check for 301/308
redirects as well as final 200 responses. The `_headers` file applies
security and cache policy without adding application JavaScript.

## CI release checks

`.woodpecker/quality.yaml` gates pull requests and `main` pushes with
Python-only CSS verification, the repository contract tests, the allowlisted
Cloudflare output and deterministic release packaging. The existing Cloudflare
build command independently runs the same Python tests.

`.woodpecker/browser.yaml` is a manual/tag release gate using Playwright's
pinned browser image (Chromium, Firefox and WebKit), enlarged-text reflow and
the theme editor. Configuring the pipeline is **not** proof that the Woodpecker
repository is activated or a pipeline executed. Require a real successful
run on the exact proposed commit before declaring CI green.

## Performance validation

Measure WebPageTest/Lighthouse in several regions and on mobile.
Track LCP, CLS, INP, transfer bytes, and first-load connection overhead.
Cloudflare reduces distance to content but does not fix CSS render costs.

For comparative measurement rules, see [performance validation](performance-validation.md).
