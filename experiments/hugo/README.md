# Hugo v0.170.0 — isolated documentation proof

**Not the live Cyberline website.** This is a build-time-only experiment.
The canonical website at index.html, gallery at docs/index.html, GitHub Pages
main-branch deployment, and free CSS releases stay unchanged.

## Why this exists

Hugo can render the existing Markdown source through filesystem mounts, while
reusing Cyberline's compiled CSS and example HTML. No Hugo theme, npm, Sass,
JavaScript bundler, Go module or new application server is needed.

Install the standard Hugo binary at **v0.170.0** and run from the repository root:

~~~sh
hugo --source experiments/hugo --destination /tmp/cyberline-hugo-preview --minify
~~~

Build output goes outside the repository. To inspect it locally:

~~~sh
hugo server --source experiments/hugo --baseURL http://localhost:1313/
~~~

The committed baseURL is a placeholder. The generated preview is not deployed.
Do not point GitHub Pages to this output unless URL parity and full site
migration have been deliberately planned.

## Rollout gates

1. Markdown guides require rendered navigation, search-ready documentation
   sections, content versioning, or frequent content updates.
2. A real output parity test preserves existing public links and downloads.
3. The build can run with a pinned executable and no frontend runtime.
4. Deployment and rollback are deterministic and independently previewed.

Current decision: **do not migrate**. Keep serving existing static HTML and
add Hugo only if the documentation content and maintenance demands grow.

## Validation recorded

Official Hugo v0.170.0 generated 11 HTML pages from the current repository
Markdown and templates. The standard-library verification script passed 67
internal references and confirmed that the output contained neither
JavaScript script tags nor Python source/cache files. This is a build smoke
test, not a hosted production deployment or full visual-accessibility audit.
