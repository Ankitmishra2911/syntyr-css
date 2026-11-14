# Cyberline v0.3.0-alpha.2 — release-candidate evidence

Status: **unreleased**, PR [#2](https://github.com/dporkka/cyberline-css/pull/2).
Reviewed 2026-11-14. This is not a claim of full production readiness or a
newly published GitHub release. The published `v0.3.0-alpha.1` remains unchanged.

## Automated validation

| Gate | Result |
| --- | --- |
| Unit and distribution contracts | PASS — 38/38 |
| Chromium interaction tests | PASS — 14/14, including native popover/dialog, keyboard, container queries, forms and forced-color border |
| Chromium browser matrix | PASS — 7 pages × 320, 390 and 1280 CSS px (21 cases) |
| Firefox browser matrix | PASS — 7 pages × 3 widths (21 cases) |
| WebKit browser matrix | PASS — 7 pages × 3 widths (21 cases), verified in an isolated official Playwright container |
| Six-theme nested boundary checks | PASS — light-inside-dark and dark-inside-light foregrounds and color schemes, Grid geometry inside Terminal, utility precedence |
| axe-core 4.10.3 tagged WCAG 2/2.1/2.2 A/AA | 0 automated violations across 7 pages; **9 inconclusive checks requiring manual review** |
| CSS stylesheet parsing (tinycss2) | PASS — no top-level syntax errors across six distribution files |
| Reproducible distributions | PASS — `python3 scripts/build.py --check` |
| Source and ZIP release contract | PASS — deterministic 9-file ZIP including optional utilities |
| Core size | 4,388 bytes gzip, within 5,120-byte budget |
| All-module size | 5,319 bytes gzip, within 8,192-byte budget |
| Library runtime JavaScript / npm | 0 / 0 |

The WebKit matrix was run with Python Playwright 1.64.1 against the browser
binaries already present in the official
`mcr.microsoft.com/playwright:v1.64.0-noble` test-only image. The UI is
independent of the container and does not ship browser tooling.

The test sequence reproduced three real review findings before their fixes:
nested theme text could retain the outer foreground; Grid/Noir geometry
could inherit another theme's corner tokens; and `cy-u-center` could
override `cy-u-between`. Regression checks now cover these behaviors.

## Still required before a production-quality compatibility claim

- Inspect the **9 inconclusive axe checks**, primarily text against gradient
  backgrounds, and conduct a manual contrast review at relevant UI states.
- Verify keyboard and screen-reader interaction on representative real apps,
  including light and dark nested semantic forms.
- Check browser zoom at 200% and 400%; using a 320px viewport alone is **not**
  equivalent to real browser zoom.
- Review forced-colors appearance across all palettes, not just the smoke
  assertion that controls retain visible borders.
- Confirm browser support policy, trademark clearance of the provisional
  Cyberline name, and commercial license before paid assets ship.

Keep the MIT CSS core fully usable without premium components. The premium
Console Kit remains a non-purchasable concept, and the design-partner pilot
does not establish buyer demand.
