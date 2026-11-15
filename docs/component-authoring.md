# Syntyr component-authoring contract (experimental)

This document defines conventions for application-owned, framework-owned, and
future optional Syntyr-compatible Web Components. It does **not** introduce a
JavaScript API, runtime dependency, or widget package into `@syntyr/css`.

## Public styling contract

1. **Real HTML semantics first:** use `button` for actions, `a` for
   navigation, `label` and correctly associated form controls, native
   `details`/`dialog`/`popover` where supported. A styled generic element
   is not automatically a usable control.
2. **One styling namespace:** use Syntyr classes `.syn-*`, CSS custom
   properties `--syn-*`, and `data-syn-*` only for Syntyr-specific
   presentation state. Do not add a competing global reset or theme registry.
3. **Explicit scope:** document styles require an enclosing `.syn-root`;
   `.syn-semantic` is optional and applies only to its marked subtree.
   Shadow DOM internals must consume inherited tokens via their own styles,
   or explicitly load scoped Syntyr CSS internally.
4. **Theme independence:** components should work under every theme; prefer
   public semantic design tokens over hard-coded palettes and per-theme forks.
5. **State:** use native `disabled`, `checked`, `required`, `aria-pressed`,
   `aria-expanded`, `aria-invalid`, or `aria-busy` where semantically
   appropriate. Use `data-syn-state` only for supplemental visual state,
   and keep any ARIA state synchronized with real behavior.
6. **Events:** reuse standard DOM events when sufficient. If using
   `CustomEvent`, document its name, `detail` payload, dispatch source,
   bubbling and composed behavior. Use `bubbles: true` and `composed: true`
   for consumer-facing events intended to cross a Shadow DOM boundary.
7. **Properties and attributes:** prefer native properties and meaningful
   primitive attributes. Use documented defaults, avoid conflicting states,
   and only reflect state to attributes when useful for external consumers.
8. **Composition:** slots and `::part()` should expose deliberately supported
   customization surfaces, not all internal markup as a permanent API.
   Light DOM components can reuse existing `.syn-*` styles directly.
9. **Progressive enhancement:** preserve readable content and working native
   navigation/form fallbacks if JavaScript is blocked or fails. Interactivity,
   authorization, validation and persistence belong to the host application.
10. **Accessibility:** validate keyboard-only activation and focus order,
    visible `:focus-visible`, accessible names, announced status, motion
    preferences, forced colors, text contrast and zoom/reflow. Do not replace
    accessible native behaviors with untested ARIA patterns.

## Suggested review checklist

- Has an HTML-only fallback when the workflow requires it
- Does not require a particular frontend framework for presentation
- Documents all public tokens, attributes, and emitted custom events
- Works in nested Studio/Grid/Noir themes and a narrow embedded host
- Does not restyle the document outside `.syn-root`
- Maintains accessible state when disabled or busy
- Handles text content safely without raw-HTML interpolation
- Passes cross-engine tests and manual assistive-technology review

## Example boundaries

The optional [Syntyr + Lit sample](https://github.com/dporkka/syntyr-css/tree/main/examples/lit) provides
light-DOM class styling and Shadow DOM token + `::part()` styling. It
demonstrates a `CustomEvent` contract but uses only local demonstration
state. It is not a proposed production widget API.

For stable CSS selector/token guarantees see [API stability](api-stability.md).
For native HTML fallbacks see
[progressive enhancement](progressive-enhancement.md).
