"""Constants for the HAKboard integration."""
import re

DOMAIN = "hakboard"

# --- API CONFIGURATION ---
CONF_API_ENDPOINT = "api_endpoint"
CONF_API_TOKEN = "api_token"
CONF_VERIFY_SSL = "verify_ssl"

# --- INSTANCE CONFIGURATION ---
CONF_INSTANCE_KEY = "instance_key"
CONF_INSTANCE_NAME = "instance_name"
# Backward compatibility - keep old constant for migration
CONF_DISPLAY_NAME = "display_name"  # Deprecated, use CONF_INSTANCE_NAME

# --- FILTERING & POLLING ---
CONF_PROJECT_FILTER = "project_filter"
CONF_POLL_INTERVAL = "poll_interval"
CONF_POLL_INTERVAL_SECONDS = "poll_interval_seconds"

# --- VALIDATION CONSTANTS ---
MIN_API_TOKEN_LENGTH = 40
MAX_INSTANCE_KEY_LENGTH = 20
MAX_TEXT_LENGTH = 500  # For URL/Token

# --- DEFAULT VALUES ---
DEFAULT_API_TOKEN = ""
DEFAULT_API_ENDPOINT = ""
DEFAULT_INSTANCE_KEY = "hl"
DEFAULT_INSTANCE_NAME = "Homelab"
DEFAULT_PROJECT_FILTER = "1-10"
DEFAULT_POLL_INTERVAL = 300
DEFAULT_VERIFY_SSL = True
MINIMUM_POLL_INTERVAL = 5

# --- VALIDATION PATTERNS ---
INSTANCE_KEY_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")
API_TOKEN_PATTERN = re.compile(r"^[A-Fa-f0-9]{40,80}$")
