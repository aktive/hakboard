console.info(
  "%c HAKboard-Status-Card %c v0.1.0 ",
  "color: white; background: #b3710eff; font-weight: bold;",
  "color: #b3710eff; background: white;"
);

// Official HA approach: import from unpkg CDN
import {
  LitElement,
  html,
  css,
} from "https://unpkg.com/lit@3.2.0/index.js?module";

class HakboardStatusCard extends LitElement {
  static get properties() {
    return { hass: {}, config: {} };
  }

  static getConfigElement() {
    return document.createElement("hakboard-status-card-editor");
  }

  static getStubConfig(hass) {
    const defaults = {
      show_workload: true,
      show_filter: true,
      show_interval: true,
      show_kanboard_link: true,
      show_config: true,
      show_refresh: true,

      show_total_projects: true,
      show_synced_projects: true,
      show_total_users: true,
      show_active_users: true,
      show_admin_users: true,

      endpoint: "hl",
    };

    const system = Object.keys(hass.states).filter(
      (e) => e.startsWith("sensor.hakboard_") && e.endsWith("_system_status")
    );
    if (system.length > 0) {
      const p = system[0].split("_");
      if (p.length >= 3) defaults.endpoint = p[1].toLowerCase();
      return defaults;
    }

    const summary = Object.keys(hass.states).filter(
      (e) => e.startsWith("sensor.hakboard_") && e.endsWith("_summary_status")
    );
    if (summary.length > 0) {
      const p = summary[0].split("_");
      if (p.length >= 3) defaults.endpoint = p[1].toLowerCase();
    }

    return defaults;
  }

  static get styles() {
    return css`
      ha-card {
        display: flex;
        flex-direction: column;
      }

      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 6px 0 16px;
      }

      .title {
        font-size: var(--paper-font-headline_-_font-size);
        font-weight: var(--paper-font-headline_-_font-weight);
        color: var(--primary-text-color);
      }

      .header-actions {
        display: flex;
        gap: 2px;
      }

      .icon-btn {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--secondary-text-color);
        cursor: pointer;
        transition: background 0.2s;
      }

      .icon-btn:hover {
        background: rgba(127, 127, 127, 0.15);
        color: var(--primary-text-color);
      }

      .card-content {
        padding: 14px 16px 18px 16px;
      }

      .row {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
      }

      .row:last-child {
        margin-bottom: 0;
      }

      .row ha-icon {
        margin-right: 14px;
      }

      .label-value {
        display: flex;
        gap: 4px;
        align-items: baseline;
      }

      .label-value .lbl {
        font-weight: bold;
      }

      .error {
        color: var(--error-color);
      }
    `;
  }

  setConfig(config) {
    if (!config.endpoint) throw new Error("Missing 'endpoint'");
    this.config = config;
  }

  _timeAgo(ts) {
    if (!ts) return "Never";
    const d = new Date(ts);
    const sec = Math.max(0, (Date.now() - d) / 1000);
    const units = [
      [31536000, "years"],
      [2592000, "months"],
      [86400, "days"],
      [3600, "hours"],
      [60, "minutes"],
    ];
    for (const [div, label] of units) {
      const v = sec / div;
      if (v > 1) return `${Math.floor(v)} ${label} ago`;
    }
    return `${Math.floor(sec)} seconds ago`;
  }

