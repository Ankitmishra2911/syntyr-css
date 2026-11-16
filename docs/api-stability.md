# SYNTYR CSS public API and prerelease stability

**Status: experimental `0.3.0-alpha.5` candidate; no v1 stability promise.**
This document names the intended public contracts so that changes can be
reviewed consistently before `1.0.0`. It is not a new compatibility guarantee.

## Public surface and intended v1 boundaries

| Surface | Current policy | Intent for v1 |
| --- | --- | --- |
| `syntyr.core.css`, `.syn-root`, stable component classes | Public prerelease API | Stable selectors and behavior |
| New `.syn-field`, `.syn-field-row`, `.syn-field-body`, `.syn-input-group`, `.syn-input-addon` form compositions | Experimental prerelease core additions | Evaluate for v1 stabilization after browser/accessibility review |
| Documented `--syn-*` design-token names | Public prerelease API | Stable names, not fixed default values |
| New documented component-local layout variables | Experimental alpha.5 opt-in API | Evaluate for stability after responsive review |
| `data-syn-color-space="oklch"` | Experimental alpha.5 presentation opt-in | Evaluate perceptual color/contrast before v1 |
| `data-syn-theme` and documented `data-syn-*` state hooks | Public prerelease API | Stable names and meanings |
| `syntyr.semantic.css` and `.syn-semantic` | Opt-in prerelease API | Stable scoped semantics after audit |
| `dist/presets/{minimal,saas,cinematic}.css` | Experimental single-file entrypoints | Stabilize names and inclusion contract only after explicit review |
| `metadata/css-contract.v1.json` | Build artifact-manifest schema v1 | Version schema independently of public CSS API |
| `syntyr.recipes.css`, `syntyr.geometry.css` | Experimental, opt-in | Evaluate for individual stabilization |
| `syntyr.effects.css`, `syntyr.utilities.css` | Experimental, opt-in | Evaluate for individual stabilization |
| `syntyr.css`, `syntyr.all.css` | Public convenience bundles | Maintain documented contents/meaning at v1 |
| `terminal/palettes.json` | Optional example/palette asset | Separate compatibility decision from CSS |
| `integrations/`, `examples/`, documentation editor | Non-core adapters/showcases | No automatic CSS-core stability promise |

The `syn-*` selector namespace, `--syn-*` properties and `data-syn-*` attributes
remain the only Syntyr-specific styling namespace. ARIA states such as
`aria-pressed`, `aria-busy`, `aria-invalid` and native HTML state remain governed
by web-platform semantics, not a separate Syntyr state machine.

Core classes do **not** require an application build pipeline. The opt-in
semantic mode only styles elements under `.syn-semantic` within `.syn-root`.
Themes set design tokens; component selectors should not fork per theme. The
finite utilities are explicit overrides in their own final `syn.utilities`
cascade layer. Do not load a convenience bundle and its component modules
simultaneously.

## Proposed minimum v1 contract (not yet approved)

**Proposal only.** The source is still `0.3.0-alpha.5` and the published
`0.3.0-alpha.4` files remain immutable. This shortlist is for v1 API review,
not a declaration that 1.0 is released or that other current APIs are removed.
Do not promise every prerelease class, token, optional stylesheet or theme name
as a permanent compatibility commitment by default.

| v1 candidate | Intended stable responsibility | Outside the initial freeze |
| --- | --- | --- |
| `syntyr.core.css`, `.syn-root` | Self-hosted, scoped CSS without framework or runtime requirements | Adapter, preset and convenience-bundle inclusion details |
| `.syn-shell`, `.syn-stack`, `.syn-grid`, `.syn-inline`, `.syn-panel` | Basic layout and surfaces assembled with HTML | Specialized dashboard, geometry and cinematic compositions |
| `.syn-button`, `.syn-input`, `.syn-select`, `.syn-textarea`, `.syn-table`, `.syn-table-wrap` | Common native controls and readable tabular content | Advanced widget behavior, grid interaction and framework states |
| `.syn-heading`, `.syn-muted`, `.syn-badge` | Small portable typographic affordances | Theme-specific graphic treatments and decorative variants |
| `--syn-bg`, `--syn-surface`, `--syn-text`, `--syn-muted`, `--syn-accent`, `--syn-on-accent`, `--syn-frame` | Minimal semantic palette roles; values may change for contrast fixes | Internal derived shades and theme-specific effect tokens |
| `--syn-font`, `--syn-radius`, `--syn-space-1` through `--syn-space-4` | Basic typography, shape and spacing customization | Experimental component-local layout overrides |
| `data-syn-theme`, native HTML and semantic ARIA states | Token-based theme boundaries and state presentation | Freezing every named palette, intensity and density profile |

