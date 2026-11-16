# Nulang Web + Syntyr CSS

This optional, copy-owned example serves two HTML pages with **Nulang Web** and styles them using the unmodified **Syntyr core CSS**. It needs no Syntyr package, application-authored JavaScript, React, Node.js, or CSS compiler.

## Run

From the Syntyr repository root:

```sh
python3 examples/nulang-web/prepare.py
cd examples/nulang-web
nulang nula dev
# open http://127.0.0.1:3000/
```

Use a Nulang CLI revision that supports the experimental `app` web syntax and `nula dev`. If you built the CLI locally, substitute its absolute binary path for `nulang`.

If an older source-built compiler fails route validation with
`Unknown type name: 'Html'`, set `NULANG_STDLIB` to the absolute path of
your Nulang checkout's `src/stdlib` directory before running the command.
The integration's companion Nulang compiler fix makes this unnecessary for
source-built binaries launched outside the Nulang checkout.

The preparation step copies `../../dist/syntyr.core.css` into this example's `static/` directory. It never edits the canonical stylesheet; the copied artifact is ignored by Git. In your own application, copy the pinned CSS file directly or add the same step to your own build.

For a static build:

```sh
nulang nula build --web
```

The generated site includes the CSS under `dist/`. Nulang may generate its own client runtime artifact, but these static pages do not load it. The only stylesheet used is `syntyr.core.css`; optional Syntyr semantic/recipes/effects modules are not necessary.

## Contract

- Nulang owns routing, rendering, and future interactions.
- HTML uses native element names, escaped `Html` text, normal attributes, and semantic tables/forms.
- Syntyr owns visual presentation through `syn-*` classes and `data-syn-theme`.
- `.syn-root` is on the stable page body, not inside an element that would be replaced by a client update.
- Navigation and the GET form work without JavaScript; the example performs no mutations and uses no unsafe `raw()` interpolation.
- For interactive signals, use Nulang's native state to update `aria-*`, `data-syn-state`, or `class` attributes; Syntyr never owns state.

**Limitations:** Nulang's Web host remains experimental. This demo is not a security or production-readiness certification. For dynamic partial updates, preserve the theme ancestor, focus, and unrelated attributes; verify actual browser behavior before shipping.
