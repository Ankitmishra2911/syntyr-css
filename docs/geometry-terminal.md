# Advanced frames and terminal presentation

These are original, MIT-licensed SYNTYR CSS components. They do not replicate entertainment franchise assets or require JavaScript.

## Installation

Load only the modules you need. Advanced geometry is a separate file so apps need not fetch extra frame CSS when they only use the core:

```html
<link rel="stylesheet" href="/css/syntyr.core.css">
<link rel="stylesheet" href="/css/syntyr.geometry.css">
<!-- Only for the optional application/terminal layouts: -->
<link rel="stylesheet" href="/css/syntyr.recipes.css">
```

The all-in-one stylesheet includes geometry and recipes already. Do not load it alongside the individual modules.

## Five independent frame profiles

Use `.syn-frame` with exactly **one** shape modifier. These can decorate an article, section, or any normal element. The surrounding content stays semantic:

```html
<section class="syn-root" data-syn-theme="grid">
  <article class="syn-panel syn-frame syn-frame--bevel" style="--syn-frame-cut: 1.5rem">
    <h2>Monitoring</h2>
    <p>All systems operational.</p>
    <a href="/status">See status</a>
  </article>
</section>
```

| Class | Purpose |
| --- | --- |
| `.syn-frame--bevel` | Diagonal cut on all four corners |
| `.syn-frame--notch` | Asymmetric top-right and bottom-left cuts |
| `.syn-frame--bracket` | Four HUD-style L-shaped corner markers |
| `.syn-frame--inset` | Nested technical border |
| `.syn-frame--circuit` | Subtle corner trace bars |

These style variables are inherited and can be overridden on a specific panel:

- `--syn-frame-cut`: default `1rem`; controls bevel/notch/corner size
- `--syn-frame-stroke`: default `1px`; border thickness
- `--syn-frame-fill`: default `var(--syn-surface)`; interior background
- `--syn-frame-outline`: default `var(--syn-frame-strong)`; border tone

**Important:** Advanced frame profiles own both pseudo-elements of the host node. Do not combine them on the same element with `.syn-panel--cut` or the older `.syn-frame--precision` variant, which also uses pseudo-elements. Nest elements if you need to combine decorations. The clipped border geometry does not depend on a matching parent background.

In forced-colors mode, decorative pseudo-elements disappear and a visible native border and Canvas background take over. Frames should not be the only way you communicate operational state.

## Browser terminal

Load `syntyr.recipes.css` for the existing `.syn-terminal` base and the additional presentation classes:

| Class | Role |
| --- | --- |
| `.syn-terminal-bar`, `.syn-terminal-title`, `.syn-terminal-dots` | Window chrome; mark visual-only dots `aria-hidden="true"` |
| `.syn-terminal-body`, `.syn-terminal-line`, `.syn-terminal-output` | Readable lines, wrapped output |
| `.syn-terminal-command`, `.syn-terminal-path`, `.syn-terminal-prompt` | CLI command anatomy |
| `.syn-terminal-success`, `.syn-terminal-warning`, `.syn-terminal-error` | Colored output (with textual status) |
| `.syn-terminal-meta`, `.syn-terminal-muted` | Secondary readouts |
| `.syn-terminal-cursor` | Static decorative caret; hide from accessibility APIs |

The terminal is **not** a shell emulator. It performs no input capture or commands. Applications implement real interaction separately; native CLI applications use `terminal/palettes.json` rather than browser CSS.

## Table and button behavior

The existing `.syn-table-emphasis` class highlights whichever cell you choose: there is no implicit highlight on the last column. Use `.syn-cell--numeric` on monetary or numeric cells for right-aligned tabular numbers.

The native HTML `disabled` attribute blocks button activation. The ARIA `aria-disabled="true"` attribute only communicates a disabled state; it **does not block activation**. Application/server code must enforce disabled behavior. CSS alone cannot guarantee it. For a disabled action that must remain discoverable to keyboard users, preserve focus and handle input appropriately.

## Validation

```sh
python3 scripts/build.py
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v
python3 tests/browser_matrix.py --browsers chromium firefox webkit
```

See [the frame + terminal example](../examples/geometry-terminal.html). Browser checks are developer-only; the distributed CSS still has zero runtime JS or dependencies.
