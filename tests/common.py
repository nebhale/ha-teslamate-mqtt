"""Common helpers for TeslaMate MQTT tests."""

import asyncio
from collections.abc import Callable, Coroutine
from typing import Any
from unittest.mock import patch

from homeassistant.components import mqtt
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_fire_mqtt_message,
)

from custom_components.teslamate_mqtt.const import CONF_TOPIC_ROOT, DOMAIN

DEFAULT_DISPLAY_NAME = "Roadrunner"
DEFAULT_TOPIC_ROOT = "teslamate/cars/1"


@callback
def async_on_subscribe_done(
    hass: HomeAssistant,
    topic: str,
    qos: int,
    on_subscribe_status: Callable[[], None],
) -> CALLBACK_TYPE:
    """Call the MQTT subscribe status callback immediately."""
    on_subscribe_status()
    return lambda: None


async def async_setup_teslamate_mqtt_entry(
    hass: HomeAssistant,
    topic_root: str = DEFAULT_TOPIC_ROOT,
    display_name: str = DEFAULT_DISPLAY_NAME,
) -> MockConfigEntry:
    """Set up a TeslaMate MQTT config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=display_name,
        data={CONF_TOPIC_ROOT: topic_root},
        unique_id=topic_root,
    )
    entry.add_to_hass(hass)

    subscribe_started = asyncio.Event()
    real_async_subscribe = mqtt.async_subscribe

    async def async_subscribe(
        hass: HomeAssistant,
        topic: str,
        msg_callback: Callable[[mqtt.ReceiveMessage], Coroutine[Any, Any, None] | None],
        qos: int = 0,
        encoding: str | None = "utf-8",
    ) -> CALLBACK_TYPE:
        """Subscribe to MQTT and mark the subscription as started."""
        unsub = await real_async_subscribe(hass, topic, msg_callback, qos, encoding)
        subscribe_started.set()
        return unsub

    with (
        patch(
            "custom_components.teslamate_mqtt.mqtt.async_on_subscribe_done",
            side_effect=async_on_subscribe_done,
        ),
        patch(
            "custom_components.teslamate_mqtt.mqtt.async_subscribe",
            side_effect=async_subscribe,
        ),
    ):
        setup_task = hass.async_create_task(
            hass.config_entries.async_setup(entry.entry_id)
        )
        await subscribe_started.wait()
        async_fire_teslamate_mqtt_message(
            hass, "display_name", display_name, retain=True
        )
        assert await setup_task
    await hass.async_block_till_done()

    return entry


def async_fire_teslamate_mqtt_message(
    hass: HomeAssistant,
    topic: str,
    payload: str,
    topic_root: str = DEFAULT_TOPIC_ROOT,
    retain: bool = False,
) -> None:
    """Fire a TeslaMate MQTT message for the default test car."""
    async_fire_mqtt_message(hass, f"{topic_root}/{topic}", payload, retain=retain)
