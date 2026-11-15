# Deployed Syntyr mobile performance / cache / accessibility audit

Date: **November 15, 2026**. The subject was the publicly deployed
[SYNTYR Cloudflare site](https://syntyr-css.pages.dev), at its real
canonical `/examples/business` and `/examples/saas` URLs. This is
**not field Core Web Vitals** data.

## Reproduction

With optional, developer-only Playwright + Chromium installed, and a local
copy of axe-core (the site never loads axe):

```sh
python3 scripts/audit_live_performance.py \
  --origin https://syntyr-css.pages.dev \
  --runs 7 --latency-ms 150 --download-kbps 1600 --cpu-rate 4 \
  --axe-file /tmp/axe.min.js \
  --output /tmp/syntyr-live-performance.json
```

The script rejects non-Syntyr public targets and arbitrary remote URLs.
It uses Chromium DevTools network throttling (150 ms extra latency,
1.6 Mbps download and 4× CPU slowdown), a 390×844 mobile viewport,
reduced motion, and seven new-context cold navigations plus same-context
warm re-navigations per page. It collects browser FCP/LCP, non-input CLS,
TTFB, resource transfer sizes, request counts, cache headers,
JavaScript errors and optional automated WCAG-tagged axe results.

The network profile is deliberately synthetic. It does **not** model
actual cellular packet loss, CPU architecture, local device thermals,
field INP, or latency to every region. Browser and Cloudflare caches
may vary over time. Resource Timing `transferSize` includes response
headers and can be zero for cache hits; it is not an application billing
or bandwidth metric. Browser instrumentation is not required by sites.

## Observed results

All times in **milliseconds**; medians from seven samples.

| Deployed page | Cold FCP/LCP | Warm FCP/LCP | Cold CSS transfer | Warm CSS transfer |
| --- | ---: | ---: | ---: | ---: |
| Business website | 508 | 364 | 12,075 bytes | 900 bytes |
| SaaS dashboard | 492 | 360 | 11,010 bytes | 600 bytes |

These two pages were text-LCP dominated in this test: median FCP
matched median LCP. They are not evidence about hero-image-heavy
landing pages. Neither page reported non-input CLS in Chromium; both
had one visible main element, one H1, **zero runtime scripts**, no
horizontal overflow at 390 px, no page errors and no failed requests.

### Cache delivery

All live `/dist/syntyr.*.css` stylesheet responses declared
`Cache-Control: public, max-age=0, must-revalidate`. The business
page loaded 3 stylesheets, the dashboard 2. The repeat navigation
still requested each stylesheet (cached validation responses account
for the small transferred bytes). This is not the same as serving
immutable content-addressed CSS to the documentation website.

The existing public `/v/<published-version>/` CSS releases correctly
send `Cache-Control: public, max-age=31536000, immutable`. That
mechanism cannot simply replace the site's **unreleased alpha.5**
preview styles, which are allowed to change between builds.

**Recommendation:** prefer content-addressed, immutable stylesheet
copies for the site's own live HTML, while preserving public
`/dist/` and immutable `/v/` URLs. Validate a generated preview
before changing Cloudflare production. Do not mark mutable `/dist`
assets immutable: stale CSS could break pages after a deployment.

### Accessibility and CSP

The developer-injected axe-core WCAG 2/2.1/2.2 tag audit reported:

| Page | Automated violations | Incomplete checks |
| --- | ---: | --- |
| Business | 0 | 1: `color-contrast` |
| SaaS dashboard | 0 | 0 |

**0 automated violations is not a WCAG compliance certification.**
Business contrast remains a manual review item; keyboard,
screen-reader, native zoom, forced-colors and WebKit behaviors
require separate coverage.

Neither page returned an enforced `Content-Security-Policy` or
report-only CSP header. Both pages intentionally use inline style
attributes (8 on the business page, 1 on the SaaS example).
Adding `style-src 'self'` directly would block these declarations,
potentially changing layout and bar heights. Do not impose that
strict CSP on the site without replacing inline styles or adopting
an explicit, tested nonce/hash policy. Syntyr's core itself needs
no inline script for these pages.

## Release decision

Keep CSS-first, JavaScript-optional runtime behavior. The direct
site improvements worth exploring are **immutable generated CSS
URLs** and manual accessibility verification. No result here
justifies making automatic critical-CSS extraction mandatory.
