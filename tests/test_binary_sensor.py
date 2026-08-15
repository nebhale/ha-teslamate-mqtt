"""Tests for TeslaMate MQTT binary sensors."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_ICON,
    STATE_OFF,
    STATE_ON,
    STATE_UNKNOWN,
    EntityCategory,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
import pytest

from tests.common import (
    async_fire_teslamate_mqtt_message,
    async_setup_teslamate_mqtt_entry,
)
from tests.typing import MqttMockHAClient


async def test_binary_sensors(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test TeslaMate MQTT binary sensors."""
    await async_setup_teslamate_mqtt_entry(hass)

    assert hass.states.get("binary_sensor.roadrunner_charge_port").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_charging").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_doors").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_door_driver_front").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_door_driver_rear").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_door_passenger_front").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_door_passenger_rear").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_frunk").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_health").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_climate").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_preconditioning").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_occupancy").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_lock").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_plug").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_sentry_mode").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_trunk").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_windows").state == STATE_UNKNOWN
    assert (
        hass.states.get("binary_sensor.roadrunner_tire_soft_front_left").state
        == STATE_UNKNOWN
    )
    assert (
        hass.states.get("binary_sensor.roadrunner_tire_soft_front_right").state
        == STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_tire_soft_rear_left").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_tire_soft_rear_right").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_update") is None

    async_fire_teslamate_mqtt_message(hass, "charge_port_door_open", "true")
    async_fire_teslamate_mqtt_message(hass, "charging_state", "NoPower")
    async_fire_teslamate_mqtt_message(hass, "doors_open", "true")
    async_fire_teslamate_mqtt_message(hass, "driver_front_door_open", "true")
    async_fire_teslamate_mqtt_message(hass, "driver_rear_door_open", "false")
    async_fire_teslamate_mqtt_message(hass, "passenger_front_door_open", "true")
    async_fire_teslamate_mqtt_message(hass, "passenger_rear_door_open", "false")
    async_fire_teslamate_mqtt_message(hass, "frunk_open", "true")
    async_fire_teslamate_mqtt_message(hass, "healthy", "false")
    async_fire_teslamate_mqtt_message(hass, "is_climate_on", "true")
    async_fire_teslamate_mqtt_message(hass, "is_preconditioning", "false")
    async_fire_teslamate_mqtt_message(hass, "is_user_present", "true")
    async_fire_teslamate_mqtt_message(hass, "locked", "true")
    async_fire_teslamate_mqtt_message(hass, "plugged_in", "true")
    async_fire_teslamate_mqtt_message(hass, "sentry_mode", "true")
    async_fire_teslamate_mqtt_message(hass, "trunk_open", "true")
    async_fire_teslamate_mqtt_message(hass, "windows_open", "true")
    async_fire_teslamate_mqtt_message(hass, "tpms_soft_warning_fl", "true")
    async_fire_teslamate_mqtt_message(hass, "tpms_soft_warning_fr", "false")
    async_fire_teslamate_mqtt_message(hass, "tpms_soft_warning_rl", "false")
    async_fire_teslamate_mqtt_message(hass, "tpms_soft_warning_rr", "true")
    await hass.async_block_till_done()

    charge_port_state = hass.states.get("binary_sensor.roadrunner_charge_port")
    assert charge_port_state.state == STATE_ON
    assert (
        charge_port_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.DOOR
    )
    assert charge_port_state.attributes[ATTR_ICON] == "mdi:ev-plug-tesla"

    charging_state = hass.states.get("binary_sensor.roadrunner_charging")
    assert charging_state.state == STATE_OFF
    assert (
        charging_state.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.BATTERY_CHARGING
    )
    assert charging_state.attributes[ATTR_ICON] == "mdi:battery-charging"

    assert hass.states.get("binary_sensor.roadrunner_doors").state == STATE_ON
    assert (
        hass.states.get("binary_sensor.roadrunner_doors").attributes[ATTR_ICON]
        == "mdi:car-door"
    )

    driver_front_door_state = hass.states.get(
        "binary_sensor.roadrunner_door_driver_front"
    )
    assert driver_front_door_state.state == STATE_ON
    assert (
        driver_front_door_state.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.DOOR
    )
    assert driver_front_door_state.attributes[ATTR_ICON] == "mdi:car-door"

    driver_rear_door_state = hass.states.get(
        "binary_sensor.roadrunner_door_driver_rear"
    )
    assert driver_rear_door_state.state == STATE_OFF
    assert (
        driver_rear_door_state.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.DOOR
    )
    assert driver_rear_door_state.attributes[ATTR_ICON] == "mdi:car-door"

    passenger_front_door_state = hass.states.get(
        "binary_sensor.roadrunner_door_passenger_front"
    )
    assert passenger_front_door_state.state == STATE_ON
    assert (
        passenger_front_door_state.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.DOOR
    )
    assert passenger_front_door_state.attributes[ATTR_ICON] == "mdi:car-door"

    passenger_rear_door_state = hass.states.get(
        "binary_sensor.roadrunner_door_passenger_rear"
    )
    assert passenger_rear_door_state.state == STATE_OFF
    assert (
        passenger_rear_door_state.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.DOOR
    )
    assert passenger_rear_door_state.attributes[ATTR_ICON] == "mdi:car-door"

    frunk_state = hass.states.get("binary_sensor.roadrunner_frunk")
    assert frunk_state.state == STATE_ON
    assert frunk_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.DOOR
    assert frunk_state.attributes[ATTR_ICON] == "mdi:car"

    trunk_state = hass.states.get("binary_sensor.roadrunner_trunk")
    assert trunk_state.state == STATE_ON
    assert trunk_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.DOOR
    assert trunk_state.attributes[ATTR_ICON] == "mdi:car"

    windows_state = hass.states.get("binary_sensor.roadrunner_windows")
    assert windows_state.state == STATE_ON
    assert windows_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.WINDOW
    assert windows_state.attributes[ATTR_ICON] == "mdi:car-door"

    health_state = hass.states.get("binary_sensor.roadrunner_health")
    assert health_state.state == STATE_ON
    assert health_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.PROBLEM
    assert health_state.attributes[ATTR_ICON] == "mdi:heart-pulse"

    climate_state = hass.states.get("binary_sensor.roadrunner_climate")
    assert climate_state.state == STATE_ON
    assert (
        climate_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.RUNNING
    )
    assert climate_state.attributes[ATTR_ICON] == "mdi:air-conditioner"

    preconditioning_state = hass.states.get("binary_sensor.roadrunner_preconditioning")
    assert preconditioning_state.state == STATE_OFF
    assert (
        preconditioning_state.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.RUNNING
    )
    assert preconditioning_state.attributes[ATTR_ICON] == "mdi:air-conditioner"

    occupied_state = hass.states.get("binary_sensor.roadrunner_occupancy")
    assert occupied_state.state == STATE_ON
    assert (
        occupied_state.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.OCCUPANCY
    )
    assert occupied_state.attributes[ATTR_ICON] == "mdi:account"

    locked_state = hass.states.get("binary_sensor.roadrunner_lock")
    assert locked_state.state == STATE_OFF
    assert locked_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.LOCK

    plug_state = hass.states.get("binary_sensor.roadrunner_plug")
    assert plug_state.state == STATE_ON
    assert plug_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.PLUG

    sentry_mode = hass.states.get("binary_sensor.roadrunner_sentry_mode")
    assert sentry_mode.state == STATE_ON
    assert sentry_mode.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.RUNNING
    assert sentry_mode.attributes[ATTR_ICON] == "mdi:cctv"

    tire_soft_front_left = hass.states.get(
        "binary_sensor.roadrunner_tire_soft_front_left"
    )
    assert tire_soft_front_left.state == STATE_ON
    assert (
        tire_soft_front_left.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.PROBLEM
    )
    assert tire_soft_front_left.attributes[ATTR_ICON] == "mdi:car-tire-alert"

    tire_soft_front_right = hass.states.get(
        "binary_sensor.roadrunner_tire_soft_front_right"
    )
    assert tire_soft_front_right.state == STATE_OFF
    assert (
        tire_soft_front_right.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.PROBLEM
    )
    assert tire_soft_front_right.attributes[ATTR_ICON] == "mdi:car-tire-alert"

    tire_soft_rear_left = hass.states.get(
        "binary_sensor.roadrunner_tire_soft_rear_left"
    )
    assert tire_soft_rear_left.state == STATE_OFF
    assert (
        tire_soft_rear_left.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.PROBLEM
    )
    assert tire_soft_rear_left.attributes[ATTR_ICON] == "mdi:car-tire-alert"

    tire_soft_rear_right = hass.states.get(
        "binary_sensor.roadrunner_tire_soft_rear_right"
    )
    assert tire_soft_rear_right.state == STATE_ON
    assert (
        tire_soft_rear_right.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.PROBLEM
    )
    assert tire_soft_rear_right.attributes[ATTR_ICON] == "mdi:car-tire-alert"

    assert (
        entity_registry.async_get("binary_sensor.roadrunner_charge_port").unique_id
        == "teslamate/cars/1/charge_port_door_open"
    )
    assert entity_registry.async_get("binary_sensor.roadrunner_charging").unique_id == (
        "teslamate/cars/1/charging_state"
    )
    assert entity_registry.async_get("binary_sensor.roadrunner_doors").unique_id == (
        "teslamate/cars/1/doors_open"
    )
    assert (
        entity_registry.async_get(
            "binary_sensor.roadrunner_door_driver_front"
        ).unique_id
        == "teslamate/cars/1/driver_front_door_open"
    )
    assert (
        entity_registry.async_get("binary_sensor.roadrunner_door_driver_rear").unique_id
        == "teslamate/cars/1/driver_rear_door_open"
    )
    assert (
        entity_registry.async_get(
            "binary_sensor.roadrunner_door_passenger_front"
        ).unique_id
        == "teslamate/cars/1/passenger_front_door_open"
    )
    assert (
        entity_registry.async_get(
            "binary_sensor.roadrunner_door_passenger_rear"
        ).unique_id
        == "teslamate/cars/1/passenger_rear_door_open"
    )
    assert entity_registry.async_get("binary_sensor.roadrunner_frunk").unique_id == (
        "teslamate/cars/1/frunk_open"
    )
    assert entity_registry.async_get("binary_sensor.roadrunner_trunk").unique_id == (
        "teslamate/cars/1/trunk_open"
    )
    assert entity_registry.async_get("binary_sensor.roadrunner_windows").unique_id == (
        "teslamate/cars/1/windows_open"
    )
    assert entity_registry.async_get("binary_sensor.roadrunner_health").unique_id == (
        "teslamate/cars/1/healthy"
    )
    assert (
        entity_registry.async_get("binary_sensor.roadrunner_health").entity_category
        == EntityCategory.DIAGNOSTIC
    )
    assert entity_registry.async_get("binary_sensor.roadrunner_climate").unique_id == (
        "teslamate/cars/1/is_climate_on"
    )
    assert (
        entity_registry.async_get("binary_sensor.roadrunner_preconditioning").unique_id
        == "teslamate/cars/1/is_preconditioning"
    )
    assert entity_registry.async_get(
        "binary_sensor.roadrunner_occupancy"
    ).unique_id == ("teslamate/cars/1/is_user_present")
    assert entity_registry.async_get("binary_sensor.roadrunner_lock").unique_id == (
        "teslamate/cars/1/locked"
    )
    assert entity_registry.async_get("binary_sensor.roadrunner_plug").unique_id == (
        "teslamate/cars/1/plugged_in"
    )
    assert (
        entity_registry.async_get("binary_sensor.roadrunner_sentry_mode").unique_id
        == "teslamate/cars/1/sentry_mode"
    )
    assert (
        entity_registry.async_get(
            "binary_sensor.roadrunner_tire_soft_front_left"
        ).unique_id
        == "teslamate/cars/1/tpms_soft_warning_fl"
    )
    assert (
        entity_registry.async_get(
            "binary_sensor.roadrunner_tire_soft_front_left"
        ).entity_category
        == EntityCategory.DIAGNOSTIC
    )
    assert (
        entity_registry.async_get(
            "binary_sensor.roadrunner_tire_soft_front_right"
        ).unique_id
        == "teslamate/cars/1/tpms_soft_warning_fr"
    )
    assert (
        entity_registry.async_get(
            "binary_sensor.roadrunner_tire_soft_front_right"
        ).entity_category
        == EntityCategory.DIAGNOSTIC
    )
    assert (
        entity_registry.async_get(
            "binary_sensor.roadrunner_tire_soft_rear_left"
        ).unique_id
        == "teslamate/cars/1/tpms_soft_warning_rl"
    )
    assert (
        entity_registry.async_get(
            "binary_sensor.roadrunner_tire_soft_rear_left"
        ).entity_category
        == EntityCategory.DIAGNOSTIC
    )
    assert (
        entity_registry.async_get(
            "binary_sensor.roadrunner_tire_soft_rear_right"
        ).unique_id
        == "teslamate/cars/1/tpms_soft_warning_rr"
    )
    assert (
        entity_registry.async_get(
            "binary_sensor.roadrunner_tire_soft_rear_right"
        ).entity_category
        == EntityCategory.DIAGNOSTIC
    )
    assert entity_registry.async_get("binary_sensor.roadrunner_update") is None

    async_fire_teslamate_mqtt_message(hass, "doors_open", "false")
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.roadrunner_doors").state == STATE_OFF


