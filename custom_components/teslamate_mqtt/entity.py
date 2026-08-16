"""Base entity for TeslaMate MQTT."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from . import TeslaMateMqttData
from .const import TOPIC_ACTIVE_ROUTE


class TeslaMateMqttEntity(Entity):
    """Base class for TeslaMate MQTT entities."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, data: TeslaMateMqttData, key: str) -> None:
        """Initialize the entity."""
        self.data = data
        self.key = key
        self._attr_unique_id = f"{data.topic_root}/{key}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return self.data.device_info

    async def async_added_to_hass(self) -> None:
        """Call when entity is added."""
        await super().async_added_to_hass()
        self.async_on_remove(self.data.async_add_listener(self.async_write_ha_state))


class TeslaMateActiveRouteEntity(TeslaMateMqttEntity):
    """Base entity derived from the TeslaMate active route JSON topic."""

    @property
    def _active_route(self) -> dict[str, object] | None:
        """Return the active route when one is available."""
        if (route := self.data.json_value(TOPIC_ACTIVE_ROUTE)) is None:
            return None
        if route.get("error"):
            return None
        return route

    @property
    def available(self) -> bool:
        """Return whether an active route is available."""
        return self._active_route is not None

    def active_route_value(self, key: str) -> object | None:
        """Return a value from the active route."""
        if (route := self._active_route) is None:
            return None
        return route.get(key)
