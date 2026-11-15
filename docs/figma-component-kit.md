# Syntyr Figma Component Kit — alpha.5 preview

[Open the editable Syntyr Figma kit](https://www.figma.com/design/Lj8uKUtgJfXMyzVb96x5Q1)

This is a **first component-library pilot**, not a published Figma Community
library or a complete replacement for browser rendering.

## What exists

- Seven independent single-mode color variable collections: Studio, Grid,
  Noir, Industrial, Terminal, Corporate and Minimal.
- Four native reusable components using Studio variables: primary button,
  outline button, default panel and success status.
- An instance-based review frame with editable text and auto-layout.
- CSS token code syntax (`var(--syn-*)`) and descriptive component names.

Figma Starter mode limits this file to **one mode per collection**, so all seven
themes are separate collections rather than seven switchable modes. Do not
claim that theme switching works on the same component instance.

## Source of truth and parity

CSS: `src/tokens.css`, `src/components/buttons.css`,
`src/components/data.css`. Machine-readable palettes:
`metadata/figma/syntyr-<theme>.tokens.json`.

Studio reference values: background #F5F7FB, surface #FFFFFF,
text #15233A, accent #2458C6, accent foreground #FFFFFF,
border #B8C6D8, success #17694B. Button minimum height 44px,
14px semi-bold type, 16px horizontal padding and 4px corners
(normal CSS `--syn-radius` .25rem at a 16px root).

The pilot uses Inter as a practical local font substitute for
Syntyr's platform system font stack; it is **not exact typography parity**.
Native hover, focus-visible, disabled behavior and geometry effects
remain browser responsibilities. Browser validation and contrast testing
are required before publishing or distributing this as a production kit.

## Next Figma steps

- Add a coherent Button component set with state and size variants and
  variable bindings for all applicable states.
- Add spacing, typography and semantic alias variables.
- Add native input, table, card, navigation and accessible form patterns.
- Validate on-canvas components against CSS screenshots across themes.
- Upgrade Figma plan only if a single collection with seven modes is needed.
