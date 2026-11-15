# SYNTYR alpha.5 — outstanding accessibility review

The current November 14, 2026 (Brasília time) production baseline is `main` commit `4a623d0`, including merged [PR #21](https://github.com/dporkka/syntyr-css/pull/21). The **alpha.5 seven-theme release remains unpublished**; the published alpha.4 release is unchanged. The merged CSS and selected public documents have byte-for-byte SHA-256 parity with the live Cloudflare Pages site. This document tracks test evidence, **not an accessibility certification**.

## Automated axe-core findings

The fourteen-page post-merge audit with axe-core 4.10.3 and WCAG A/AA tags returned **zero confirmed violations** and **eleven inconclusive `color-contrast` rule results involving 325 individual targets**. Incomplete is not equivalent to passing.

| Page | Inconclusive elements |
| --- | ---: |
| `index.html` | 42 |
| `docs/index.html` | 115 |
| `examples/console.html` | 33 |
| `examples/resources.html` | 45 |
| `examples/pricing.html` | 8 |
| `docs/console-kit.html` | 14 |
| `examples/saas.html` | 0 |
| `examples/business.html` | 6 |
| `examples/terminal.html` | 4 |
| `examples/geometry-terminal.html` | 26 |
| `examples/operations-console.html` | 11 |
| `examples/themes.html` | 21 |
| `examples/vertigo-admin.html` | 0 |
| `examples/saas-workflows.html` | 0 |
| **Total** | **325** |

The 325 targets comprise 282 unresolved backgrounds involving gradients, 34
involving pseudo-elements, four too-short text cases, four non-text-only cases,
and one partially obscured element. They are **not** 325 proven defects.
Generate a reproducible node-by-node triage report (selectors, HTML snippets,
rule and failure summaries) in a local file using the developer-only audit:

```sh
python3 tests/axe_audit.py --axe-file /tmp/axe.min.js \
  --report /tmp/syntyr-axe-manual-review.json
```

The automated checker cannot establish the effective paint underneath these foregrounds where gradients and pseudo-elements overlap text. Contrast-token unit tests are useful but do not certify composited backgrounds.

## Supplemental browser-pixel contrast triage — merged `4a623d0`

The axe report's **325 incomplete targets** were also investigated with a
one-off Chromium screenshot-sampling pass on the merged source. This does not
alter the number of axe findings or convert an incomplete axe result to a pass.

| Viewport | Elements with pixel samples | Not directly sampled | Background-pixel samples | Lowest measured contrast |
| --- | ---: | ---: | ---: | ---: |
| 1280 px | 324 | 1 | 5,970 | 4.65:1 |
| 390 px | 310 | 15 | 6,480 | 5.09:1 |
| 320 px | 310 | 15 | 7,239 | 4.95:1 |
| **Total element/viewport observations** | **944** | **31** | **19,689** | — |

**No below-threshold result was found at the sampled positions** using 4.5:1
for ordinary text and 3:1 for large/bold text. The closest result was the
Studio header badge at 1280 px (4.65:1 against a gradient); it should receive
priority in visual review because its margin above 4.5:1 is narrow.

Method: Chromium **156.0.8078.4** at device scale factor 1, Playwright
**1.65.2**, a 1280/390/320 px page viewport, `getComputedStyle().color`
for text foreground, text-node `Range.getClientRects()` for location, and
full-page screenshots with glyph fill temporarily transparent to reveal
underlying gradients. Five horizontal by three vertical points per text
fragment were sampled and compared using the WCAG sRGB luminance/contrast
formula. These are **sampled background pixels**, not a guarantee about
every pixel beneath every glyph. Fixed viewport and static states do not
establish behavior across zoom, hover, focus or user-customized themes.

The sole 1280 px unsampled target was `#dispatch`, a textarea without
ordinary text nodes; its computed placeholder color `rgb(173,191,202)`
against background `rgb(8,15,25)` measures **10.14:1**, and its input
text color measures **17.93:1**. At 320/390 px, the 14 additional unsampled
targets were horizontally off-screen cells/statuses inside the deliberately
scrollable `examples/resources.html` table. These cells were sampled at
1280 px, but their mobile scrolled state still warrants manual inspection.

**Interpretation:** this triage found no obvious color-contrast regression in
the sampled cases; it **does not** close the 325 manual-review targets or
certify WCAG AA. Background sampling can miss local gradient extrema,
overlapping pseudo-elements, text-shadow effects, embedded graphics, and
interactive states. The actual screen reader, real zoom, high-contrast mode,
and representative-product checks below remain open.

## Manual verification protocol

For each flagged element, record selector, theme, browser, viewport/zoom setting, sampled foreground and effective background, measured contrast and screenshot. Test the lowest-contrast part of each gradient. Apply WCAG thresholds of at least 4.5:1 for regular text and 3:1 for large text and applicable essential UI graphics. Check hover, focus, disabled, selected and nested-theme contexts.

Automated browser evidence covers **126 viewport cases** across Chromium/Firefox/WebKit and **168 enlarged-text reflow cases**. The Chromium forced-colors primary-link screenshot and focus tests pass for all seven palettes. None of these substitute for native Windows High Contrast or other OS-level modes, real browser zoom, or a screen reader.

## Remaining release checklist

- [ ] Measure or adjudicate each of the 325 inconclusive text/background cases.
- [ ] Test keyboard-only navigation, native dialog/popover focus, table regions, disclosure and form semantics in a representative real app.
- [ ] Perform real assistive-technology testing with NVDA, JAWS, VoiceOver or Orca and record evidence.
- [ ] Test true 200% and 400% browser zoom on supported browsers; verify navigation, reflow and target visibility.
- [ ] Check actual OS forced-colors/high-contrast and reduced-motion settings.
- [x] Record the browser engines and versions used for automated testing (not a permanent support guarantee): Chromium 159.0.8154.6, Firefox 159.0, WebKit 27.2 in the Linux Playwright 1.65.2 test container.
- [ ] Establish browser support versions and unresolved exceptions before a stable release.

A passing axe-core run alone is **not** sufficient to claim WCAG conformance.
