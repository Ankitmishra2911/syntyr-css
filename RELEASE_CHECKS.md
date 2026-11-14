# Syntyr CSS v0.3.0-alpha.4 — release verification

**Checked November 14, 2026.** Integrated candidate: `integrate/reflow-alpha2`,
including Studio/CLI/business layouts from `main` and the narrow-text reflow
fix from `4e6e8bc`. This report describes executed checks; it does not
constitute a WCAG certification.

| Check | Result |
| --- | --- |
| CSS build matches deterministic committed output | PASS |
| Python source/release contract suite | **45/45 PASS** |
| Chromium interactive/browser unit suite | **17/17 PASS** |
| Browser matrix: 9 pages × 3 widths × 3 engines | **81/81 PASS** |
| Enlarged-text stress: 9 pages × 4 viewport/text settings × 3 engines | **108/108 PASS** |
| axe-core 4.10.3 WCAG A/AA-tagged scan on 9 pages | **0 confirmed violations; 8 incomplete checks** |
| Core CSS gzip | **4,187 bytes** (budget 5,120) |
| All-in-one CSS gzip | **6,177 bytes** (budget 8,192) |
| Runtime JavaScript | **0 bytes** |
| Runtime dependencies | **0** |

## Executed environments

- Chromium system browser and Playwright Firefox ran on Fedora 44.
- WebKit ran in the official Playwright Python container
  `mcr.microsoft.com/playwright/python:v1.64.1-noble`, with
  `playwright==1.64.1`, on a separate Linux CI host.
- Browser matrix: showcase, gallery, free console, resource index, pricing,
  Console Kit research page, SaaS, business and terminal examples at 320,
  390 and 1280 px.
- Enlarged-text suite: those same nine pages, at 320/390 px and 100%, 150%
  and 200% root-font scales. The new Studio business page initially clipped
  buttons at 320px + 200% text. It now passes after using a zero-minimum
  grid track for its mobile hero.
- axe-core: automated inspection in Chromium on Fedora. Eight unresolved
  `incomplete` outcomes are **not** passing assertions.

## Unreleased branch follow-up (November 14, 2026)

The historical table above describes the alpha.4 release candidate, **not** the
subsequent navigation and theme-editor changes. On the isolated improvement
branch, the latest local verification is:

- Source and generated CSS match (`python3 scripts/build.py --check`).
- Python suite: 78 passing tests (including new navigation, loading, theme-editor and internal-link contracts).
- Chromium and Firefox: 13 pages × 3 widths each, including native focus and navigation checks, passed.
- Standalone docs-only theme editor: 3 Chromium widths, theme switching, contrast warning, reset and scope tests passed.
- Core CSS: 4,634 gzip bytes (budget 5,120); all modules: 7,475 gzip bytes (budget 8,192).
- WebKit **not rechecked** for these changes: the Gertrude host lacks required WebKit system libraries. Run the existing containerized WebKit matrix before a stable release.
- No JavaScript is added to the distributed stylesheets or the main gallery. The theme editor has one optional, local, standalone script.

## Remaining release gates

- **Actual browser zoom** at 200%/400%, and manual screen-reader checks
  (NVDA or VoiceOver; Orca where applicable). Artificially enlarging the
  root font size is a useful stress test but not an equivalent substitute.
- Accessibility review of axe-core inconclusive findings, visual
  high-contrast/forced-colors appearance, older browsers, and production
  workflows with form validation.
- Trademark/name clearance in the United States and Brazil:
  [preliminary name screen](business/syntyr-trademark-screen.md). The word
  Syntyr remains **provisional**. No legal availability conclusion is drawn.
- Demonstrated willingness to pay: ten design-partner interviews planned,
  zero interviews and zero paid commitments reported so far.
- The proposed $59 Console Kit is **not offered for sale**. Its future
  commercial screen templates would have separately authored contents and
  licenses. All existing code, themes, demo screens and recipes are MIT.

The deterministic `scripts/package_release.py` ZIP allowlists the MIT
LICENSE, README, distribution instructions, seven CSS files and terminal
palette JSON. No unrelated development, business planning, or credentials
are included.
