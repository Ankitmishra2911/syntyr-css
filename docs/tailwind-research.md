# What Syntyr borrows conceptually from Tailwind CSS and Tailwind Plus

Research updated 2026-11-14. **This project contains no Tailwind Plus component code, markup, graphics, screenshots, or licensed assets.** Tailwind CSS and Tailwind Plus are third-party products; Syntyr is independent.

## Engineering comparison

| Tailwind idea | Syntyr adaptation | Reason |
| --- | --- | --- |
| CSS-first theme configuration and native variables (Tailwind v4) | Public `--syn-*` CSS tokens in a layered stylesheet | Works without Tailwind, JS, config files, or compilation |
| Cascade layers and predictable override priority | `syn.tokens`, `syn.base`, `syn.components`, `syn.semantic`, `syn.effects` | Preserve host-app override control and prevent unscoped resets |
| Container query responsiveness | `.syn-region` with a named container; `.syn-stats`, `.syn-split`, `.syn-pricing` respond to their container | Embeds remain responsive in narrow panels and sidebars |
| Variants driven by attributes | Native `aria-pressed`, `aria-busy`, `aria-current`, opt-in `data-syn-state` and `data-syn-featured` | Accessible state where semantic; decorative state without false semantics |
| Theme composition in ordinary CSS | Grid/Noir token scopes via `data-syn-theme`; unlayered application CSS overrides | Predictable theme customizations with zero compiler |
| Responsive reusable UI recipes | Composable named CSS classes plus HTML partials | Better fit for server templates and avoids dozens of atomic classes |
| Tailwind Plus application UI categories and whole-page kits | Free primitives and free examples; separately authored paid complete layouts | Business value comes from workflow-complete templates, not essential CSS access |
| Tailwind Plus one-time licensing | Pilot one-time kit purchase with perpetual rights to purchased versions | More credible initial model than forcing subscriptions for static files |

## Ideas deliberately rejected

- No full Tailwind-style general-purpose utility compiler or class scanner. Those create build-system and markup complexity contrary to Syntyr's explicit constraints.
- No Tailwind `@theme`, `@utility`, or `@apply` directives in Syntyr CSS: these are Tailwind-specific compile-time syntax, not browser-standard CSS features.
- No default dependency on Tailwind Plus Elements or its JavaScript. Use native HTML, with optional host-owned JS for complex interactions.
- No Tailwind Plus components, snippets, or templates copied into Syntyr. Their commercial license restricts redistributing derivative component libraries and template products.
- No Tailwind CSS branding or entertainment franchise assets in Syntyr deliverables.

## Primary sources

- [Tailwind CSS v4 overview](https://tailwindcss.com/blog/tailwindcss-v4)
- [CSS theme variables](https://tailwindcss.com/docs/theme)
- [Responsive design/container queries](https://tailwindcss.com/docs/responsive-design)
- [ARIA/data state variants](https://tailwindcss.com/docs/hover-focus-and-other-states)
- [Tailwind Plus application UI taxonomy](https://tailwindcss.com/plus/ui-blocks/application-ui)
- [Tailwind UI rebrand and one-time licensing](https://tailwindcss.com/blog/tailwind-plus)
- [Tailwind Plus FAQ and commercial restriction examples](https://tailwindcss.com/plus/templates/syntax)
- [Tailwind Plus HTML interaction dependency](https://tailwindcss.com/plus/ui-blocks/documentation/using-html)

## Recommendation

Build **the simplest coherent branded CSS vocabulary**, plus browser-tested original compositions. Syntyr should not chase parity with the enormous Tailwind utility surface or advertise artificial savings from avoiding a build step when a team's existing build tooling is already reliable. The premium product should be *complete application screens* where buyer time saved is observable.
