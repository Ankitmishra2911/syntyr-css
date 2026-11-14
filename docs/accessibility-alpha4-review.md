# SYNTYR alpha.4 accessibility review — open manual gates

Review date: November 14, 2026. This is the integrated [PR #2](https://github.com/dporkka/syntyr-css/pull/2) candidate and includes the previously merged geometry/terminal and operations-console examples. This document records test evidence **and remaining limitations**, not a WCAG certification.

## axe-core 4.10.3 findings

The 13-page WCAG 2.0/2.1/2.2 A/AA-tagged Chromium audit reported **zero confirmed automated violations** and **11 inconclusive color-contrast rule results covering 310 individual text elements**. Inconclusive does not mean passing.

| Page | Inconclusive elements |
| --- | ---: |
| `index.html` | 42 |
| `docs/index.html` | 100 |
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
| **Total** | **310** |

The inconclusive rule is `color-contrast`; axe cannot reliably infer the effective background paint behind text for layered gradients and pseudo-elements. Separate assertions verify solid-color theme tokens, but **those token tests do not resolve composited-background contrast**.

## Manual contrast procedure

Review each page under its intended theme and nested-theme boundaries. For each flagged text element, inspect foreground and actual pixels behind glyphs under the darkest and lightest part of gradients. Measure and record regular-text contrast (4.5:1), large-text contrast (3:1), and essential graphical control boundaries or non-text indicators (3:1), where applicable. Check focus, hover, selection and disabled states. Record the browser version, theme, selector, screenshot and measured ratio. Re-check after any relevant CSS changes.

## Browser and assistive technology coverage

The integrated branch passed **117 browser matrix cases** across Chromium, Firefox and WebKit at 320, 390 and 1280 CSS-pixel widths, and **156 enlarged-text reflow cases** across four width/font combinations per page. These are useful regression checks, but **neither is a real browser 200%/400% zoom test**.

Chromium's forced-colors simulation passed two screenshot/focus tests for seven-theme primary actions. This does not certify native Windows High Contrast or other operating-system high-contrast implementations.

Native popovers, disclosures, meaningful group roles, visible focus and table landmarks received automated checks. Manual NVDA/JAWS/VoiceOver/Orca navigation and actual physical-keyboard exploration remain outstanding.

## Release checklist

- [ ] Resolve all 310 inconclusive contrast elements with documented measurements or justified exceptions.
- [ ] Test representative navigation, forms, popover/dialog focus, tables, disclosures and the operations-console region using actual screen readers.
- [ ] Perform real 200% and 400% browser zoom checks with desktop browser controls; measure clipping and reflow.
- [ ] Validate OS-level high contrast and reduced-motion presentation.
- [ ] Record the browser/version support policy and retest in that exact support matrix.
- [ ] Update the evidence after each visual change; automated zero-violation counts do not close the manual gates.

No alpha.4 tag has been published by this review.