  render() {
    if (!this.hass || !this.config) return html``;

    const ep = (this.config.endpoint || "").toLowerCase();
    const id = `sensor.hakboard_${ep}_system_status`;
    const s = this.hass.states[id];

    if (!s) {
      return html`
        <ha-card>
          <div class="card-content">
            <div class="row">
              <ha-icon icon="mdi:alert-circle" class="error"></ha-icon>
              <div>
                <div class="lbl error">Instance Not Available</div>
                <div>Entity '${id}' not found.</div>
              </div>
            </div>
          </div>
        </ha-card>
      `;
    }

    const title = this.config.title || `${s.attributes.instance_name} • Status`;

    const totalProj = this.hass.states[`sensor.hakboard_${ep}_summary_projects_total`]?.state;
    const syncedProj = this.hass.states[`sensor.hakboard_${ep}_summary_projects_synced`]?.state;
    const users = this.hass.states[`sensor.hakboard_${ep}_summary_users`];
    const totUsers = users?.state;
    const actUsers = users?.attributes?.active_count;
    const admUsers = users?.attributes?.admin_count;

    return html`
      <ha-card>
        <div class="card-header">
          <div class="title">${title}</div>

          <div class="header-actions">
            ${this.config.show_kanboard_link !== false
              ? html`
                  <div class="icon-btn" @click=${() => this._handleKanboard(s)}>
                    <ha-icon icon="mdi:open-in-new"></ha-icon>
                  </div>
                `
              : ""}

            ${this.config.show_config !== false
              ? html`
                  <div class="icon-btn" @click=${() => this._handleConfig()}>
                    <ha-icon icon="mdi:cog"></ha-icon>
                  </div>
                `
              : ""}

            ${this.config.show_refresh !== false
              ? html`
                  <div class="icon-btn" @click=${() => this._handleSync(s)}>
                    <ha-icon icon="mdi:refresh"></ha-icon>
                  </div>
                `
              : ""}
          </div>
        </div>

        <div class="card-content">
          ${this.config.show_workload !== false
            ? html`
                <div class="row">
                  <ha-icon icon="mdi:pulse"></ha-icon>
                  <div class="label-value">
                    <span class="lbl">Total Workload:</span>
                    <span>${s.state} Tasks</span>
                  </div>
                </div>
              `
            : ""}

          ${this.config.show_filter !== false
            ? html`
                <div class="row">
                  <ha-icon icon="mdi:filter"></ha-icon>
                  <div class="label-value">
                    <span class="lbl">Project Filter:</span>
                    <span>${s.attributes.project_filter}</span>
                  </div>
                </div>
              `
            : ""}

          ${this.config.show_interval !== false
            ? html`
                <div class="row">
                  <ha-icon icon="mdi:timer-outline"></ha-icon>
                  <div class="label-value">
                    <span class="lbl">Polling Interval:</span>
                    <span>${s.attributes.poll_interval}</span>
                  </div>
                </div>
              `
            : ""}

          ${this.config.show_total_projects !== false
            ? html`
                <div class="row">
                  <ha-icon icon="mdi:clipboard-list-outline"></ha-icon>
                  <div class="label-value">
                    <span class="lbl">Total Projects:</span>
                    <span>${totalProj}</span>
                  </div>
                </div>
              `
            : ""}

          ${this.config.show_synced_projects !== false
            ? html`
                <div class="row">
                  <ha-icon icon="mdi:clipboard-check-outline"></ha-icon>
                  <div class="label-value">
                    <span class="lbl">Synced Projects:</span>
                    <span>${syncedProj}</span>
                  </div>
                </div>
              `
            : ""}

          ${this.config.show_total_users !== false
            ? html`
                <div class="row">
                  <ha-icon icon="mdi:account-group-outline"></ha-icon>
                  <div class="label-value">
                    <span class="lbl">Total Users:</span>
                    <span>${totUsers}</span>
                  </div>
                </div>
              `
            : ""}

          ${this.config.show_active_users !== false
            ? html`
                <div class="row">
                  <ha-icon icon="mdi:account-check-outline"></ha-icon>
                  <div class="label-value">
                    <span class="lbl">Active Users:</span>
                    <span>${actUsers}</span>
                  </div>
                </div>
              `
            : ""}

          ${this.config.show_admin_users !== false
            ? html`
                <div class="row">
                  <ha-icon icon="mdi:shield-account"></ha-icon>
                  <div class="label-value">
                    <span class="lbl">Admins:</span>
                    <span>${admUsers}</span>
                  </div>
                </div>
              `
            : ""}
        </div>
      </ha-card>
    `;
  }

  _handleSync(state) {
    if (!state || !state.attributes || !state.attributes.config_entry_id) {
      console.warn("HAKboard: No config_entry_id on system_status entity");
      return;
    }

    const configEntryId = state.attributes.config_entry_id;

    this.hass.callService("homeassistant", "reload_config_entry", {
      entry_id: configEntryId,
    });
  }

  _handleConfig() {
    window.history.pushState(null, "", "/config/integrations/integration/hakboard");
    window.dispatchEvent(new Event("location-changed", { bubbles: true, composed: true }));
  }

