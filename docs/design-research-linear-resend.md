# Design research: Linear, Resend, and practical developer UI

Syntyr borrows **principles**, not source code, brand tokens, trademarks, logos,
screenshots, or company-specific component arrangements. Syntyr remains an
independent MIT-licensed, CSS-first project.

## Findings (November 2026)

### Linear: quiet structure and information density

Linear's [March 2026 UI refresh](https://linear.app/now/behind-the-latest-design-refresh)
describes a deliberate reduction in chrome: dimmer secondary navigation, fewer
visible separators, smaller less-prominent icons, and content that gets visual
priority. The company emphasizes preserving information density without
making every control compete for attention. Its
[2024 redesign write-up](https://linear.app/now/how-we-redesigned-the-linear-ui)
also discusses cross-view alignment, type hierarchy, and cohesive light/dark
themes.

**Applied in Syntyr:** quieter derived borders for decorative card/table
separators, recessed app navigation surfaces, opt-in compact density, readable
UI fonts by role, and an explicit selected-table-row state. Stronger control
borders and visible focus outlines remain available for accessibility.

### Resend: premium restraint and editorial presentation

Resend's [July 2026 brand guidelines](https://resend.com/handbook/design/what-are-our-brand-guidelines)
describe the brand as simple, modern, and memorable, with dark-first styling,
neutral material-inspired color scales, distinct product versus editorial type,
and deliberate use of gradients. Its
[public brand skill](https://github.com/resend/design-skills)
emphasizes semantic colors and separate display, UI, and code typography.

**Applied in Syntyr:** optional system-serif editorial headline recipe,
static gradient wash in the optional effects stylesheet, explicit UI/display
font tokens, and semantic states already present in Syntyr. Fonts are local
system stacks only. We do not import Resend fonts, logos, colors, or assets.

### Earlier references: Vercel, Stripe, Apple, Google, PostHog, Sentry, Cloudflare

These remain reference points for precise controls, marketing composition,
restrained depth, responsive themes, brand distinction, observability, and
operational information hierarchy respectively. Their proprietary components
and brand assets are not dependencies or templates for Syntyr.

## Architecture choices

- **Seven existing themes, not seven more themes.** Grid and Terminal retain
  monospace UI presentation; Studio, Corporate, Minimal, Noir, and Industrial
  use system UI fonts. Marketing hero typography can opt into a local serif.
- **Derived, theme-aware surface roles.** `--syn-surface-recessed`,
  `--syn-surface-raised`, and `--syn-border-subtle` are recomputed in nested
  theme contexts, so a dark panel inside a light page is not stuck with its
  parent's palette. The original tokens remain stable.
- **Density is layout, not text scaling.** Use `data-syn-density="compact"`
  on a Syntyr root or nested region. It reduces padding and control height
  while leaving fonts readable. It does not imply any JavaScript widget state.
- **Effects are opt-in.** `syn-gradient-wash` is a static decorative gradient
  in `syntyr.effects.css` and is disabled under forced-colors.
  `syn-site-heading--editorial` is a separate `syntyr.recipes.css` class.
- **No arbitrary CSS byte ceilings.** The deterministic build reports raw and
  gzip bytes. Regressions are assessed via browser testing, not blocked by
  fixed 5 KiB/8 KiB numbers. Keep modules optional and CSS without runtime JS.

## Examples

```html
<link rel="stylesheet" href="syntyr.core.css">
<link rel="stylesheet" href="syntyr.recipes.css">
<link rel="stylesheet" href="syntyr.effects.css">

<main class="syn-root" data-syn-theme="studio">
  <section class="syn-site-hero syn-gradient-wash">
    <h1 class="syn-site-heading syn-site-heading--editorial">
      Sophisticated by default.
    </h1>
    <p>Original editorial typography using system fonts only.</p>
  </section>
  <section data-syn-density="compact" aria-label="Operational records">
    <table class="syn-table"><!-- semantic data table --></table>
  </section>
</main>
```

Live repository examples: `examples/business.html` for the restrained
marketing direction, and `examples/operations-console.html` for compact
operational density.

## Deliberately not borrowed

We do not add complex tabs, combo boxes, custom menus, animation engines,
external fonts, mandatory icon sets, design-system runtimes, company-branded
palettes, or opaque theme generators. Native HTML semantics, CSS cascade
layers, strong focus states, and application-controlled interaction remain
Syntyr's long-term contract.
