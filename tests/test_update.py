"""Tests for TeslaMate MQTT update entities."""

from homeassistant.components.update import UpdateDeviceClass
from homeassistant.components.update.const import (
    ATTR_INSTALLED_VERSION,
    ATTR_LATEST_VERSION,
)
from homeassistant.const import ATTR_DEVICE_CLASS, STATE_ON, STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from tests.common import (
    async_fire_teslamate_mqtt_message,
    async_setup_teslamate_mqtt_entry,
)
from tests.typing import MqttMockHAClient


async def test_update(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test TeslaMate MQTT update entity."""
    await async_setup_teslamate_mqtt_entry(hass)

    assert hass.states.get("update.roadrunner_update").state == STATE_UNKNOWN

    async_fire_teslamate_mqtt_message(hass, "update_available", "true")
    async_fire_teslamate_mqtt_message(hass, "update_version", "2026.20.1")
    async_fire_teslamate_mqtt_message(hass, "version", "2026.14.1")
    await hass.async_block_till_done()

    update_state = hass.states.get("update.roadrunner_update")
    assert update_state.state == STATE_ON
    assert update_state.attributes[ATTR_DEVICE_CLASS] == UpdateDeviceClass.FIRMWARE
    assert update_state.attributes[ATTR_INSTALLED_VERSION] == "2026.14.1"
    assert update_state.attributes[ATTR_LATEST_VERSION] == "2026.20.1"

    assert entity_registry.async_get("update.roadrunner_update").unique_id == (
        "teslamate/cars/1/update_available"
    )
