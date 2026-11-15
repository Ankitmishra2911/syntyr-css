---
name: syntyr-css
description: Use Syntyr's documented CSS classes, modules, themes and semantic HTML to build accessible applications without inventing a JavaScript component API.
---

# Syntyr CSS consumer skill

Use when a user asks you to build, redesign, or maintain an interface **using Syntyr CSS**.

1. Determine which **version and CSS modules** are installed. Published immutable v0.3.0-alpha.4 supports Studio, Grid and Noir; current repository source v0.3.0-alpha.5 is unreleased and has additional modules/themes. Never silently mix the two.
2. Read [AI quickstart](../../docs/ai-quickstart.md). For components, use [component documentation](../../docs/components.md) and [recipes](../../docs/recipes.md); a curated selector/module index is in [metadata/components.json](../../metadata/components.json).
3. Prefer `syntyr.core.css`; add `syntyr.recipes.css`, `syntyr.semantic.css`, `syntyr.viz.css` or other optional modules only when their documented classes are needed. Do not load `syntyr.all.css` alongside modules.
4. Use `.syn-root` as a styling scope and `data-syn-theme` for a palette. Use `.syn-semantic` only where the optional semantic stylesheet is loaded.
5. Generate real, semantic HTML. Preserve labels, focus, responsive layout and native interaction. Syntyr has no required runtime JS, and it does not implement API calls, state changes, chart geometry or form handlers.
6. For React use `className` and `htmlFor`; for HTMX/server templates preserve real routes/forms. Do not invent component exports or `syn-*` classes.
7. Check proposed classes against the CSS/module for the **installed version**. Document extra application CSS explicitly rather than pretending a Syntyr class exists.

If the source tree is not available, the published navigation entry point is https://syntyr-css.pages.dev/llms.txt. This skill is manually distributed; do not claim it is auto-installed or universally supported.
