# Cyberline CSS accessibility validation

**Status:** experimental alpha; not a WCAG certification or professional audit.

## What is and is not covered

- Source contracts: native HTML, semantic labels, opt-in scoping, predictable
  focus-visible outline, reduced-motion support, and forced-color hooks.
- Real browser matrix: Chromium, Firefox, and WebKit on desktop/mobile viewport widths,
  testing navigation, table semantics, native popover, disclosure, and overflow.
- Automated accessibility: axe-core WCAG 2.0/2.1/2.2 A/AA tagged checks on the
  showcase, component gallery, and seven additional pages. The tool may return
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
python3 tests/reflow_test.py --browsers chromium firefox webkit
```

For a pinned axe-core 4.10.3 audit, provide the checker at test time. No
JavaScript file is shipped to application consumers:

```sh
curl -fsSL https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js -o /tmp/axe.min.js
python3 tests/axe_audit.py --axe-file /tmp/axe.min.js
```

For reproducible WebKit on an isolated testing host with Podman or Docker, clone
the repository to a directory that the container can read and run:

```sh
podman run --rm --shm-size=1g -v "$PWD":/work:ro,Z -w /work \
  mcr.microsoft.com/playwright/python:v1.64.1-noble \
  bash -lc 'python3 -m pip install -q playwright==1.64.1 && \
    python3 tests/browser_matrix.py --browsers webkit'
```

The image supplies browser binaries and native dependencies, not the Python
Playwright package. This test-only container may download packages and should
be run against trusted code. The `:Z` mount flag is Podman/SELinux-specific;
adjust for Docker hosts. Keep the Python and browser versions aligned.

The remote URL is part of a **developer-only test**, not a browser runtime
dependency. Pin the checker release, review its MIT license, and verify its
provenance if incorporating it into build infrastructure.

## Interpretation and known limitations (2026-11-14)

- Chromium and Firefox: **nine pages × three viewport widths** (320, 390,
  1280px), keyboard focus, popover and disclosure checks passed on Fedora 44.
- WebKit: those nine pages and three viewports passed in the separate Linux
  CI host, with `mcr.microsoft.com/playwright/python:v1.64.1-noble` and
  `playwright==1.64.1`. The tested integrated branch included the new
  Studio, SaaS, business and browser terminal examples.
- Total standard browser matrix: **81** page-and-viewport checks across
  Chromium, Firefox and WebKit.
- Enlarged-text stress: **108** checks on the nine pages (320/390px viewport
  and 100%/150%/200% root-font sizes). The test caught and drove a fix for
  narrow-layout overflow and subsequently detected clipped buttons in the
  new Studio business example. Both problems are fixed in alpha.2.
- These artificial layout/text measurements **are not equivalent** to real
  browser zoom at 200% or 400%. Perform real zoom and screen-reader manual
  tests before claiming WCAG accessibility.
- The Chromium axe-core 4.10.3 WCAG-tagged scan on nine pages recorded
  **zero confirmed violations and eight incomplete checks** for manual review.
  Zero automated violations is not an accessibility certification.
- Native HTML `commandfor="…" command="show-modal"` support varies by
  browser. Critical flows should offer supported fallbacks/alternative
  routes in production applications.

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

## v0.3.0-alpha.3 candidate regression evidence (2026-11-14)

The expanded matrix covers ten pages, including the new seven-theme gallery,
Studio SaaS, business and browser-terminal examples. Chromium, Firefox and
WebKit each passed 10 pages × 3 CSS viewport widths (320, 390, 1280), for
**90 automated page/viewport cases**. Tests cover light/dark nested foregrounds,
geometry token isolation and composable utilities. A separate 17-test Chromium
suite covers native interactions and layout.

axe-core 4.10.3 returned **zero automated WCAG A/AA violations** across ten
pages, with **nine inconclusive checks**, primarily where decorative gradients
make automated color contrast indeterminate. Human inspection is still required.

For reproducible build sizes, distribution checks and remaining release gates,
see [the alpha.3 candidate evidence](../RELEASE_CHECKS_ALPHA3.md).
