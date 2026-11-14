# Advanced frames and terminal presentation

These are original, MIT-licensed Cyberline CSS components. They do not replicate entertainment franchise assets or require JavaScript.

## Installation

Load only the modules you need. Advanced geometry is a separate file so the small core stays within its 5 KiB gzip budget:

```html
<link rel="stylesheet" href="/css/cyberline.core.css">
<link rel="stylesheet" href="/css/cyberline.geometry.css">
<!-- Only for the optional application/terminal layouts: -->
<link rel="stylesheet" href="/css/cyberline.recipes.css">
```

The all-in-one stylesheet includes geometry and recipes already. Do not load it alongside the individual modules.

## Five independent frame profiles

Use `.cy-frame` with exactly **one** shape modifier. These can decorate an article, section, or any normal element. The surrounding content stays semantic:

```html
<section class="cy-root" data-cy-theme="grid">
  <article class="cy-panel cy-frame cy-frame--bevel" style="--cy-frame-cut: 1.5rem">
    <h2>Monitoring</h2>
    <p>All systems operational.</p>
    <a href="/status">See status</a>
  </article>
</section>
```

| Class | Purpose |
| --- | --- |
| `.cy-frame--bevel` | Diagonal cut on all four corners |
| `.cy-frame--notch` | Asymmetric top-right and bottom-left cuts |
| `.cy-frame--bracket` | Four HUD-style L-shaped corner markers |
| `.cy-frame--inset` | Nested technical border |
| `.cy-frame--circuit` | Subtle corner trace bars |

These style variables are inherited and can be overridden on a specific panel:

- `--cy-frame-cut`: default `1rem`; controls bevel/notch/corner size
- `--cy-frame-stroke`: default `1px`; border thickness
- `--cy-frame-fill`: default `var(--cy-surface)`; interior background
- `--cy-frame-outline`: default `var(--cy-frame-strong)`; border tone

**Important:** Advanced frame profiles own both pseudo-elements of the host node. Do not combine them on the same element with `.cy-panel--cut` or the older `.cy-frame--precision` variant, which also uses pseudo-elements. Nest elements if you need to combine decorations. The clipped border geometry does not depend on a matching parent background.

In forced-colors mode, decorative pseudo-elements disappear and a visible native border and Canvas background take over. Frames should not be the only way you communicate operational state.

## Browser terminal

Load `cyberline.recipes.css` for the existing `.cy-terminal` base and the additional presentation classes:

| Class | Role |
| --- | --- |
| `.cy-terminal-bar`, `.cy-terminal-title`, `.cy-terminal-dots` | Window chrome; mark visual-only dots `aria-hidden="true"` |
| `.cy-terminal-body`, `.cy-terminal-line`, `.cy-terminal-output` | Readable lines, wrapped output |
| `.cy-terminal-command`, `.cy-terminal-path`, `.cy-terminal-prompt` | CLI command anatomy |
| `.cy-terminal-success`, `.cy-terminal-warning`, `.cy-terminal-error` | Colored output (with textual status) |
| `.cy-terminal-meta`, `.cy-terminal-muted` | Secondary readouts |
| `.cy-terminal-cursor` | Static decorative caret; hide from accessibility APIs |

The terminal is **not** a shell emulator. It performs no input capture or commands. Applications implement real interaction separately; native CLI applications use `terminal/palettes.json` rather than browser CSS.

## Table and button behavior

The existing `.cy-table-emphasis` class highlights whichever cell you choose: there is no implicit highlight on the last column. Use `.cy-cell--numeric` on monetary or numeric cells for right-aligned tabular numbers.

The native HTML `disabled` attribute blocks button activation. The ARIA `aria-disabled="true"` attribute only communicates a disabled state; it **does not block activation**. Application/server code must enforce disabled behavior. CSS alone cannot guarantee it. For a disabled action that must remain discoverable to keyboard users, preserve focus and handle input appropriately.

## Validation

```sh
python3 scripts/build.py
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v
python3 tests/browser_matrix.py --browsers chromium firefox webkit
```

See [the frame + terminal example](../examples/geometry-terminal.html). Browser checks are developer-only; the distributed CSS still has zero runtime JS or dependencies.
