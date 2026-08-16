"""Tests for TeslaMate MQTT device trackers."""

import json

from homeassistant.const import (
    ATTR_GPS_ACCURACY,
    ATTR_ICON,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    STATE_UNAVAILABLE,
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


async def test_active_route_location_tracker(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test the device tracker derived from the active route JSON topic."""
    await async_setup_teslamate_mqtt_entry(hass)

    entity_id = "device_tracker.roadrunner_active_route_location"
    assert hass.states.get(entity_id).state == STATE_UNAVAILABLE

    async_fire_teslamate_mqtt_message(
        hass,
        "active_route",
        json.dumps(
            {
                "destination": "Home",
                "location": {"latitude": 35.278131, "longitude": 29.744801},
                "error": None,
            }
        ),
    )
    await hass.async_block_till_done()

    tracker_state = hass.states.get(entity_id)
    assert tracker_state.state == "not_home"
    assert tracker_state.attributes[ATTR_LATITUDE] == 35.278131
    assert tracker_state.attributes[ATTR_LONGITUDE] == 29.744801
    assert tracker_state.attributes[ATTR_GPS_ACCURACY] == 0
    assert tracker_state.attributes[ATTR_ICON] == "mdi:crosshairs-gps"

    tracker_entry = entity_registry.async_get(entity_id)
    assert tracker_entry.unique_id == "teslamate/cars/1/active_route_location"
    assert tracker_entry.entity_category is None

    async_fire_teslamate_mqtt_message(
        hass,
        "active_route",
        json.dumps({"error": "No active route available"}),
    )
    await hass.async_block_till_done()

    assert hass.states.get(entity_id).state == STATE_UNAVAILABLE
