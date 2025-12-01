import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import selector
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    CONF_API_ENDPOINT,
    CONF_API_TOKEN,
    CONF_INSTANCE_KEY,
    CONF_DISPLAY_NAME,
    CONF_PROJECT_FILTER,
    CONF_POLL_INTERVAL,
    CONF_POLL_INTERVAL_SECONDS,
    DEFAULT_API_ENDPOINT,
    DEFAULT_API_TOKEN,
    DEFAULT_INSTANCE_KEY,
    DEFAULT_DISPLAY_NAME,
    DEFAULT_PROJECT_FILTER,
    DEFAULT_POLL_INTERVAL,
    MINIMUM_POLL_INTERVAL,
    MAX_INSTANCE_KEY_LENGTH,
    MAX_TEXT_LENGTH,
    INSTANCE_KEY_PATTERN,
    API_TOKEN_PATTERN,
)
from .utils import parse_text_into_ids
from .api import HakboardAPI

_LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------
# Soft API token validator (does NOT block setup)
# ---------------------------------------------------------
async def async_validate_token(endpoint: str, token: str) -> bool:
    api = HakboardAPI(endpoint, token)
    try:
        valid = await api.async_validate_credentials()
        return valid
    except Exception as err:
        _LOGGER.error("Credential validation error: %s", err)
        return False


# ---------------------------------------------------------
# Schema builder
# ---------------------------------------------------------
def get_schema(defaults=None, include_identifier=True):

    if defaults is None:
        defaults = {}

    seconds = defaults.get(CONF_POLL_INTERVAL_SECONDS, DEFAULT_POLL_INTERVAL)

    base = {
        vol.Required(
            CONF_API_ENDPOINT,
            default=defaults.get(CONF_API_ENDPOINT, DEFAULT_API_ENDPOINT),
        ): vol.All(str, vol.Length(max=MAX_TEXT_LENGTH)),

        # IMPORTANT: No length rules here.
        vol.Required(
            CONF_API_TOKEN,
            default=defaults.get(CONF_API_TOKEN, DEFAULT_API_TOKEN),
        ): cv.string,

        vol.Required(
            CONF_PROJECT_FILTER,
            default=defaults.get(CONF_PROJECT_FILTER, DEFAULT_PROJECT_FILTER),
        ): str,

        vol.Required(
            CONF_POLL_INTERVAL,
            default={
                "hours": 0,
                "minutes": seconds // 60,
                "seconds": seconds % 60,
            },
        ): selector({"duration": {}}),
    }

    if include_identifier:
        # Initial setup: instance key first, then display name, then base
        return vol.Schema(
            {
                vol.Required(
                    CONF_INSTANCE_KEY,
                    default=defaults.get(CONF_INSTANCE_KEY, DEFAULT_INSTANCE_KEY),
                ): vol.All(
                    cv.string,
                    vol.Length(min=1, max=MAX_INSTANCE_KEY_LENGTH),
                ),
                vol.Optional(
                    CONF_DISPLAY_NAME,
                    default=defaults.get(CONF_DISPLAY_NAME, DEFAULT_DISPLAY_NAME),
                ): vol.All(cv.string, vol.Length(min=1, max=20)),
                **base,
            }
        )

    # Options flow: **display name first**, then the rest of the fields
    return vol.Schema(
        {
            vol.Optional(
                CONF_DISPLAY_NAME,
                default=defaults.get(CONF_DISPLAY_NAME, DEFAULT_DISPLAY_NAME),
            ): vol.All(cv.string, vol.Length(min=1, max=20)),
            **base,
        }
    )


