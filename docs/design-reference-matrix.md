# Web design reference matrix and Syntyr benchmark applications

Research rubric for the **unreleased alpha.5 source candidate**, not a statement about the published alpha.4 package. Updated 2026-11-15. This matrix identifies what to *study*, not assets to redistribute. Design inspiration and design principles are not licenses.

## Ranked reference matrix

| Priority | Reference and source | Study | Syntyr application / acceptance criterion | Boundary |
| --- | --- | --- | --- | --- |
| P0 | [Open Props](https://open-props.style/) | Reusable custom properties, color and motion scales | Keep coherent `--syn-*` token roles, isolate theme overrides, verify in nested roots | Study token strategy; do not import source unchanged without license review |
| P0 | [Every Layout](https://every-layout.dev/) | Intrinsic layout primitives | Reduce bespoke media queries and test reflow at 320 CSS px and 200% zoom | Concepts only; examples may have separate licenses |
| P0 | [SmolCSS](https://smolcss.dev/) | Small responsive recipes | Keep CSS composition independent of JS and build tools | Attribute source when adapting; review per-recipe terms |
| P0 | [W3C ARIA APG](https://www.w3.org/WAI/ARIA/apg/) | Native keyboard and focus interaction guidance | Validate labels, focus order, and dynamic semantics in actual browser tests | ARIA guidance does not provide interactive behavior |
| P0 | [web.dev Learn CSS](https://web.dev/learn/css/) | Cascade, modern CSS, progressive enhancement | Test forced colors, reduced motion, and unsupported CSS fallback | Verify browser targets before depending on newer primitives |
| P1 | [GitHub Primer](https://primer.style/) | Accessible states, density, documented tokens | Compare data tables, responsive navigation, error/help states | Do not copy GitHub branding |
| P1 | [PatternFly](https://www.patternfly.org/) | Complex B2B admin workflows | Cover multi-column CRM records, search, status and overflow handling | Framework implementation not a runtime dependency |
| P1 | [IBM Carbon](https://carbondesignsystem.com/) | Data-rich UX patterns and hierarchy | Verify content density, long labels, tables, status without color alone | Don't transplant proprietary assets |
| P1 | [GOV.UK Design System](https://design-system.service.gov.uk/) | Error summaries, labels and validation patterns | Include real labels and meaningful help/error copy in future interactive examples | Not a guarantee of full WCAG conformance |
| P1 | [CUBE CSS](https://cube.fyi/) | Composition, utilities, blocks, exceptions | Prefer scoped low-specificity CSS over application-level override wars | Pattern inspiration rather than imported code |
| P1 | [Utopia](https://utopia.fyi/) | Fluid type and spacing | Prefer `clamp()` and intrinsic sizing where they improve readability | Verify min/max type sizes for zoom and content |
| P2 | [Mobbin](https://mobbin.com/) | Real product navigation, onboarding and forms | Benchmark authentic information architecture, not just isolated cards | Commercial screenshots are references only |
| P2 | [Refero](https://refero.design/) | SaaS dashboard and marketing layout patterns | Build practical composition samples with independent original copy | Do not copy screenshots/templates |
| P2 | [Codrops](https://tympanus.net/codrops/) | Expressive CSS, typography, subtle motion | Keep futuristic effects opt-in, accessible and motion-reducible | Review each demo's license; no direct copying |
| P2 | [Tailwind Plus](https://tailwindcss.com/plus) | Commercial template packaging and support | Keep MIT CSS fundamentals free; monetize original complete templates | Commercial examples are **not** MIT source assets |

## Decision framework

- **Core first:** native controls, semantic tokens, keyboard focus, responsive layouts and table reflow.
- **Optional recipes:** dashboard shell, marketing hero, code documentation, navigation. Import only needed modules.
- **Commercial boundary:** Free MIT token/component contract; original full-page themes, design files and templates can be sold separately. Avoid creating a feature paywall around accessibility.
- **Do not copy** competitor screenshots, proprietary HTML/CSS, logos, fonts, graphics or exact visual compositions into the repository. A public webpage is not necessarily an open-source asset.
- **Not implemented by CSS:** authentication, filtering, CRUD, stored settings, asynchronous loading, real time charts, server actions. Demo content is fictional and static.

## Benchmark applications

Three intentionally independent, static Syntyr sample interfaces:

1. [Marketing website](../examples/design-benchmarks/marketing.html) — product navigation, hero, feature pricing, CTA and content hierarchy.
2. [CRM dashboard](../examples/design-benchmarks/crm.html) — sidebar navigation, KPIs, captioned data table, GET search form and status text.
3. [Documentation website](../examples/design-benchmarks/documentation.html) — table of contents, inline code, sample command, version caveats and disclosure.

The application pages use `syntyr.core.css` and the optional `syntyr.recipes.css`. Their shared **original** composition stylesheet is `examples/design-benchmarks/benchmark.css`; no font CDN, icon CDN or runtime JavaScript is required. This benchmark tests three *Syntyr adoption scenarios*, not a controlled side-by-side comparison against other CSS frameworks. For comparative framework measurements see `scripts/perf_framework_fixtures.py`.

### Reproduce offline measurements

From a checkout with distribution files built:

```sh
python3 scripts/build.py --check
python3 scripts/design_reference_audit.py
python3 scripts/design_reference_audit.py --json
python3 -m unittest discover -s tests -p test_design_reference_benchmarks.py -v
```

The audit reports real HTML bytes, local Syntyr stylesheet bytes and gzip bytes, custom stylesheet bytes and gzip bytes, the number of custom `--syn-*` overrides, and runtime JS bytes. Gzip uses deterministic `mtime=0`; stylesheets are counted once per page and are **not** equivalent to browser transfer totals with caching. The metrics do **not** claim real-world LCP, CLS, browser-interaction latency, color contrast, or full WCAG conformance. Run the repository's Playwright/axe checks for those claims. Source checkout and published alpha.4 differ.

### Follow-up quality gates

- Compare the three designs at 320, 375, 768, 1280 CSS pixels, 200% zoom, and with long translated strings.
- Test keyboard-only navigation, high contrast / forced colors and reduced-motion preferences in Chromium, Firefox and WebKit.
- Profile with and without warm CSS caches; capture LCP, CLS, INP and visual screenshots before changing the core.
- Track Syntyr-specific CSS overrides over time, minimizing them when reusable primitives can replace them safely.
