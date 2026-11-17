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
  }
];
