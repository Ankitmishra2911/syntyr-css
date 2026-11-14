# SYNTYR v0.3.0-alpha.4 — release-candidate evidence

Status: **unreleased**, [PR #2](https://github.com/dporkka/syntyr-css/pull/2).
Validated 2026-11-14. The published `v0.3.0-alpha.3` tag is the SYNTYR brand migration release; this seven-theme alpha.4 candidate is not published.
This document does not claim full production readiness.

## Automated verification

| Gate | Result |
| --- | --- |
| Standard-library unit/distribution contracts | PASS — 64/64 |
| Chromium interaction tests | PASS — 17/17 (native popover/dialog, keyboard, forms, responsive layouts, forced-color border) |
| Enlarged-text layout reflow | PASS — 44/44 cases in each of Chromium, Firefox, WebKit (11 pages × 4 width/scale conditions × 3 engines = 132 cases) |
| Chromium browser matrix | PASS — 11 pages × 320, 390, 1280 CSS px (33 cases) |
| Firefox browser matrix | PASS — 11 pages × 3 widths (33 cases) |
| WebKit browser matrix | PASS — 11 pages × 3 widths = 33/33 cases, exact source commit `39e9def`, isolated Playwright container |
| Chromium forced-colors primary controls | PASS — seven theme labels visibly rendered in light palette; dark system palette checked visually; keyboard focus remains visible |
| Seven-theme nesting and utility contracts | PASS — light inside dark, dark inside light, geometry isolation, utility precedence |
| axe-core 4.10.3 tagged WCAG 2/2.1/2.2 A/AA | 0 automated violations across 11 pages; **9 color-contrast inconclusive rule results covering 270 elements**, all requiring review |
| CSS parsing with developer-only tinycss2 | PASS — 14 distribution files, zero top-level syntax errors |
| Deterministic build and release packaging | PASS — `scripts/build.py --check` and reproducible 18-file ZIP (CSS, terminal palette data, MIT license, docs) |
| Core stylesheet | 4,691 bytes gzip (limit 5,120) |
| Backwards-compatible core + effects | 5,110 bytes gzip (legacy limit 5,120) |
| Full CSS bundle | 6,962 bytes gzip (limit 8,192) |
| Library runtime JavaScript / npm dependencies | 0 / 0 |

The eleven-page WebKit matrix and reflow tests passed on exact source commit
`39e9def` in the official test-only Playwright container, with Python
Playwright 1.64.1. Across Chromium, Firefox and WebKit, 99 page/viewport
cases and 132 enlarged-text reflow cases passed. Browser tooling is not shipped
to consumers. Core, semantic, effects, recipes and utilities can be self-hosted
without an application build step.

The integration includes Studio SaaS and business layouts, an optional browser
terminal recipe, a three-palette ANSI example, an opt-in Vertigo admin skin,
an isolated Hugo preview experiment, and seven interchangeable CSS themes.
The existing premium Console Kit remains an illustrative, non-purchasable
concept. No paid assets or proprietary CSS are included.

## Reviewed defects with regression coverage

- Nested theme text previously inherited the outer theme's computed foreground
  even though CSS custom property values changed.
- Grid/Noir geometry inherited a parent theme's radius and cut variables.
- `cy-u-center` overrode `cy-u-between` despite their documented composition.
- The theme gallery exposed an invalid `aria-label` on a plain div and inert
  decorative buttons; its controls now navigate to the component documentation.
- A plain nested theme section could change foreground color without providing a
  corresponding background. The base theme boundary now supplies both, while
  component surface rules retain their higher-priority backgrounds.

Additional screenshot-based forced-colors tests reproduced invisible primary-action
labels in all seven palettes; system ButtonFace/ButtonText styling restored the
rendered words without adding runtime JS. The new optional Vertigo example also
received a semantic group role after a failing contract test.

The corresponding focused tests failed on the original implementation and
passed after the fixes. The browser matrix checks computed theme foregrounds,
native `color-scheme`, geometry and utility precedence.

## Manual gates still open

- Review the nine inconclusive axe groups covering **270 elements**, especially
  text over gradients. No WCAG conclusion may be drawn from an inconclusive result.
  See [the element-level manual review plan](docs/accessibility-alpha4-review.md).
- Verify representative pages with actual screen readers and keyboard-only
  navigation, including nested semantic forms and data tables.
- Test real 200% and 400% browser zoom. Headless and isolated headed Chromium
  did not respond to automation zoom shortcuts or profile defaults; narrowing
  the viewport and enlarging root font size are **not real browser zoom**.
- Inspect native Windows High Contrast themes and actual screen-reader navigation.
  Chromium forced-colors simulation was checked in light and dark system palettes;
  that is not a substitute for operating-system assistive technology.
- Review the supported browser baseline, provisional SYNTYR trademark,
  and eventual separate commercial license before making marketing or v1 claims.

No v0.3.0-alpha.4 GitHub tag or release has been created by this work.
