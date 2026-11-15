# SYNTYR alpha.5 — outstanding accessibility review

This report distinguishes the most recent automated findings from older
pixel-sampling evidence. It is **not** a WCAG certification.

## Follow-up audit: `9f7f22b` (November 15, 2026)

This is a **newer source-only candidate audit**, not a published
release or an accessibility certification. It incorporates the enlarged-text
WebKit reflow fixes and the restored `examples/native-apis.html` audit coverage.

- Chromium headless, Playwright 1.58.0 and the pinned axe-core **4.10.3**:
  **28 pages audited, zero confirmed automated WCAG-tagged violations**,
  **14 incomplete color-contrast rule results involving 162 distinct
  element entries**. The axe payload SHA-256 was
  `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`.
- Source CSS includes targeted min-content grid sizing, text wrapping,
  and long-label reflow improvements. The original 320px / 2× WebKit
  reproducible overflow failures on six pages were resolved in focused tests.
- WebKit **26.0** was launched with user-local native libraries and
  Playwright 1.58.0 on Ubuntu 24.04; neither the operating-system packages
  nor Syntyr consumer JavaScript dependencies were changed. This is useful
  browser evidence but does **not** substitute for the pinned Playwright
  1.65.2 release-image gate, genuine browser 200%/400% zoom,
  OS-native high-contrast, or screen-reader testing.

| Page | Incomplete contrast element entries |
| --- | ---: |
| `docs/blocks.html` | 37 |
| `examples/geometry-terminal.html` | 30 |
| `docs/index.html` | 17 |
| `examples/flagship-grid.html` | 16 |
| `examples/flagship-noir.html` | 14 |
| `examples/operations-console.html` | 11 |
| `examples/pricing.html` | 7 |
| `examples/saas-workflows.html` | 7 |
| `examples/business.html` | 6 |
| `examples/console.html` | 5 |
| `examples/symbols.html` | 5 |
| `examples/terminal.html` | 4 |
| `docs/catalog.html` | 2 |
| `examples/native-apis.html` | 1 |
| Other audited pages | 0 |
| **Total** | **162** |

The audit's incomplete results may reflect gradients, pseudo-elements or
complex backgrounds; they are **unresolved** rather than passed or failed
contrast measurements. Prioritize the Blocks, geometry, documentation and
flagship hero surfaces for a real painted-background assessment. Manual
accessibility review, actual browser zoom and assistive-technology evidence,
naming clearance and authenticated distribution ownership all remain open.
**Do not freeze, tag or publish alpha.5 solely based on this evidence.**

## Verified source snapshot: `038a24d` (November 15, 2026)

This **point-in-time source audit** includes PR #68 (the native CSS
flow/high-contrast corrections) and the Blocks/Assets gallery changes through
`038a24dd626c3299a10abd0de8ff6890adc7ea3d`. It is not a verdict on commits
merged afterward, the published alpha.4 assets, or the future alpha.5 release.

- Reproducible CSS, API metadata, generated LLM reference and optional
  ecosystem adapters: **PASS** with `--check`. Full Python stdlib suite:
  **311 passed**. A public-only Cloudflare site build included **114 allowlisted
  files**; the 39-file alpha.5 candidate ZIP packaged successfully **without
  publishing, freezing, or tagging a release**.
- The developer-only Linux Playwright **1.65.2** matrix covered
  **22 pages × 3 viewport widths × 3 engines = 198 passing browser cases**
  in Chromium, Firefox and WebKit, including gallery-specific keyboard/popover
  assertions. The accompanying **88 enlarged-root-font reflow cases per engine
  (264 total)**, **two Chromium forced-colors-emulation tests**, and focused
  seven-theme native CSS tests in all three engines also passed. This stress
  testing is not actual browser zoom or OS-native high contrast. Tests changed
  no consumer runtime dependencies.
- A separate pinned **axe-core 4.10.3** audit of **21 pages** found
  **zero confirmed automated WCAG-tagged violations**, with **11 incomplete
  color-contrast rule results containing 129 unresolved nodes**. SHA-256 of
  the repository audit harness (`tests/axe_audit.py` at audited commit
  `038a24d`): `3f94a5672d13c39b511131386bc70abba43b81cba37a672f62b382c8908ddd58`.
  SHA-256 of the separately downloaded axe-core 4.10.3 JavaScript payload
  used by that harness: `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`.
  Incompletes are not passing contrast measurements or proven defects.
- GitHub showed Cloudflare Pages, build, deploy, and build-status checks
  successful for the audited commit. **A real exact-head Woodpecker pipeline
  is still unverified.** PR #68's CodeRabbit check was cancelled after the PR
  closed; this was not an independently completed CodeRabbit approval.

| Page | Unresolved axe color-contrast nodes |
| --- | ---: |
| `docs/blocks.html` | 38 |
| `examples/geometry-terminal.html` | 30 |
| `docs/index.html` | 14 |
| `examples/operations-console.html` | 11 |
| `examples/pricing.html` | 7 |
| `examples/saas-workflows.html` | 7 |
| `examples/business.html` | 6 |
| `examples/console.html` | 5 |
| `examples/symbols.html` | 5 |
| `examples/terminal.html` | 4 |
| `docs/catalog.html` | 2 |
| Remaining 10 audited pages | 0 |
| **Total** | **129** |

