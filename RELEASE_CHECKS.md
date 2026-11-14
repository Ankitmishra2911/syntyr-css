# Cyberline CSS v0.3.0-alpha.2 — release evidence

Checked 2026-11-14. Source candidate code on branch
`fix/text-reflow-a11y` at commit `ce3b649` (CSS implementation from
`0c31b9c`). Evidence is scoped to the stated tests and browser environments.

| Verification | Observed result |
| --- | --- |
| Reproducible CSS bundles (`python3 scripts/build.py --check`) | PASS |
| Source and packaging contract tests (`python3 -m unittest discover -s tests -q`) | **32/32 PASS** |
| Existing Chromium native interaction tests (`python3 tests/browser_test.py`) | **14/14 PASS** |
| Browser matrix: 6 pages × 3 widths × 3 engines | **54/54 PASS** |
| Enlarged-text stress matrix: 6 pages × 4 width/text-scale combinations × 3 engines | **72/72 PASS** |
| Chromium/Fedora axe-core 4.10.3 WCAG-tagged audit | **0 confirmed violations, 8 incomplete checks** |
| Core CSS gzip, Python gzip with mtime=0 | **3,859 bytes** (budget 5,120) |
| All-in-one CSS gzip | **4,521 bytes** (budget 8,192) |
| Runtime JS and required runtime packages | **0** |
| MIT license and modular CSS distribution | PASS |

## Test environments

- Chromium: Fedora 44 system Chromium via Playwright. Firefox: Playwright
  browser on Fedora 44. Both checked the site paths and example pages.
- WebKit: official `mcr.microsoft.com/playwright/python:v1.64.1-noble`
  container on a separate Linux CI host, with `playwright==1.64.1`.
- Reflow test: **layout stress test**, not real browser 200%/400% zoom.
  It uses 320px/390px viewport widths and changes the document's root text
  size to 100%, 150%, or 200%. Data tables may have internal scrolling.
  The text-size stress check caught and drove a fix for horizontally
  overflowing grid tracks, controls and long labels.
- Packaging: deterministic ZIP created from eight allowlisted files with
  Python standard library only. Premium business planning files are excluded.

## Still unresolved before production or paid commercialization

1. Manual screen-reader use (NVDA, VoiceOver or Orca with actual user interaction)
   and genuine browser zoom verification at 200%/400%; keyboard and
   axe-core automation do not certify WCAG 2.2 AA.
2. Review the eight axe-core inconclusive checks, actual high-contrast
   appearance, supported browser baselines, and realistic application forms.
3. Trademark/name clearance in the U.S. and Brazil for the **provisional**
   Cyberline name (see `business/trademark-screen.md`). A historical U.S.
   filing does not establish current status.
4. Product-market validation: the 10-interview recruiting issue is public,
   but **no interviews or paid commitments have been recorded**.
5. Commercial template license and refunds/delivery terms are only drafts;
   no Console Kit is offered for sale.

All CSS, current pages, templates, examples, tests and themes in this
repository remain MIT-licensed. No Tailwind Plus commercial source was reused.
