"""Constants for the comma.ai integration."""

from __future__ import annotations

from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "comma_ai"
PLATFORMS = [Platform.SENSOR, Platform.DEVICE_TRACKER, Platform.NUMBER]

CONF_JWT_TOKEN: Final = "jwt_token"
CONF_IGNORE_NON_OWNED: Final = "ignore_non_owned"
CONF_UPDATE_INTERVAL: Final = "update_interval"

API_BASE_URL: Final = "https://api.commadotai.com"

# Update interval in seconds
MIN_UPDATE_INTERVAL: Final = 5
MAX_UPDATE_INTERVAL: Final = 600
DEFAULT_UPDATE_INTERVAL: Final = 60