  _handleKanboard(state) {
    // Use custom URL if set, otherwise fall back to instance_url from sensor
    const customUrl = this.config.custom_kanboard_url;
    const defaultUrl = state?.attributes?.instance_url;

    let url = customUrl || defaultUrl;

    if (!url) {
      console.warn("HAKboard: No URL available (custom or instance_url)");
      return;
    }

    // Ensure URL has a protocol (http:// or https://)
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
      url = "https://" + url;
    }

    window.open(url, "_blank");
  }
}

customElements.define("hakboard-status-card", HakboardStatusCard);

class HakboardStatusCardEditor extends LitElement {
  static get properties() {
    return {
      hass: {},
      config: {},
      _endpoints: { state: true },
      _showCustomUrl: { state: true },
      _urlError: { state: true }
    };
  }

  static get styles() {
    return css`
      .card-config { display: flex; flex-direction: column; gap: 16px; }

      .field { display: flex; flex-direction: column; gap: 6px; }

      select, input[type="text"] {
        width: 100%;
        padding: 8px;
        box-sizing: border-box;
        border: 1px solid var(--divider-color);
        border-radius: 4px;
        background: var(--card-background-color);
        color: var(--primary-text-color);
      }

      .checkbox-columns {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
      }

      .checkbox-column {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }

      .checkbox-row {
        display: flex;
        align-items: center;
        gap: 10px;
      }

      .checkbox-row label {
        cursor: pointer;
      }

      .checkbox-with-toggle {
        display: flex;
        align-items: center;
        gap: 6px;
      }

      .toggle-cog {
        --mdc-icon-size: 15px;
        font-size: 15px;
        cursor: pointer;
        color: var(--secondary-text-color);
        transition: color 0.2s;
        display: inline-flex;
        align-items: center;
      }

      .toggle-cog:hover {
        color: var(--primary-text-color);
      }

      .custom-url-field {
        margin-top: 6px;
      }

      .custom-url-field input {
        width: 100%;
      }

      .custom-url-field input.error {
        border-color: var(--error-color);
      }

      .error-message {
        color: var(--error-color);
        font-size: 12px;
        margin-top: 4px;
      }
    `;
  }

  setConfig(cfg) {
    this.config = cfg;
  }

  set hass(h) {
    this._hass = h;
    if (h && !this._endpoints) this._fetchEndpoints();
  }

  get hass() {
    return this._hass;
  }

  async _fetchEndpoints() {
    try {
      const res = await this.hass.callWS({ type: "hakboard/get_endpoints" });
      const eps = [...new Set(res.map((x) => x.instance_key?.toLowerCase()).filter(Boolean))].sort();

      this._endpoints = eps;

      const cfgEp = (this.config.endpoint || "").toLowerCase();
      if (!cfgEp && eps.length > 0) this._emitChange("endpoint", eps[0]);

      this.requestUpdate();
    } catch (e) {
      console.error("HAKboard: WS fetch failed", e);
      this._endpoints = [];
    }
  }

  render() {
    if (!this.config) return html``;

    const opts = this._endpoints || [];
    const cfgEp = (this.config.endpoint || "").toLowerCase();
    const check = (v) => v !== false;

    return html`
      <div class="card-config">

        <div class="field">
          <div>Instance Key</div>
          <select .value=${cfgEp} @change=${(e) => this._chg(e, "endpoint")}>
            ${opts.map((ep) => html`<option value=${ep}>${ep}</option>`)}
            ${!opts.includes(cfgEp) && cfgEp
              ? html`<option selected value=${cfgEp}>${cfgEp}</option>`
              : ""}
          </select>
        </div>

        <div class="field">
          <div>Card Title (optional)</div>
          <input
            type="text"
            .value=${this.config.title || ""}
            @input=${(e) => this._chg(e, "title")}
          />
        </div>

        <div class="checkbox-columns">
          <div class="checkbox-column">
            ${this._checkbox("Total Workload", "show_workload", check)}
            ${this._checkbox("Project Filter", "show_filter", check)}
            ${this._checkbox("Polling Interval", "show_interval", check)}
            ${this._checkbox("Total Projects", "show_total_projects", check)}
            ${this._checkbox("Synced Projects", "show_synced_projects", check)}
            ${this._checkbox("Total Users", "show_total_users", check)}
            ${this._checkbox("Active Users", "show_active_users", check)}
            ${this._checkbox("Admins", "show_admin_users", check)}
          </div>

          <div class="checkbox-column">
            ${this._checkboxWithToggle("Kanboard Link Button", "show_kanboard_link", check)}
            ${this._showCustomUrl ? html`
              <div class="custom-url-field">
                <input
                  type="text"
                  placeholder="Custom URL (optional)"
                  .value=${this.config.custom_kanboard_url || ""}
                  @input=${(e) => this._handleUrlInput(e)}
                  class=${this._urlError ? "error" : ""}
                />
                ${this._urlError ? html`<div class="error-message">${this._urlError}</div>` : ""}
              </div>
            ` : ""}
            ${this._checkbox("Config Button", "show_config", check)}
            ${this._checkbox("Refresh Button", "show_refresh", check)}
          </div>
        </div>
      </div>
    `;
  }

