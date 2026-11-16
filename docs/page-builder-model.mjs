/* Docs-only editor model. No dependency on a framework, editor engine or browser API. */
export const SCHEMA_VERSION = "syntyr.page.v1";
export const THEMES = Object.freeze(["studio", "grid", "noir", "industrial", "terminal", "corporate", "minimal", "auto"]);

const DEFINITIONS = {
  hero: {
    label: "Hero", description: "Lead with a headline and a clear action.",
    fields: {
      eyebrow: "MADE WITH SYNTYR",
      title: "Build your next website visually.",
      description: "A composable page built from semantic HTML and the Syntyr CSS system.",
      actionText: "Explore more", actionHref: "#features"
    }
  },
  features: {
    label: "Feature cards", description: "Introduce three benefits or services.",
    fields: {
      heading: "Everything you need",
      firstTitle: "Portable", firstText: "Export ordinary HTML and CSS.",
      secondTitle: "Adaptable", secondText: "Change your theme without rewriting markup.",
      thirdTitle: "Accessible", thirdText: "Native elements and meaningful structure."
    }
  },
  split: {
    label: "Text & action", description: "A focused explanation with a supporting link.",
    fields: {
      eyebrow: "BETTER BY DESIGN", heading: "Keep your content in control.",
      description: "Use Syntyr blocks to create a consistent page without a heavyweight runtime.",
      actionText: "Get started", actionHref: "#contact"
    }
  },
  quote: {
    label: "Testimonial", description: "A short quotation and its attribution.",
    fields: {
      quote: "Our team can move faster without losing control of the markup.",
      attribution: "A thoughtful customer"
    }
  },
  faq: {
    label: "FAQ", description: "Native disclosure questions using details and summary.",
    fields: {
      heading: "Frequently asked questions",
      firstQuestion: "Can I use this without React?", firstAnswer: "Yes. The exported page is HTML and CSS.",
      secondQuestion: "Can I host this myself?", secondAnswer: "Yes. Download the HTML and the matching Syntyr stylesheet."
    }
  },
  cta: {
    label: "Call to action", description: "Invite the reader to take one next step.",
    fields: {
      heading: "Ready to build?", description: "Your design. Your code. Your hosting.",
      actionText: "Contact us", actionHref: "#contact"
    }
  },
  footer: {
    label: "Footer", description: "Closing brand information and a link.",
    fields: {
      brand: "Your company", description: "Independent by design.",
      linkText: "Back to top", linkHref: "#top"
    }
  },
  header: {
    label: "Site header", description: "Brand name and primary navigation link.",
    fields: {
      brand: "Your company", linkText: "Learn more", linkHref: "#features"
    }
  }
};

export const BLOCK_TYPES = Object.freeze(Object.keys(DEFINITIONS));
export const BLOCK_DEFINITIONS = Object.freeze(DEFINITIONS);
const MAX_BLOCKS = 50;
const MAX_FIELD = 5000;

function plainObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}
function own(object, key) {
  return Object.prototype.hasOwnProperty.call(object, key);
}
function escapeHtml(value) {
  return String(value).replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}
