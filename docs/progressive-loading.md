# Progressive loading and critical CSS

Syntyr is a CSS-first, **zero-required-JavaScript** library. For most sites,
a regular, self-hosted, cacheable `syntyr.core.css` loaded early is the
baseline to beat. Do not add a critical CSS pipeline merely because it is
available. Optimize **LCP**, **CLS**, browser style/layout/paint work and the
repeat-visit experience, not only the apparent time of the first paint.

See the [performance-first example](../examples/performance-first.html), the
[existing rendering benchmark](performance-and-polish.md) and the
[benchmark comparison protocol](performance-validation.md).

## Recommended default: early CSS, selective modules, native image priority

```html
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="/css/syntyr.core.css">
  <!-- Include only optional modules actually used on this route. -->
  <link rel="stylesheet" href="/css/syntyr.recipes.css">
</head>
<body class="syn-root" data-syn-theme="studio">
  <main>
    <h1>Real page content</h1>
    <!-- Only assign high priority to a likely, verified LCP image. -->
    <img src="/media/hero.webp" alt="Preview of the product dashboard"
         width="1200" height="700" loading="eager"
         fetchpriority="high" decoding="async">
    <!-- Below the first viewport, if appropriate: -->
    <img src="/media/details.webp" alt="Detailed product view"
         width="1200" height="700" loading="lazy" decoding="async">
  </main>
</body>
```

- Load core early as a regular render-blocking stylesheet. CSS is necessary
  for a correct first paint. Same-origin, versioned and cacheable assets
  commonly outperform adding a second CDN connection.
- Do **not** add `<link rel="preload" as="style">` for CSS that the
  browser already discovers early in `<head>`. Duplicate preloads can
  compete for bandwidth, and preloading is not the same as inlining.
- Keep the likely LCP image eager and give it `fetchpriority="high"` only
  if browser traces support that decision. Hero CSS background images are
  often discovered later than an actual HTML `<img>`; consider an HTML
  image for important content. For responsive images use `srcset` and
  `sizes`; reserve the correct aspect ratio at every breakpoint.
- Use `loading="lazy"` for truly offscreen images and iframes, not for
  the first screen or the LCP element. Browser heuristics and viewport
  dimensions vary. A small page does not need lazy loading everywhere.
- Keep system fonts by default. If a brand font is necessary, self-host it,
  subset it, and consider `font-display` and selective font preloading
  *only* for a font actually used above the fold. Avoid preloading every
  weight. Fonts can change text geometry and CLS.
- Lazy video, heavy embeds, third-party scripts and hydration belong to the
  consuming application, not to Syntyr's CSS runtime. Supply accessible
  fallbacks and an actual server-rendered content path.

## Use selective builds only when modules really matter

The optional standard-library builder selects explicit **source modules**,
not CSS selectors. It never scans templates or purges dynamic classes:

```sh
python3 scripts/build_selective.py \
  --components layout,typography,buttons,forms \
  --modules recipes \
  --output /tmp/syntyr.marketing.css \
  --report /tmp/syntyr.marketing.json
```

That file is a standalone stylesheet with the required tokens/base and
canonical cascade order. It is **not** a critical CSS extractor: Syntyr
cannot infer what is visible in the first viewport, and the consumer must
select all components needed by its routes. If a route uses numerous
components or themes, the prebuilt core may be simpler and faster.

Avoid combining `syntyr.all.css` with modules already present in that bundle.
Do not split dependencies in ways that break variables, cascade layers,
nested themes or responsive rules.

## Critical CSS: conditional, optional and measured

Critical CSS means the subset of styles needed to render the **initial
viewport**. It is typically **inlined into the document head**, not
preloaded. Deferring the remaining stylesheet is a separate operation with
correctness and accessibility consequences.

Syntyr currently **does not ship automatic above-the-fold extraction or a
runtime CSS loader**. A tool claiming that explicit source modules are
necessarily "critical" would be misleading: real critical CSS varies with
the document, viewport, device, color scheme, state, font loading and route.