# ---------------------------------------------------------
# Input validation (regex, parsing, rules)
# ---------------------------------------------------------
def validate_input(user_input):
    errors = {}
    cleaned = user_input.copy()

    # -----------------------------
    # STRICT URL VALIDATION
    # -----------------------------
    endpoint = user_input.get(CONF_API_ENDPOINT, "").strip()

    try:
        cv.url(endpoint)
    except vol.Invalid:
        errors[CONF_API_ENDPOINT] = "invalid_url"
    else:
        if not endpoint.lower().endswith("/jsonrpc.php"):
            errors[CONF_API_ENDPOINT] = "invalid_url"
        elif "://" not in endpoint:
            errors[CONF_API_ENDPOINT] = "invalid_url"
        elif " " in endpoint:
            errors[CONF_API_ENDPOINT] = "invalid_url"

    # -----------------------------
    # Instance Key (setup only)
    # -----------------------------
    if CONF_INSTANCE_KEY in user_input:
        key = user_input[CONF_INSTANCE_KEY]
        if not INSTANCE_KEY_PATTERN.match(key):
            errors[CONF_INSTANCE_KEY] = "invalid_instance_key_format"

    # -----------------------------
    # API Token — Regex ONLY
    # -----------------------------
    token = user_input.get(CONF_API_TOKEN, "")
    if not API_TOKEN_PATTERN.match(token):
        errors[CONF_API_TOKEN] = "invalid_api_token_format"

    # -----------------------------
    # Project Filter
    # -----------------------------
    try:
        parse_text_into_ids(user_input[CONF_PROJECT_FILTER])
    except Exception:
        errors[CONF_PROJECT_FILTER] = "invalid_project_filter"

    # -----------------------------
    # Poll interval logic
    # -----------------------------
    d = user_input[CONF_POLL_INTERVAL]
    seconds = (
        d.get("hours", 0) * 3600
        + d.get("minutes", 0) * 60
        + d.get("seconds", 0)
    )

    if seconds < MINIMUM_POLL_INTERVAL:
        errors[CONF_POLL_INTERVAL] = "interval_too_short"
    else:
        cleaned[CONF_POLL_INTERVAL_SECONDS] = seconds

    return cleaned, errors


# =========================================================
#                   CONFIG FLOW
# =========================================================
class HakboardConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(entry):
        return HakboardOptionsFlow()

    async def async_step_user(self, user_input=None):
        errors = {}
        defaults = user_input or {}

        if user_input is not None:
            try:
                get_schema(defaults=defaults, include_identifier=True)(
                    user_input
                )
                cleaned, errors = validate_input(user_input)
            except vol.Invalid:
                errors["base"] = "invalid_input"
                cleaned = user_input

            # Duplicate instance key check
            if not errors:
                inst = cleaned[CONF_INSTANCE_KEY].lower()
                for entry in self._async_current_entries():
                    if entry.unique_id.lower() == inst:
                        errors[CONF_INSTANCE_KEY] = "endpoint_already_exists"

            # Soft token validation
            if not errors:
                ok = await async_validate_token(
                    cleaned[CONF_API_ENDPOINT],
                    cleaned[CONF_API_TOKEN],
                )
                if not ok:
                    _LOGGER.warning(
                        "Soft credential validation failed for %s",
                        cleaned[CONF_API_ENDPOINT],
                    )

            if not errors:
                inst = cleaned[CONF_INSTANCE_KEY].lower()
                await self.async_set_unique_id(inst)
                self._abort_if_unique_id_configured()

                label = (
                    cleaned.get(CONF_DISPLAY_NAME)
                    or cleaned[CONF_INSTANCE_KEY]
                )
                return self.async_create_entry(
                    title=f"HAKboard ({label})",
                    data=cleaned,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=get_schema(
                defaults=defaults,
                include_identifier=True,
            ),
            errors=errors,
            description_placeholders={
                "api_help": "URL must end with /jsonrpc.php and token must be 40–80 hex characters."
            },
        )


# =========================================================
#                   OPTIONS FLOW
# =========================================================
class HakboardOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        errors = {}
        defaults = user_input or {}

        if user_input is not None:
            try:
                # Options flow = include_identifier=False, but now includes display_name first
                get_schema(defaults=defaults, include_identifier=False)(
                    user_input
                )
                cleaned, errors = validate_input(user_input)
            except vol.Invalid:
                errors["base"] = "invalid_input"
                cleaned = user_input

            if not errors:
                ok = await async_validate_token(
                    cleaned[CONF_API_ENDPOINT],
                    cleaned[CONF_API_TOKEN],
                )
                if not ok:
                    _LOGGER.warning(
                        "Soft credential validation failed (options) for %s",
                        cleaned[CONF_API_ENDPOINT],
                    )

                return self.async_create_entry(title="", data=cleaned)

        merged = {**self.config_entry.data, **self.config_entry.options}

        return self.async_show_form(
            step_id="user",
            data_schema=get_schema(
                defaults=merged,
                include_identifier=False,
            ),
            errors=errors,
            description_placeholders={
                "endpoint_id": merged.get(CONF_INSTANCE_KEY, "Instance Key"),
                "display_name": merged.get(CONF_DISPLAY_NAME, "Instance Display Name"),
                "api_help": "URL must end with /jsonrpc.php and token must be 40–80 hex characters.",
            },
        )
