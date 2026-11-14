# Cyberline CSS

**Experimental v0.3.0-alpha.3 (unreleased candidate)** — framework-neutral, low-dependency, CSS-first styling for modern SaaS apps, professional business websites and optional cinematic Grid/Noir designs.

- **0 JavaScript / 0 runtime dependencies / 0 network assets.** Works with server-rendered HTML, React, HTMX, Go templates, Astro, and other HTML renderers.
- **Compositional layouts:** native container-query responsive telemetry, empty states and pricing layouts. State styles use ARIA when semantic and data attributes otherwise.
- **Modern, plain CSS.** Native HTML primitives, cascade layers, color-mix, responsive Grid, accessible contrast targets and scoped theme tokens.
- **Seven CSS themes:** Grid, Noir, Studio, Industrial, Terminal, Corporate and Minimal share the same component contract.
- **Two modes:** explicit component classes, and a Pico-like *optional* `.cy-semantic` mode.
- **Modular:** core, semantic, recipes, effects and optional finite utilities; includes convenience bundles.
- **No installation:** copy prebuilt CSS. Python 3 is used only by maintainers to regenerate it.

## Live gallery and installation

- [Live website](https://dporkka.github.io/cyberline-css/)
- [Component gallery](https://dporkka.github.io/cyberline-css/docs/)
- [Latest published v0.3.0-alpha.2 (Studio/CLI release)](https://github.com/dporkka/cyberline-css/releases/tag/v0.3.0-alpha.2)
- [Dependency-free CSS distribution guide](docs/distribution.md)
- [Theme customization, design tokens, and copy-paste recipes](docs/theme-customization.md)
- [Accessibility and browser-matrix methodology](docs/accessibility.md)
- [Commercial Console Kit concept (not available for purchase)](docs/console-kit.html)
- [Public design-partner review issue (seeking 10 participants)](https://github.com/dporkka/cyberline-css/issues/3)
- [Design-partner interview pilot (not yet recruited)](business/design-partner-pilot.md)
- [Free original Noir resource archive demo](examples/resources.html)
- [Seven-theme CSS comparison gallery](examples/themes.html)
- [Optional Vertigo admin demo](examples/vertigo-admin.html) and [integration guide](docs/vertigo-integration.md)
- [Hugo/Zola/static docs decision](docs/site-generator-decision.md) and [isolated Hugo preview](experiments/hugo/README.md)
- [Unreleased alpha.3 verification and remaining gates](RELEASE_CHECKS_ALPHA3.md)
- [Alpha.3 accessibility element-level review and outstanding manual gates](docs/accessibility-alpha3-review.md)

Use the release ZIP, copy `dist/cyberline.core.css` into your static assets, and load it with a normal stylesheet link. No NPM, JS or build step is needed in an application.

## Start in 10 seconds

Open [docs/index.html](docs/index.html) in a browser. Try the [SaaS dashboard](examples/saas.html), [business website](examples/business.html), [browser terminal](examples/terminal.html), [Grid console](examples/console.html), [Noir landing page](examples/landing.html), or [Noir pricing demo](examples/pricing.html). Compare [all seven palettes](examples/themes.html). The gallery needs no server, Node, NPM, runtime JS or remote fonts.

```html
<link rel="stylesheet" href="cyberline.core.css">
<section class="cy-root" data-cy-theme="grid">
  <article class="cy-panel cy-panel--cut">
    <span class="cy-badge">SYSTEM ONLINE</span>
    <h2 class="cy-heading">Command Center</h2>
    <button class="cy-button cy-button--primary">Execute</button>
  </article>
</section>
```

For semantic mode, add `cyberline.semantic.css` **after** core:

```html
<link rel="stylesheet" href="cyberline.core.css">
<link rel="stylesheet" href="cyberline.semantic.css">
<div class="cy-root cy-semantic" data-cy-theme="noir">
  <article>
    <label for="operator">Operator<input id="operator" required></label>
    <button>Continue</button>
  </article>
</div>
```

`cy-semantic` only styles unclassed semantic elements inside that subtree; elements elsewhere are unaffected. Core component classes do not rely on semantic mode. Switch `data-cy-theme` among `grid`, `noir`, `studio`, `industrial`, `terminal`, `corporate` and `minimal`, including nested themed areas.

## Build outputs

| File | Description |
| --- | --- |
| `dist/cyberline.core.css` | Tokens, scoped base, components (default choice) |
| `dist/cyberline.semantic.css` | Optional semantic HTML styling (load after core) |
| `dist/cyberline.effects.css` | Optional, static decorative effects |
| `dist/cyberline.recipes.css` | Optional SaaS, marketing and browser-terminal layouts |
| `dist/cyberline.utilities.css` | Optional finite layout, spacing and accessibility utilities |
| `terminal/palettes.json` | Color palettes for native ANSI terminal applications (not CSS) |
| `dist/cyberline.css` | Backwards-compatible core + effects bundle |
| `dist/cyberline.all.css` | All modules (semantic still opt-in by class) |

The source is split into `src/components/*.css`, `src/tokens.css`, `src/base.css`, `src/semantic.css`, `src/recipes.css`, `src/utilities.css`, and `src/effects.css`. Check the [component and token contract](docs/components.md), [free composition recipes](docs/recipes.md), and [Tailwind/Tailwind Plus study](docs/tailwind-research.md).

## Modern SaaS, CLI and business websites

Use `data-cy-theme="studio"` for a neutral, professional light theme. Grid, Noir, Industrial and Terminal offer dark palettes; Corporate and Minimal are additional light options. The theme changes colors, while optional `cy-frame--precision`, `cy-frame--industrial` and `cy-frame--soft` classes control visual geometry independently.

For production-oriented examples, load `cyberline.core.css` **then** `cyberline.recipes.css` for responsive application shells (`cy-app-shell`), business landing layouts (`cy-site-hero`) and browser terminal panels (`cy-terminal`). Continue to use real headings, tables, labels, links and forms. The recipes provide layout and presentation, not authentication, data fetching, filtering or backend actions.

**Native CLI apps cannot consume CSS.** Instead, use `terminal/palettes.json` with Go, Rust, Python or another CLI implementation to define ANSI 16-color palettes and foreground/background preferences. See the [stdlib Python demonstration](examples/ansi_cli.py) and [integration guide](docs/saas-cli-business.md). Respect `NO_COLOR`, TTY detection and user terminal preferences.

All additions are MIT licensed and do not change the core runtime dependency contract. These development-branch enhancements are **not part of the published v0.3.0-alpha.2 release** until a new release is cut.

## Development and verification

```sh
python3 scripts/build.py
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v
python3 scripts/package_release.py
```

Chromium browser tests use Playwright (a **dev-only optional tool**) and run with:

```sh
python3 tests/browser_test.py
python3 tests/browser_matrix.py --browsers chromium firefox webkit
python3 tests/axe_audit.py --axe-file /tmp/axe.min.js # dev-only checker; see docs/accessibility.md
```

The browser scripts require `playwright` and a Chromium browser to be present; it autodetects `chromium` or `chromium-browser`, or accepts `PLAYWRIGHT_CHROMIUM_EXECUTABLE`; consumers of the CSS do **not** require either. This project intentionally avoids adding a package manager or dependency manager to the runtime/library.

## Important boundaries

- This is a **CSS library**, not a JS widget framework. Native `dialog`, `[popover]` and `details` provide native interaction in supported browsers. The HTML Invoker Commands API used to open modal dialogs is not supported in every older browser. Use progressive enhancement for critical interactions.
- No custom combobox, tabs, virtualized tables, or fake ARIA widgets. Advanced widgets can be built separately without coupling them to the visual system.
- Accessibility and cross-browser compatibility require more verification before a production v1.0 release. Test real applications at 200% and 400% zoom and with screen readers.
- Runtime zero dependencies does not mean zero maintainer/tooling dependencies. The standard library build script is deliberately small, and Playwright is only used for optional tests.
- The `cy-root` scope works for compact embedded sections. `body.cy-root` gets full viewport height, or add `.cy-page` explicitly when needed.

## Roadmap

v0.2-alpha: free console + landing demos, accessible form-error styles, button variants, independent page/embedded scopes. v0.3-alpha: portable container-query recipes, attribute state styling, pricing example and Tailwind/Plus architectural study. v0.4: docs/theme editor; v1: stability + expanded browser/accessibility validation. Budgets: core CSS <= 5 KiB gzip, all modules <= 8 KiB gzip, runtime JS 0 bytes. These budgets are verified by tests rather than marketing claims.

## Provenance and license

This implementation is original MIT-licensed code; it has not imported or ported any Pico, Chota, Open Props or other third-party source. Those libraries are design/architecture research references only. Any future code borrowing must retain necessary copyright and license notices in `THIRD_PARTY_NOTICES.md`.

See [LICENSE](LICENSE).


## Business model: open source stays open source

**The entire current repository (including core, themes, examples, docs and tests) is MIT-licensed.** The design system is not a crippled free tier. A future business can sell **separately authored premium page templates and design kits**, plus optional custom integrations. The premium template source, if created, would ship separately with a commercial license; any embedded MIT Cyberline core retains MIT rights.

- [Business strategy, product scope and price tests](business/strategy.md)
- [Proposed premium Console Kit scope (not on sale)](business/console-kit-spec.md)
- [Draft license boundary for *future* premium assets](business/premium-license-draft.md) — **not an operative contract**
- [Validation and go/no-go plan](business/validation-plan.md)

No paid kit has been shipped or put up for sale in this repository. No billing or license-key code is included. The Grid and Noir visual themes are original, not officially affiliated with any entertainment franchise. **Cyberline is a provisional name**, pending brand clearance.
