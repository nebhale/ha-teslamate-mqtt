"""Tests for TeslaMate MQTT sensors."""

import json
import logging

from homeassistant.components.sensor import (
    ATTR_STATE_CLASS,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_ICON,
    ATTR_UNIT_OF_MEASUREMENT,
    DEGREE,
    PERCENTAGE,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfLength,
    UnitOfPower,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.util.unit_system import METRIC_SYSTEM, US_CUSTOMARY_SYSTEM
import pytest

from tests.common import (
    async_fire_teslamate_mqtt_message,
    async_setup_teslamate_mqtt_entry,
)
from tests.typing import MqttMockHAClient

DISABLED_SENSOR_ENTITIES = {
    "sensor.roadrunner_display_name": ("display_name", EntityCategory.DIAGNOSTIC),
    "sensor.roadrunner_latitude": ("latitude", None),
    "sensor.roadrunner_location": ("location", None),
    "sensor.roadrunner_longitude": ("longitude", None),
    "sensor.roadrunner_model": ("model", EntityCategory.DIAGNOSTIC),
    "sensor.roadrunner_spoiler_type": (
        "spoiler_type",
        EntityCategory.DIAGNOSTIC,
    ),
    "sensor.roadrunner_sunroof_installed": (
        "sun_roof_installed",
        EntityCategory.DIAGNOSTIC,
    ),
    "sensor.roadrunner_trim_badging": (
        "trim_badging",
        EntityCategory.DIAGNOSTIC,
    ),
    "sensor.roadrunner_update_available": (
        "update_available",
        EntityCategory.DIAGNOSTIC,
    ),
    "sensor.roadrunner_update_version": (
        "update_version",
        EntityCategory.DIAGNOSTIC,
    ),
    "sensor.roadrunner_version": ("version", EntityCategory.DIAGNOSTIC),
    "sensor.roadrunner_wheel_type": ("wheel_type", EntityCategory.DIAGNOSTIC),
}

ACTIVE_ROUTE_SENSOR_ENTITIES = {
    "sensor.roadrunner_active_route_destination": "active_route_destination",
    "sensor.roadrunner_active_route_energy_at_arrival": (
        "active_route_energy_at_arrival"
    ),
    "sensor.roadrunner_active_route_distance_to_arrival": (
        "active_route_distance_to_arrival"
    ),
    "sensor.roadrunner_active_route_minutes_to_arrival": (
        "active_route_minutes_to_arrival"
    ),
    "sensor.roadrunner_active_route_traffic_minutes_delay": (
        "active_route_traffic_minutes_delay"
    ),
}


async def test_sensors(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test TeslaMate MQTT sensors."""
    await async_setup_teslamate_mqtt_entry(hass)

    assert hass.states.get("sensor.roadrunner_battery").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_center_display").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_energy_added").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_charge_limit").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_charge_current_request").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("sensor.roadrunner_charge_current_request_max").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("sensor.roadrunner_charger_current").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_charger_phases").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_charger_power").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_charger_voltage").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_charging_state").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_climate_keeper").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_display_name") is None
    assert hass.states.get("sensor.roadrunner_elevation").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_exterior_color").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_geofence").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_heading").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_temperature_inside").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("sensor.roadrunner_temperature_outside").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("sensor.roadrunner_odometer").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_power").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_range_estimated").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_range_ideal").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_range_rated").state == STATE_UNKNOWN
    assert (
        hass.states.get("sensor.roadrunner_charging_start_time").state == STATE_UNKNOWN
    )
    assert hass.states.get("sensor.roadrunner_shift_state").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_last_seen").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_speed").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_spoiler_type") is None
    assert hass.states.get("sensor.roadrunner_state").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_charging_time_left").state == (
        STATE_UNKNOWN
    )
    assert (
        hass.states.get("sensor.roadrunner_tire_pressure_front_left").state
        == STATE_UNKNOWN
    )
    assert (
        hass.states.get("sensor.roadrunner_tire_pressure_front_right").state
        == STATE_UNKNOWN
    )
    assert hass.states.get("sensor.roadrunner_tire_pressure_rear_left").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("sensor.roadrunner_tire_pressure_rear_right").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("sensor.roadrunner_update_version") is None
    assert hass.states.get("sensor.roadrunner_usable_battery").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_version") is None
    assert hass.states.get("sensor.roadrunner_wheel_type") is None

    async_fire_teslamate_mqtt_message(hass, "battery_level", "74")
    async_fire_teslamate_mqtt_message(hass, "center_display_state", "8")
    async_fire_teslamate_mqtt_message(hass, "charge_energy_added", "12.3")
    async_fire_teslamate_mqtt_message(hass, "charge_limit_soc", "80")
    async_fire_teslamate_mqtt_message(hass, "charge_current_request", "24")
    async_fire_teslamate_mqtt_message(hass, "charge_current_request_max", "48")
    async_fire_teslamate_mqtt_message(hass, "charger_actual_current", "40")
    async_fire_teslamate_mqtt_message(hass, "charger_phases", "3")
    async_fire_teslamate_mqtt_message(hass, "charger_power", "11")
    async_fire_teslamate_mqtt_message(hass, "charger_voltage", "240")
    async_fire_teslamate_mqtt_message(hass, "charging_state", "NoPower")
    async_fire_teslamate_mqtt_message(hass, "climate_keeper_mode", "dog")
    async_fire_teslamate_mqtt_message(hass, "elevation", "123")
    async_fire_teslamate_mqtt_message(hass, "exterior_color", "DeepBlue")
    async_fire_teslamate_mqtt_message(hass, "geofence", "Home")
    async_fire_teslamate_mqtt_message(hass, "heading", "270")
    async_fire_teslamate_mqtt_message(hass, "inside_temp", "22.4")
    async_fire_teslamate_mqtt_message(hass, "outside_temp", "18.7")
    async_fire_teslamate_mqtt_message(hass, "odometer", "12345.6")
    async_fire_teslamate_mqtt_message(hass, "power", "-7")
    async_fire_teslamate_mqtt_message(hass, "est_battery_range_km", "321.5")
    async_fire_teslamate_mqtt_message(hass, "ideal_battery_range_km", "330.1")
    async_fire_teslamate_mqtt_message(hass, "rated_battery_range_km", "325.7")
    async_fire_teslamate_mqtt_message(
        hass, "scheduled_charging_start_time", "2026-06-07T12:34:56+00:00"
    )
    async_fire_teslamate_mqtt_message(hass, "shift_state", "D")
    async_fire_teslamate_mqtt_message(hass, "since", "2026-06-07T12:00:00+00:00")
    async_fire_teslamate_mqtt_message(hass, "speed", "88")
    async_fire_teslamate_mqtt_message(hass, "spoiler_type", "CarbonFiber")
    async_fire_teslamate_mqtt_message(hass, "state", "suspended")
    async_fire_teslamate_mqtt_message(hass, "time_to_full_charge", "1.75")
    async_fire_teslamate_mqtt_message(hass, "tpms_pressure_fl", "2.9")
    async_fire_teslamate_mqtt_message(hass, "tpms_pressure_fr", "2.8")
    async_fire_teslamate_mqtt_message(hass, "tpms_pressure_rl", "2.7")
    async_fire_teslamate_mqtt_message(hass, "tpms_pressure_rr", "2.6")
    async_fire_teslamate_mqtt_message(hass, "update_version", "2026.20.1")
    async_fire_teslamate_mqtt_message(hass, "usable_battery_level", "71")
    async_fire_teslamate_mqtt_message(hass, "version", "2026.14.1")
    async_fire_teslamate_mqtt_message(hass, "wheel_type", "SonicCarbonTwinTurbine19")
    await hass.async_block_till_done()

    battery_state = hass.states.get("sensor.roadrunner_battery")
    assert battery_state.state == "74"
    assert battery_state.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.BATTERY
    assert battery_state.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert battery_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == PERCENTAGE

    usable_battery_state = hass.states.get("sensor.roadrunner_usable_battery")
    assert usable_battery_state.state == "71"
    assert (
        usable_battery_state.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.BATTERY
    )
    assert (
        usable_battery_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert usable_battery_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == PERCENTAGE

    center_display_state = hass.states.get("sensor.roadrunner_center_display")
    assert center_display_state.state == "dog_mode"
    assert center_display_state.attributes[ATTR_ICON] == "mdi:television"
    assert center_display_state.attributes["raw_value"] == "8"

    charge_energy_added_state = hass.states.get("sensor.roadrunner_energy_added")
    assert charge_energy_added_state.state == "12.3"
    assert (
        charge_energy_added_state.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.ENERGY
    )
    assert (
        charge_energy_added_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.TOTAL_INCREASING
    )
    assert (
        charge_energy_added_state.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfEnergy.KILO_WATT_HOUR
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_energy_added").options["sensor"][
            "suggested_display_precision"
        ]
        == 1
    )

    charge_limit_soc_state = hass.states.get("sensor.roadrunner_charge_limit")
    assert charge_limit_soc_state.state == "80"
    assert charge_limit_soc_state.attributes[ATTR_ICON] == "mdi:battery-charging-90"
    assert (
        charge_limit_soc_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert charge_limit_soc_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == PERCENTAGE
    assert (
        entity_registry.async_get("sensor.roadrunner_charge_limit").options["sensor"][
            "suggested_display_precision"
        ]
        == 0
    )

    charge_current_request_state = hass.states.get(
        "sensor.roadrunner_charge_current_request"
    )
    assert charge_current_request_state.state == "24"
    assert (
        charge_current_request_state.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.CURRENT
    )
    assert (
        charge_current_request_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert (
        charge_current_request_state.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfElectricCurrent.AMPERE
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_charge_current_request").options[
            "sensor"
        ]["suggested_display_precision"]
        == 0
    )

    charge_current_request_max_state = hass.states.get(
        "sensor.roadrunner_charge_current_request_max"
    )
    assert charge_current_request_max_state.state == "48"
    assert (
        charge_current_request_max_state.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.CURRENT
    )
    assert (
        charge_current_request_max_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert (
        charge_current_request_max_state.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfElectricCurrent.AMPERE
    )
    assert (
        entity_registry.async_get(
            "sensor.roadrunner_charge_current_request_max"
        ).options["sensor"]["suggested_display_precision"]
        == 0
    )

    charger_actual_current_state = hass.states.get("sensor.roadrunner_charger_current")
    assert charger_actual_current_state.state == "40"
    assert (
        charger_actual_current_state.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.CURRENT
    )
    assert (
        charger_actual_current_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert (
        charger_actual_current_state.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfElectricCurrent.AMPERE
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_charger_current").options[
            "sensor"
        ]["suggested_display_precision"]
        == 0
    )

    charger_phases_state = hass.states.get("sensor.roadrunner_charger_phases")
    assert charger_phases_state.state == "3"
    assert charger_phases_state.attributes[ATTR_ICON] == "mdi:sine-wave"
    assert (
        charger_phases_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert charger_phases_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == "phases"
    assert (
        entity_registry.async_get("sensor.roadrunner_charger_phases").options["sensor"][
            "suggested_display_precision"
        ]
        == 0
    )

    charger_power_state = hass.states.get("sensor.roadrunner_charger_power")
    assert charger_power_state.state == "11"
    assert charger_power_state.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.POWER
    assert (
        charger_power_state.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    )
    assert (
        charger_power_state.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfPower.KILO_WATT
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_charger_power").options["sensor"][
            "suggested_display_precision"
        ]
        == 0
    )

    charger_voltage_state = hass.states.get("sensor.roadrunner_charger_voltage")
    assert charger_voltage_state.state == "240"
    assert (
        charger_voltage_state.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.VOLTAGE
    )
    assert (
        charger_voltage_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert (
        charger_voltage_state.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfElectricPotential.VOLT
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_charger_voltage").options[
            "sensor"
        ]["suggested_display_precision"]
        == 0
    )

    charging_state = hass.states.get("sensor.roadrunner_charging_state")
    assert charging_state.state == "No Power"
    assert charging_state.attributes[ATTR_ICON] == "mdi:ev-station"

    climate_keeper = hass.states.get("sensor.roadrunner_climate_keeper")
    assert climate_keeper.state == "Dog"
    assert climate_keeper.attributes[ATTR_ICON] == "mdi:air-conditioner"

    elevation = hass.states.get("sensor.roadrunner_elevation")
    assert elevation.state == "123.0"
    assert elevation.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.DISTANCE
    assert elevation.attributes[ATTR_ICON] == "mdi:image-filter-hdr"
    assert elevation.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert elevation.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfLength.METERS
    assert (
        entity_registry.async_get("sensor.roadrunner_elevation").options["sensor"][
            "suggested_display_precision"
        ]
        == 0
    )

    exterior_color = hass.states.get("sensor.roadrunner_exterior_color")
    assert exterior_color.state == "Deep Blue"
    assert exterior_color.attributes[ATTR_ICON] == "mdi:format-color-fill"

    geofence = hass.states.get("sensor.roadrunner_geofence")
    assert geofence.state == "Home"
    assert geofence.attributes[ATTR_ICON] == "mdi:earth"

    heading = hass.states.get("sensor.roadrunner_heading")
    assert heading.state == "270"
    assert heading.attributes[ATTR_ICON] == "mdi:compass"
    assert heading.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert heading.attributes[ATTR_UNIT_OF_MEASUREMENT] == DEGREE
    assert (
        entity_registry.async_get("sensor.roadrunner_heading").options["sensor"][
            "suggested_display_precision"
        ]
        == 0
    )

    inside_temp = hass.states.get("sensor.roadrunner_temperature_inside")
    assert inside_temp.state == "22.4"
    assert inside_temp.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.TEMPERATURE
    assert inside_temp.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert inside_temp.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfTemperature.CELSIUS
    assert (
        entity_registry.async_get("sensor.roadrunner_temperature_inside").options[
            "sensor"
        ]["suggested_display_precision"]
        == 1
    )

    outside_temp = hass.states.get("sensor.roadrunner_temperature_outside")
    assert outside_temp.state == "18.7"
    assert outside_temp.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.TEMPERATURE
    assert outside_temp.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert (
        outside_temp.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfTemperature.CELSIUS
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_temperature_outside").options[
            "sensor"
        ]["suggested_display_precision"]
        == 1
    )

    odometer = hass.states.get("sensor.roadrunner_odometer")
    assert odometer.state == "12345.6"
    assert odometer.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.DISTANCE
    assert odometer.attributes[ATTR_ICON] == "mdi:counter"
    assert odometer.attributes[ATTR_STATE_CLASS] == SensorStateClass.TOTAL_INCREASING
    assert odometer.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfLength.KILOMETERS
    assert (
        entity_registry.async_get("sensor.roadrunner_odometer").options["sensor"][
            "suggested_display_precision"
        ]
        == 0
    )

    power = hass.states.get("sensor.roadrunner_power")
    assert power.state == "-7"
    assert power.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.POWER
    assert power.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert power.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfPower.KILO_WATT
    assert (
        entity_registry.async_get("sensor.roadrunner_power").options["sensor"][
            "suggested_display_precision"
        ]
        == 0
    )

    estimated_range = hass.states.get("sensor.roadrunner_range_estimated")
    assert estimated_range.state == "321.5"
    assert estimated_range.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.DISTANCE
    assert estimated_range.attributes[ATTR_ICON] == "mdi:map-marker-distance"
    assert estimated_range.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert (
        estimated_range.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfLength.KILOMETERS
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_range_estimated").options[
            "sensor"
        ]["suggested_display_precision"]
        == 0
    )

    ideal_range = hass.states.get("sensor.roadrunner_range_ideal")
    assert ideal_range.state == "330.1"
    assert ideal_range.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.DISTANCE
    assert ideal_range.attributes[ATTR_ICON] == "mdi:map-marker-distance"
    assert ideal_range.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert ideal_range.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfLength.KILOMETERS
    assert (
        entity_registry.async_get("sensor.roadrunner_range_ideal").options["sensor"][
            "suggested_display_precision"
        ]
        == 0
    )

    rated_range = hass.states.get("sensor.roadrunner_range_rated")
    assert rated_range.state == "325.7"
    assert rated_range.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.DISTANCE
    assert rated_range.attributes[ATTR_ICON] == "mdi:map-marker-distance"
    assert rated_range.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert rated_range.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfLength.KILOMETERS
    assert (
        entity_registry.async_get("sensor.roadrunner_range_rated").options["sensor"][
            "suggested_display_precision"
        ]
        == 0
    )

    scheduled_start_time = hass.states.get("sensor.roadrunner_charging_start_time")
    assert scheduled_start_time.state == "2026-06-07T12:34:56+00:00"
    assert (
        scheduled_start_time.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.TIMESTAMP
    )

    shift_state = hass.states.get("sensor.roadrunner_shift_state")
    assert shift_state.state == "D"
    assert shift_state.attributes[ATTR_ICON] == "mdi:car-shift-pattern"

    since = hass.states.get("sensor.roadrunner_last_seen")
    assert since.state == "2026-06-07T12:00:00+00:00"
    assert since.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.TIMESTAMP
    assert since.attributes[ATTR_ICON] == "mdi:timer-sand"

    speed = hass.states.get("sensor.roadrunner_speed")
    assert speed.state == "88.0"
    assert speed.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.SPEED
    assert speed.attributes[ATTR_ICON] == "mdi:speedometer"
    assert speed.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert speed.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfSpeed.KILOMETERS_PER_HOUR
    assert (
        entity_registry.async_get("sensor.roadrunner_speed").options["sensor"][
            "suggested_display_precision"
        ]
        == 0
    )

    vehicle_state = hass.states.get("sensor.roadrunner_state")
    assert vehicle_state.state == "Suspended"
    assert vehicle_state.attributes[ATTR_ICON] == "mdi:car-connected"

    charging_time_left = hass.states.get("sensor.roadrunner_charging_time_left")
    assert charging_time_left.state == "1.75"
    assert (
        charging_time_left.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.DURATION
    )
    assert charging_time_left.attributes[ATTR_ICON] == "mdi:timer"
    assert (
        charging_time_left.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    )
    assert charging_time_left.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfTime.HOURS

    tire_pressure_front_left = hass.states.get(
        "sensor.roadrunner_tire_pressure_front_left"
    )
    assert tire_pressure_front_left.state == "2.9"
    assert (
        tire_pressure_front_left.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.PRESSURE
    )
    assert tire_pressure_front_left.attributes[ATTR_ICON] == "mdi:gauge"
    assert (
        tire_pressure_front_left.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert (
        tire_pressure_front_left.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfPressure.BAR
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_tire_pressure_front_left").options[
            "sensor"
        ]["suggested_display_precision"]
        == 1
    )

    tire_pressure_front_right = hass.states.get(
        "sensor.roadrunner_tire_pressure_front_right"
    )
    assert tire_pressure_front_right.state == "2.8"
    assert (
        tire_pressure_front_right.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.PRESSURE
    )
    assert tire_pressure_front_right.attributes[ATTR_ICON] == "mdi:gauge"
    assert (
        tire_pressure_front_right.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert (
        tire_pressure_front_right.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfPressure.BAR
    )
    assert (
        entity_registry.async_get(
            "sensor.roadrunner_tire_pressure_front_right"
        ).options["sensor"]["suggested_display_precision"]
        == 1
    )

    tire_pressure_rear_left = hass.states.get(
        "sensor.roadrunner_tire_pressure_rear_left"
    )
    assert tire_pressure_rear_left.state == "2.7"
    assert (
        tire_pressure_rear_left.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.PRESSURE
    )
    assert tire_pressure_rear_left.attributes[ATTR_ICON] == "mdi:gauge"
    assert (
        tire_pressure_rear_left.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert (
        tire_pressure_rear_left.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfPressure.BAR
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_tire_pressure_rear_left").options[
            "sensor"
        ]["suggested_display_precision"]
        == 1
    )

    tire_pressure_rear_right = hass.states.get(
        "sensor.roadrunner_tire_pressure_rear_right"
    )
    assert tire_pressure_rear_right.state == "2.6"
    assert (
        tire_pressure_rear_right.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.PRESSURE
    )
    assert tire_pressure_rear_right.attributes[ATTR_ICON] == "mdi:gauge"
    assert (
        tire_pressure_rear_right.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert (
        tire_pressure_rear_right.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfPressure.BAR
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_tire_pressure_rear_right").options[
            "sensor"
        ]["suggested_display_precision"]
        == 1
    )

    assert hass.states.get("sensor.roadrunner_update_version") is None
    assert hass.states.get("sensor.roadrunner_version") is None

    assert entity_registry.async_get("sensor.roadrunner_battery").unique_id == (
        "teslamate/cars/1/battery_level"
    )
    assert entity_registry.async_get("sensor.roadrunner_usable_battery").unique_id == (
        "teslamate/cars/1/usable_battery_level"
    )
    assert entity_registry.async_get("sensor.roadrunner_center_display").unique_id == (
        "teslamate/cars/1/center_display_state"
    )
    assert entity_registry.async_get("sensor.roadrunner_energy_added").unique_id == (
        "teslamate/cars/1/charge_energy_added"
    )
    assert entity_registry.async_get("sensor.roadrunner_charge_limit").unique_id == (
        "teslamate/cars/1/charge_limit_soc"
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_charge_current_request").unique_id
        == "teslamate/cars/1/charge_current_request"
    )
    assert (
        entity_registry.async_get(
            "sensor.roadrunner_charge_current_request_max"
        ).unique_id
        == "teslamate/cars/1/charge_current_request_max"
    )
    assert entity_registry.async_get("sensor.roadrunner_charger_current").unique_id == (
        "teslamate/cars/1/charger_actual_current"
    )
    assert entity_registry.async_get("sensor.roadrunner_charger_phases").unique_id == (
        "teslamate/cars/1/charger_phases"
    )
    assert entity_registry.async_get("sensor.roadrunner_charger_power").unique_id == (
        "teslamate/cars/1/charger_power"
    )
    assert entity_registry.async_get("sensor.roadrunner_charger_voltage").unique_id == (
        "teslamate/cars/1/charger_voltage"
    )
    assert entity_registry.async_get("sensor.roadrunner_charging_state").unique_id == (
        "teslamate/cars/1/charging_state"
    )
    assert entity_registry.async_get("sensor.roadrunner_climate_keeper").unique_id == (
        "teslamate/cars/1/climate_keeper_mode"
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_display_name").disabled_by
        == er.RegistryEntryDisabler.INTEGRATION
    )
    assert entity_registry.async_get("sensor.roadrunner_elevation").unique_id == (
        "teslamate/cars/1/elevation"
    )
    assert entity_registry.async_get("sensor.roadrunner_exterior_color").unique_id == (
        "teslamate/cars/1/exterior_color"
    )
    assert entity_registry.async_get("sensor.roadrunner_geofence").unique_id == (
        "teslamate/cars/1/geofence"
    )
    assert entity_registry.async_get("sensor.roadrunner_heading").unique_id == (
        "teslamate/cars/1/heading"
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_temperature_inside").unique_id
        == "teslamate/cars/1/inside_temp"
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_temperature_outside").unique_id
        == "teslamate/cars/1/outside_temp"
    )
    assert entity_registry.async_get("sensor.roadrunner_odometer").unique_id == (
        "teslamate/cars/1/odometer"
    )
    assert entity_registry.async_get("sensor.roadrunner_power").unique_id == (
        "teslamate/cars/1/power"
    )
    assert entity_registry.async_get("sensor.roadrunner_range_estimated").unique_id == (
        "teslamate/cars/1/est_battery_range_km"
    )
    assert entity_registry.async_get("sensor.roadrunner_range_ideal").unique_id == (
        "teslamate/cars/1/ideal_battery_range_km"
    )
    assert entity_registry.async_get("sensor.roadrunner_range_rated").unique_id == (
        "teslamate/cars/1/rated_battery_range_km"
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_charging_start_time").unique_id
        == "teslamate/cars/1/scheduled_charging_start_time"
    )
    assert entity_registry.async_get("sensor.roadrunner_shift_state").unique_id == (
        "teslamate/cars/1/shift_state"
    )
    assert entity_registry.async_get("sensor.roadrunner_last_seen").unique_id == (
        "teslamate/cars/1/since"
    )
    assert entity_registry.async_get("sensor.roadrunner_speed").unique_id == (
        "teslamate/cars/1/speed"
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_spoiler_type").disabled_by
        == er.RegistryEntryDisabler.INTEGRATION
    )
    assert entity_registry.async_get("sensor.roadrunner_state").unique_id == (
        "teslamate/cars/1/state"
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_wheel_type").disabled_by
        == er.RegistryEntryDisabler.INTEGRATION
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_charging_time_left").unique_id
        == "teslamate/cars/1/time_to_full_charge"
    )
    assert (
        entity_registry.async_get(
            "sensor.roadrunner_tire_pressure_front_left"
        ).unique_id
        == "teslamate/cars/1/tpms_pressure_fl"
    )
    assert (
        entity_registry.async_get(
            "sensor.roadrunner_tire_pressure_front_right"
        ).unique_id
        == "teslamate/cars/1/tpms_pressure_fr"
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_tire_pressure_rear_left").unique_id
        == "teslamate/cars/1/tpms_pressure_rl"
    )
    assert (
        entity_registry.async_get(
            "sensor.roadrunner_tire_pressure_rear_right"
        ).unique_id
        == "teslamate/cars/1/tpms_pressure_rr"
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_update_version").disabled_by
        == er.RegistryEntryDisabler.INTEGRATION
    )
    assert (
        entity_registry.async_get("sensor.roadrunner_version").disabled_by
        == er.RegistryEntryDisabler.INTEGRATION
    )

    async_fire_teslamate_mqtt_message(hass, "charge_energy_added", "1.1")
    await hass.async_block_till_done()

    assert hass.states.get("sensor.roadrunner_energy_added").state == "1.1"


async def test_reused_topic_sensors_disabled_by_default(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test sensors for reused MQTT topics are disabled by default."""
    await async_setup_teslamate_mqtt_entry(hass)

    for entity_id, (topic, entity_category) in DISABLED_SENSOR_ENTITIES.items():
        assert hass.states.get(entity_id) is None
        registry_entry = entity_registry.async_get(entity_id)
        assert registry_entry.unique_id == f"teslamate/cars/1/{topic}"
        assert registry_entry.disabled_by == er.RegistryEntryDisabler.INTEGRATION
        assert registry_entry.entity_category == entity_category


async def test_reused_topic_sensors_when_enabled(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test values exposed by enabled sensors for reused MQTT topics."""
    for entity_id, (topic, _) in DISABLED_SENSOR_ENTITIES.items():
        entity_registry.async_get_or_create(
            "sensor",
            "teslamate_mqtt",
            f"teslamate/cars/1/{topic}",
            suggested_object_id=entity_id.removeprefix("sensor."),
        )

    await async_setup_teslamate_mqtt_entry(hass)

    topic_values = {
        "latitude": "37.5",
        "location": "Home",
        "longitude": "-122.25",
        "model": "3",
        "spoiler_type": "CarbonFiber",
        "sun_roof_installed": "true",
        "trim_badging": "Performance",
        "update_available": "true",
        "update_version": "2026.20.1",
        "version": "2026.14.1",
        "wheel_type": "SonicCarbonTwinTurbine19",
    }
    for topic, value in topic_values.items():
        async_fire_teslamate_mqtt_message(hass, topic, value)
    await hass.async_block_till_done()

    expected_states = {
        "sensor.roadrunner_display_name": "Roadrunner",
        **{
            entity_id: topic_values[topic]
            for entity_id, (topic, _) in DISABLED_SENSOR_ENTITIES.items()
            if topic != "display_name"
        },
    }
    for entity_id, state in expected_states.items():
        assert hass.states.get(entity_id).state == state

    for entity_id in ("sensor.roadrunner_latitude", "sensor.roadrunner_longitude"):
        coordinate_state = hass.states.get(entity_id)
        assert coordinate_state.attributes[ATTR_STATE_CLASS] == (
            SensorStateClass.MEASUREMENT
        )
        assert coordinate_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == DEGREE


async def test_active_route_sensors(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test sensors derived from the active route JSON topic."""
    hass.config.units = US_CUSTOMARY_SYSTEM
    await async_setup_teslamate_mqtt_entry(hass)

    for entity_id in ACTIVE_ROUTE_SENSOR_ENTITIES:
        assert hass.states.get(entity_id).state == STATE_UNAVAILABLE

    async_fire_teslamate_mqtt_message(
        hass,
        "active_route",
        json.dumps(
            {
                "destination": "Home",
                "energy_at_arrival": 73,
                "miles_to_arrival": 6.485299,
                "minutes_to_arrival": 23.466667,
                "traffic_minutes_delay": 0.0,
                "location": {"latitude": 35.278131, "longitude": 29.744801},
                "error": None,
            }
        ),
    )
    await hass.async_block_till_done()

    destination = hass.states.get("sensor.roadrunner_active_route_destination")
    assert destination.state == "Home"
    assert destination.attributes[ATTR_ICON] == "mdi:map-marker"

    energy = hass.states.get("sensor.roadrunner_active_route_energy_at_arrival")
    assert energy.state == "73"
    assert energy.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.BATTERY
    assert energy.attributes[ATTR_ICON] == "mdi:battery-80"
    assert energy.attributes[ATTR_UNIT_OF_MEASUREMENT] == PERCENTAGE

    distance = hass.states.get("sensor.roadrunner_active_route_distance_to_arrival")
    assert distance.state == "6.485299"
    assert distance.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.DISTANCE
    assert distance.attributes[ATTR_ICON] == "mdi:map-marker-distance"
    assert distance.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfLength.MILES

    minutes = hass.states.get("sensor.roadrunner_active_route_minutes_to_arrival")
    assert minutes.state == "23.466667"
    assert minutes.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.DURATION
    assert minutes.attributes[ATTR_ICON] == "mdi:clock-outline"
    assert minutes.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfTime.MINUTES

    traffic_delay = hass.states.get(
        "sensor.roadrunner_active_route_traffic_minutes_delay"
    )
    assert traffic_delay.state == "0.0"
    assert traffic_delay.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.DURATION
    assert traffic_delay.attributes[ATTR_ICON] == "mdi:clock-alert-outline"
    assert traffic_delay.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfTime.MINUTES

    for entity_id, topic in ACTIVE_ROUTE_SENSOR_ENTITIES.items():
        registry_entry = entity_registry.async_get(entity_id)
        assert registry_entry.unique_id == f"teslamate/cars/1/{topic}"
        assert registry_entry.disabled_by is None

    async_fire_teslamate_mqtt_message(
        hass,
        "active_route",
        json.dumps({"error": "No active route available"}),
    )
    await hass.async_block_till_done()

    for entity_id in ACTIVE_ROUTE_SENSOR_ENTITIES:
        assert hass.states.get(entity_id).state == STATE_UNAVAILABLE


async def test_active_route_sensors_unavailable_for_invalid_json(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
) -> None:
    """Test malformed active route JSON leaves derived sensors unavailable."""
    await async_setup_teslamate_mqtt_entry(hass)

    async_fire_teslamate_mqtt_message(hass, "active_route", "not json")
    await hass.async_block_till_done()

    for entity_id in ACTIVE_ROUTE_SENSOR_ENTITIES:
        assert hass.states.get(entity_id).state == STATE_UNAVAILABLE


async def test_active_route_distance_uses_home_assistant_unit_conversion(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
) -> None:
    """Test Home Assistant converts the native active route distance."""
    hass.config.units = METRIC_SYSTEM
    await async_setup_teslamate_mqtt_entry(hass)

    async_fire_teslamate_mqtt_message(
        hass,
        "active_route",
        json.dumps({"miles_to_arrival": 1, "error": None}),
    )
    await hass.async_block_till_done()

    distance = hass.states.get("sensor.roadrunner_active_route_distance_to_arrival")
    assert float(distance.state) == pytest.approx(1.609344)
    assert distance.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfLength.KILOMETERS


async def test_new_sensors(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test sensors added for new TeslaMate MQTT topics."""
    await async_setup_teslamate_mqtt_entry(hass)

    percentage_entities = {
        "sensor.roadrunner_software_update_download": (
            "download_perc",
            "100",
            "mdi:download",
        ),
        "sensor.roadrunner_software_update_installation": (
            "install_perc",
            "42",
            "mdi:update",
        ),
        "sensor.roadrunner_sunroof_open": (
            "sun_roof_percent_open",
            "80",
            "mdi:car-convertible",
        ),
    }
    for entity_id in (*percentage_entities, "sensor.roadrunner_sunroof_state"):
        assert hass.states.get(entity_id).state == STATE_UNKNOWN

    async_fire_teslamate_mqtt_message(hass, "download_perc", "100")
    async_fire_teslamate_mqtt_message(hass, "install_perc", "42")
    async_fire_teslamate_mqtt_message(hass, "sun_roof_percent_open", "80")
    async_fire_teslamate_mqtt_message(hass, "sun_roof_state", "partially_open")
    await hass.async_block_till_done()

    for entity_id, (topic, state, icon) in percentage_entities.items():
        percentage_state = hass.states.get(entity_id)
        assert percentage_state.state == state
        assert percentage_state.attributes[ATTR_STATE_CLASS] == (
            SensorStateClass.MEASUREMENT
        )
        assert percentage_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == PERCENTAGE
        assert percentage_state.attributes[ATTR_ICON] == icon
        registry_entry = entity_registry.async_get(entity_id)
        assert registry_entry.unique_id == f"teslamate/cars/1/{topic}"
        assert registry_entry.options["sensor"]["suggested_display_precision"] == 0

    sunroof_state = hass.states.get("sensor.roadrunner_sunroof_state")
    assert sunroof_state.state == "Partially Open"
    assert sunroof_state.attributes[ATTR_ICON] == "mdi:car-convertible"
    assert entity_registry.async_get("sensor.roadrunner_sunroof_state").unique_id == (
        "teslamate/cars/1/sun_roof_state"
    )


@pytest.mark.parametrize(
    ("payload", "state"),
    [
        pytest.param("Charging", "Charging", id="single_word"),
        pytest.param("NoPower", "No Power", id="camel_case"),
    ],
)
async def test_charging_state_values(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient, payload: str, state: str
) -> None:
    """Test charging state value formatting."""
    await async_setup_teslamate_mqtt_entry(hass)

    async_fire_teslamate_mqtt_message(hass, "charging_state", payload)
    await hass.async_block_till_done()

    assert hass.states.get("sensor.roadrunner_charging_state").state == state


@pytest.mark.parametrize(
    ("payload", "state"),
    [
        pytest.param("off", "Off", id="lowercase"),
        pytest.param("DOG", "Dog", id="uppercase"),
    ],
)
async def test_climate_keeper_mode_values(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient, payload: str, state: str
) -> None:
    """Test climate keeper mode value formatting."""
    await async_setup_teslamate_mqtt_entry(hass)

    async_fire_teslamate_mqtt_message(hass, "climate_keeper_mode", payload)
    await hass.async_block_till_done()

    assert hass.states.get("sensor.roadrunner_climate_keeper").state == state


@pytest.mark.parametrize(
    ("payload", "state"),
    [
        pytest.param("online", "Online", id="online"),
        pytest.param("offline", "Offline", id="offline"),
        pytest.param("suspended", "Suspended", id="suspended"),
    ],
)
async def test_state_values(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient, payload: str, state: str
) -> None:
    """Test vehicle state value formatting."""
    await async_setup_teslamate_mqtt_entry(hass)

    async_fire_teslamate_mqtt_message(hass, "state", payload)
    await hass.async_block_till_done()

    assert hass.states.get("sensor.roadrunner_state").state == state


@pytest.mark.parametrize(
    ("payload", "state"),
    [
        pytest.param("0", "off", id="off"),
        pytest.param("2", "standby", id="standby"),
        pytest.param("3", "charging", id="charging"),
        pytest.param("4", "on", id="on"),
        pytest.param("5", "large_charging", id="large_charging"),
        pytest.param("6", "ready_to_unlock", id="ready_to_unlock"),
        pytest.param("7", "sentry_mode", id="sentry_mode"),
        pytest.param("8", "dog_mode", id="dog_mode"),
        pytest.param("9", "media", id="media"),
    ],
)
async def test_center_display_state_values(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient, payload: str, state: str
) -> None:
    """Test center display state value mapping."""
    await async_setup_teslamate_mqtt_entry(hass)

    async_fire_teslamate_mqtt_message(hass, "center_display_state", payload)
    await hass.async_block_till_done()

    center_display_state = hass.states.get("sensor.roadrunner_center_display")
    assert center_display_state.state == state
    assert center_display_state.attributes["raw_value"] == payload


async def test_center_display_state_undocumented_value(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient, caplog: pytest.LogCaptureFixture
) -> None:
    """Test undocumented center display state value."""
    await async_setup_teslamate_mqtt_entry(hass)
    caplog.set_level(logging.WARNING)

    async_fire_teslamate_mqtt_message(hass, "center_display_state", "1")
    await hass.async_block_till_done()

    center_display_state = hass.states.get("sensor.roadrunner_center_display")
    assert center_display_state.state == STATE_UNKNOWN
    assert center_display_state.attributes["raw_value"] == "1"
    assert "Unexpected center display state value" not in caplog.text


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param("10", id="unmapped_integer"),
        pytest.param("bogus", id="non_integer"),
    ],
)
async def test_center_display_state_unexpected_value(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    caplog: pytest.LogCaptureFixture,
    payload: str,
) -> None:
    """Test unexpected center display state values."""
    await async_setup_teslamate_mqtt_entry(hass)
    caplog.set_level(logging.WARNING)

    async_fire_teslamate_mqtt_message(hass, "center_display_state", payload)
    await hass.async_block_till_done()

    center_display_state = hass.states.get("sensor.roadrunner_center_display")
    assert center_display_state.state == STATE_UNKNOWN
    assert center_display_state.attributes["raw_value"] == payload
    assert f"Unexpected center display state value: {payload}" in caplog.text
