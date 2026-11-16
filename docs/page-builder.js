/* Docs-only, dependency-free visual composition. The shipped Syntyr CSS stays JS-free. */
import {
  BLOCK_TYPES, BLOCK_DEFINITIONS, THEMES,
  createBlock, createDefaultDocument, parseDocument, moveBlock, exportHtml
} from "./page-builder-model.mjs";

const byId = (id) => document.getElementById(id);
const palette = byId("builder-palette");
const outline = byId("builder-outline");
const inspector = byId("builder-inspector");
const preview = byId("builder-preview");
const status = byId("builder-status");
const theme = byId("builder-theme");
const title = byId("builder-page-title");
const viewport = byId("builder-viewport");
const viewportFrame = byId("builder-viewport-frame");
const undo = byId("builder-undo");
const redo = byId("builder-redo");
const history = [];
const future = [];
let page = createDefaultDocument();
let selectedId = page.blocks[0].id;
let sequence = 4;
let draggingIndex = null;
let titleEditing = false;

function notify(message) {
  status.textContent = message;
}
function remember(snapshot = JSON.stringify(page)) {
  history.push(snapshot);
  if (history.length > 40) history.shift();
  future.length = 0;
  updateHistoryButtons();
}
function updateHistoryButtons() {
  undo.disabled = !history.length;
  redo.disabled = !future.length;
}
function commit(next, message) {
  const normalized = parseDocument(next);
  remember();
  page = normalized;
  if (!page.blocks.some(block => block.id === selectedId)) selectedId = page.blocks[0]?.id || null;
  redraw();
  notify(message);
}
function makeElement(tag, text, className) {
  const element = document.createElement(tag);
  if (text !== undefined && text !== null) element.textContent = text;
  if (className) element.className = className;
  return element;
}
function makeButton(label, action, disabled = false) {
  const element = makeElement("button", label);
  element.type = "button";
  element.dataset.action = action;
  element.disabled = disabled;
  return element;
}

function renderPalette() {
  for (const type of BLOCK_TYPES) {
    const def = BLOCK_DEFINITIONS[type];
    const button = makeElement("button", null, "builder-add");
    button.type = "button";
    button.dataset.blockType = type;
    button.append(makeElement("strong", "+ " + def.label), makeElement("small", def.description));
    palette.append(button);
  }
}
function renderOutline() {
  outline.replaceChildren();
  page.blocks.forEach((block, index) => {
    const item = makeElement("li", null, "builder-outline-item");
    item.draggable = true;
    item.dataset.index = String(index);
    item.dataset.selected = String(block.id === selectedId);
    const name = makeButton((index + 1) + ". " + BLOCK_DEFINITIONS[block.type].label, "select");
    name.className = "builder-outline-select";
    name.setAttribute("aria-label", "Edit " + BLOCK_DEFINITIONS[block.type].label + ", block " + (index + 1));
    const actions = makeElement("div", null, "builder-outline-actions");
    actions.append(
      makeButton("↑ Up", "up", index === 0),
      makeButton("↓ Down", "down", index === page.blocks.length - 1),
      makeButton("Remove", "remove")
    );
    item.append(name, actions);
    outline.append(item);
  });
  updateHistoryButtons();
}
function renderInspector() {
  inspector.replaceChildren();
  const block = page.blocks.find(item => item.id === selectedId);
  if (!block) {
    inspector.append(makeElement("p", "Add or select a block to edit its content."));
    byId("builder-inspector-help").textContent = "No block selected.";
    return;
  }
  const def = BLOCK_DEFINITIONS[block.type];
  byId("builder-inspector-help").textContent = def.description;
  inspector.append(makeElement("p", def.label, "builder-block-name"));
  for (const name of Object.keys(def.fields)) {
    const label = makeElement("label", null, "syn-label");
    const friendlyName = name.replace(/([A-Z])/g, " $1").toUpperCase();
    label.append(document.createTextNode(friendlyName));
    const value = block.props[name];
    const multi = value.length > 65 || /description|answer|quote|Text$/i.test(name);
    const control = makeElement(multi ? "textarea" : "input", null, "syn-input");
    if (multi) control.rows = 3;
    else control.type = "text";
    control.value = value;
    control.maxLength = 5000;
    control.dataset.field = name;
    control.autocomplete = "off";
    let editing = false;
    control.addEventListener("input", () => {
      if (!editing) { remember(); editing = true; }
      const current = page.blocks.find(item => item.id === selectedId);
      if (!current) return;
      current.props[name] = control.value;
      renderPreview();
      notify("Block content updated. Save project JSON to keep it editable.");
    });
    control.addEventListener("blur", () => { editing = false; });
    label.append(control);
    inspector.append(label);
  }
}

