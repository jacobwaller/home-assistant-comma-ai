"""Number entities for comma.ai."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.const import UnitOfTime

from .const import (
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
    MAX_UPDATE_INTERVAL,
    MIN_UPDATE_INTERVAL,
)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from . import CommaConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: CommaConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up comma.ai number entities."""
    async_add_entities([CommaUpdateIntervalNumber(config_entry)])


class CommaUpdateIntervalNumber(NumberEntity):
    """Slider entity that controls polling update interval."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_translation_key = "update_interval"
    _attr_mode = NumberMode.SLIDER
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_native_min_value = MIN_UPDATE_INTERVAL
    _attr_native_max_value = MAX_UPDATE_INTERVAL
    _attr_native_step = 1

    def __init__(self, config_entry: CommaConfigEntry) -> None:
        """Initialize the update interval number."""
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_update_interval"

    @property
    def native_value(self) -> float:
        """Return the configured update interval."""
        value = self._config_entry.options.get(
            CONF_UPDATE_INTERVAL,
            self._config_entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
        )
        try:
            interval = int(value)
        except (TypeError, ValueError):
            interval = DEFAULT_UPDATE_INTERVAL
        return float(max(MIN_UPDATE_INTERVAL, min(interval, MAX_UPDATE_INTERVAL)))

    async def async_set_native_value(self, value: float) -> None:
        """Update polling interval option from slider."""
        interval = max(MIN_UPDATE_INTERVAL, min(int(value), MAX_UPDATE_INTERVAL))
        updated_options = dict(self._config_entry.options)
        updated_options[CONF_UPDATE_INTERVAL] = interval
        self.hass.config_entries.async_update_entry(self._config_entry, options=updated_options)
        self.async_write_ha_state()
