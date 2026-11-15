# Nulang and Syntyr — optional integration

Syntyr CSS is **not bundled into Nulang**, and Nulang is **not a Syntyr runtime dependency**. This is a reference integration for two independent projects: Nulang renders HTML and owns state/actions; Syntyr supplies static styles.

**Status:** Experimental adapter/source examples for Syntyr alpha.5, not a released Nulang library or production action runtime. The Nulang Web framework and `nulang-ui/1` protocol are experimental. Pin tested versions of both projects.

## Path A: Style a real Nulang Web application

See the [Nulang Web sample source](https://github.com/dporkka/syntyr-css/tree/main/integrations/nulang/web-example), which follows Nulang's own `examples/hello-web` package patterns. The page uses native `Html` elements with `syn-root`, `syn-panel`, `syn-heading`, `syn-badge` and `syn-button` classes. No Syntyr-specific compiler, component runtime, or JavaScript is required.

Run it from a checkout containing `integrations/nulang/web-example`:

```sh
cd integrations/nulang/web-example
mkdir -p static
cp ../../../dist/syntyr.core.css static/syntyr.core.css
nulang nula dev
```

The `[web]` config mounts `static/` for `/syntyr.core.css`. The link is same-origin; do not depend on remote fonts, script bundles, or a CSS CDN. For a static deployment, try `nulang nula build --web` and inspect the generated `dist/`. Nulang's **development host may inject its own client runtime**, entirely separate from Syntyr. Production behavior and security depend on Nulang and its host configuration.

The Nulang example was reviewed against Nulang's current Web examples and documentation. **It has not been compiled or served in this Syntyr validation run:** a native Nulang executable was not available on the test device. Do not treat static source checks as proof of Nulang compiler/runtime compatibility.

## Path B: Render a restricted `nulang-ui/1` semantic document

The independent Python 3 standard-library adapter `integrations/nulang/render.py` reads the authentic Nulang UI document envelope:

- `protocol: "nulang-ui/1"`, `document_id`, `revision` as a decimal string, `root`, and `nodes`.
- Each node has a stable `id`, `kind`, tagged typed `properties`, ordered `children` references, and optional `actions`.
- The adapter's **opt-in kinds**, which are not universal Nulang kind semantics, are `column`, `row`, `panel`, `heading`, `text`, `badge`, `metric`, and `link`.
- Only leaf properties defined by the adapter are permitted; strings use `{"type":"string","value":"..."}`, and numeric metrics can use lossless `{"type":"i64","value":"42"}`.

Run from the Syntyr repository root:

```sh
python3 integrations/nulang/render.py \
  --input integrations/nulang/sample-ui.json \
  --output examples/nulang-ui.html
python3 integrations/nulang/render.py \
  --input integrations/nulang/sample-ui.json \
  --output examples/nulang-ui.html --check
python3 scripts/syntyr_check.py examples/nulang-ui.html
```

The generated [Syntyr-styled Nulang UI preview](../examples/nulang-ui.html) is static HTML. It references the repository's built `dist/syntyr.core.css` with a local relative URL. You can opt into a different supported theme using `--theme grid` or change the local CSS path with `--css`.

This is a **snapshot renderer**, not a Nulang host or a UI client. In particular, Nulang's compiler-produced `SignalGraph.to_ui_document()` emits `interaction_root`, `signal`, `signal_read` and `action` nodes that express relationships, **not a second DOM tree**. The adapter rejects these rather than inventing markup. It also rejects action bindings instead of producing buttons that appear to work but do nothing; action placement, dispatch, authorization, idempotency, and incremental patches stay with the Nulang runtime/host.

### Contract, safety, and limits

The renderer checks that every class it uses is available in Syntyr's generated `metadata/syntyr-contract.json` and in `syntyr.core.css`. It validates protocol version, node identity and graph structure, depth, typed attributes, themes, and link URLs. Text and HTML attributes are escaped; arbitrary tags, CSS, event handlers and scripts are not allowed. It validates only a small documented subset, with a maximum of 512 nodes and 64 levels; it is **not** a replacement for Nulang's Rust protocol validator, template escape rules, or browser accessibility tests.

To support real Nulang interactions, write a separate explicitly trusted renderer/host integration that forwards actions and patches to Nulang, with its own security boundary and end-to-end tests. A static preview is intentionally not that host.

### Verification

On this Syntyr branch, `tests/test_nulang_integration.py` validates supported schema rendering, HTML injection escaping, unsafe URL rejection, action refusal, malformed graphs and class provenance; the checked-in preview is rebuilt deterministically and analyzed by Syntyr's static checker. The Nulang compiler and browser action dispatch are **not** covered by these tests.
