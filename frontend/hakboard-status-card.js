console.info(
  "%c HAKboard-Satus-Card %c v0.1.0 ",
  "color: white; background: #b3710eff; font-weight: bold;",
  "color: #b3710eff; background: white;"
);

import {
  LitElement,
  html,
  css,
} from "https://unpkg.com/lit@2.8.0/index.js?module";

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
        padding: 14px 16px 0 16px;
      }

      .title {
        font-size: var(--paper-font-headline_-_font-size);
        font-weight: var(--paper-font-headline_-_font-weight);
        color: var(--primary-text-color);
      }

      .header-actions {
        display: flex;
        gap: 6px;
      }

      .icon-btn {
        width: 40px;
        height: 40px;
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

    const title = this.config.title || `${s.attributes.display_name} • Status`;

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
}

customElements.define("hakboard-status-card", HakboardStatusCard);

class HakboardStatusCardEditor extends LitElement {
  static get properties() {
    return { hass: {}, config: {}, _endpoints: { state: true } };
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

      .checkbox-row {
        display: flex;
        align-items: center;
        gap: 10px;
      }

      .checkbox-row label {
        cursor: pointer;
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
      const eps = [...new Set(res.map((x) => x.endpoint_id?.toLowerCase()).filter(Boolean))].sort();

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

        ${this._checkbox("Total Workload", "show_workload", check)}
        ${this._checkbox("Project Filter", "show_filter", check)}
        ${this._checkbox("Polling Interval", "show_interval", check)}
        ${this._checkbox("Config Button", "show_config", check)}
        ${this._checkbox("Refresh Button", "show_refresh", check)}
        ${this._checkbox("Total Projects", "show_total_projects", check)}
        ${this._checkbox("Synced Projects", "show_synced_projects", check)}
        ${this._checkbox("Total Users", "show_total_users", check)}
        ${this._checkbox("Active Users", "show_active_users", check)}
        ${this._checkbox("Admins", "show_admin_users", check)}
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
