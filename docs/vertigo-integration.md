# Optional Cyberline CSS skin for Vertigo admin

**Status: original MIT styling demonstration, not an installed Vertigo
plugin or an end-to-end Vertigo deployment.** No Vertigo database, auth,
billing or tenant state was invoked to render the static example.

The live example is at
https://dporkka.github.io/cyberline-css/examples/vertigo-admin.html

## Why optional, not a hard dependency

Vertigo's Go admin templates in kit/admin/admin.go use an inline stylesheet
and classes such as .row, .cards, .card, .button, .search, .tablewrap and
.notice. Cyberline includes a separate opt-in stylesheet that targets these
existing class names, scoped to the body class cy-vertigo-admin.

No user of Vertigo must install Cyberline. No user of Cyberline must install
Vertigo. This adapter is an optional presentation layer only.

## Integration outline (on your Vertigo application branch)

1. Copy Cyberline's MIT-licensed compiled core CSS and
   integrations/vertigo/admin.css into assets served **locally** by the
   Vertigo application, for example at /assets/cyberline.core.css and
   /assets/cyberline.vertigo.css. Keep license attribution.
2. Mount a public read-only static asset handler for those exact paths
   using Go's net/http or your existing static server. Do not add CDN or
   authentication requirements for public CSS files.
3. The current Vertigo admin pageShell helper builds a common HTML shell
   with an inline default CSS block. Change the *application-specific*
   shell only if you choose to enable Cyberline; link both CSS files
   **after** its existing inline style, and add body classes and a theme:

~~~html
<!-- After Vertigo's existing <style>...</style> in <head> -->
<link rel="stylesheet" href="/assets/cyberline.core.css">
<link rel="stylesheet" href="/assets/cyberline.vertigo.css">
<!-- In the shared body tag -->
<body class="cy-root cy-vertigo-admin" data-cy-theme="studio">
~~~

4. Leave the default Vertigo HTML templates and security middleware intact.
   Test admin index, list, edit/create, errors, confirmations, tenant
   boundaries, keyboard navigation and forms against your real application.
5. For the dark themes, switch the body to data-cy-theme="grid" or
   data-cy-theme="noir". Both palettes are in the same CSS core.

**This repository does not modify Vertigo pageShell automatically.** The
current Vertigo function compiles templates with a hard-coded shell; a
production-quality opt-in shell configuration belongs in Vertigo, with its
own tests, if enough customers request it.

## Boundaries and accessibility

- CSS changes presentation, not route authorization, CSRF validation,
  RLS, tenant routing, billing entitlements or input validation.
- The default Vertigo admin template includes native form controls; some
  search fields and data tables should still be audited for accessible
  labels, headings, error references and table headers in their real state.
- Vertigo's own dangerous-action confirmation currently uses inline
  JavaScript in some admin templates. Cyberline's adapter adds **zero**
  JavaScript but does not remove script used elsewhere in Vertigo.
- In a production app, load from your own server, pin the Cyberline
  stylesheet version, test with a CSP, and verify focus, reduced motion,
  real zoom and high-contrast modes.

The styling adapter is independent of Hugo and Zola. Cyberline's static
site does not need a Vertigo process to use this CSS.
