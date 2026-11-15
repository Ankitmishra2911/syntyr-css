# Copy-owned form recipes

These are **MIT-licensed, plain-HTML examples**. Copy and modify them without installing a Syntyr CLI, template registry, React, or a JavaScript runtime. Syntyr provides presentation; your browser and application provide behavior.

Load `dist/syntyr.core.css` and apply `.syn-root` on a stable ancestor. Input groups and fields are included in core. The examples below also work in Go/templ, Askama, Django templates, Astro, React, and HTMX.

## 1. Labeled field with assistance and server-side validation

```html
<div class="syn-root" data-syn-theme="studio">
  <div class="syn-field">
    <label class="syn-label" for="email">Work email</label>
    <input class="syn-input" id="email" name="email" type="email"
           autocomplete="email" aria-invalid="true"
           aria-describedby="email-help email-error" required>
    <p class="syn-help" id="email-help">Use your company email address.</p>
    <p class="syn-error" id="email-error">Enter a valid work email.</p>
  </div>
</div>
```

Only render `aria-invalid="true"` and the error message when the form is actually invalid. Do not use CSS as a substitute for server-side validation. The field class groups presentation; the native `label for` association supplies the accessible name.

## 2. Search field with a connected button

```html
<search class="syn-root" data-syn-theme="studio" aria-label="Search accounts">
  <form method="get" action="/accounts">
    <div class="syn-field">
      <label class="syn-label" for="account-query">Account name</label>
      <div class="syn-input-group">
        <input class="syn-input" id="account-query" name="q"
               type="search" placeholder="Search accounts">
        <button class="syn-button syn-button--primary" type="submit">Search</button>
      </div>
    </div>
  </form>
</search>
```

This is **progressive enhancement**: the GET form submits with **No JavaScript**. An HTMX application may add `hx-get` and `hx-target` while preserving `action`, `method`, and a server-rendered fallback. The application must implement the endpoint and return actual search results.

## 3. Input addon (currency and unit)

```html
<div class="syn-root" data-syn-theme="studio">
  <div class="syn-field">
    <label class="syn-label" for="monthly-budget">Monthly budget (USD)</label>
    <div class="syn-input-group">
      <span class="syn-input-addon" aria-hidden="true">$</span>
      <input class="syn-input" id="monthly-budget" name="budget"
             type="number" min="0" step="0.01" inputmode="decimal">
      <span class="syn-input-addon" aria-hidden="true">USD</span>
    </div>
  </div>
</div>
```

The unit is included in the label, not only in the decorative addon; assistive technologies must not depend on a symbol alone. Keep addons concise; overly long addons can compress their associated input.

## 4. Container-responsive horizontal form

```html
<form class="syn-root syn-region syn-form" action="/settings" method="post"
      data-syn-theme="corporate">
  <div class="syn-field-row">
    <label class="syn-label" for="org-name">Organization</label>
    <div class="syn-field-body">
      <input class="syn-input" id="org-name" name="organization"
             aria-describedby="org-help" required>
      <p class="syn-help" id="org-help">Visible to members of your team.</p>
    </div>
  </div>
  <button class="syn-button syn-button--primary" type="submit">Save</button>
</form>
```

The `syn-region` container determines whether rows become horizontal at 42rem. Without that ancestor they remain safely stacked. This is intentionally not a full grid/breakpoint framework. The help text is associated with its input via `aria-describedby`. A production POST endpoint must handle authorization, validation and CSRF.

## Optional companion styles

- [Radix Primitives state styling](radix-integration.md) provides an opt-in adapter for React applications while keeping Radix responsible for keyboard behavior.
- shadcn/ui components can adopt Syntyr tokens in application-owned CSS. Modern color variables can use values such as `--background: var(--syn-bg)` and `--foreground: var(--syn-text)`, **only when** the shadcn component expects complete CSS color values. Older `hsl(var(--background))` consumers require an HSL-channel bridge instead; do not apply the mappings blindly.
- `syntyr.semantic.css` remains a separate opt-in style for unclassed native HTML. Do not apply it indiscriminately around other component libraries.

See [the static form showcase](../examples/form-composition.html) and the [main component contract](components.md).

## Server-owned validation and local component variables (alpha.5 candidate)

Syntyr does **not** validate data, track touched fields, submit forms, or
announce errors automatically. The server should return the invalid form with
`aria-invalid="true"` on the affected field, an associated error via
`aria-describedby`, and optionally a visible error summary containing real
fragment links to the invalid fields. The browser's native `:user-invalid`
and `:user-valid` states style fields after user interaction where supported;
server-confirmed valid values may opt into
`data-syn-validation="valid"` (a **visual hint**, not ARIA and not proof).
Do not display success styling on untouched inputs. Never render an error
summary merely to hide it with CSS; omit it when the form is valid.

The optional `.syn-error-summary` class from `syntyr.recipes.css` leaves the summary visible and readable
in forced-colors mode. If the server inserts the message following a submit,
the host application determines focus, announcement and validation logic.

For one-off app themes, override **component-local CSS custom properties**
rather than selectors. Examples: `--syn-button-bg`,
`--syn-button-color`, `--syn-button-border-color`,
`--syn-button-hover-bg`, `--syn-panel-bg`,
`--syn-panel-border-color`, `--syn-field-bg`,
`--syn-field-border-color`, `--syn-field-valid-border-color`,
and `--syn-field-invalid-border-color`. All use existing Syntyr theme tokens
as fallbacks. Set the variables on the actual element or a containing
theme scope; they do not require Sass or JavaScript. For button color changes,
choose foreground/hover colors that meet applicable contrast requirements.

[See the static example with server-error, valid, disabled and token states](../examples/form-state-contracts.html).
