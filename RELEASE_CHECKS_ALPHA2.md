# Cyberline v0.3.0-alpha.3 — release-candidate evidence

Status: **unreleased**, [PR #2](https://github.com/dporkka/cyberline-css/pull/2).
Validated 2026-11-14. The published `v0.3.0-alpha.2` tag is a distinct Studio/CLI release and does not contain this seven-theme candidate.
This document does not claim full production readiness.

## Automated verification

| Gate | Result |
| --- | --- |
| Standard-library unit/distribution contracts | PASS — 51/51 |
| Chromium interaction tests | PASS — 17/17 (native popover/dialog, keyboard, forms, responsive layouts, forced-color border) |
| Chromium browser matrix | PASS — 10 pages × 320, 390, 1280 CSS px (30 cases) |
| Firefox browser matrix | PASS — 10 pages × 3 widths (30 cases) |
| WebKit browser matrix | PASS — 10 pages × 3 widths (30 cases), isolated Playwright container |
| Seven-theme nesting and utility contracts | PASS — light inside dark, dark inside light, geometry isolation, utility precedence |
| axe-core 4.10.3 tagged WCAG 2/2.1/2.2 A/AA | 0 automated violations across 10 pages; **9 inconclusive checks requiring manual review** |
| CSS parsing with developer-only tinycss2 | PASS — 7 distribution files, zero top-level syntax errors |
| Deterministic build and release packaging | PASS — `scripts/build.py --check` and reproducible 11-file ZIP (CSS, terminal palette data, MIT license, docs) |
| Core stylesheet | 4,684 bytes gzip (limit 5,120) |
| Backwards-compatible core + effects | 5,102 bytes gzip (legacy limit 5,120) |
| Full CSS bundle | 6,957 bytes gzip (limit 8,192) |
| Library runtime JavaScript / npm dependencies | 0 / 0 |

The isolated WebKit run uses Python Playwright 1.64.1 and the WebKit browser
provided in the cached official test-only
`mcr.microsoft.com/playwright:v1.64.0-noble` image. Browser tooling is not
shipped to consumers. Core/semantic/effects/recipes/utilities can be self-hosted
without an application build step.

The integration includes Studio SaaS and business layouts, an optional browser
terminal recipe, a three-palette ANSI example, and seven interchangeable CSS
themes. The existing premium Console Kit remains an illustrative, non-purchasable
concept. No paid assets or proprietary CSS are included.

## Reviewed defects with regression coverage

- Nested theme text previously inherited the outer theme's computed foreground
  even though CSS custom property values changed.
- Grid/Noir geometry inherited a parent theme's radius and cut variables.
- `cy-u-center` overrode `cy-u-between` despite their documented composition.
- The theme gallery exposed an invalid `aria-label` on a plain div and inert
  decorative buttons; its controls now navigate to the component documentation.

The corresponding focused tests failed on the original implementation and
passed after the fixes. The browser matrix checks computed theme foregrounds,
native `color-scheme`, geometry and utility precedence.

## Manual gates still open

- Review the 9 inconclusive axe results, especially text over gradient
  backgrounds, and inspect contrast of controls in all interaction states.
- Verify representative pages with actual screen readers and keyboard-only
  navigation, including nested semantic forms and data tables.
- Test real 200% and 400% browser zoom. A 320px CSS viewport is **not** the
  equivalent of real zoom testing.
- Visually inspect forced-colors and high-contrast behavior across all seven
  palettes rather than relying on a single automated border smoke test.
- Review the supported browser baseline, provisional Cyberline trademark,
  and eventual separate commercial license before making marketing or v1 claims.

No new GitHub tag or production release is authorized by this document.