The list is deliberately small and **not exhaustive**. Additional existing
public alpha selectors remain available as documented for their particular
version; deciding which belong in v1 requires evidence rather than an automatic
rename or removal. Before stabilizing an entry, verify it is used in at least
two independent, non-showcase consumer contexts, has documented composition and
extension behavior, passes browser/accessibility review, and has no necessary
framework-specific coupling. Consider opt-in `.syn-semantic` independently
once the accessibility and scope review is complete.

Versioned release assets and pre-v1 compatibility rules remain unchanged.
Removal of unnecessary experimental aliases is possible **before** the v1
freeze; after stabilization, semver and migration documentation apply. Do not
add core API solely to make an optional integration easier.

### Alpha.5 opt-in CRM compositions and density profiles

The source-only `syntyr.recipes.css` adds optional `.syn-filter-bar`,
`.syn-pipeline` and `.syn-record-fields` compositions. These selectors are
experimental and are not in immutable alpha.4. Core adds explicit
`data-syn-density="comfortable"` and `"spacious"` profiles alongside the
existing `"compact"` profile, allowing nested density overrides.
No application behaviors or JavaScript are shipped with these compositions.

### Alpha.5 native CSS refinements

Core layout components expose optional local `--syn-grid-*`,
`--syn-layout-*`, `--syn-stack-gap` and `--syn-inline-gap` overrides.
Optional recipes expose KPI, filter and detail-layout equivalents. Their
fallbacks preserve the earlier default layouts, without a compiler or extra
runtime dependency. `.syn-field` gains progressive native focus/error label
styling, and `.syn-panel[inert]` gains a presentation-only unavailable cue.

The experimental `data-syn-color-space="oklch"` attribute changes only the
surface-hover color-mix role on explicitly opted-in regions. Default palettes,
semantic foreground pairs and fallback colors are unchanged. It is not a new
default theme or a stability commitment; see the [theme customization guide](theme-customization.md).

### Alpha.5 semantic HTML authoring changes

The unreleased semantic CSS candidate gives native classless `form` and
`fieldset` a composed vertical layout, a comfortable native `summary`
target, and readable table `caption` styling. Classed forms continue using
their explicit component API. For ordinary `.syn-table` rows,
`data-syn-state="selected"` remains the visual state; the
`aria-selected="true"` row selector now applies only to a real ARIA grid or
treegrid. Consumers styling ordinary table rows with `aria-selected` should
switch to the visual data attribute rather than inventing widget semantics.
The published immutable alpha.4 assets are unchanged.

The optional validator `--semantic` mode adds conservative native HTML
diagnostics, with no change to default validation or consumer runtime.

### Alpha.5 data-table wrapping migration

The unreleased alpha.5 candidate changes classed `.syn-table` cells to wrap
descriptive text by default, including when a table is placed in a narrow
container. This **prerelease layout compatibility change** may increase row
height in existing screens. To preserve the former implicit no-wrap behavior
for short codes, dates, or identifiers, explicitly add `.syn-cell--nowrap`
to those cells. Numeric cells with `.syn-cell--numeric` remain no-wrap.
Keep long prose wrapping whenever possible; if full columns require sideways
scrolling, use `.syn-table-wrap` with keyboard reachability and an accessible
table caption. The published immutable alpha.4 stylesheet is unchanged.

## Compatibility and version policy

- Before v1: breaking prerelease changes are possible; document them in the
  changelog. Do not maintain obsolete aliases solely for alpha compatibility.
- After v1: breaking changes to stabilized selector names, attribute meanings,
  documented file entrypoints and core component behavior require a major
  version. Additions can use minor releases; corrections use patch releases
  when semantically compatible.
- Values and appearance are not identical across patch versions. Accessibility
  fixes may adjust color, spacing, focus or contrast without renaming tokens.
- Custom, undocumented selectors and implementation variables are not a
  supported extension API. Use documented tokens and composition instead.
- Versioned `/v/<version>/` CDN assets remain byte-for-byte immutable; prefer
  self-hosting or pinning a version for production deployments.

## Pre-1.0 release checklist

1. Confirm which individual classes and tokens merit permanent compatibility.
2. Finish keyboard, screen-reader, browser zoom and contrast review; automated
   scans do not establish WCAG conformance.
3. Validate the supported browser/version matrix on realistic applications,
   including nested themes, CSS utilities and semantic opt-in behavior.
4. Publish versioned docs, a reproducible CSS distribution and a complete
   migration note if prerelease contracts change.

See [`ARCHITECTURE.md`](../ARCHITECTURE.md) for feature-admission criteria,
layer ownership and dependency boundaries. Optional package integrations may
provide additional contracts but must never introduce a mandatory core
runtime dependency.
