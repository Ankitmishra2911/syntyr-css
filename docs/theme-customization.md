# Cyberline theme customization — copy, override, ship

Cyberline themes are **CSS custom properties**, not JavaScript configuration.
The MIT core includes seven palettes, from Grid and Noir to Studio, Corporate and Minimal, plus responsive primitives,
accessible focus styling and semantic element options.

## 1. Choose a theme

Load the published `cyberline.core.css` in your application and use regular HTML:

```html
<link rel="stylesheet" href="/css/cyberline.core.css">
<section class="cy-root" data-cy-theme="grid">
  <article class="cy-panel cy-panel--cut">
    <h2 class="cy-heading">Sector status</h2>
    <button class="cy-button cy-button--primary">Open</button>
  </article>
  <aside data-cy-theme="noir" class="cy-panel">
    Nested Noir preview
  </aside>
</section>
```

Use `data-cy-theme="noir"` for warm amber. Native HTML features
such as `details`, `dialog` and `popover` don't need framework JavaScript.

## 2. Override tokens using application CSS

Cyberline declares its defaults in named cascade layers. App CSS without a
layer takes precedence over layered author rules regardless of selector specificity.
Load application overrides **after** the Cyberline stylesheet to reduce surprises:

```css
/* app.css: original tokens, not copied from existing entertainment IP. */
.cy-root[data-cy-theme="grid"] {
  --cy-accent: #80dfef;
  --cy-on-accent: #07121a;
  --cy-accent-soft: rgb(128 223 239 / 10%);
  --cy-frame: #34576c;
}

/* Override one nested region without affecting the rest of the site. */
.my-warning-panel {
  --cy-surface: #1b232d;
  --cy-warning: #ffe2aa;
}
```

Important: `--cy-accent` is the most visible token, but `--cy-on-accent`
is the contrasting **foreground on primary buttons**. Change both when
necessary. Verify 4.5:1 contrast for body text and 3:1 for essential non-text
graphics; don't assume arbitrary overrides remain accessible.

Useful tokens:

| Token | Description |
| --- | --- |
| `--cy-bg` | Main background |
| `--cy-surface`, `--cy-surface-hi` | Cards and controls |
| `--cy-text`, `--cy-muted` | Main and secondary text |
| `--cy-accent`, `--cy-on-accent`, `--cy-accent-soft` | Brand accent, its foreground, soft fill |
| `--cy-frame`, `--cy-danger`, `--cy-success`, `--cy-warning` | Borders and status |
| `--cy-font`, `--cy-mono` | System-first font stacks |
| `--cy-space-1` … `--cy-space-5` | Spacing |
| `--cy-cut`, `--cy-radius`, `--cy-control-height` | Geometry |
| `--cy-duration-fast`, `--cy-ease` | Optional transitions |

## 3. CSS component mode versus native semantic mode

Scoped component classes: `.cy-panel`, `.cy-button`, `.cy-table`.
They work with only `cyberline.core.css`.

For classless HTML resembling Pico CSS, load **both** files and opt in:

```html
<link rel="stylesheet" href="/css/cyberline.core.css">
<link rel="stylesheet" href="/css/cyberline.semantic.css">
<div class="cy-root cy-semantic" data-cy-theme="noir">
  <article>
    <h2>Operator access</h2>
    <label for="operator">Operator ID</label>
    <input id="operator" name="operator" required>
    <button>Continue</button>
  </article>
</div>
```

Unclassed controls outside `.cy-semantic` are not restyled.
If you need glows or static grid effects, add `cyberline.effects.css`
as a third optional file. Don't load `cyberline.all.css` **and** its
individual component files at the same time.

## 4. Responsive applications and accessibility

Use `.cy-region` as the parent for container-responsive patterns such as
`.cy-stats`, `.cy-split`, `.cy-pricing`; width comes from the container,
not the whole viewport. Use `.cy-page` only for a full-page experience.

Cyberline honors `prefers-reduced-motion: reduce`. Theme overrides
must not remove focus outlines, fake disabled states, or communicate state
only through color. Test keyboard navigation, 200%/400% browser zoom,
high-contrast/forced-colors, and relevant screen readers in the target app.

**No runtime JavaScript is required for styling.** Search, authentication,
live data, and server-side form handling are intentionally application
responsibilities; optional advanced widgets are outside the CSS core.

## 5. Seven interchangeable palettes (including light-mode business UI)

Every palette supplies the **same** component tokens and classes. Switch themes
without rewriting markup or installing Tailwind, React or a CSS compiler:

| Theme | Recommended use | Native color scheme |
| --- | --- | --- |
| `data-cy-theme="grid"` | High-contrast signal/cyberpunk dashboards | Dark |
| `data-cy-theme="noir"` | Warm atmospheric interfaces and landing pages | Dark |
| `data-cy-theme="studio"` | SaaS, analytics and business site components | Light |
| `data-cy-theme="industrial"` | Operations consoles and control-room applications | Dark |
| `data-cy-theme="terminal"` | CLI-adjacent tools and developer dashboards | Dark |
| `data-cy-theme="corporate"` | Professional SaaS and B2B application shells | Light |
| `data-cy-theme="minimal"` | Neutral marketing and business websites | Light |

All seven work on `.cy-root` or a nested `[data-cy-theme]` region. Native
controls and scrollbars follow the theme's `color-scheme`. The same markup and
component classes remain usable across all themes. Theme palettes are not
automatic `prefers-color-scheme` overrides; the application chooses a theme.

[Browse all seven themes](../examples/themes.html).

## 6. Optional tiny utilities, not a utility compiler

Load the separate stylesheet **after** the core file. The utility classes are
intentionally finite, scoped to `.cy-root`, and use the same spacing variables:

```html
<link rel="stylesheet" href="/css/cyberline.core.css">
<link rel="stylesheet" href="/css/cyberline.utilities.css">
<div class="cy-root" data-cy-theme="corporate">
  <div class="cy-u-flex cy-u-between cy-u-center cy-u-gap-2">
    <h2>Account overview</h2>
    <a class="cy-button" href="/settings">Settings</a>
  </div>
  <div class="cy-u-grid cy-u-gap-2 cy-u-mt-2">
    <article class="cy-panel cy-u-p-2">Accessible HTML, no runtime JavaScript.</article>
  </div>
</div>
```

Classes: `cy-u-flex`, `cy-u-grid`, `cy-u-stack`, `cy-u-inline`,
`cy-u-between`, `cy-u-center`, `cy-u-gap-1..3`, `cy-u-p-1..3`,
`cy-u-mt-1..3`, and `cy-u-sr-only` for visually hidden text.
No design depends on utilities: existing `cy-shell`, `cy-panel` and
`cy-region` classes continue to work without this file.

**Import choice:** `cyberline.all.css` includes the utility classes;
`cyberline.core.css` and the backwards-compatible `cyberline.css` do not.
