import { LitElement, html } from "lit";

// Light DOM: Syntyr's existing class selectors can style rendered elements.
// Only use this when shadow encapsulation is not required.
export class DemoStatusPanel extends LitElement {
  static properties = {
    service: { type: String },
    online: { type: Boolean, reflect: true },
    busy: { type: Boolean, reflect: true },
  };

  constructor() {
    super();
    this.service = "North hub";
    this.online = false;
    this.busy = false;
  }

  createRenderRoot() {
    // Preserve useful static content until the component upgrades.
    // Remove it on upgrade so it is not duplicated next to Lit's output.
    this.querySelector("[data-lit-fallback]")?.remove();
    return this;
  }

  _toggleStatus() {
    if (this.busy) return;
    this.online = !this.online;
    this.dispatchEvent(new CustomEvent("syn-demo-status-change", {
      detail: { service: this.service, online: this.online },
      bubbles: true,
      composed: true,
    }));
  }

  render() {
    return html`
      <article class="syn-panel" aria-label="Service status">
        <p class="syn-eyebrow">LIGHT DOM / SYNTYR CLASSES</p>
        <h3 class="syn-heading">${this.service}</h3>
        <p class="syn-status ${this.online ? "syn-status--success" : "syn-status--warning"}"
           role="status">${this.online ? "Online" : "Offline"}</p>
        <p class="syn-muted">The component renders into the light DOM. No shadow stylesheet is needed.</p>
        <button class="syn-button syn-button--primary" type="button"
                ?disabled=${this.busy} @click=${this._toggleStatus}>
          ${this.online ? "Mark offline" : "Mark online"}
        </button>
      </article>
    `;
  }
}

customElements.define("syn-demo-status-panel", DemoStatusPanel);
