# Syntyr ecosystem interoperability (alpha.5 source candidate)

All adapters are **opt-in**. Syntyr core still ships ordinary CSS with zero
JavaScript, runtime dependencies, required compiler, or global theme reset.
These files are for current source/prerelease testing, **not claims of registry,
VS Code Marketplace, or Figma Community publication**.

## Tailwind CSS v4: coexist, don't migrate

Use Tailwind for layout and Syntyr for presentation. Tailwind 4's `@theme inline`
can expand Syntyr's scoped runtime variables into utility styles. No plugin,
config file, or Tailwind dependency is added to the Syntyr core.

In the consuming project's stylesheet, with Tailwind v4 installed there:

```css
@import "tailwindcss";
@import "@syntyr/css/core.css";
@import "@syntyr/css/tailwind.css";
```

The scoped palette stays on a real ancestor. Utilities work on that element
and its descendants:

```html
<section class="syn-root" data-syn-theme="grid">
  <div class="grid gap-4 md:grid-cols-2">
    <article class="syn-panel bg-syntyr-surface text-syntyr-text">
      <h2 class="syn-heading">System status</h2>
      <button class="syn-button syn-button--primary">Inspect</button>
    </article>
  </div>
</section>
```

The generated bridge is `integrations/tailwind/syntyr.theme.css`; the
`@syntyr/css/tailwind.css` package subpath is **prepared for the future npm
release** and can be tested with a local `npm pack`. Do not claim it is
already available on npm. If using copied CSS, put the bridge in the host's
Tailwind-processed entrypoint: **browsers do not process `@theme` by
themselves**.

The `bg-syntyr-*` utilities consume `--syn-*` values **at the element**, so
nested `data-syn-theme` regions can change the palette. This requires a
nearest `.syn-root` and proper Syntyr CSS loading. The bridge intentionally
doesn't map Tailwind's global `primary`, `background`, or `border`
tokens: that would silently recolor unrelated Tailwind/shadcn components.

Tailwind Preflight can reset ordinary HTML elements globally; Syntyr's explicit
`syn-*` classes and `.syn-root` scope reduce but do not eliminate cascade
interactions. Test forms, headings, portals, reset order, focus indicators and
nested themes in the actual host app. Don't load `syntyr.all.css` alongside
`core.css`.

Source: https://tailwindcss.com/docs/theme

## VS Code: local extension and metadata

`integrations/vscode/` is a **locally packageable**, extension-host-free
manifest. It contributes VS Code's standard HTML and CSS custom data, plus
snippets for HTML, JSX, and TSX. It bundles generated copies of Syntyr
metadata, so users of the extension don't need to change each workspace's
`.vscode/settings.json`.

For manual testing, in `integrations/vscode/` package with the optional
developer tool `@vscode/vsce`:

```sh
npx @vscode/vsce package --no-dependencies
code --install-extension syntyr-css-*.vsix
```

The `syntyr-local` publisher identifier is intentionally a placeholder for
local testing; **no VS Code Marketplace listing or ownership is claimed**.
Publication requires a verified publisher, reviewed metadata and packaging.

For developers who don't want an extension, use the existing copy-and-configure
approach in [editor integration](editor-integration.md). Native VS Code custom
data provides HTML/CSS language features, but does not guarantee class-name
completion in every JSX/TSX editor mode. The bundled snippets support those
languages explicitly.

Source: https://code.visualstudio.com/api/extension-guides/custom-data-extension

## Figma: importable tokens, not a component library yet

`metadata/figma/syntyr-<theme>.tokens.json` contains an independent DTCG
design-token mode for each of **seven alpha.5 source themes**. These exports
are generated from literal CSS palette values; each file has the same
color and dimension token names and types.

In Figma Design's Variables view, create a token collection and import the
Studio file first. Import the other files as additional modes under that
collection, using Figma's **Import mode** control. Check the resulting variables
before publishing a shared library.

The exported values include thirteen literal SRGB palette colors and
`radius`/`cut` dimensions. Root `rem` is converted to px using an
**assumed 16px root size** for editable design coordinates; browser CSS
continues to use `rem`. Derived `color-mix()` values, `auto` mode and
component-specific expressions are excluded rather than approximated. A
genuine Figma **component library** (Auto Layout, variants, responsive
compositions, design/code parity) is separate work, not delivered by token
JSON alone.

Source: https://help.figma.com/hc/en-us/articles/15343816063383-Modes-for-variables

## Keeping exports synchronized

After changes to `src/tokens.css` or editor API metadata:

```sh
python3 scripts/export_api_metadata.py
python3 scripts/export_ecosystem_adapters.py
python3 scripts/export_api_metadata.py --check
python3 scripts/export_ecosystem_adapters.py --check
python3 -m unittest discover -s tests -p test_ecosystem_adapters.py -v
```

The Python generator fails closed if a source palette is missing, duplicated,
or contains an unsupported nonliteral token. It doesn't modify `dist/` or
insert any adapter into a production stylesheet by default.

## Deferred integrations

- **shadcn/ui and daisyUI**: test an explicit, opt-in semantic bridge only
  after the Tailwind coexistence example runs in a representative real app;
  do not overwrite global component tokens.
- **Storybook**: add browser-backed reference stories and contrast/state
  coverage, with dev-only tooling.
- **Webflow and Framer**: start with tested templates and import guides rather
  than platform-specific component forks.
