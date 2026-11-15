# Opt-in Syntyr ↔ shadcn/ui semantic token bridge

The bridge at `integrations/shadcn/syntyr.tokens.css` maps documented
shadcn/ui roles to Syntyr variables **only within** a `.syn-shadcn`
subtree of `.syn-root`. It leaves the Syntyr runtime, global `:root`,
`.dark` and the host application's other Tailwind/shadcn components
untouched. It contains **no JavaScript or Tailwind compiler instructions**.

## Integration

Use your shadcn project as normal, with `tailwind.cssVariables: true`.
Import the Syntyr CSS **after** core, and keep your application's own
shadcn `@theme inline` mapping:

```css
@import "tailwindcss";
@import "@syntyr/css/core.css";
@import "@syntyr/css/shadcn.css";

/* Your shadcn CSS already defines these mappings: */
@theme inline {
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-background: var(--background);
  --color-foreground: var(--foreground);
}
```

```html
<section class="syn-root syn-shadcn" data-syn-theme="studio">
  <button class="bg-primary text-primary-foreground">Action</button>
  <div data-syn-theme="noir" class="bg-card text-card-foreground">
    Nested Noir region
  </div>
</section>
```

Nested `data-syn-theme` regions **redeclare** shadcn aliases so CSS
custom-property computed values do not freeze at the ancestor palette.

The adapter is not a fork, registry distribution of shadcn components,
or a replacement for Radix focus management. The fixture at
`examples/shadcn-bridge/` compiles actual shadcn **semantic utility
classes** with Tailwind v4, but it does **not yet verify a real generated
React/Radix/shadcn component**. Portal placement, component-owned classes,
keyboard interaction, errors and color contrast must be checked when used
in a production shadcn project.

Official theming reference:
https://ui.shadcn.com/docs/theming

**Release status:** the `@syntyr/css/shadcn.css` subpath exists in
the local package manifest but remains unpublished until an authorized
prerelease is made.
