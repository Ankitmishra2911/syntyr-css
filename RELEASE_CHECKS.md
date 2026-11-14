# Cyberline v0.3-alpha release evidence

Tested 2026-11-14 in the provided local execution environment.

| Check | Result |
| --- | --- |
| Reproducible CSS bundles (`python3 scripts/build.py --check`) | PASS |
| Unit and package contract tests (`python3 -m unittest discover -s tests -v`) | 20/20 PASS |
| Chromium smoke, interaction and responsive tests (`python3 tests/browser_test.py`) | 14/14 PASS |
| CSS stylesheet parse with developer-only `tinycss2` | 0 top-level parse errors |
| Runtime JS files/scripts | 0 |
| Runtime package dependencies | 0 |
| Remote font/image requests declared by the gallery and pricing example | 0 |
| Core stylesheet gzip | 3,840 bytes (target <= 5,120) |
| All-in-one stylesheet gzip | 4,499 bytes (target <= 8,192) |

## Still required before claiming production readiness

- Actual Firefox and WebKit browser test matrices; Chromium-only success is not cross-browser proof.
- Manual screen-reader and keyboard checks across all free examples, including at 200% and 400% zoom.
- A documented supported browser baseline (especially HTML Invoker Commands API support).
- Contrast testing of *all* component states, not only sample text pairings, and a forced-colors visual review.
- Brand availability/trademark review of the provisional `Cyberline` name.
- Real product-market validation and a proper premium license review before selling assets.

All new templates/code in this archive are original. Tailwind Plus commercial sources were not copied.
