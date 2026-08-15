"""Tests for TeslaMate MQTT integration setup."""

import asyncio
from unittest.mock import patch

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.teslamate_mqtt.const import CONF_TOPIC_ROOT, DOMAIN
from tests.common import (
    async_fire_teslamate_mqtt_message,
    async_on_subscribe_done,
    async_setup_teslamate_mqtt_entry,
)
from tests.typing import MqttMockHAClient


async def test_display_name_updates_entry_and_device(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test display name updates the config entry and device."""
    entry = await async_setup_teslamate_mqtt_entry(hass)

    assert entry.title == "Roadrunner"

    async_fire_teslamate_mqtt_message(hass, "display_name", "Bluebird")
    await hass.async_block_till_done()

    assert entry.title == "Bluebird"
    assert (
        device_registry.async_get_device(
            identifiers={(DOMAIN, "teslamate/cars/1")}
        ).name
        == "Bluebird"
    )


async def test_device_info(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test TeslaMate MQTT device info."""
    await async_setup_teslamate_mqtt_entry(hass)

    async_fire_teslamate_mqtt_message(hass, "version", "2026.14.1")
    async_fire_teslamate_mqtt_message(hass, "model", "3")
    async_fire_teslamate_mqtt_message(hass, "trim_badging", "Performance")
    async_fire_teslamate_mqtt_message(hass, "wheel_type", "SonicCarbonTwinTurbine19")
    async_fire_teslamate_mqtt_message(hass, "spoiler_type", "CarbonFiber")
    async_fire_teslamate_mqtt_message(hass, "sun_roof_installed", "true")
    await hass.async_block_till_done()

    device = device_registry.async_get_device(
        identifiers={(DOMAIN, "teslamate/cars/1")}
    )
    assert device is not None
    assert device.manufacturer == "Tesla"
    assert device.name == "Roadrunner"
    assert device.model == (
        'Model 3 Performance (Sonic Carbon Twin Turbine 19" Wheels, '
        "Carbon Fiber Spoiler, Sunroof)"
    )
    assert device.sw_version == "2026.14.1"


@pytest.mark.parametrize(
    ("wheel_type", "spoiler_type", "sun_roof_installed", "model"),
    [
        pytest.param(
            "SonicCarbonTwinTurbine19",
            "CarbonFiber",
            "true",
            'Model 3 Performance (Sonic Carbon Twin Turbine 19" Wheels, '
            "Carbon Fiber Spoiler, Sunroof)",
            id="wheel_spoiler_and_sunroof",
        ),
        pytest.param(
            "Slipstream",
            "none",
            "false",
            "Model 3 Performance (Slipstream Wheels)",
            id="wheel_without_spoiler_or_sunroof",
        ),
    ],
)
async def test_model_name_details(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    device_registry: dr.DeviceRegistry,
    wheel_type: str,
    spoiler_type: str,
    sun_roof_installed: str,
    model: str,
) -> None:
    """Test device model detail formatting."""
    await async_setup_teslamate_mqtt_entry(hass)

    async_fire_teslamate_mqtt_message(hass, "model", "3")
    async_fire_teslamate_mqtt_message(hass, "trim_badging", "Performance")
    async_fire_teslamate_mqtt_message(hass, "wheel_type", wheel_type)
    async_fire_teslamate_mqtt_message(hass, "spoiler_type", spoiler_type)
    async_fire_teslamate_mqtt_message(hass, "sun_roof_installed", sun_roof_installed)
    await hass.async_block_till_done()

    device = device_registry.async_get_device(
        identifiers={(DOMAIN, "teslamate/cars/1")}
    )
    assert device is not None
    assert device.model == model


async def test_setup_fails_without_display_name(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient
) -> None:
    """Test setup is retried when the display name topic is not retained."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Roadrunner",
        data={CONF_TOPIC_ROOT: "teslamate/cars/1"},
        unique_id="teslamate/cars/1",
    )
    entry.add_to_hass(hass)

    with patch("custom_components.teslamate_mqtt.DISPLAY_NAME_TIMEOUT", 0):
        with patch(
            "custom_components.teslamate_mqtt.mqtt.async_on_subscribe_done",
            side_effect=async_on_subscribe_done,
        ):
            setup_task = hass.async_create_task(
                hass.config_entries.async_setup(entry.entry_id)
            )
            await asyncio.sleep(0)
        assert not await setup_task


async def test_setup_retries_when_mqtt_disconnected(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient
) -> None:
    """Test setup is retried when the MQTT client is not connected."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Roadrunner",
        data={CONF_TOPIC_ROOT: "teslamate/cars/1"},
        unique_id="teslamate/cars/1",
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.teslamate_mqtt.mqtt.is_connected",
        return_value=False,
    ):
        assert not await hass.config_entries.async_setup(entry.entry_id)