  _checkbox(label, key, checkFn) {
    const id = `hakboard-${key}`;
    return html`
      <div class="checkbox-row">
        <input
          type="checkbox"
          id=${id}
          ?checked=${checkFn(this.config[key])}
          @change=${(e) => this._chg(e, key, true)}
        />
        <label for=${id}>${label}</label>
      </div>
    `;
  }

  _checkboxWithToggle(label, key, checkFn) {
    const id = `hakboard-${key}`;
    return html`
      <div class="checkbox-row">
        <input
          type="checkbox"
          id=${id}
          ?checked=${checkFn(this.config[key])}
          @change=${(e) => this._chg(e, key, true)}
        />
        <div class="checkbox-with-toggle">
          <label for=${id}>${label}</label>
          <ha-icon
            class="toggle-cog"
            icon="mdi:cog-outline"
            @click=${() => this._toggleCustomUrl()}
          ></ha-icon>
        </div>
      </div>
    `;
  }

  _toggleCustomUrl() {
    this._showCustomUrl = !this._showCustomUrl;
  }

  _handleUrlInput(e) {
    const value = e.target.value.trim();

    // Clear error if field is empty (optional field)
    if (!value) {
      this._urlError = null;
      this._emitChange("custom_kanboard_url", "");
      return;
    }

    // Validate URL format
    if (!this._isValidUrl(value)) {
      this._urlError = "Please enter a valid URL";
    } else {
      this._urlError = null;
    }

    this._emitChange("custom_kanboard_url", value);
  }

  _isValidUrl(urlString) {
    // Only reject things that will actually break or cause errors
    // Allow simple hostnames for homelab DNS entries (e.g., "kanboard", "server")

    // Reject if starts with invalid characters (not alphanumeric or protocol)
    if (/^[^a-zA-Z0-9]/.test(urlString) && !urlString.startsWith("http")) {
      return false;
    }

    // Reject strings with characters that browsers can't handle
    const invalidChars = /[<>"\s{}|\\^`]/;
    if (invalidChars.test(urlString)) {
      return false;
    }

    // Reject strings that are obviously garbage (multiple consecutive special chars)
    if (/[#@]{2,}|[@#&]{3,}/.test(urlString)) {
      return false;
    }

    // Try to construct URL object - if it fails, it's invalid
    try {
      let testUrl = urlString;
      // Add protocol if missing
      if (!urlString.startsWith("http://") && !urlString.startsWith("https://")) {
        testUrl = "https://" + urlString;
      }

      const url = new URL(testUrl);

      // Must have a hostname
      if (!url.hostname) {
        return false;
      }

      // Hostname should only contain valid characters
      // Allow hyphens and dots, plus alphanumeric
      if (!/^[a-zA-Z0-9.-]+$/.test(url.hostname)) {
        return false;
      }

      return true;
    } catch {
      return false;
    }
  }

  _chg(ev, key, isChk = false) {
    const val = isChk ? ev.target.checked : ev.target.value;
    this._emitChange(key, key === "endpoint" ? val.toLowerCase() : val);
  }

  _emitChange(key, val) {
    this.dispatchEvent(
      new CustomEvent("config-changed", {
        detail: { config: { ...this.config, [key]: val } },
        bubbles: true,
        composed: true,
      })
    );
  }
}

customElements.define("hakboard-status-card-editor", HakboardStatusCardEditor);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "hakboard-status-card",
  name: "HAKboard Status",
  description: "Show system health and sync controls.",
  preview: true,
});
