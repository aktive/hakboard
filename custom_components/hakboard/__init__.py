"""The HAKboard integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.components import websocket_api
from homeassistant.helpers import device_registry as dr
from homeassistant.loader import async_get_integration

from .api import HakboardAPI
from .const import (
    DOMAIN,
    CONF_API_ENDPOINT,
    CONF_API_TOKEN,
    CONF_INSTANCE_KEY,
    CONF_INSTANCE_NAME,
    CONF_DISPLAY_NAME,  # Backward compatibility
    CONF_PROJECT_FILTER,
    CONF_POLL_INTERVAL_SECONDS,
    CONF_VERIFY_SSL,
    DEFAULT_POLL_INTERVAL,
    DEFAULT_INSTANCE_NAME,
    DEFAULT_VERIFY_SSL,
)
from .utils import parse_text_into_ids

_LOGGER = logging.getLogger(__name__)

FRONTEND_SCRIPT_URL = "/hakboard_static/hakboard-status-card.js"

# =========================================================
#   WEBSOCKET
# =========================================================
@websocket_api.websocket_command({
    vol.Required("type"): "hakboard/get_endpoints",
})
@callback
def websocket_get_endpoints(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle WebSocket request to get HAKboard instance keys."""
    entries = hass.config_entries.async_entries(DOMAIN)
    result = []
    for entry in entries:
        result.append({
            "entry_id": entry.entry_id,
            "title": entry.title,
            "instance_key": entry.data.get(CONF_INSTANCE_KEY, "Unknown"),
        })
    connection.send_result(msg["id"], result)


# =========================================================
#   SETUP ENTRY
# =========================================================
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.info("Setting up HAKboard integration: %s", entry.title)

    # 1. Register frontend assets
    await hass.http.async_register_static_paths([
        StaticPathConfig(
            "/hakboard_static",
            hass.config.path("custom_components/hakboard/frontend"),
            cache_headers=True,
        )
    ])
    add_extra_js_url(hass, FRONTEND_SCRIPT_URL)

    # 2. Register custom WebSocket API
    try:
        websocket_api.async_register_command(hass, websocket_get_endpoints)
    except ValueError:
        # Command already registered (e.g., during reload)
        _LOGGER.debug("WebSocket command already registered")

    # 3. Standard Setup Logic
    config = {**entry.data, **entry.options}

    instance_key_cased = config.get(CONF_INSTANCE_KEY)
    instance_key = instance_key_cased.lower()

    # Get instance_name with backward compatibility for display_name
    instance_name = config.get(CONF_INSTANCE_NAME) or config.get(
        CONF_DISPLAY_NAME, DEFAULT_INSTANCE_NAME
    )

    poll_interval = config.get(CONF_POLL_INTERVAL_SECONDS, DEFAULT_POLL_INTERVAL)
    api_endpoint = config.get(CONF_API_ENDPOINT)
    api_token = config.get(CONF_API_TOKEN)
    verify_ssl = config.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL)

    filter_text = config.get(CONF_PROJECT_FILTER, "")
    allowed_ids = parse_text_into_ids(filter_text)

    api = HakboardAPI(
        api_endpoint, api_token, verify_ssl,
        instance_key=instance_key,
        instance_name=instance_name,
    )

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"{DOMAIN}_{instance_key}",
        update_method=lambda: api.async_fetch_data(allowed_ids),
        update_interval=timedelta(seconds=poll_interval),
    )

    coordinator.config_entry = entry

    # Store state
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "instance_key": instance_key
    }

    # REGISTER DEVICE AS A "SERVICE"
    # Get version from manifest.json
    integration = await async_get_integration(hass, DOMAIN)
    sw_version = str(integration.version) if integration.version else "unknown"

    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, instance_key)},
        manufacturer="HAKboard",
        name=f"HAKboard • {instance_name}",
        model="Kanboard Integration",
        sw_version=sw_version,
        entry_type="service",
    )

    entry.async_on_unload(entry.add_update_listener(update_listener))

    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Reload integration when options are changed."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
