# Syntyr theme customization — copy, override, ship

Syntyr themes are **CSS custom properties**, not JavaScript configuration.
The MIT core already includes Grid and Noir palettes, responsive primitives,
accessible focus styling and semantic element options.

## 1. Choose a theme

Load the published `syntyr.core.css` in your application and use regular HTML:

```html
<link rel="stylesheet" href="/css/syntyr.core.css">
<section class="syn-root" data-syn-theme="grid">
  <article class="syn-panel syn-panel--cut">
    <h2 class="syn-heading">Sector status</h2>
    <button class="syn-button syn-button--primary">Open</button>
  </article>
  <aside data-syn-theme="noir" class="syn-panel">
    Nested Noir preview
  </aside>
</section>
```

Use `data-syn-theme="noir"` for warm amber. Native HTML features
such as `details`, `dialog` and `popover` don't need framework JavaScript.

## 2. Override tokens using application CSS

Syntyr declares its defaults in named cascade layers. App CSS without a
layer takes precedence over layered author rules regardless of selector specificity.
Load application overrides **after** the Syntyr stylesheet to reduce surprises:

```css
/* app.css: original tokens, not copied from existing entertainment IP. */
.syn-root[data-syn-theme="grid"] {
  --syn-accent: #80dfef;
  --syn-on-accent: #07121a;
  --syn-accent-soft: rgb(128 223 239 / 10%);
  --syn-frame: #34576c;
}

/* Override one nested region without affecting the rest of the site. */
.my-warning-panel {
  --syn-surface: #1b232d;
  --syn-warning: #ffe2aa;
}
```

Important: `--syn-accent` is the most visible token, but `--syn-on-accent`
is the contrasting **foreground on primary buttons**. Change both when
necessary. Verify 4.5:1 contrast for body text and 3:1 for essential non-text
graphics; don't assume arbitrary overrides remain accessible.

Useful tokens:

| Token | Description |
| --- | --- |
| `--syn-bg` | Main background |
| `--syn-surface`, `--syn-surface-hi` | Cards and controls |
| `--syn-text`, `--syn-muted` | Main and secondary text |
| `--syn-accent`, `--syn-on-accent`, `--syn-accent-soft` | Brand accent, its foreground, soft fill |
| `--syn-frame`, `--syn-danger`, `--syn-success`, `--syn-warning` | Borders and status |
| `--syn-font`, `--syn-mono`, `--syn-font-ui`, `--syn-font-display` | Body, technical, control, and display typography |
| `--syn-type-xs`, `--syn-type-sm`, `--syn-type-base` | Typography sizes |
| `--syn-surface-recessed`, `--syn-surface-raised`, `--syn-border-subtle` | Derived surfaces and quiet separators |
| `--syn-row-padding-block`, `--syn-card-padding` | Density-aware spacing |
| `--syn-space-1` … `--syn-space-5` | Spacing |
| `--syn-cut`, `--syn-radius`, `--syn-control-height` | Geometry |
| `--syn-duration-fast`, `--syn-ease` | Optional transitions |

## 3. CSS component mode versus native semantic mode

Scoped component classes: `.syn-panel`, `.syn-button`, `.syn-table`.
They work with only `syntyr.core.css`.

For classless HTML resembling Pico CSS, load **both** files and opt in:

```html
<link rel="stylesheet" href="/css/syntyr.core.css">
<link rel="stylesheet" href="/css/syntyr.semantic.css">
<div class="syn-root syn-semantic" data-syn-theme="noir">
  <article>
    <h2>Operator access</h2>
    <label for="operator">Operator ID</label>
    <input id="operator" name="operator" required>
    <button>Continue</button>
  </article>
</div>
```

Unclassed controls outside `.syn-semantic` are not restyled.
If you need glows or static grid effects, add `syntyr.effects.css`
as a third optional file. Don't load `syntyr.all.css` **and** its
individual component files at the same time.

## 4. Responsive applications and accessibility

Use `.syn-region` as the parent for container-responsive patterns such as
`.syn-stats`, `.syn-split`, `.syn-pricing`; width comes from the container,
not the whole viewport. Use `.syn-page` only for a full-page experience.

Syntyr honors `prefers-reduced-motion: reduce`. Theme overrides
must not remove focus outlines, fake disabled states, or communicate state
only through color. Test keyboard navigation, 200%/400% browser zoom,
high-contrast/forced-colors, and relevant screen readers in the target app.

**No runtime JavaScript is required for styling.** Search, authentication,
live data, and server-side form handling are intentionally application
responsibilities; optional advanced widgets are outside the CSS core.

## Seven theme palettes (unreleased alpha.5 candidate)

The published alpha.4 tag offers Grid, Noir and Studio. This candidate adds Industrial, Terminal, Corporate and Minimal. Use the same HTML and change only the theme attribute:

- `data-syn-theme="grid"`
- `data-syn-theme="noir"`
- `data-syn-theme="studio"`
- `data-syn-theme="industrial"`
- `data-syn-theme="terminal"`
- `data-syn-theme="corporate"`
- `data-syn-theme="minimal"`

To use finite opt-in layout utilities, load `syntyr.utilities.css` after `syntyr.core.css` (or use the all bundle). Utilities include `.syn-u-flex`, `.syn-u-grid`, `.syn-u-between`, spacing helpers and a visually hidden helper. No compiler or runtime JavaScript is required.

## Typography, density, and quiet surfaces

Control and navigation text uses `--syn-font-ui`. Display headings use
`--syn-font-display`, while code and CLI regions retain `--syn-mono`.
Grid and Terminal choose monospace UI by default; light themes and Noir use
system sans-serif controls. Replace the font variables if a product has its
own typeface, without introducing required external fonts.

The `--syn-surface-recessed`, `--syn-surface-raised`, and
`--syn-border-subtle` tokens derive from the active theme palette and
recompute in nested themed regions. Strong borders remain available for
focus and essential controls. Avoid treating subtle separators as a substitute
for accessible non-text contrast where boundaries are required.

To opt into compact operational layouts:

```html
<section class="syn-root" data-syn-theme="minimal" data-syn-density="compact">
  <table class="syn-table"><!-- ... semantic rows ... --></table>
</section>
```

Compact density reduces padding and control heights, **not font sizes**.
Use the default density for content-heavy business pages or touch-first forms.
For an optional editorial hero, combine `syn-site-heading--editorial` from
`syntyr.recipes.css` with `syn-gradient-wash` from `syntyr.effects.css`.
Both use local fonts and static CSS without runtime dependencies.