function safeHref(value) {
  const href = value.trim();
  if (/^#[a-zA-Z][a-zA-Z0-9_-]*$/.test(href)) return href;
  if (/^\/(?!\/)[a-zA-Z0-9_./#?&=%+-]*$/.test(href)) return href;
  if (/^https:\/\/[a-zA-Z0-9.-]+(?::[0-9]+)?(?:[/?#][^\s"'<>]*)?$/i.test(href)) return href;
  return "#";
}
function action(label, href, primary = true) {
  const variant = primary ? " syn-button--primary" : "";
  return '<a class="syn-button' + variant + '" href="' + escapeHtml(safeHref(href)) +
    '">' + escapeHtml(label) + "</a>";
}
function field(name, value) {
  return '<span class="syn-eyebrow">' + escapeHtml(value) + "</span>";
}
function heading(level, value) {
  return "<h" + level + ' class="syn-heading">' + escapeHtml(value) + "</h" + level + ">";
}
function paragraph(value) {
  return '<p class="syn-muted">' + escapeHtml(value) + "</p>";
}

export function createBlock(type, id = type + "-1") {
  if (!own(DEFINITIONS, type)) throw new Error("Unknown block: " + type);
  if (!/^[a-zA-Z0-9_-]{1,64}$/.test(id)) throw new Error("Invalid block id");
  return { id, type, props: { ...DEFINITIONS[type].fields } };
}

export function createDefaultDocument() {
  return {
    schema: SCHEMA_VERSION,
    title: "My Syntyr page",
    theme: "studio",
    blocks: [
      createBlock("hero", "hero-1"),
      createBlock("features", "features-1"),
      createBlock("cta", "cta-1")
    ]
  };
}

export function parseDocument(input) {
  let page;
  if (typeof input === "string") {
    if (input.length > 500000) throw new Error("Project JSON is too large");
    try { page = JSON.parse(input); }
    catch { throw new Error("Invalid project JSON"); }
  } else {
    page = input;
  }
  if (!plainObject(page)) throw new Error("Page must be an object");
  if (page.schema !== SCHEMA_VERSION) throw new Error("Unsupported page schema");
  if (typeof page.title !== "string" || page.title.length > 160) throw new Error("Invalid page title");
  if (!THEMES.includes(page.theme)) throw new Error("Unknown page theme");
  if (!Array.isArray(page.blocks) || page.blocks.length > MAX_BLOCKS)
    throw new Error("Page must contain at most 50 blocks");
  const ids = new Set();
  const blocks = page.blocks.map((block) => {
    if (!plainObject(block) || !own(DEFINITIONS, block.type))
      throw new Error("Unknown block: " + String(block?.type));
    if (typeof block.id !== "string" || !/^[a-zA-Z0-9_-]{1,64}$/.test(block.id))
      throw new Error("Invalid block id");
    if (ids.has(block.id)) throw new Error("Duplicate block id: " + block.id);
    ids.add(block.id);
    if (!plainObject(block.props)) throw new Error("Invalid block properties");
    const declared = DEFINITIONS[block.type].fields;
    const props = {};
    for (const name of Object.keys(declared)) {
      if (!own(block.props, name) || typeof block.props[name] !== "string")
        throw new Error("Field " + name + " must be a string");
      if (block.props[name].length > MAX_FIELD) throw new Error("Field " + name + " is too long");
      props[name] = block.props[name];
    }
    if (Object.keys(block.props).some(key => !own(declared, key)))
      throw new Error("Unknown block property");
    return { id: block.id, type: block.type, props };
  });
  return { schema: SCHEMA_VERSION, title: page.title, theme: page.theme, blocks };
}

export function moveBlock(page, from, to) {
  const normalized = parseDocument(page);
  if (!Number.isInteger(from) || !Number.isInteger(to) ||
      from < 0 || to < 0 || from >= normalized.blocks.length || to >= normalized.blocks.length)
    throw new Error("Move indices out of range");
  const [block] = normalized.blocks.splice(from, 1);
  normalized.blocks.splice(to, 0, block);
  return normalized;
}

function renderBlock(block, anchor) {
  const p = block.props;
  const id = ' data-syntyr-block-id="' + escapeHtml(block.id) + '"';
  const sectionAnchor = anchor ? ' id="' + escapeHtml(anchor) + '"' : "";
  switch (block.type) {
    case "header":
      return '<header class="syn-header"' + id + '><strong class="syn-logo">' +
        escapeHtml(p.brand) + '</strong><nav aria-label="Primary navigation">' +
        action(p.linkText, p.linkHref, false) + "</nav></header>";
    case "hero":
      return '<section class="syn-stage"' + sectionAnchor + id + ">" + field("eyebrow", p.eyebrow) +
        '<h1 class="syn-title">' + escapeHtml(p.title) + '</h1><p class="syn-lede">' +
        escapeHtml(p.description) + '</p><div class="syn-inline">' +
        action(p.actionText, p.actionHref) + "</div></section>";
    case "features": {
      const cards = [["firstTitle", "firstText"], ["secondTitle", "secondText"], ["thirdTitle", "thirdText"]];
      return '<section class="syn-region"' + sectionAnchor + id + ">" + heading(2, p.heading) +
        '<div class="syn-grid">' + cards.map(([title, text]) =>
          '<article class="syn-panel">' + heading(3, p[title]) + paragraph(p[text]) + "</article>"
        ).join("") + "</div></section>";
    }
    case "split":
      return '<section class="syn-panel syn-region"' + id + ">" + field("eyebrow", p.eyebrow) +
        heading(2, p.heading) + paragraph(p.description) + action(p.actionText, p.actionHref) + "</section>";
    case "quote":
      return '<figure class="syn-panel"' + id + '><blockquote><p>' +
        escapeHtml(p.quote) + '</p></blockquote><figcaption class="syn-caption">' +
        escapeHtml(p.attribution) + "</figcaption></figure>";
    case "faq":
      return '<section class="syn-region"' + id + ">" + heading(2, p.heading) +
        '<details><summary>' + escapeHtml(p.firstQuestion) + "</summary>" +
        paragraph(p.firstAnswer) + '</details><details><summary>' +
        escapeHtml(p.secondQuestion) + "</summary>" + paragraph(p.secondAnswer) + "</details></section>";
    case "cta":
      return '<section class="syn-panel syn-region"' + sectionAnchor + id + ">" +
        heading(2, p.heading) + paragraph(p.description) +
        action(p.actionText, p.actionHref) + "</section>";
    case "footer":
      return '<footer class="syn-region"' + id + '><strong>' + escapeHtml(p.brand) +
        '</strong>' + paragraph(p.description) + action(p.linkText, p.linkHref, false) + "</footer>";
    default:
      throw new Error("Unknown block");
  }
}

export function renderSections(page) {
  const anchors = new Set();
  return parseDocument(page).blocks.map((block) => {
    const base = { hero: "top", features: "features", cta: "contact" }[block.type];
    const anchor = base ? (anchors.has(base) ? "section-" + block.id : base) : "";
    if (base) anchors.add(base);
    return renderBlock(block, anchor);
  }).join("\n");
}

export function exportHtml(page) {
  const normalized = parseDocument(page);
  return [
    "<!doctype html>",
    '<html lang="en"><head><meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    "<title>" + escapeHtml(normalized.title) + "</title>",
    '<link rel="stylesheet" href="syntyr.all.css">',
    "</head>",
    '<body class="syn-root syn-page" data-syn-theme="' + escapeHtml(normalized.theme) + '">',
    '<main class="syn-shell">' + renderSections(normalized) + "</main>",
    "</body></html>"
  ].join("\n");
}
