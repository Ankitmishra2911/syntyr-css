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
| `--syn-font`, `--syn-mono` | System-first font stacks |
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

## Independent density and geometry presets (unreleased)

Load `syntyr.presets.css` after core. Palette, density and geometry are
independent scoped attributes, and a nested palette inherits its nearest
geometry and density overrides unless that scope overrides them again:

```html
<link rel="stylesheet" href="syntyr.core.css">
<link rel="stylesheet" href="syntyr.presets.css">
<section class="syn-root" data-syn-theme="corporate"
         data-syn-density="compact" data-syn-geometry="precision">
  <div class="syn-panel" data-syn-theme="noir">Nested Noir, same geometry</div>
  <div class="syn-panel" data-syn-density="comfortable"
       data-syn-geometry="soft">Comfortable, soft panel</div>
</section>
```

Only the two non-default density presets are provided. Without a density
attribute the original Syntyr spacing remains unchanged. Geometry presets
influence `--syn-radius`, `--syn-cut` and optional frame cut sizing while
preserving existing per-theme defaults when omitted. You can still directly
override public tokens in application CSS.

Note: compact controls are 40 CSS pixels tall and can fall short of the
44 CSS pixel touch-target recommendation. Prefer default/comfortable density
for touch-first screens, or ensure equivalent target spacing.

## Derived accents and component-level overrides

Each built-in palette derives `--syn-accent-soft` from `--syn-accent` with `color-mix()` using that palette's opacity. Override both on a nested subtree if you change the accent there: inherited custom properties can already be resolved at the ancestor theme boundary. You can independently customize `--syn-button-padding-block`, `--syn-button-padding-inline` and `--syn-panel-padding`. The optional presets file changes button padding with density without coupling it to palette selection.
