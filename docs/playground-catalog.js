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
  }
];
