# SYNTYR alpha.5 — outstanding accessibility review

This November 14, 2026 post-merge verification of `main` commit `6109b79` accompanies the **unreleased alpha.5 seven-theme candidate**. It is not an accessibility certification. The published alpha.4 release remains unchanged.

## Automated axe-core findings

The fourteen-page post-merge audit with axe-core 4.10.3 and WCAG A/AA tags returned **zero confirmed violations** and **eleven inconclusive `color-contrast` rule results involving 325 individual targets**. Incomplete is not equivalent to passing.

| Page | Inconclusive elements |
| --- | ---: |
| `index.html` | 42 |
| `docs/index.html` | 115 |
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
| `examples/saas-workflows.html` | 0 |
| **Total** | **325** |

The 325 targets comprise 282 unresolved backgrounds involving gradients, 34
involving pseudo-elements, four too-short text cases, four non-text-only cases,
and one partially obscured element. They are **not** 325 proven defects.
Generate a reproducible node-by-node triage report (selectors, HTML snippets,
rule and failure summaries) in a local file using the developer-only audit:

```sh
python3 tests/axe_audit.py --axe-file /tmp/axe.min.js \
  --report /tmp/syntyr-axe-manual-review.json
```

The automated checker cannot establish the effective paint underneath these foregrounds where gradients and pseudo-elements overlap text. Contrast-token unit tests are useful but do not certify composited backgrounds.

## Manual verification protocol

For each flagged element, record selector, theme, browser, viewport/zoom setting, sampled foreground and effective background, measured contrast and screenshot. Test the lowest-contrast part of each gradient. Apply WCAG thresholds of at least 4.5:1 for regular text and 3:1 for large text and applicable essential UI graphics. Check hover, focus, disabled, selected and nested-theme contexts.

Automated browser evidence covers **126 viewport cases** across Chromium/Firefox/WebKit and **168 enlarged-text reflow cases**. The Chromium forced-colors primary-link screenshot and focus tests pass for all seven palettes. None of these substitute for native Windows High Contrast or other OS-level modes, real browser zoom, or a screen reader.

## Remaining release checklist

- [ ] Measure or adjudicate each of the 325 inconclusive text/background cases.
- [ ] Test keyboard-only navigation, native dialog/popover focus, table regions, disclosure and form semantics in a representative real app.
- [ ] Perform real assistive-technology testing with NVDA, JAWS, VoiceOver or Orca and record evidence.
- [ ] Test true 200% and 400% browser zoom on supported browsers; verify navigation, reflow and target visibility.
- [ ] Check actual OS forced-colors/high-contrast and reduced-motion settings.
- [x] Record the browser engines and versions used for automated testing (not a permanent support guarantee): Chromium 159.0.8154.6, Firefox 159.0, WebKit 27.2 in the Linux Playwright 1.65.2 test container.
- [ ] Establish browser support versions and unresolved exceptions before a stable release.

A passing axe-core run alone is **not** sufficient to claim WCAG conformance.
