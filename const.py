# const.py
import re
import voluptuous as vol
from homeassistant.helpers import config_validation as cv

DOMAIN = "hakboard"
CONF_API_ENDPOINT = "api_endpoint"
CONF_API_TOKEN = "api_token"

CONF_INSTANCE_KEY = "instance_key"
CONF_DISPLAY_NAME = "display_name"

CONF_PROJECT_FILTER = "project_filter"
CONF_POLL_INTERVAL = "poll_interval"
CONF_POLL_INTERVAL_SECONDS = "poll_interval_seconds"

SERVICE_SYNC_NOW = "sync_now"

# --- SYSTEM/API CONSTANTS ---
MIN_API_TOKEN_LENGTH = 40
MAX_INSTANCE_KEY_LENGTH = 20
MAX_TEXT_LENGTH = 500  # For URL/Token

# --- DEFAULT VALUES ---
DEFAULT_API_TOKEN = ""
DEFAULT_API_ENDPOINT = ""
DEFAULT_INSTANCE_KEY = "hl"
DEFAULT_DISPLAY_NAME = "Homelab"
DEFAULT_PROJECT_FILTER = "1-10"
DEFAULT_POLL_INTERVAL = 300
MINIMUM_POLL_INTERVAL = 5

# --- VALIDATION PATTERNS ---
INSTANCE_KEY_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")
API_TOKEN_PATTERN = re.compile(r"^[A-Fa-f0-9]{40,80}$")
