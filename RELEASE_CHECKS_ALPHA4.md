# SYNTYR v0.3.0-alpha.4 — integrated release-candidate validation

Status: **unreleased**. This is evidence for [PR #2](https://github.com/dporkka/syntyr-css/pull/2), integrating its seven-theme and utility work with the already merged geometry/terminal PR #6 and operations-dashboard PR #7. The published alpha.3 tag is unchanged.

Verification date: November 14, 2026. These results were collected on the integrated candidate worktree; a fresh-clone/head verification is required after publishing the integration commit. Passing automated checks does not establish WCAG conformance, browser version support policy, or production maturity.

## Automated results

| Gate | Integrated candidate result |
| --- | --- |
| Python standard-library contracts | PASS — 85 tests (all retained from main and the theme branch, plus integration contracts) |
| Browser matrix | PASS — 117 cases (13 pages × 3 widths × Chromium, Firefox, WebKit) |
| Enlarged-text reflow | PASS — 156 cases (13 pages × 4 width/font settings × 3 engines) |
| Chromium simulated forced-colors | PASS — 2 screenshot/focus tests across seven themes |
| axe-core 4.10.3, WCAG A/AA-tagged rules | Zero confirmed violations across 13 pages; **11 inconclusive contrast results involving 310 elements** |
| Deterministic CSS generation | PASS — 16 SYNTYR and legacy CSS distribution files |
| Core CSS | 4,731 bytes gzip (5,120-byte maximum) |
| Legacy core + effects CSS | 5,048 bytes gzip (5,120-byte maximum) |
| Full CSS bundle | 7,803 bytes gzip (8,192-byte maximum) |
| Geometry module | 991 bytes gzip, optional |
| Utility module | 464 bytes gzip, optional |
| Runtime JavaScript and runtime packages | Zero |

The three-engine browser and reflow tests used the test-only official Playwright Python v1.65.2 container. Browser tests exercised native popovers/disclosures, keyboard focus, theme boundaries, theme-specific foregrounds and geometry, disabled controls, and the operations dashboard. The CSS library itself needs no Python/Playwright installation.

The initial integrated candidate failed on two verifiable issues: an old three-theme assertion rejected the Minimal theme, and the core-plus-effects distribution exceeded its 5 KiB limit. Both received regression coverage and fixes. Source-comment cleanup reduced compressed bytes without changing CSS declarations or adding a minifier.

## Preserved integration behavior

- Grid, Noir, Studio, Industrial, Terminal, Corporate, and Minimal expose consistent scoped tokens, including nested light/dark boundaries.
- Optional geometric frames and finite utilities are independently loadable; both are included in `syntyr.all.css`, but not `syntyr.core.css`.
- SYNTYR and Cyberline distributions are byte-identical per module. Legacy `cy-` class and token names are preserved.
- The MIT operations console, geometry/terminal demo, native terminal ANSI palette example, optional Vertigo skin, and Hugo proof-of-concept are retained.
- The gallery contains all distinct examples, and browser, enlarged-text, and axe test matrices cover each exactly once.

## Remaining release gates

1. Manually measure the 310 inconclusive text/background contrast elements, especially layered gradients and decorative pseudo-elements. See [the element-by-element inventory](docs/accessibility-alpha4-review.md).
2. Run actual NVDA, Orca, VoiceOver or other relevant screen-reader checks and keyboard-only flows across real browsers.
3. Test genuine browser zoom at 200% and 400%; changing root font size or viewport width is not equivalent.
4. Review operating-system high-contrast behavior and set a supported-browser/version policy.
5. Complete name clearance and any independent premium licensing decisions before a commercial launch.

**No alpha.4 release or GitHub tag has been created by this integration.**