Before deploying a route-specific extraction integration:

1. Measure a baseline with normal early core CSS, on both cold and warm
   navigations. Include a mobile-sized viewport, realistic image assets
   and representative slow networks and CPUs.
2. Generate candidate critical CSS with an application build tool or a
   browser-aware extractor, **without altering Syntyr's source**.
   Preserve `@layer` ordering, custom property dependencies, `@media`,
   container queries, themes, focus and forced-colors styles.
3. Include the rest of the stylesheet correctly and test no-script,
   failed-network, print, dynamic routes, zoom, dark/light and reduced
   motion. A standard `<link rel="stylesheet">` after inlining can still
   block rendering, negating the intended improvement. Nonblocking load
   patterns have extra failure modes; do not hide unstyled content or
   require client JavaScript for essential styling.
4. Account for **CSP**: an inline `<style>` requires an authorized hash
   or nonce (or another explicitly allowed policy). Never recommend
   `unsafe-inline` just to make a build optimization work.
5. Check CSS delivery **and HTML cache duplication**. Inline rules are
   sent again on each HTML response; external CSS can remain cached across
   pages. Count duplicated declarations and inspect cumulative CSS.
6. Adopt only if the candidate improves *measured* LCP or related rendering
   work without worsening CLS, follow-up navigations, interactivity or
   visual/accessibility correctness. Otherwise retain normal stylesheets.

Do not use `media="print" onload="this.media='all'"` as a universal
recommendation: it depends on inline script execution, needs a fallback,
changes priority and requires CSP handling. Adding JS solely to load the
small Syntyr core contradicts its default performance contract.

## Compare two variants reproducibly

The optional Playwright comparison tool accepts **two actual HTTP(S)
pages**: a normal-stylesheet baseline and a candidate generated in the
application. Both must contain equivalent DOM, images and text. This
comparison tool generates *no* CSS and requires *no* JavaScript in the
application. Its own instrumentation uses Playwright at development time.

```sh
# Example only: serve the two application variants yourself.
python3 scripts/perf_loading_compare.py \
  --baseline http://localhost:8000/baseline.html \
  --candidate http://localhost:8000/critical-candidate.html \
  --browsers chromium,firefox,webkit \
  --viewports mobile,desktop --runs 10 \
  --screenshots /tmp/syntyr-loading-shots \
  --output /tmp/syntyr-loading-comparison.json
```

Install optional Playwright browsers as described in
[performance and polish](performance-and-polish.md).
The tool reports median and nearest-rank p75 browser FCP, LCP,
non-input CLS and stylesheet request counts, separately for **cold**
(new browser context) and **warm** (repeat navigation) sessions.
It reports unavailable browser metrics as `null`, not zero.
Screenshots help detect a visually incorrect candidate; they are not
a substitute for a11y, reflow or forced-color testing.

A clean result on localhost cannot establish field Core Web Vitals, production
network RTT, HTTP transfer bytes, realistic cache distributions or INP.
The tool does not throttle networks or emulate slow CPUs; do that with
appropriate browser/performance infrastructure and disclose the settings.
A stylesheet request count is **not** the transferred CSS byte count.
Run a real-user measurement where traffic permits.

## Rendering and release decisions

Large independent below-the-fold regions may opt in to
`.syn-defer-section` (`content-visibility: auto`). Do not defer the
hero, sticky navigation, interactive controls that need focus, or the
user's likely next interaction. See the caveats and engine-by-engine
counterexample in [the rendering benchmark](performance-and-polish.md).

**Release decision:** keep Syntyr's core and CSS distributions unchanged.
Only consider an optional external/adapter critical CSS extractor after
repeatable LCP/CLS and visual evidence from realistic marketing and SaaS
routes. No arbitrary gzip-size release gates are justified.
