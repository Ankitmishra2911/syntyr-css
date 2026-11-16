# Progressive enhancement and document rendering

Syntyr's default contract is **HTML first**. Core CSS doesn't include JavaScript,
network requests, icons, fonts or a client-side build step. Progressive enhancement
should add polish and optional interactions to working baseline workflows.

For a static showcase of `search`, `figure`, `mark`, `kbd`, `output`, `meter` and safe code overflow with zero scripts, see [native-elements.html](../examples/native-elements.html). The example is presentational, not a working search service.

## Native actions and server responses come first

Always use anchors for navigation, buttons for actions, associated labels for
controls, and native form submission where the application has a server endpoint.
A GET form below remains usable without HTMX, React, or other client JavaScript:

```html
<form action="/customers" method="get" role="search">
  <label for="q">Search customers</label>
  <input id="q" name="q" type="search" required>
  <button type="submit" class="syn-button syn-button--primary">Search</button>
</form>
```

HTMX or other adapters can enhance the same form. Return safe server-rendered
HTML; handle validation and permissions on the server. If the enhancement fails,
the form still navigates to the server search result. The host owns those routes.

Native `details` is appropriate for disclosure. For a modal preview, include a
real navigation route for critical information because `commandfor` and
`command="show-modal"` are not universally supported in older browsers:

```html
<a href="/reports/quarterly">Read full report</a>
<button type="button" commandfor="report-preview" command="show-modal">
  Preview report
</button>
<dialog id="report-preview" aria-labelledby="report-preview-title">
  <h2 id="report-preview-title">Report preview</h2>
  <p>Illustrative summary. The full report link works in every browser.</p>
  <form method="dialog"><button>Close</button></form>
</dialog>
```

Don't rely on ARIA to implement state changes or disable interactions. Use
native control semantics; any optional JavaScript must feature-detect browser
support, preserve keyboard focus, and never hide the only path to important data.

## Escalation ladder: add only the behavior the platform cannot supply

| Need | Prefer | When to add a dependency |
| --- | --- | --- |
| Links, form submission, validation | Native `a`, `form`, `input` and server responses | Only for workflow requirements beyond the browser |
| Disclosure, modal, basic popover | `details`, `dialog` and `popover` | A tested fallback if target browsers lack the required primitive |
| Responsive component presentation | CSS Grid, container queries, `:has()` and tokens | Only if the UI requires measured dimensions in application logic |
| Incremental server-rendered updates | Optional HTMX/Datastar in the host application | If normal navigation cannot meet the interaction requirements |
| Small client-side state | A host-owned JavaScript module | If HTML/CSS alone cannot represent the state |
| Reusable cross-framework behavior | A separately installed, accessible custom element or Lit adapter | Only when encapsulation and reuse outweigh lifecycle costs |
| Searchable combobox, rich editor, virtualized grid | Independently tested accessible widget package | Usually; don't recreate complex keyboard/focus semantics in CSS |

Syntyr owns **presentation**, not input validation, business logic, focus management,
server navigation, asynchronous state, or keyboard controllers. Applications own
these responsibilities. A native custom element is not inherently simpler than
native HTML; do not wrap existing controls solely to create another abstraction.
Keep all optional adapters independently removable without changing the core
stylesheet or its public selectors.

## Built-in system-aware theme

Load core and set `data-syn-theme="auto"`. No separate automatic theme
stylesheet is needed:

```html
<link rel="stylesheet" href="/css/syntyr.core.css">
<main class="syn-root" data-syn-theme="auto">...</main>
```

`auto` uses the Grid palette for dark system preferences and Studio for light.
It works on both root and nested themed regions, requires zero JavaScript, and
does **not** override a user's explicitly selected `grid`, `noir`, or
`studio` theme. Host apps can change the attribute if they provide a theme picker.
Automatic themes use the native `light-dark()` CSS feature with a compatible
fallback; existing tests verify that the palette stays aligned with Grid and Studio.

## Opt-in print styling

Load `syntyr.print.css` after core when printing reports or invoices:

```html
<link rel="stylesheet" href="/css/syntyr.core.css">
<link rel="stylesheet" href="/css/syntyr.print.css">
```

It uses a readable light palette on paper, drops decorative backgrounds and
shadows, and expands overflow regions. Use `.syn-print-hide` only on genuinely
nonessential controls. The app must still ensure that its server-rendered data
is complete, because CSS cannot materialize unloaded or virtualized rows.

## Responsive, legible, and fast

- `.syn-layout` now uses intrinsic auto-fit tracks. It adapts to the width of
  its **actual host**, not only the viewport; narrow embedded panels stack.
- The current design uses scalable typography tokens; small labels use
  `--syn-type-sm` and optional metadata styles can be tuned by consumers.
  Preserve user font scaling and test 200% and 400% genuine browser zoom.
- Core never requires a polyfill. Load optional stylesheets only when their
  capabilities are needed, or use `syntyr.all.css` for demos.
- Reduced motion, forced colors and assistive-technology behavior still need
  manual, representative real-device verification. Automated checks alone
  cannot establish WCAG compliance.

## Cross-engine regression verification

The development-only `tests/progressive_browser.py` checks computed theme
colors, nested opt-in themes, semantic-mode isolation, narrow embedded layout,
print-safe readable data, and disabled print motion in real browser engines:

```sh
python3 tests/progressive_browser.py --browsers chromium firefox webkit
```

It requires Playwright and installed browser binaries for **development only**.
For a host without WebKit libraries, use an official matching Playwright
container. The test fails visibly if a browser cannot launch; it never counts
unexecuted engines as passing. Run accessibility and reflow suites separately.

**Limitations:** Playwright viewport/root-font stress tests do not establish
real browser UI zoom at 200%/400%. CSS `zoom` and CDP page scale are not
interchangeable with native browser zoom: page scale may be post-layout.
Real OS high-contrast and assistive-technology testing must be done manually.
