# Cyberline CSS accessibility validation

**Status:** experimental alpha; not a WCAG certification or professional audit.

## What is and is not covered

- Source contracts: native HTML, semantic labels, opt-in scoping, predictable
  focus-visible outline, reduced-motion support, and forced-color hooks.
- Real browser matrix: Chromium and Firefox on desktop/mobile viewport widths,
  testing navigation, table semantics, native popover, disclosure, and overflow.
- Automated accessibility: axe-core WCAG 2.0/2.1/2.2 A/AA tagged checks on the
  showcase, component gallery, and four examples. The tool may return
  **incomplete/manual-review** findings even with zero confirmed violations.
- Still needed: screen reader testing (NVDA + Firefox or Chrome, VoiceOver +
  Safari), actual browser zoom at 200% and 400%, touch target examination,
  interactive error states, font reflow and low-vision inspection.

## Reproduce the tests without installing production dependencies

Run the standard library contracts and optional Playwright checks:

```sh
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v

# Dev-only installation; choose your package/environment manager.
python3 tests/browser_test.py
python3 tests/browser_matrix.py --browsers chromium firefox webkit
```

For a pinned axe-core 4.10.3 audit, provide the checker at test time. No
JavaScript file is shipped to application consumers:

```sh
curl -fsSL https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js -o /tmp/axe.min.js
python3 tests/axe_audit.py --axe-file /tmp/axe.min.js
```

The remote URL is part of a **developer-only test**, not a browser runtime
dependency. Pin the checker release, review its MIT license, and verify its
provenance if incorporating it into build infrastructure.

## Interpretation and known limitations (2026-11-14)

- Chromium and Firefox: 6 pages × 3 viewport sizes, focus/popover/details
  smoke tests passed on Fedora 44.
- WebKit: fallback browser downloaded, but native libraries required by
  Playwright were missing on Fedora 44. **Blocked, not passed.** Run
  on an officially supported Playwright image/host before claiming coverage.
- An early axe-core audit identified incorrect `aria-label` use on palette
  swatch `div` elements, fixed by adding `role="group"`.
- Automated axe-core results include inconclusive/manual checks. Do not
  treat zero violations as proof that every component is accessible.
- Native HTML `commandfor="…" command="show-modal"` browser support
  varies by browser release. Critical flows should offer fallbacks in the
  application or use an always-accessible alternative.

## Manual checklist

1. Tab from the top of every page; test visible focus, no keyboard traps and
   skip-link behavior. Open and dismiss popovers/dialogs with keyboard.
2. At 200% and 400% zoom, inspect all content at narrow widths; no clipped
   actions, invisible labels or lost table information.
3. Test one screen reader per major browser engine for headings, landmarks,
   table captions, form labels and live status; document the actual device,
   browser version and assistive technology.
4. Force-colors/high-contrast: check panel separation, focus and form controls.
5. Disable animations in system settings and ensure nothing depends on motion.
6. Validate both the default Grid/Noir palettes and any project-specific
   token overrides for text contrast and non-text essential indicators.
