import logging
import voluptuous as vol
import re
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.components import websocket_api
from homeassistant.helpers import device_registry as dr

from .api import HakboardAPI
from .const import (
    DOMAIN,
    CONF_API_ENDPOINT,
    CONF_API_TOKEN,
    CONF_INSTANCE_KEY,
    CONF_PROJECT_FILTER,
    CONF_POLL_INTERVAL_SECONDS,
    DEFAULT_POLL_INTERVAL,
    CONF_DISPLAY_NAME,
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
def websocket_get_endpoints(hass, connection, msg):
    entries = hass.config_entries.async_entries(DOMAIN)
    result = []
    for entry in entries:
        result.append({
            "entry_id": entry.entry_id,
            "title": entry.title,
            "endpoint_id": entry.data.get(CONF_INSTANCE_KEY, "Unknown"),
        })
    connection.send_result(msg["id"], result)


# =========================================================
#   SETUP ENTRY
# =========================================================
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.info("HAKBOARD: Starting setup for %s", entry.title)

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
    except Exception:
        pass

    # 3. Standard Setup Logic
    config = {**entry.data, **entry.options}

    instance_key_cased = config.get(CONF_INSTANCE_KEY)
    instance_key = instance_key_cased.lower()

    display_name = entry.title

    poll_interval = config.get(CONF_POLL_INTERVAL_SECONDS, DEFAULT_POLL_INTERVAL)
    api_endpoint = config.get(CONF_API_ENDPOINT)
    api_token = config.get(CONF_API_TOKEN)

    filter_text = config.get(CONF_PROJECT_FILTER, "")
    allowed_ids = parse_text_into_ids(filter_text)

    api = HakboardAPI(api_endpoint, api_token)

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

    # REGISTER DEVICE AS A “SERVICE”
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, instance_key)},
        manufacturer="HAKboard",
        name=f"HAKboard ({display_name})",
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