function renderPreview() {
  // Imported content is validated and every user string escaped by exportHtml.
  // The iframe cannot run scripts or submit forms, including pasted hostile content.
  const styleOrigin = /^https?:$/.test(location.protocol) ? location.origin : "'self'";
  const csp = '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'self\' \'unsafe-inline\' ' +
    styleOrigin + '; img-src data:; base-uri \'none\'; form-action \'none\'">';
  preview.srcdoc = exportHtml(page)
    .replace('href="syntyr.all.css"', 'href="../dist/syntyr.all.css"')
    .replace("</head>", csp + "</head>");
}
preview.addEventListener("load", () => {
  try {
    const frameDoc = preview.contentDocument;
    if (!frameDoc) return;
    for (const block of frameDoc.querySelectorAll("[data-syntyr-block-id]")) {
      if (block.dataset.syntyrBlockId === selectedId) {
        block.style.outline = "2px solid var(--syn-accent)";
        block.style.outlineOffset = "3px";
      }
    }
    frameDoc.addEventListener("click", (event) => {
      event.preventDefault();
      const block = event.target.closest("[data-syntyr-block-id]");
      if (block && block.dataset.syntyrBlockId !== selectedId) {
        selectedId = block.dataset.syntyrBlockId;
        renderOutline();
        renderInspector();
        renderPreview();
      }
    });
  } catch {
    notify("The sandbox prevented preview selection. Edit using the page outline.");
  }
});
function redraw() {
  title.value = page.title;
  theme.value = page.theme;
  renderOutline();
  renderInspector();
  renderPreview();
}
function nextBlockId(type) {
  let id;
  do { id = type + "-" + sequence++; }
  while (page.blocks.some(block => block.id === id));
  return id;
}
function shift(from, to) {
  if (from === to) return;
  const movedId = page.blocks[from].id;
  commit(moveBlock(page, from, to), "Block reordered.");
  selectedId = movedId;
  renderOutline();
  renderInspector();
}
palette.addEventListener("click", (event) => {
  const button = event.target.closest("[data-block-type]");
  if (!button) return;
  try {
    const block = createBlock(button.dataset.blockType, nextBlockId(button.dataset.blockType));
    const next = structuredClone(page);
    next.blocks.push(block);
    commit(next, BLOCK_DEFINITIONS[block.type].label + " added.");
    selectedId = block.id;
    redraw();
  } catch (error) {
    notify(error.message);
  }
});
outline.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-action]");
  const item = event.target.closest("[data-index]");
  if (!button || !item) return;
  const index = Number(item.dataset.index);
  const action = button.dataset.action;
  if (action === "select") {
    selectedId = page.blocks[index].id;
    redraw();
    return;
  }
  if (action === "up" && index > 0) shift(index, index - 1);
  if (action === "down" && index < page.blocks.length - 1) shift(index, index + 1);
  if (action === "remove") {
    const next = structuredClone(page);
    next.blocks.splice(index, 1);
    commit(next, "Block removed.");
  }
});
outline.addEventListener("dragstart", (event) => {
  const item = event.target.closest("[data-index]");
  if (!item) return;
  draggingIndex = Number(item.dataset.index);
  event.dataTransfer.effectAllowed = "move";
  event.dataTransfer.setData("text/plain", String(draggingIndex));
});
outline.addEventListener("dragover", (event) => {
  if (event.target.closest("[data-index]")) event.preventDefault();
});
outline.addEventListener("drop", (event) => {
  const item = event.target.closest("[data-index]");
  if (!item || draggingIndex === null) return;
  event.preventDefault();
  shift(draggingIndex, Number(item.dataset.index));
  draggingIndex = null;
});
outline.addEventListener("dragend", () => { draggingIndex = null; });

function stepBack() {
  if (!history.length) return;
  future.push(JSON.stringify(page));
  page = parseDocument(history.pop());
  if (!page.blocks.some(item => item.id === selectedId)) selectedId = page.blocks[0]?.id || null;
  redraw();
  notify("Change undone.");
}
function stepForward() {
  if (!future.length) return;
  history.push(JSON.stringify(page));
  page = parseDocument(future.pop());
  if (!page.blocks.some(item => item.id === selectedId)) selectedId = page.blocks[0]?.id || null;
  redraw();
  notify("Change restored.");
}
undo.addEventListener("click", stepBack);
redo.addEventListener("click", stepForward);
document.addEventListener("keydown", (event) => {
  if (!(event.ctrlKey || event.metaKey) || event.altKey) return;
  if (/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName || "")) return;
  if (event.key.toLowerCase() === "z") {
    event.preventDefault();
    if (event.shiftKey) stepForward();
    else stepBack();
  } else if (event.key.toLowerCase() === "y") {
    event.preventDefault();
    stepForward();
  }
});
title.addEventListener("input", () => {
  if (!titleEditing) { remember(); titleEditing = true; }
  page.title = title.value;
  renderPreview();
});
title.addEventListener("blur", () => { titleEditing = false; });
theme.addEventListener("change", () => {
  if (!THEMES.includes(theme.value) || theme.value === page.theme) return;
  const next = structuredClone(page);
  next.theme = theme.value;
  commit(next, "Theme updated to " + theme.value + ".");
});
viewport.addEventListener("change", () => {
  const value = ["desktop", "tablet", "mobile"].includes(viewport.value) ? viewport.value : "desktop";
  viewportFrame.className = "builder-viewport builder-viewport--" + value;
  notify("Preview: " + value + ".");
});
function download(filename, data, type) {
  const url = URL.createObjectURL(new Blob([data], { type }));
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.append(link);
  link.click();
  link.remove();
  // Keep the object URL alive while the browser finalizes its download.
  setTimeout(() => URL.revokeObjectURL(url), 30000);
}
byId("builder-export-html").addEventListener("click", () => {
  download("index.html", exportHtml(page), "text/html;charset=utf-8");
  notify("HTML exported. Download syntyr.all.css alongside index.html.");
});
byId("builder-export-json").addEventListener("click", () => {
  download("syntyr-page.json", JSON.stringify(parseDocument(page), null, 2) + "\n", "application/json");
  notify("Editable JSON project downloaded.");
});
byId("builder-import").addEventListener("change", async (event) => {
  const file = event.target.files?.[0];
  if (!file) return;
  try {
    if (file.size > 500000) throw new Error("Project file exceeds 500 KB");
    const imported = parseDocument(await file.text());
    commit(imported, "Project opened.");
    sequence = Math.max(sequence, imported.blocks.length + 5);
  } catch (error) {
    notify("Cannot open project: " + error.message);
  } finally {
    event.target.value = "";
  }
});

renderPalette();
redraw();
