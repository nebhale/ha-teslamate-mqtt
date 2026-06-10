"""Tests for TeslaMate MQTT device trackers."""

from homeassistant.const import (
    ATTR_GPS_ACCURACY,
    ATTR_ICON,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    STATE_UNKNOWN,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from tests.common import (
    async_fire_teslamate_mqtt_message,
    async_setup_teslamate_mqtt_entry,
)
from tests.typing import MqttMockHAClient


async def test_device_tracker(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test TeslaMate MQTT device tracker."""
    await async_setup_teslamate_mqtt_entry(hass)

    assert hass.states.get("device_tracker.roadrunner").state == STATE_UNKNOWN

    async_fire_teslamate_mqtt_message(hass, "latitude", "37.123")
    async_fire_teslamate_mqtt_message(hass, "longitude", "-122.456")
    await hass.async_block_till_done()

    tracker_state = hass.states.get("device_tracker.roadrunner")
    assert tracker_state.state == "not_home"
    assert tracker_state.attributes[ATTR_LATITUDE] == 37.123
    assert tracker_state.attributes[ATTR_LONGITUDE] == -122.456
    assert tracker_state.attributes[ATTR_GPS_ACCURACY] == 0
    assert tracker_state.attributes[ATTR_ICON] == "mdi:crosshairs-gps"

    tracker_entry = entity_registry.async_get("device_tracker.roadrunner")
    assert tracker_entry.unique_id == "teslamate/cars/1/location"
    assert tracker_entry.entity_category is None
