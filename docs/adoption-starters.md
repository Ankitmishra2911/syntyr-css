# Runnable adoption fixtures

These fixtures exercise a **real consuming build** using the local Syntyr
CSS-only package. They are independent, optional development projects.

## Tailwind CSS v4

[Source](../examples/tailwind-v4/) — one HTML page using Tailwind utility
layout plus namespaced Syntyr tokens and components. It includes nested
Noir styling and exercises the generated Tailwind `@theme inline` bridge.

```sh
cd examples/tailwind-v4
npm install
npm run build
python3 -m http.server 8000
```

## Astro

[Source](../examples/astro/) — static Astro application using Syntyr's
`core.css` package subpath. No browser JavaScript is needed for the UI.

```sh
cd examples/astro
npm install
npm run build
npm run preview
```

## shadcn/ui semantic token compatibility

[Source](../examples/shadcn-bridge/) — a Tailwind v4 project exercising
scoped shadcn semantic colors, a nested Noir palette and host isolation.
This exercises shadcn-style utility output, not an actual generated React
component. See the [adapter guide](shadcn-integration.md).

```sh
cd examples/shadcn-bridge
npm install
npm run build
python3 -m http.server 8000
```

All three starters refer to `"@syntyr/css": "file:../.."` to avoid implying
the alpha.5 package is published. Replace this with an actual pinned version
after npm release. Generated assets, caches and dependencies are ignored.

The Syntyr core package itself still requires no Node, Astro, Tailwind or
other runtime dependency.
