# SYNTYR v0.3.0-alpha.5 — integrated release candidate

**Status: unreleased.** This candidate ports the seven-theme/utility feature work from [PR #2](https://github.com/dporkka/syntyr-css/pull/2) onto the **SYNTYR-only `syn-` namespace** introduced in the published [alpha.4 release](https://github.com/dporkka/syntyr-css/releases/tag/v0.3.0-alpha.4). It must not recreate former CSS aliases or overwrite that release.

Validation date: November 14, 2026. Results below were verified on the candidate working tree. A fresh clone and exact-head validation will follow the integration commit. These results do not establish a WCAG conformance claim or v1 compatibility guarantee.

## Automated checks

| Gate | Candidate result |
| --- | --- |
| Python standard-library contracts | **94 passed** |
| Browser matrix | **117 passed** — 13 pages × 3 viewport widths × Chromium, Firefox and WebKit |
| Enlarged-text reflow | **156 passed** — 13 pages × 4 width/font-size combinations × 3 engines |
| Chromium simulated forced colors | **2 passed** — seven primary actions retain readable labels and visible keyboard focus |
| axe-core 4.10.3 A/AA-tagged audit | **Zero confirmed automated violations** across 13 pages; 11 inconclusive contrast rule results covering 310 elements |
| CSS generation | Deterministic, Python standard library only |
| CSS distributions | 8 current SYNTYR files, no retired files or namespace |
| SYNTYR core | **4,656 bytes gzip** (budget 5,120) |
| Core + optional effects | **4,978 bytes gzip** (budget 5,120) |
| Full bundle | **7,746 bytes gzip** (budget 8,192) |
| Geometry module | 992 bytes gzip, opt-in |
| Utilities module | 465 bytes gzip, opt-in |
| Runtime JavaScript / npm dependencies | **0 / 0** |

Browser matrix and reflow checks were run in the official test-only Playwright v1.65.2 container. Chromium additionally exercised keyboard focus, native controls, nested light/dark theme boundaries, computed geometry values and utility composition. The separate utilities sheet is included in `syntyr.all.css` but absent from `syntyr.core.css`. Existing geometry, operations console, Vertigo skin, marketing demos and terminal example remain intact.

## Bugs found and fixed

1. Ported theme tests used an obsolete JavaScript dataset property, preventing nested-theme overrides from activating. The probes now set `dataset.synTheme`.
2. Chromium painted all seven theme-gallery primary action labels as opaque rectangles under simulated forced colors. Using native `ButtonFace`/`ButtonText` restored readable labels; regression screenshots now pass.
3. An existing Vertigo summaries container lacked a grouping role despite having an accessible label; it now has `role="group"`.
4. The package and browser lists were reconciled for the eighth utilities distribution and unique coverage of all thirteen pages.
5. Source-comment compaction preserved the legacy 5 KiB core-plus-effects size target without a runtime toolchain or CSS declaration changes.

## Cloudflare publishing integrity

The candidate incorporates the independently merged Cloudflare Pages build,
accessible navigation primitives, and optional JavaScript documentation theme editor.
The static-site builder now explicitly publishes the new theme gallery and
utilities file, without exposing development files. Its tests verify the
**existing immutable alpha.4 snapshot** instead of requiring the alpha.5
candidate to have already been released. The existing published alpha.4
assets and checksums were left unchanged. The docs-only theme editor is not
a runtime dependency of the CSS library.

## Post-merge verification (November 14, 2026; main `6109b79`)

The original candidate figures above are preserved as historical evidence.
A new head-level verification includes the additional SaaS workflows page and
passes **126 browser** and **168 enlarged-text reflow** cases across Chromium,
Firefox and WebKit using the Playwright 1.65.2 Linux image. The current
Chromium axe-core 4.10.3 scan reports **0 confirmed violations, 11 incomplete
rules and 325 review targets**; the prior 310 count is superseded for current
main. The manual accessibility gates below remain open. Details and a
reproducible JSON review-target command are in
`docs/accessibility-alpha5-review.md`.

## Release gates still open

- Manually evaluate **325 current inconclusive text/background contrast targets**, especially layered gradients and pseudo-elements.
- Test keyboard and real screen-reader navigation (NVDA/JAWS/VoiceOver/Orca) on representative pages.
- Verify genuine 200% and 400% browser zoom, not just simulated text enlargement or narrow viewports.
- Check native operating-system high-contrast modes and establish the supported browser/version matrix.
- Complete the separate SYNTYR naming-clearance review before commercial branding or monetization.

These are not reasons to discard tested code, but they are reasons **not to label it production-certified**. No alpha.5 tag or release has been published by this work.
