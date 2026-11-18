/* Docs-only CodeMirror 6 adapter. No CodeMirror code ships in Syntyr's CSS package. */
import { EditorView, basicSetup } from "codemirror";
import { html } from "@codemirror/lang-html";

const textarea = document.getElementById("playground-markup");
const mount = document.getElementById("playground-editor-mount");

if (textarea && mount) {
  let view;
  try {
    // The static textarea remains the contract with the existing playground.
    // All CodeMirror edits synchronously update it and trigger the live preview.
    view = new EditorView({
      parent: mount,
      doc: textarea.value,
      extensions: [
        basicSetup,
        html(),
        EditorView.lineWrapping,
        EditorView.contentAttributes.of({
          "aria-labelledby": "playground-markup-label",
          "aria-describedby": "playground-help",
          "spellcheck": "false"
        }),
        EditorView.theme({
          "&": {
            minHeight: "23rem",
            backgroundColor: "var(--syn-surface)",
            color: "var(--syn-text)",
            fontSize: ".875rem",
            borderRadius: "var(--syn-radius)",
            border: "1px solid var(--syn-border-default)"
          },
          "&.cm-focused": {
            outline: "2px solid var(--syn-accent)",
            outlineOffset: "2px"
          },
          ".cm-scroller": {
            maxHeight: "65vh",
            overflow: "auto",
            fontFamily: "var(--syn-mono, ui-monospace, monospace)",
            lineHeight: "1.55"
          },
          ".cm-content": { padding: "1rem .35rem", caretColor: "var(--syn-text)" },
          ".cm-gutters": {
            backgroundColor: "var(--syn-bg)",
            color: "var(--syn-muted, #64748b)",
            borderRight: "1px solid var(--syn-border-default)"
          },
          ".cm-activeLine": { backgroundColor: "color-mix(in srgb, var(--syn-accent) 6%, transparent)" },
          ".cm-activeLineGutter": { backgroundColor: "color-mix(in srgb, var(--syn-accent) 8%, transparent)" }
        }),
        EditorView.updateListener.of(update => {
          if (!update.docChanged) return;
          textarea.value = update.state.doc.toString();
          textarea.dispatchEvent(new Event("input", { bubbles: true }));
        })
      ]
    });

    // Switching examples is owned by playground.js. Synchronize via a
    // dedicated event rather than monkeypatching textarea.value.
    const syncFromTextarea = () => {
      const next = textarea.value;
      if (view.state.doc.toString() === next) return;
      view.dispatch({
        changes: { from: 0, to: view.state.doc.length, insert: next }
      });
    };
    textarea.addEventListener("syntyr:load-example", syncFromTextarea);
    textarea.addEventListener("input", syncFromTextarea);

    // Hide the fallback only after CodeMirror has mounted successfully.
    mount.hidden = false;
    textarea.hidden = true;
    mount.dataset.editor = "codemirror6";
  } catch (error) {
    view?.destroy();
    mount.replaceChildren();
    mount.hidden = true;
    textarea.hidden = false;
    console.warn("CodeMirror unavailable; using the native textarea.", error);
  }
}
