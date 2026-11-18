window.SYNTYR_PLAYGROUND_CATALOG = [
  {
    "id": "catalog-buttons-title",
    "title": "Buttons",
    "module": "syntyr.core.css",
    "description": "Use native buttons for actions; variants change appearance only.",
    "html": "\u003cdiv class=\"syn-inline\">\n  \u003cbutton type=\"button\" class=\"syn-button syn-button--primary\">Save changes\u003c/button>\n  \u003cbutton type=\"button\" class=\"syn-button syn-button--outline\">Preview\u003c/button>\n  \u003cbutton type=\"button\" class=\"syn-button\" disabled>Disabled\u003c/button>\n\u003c/div>",
    "keywords": "actions controls primary outline",
    "guidance": "Use button for actions and a for navigation. ARIA states describe real application state."
  },
  {
    "id": "catalog-forms-title",
    "title": "Labeled fields",
    "module": "syntyr.core.css",
    "description": "Use real labels and native validation; form submission belongs to your app.",
    "html": "\u003cdiv class=\"syn-form\">\n  \u003clabel class=\"syn-label\" for=\"catalog-email\">Email address\u003c/label>\n  \u003cinput class=\"syn-input\" id=\"catalog-email\" type=\"email\" placeholder=\"you@example.com\" required>\n  \u003cp class=\"syn-help\">Use your work email.\u003c/p>\n\u003c/div>",
    "keywords": "input text validation form accessibility",
    "guidance": "Real handlers and field validation belong to the application."
  },
  {
    "id": "catalog-native-controls-title",
    "title": "Native range, file and color",
    "module": "syntyr.core.css",
    "description": "One existing input class; native keyboard, picker and file selection behavior.",
    "html": "\u003cdiv class=\"syn-form\" id=\"catalog-native-controls\">\n  \u003clabel class=\"syn-label\" for=\"catalog-range\">Threshold\u003c/label>\n  \u003cinput id=\"catalog-range\" type=\"range\" class=\"syn-input\" min=\"0\" max=\"100\" value=\"60\">\n  \u003clabel class=\"syn-label\" for=\"catalog-file\">Attach artwork\u003c/label>\n  \u003cinput id=\"catalog-file\" type=\"file\" class=\"syn-input\">\n  \u003clabel class=\"syn-label\" for=\"catalog-color\">Accent color\u003c/label>\n  \u003cinput id=\"catalog-color\" type=\"color\" class=\"syn-input\" value=\"#3355aa\">\n\u003c/div>",
    "keywords": "native range file color slider upload chooser form",
    "guidance": "Real handlers and field validation belong to the application."
  },
  {
    "id": "catalog-interaction-card-0",
    "title": "Exclusive accordion",
    "module": "syntyr.core.css",
    "description": "Related disclosures use native details name; no script or custom roles.",
    "html": "\u003csection aria-labelledby=\"catalog-faq-heading\">\n  \u003ch3 id=\"catalog-faq-heading\">Common questions\u003c/h3>\n  \u003cdetails class=\"syn-details\" name=\"catalog-interaction-faq\" open>\n    \u003csummary>Can I use standard HTML?\u003c/summary>\n    \u003cp>Yes, Syntyr styles browser-native elements.\u003c/p>\n  \u003c/details>\n  \u003cdetails class=\"syn-details\" name=\"catalog-interaction-faq\">\n    \u003csummary>Do I need a JavaScript runtime?\u003c/summary>\n    \u003cp>No. Native disclosures handle their own open state.\u003c/p>\n  \u003c/details>\n\u003c/section>",
    "keywords": "native accordion FAQ details summary exclusive disclosure",
    "guidance": "See the component API reference for compatible classes and CSS modules."
  },
  {
    "id": "catalog-interaction-card-1",
    "title": "GET search form",
    "module": "syntyr.core.css",
    "description": "Real search landmark and GET submission; the static destination does not filter results.",
    "html": "\u003csearch aria-label=\"Search example inventory\">\n  \u003cform class=\"syn-form\" action=\"../examples/native-interactions.html\" method=\"get\">\n    \u003clabel class=\"syn-label\" for=\"catalog-inventory-query\">Inventory search\u003c/label>\n    \u003cinput class=\"syn-input\" id=\"catalog-inventory-query\" type=\"search\"\n           name=\"q\" required placeholder=\"Enter a keyword\">\n    \u003cbutton class=\"syn-button syn-button--primary\" type=\"submit\">Search\u003c/button>\n  \u003c/form>\n\u003c/search>",
    "keywords": "native search get landmark searchform filtering server",
    "guidance": "Real handlers and field validation belong to the application."
  },
  {
    "id": "catalog-interaction-card-2",
    "title": "Confirmation dialog",
    "module": "syntyr.core.css",
    "description": "Native modal command and dialog-only choices; confirming this preview does not persist changes.",
    "html": "\u003cdiv class=\"syn-inline\">\n  \u003cbutton type=\"button\" class=\"syn-button\" commandfor=\"catalog-interaction-dialog\"\n          command=\"show-modal\">Open confirmation\u003c/button>\n  \u003cdialog class=\"syn-dialog\" id=\"catalog-interaction-dialog\"\n          aria-labelledby=\"catalog-interaction-dialog-title\">\n    \u003ch3 id=\"catalog-interaction-dialog-title\">Confirm preview?\u003c/h3>\n    \u003cp>This static example changes no data.\u003c/p>\n    \u003cform method=\"dialog\" class=\"syn-inline\">\n      \u003cbutton class=\"syn-button syn-button--outline\" type=\"submit\"\n              value=\"cancel\" autofocus>Cancel\u003c/button>\n      \u003cbutton class=\"syn-button syn-button--primary\" type=\"submit\"\n              value=\"confirm\">Confirm preview\u003c/button>\n    \u003c/form>\n  \u003c/dialog>\n\u003c/div>",
    "keywords": "native dialog modal confirmation commandfor method dialog",
    "guidance": "Use button for actions and a for navigation. ARIA states describe real application state."
  },
  {
    "id": "catalog-interaction-card-3",
    "title": "Datalist suggestions",
    "module": "syntyr.core.css",
    "description": "Browser suggestions for a free-text input; not a searchable select or combobox implementation.",
    "html": "\u003cdiv class=\"syn-form\">\n  \u003clabel class=\"syn-label\" for=\"catalog-suggested-city\">City\u003c/label>\n  \u003cinput class=\"syn-input\" id=\"catalog-suggested-city\" name=\"city\"\n         list=\"catalog-city-options\" placeholder=\"Start typing a city\">\n  \u003cdatalist id=\"catalog-city-options\">\n    \u003coption value=\"Bras\u00edlia\">\u003c/option>\n    \u003coption value=\"Chicago\">\u003c/option>\n    \u003coption value=\"New York\">\u003c/option>\n  \u003c/datalist>\n\u003c/div>",
    "keywords": "native datalist suggestions autocomplete input optgroup",
    "guidance": "Real handlers and field validation belong to the application."
  },
  {
    "id": "catalog-interaction-card-4",
    "title": "Meter and output",
    "module": "syntyr.core.css",
    "description": "Native bounded measurements and static server result; calculations belong to the host.",
    "html": "\u003cdiv class=\"syn-semantic syn-stack\">\n  \u003clabel for=\"catalog-capacity-meter\">Utilization\u003c/label>\n  \u003cmeter id=\"catalog-capacity-meter\" min=\"0\" max=\"100\" low=\"20\"\n         high=\"85\" optimum=\"40\" value=\"68\">68%\u003c/meter>\n  \u003clabel for=\"catalog-inventory-output\">Matching inventory\u003c/label>\n  \u003coutput id=\"catalog-inventory-output\" name=\"results\">42 available locations\u003c/output>\n\u003c/div>",
    "keywords": "native meter output capacity calculation progress gauge",
    "guidance": "See the component API reference for compatible classes and CSS modules."
  },
  {
    "id": "catalog-panels-title",
    "title": "Panels and token overrides",
    "module": "syntyr.core.css",
    "description": "Override component tokens locally without rebuilding the stylesheet.",
    "html": "\u003carticle class=\"syn-panel\" style=\"--syn-surface: var(--syn-surface-hi)\">\n  \u003ch3 class=\"syn-heading\">Workspace settings\u003c/h3>\n  \u003cp>Use scoped CSS properties to customize an individual panel.\u003c/p>\n\u003c/article>",
    "keywords": "surface card border padding radius CSS variables",
    "guidance": "Choose native headings and accessible labels."
  },
  {
    "id": "catalog-metrics-title",
    "title": "Responsive metrics",
    "module": "syntyr.core.css",
    "description": "A named container lets metrics respond to their parent, not the viewport.",
    "html": "\u003csection class=\"syn-region\" aria-label=\"Service metrics\">\n  \u003cdiv class=\"syn-stats\">\n    \u003carticle class=\"syn-stat\">\u003cspan class=\"syn-stat-label\">UPTIME\u003c/span>\u003cstrong class=\"syn-stat-value\">99.9%\u003c/strong>\u003c/article>\n    \u003carticle class=\"syn-stat\">\u003cspan class=\"syn-stat-label\">USERS\u003c/span>\u003cstrong class=\"syn-stat-value\">2,840\u003c/strong>\u003c/article>\n  \u003c/div>\n\u003c/section>",
    "keywords": "stats grid telemetry container query region",
    "guidance": "Named container must be an ancestor of responsive children."
  },
  {
    "id": "catalog-tables-title",
    "title": "Accessible data tables",
    "module": "syntyr.core.css",
    "description": "Keep semantic table markup and provide scrolling on narrow screens.",
    "html": "\u003cdiv class=\"syn-table-wrap\">\n  \u003ctable class=\"syn-table\">\n    \u003ccaption>Recent deployments\u003c/caption>\n    \u003cthead>\u003ctr>\u003cth scope=\"col\">Build\u003c/th>\u003cth scope=\"col\">Status\u003c/th>\u003c/tr>\u003c/thead>\n    \u003ctbody>\u003ctr>\u003ctd>v1.2\u003c/td>\u003ctd>Passed\u003c/td>\u003c/tr>\u003ctr>\u003ctd>v1.1\u003c/td>\u003ctd>Passed\u003c/td>\u003c/tr>\u003c/tbody>\n  \u003c/table>\n\u003c/div>",
    "keywords": "table tabular records scroll responsive data",
    "guidance": "Use proper headers, captions and scroll containers."
  },
  {
    "id": "catalog-alerts-title",
    "title": "Alerts",
    "module": "syntyr.core.css",
    "description": "Use visible text and semantic status only for real application updates.",
    "html": "\u003cdiv class=\"syn-alert\">Your changes have been saved.\u003c/div>\n\u003cdiv class=\"syn-alert syn-alert--danger\">Could not connect. Try again.\u003c/div>",
    "keywords": "error warning info status important notification",
    "guidance": "See the component API reference for compatible classes and CSS modules."
  },
  {
    "id": "catalog-disclosures-title",
    "title": "Native disclosure",
    "module": "syntyr.core.css",
    "description": "Browser-native disclosure works without custom JavaScript.",
    "html": "\u003cdetails class=\"syn-details\">\n  \u003csummary>What does Syntyr require?\u003c/summary>\n  \u003cp>Just CSS and semantic HTML. JavaScript is optional.\u003c/p>\n\u003c/details>",
    "keywords": "details accordion faq expandable summary",
    "guidance": "See the component API reference for compatible classes and CSS modules."
  },
  {
    "id": "catalog-breadcrumbs-title",
    "title": "Breadcrumb navigation",
    "module": "syntyr.core.css",
    "description": "Use a real navigation landmark and mark the current page.",
    "html": "\u003cnav class=\"syn-breadcrumbs\" aria-label=\"Breadcrumb\">\n  \u003col>\n    \u003cli>\u003ca href=\"/\">Home\u003c/a>\u003c/li>\n    \u003cli>\u003cspan aria-current=\"page\">Settings\u003c/span>\u003c/li>\n  \u003c/ol>\n\u003c/nav>",
    "keywords": "nav pages route links aria current",
    "guidance": "Real links and aria-current only for the actual current page."
  },
  {
    "id": "catalog-progress-title",
    "title": "Progress indicator",
    "module": "syntyr.core.css",
    "description": "Native progress exposes a meaningful value to assistive technology.",
    "html": "\u003clabel class=\"syn-label\" for=\"catalog-progress\">Uploading files\u003c/label>\n\u003cprogress id=\"catalog-progress\" class=\"syn-meter\" value=\"65\" max=\"100\">65%\u003c/progress>",
    "keywords": "meter native progress loading",
    "guidance": "Real handlers and field validation belong to the application."
  },
  {
    "id": "catalog-pricing-title",
    "title": "Pricing cards",
    "module": "syntyr.core.css",
    "description": "Container-responsive pricing, with no client-side layout logic.",
    "html": "\u003csection class=\"syn-region\" aria-label=\"Example plans\">\n  \u003cdiv class=\"syn-pricing\">\n    \u003carticle class=\"syn-price-card\">\u003ch3>Starter\u003c/h3>\u003cp class=\"syn-price-value\">$19\u003c/p>\u003ca href=\"#catalog-top\" class=\"syn-button\">Explore\u003c/a>\u003c/article>\n    \u003carticle class=\"syn-price-card\" data-syn-featured>\u003ch3>Pro\u003c/h3>\u003cp class=\"syn-price-value\">$49\u003c/p>\u003ca href=\"#catalog-top\" class=\"syn-button syn-button--primary\">Explore\u003c/a>\u003c/article>\n  \u003c/div>\n\u003c/section>",
    "keywords": "plan subscriptions marketing grid featured",
    "guidance": "Use button for actions and a for navigation. ARIA states describe real application state."
  },
  {
    "id": "catalog-typography-and-inline-text-title",
    "title": "Typography and inline text",
    "module": "syntyr.core.css",
    "description": "Use heading hierarchy for meaning, not visual size; mark highlights relevance.",
    "html": "\u003csection aria-label=\"Typography sample\">\n  \u003ch2 class=\"syn-heading\">Design with native text\u003c/h2>\n  \u003cp>Combine \u003cstrong>importance\u003c/strong>, \u003cem>emphasis\u003c/em>, and \u003cmark>relevance\u003c/mark>.\u003c/p>\n  \u003cp>\u003csmall>Small print belongs in meaningful supporting text.\u003c/small>\u003c/p>\n\u003c/section>",
    "keywords": "headings heading paragraph emphasis strong mark small",
    "guidance": "See the component API reference for compatible classes and CSS modules."
  },
  {
    "id": "catalog-code-and-keyboard-input-title",
    "title": "Code and keyboard input",
    "module": "syntyr.core.css",
    "description": "Use code for tokens, pre for blocks, and kbd for user input.",
    "html": "\u003csection aria-label=\"Code sample\">\n  \u003cp>Press \u003ckbd>Ctrl\u003c/kbd> + \u003ckbd>K\u003c/kbd> to search.\u003c/p>\n  \u003cpre>\u003ccode>&lt;button type=\"button\"&gt;Save&lt;/button&gt;\u003c/code>\u003c/pre>\n\u003c/section>",
    "keywords": "code pre kbd developer shortcut snippet monospace",
    "guidance": "See the component API reference for compatible classes and CSS modules."
  },
  {
    "id": "catalog-ordered-and-unordered-lists-title",
    "title": "Ordered and unordered lists",
    "module": "syntyr.core.css",
    "description": "Use ordered steps for sequences and unordered lists for collections.",
    "html": "\u003cdiv class=\"syn-grid\">\n  \u003cul>\u003cli>Accessible markup\u003c/li>\u003cli>Scoped styling\u003c/li>\u003c/ul>\n  \u003col>\u003cli>Add the stylesheet\u003c/li>\u003cli>Choose a theme\u003c/li>\u003c/ol>\n\u003c/div>",
    "keywords": "bullets list ol ul li content steps",
    "guidance": "See the component API reference for compatible classes and CSS modules."
  },
  {
    "id": "catalog-definition-list-title",
    "title": "Definition list",
    "module": "syntyr.core.css",
    "description": "A definition list preserves the association between terms and values.",
    "html": "\u003cdl>\n  \u003cdt>Deployment\u003c/dt>\u003cdd>Production\u003c/dd>\n  \u003cdt>Region\u003c/dt>\u003cdd>Americas\u003c/dd>\n\u003c/dl>",
    "keywords": "description terms dl dt dd metadata key value",
    "guidance": "See the component API reference for compatible classes and CSS modules."
  },
  {
    "id": "catalog-article-with-header-and-footer-title",
    "title": "Article with header and footer",
    "module": "syntyr.core.css",
    "description": "Use a self-contained article for independently meaningful content.",
    "html": "\u003carticle class=\"syn-panel\">\n  \u003cheader>\u003ch3>Release notes\u003c/h3>\u003c/header>\n  \u003cp>Native-first components reduce upkeep.\u003c/p>\n  \u003cfooter>\u003csmall>Updated November 2026\u003c/small>\u003c/footer>\n\u003c/article>",
    "keywords": "section article header footer landmark semantic blog",
    "guidance": "Choose native headings and accessible labels."
  },
  {
    "id": "catalog-fieldset-and-choice-inputs-title",
    "title": "Fieldset and choice inputs",
    "module": "syntyr.core.css",
    "description": "A fieldset and legend give related inputs an accessible group name.",
    "html": "\u003cform action=\"#catalog-top\" method=\"get\">\n  \u003cfieldset>\n    \u003clegend>Notification frequency\u003c/legend>\n    \u003clabel>\u003cinput type=\"radio\" name=\"catalog-frequency\" value=\"daily\" checked> Daily\u003c/label>\n    \u003clabel>\u003cinput type=\"radio\" name=\"catalog-frequency\" value=\"weekly\"> Weekly\u003c/label>\n  \u003c/fieldset>\n  \u003clabel>\u003cinput type=\"checkbox\" name=\"catalog-updates\" checked> Product updates\u003c/label>\n  \u003cbutton type=\"submit\" class=\"syn-button\">Apply\u003c/button>\n\u003c/form>",
    "keywords": "fieldset legend radio checkbox label choice form",
    "guidance": "Use button for actions and a for navigation. ARIA states describe real application state."
  },
  {
    "id": "catalog-select-and-textarea-title",
    "title": "Select and textarea",
    "module": "syntyr.core.css",
    "description": "Use native select and textarea before introducing custom widgets.",
    "html": "\u003cdiv class=\"syn-form\">\n  \u003clabel class=\"syn-label\" for=\"catalog-role\">Role\u003c/label>\n  \u003cselect class=\"syn-input\" id=\"catalog-role\">\n    \u003coption>Designer\u003c/option>\u003coption>Developer\u003c/option>\n  \u003c/select>\n  \u003clabel class=\"syn-label\" for=\"catalog-note\">Notes\u003c/label>\n  \u003ctextarea class=\"syn-input\" id=\"catalog-note\" rows=\"2\" placeholder=\"Optional details\">\u003c/textarea>\n\u003c/div>",
    "keywords": "select option textarea label notes form dropdown",
    "guidance": "Real handlers and field validation belong to the application."
  },
  {
    "id": "catalog-dates-and-structured-values-title",
    "title": "Dates and structured values",
    "module": "syntyr.core.css",
    "description": "Encode dates and values for machines while keeping text readable.",
    "html": "\u003cdl>\n  \u003cdt>Launch\u003c/dt>\u003cdd>\u003ctime datetime=\"2026-11-16\">November 16, 2026\u003c/time>\u003c/dd>\n  \u003cdt>Seats\u003c/dt>\u003cdd>\u003cdata value=\"12\">12 active seats\u003c/data>\u003c/dd>\n\u003c/dl>",
    "keywords": "time datetime data value machine readable metadata",
    "guidance": "See the component API reference for compatible classes and CSS modules."
  },
  {
    "id": "catalog-responsive-image-with-caption-title",
    "title": "Responsive image with caption",
    "module": "syntyr.core.css",
    "description": "A picture provides art-direction sources; the img provides the fallback and alt text.",
    "html": "\u003cfigure>\n  \u003cpicture>\n    \u003csource media=\"(min-width: 50rem)\" srcset=\"../assets/og-syntyr.png\">\n    \u003cimg src=\"../assets/syntyr-mark.svg\" alt=\"Syntyr design system mark\" width=\"240\" height=\"120\" loading=\"lazy\">\n  \u003c/picture>\n  \u003cfigcaption>Replace these local demo assets with your own images.\u003c/figcaption>\n\u003c/figure>",
    "keywords": "figure figcaption img picture source responsive image art direction",
    "guidance": "See the component API reference for compatible classes and CSS modules."
  },
  {
    "id": "catalog-quotation-and-source-title",
    "title": "Quotation and source",
    "module": "syntyr.core.css",
    "description": "Use blockquote for quoted passages and cite for the title of a work.",
    "html": "\u003cfigure>\n  \u003cblockquote>\u003cp>Prefer the native browser platform.\u003c/p>\u003c/blockquote>\n  \u003cfigcaption>From \u003ccite>Interface Design Notes\u003c/cite>\u003c/figcaption>\n\u003c/figure>",
    "keywords": "blockquote cite q quote citation figure attribution",
    "guidance": "See the component API reference for compatible classes and CSS modules."
  },
  {
    "id": "catalog-native-popover-title",
    "title": "Native popover",
    "module": "syntyr.core.css",
    "description": "Native popovers preserve browser-managed opening, dismissal, and focus behavior.",
    "html": "\u003cbutton type=\"button\" class=\"syn-button\" popovertarget=\"catalog-help-popover\">More information\u003c/button>\n\u003cdiv id=\"catalog-help-popover\" popover class=\"syn-popover\">\n  \u003cp>Browser-native popover; no JavaScript component required.\u003c/p>\n  \u003cbutton type=\"button\" class=\"syn-button\" popovertarget=\"catalog-help-popover\" popovertargetaction=\"hide\">Close\u003c/button>\n\u003c/div>",
    "keywords": "popover popovertarget overlay help no javascript browser",
    "guidance": "Use button for actions and a for navigation. ARIA states describe real application state."
  },
  {
    "id": "catalog-input-group-title",
    "title": "Connected input groups",
    "module": "syntyr.core.css",
    "description": "Native text input with a connected visual prefix and an accessible field label.",
    "html": "\u003cdiv class=\"syn-field\">\n  \u003clabel class=\"syn-label\" for=\"catalog-website\">Website URL\u003c/label>\n  \u003cdiv class=\"syn-input-group\">\n    \u003cspan class=\"syn-input-addon\" aria-hidden=\"true\">https://\u003c/span>\n    \u003cinput class=\"syn-input\" id=\"catalog-website\" name=\"website\" type=\"text\" inputmode=\"url\" placeholder=\"example.com\">\n  \u003c/div>\n  \u003cp class=\"syn-help\">Enter the host name; validate the full URL in your app.\u003c/p>\n\u003c/div>",
    "keywords": "form composition prefix addon connected input",
    "guidance": "Unreleased alpha.5 candidate only. Native form behavior, associated labels, server validation; use syn-region for container-responsive rows. The Radix adapter is separately optional."
  },
  {
    "id": "catalog-crm-filters-title",
    "title": "CRM filter toolbar",
    "module": "syntyr.recipes.css",
    "description": "Optional responsive filter layout. The linked static demo does not implement server-side filtering.",
    "html": "\u003cform class=\"syn-filter-bar\" action=\"../examples/crm.html#pipeline\" method=\"get\">\n  \u003clabel class=\"syn-label syn-filter-field syn-filter-field--query\" for=\"catalog-account-query\">Account\n    \u003cinput class=\"syn-input\" id=\"catalog-account-query\" name=\"query\" type=\"search\" placeholder=\"Search accounts\">\n  \u003c/label>\n  \u003clabel class=\"syn-label syn-filter-field\" for=\"catalog-stage\">Stage\n    \u003cselect class=\"syn-select\" id=\"catalog-stage\" name=\"status\">\n      \u003coption value=\"\">All stages\u003c/option>\n      \u003coption value=\"qualified\">Qualified\u003c/option>\n    \u003c/select>\n  \u003c/label>\n  \u003cdiv class=\"syn-filter-actions\">\u003cbutton class=\"syn-button syn-button--primary\" type=\"submit\">Apply\u003c/button>\u003c/div>\n\u003c/form>",
    "keywords": "search crm filter bar stage records toolbar",
    "guidance": "Unreleased alpha.5, CSS-only optional layouts. Use a GET form, labelled stages, focusable board overflow and definition-list details; application implements filtering and pipeline state."
  },
  {
    "id": "catalog-recovery-state-title",
    "title": "Empty and recovery state",
    "module": "syntyr.recipes.css",
    "description": "Optional app-state composition. Provide a working destination for any recovery action.",
    "html": "\u003csection class=\"syn-result-state\" aria-labelledby=\"catalog-recovery-title\">\n  \u003ch3 id=\"catalog-recovery-title\">No matching records\u003c/h3>\n  \u003cp>Try a broader search or review the documentation.\u003c/p>\n  \u003ca class=\"syn-button syn-button--outline\" href=\"guides.html\">Browse guides\u003c/a>\n\u003c/section>",
    "keywords": "empty no results recovery error reset action",
    "guidance": "See the component API reference for compatible classes and CSS modules."
  },
  {
    "id": "catalog-geometry-frame-title",
    "title": "Geometry frame",
    "module": "syntyr.geometry.css",
    "description": "An optional decorative bracket frame; content stays semantic HTML.",
    "html": "\u003carticle class=\"syn-panel syn-frame syn-frame--bracket\" aria-labelledby=\"catalog-frame-title\">\n  \u003ch3 class=\"syn-heading\" id=\"catalog-frame-title\">Connection established\u003c/h3>\n  \u003cp>Geometry changes presentation, not meaning.\u003c/p>\n\u003c/article>",
    "keywords": "decorative frame bracket accent geometry visual",
    "guidance": "Load optional geometry CSS. One shape per frame; accent emphasis is additive. Refer to visual-intensity.md for pseudo-element ownership and backgrounds."
  },
  {
    "id": "catalog-viz-bars-title",
    "title": "Accessible data bars",
    "module": "syntyr.viz.css",
    "description": "Optional CSS-only bars with visible values; your app supplies real measurements.",
    "html": "\u003col class=\"syn-viz-bars\" aria-label=\"Illustrative channel share\">\n  \u003cli class=\"syn-viz-bar\">\n    \u003cdiv class=\"syn-viz-bar-label\">\u003cspan>Direct\u003c/span>\u003cdata value=\"54\">54%\u003c/data>\u003c/div>\n    \u003cdiv class=\"syn-viz-bar-track\" aria-hidden=\"true\">\u003cspan class=\"syn-viz-bar-fill\" style=\"--syn-viz-value: 54\">\u003c/span>\u003c/div>\n  \u003c/li>\n  \u003cli class=\"syn-viz-bar\">\n    \u003cdiv class=\"syn-viz-bar-label\">\u003cspan>Agency\u003c/span>\u003cdata value=\"31\">31%\u003c/data>\u003c/div>\n    \u003cdiv class=\"syn-viz-bar-track\" aria-hidden=\"true\">\u003cspan class=\"syn-viz-bar-fill\" style=\"--syn-viz-value: 31\">\u003c/span>\u003c/div>\n  \u003c/li>\n\u003c/ol>",
    "keywords": "visualization graph chart ranked bars percentages data",
    "guidance": "See the component API reference for compatible classes and CSS modules."
  },
  {
    "id": "block-hero-product",
    "title": "Product launch hero",
    "module": "syntyr.core.css + syntyr.recipes.css",
    "description": "A concise product introduction with real calls to action.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-hero-product\">\n  \u003cdiv class=\"syn-site-hero\">\n    \u003cp class=\"syn-eyebrow\">ANALYTICS / WITHOUT FRICTION\u003c/p>\n    \u003ch2 id=\"syn-hero-product\" class=\"syn-site-heading\">Understand your product. \u003cstrong>Act with confidence.\u003c/strong>\u003c/h2>\n    \u003cp class=\"syn-lede\">One clear workspace for teams tracking what matters.\u003c/p>\n    \u003cdiv class=\"syn-actions\">\n      \u003ca class=\"syn-button syn-button--primary\" href=\"/start\">Start free\u003c/a>\n      \u003ca class=\"syn-button syn-button--outline\" href=\"/demo\">Explore demo\u003c/a>\n    \u003c/div>\n  \u003c/div>\n\u003c/section>",
    "keywords": "Product launch hero A concise product introduction with real calls to action. hero landing product",
    "kind": "block",
    "category": "Marketing",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-hero-security",
    "title": "Security-first hero",
    "module": "syntyr.core.css + syntyr.recipes.css",
    "description": "A restrained security product hero with an explicit trust message.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-hero-security\">\n  \u003cdiv class=\"syn-site-hero\">\n    \u003cspan class=\"syn-badge\">SECURITY BY DESIGN\u003c/span>\n    \u003ch2 id=\"syn-hero-security\" class=\"syn-site-heading\">Ship fast. \u003cstrong>Stay in control.\u003c/strong>\u003c/h2>\n    \u003cp class=\"syn-lede\">Deploy reliable software without trading away visibility or ownership.\u003c/p>\n    \u003cdiv class=\"syn-actions\">\u003ca class=\"syn-button syn-button--primary\" href=\"/docs\">Read the docs\u003c/a>\u003c/div>\n    \u003cp class=\"syn-caption\">Self-hosting and access controls are supplied by your application, not by CSS.\u003c/p>\n  \u003c/div>\n\u003c/section>",
    "keywords": "Security-first hero A restrained security product hero with an explicit trust message. security hero saas",
    "kind": "block",
    "category": "Marketing",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-feature-grid",
    "title": "Three-feature grid",
    "module": "syntyr.core.css + syntyr.recipes.css",
    "description": "Responsive feature cards based on a fluid CSS grid.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-feature-heading\">\n  \u003ch2 id=\"syn-feature-heading\" class=\"syn-heading\">Everything in one place\u003c/h2>\n  \u003cdiv class=\"syn-feature-grid\">\n    \u003carticle class=\"syn-feature-card\">\u003ch3>Bring your data\u003c/h3>\u003cp>Connect the tools your team already uses.\u003c/p>\u003c/article>\n    \u003carticle class=\"syn-feature-card\">\u003ch3>See what changed\u003c/h3>\u003cp>Inspect the activity behind each decision.\u003c/p>\u003c/article>\n    \u003carticle class=\"syn-feature-card\">\u003ch3>Keep moving\u003c/h3>\u003cp>Turn insights into actionable workflows.\u003c/p>\u003c/article>\n  \u003c/div>\n\u003c/section>",
    "keywords": "Three-feature grid Responsive feature cards based on a fluid CSS grid. features cards grid",
    "kind": "block",
    "category": "Marketing",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-feature-checklist",
    "title": "Benefits checklist",
    "module": "syntyr.core.css + syntyr.recipes.css",
    "description": "A short benefits section with native list semantics.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-checklist-heading\">\n  \u003cdiv class=\"syn-panel\">\n    \u003cp class=\"syn-eyebrow\">WHY TEAMS SWITCH\u003c/p>\n    \u003ch2 id=\"syn-checklist-heading\" class=\"syn-heading\">A more deliberate workflow\u003c/h2>\n    \u003cul class=\"syn-feature-list\">\n      \u003cli>Centralize critical information.\u003c/li>\n      \u003cli>Track work from request through delivery.\u003c/li>\n      \u003cli>Export data whenever you need it.\u003c/li>\n    \u003c/ul>\n  \u003c/div>\n\u003c/section>",
    "keywords": "Benefits checklist A short benefits section with native list semantics. benefits features list",
    "kind": "block",
    "category": "Marketing",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-pricing-trio",
    "title": "Three-tier pricing",
    "module": "syntyr.core.css",
    "description": "Three responsive pricing cards with a featured plan.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-pricing-heading\">\n  \u003ch2 id=\"syn-pricing-heading\" class=\"syn-heading\">Plans that scale\u003c/h2>\n  \u003cdiv class=\"syn-pricing\">\n    \u003carticle class=\"syn-price-card\">\u003ch3>Solo\u003c/h3>\u003cp class=\"syn-price-value\">$19 \u003csmall>/ mo\u003c/small>\u003c/p>\u003cul class=\"syn-feature-list\">\u003cli>One workspace\u003c/li>\u003cli>Essential reports\u003c/li>\u003c/ul>\u003ca class=\"syn-button\" href=\"/checkout/solo\">Choose Solo\u003c/a>\u003c/article>\n    \u003carticle class=\"syn-price-card\" data-syn-featured>\u003ch3>Team\u003c/h3>\u003cp class=\"syn-price-value\">$49 \u003csmall>/ mo\u003c/small>\u003c/p>\u003cul class=\"syn-feature-list\">\u003cli>Unlimited workspaces\u003c/li>\u003cli>Team permissions\u003c/li>\u003c/ul>\u003ca class=\"syn-button syn-button--primary\" href=\"/checkout/team\">Choose Team\u003c/a>\u003c/article>\n    \u003carticle class=\"syn-price-card\">\u003ch3>Scale\u003c/h3>\u003cp class=\"syn-price-value\">Custom\u003c/p>\u003cul class=\"syn-feature-list\">\u003cli>Advanced controls\u003c/li>\u003cli>Assisted onboarding\u003c/li>\u003c/ul>\u003ca class=\"syn-button\" href=\"/contact\">Contact sales\u003c/a>\u003c/article>\n  \u003c/div>\n  \u003cp class=\"syn-caption\">Example prices only; replace plan data and checkout routes.\u003c/p>\n\u003c/section>",
    "keywords": "Three-tier pricing Three responsive pricing cards with a featured plan. pricing plans conversion",
    "kind": "block",
    "category": "Marketing",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-testimonial",
    "title": "Customer testimonial",
    "module": "syntyr.core.css",
    "description": "Readable social proof with explicit quotation attribution.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-label=\"Customer testimonial\">\n  \u003cfigure class=\"syn-panel\">\n    \u003cblockquote>\u003cp class=\"syn-lede\">\u201cOur team finally has a shared view of the work that matters.\u201d\u003c/p>\u003c/blockquote>\n    \u003cfigcaption class=\"syn-muted\">Illustrative quote \u2014 replace with permission-based customer feedback.\u003c/figcaption>\n  \u003c/figure>\n\u003c/section>",
    "keywords": "Customer testimonial Readable social proof with explicit quotation attribution. testimonial quote trust",
    "kind": "block",
    "category": "Marketing",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-faq",
    "title": "Frequently asked questions",
    "module": "syntyr.core.css",
    "description": "Keyboard-accessible native disclosures without a script.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-faq-heading\">\n  \u003ch2 id=\"syn-faq-heading\" class=\"syn-heading\">Frequently asked questions\u003c/h2>\n  \u003cdetails class=\"syn-details\">\u003csummary>Can I use my own hosting?\u003c/summary>\u003cp>Yes. This example is plain HTML and CSS.\u003c/p>\u003c/details>\n  \u003cdetails class=\"syn-details\">\u003csummary>Do I need JavaScript?\u003c/summary>\u003cp>Not for this native disclosure interface.\u003c/p>\u003c/details>\n  \u003cdetails class=\"syn-details\">\u003csummary>Can I customize the theme?\u003c/summary>\u003cp>Override the documented CSS custom properties.\u003c/p>\u003c/details>\n\u003c/section>",
    "keywords": "Frequently asked questions Keyboard-accessible native disclosures without a script. faq questions disclosure",
    "kind": "block",
    "category": "Marketing",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-cta-band",
    "title": "Call-to-action band",
    "module": "syntyr.core.css + syntyr.recipes.css",
    "description": "A compact conversion section with clear hierarchy.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-cta-heading\">\n  \u003cdiv class=\"syn-cta-band\">\n    \u003cdiv>\u003ch2 id=\"syn-cta-heading\" class=\"syn-heading\">Ready to explore?\u003c/h2>\u003cp>Start with a workflow that works for your team.\u003c/p>\u003c/div>\n    \u003ca class=\"syn-button syn-button--primary\" href=\"/contact\">Talk to us\u003c/a>\n  \u003c/div>\n\u003c/section>",
    "keywords": "Call-to-action band A compact conversion section with clear hierarchy. cta conversion contact",
    "kind": "block",
    "category": "Marketing",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-metric-overview",
    "title": "KPI overview",
    "module": "syntyr.core.css",
    "description": "Container-aware operational metrics with text labels.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-kpi-heading\">\n  \u003ch2 id=\"syn-kpi-heading\" class=\"syn-heading\">Operations snapshot\u003c/h2>\n  \u003cdiv class=\"syn-stats\">\n    \u003carticle class=\"syn-stat\">\u003cp class=\"syn-stat-label\">Active accounts\u003c/p>\u003cp class=\"syn-stat-value\">1,284\u003c/p>\u003c/article>\n    \u003carticle class=\"syn-stat\">\u003cp class=\"syn-stat-label\">Open requests\u003c/p>\u003cp class=\"syn-stat-value\">38\u003c/p>\u003c/article>\n    \u003carticle class=\"syn-stat\">\u003cp class=\"syn-stat-label\">Completion\u003c/p>\u003cp class=\"syn-stat-value\">94%\u003c/p>\u003c/article>\n  \u003c/div>\n\u003c/section>",
    "keywords": "KPI overview Container-aware operational metrics with text labels. dashboard kpi metrics",
    "kind": "block",
    "category": "Applications",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-activity-feed",
    "title": "Recent activity",
    "module": "syntyr.core.css + syntyr.recipes.css",
    "description": "A compact activity feed in a reusable application card.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-activity-heading\">\n  \u003cdiv class=\"syn-app-card\">\n    \u003cheader class=\"syn-app-card-header\">\u003ch2 id=\"syn-activity-heading\" class=\"syn-heading\">Recent activity\u003c/h2>\u003cspan class=\"syn-badge\">Today\u003c/span>\u003c/header>\n    \u003col class=\"syn-activity-list\">\n      \u003cli>\u003cspan>Report prepared\u003c/span>\u003ctime datetime=\"2026-11-15T10:30:00\">10:30\u003c/time>\u003c/li>\n      \u003cli>\u003cspan>New workspace added\u003c/span>\u003ctime datetime=\"2026-11-15T09:15:00\">09:15\u003c/time>\u003c/li>\n      \u003cli>\u003cspan>Settings reviewed\u003c/span>\u003ctime datetime=\"2026-11-15T08:00:00\">08:00\u003c/time>\u003c/li>\n    \u003c/ol>\n  \u003c/div>\n\u003c/section>",
    "keywords": "Recent activity A compact activity feed in a reusable application card. activity feed application",
    "kind": "block",
    "category": "Applications",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-data-table",
    "title": "Records table",
    "module": "syntyr.core.css",
    "description": "Semantic, scrollable table with caption and column scopes.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-table-heading\">\n  \u003ch2 id=\"syn-table-heading\" class=\"syn-heading\">Active requests\u003c/h2>\n  \u003cdiv class=\"syn-table-wrap\">\n    \u003ctable class=\"syn-table\">\n      \u003ccaption>Illustrative requests and their current state\u003c/caption>\n      \u003cthead>\u003ctr>\u003cth scope=\"col\">Request\u003c/th>\u003cth scope=\"col\">Owner\u003c/th>\u003cth scope=\"col\">Status\u003c/th>\u003c/tr>\u003c/thead>\n      \u003ctbody>\n        \u003ctr>\u003cth scope=\"row\">REQ-103\u003c/th>\u003ctd>Alex\u003c/td>\u003ctd>\u003cspan class=\"syn-status syn-status--success\">Ready\u003c/span>\u003c/td>\u003c/tr>\n        \u003ctr>\u003cth scope=\"row\">REQ-104\u003c/th>\u003ctd>Casey\u003c/td>\u003ctd>\u003cspan class=\"syn-status syn-status--warning\">Review\u003c/span>\u003c/td>\u003c/tr>\n      \u003c/tbody>\n    \u003c/table>\n  \u003c/div>\n\u003c/section>",
    "keywords": "Records table Semantic, scrollable table with caption and column scopes. table records report",
    "kind": "block",
    "category": "Applications",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-filter-toolbar",
    "title": "Search and filter form",
    "module": "syntyr.core.css",
    "description": "Server-ready GET filters that preserve native form semantics.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-filter-heading\">\n  \u003ch2 id=\"syn-filter-heading\" class=\"syn-heading\">Find a request\u003c/h2>\n  \u003cform class=\"syn-panel syn-form\" method=\"get\" action=\"/requests\">\n    \u003clabel class=\"syn-label\" for=\"syn-block-query\">Search by name\u003c/label>\n    \u003cinput class=\"syn-input\" id=\"syn-block-query\" name=\"query\" type=\"search\" placeholder=\"Search requests\">\n    \u003clabel class=\"syn-label\" for=\"syn-block-status\">Status\u003c/label>\n    \u003cselect class=\"syn-select\" id=\"syn-block-status\" name=\"status\">\n      \u003coption value=\"\">All statuses\u003c/option>\u003coption value=\"open\">Open\u003c/option>\u003coption value=\"closed\">Closed\u003c/option>\n    \u003c/select>\n    \u003cbutton class=\"syn-button syn-button--primary\" type=\"submit\">Apply filters\u003c/button>\n  \u003c/form>\n\u003c/section>",
    "keywords": "Search and filter form Server-ready GET filters that preserve native form semantics. search filter form",
    "kind": "block",
    "category": "Applications",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-settings-form",
    "title": "Account settings",
    "module": "syntyr.core.css",
    "description": "Labeled settings form for server-backed applications.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-settings-heading\">\n  \u003ch2 id=\"syn-settings-heading\" class=\"syn-heading\">Workspace settings\u003c/h2>\n  \u003cform class=\"syn-panel syn-form\" method=\"post\" action=\"/settings\">\n    \u003clabel class=\"syn-label\" for=\"syn-block-name\">Workspace name\u003c/label>\n    \u003cinput class=\"syn-input\" id=\"syn-block-name\" name=\"name\" autocomplete=\"organization\" value=\"Northstar Operations\" required>\n    \u003clabel class=\"syn-label\" for=\"syn-block-timezone\">Timezone\u003c/label>\n    \u003cselect class=\"syn-select\" id=\"syn-block-timezone\" name=\"timezone\">\u003coption value=\"UTC\">UTC\u003c/option>\u003coption value=\"America/Sao_Paulo\">Bras\u00edlia\u003c/option>\u003c/select>\n    \u003cp class=\"syn-help\">Connect your actual validation, CSRF protection and persistence.\u003c/p>\n    \u003cbutton class=\"syn-button syn-button--primary\" type=\"submit\">Save settings\u003c/button>\n  \u003c/form>\n\u003c/section>",
    "keywords": "Account settings Labeled settings form for server-backed applications. settings account form",
    "kind": "block",
    "category": "Applications",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-team-directory",
    "title": "Team directory",
    "module": "syntyr.core.css + syntyr.recipes.css",
    "description": "Simple list of people and roles with descriptive content.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-team-heading\">\n  \u003cdiv class=\"syn-app-card\">\n    \u003cheader class=\"syn-app-card-header\">\u003ch2 id=\"syn-team-heading\" class=\"syn-heading\">Team members\u003c/h2>\u003cspan class=\"syn-badge\">3 members\u003c/span>\u003c/header>\n    \u003cul class=\"syn-activity-list\">\n      \u003cli>\u003cstrong>Alex Kim\u003c/strong>\u003cspan class=\"syn-muted\">Owner\u003c/span>\u003c/li>\n      \u003cli>\u003cstrong>Sam Lee\u003c/strong>\u003cspan class=\"syn-muted\">Editor\u003c/span>\u003c/li>\n      \u003cli>\u003cstrong>Casey Rivera\u003c/strong>\u003cspan class=\"syn-muted\">Viewer\u003c/span>\u003c/li>\n    \u003c/ul>\n  \u003c/div>\n\u003c/section>",
    "keywords": "Team directory Simple list of people and roles with descriptive content. team permissions people",
    "kind": "block",
    "category": "Applications",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-billing-summary",
    "title": "Billing summary",
    "module": "syntyr.core.css + syntyr.recipes.css",
    "description": "A compact, readable subscription overview.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-billing-heading\">\n  \u003carticle class=\"syn-app-card\">\n    \u003cheader class=\"syn-app-card-header\">\u003ch2 id=\"syn-billing-heading\" class=\"syn-heading\">Subscription\u003c/h2>\u003cspan class=\"syn-status syn-status--success\">Active\u003c/span>\u003c/header>\n    \u003cp class=\"syn-eyebrow\">TEAM PLAN\u003c/p>\n    \u003cp class=\"syn-metric\">$49 \u003cspan class=\"syn-caption\">/ month\u003c/span>\u003c/p>\n    \u003cp class=\"syn-muted\">Next illustrative invoice: December 1, 2026.\u003c/p>\n    \u003ca href=\"/billing\" class=\"syn-button\">Manage billing\u003c/a>\n  \u003c/article>\n\u003c/section>",
    "keywords": "Billing summary A compact, readable subscription overview. billing subscription invoice",
    "kind": "block",
    "category": "Applications",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-onboarding-steps",
    "title": "Onboarding checklist",
    "module": "syntyr.core.css + syntyr.recipes.css",
    "description": "A short onboarding progression conveyed without color-only state.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-onboarding-heading\">\n  \u003cdiv class=\"syn-panel\">\n    \u003ch2 id=\"syn-onboarding-heading\" class=\"syn-heading\">Complete your setup\u003c/h2>\n    \u003col class=\"syn-activity-list\">\n      \u003cli>\u003cspan>1. Create your workspace\u003c/span>\u003cspan class=\"syn-status syn-status--success\">Done\u003c/span>\u003c/li>\n      \u003cli>\u003cspan>2. Invite teammates\u003c/span>\u003cspan class=\"syn-status syn-status--warning\">Next\u003c/span>\u003c/li>\n      \u003cli>\u003cspan>3. Connect a data source\u003c/span>\u003cspan class=\"syn-muted\">Not started\u003c/span>\u003c/li>\n    \u003c/ol>\n    \u003ca href=\"/onboarding\" class=\"syn-button syn-button--primary\">Continue setup\u003c/a>\n  \u003c/div>\n\u003c/section>",
    "keywords": "Onboarding checklist A short onboarding progression conveyed without color-only state. onboarding checklist setup",
    "kind": "block",
    "category": "Applications",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-terminal-session",
    "title": "Terminal output",
    "module": "syntyr.core.css + syntyr.recipes.css",
    "description": "A static terminal presentation, not an interactive shell.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-terminal-heading\">\n  \u003ch2 id=\"syn-terminal-heading\" class=\"syn-heading\">Deploy preview\u003c/h2>\n  \u003cdiv class=\"syn-terminal\" role=\"group\" aria-label=\"Illustrative deployment output\">\n    \u003cdiv class=\"syn-terminal-bar\">\u003cspan class=\"syn-terminal-title\">deploy.log\u003c/span>\u003cspan>EXIT 0\u003c/span>\u003c/div>\n    \u003cpre class=\"syn-terminal-body\">\u003ccode>\u003cspan class=\"syn-terminal-prompt\">$\u003c/span> \u003cspan class=\"syn-terminal-command\">deploy --preview\u003c/span>\n\u003cspan class=\"syn-terminal-success\">\u2713 Build completed\u003c/span>\n\u003cspan class=\"syn-terminal-success\">\u2713 Static assets verified\u003c/span>\n\u003cspan class=\"syn-terminal-muted\">Preview is ready\u003c/span>\u003c/code>\u003c/pre>\n  \u003c/div>\n\u003c/section>",
    "keywords": "Terminal output A static terminal presentation, not an interactive shell. terminal developer cli",
    "kind": "block",
    "category": "Technical",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-incident-notice",
    "title": "Service incident notice",
    "module": "syntyr.core.css",
    "description": "Status notice with actionable text and honest semantics.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-incident-heading\">\n  \u003cdiv class=\"syn-alert syn-alert--danger\">\n    \u003ch2 id=\"syn-incident-heading\" class=\"syn-heading\">Degraded API performance\u003c/h2>\n    \u003cp>Some requests may be delayed. Engineers are investigating and will post updates.\u003c/p>\n    \u003ca href=\"/status\">View status history\u003c/a>\n  \u003c/div>\n\u003c/section>",
    "keywords": "Service incident notice Status notice with actionable text and honest semantics. incident status alert",
    "kind": "block",
    "category": "Technical",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-telemetry-status",
    "title": "Telemetry panel",
    "module": "syntyr.core.css",
    "description": "Readable service status with native progress indicators.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-telemetry-heading\">\n  \u003cdiv class=\"syn-panel\">\n    \u003cp class=\"syn-eyebrow\">SYSTEM TELEMETRY\u003c/p>\n    \u003ch2 id=\"syn-telemetry-heading\" class=\"syn-heading\">Cluster health\u003c/h2>\n    \u003clabel class=\"syn-label\" for=\"syn-block-uptime\">Requests completed \u2014 96%\u003c/label>\n    \u003cprogress class=\"syn-meter\" id=\"syn-block-uptime\" value=\"96\" max=\"100\">96%\u003c/progress>\n    \u003cp class=\"syn-caption\">Illustrative values; connect to real monitoring data.\u003c/p>\n  \u003c/div>\n\u003c/section>",
    "keywords": "Telemetry panel Readable service status with native progress indicators. telemetry health progress",
    "kind": "block",
    "category": "Technical",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  },
  {
    "id": "block-release-notes",
    "title": "Release notes",
    "module": "syntyr.core.css",
    "description": "Compact changelog entry with a machine-readable date.",
    "html": "\u003csection class=\"syn-root syn-region\" data-syn-theme=\"studio\" aria-labelledby=\"syn-release-heading\">\n  \u003carticle class=\"syn-panel\">\n    \u003cp class=\"syn-eyebrow\">\u003ctime datetime=\"2026-11-15\">NOV 15, 2026\u003c/time> / RELEASE\u003c/p>\n    \u003ch2 id=\"syn-release-heading\" class=\"syn-heading\">Version 1.4\u003c/h2>\n    \u003cp class=\"syn-muted\">A more focused way to review and filter your activity.\u003c/p>\n    \u003cul class=\"syn-feature-list\">\n      \u003cli>Improved record filtering.\u003c/li>\u003cli>Clearer empty and loading states.\u003c/li>\u003cli>Keyboard navigation refinements.\u003c/li>\n    \u003c/ul>\n    \u003ca href=\"/changelog\">View all releases\u003c/a>\n  \u003c/article>\n\u003c/section>",
    "keywords": "Release notes Compact changelog entry with a machine-readable date. changelog releases updates",
    "kind": "block",
    "category": "Technical",
    "guidance": "Illustrative, MIT-licensed presentation. Use the required CSS modules; your application supplies actions, validation, real data and permissions."
  }
];