**Manual prioritization:** inspect the Blocks hero and featured content,
each shaped geometry surface, the documentation hero and the operations
console first. These four pages account for **93/129** unresolved targets.
Record the effective painted background including gradients and pseudo-elements,
foreground color, theme, viewport, interaction state, a screenshot and measured
contrast; do not automatically dismiss an axe incomplete because a CSS token pair
is accessible in isolation.

**Release gates that this evidence does not close:** true 200% and 400% browser
zoom, NVDA/VoiceOver screen-reader operation, native OS high-contrast mode,
manual review of the 129 inconclusive nodes, and trademark/name clearance.
Root-font reflow stress and forced-colors *emulation* are useful but are not
substitutes. Do **not** tag/freeze/publish alpha.5 from these results alone.

## Historical post-merge snapshot: `b19c331` (November 14, 2026, Brasília)

This was the latest **executed** audit snapshot at that time, after the merges of
[PR #14](https://github.com/dporkka/syntyr-css/pull/14) and
[PR #22](https://github.com/dporkka/syntyr-css/pull/22).
The published alpha.4 CSS remains immutable; alpha.5 is not yet published.

- Deterministic build: **PASS**; Python contracts: **155 passed**.
- Pinned Playwright 1.64.1 Linux container: **23 Chromium interaction
  checks**, **16 public pages × 3 viewports × 3 browser engines** (144 cases),
  **64 reflow cases × 3 browser engines** (192 cases), and docs-only theme
  editor checks: **PASS**. These are automated tests, not actual browser zoom
  or assistive-technology operation.
- axe-core 4.10.3: **0 confirmed violations** across 16 pages; **345
  unresolved `color-contrast` target entries on 13 pages**. These have
  **not** been adjudicated as passes and do not establish WCAG compliance.
- Cloudflare Pages public deployment: current CSS, docs, new demo, and
  immutable release asset matched locally generated bytes for this exact
  main commit in sampled SHA-256 comparisons; private tests/business/.env
  paths returned HTTP 404. **63 allowlisted public assets** built locally.
- GitHub/Cloudflare build and deploy checks succeeded on `b19c331`; an
  independently executed Woodpecker pipeline on this exact commit was **not
  verified**.

| Page | Inconclusive color-contrast targets |
| --- | ---: |
| `index.html` | 42 |
| `docs/index.html` | 122 |
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
| `examples/saas-workflows.html` | 7 |
| `examples/minimalist-patterns.html` | 6 |
| `examples/design-states.html` | 0 |
| **Total** | **345** |

These are axe-core *incomplete* element entries rather than proven defects.
Regenerate the exact selector-level evidence with:

```sh
python3 tests/axe_audit.py --axe-file /tmp/axe.min.js \
  --report /tmp/syntyr-axe-manual-review.json
```

The earlier pixel-sampling results below were collected against `4a623d0`,
**not** `b19c331`. They cannot be transferred to the additional 20 findings
or used to close the current 345 targets. Prioritize gradient/pseudo-element
cases, the previously narrow 4.65:1 margin, keyboard and contrast states,
and text-overflow cases in horizontally scrollable tables.

### Manual-only release requirements still open

Real 200% and 400% browser zoom; actual screen-reader navigation with named
assistive technologies and browser versions; native OS high-contrast/forced
colors; keyboard workflows in a representative integrated application; and
review/adjudication of the 345 inconclusive contrast targets. Do not describe
these automated results as a certification.

## Historical comparison: `4a623d0` baseline

The November 14 (Brasília) baseline `4a623d0`, incorporating
[PR #21](https://github.com/dporkka/syntyr-css/pull/21), was independently
tested before subsequent PRs merged. Its historical color-contrast counts and
pixel samples are retained below; they should not be confused with the
newer post-merge report.

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

Earlier automated browser evidence covered **126 viewport cases** across Chromium/Firefox/WebKit and **168 enlarged-text reflow cases** on a historical commit. These figures are not the latest branch coverage. The Chromium forced-colors primary-link screenshot and focus tests passed for all seven palettes in that snapshot. None of these checks substitute for native Windows High Contrast or other OS-level modes, real browser zoom, or a screen reader.

## Remaining release checklist

- [ ] Measure or adjudicate each of the **162 unresolved** text/background element entries in the latest 28-page source audit above. The 345-entry and 325-entry figures below describe earlier commits and are historical, not the current review queue.
- [ ] Test keyboard-only navigation, native dialog/popover focus, table regions, disclosure and form semantics in a representative real app.
- [ ] Perform real assistive-technology testing with NVDA, JAWS, VoiceOver or Orca and record evidence.
- [ ] Test true 200% and 400% browser zoom on supported browsers; verify navigation, reflow and target visibility.
- [ ] Check actual OS forced-colors/high-contrast and reduced-motion settings.
- [x] Record browser versions used for automated testing (not a permanent
  support guarantee). The **current** 16-page matrix and 64-case/engine
  reflow run used Linux `mcr.microsoft.com/playwright/python:v1.64.1-noble`
  with Playwright Python 1.64.1: Chromium **156.0.8078.4**, Firefox
  **157.0**, and WebKit **27.2**. Versions were read directly using
  `browser.version` from the same pinned image.
- [x] Preserve the **historical** 14-page baseline's separate browser
  versions: Chromium 159.0.8154.6, Firefox 159.0, WebKit 27.2 in the
  Playwright 1.65.2 image. These do not describe the newer 1.64.1 run.
- [ ] Establish browser support versions and unresolved exceptions before a stable release.

A passing axe-core run alone is **not** sufficient to claim WCAG conformance.
