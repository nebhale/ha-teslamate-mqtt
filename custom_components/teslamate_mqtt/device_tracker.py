"""Device tracker platform for TeslaMate MQTT."""

from typing import cast

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TeslaMateMqttConfigEntry, TeslaMateMqttData
from .const import TOPIC_ACTIVE_ROUTE_LOCATION, TOPIC_LATITUDE, TOPIC_LONGITUDE
from .entity import TeslaMateActiveRouteEntity, TeslaMateMqttEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TeslaMateMqttConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up TeslaMate MQTT device tracker."""
    async_add_entities(
        [
            TeslaMateDeviceTracker(entry.runtime_data),
            TeslaMateActiveRouteLocationTracker(entry.runtime_data),
        ]
    )


class TeslaMateDeviceTracker(TeslaMateMqttEntity, TrackerEntity):
    """Representation of the Tesla location."""

    _attr_entity_category = cast(EntityCategory, None)
    _attr_icon = "mdi:crosshairs-gps"
    _attr_name = None

    def __init__(self, data: TeslaMateMqttData) -> None:
        """Initialize the device tracker."""
        super().__init__(data, "location")

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        if (value := self.data.value(TOPIC_LATITUDE)) is None:
            return None
        try:
            return float(value)
        except ValueError:
            return None

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        if (value := self.data.value(TOPIC_LONGITUDE)) is None:
            return None
        try:
            return float(value)
        except ValueError:
            return None

    @property
    def source_type(self) -> SourceType:
        """Return the source type."""
        return SourceType.GPS


class TeslaMateActiveRouteLocationTracker(TeslaMateActiveRouteEntity, TrackerEntity):
    """Representation of the active route destination location."""

    _attr_entity_category = cast(EntityCategory, None)
    _attr_icon = "mdi:crosshairs-gps"
    _attr_name = "Active Route Location"

    def __init__(self, data: TeslaMateMqttData) -> None:
        """Initialize the device tracker."""
        super().__init__(data, TOPIC_ACTIVE_ROUTE_LOCATION)

    def _coordinate(self, key: str) -> float | None:
        """Return a coordinate from the active route location."""
        location = self.active_route_value("location")
        if not isinstance(location, dict):
            return None
        value = location.get(key)
        if isinstance(value, bool) or not isinstance(value, (float, int)):
            return None
        return float(value)

    @property
    def latitude(self) -> float | None:
        """Return the active route destination latitude."""
        return self._coordinate("latitude")

    @property
    def longitude(self) -> float | None:
        """Return the active route destination longitude."""
        return self._coordinate("longitude")

    @property
    def source_type(self) -> SourceType:
        """Return the source type."""
        return SourceType.GPS
