# SYNTYR name migration

**2026-11-14:** The open-source project previously called **Cyberline CSS**
now uses the public name **SYNTYR**. The source repository is
[dporkka/syntyr-css](https://github.com/dporkka/syntyr-css).

## Existing integrations keep working

All existing CSS classes and design tokens, including `cy-root`, `cy-button`,
`cy-semantic`, `--cy-accent`, and `data-cy-theme`, are **unchanged**. The
`cy-` prefix is a stable public API, not a marketing label.

New projects should load `syntyr.core.css` (with optional
`syntyr.semantic.css`, `syntyr.recipes.css`, and `syntyr.effects.css`).
The old `cyberline.core.css` and all other `cyberline.*.css` files are
still produced from the exact same sources and remain byte-identical to their
SYNTYR counterparts. No imports or selectors need to change in existing
projects. The legacy paths are included in the release ZIP.

The GitHub repository rename redirects GitHub repo URLs, but **GitHub Pages
subpath URLs are not guaranteed to redirect**. Update bookmarks and
documentation links from `/cyberline-css/` to `/syntyr-css/` once GitHub
Pages publishes the new path. Pin to a release tag rather than the moving
main branch in production.

MIT licensing and the scope of the optional commercial Console Kit concept
are unchanged.

## Brand clearance

SYNTYR is the selected project name, **not yet legally cleared**.
Review active and related marks in software Classes 9 and 42 (including
SYNTER and SYNCYR) in the USA, Brazil and any intended sales markets.
Do not claim registered rights or accept paid brand commitments until
the clearance gate is complete. See [the preliminary screen](../business/syntyr-trademark-screen.md).
