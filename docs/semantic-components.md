# Semantic HTML component recipes

Build article previews, breadcrumbs, citations, metadata lists, change histories,
internationalized labels, and summary tables with **native HTML**. Syntyr styles
these elements without replacing browser semantics or adding a JavaScript runtime.
These are copy-owned markup compositions in the free MIT core—not new JS widgets.

[View the live semantic component gallery](../examples/semantic-compositions.html).
For the existing forms, dialogs, search and disclosure patterns, see
[native platform patterns](native-patterns.md).

## Install semantic styling

Load core first, semantic second. Both are plain CSS; styles apply only to a
`.syn-root.syn-semantic` element or a `.syn-semantic` subtree inside
`.syn-root`. Classless elements are styled automatically. Add
`data-syn-semantic` to classed elements **only** when opting them into the
semantic rules. A classed element keeps its explicitly chosen component styles.

~~~html
<link rel="stylesheet" href="/dist/syntyr.core.css">
<link rel="stylesheet" href="/dist/syntyr.semantic.css">
<main class="syn-root syn-semantic" data-syn-theme="studio">
  <article><h1>Semantic HTML, styled by Syntyr</h1></article>
</main>
~~~

Use version-pinned stylesheets from your own deployment in production. These
examples require **no JavaScript**. Any data lookup, routing, persistence or
change handling still belongs to the server or host application.

## Article preview with publication date

Use `article` for a self-contained work and `time[datetime]` for
machine-readable dates. Avoid `article` merely to get a bordered card:
use `.syn-panel` on an ordinary container instead.

~~~html
<article>
  <header>
    <h2><a href="/notes/semantic-html">Semantic HTML in practice</a></h2>
    <p>Published <time datetime="2026-11-16">16 November 2026</time></p>
  </header>
  <p>A compact guide to meaningful browser-native markup.</p>
  <footer><small>Documentation team</small></footer>
</article>
~~~

## Breadcrumb navigation

Use a real `nav` landmark, an ordered list and `aria-current="page"`.
Syntyr already provides `.syn-breadcrumbs`; do not create a second breadcrumb
component or hand-code presentational separator characters.

~~~html
<nav class="syn-breadcrumbs" aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/docs">Docs</a></li>
    <li aria-current="page">Semantics</li>
  </ol>
</nav>
~~~

## Definitions and structured metadata

Use `dl`, `dt`, and `dd` for name/value pairs; `data[value]` for a
machine-readable value, `abbr[title]` for a genuine abbreviation, and
`time[datetime]` for dates. Do not use `dl` merely as a two-column grid.

~~~html
<dl>
  <dt>Plan</dt><dd>Team</dd>
  <dt>Seats</dt><dd><data value="12">12 active seats</data></dd>
  <dt>Renewal</dt><dd><time datetime="2027-01-01">1 January 2027</time></dd>
  <dt>Availability</dt><dd><abbr title="Service-level agreement">SLA</abbr> 99.9%</dd>
</dl>
~~~

## Quotation and source attribution

Use `blockquote` for a long quotation and a `figure` with
`figcaption` for its attribution. `cite` names the *work*, not its author;
do not manufacture a URL for the `blockquote[cite]` attribute.

~~~html
<figure>
  <blockquote><p>Use the language of the platform before adding an abstraction.</p></blockquote>
  <figcaption>From <cite>Semantic Design Notes</cite></figcaption>
</figure>
~~~

A `blockquote` may alternatively include a `footer` for supporting
attribution text. The optional semantic stylesheet styles that footer, without
changing the surrounding `footer` elements elsewhere on the page.

## Document revisions

The `ins` and `del` elements communicate additions and removals. Include a
valid `datetime` if the modification date is known. For live collaborative
editing or audit history, the server remains authoritative.

~~~html
<p>Retention: <del datetime="2026-11-15">90 days</del>
  <ins datetime="2026-11-16">120 days</ins>.</p>
~~~

## Multilingual pronunciation and bidi isolation

Use `ruby` and `rt` for pronunciation annotations; `rp` supplies text
fallback in browsers without ruby presentation. Syntyr deliberately does not restyle the
annotation; the browser owns ruby positioning, text size, and fallback. Use `bdi` for a
user-supplied string with unknown direction; `bdo` intentionally overrides
direction and should be used only when that behavior is required.

~~~html
<p>Character: <ruby>漢<rp>(</rp><rt>hàn</rt><rp>)</rp></ruby></p>
<p>Author: <bdi>مريم</bdi> — saved successfully.</p>
<p>Deliberate reverse sequence: <bdo dir="rtl">ABC</bdo></p>
~~~

## Tabular totals with a real footer

Keep a caption, column headers with `scope="col"`, row headers with
`scope="row"`, and a `tfoot` summary. The browser owns table semantics;
Syntyr's optional `tfoot` styling adds only a separator and weight. For
complex tables, connect headers using `id` and `headers` as needed.

~~~html
<table>
  <caption>Monthly license usage</caption>
  <thead><tr><th scope="col">License</th><th scope="col">Seats</th></tr></thead>
  <tbody>
    <tr><th scope="row">Team</th><td>12</td></tr>
    <tr><th scope="row">Guest</th><td>3</td></tr>
  </tbody>
  <tfoot><tr><th scope="row">Total</th><td>15</td></tr></tfoot>
</table>
~~~

## Complementary content

A contextual `aside` is a complementary landmark, not a generic card. Apply
the existing `.syn-panel` class when a visual callout is desirable.

~~~html
<aside class="syn-panel" aria-labelledby="help-title">
  <h2 id="help-title">Implementation guidance</h2>
  <p>Keep routing, translations, and data validation in the host application.</p>
</aside>
~~~

**Accessibility and maintenance:** Keep real heading order and link destinations,
avoid adding redundant ARIA roles to native elements, test browser reflow and
right-to-left content, and do not add JavaScript just to imitate HTML controls.
`ruby`, `bdi`, `bdo`, `rp` and table navigation are browser-owned behavior.
