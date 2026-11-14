# Cyberline alpha.3 — accessibility review evidence and open gates

Review date: 2026-11-14. This is a verification record for the PR #2
development branch, not WCAG certification. The published alpha.2 tag is
separate. Automated audits can identify failures; inconclusive results are
**not passes**.

## axe-core 4.10.3 findings

The eleven-page WCAG 2.0/2.1/2.2 A/AA tagged audit returned **zero confirmed
automated violations**. It returned **nine inconclusive color-contrast rule
groups covering 270 element instances**:

| Page | Inconclusive elements |
| --- | ---: |
| `index.html` | 42 |
| `docs/index.html` | 97 |
| `examples/console.html` | 33 |
| `examples/resources.html` | 45 |
| `examples/pricing.html` | 8 |
| `docs/console-kit.html` | 14 |
| `examples/saas.html` | 0 |
| `examples/business.html` | 6 |
| `examples/terminal.html` | 4 |
| `examples/themes.html` | 21 |
| `examples/vertigo-admin.html` | 0 |
| **Total** | **270** |

Axe could not determine effective background paint for these text nodes,
frequently because their ancestors have layered gradients. Theme palette
token-to-solid-surface contrast has separate unit coverage, but does **not**
clear composited gradient text, dynamic backgrounds or stateful UI.

**Manual procedure:** inspect each page in its light and dark contexts. For
the nine groups, inspect every implicated foreground against the *darkest or
lightest actual background region behind the glyphs*. Record the measured
WCAG contrast, test regular text at 4.5:1, large text at 3:1, and essential
non-text controls/boundaries at 3:1. Test hover, focus, disabled and selected
states where applicable. Save device, browser version, element selector and
contrast measurements as evidence.

## Confirmed defects reproduced and fixed

- In Chromium simulated forced-colors mode, all seven gallery primary-link
  labels rendered as solid white bars. A screenshot-pixel test failed for all
  seven themes before the fix. Switching the component's forced-color
  primary state from `Highlight/HighlightText` to system
  `ButtonFace/ButtonText` restored readable label glyphs. The focused
  screenshot and keyboard-outline tests both pass.
- Light and dark *simulated* Chromium forced-color palettes were visually
  inspected for a representative Grid button. Both show readable text and a
  distinct control border. These simulations do not certify Windows High
  Contrast or other OS implementations.
- The new optional Vertigo page had a generic `div` with `aria-label` but no
  valid grouping role. An existing semantic contract test caught it; adding
  `role="group"` made the test pass.

## Responsive tests versus real browser zoom

An 11-page browser matrix checks CSS widths 320, 390 and 1280. The enlarged
font-size reflow test checks four viewport/font conditions per page; neither
substitutes for browser zoom. Experiments with Ctrl-plus in headless Chromium,
isolated headed Chromium under Xvfb, and default zoom preferences did not
change the reported zoom/viewport. **True 200%/400% zoom remains unverified.**
To close the gate, use browser UI in a genuine desktop session, record browser
zoom percentage, measure effective layout width and check clipping and
navigation on every representative page.

## Outstanding release gates

- [ ] Inspect and measure all 270 inconclusive contrast element instances,
      including gradient extremes and component states.
- [ ] Use actual NVDA/JAWS/VoiceOver/Orca sessions with the relevant browser,
      testing landmarks, skip links, links/forms/tables and dialog focus.
- [ ] Conduct genuine 200%/400% browser zoom tests and record reflow,
      content visibility and keyboard access.
- [ ] Inspect simulated *and OS-native* forced-colors modes across browsers,
      plus dark and light operating-system palettes.
- [ ] Resolve provisional Cyberline name/trademark clearance before paid
      brand or premium-product launch. See `business/trademark-screen.md`.
- [ ] Choose supported-browser and accessibility release criteria before
      labeling alpha.3 production-ready or publishing a commercial offering.

The current MIT CSS core remains zero-runtime-JavaScript and requires no npm
package to use. Playwright and axe-core above are developer-only checks.