async def test_new_binary_sensors(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test binary sensors added for new TeslaMate MQTT topics."""
    await async_setup_teslamate_mqtt_entry(hass)

    entity_ids = [
        "binary_sensor.roadrunner_window_driver_front",
        "binary_sensor.roadrunner_window_driver_rear",
        "binary_sensor.roadrunner_window_passenger_front",
        "binary_sensor.roadrunner_window_passenger_rear",
        "binary_sensor.roadrunner_service_mode",
        "binary_sensor.roadrunner_sunroof_installed",
    ]
    for entity_id in entity_ids:
        assert hass.states.get(entity_id).state == STATE_UNKNOWN

    async_fire_teslamate_mqtt_message(hass, "driver_front_window_open", "true")
    async_fire_teslamate_mqtt_message(hass, "driver_rear_window_open", "false")
    async_fire_teslamate_mqtt_message(hass, "passenger_front_window_open", "false")
    async_fire_teslamate_mqtt_message(hass, "passenger_rear_window_open", "true")
    async_fire_teslamate_mqtt_message(hass, "service_mode", "true")
    async_fire_teslamate_mqtt_message(hass, "sun_roof_installed", "true")
    await hass.async_block_till_done()

    window_entities = {
        "binary_sensor.roadrunner_window_driver_front": (
            STATE_ON,
            "driver_front_window_open",
        ),
        "binary_sensor.roadrunner_window_driver_rear": (
            STATE_OFF,
            "driver_rear_window_open",
        ),
        "binary_sensor.roadrunner_window_passenger_front": (
            STATE_OFF,
            "passenger_front_window_open",
        ),
        "binary_sensor.roadrunner_window_passenger_rear": (
            STATE_ON,
            "passenger_rear_window_open",
        ),
    }
    for entity_id, (state, topic) in window_entities.items():
        window_state = hass.states.get(entity_id)
        assert window_state.state == state
        assert (
            window_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.WINDOW
        )
        assert window_state.attributes[ATTR_ICON] == "mdi:car-door"
        assert entity_registry.async_get(entity_id).unique_id == (
            f"teslamate/cars/1/{topic}"
        )

    service_mode = hass.states.get("binary_sensor.roadrunner_service_mode")
    assert service_mode.state == STATE_ON
    assert ATTR_DEVICE_CLASS not in service_mode.attributes
    assert service_mode.attributes[ATTR_ICON] == "mdi:wrench"
    assert entity_registry.async_get(
        "binary_sensor.roadrunner_service_mode"
    ).unique_id == ("teslamate/cars/1/service_mode")

    sunroof_installed = hass.states.get("binary_sensor.roadrunner_sunroof_installed")
    assert sunroof_installed.state == STATE_ON
    assert ATTR_DEVICE_CLASS not in sunroof_installed.attributes
    assert sunroof_installed.attributes[ATTR_ICON] == "mdi:car-convertible"
    sunroof_registry_entry = entity_registry.async_get(
        "binary_sensor.roadrunner_sunroof_installed"
    )
    assert sunroof_registry_entry.unique_id == "teslamate/cars/1/sun_roof_installed"
    assert sunroof_registry_entry.entity_category == EntityCategory.DIAGNOSTIC


@pytest.mark.parametrize(
    ("payload", "state"),
    [
        pytest.param("Charging", STATE_ON, id="charging"),
        pytest.param("NoPower", STATE_OFF, id="not_charging"),
        pytest.param("charging", STATE_OFF, id="case_sensitive"),
    ],
)
async def test_charging_values(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient, payload: str, state: str
) -> None:
    """Test charging binary sensor value mapping."""
    await async_setup_teslamate_mqtt_entry(hass)

    async_fire_teslamate_mqtt_message(hass, "charging_state", payload)
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.roadrunner_charging").state == state


@pytest.mark.parametrize(
    ("payload", "state"),
    [
        pytest.param("true", STATE_OFF, id="healthy"),
        pytest.param("false", STATE_ON, id="problem"),
    ],
)
async def test_health_values(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient, payload: str, state: str
) -> None:
    """Test health value mapping."""
    await async_setup_teslamate_mqtt_entry(hass)

    async_fire_teslamate_mqtt_message(hass, "healthy", payload)
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.roadrunner_health").state == state


@pytest.mark.parametrize(
    ("payload", "state"),
    [
        pytest.param("true", STATE_OFF, id="locked"),
        pytest.param("false", STATE_ON, id="unlocked"),
    ],
)
async def test_locked_values(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient, payload: str, state: str
) -> None:
    """Test locked value mapping."""
    await async_setup_teslamate_mqtt_entry(hass)

    async_fire_teslamate_mqtt_message(hass, "locked", payload)
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.roadrunner_lock").state == state
