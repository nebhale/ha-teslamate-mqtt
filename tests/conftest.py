"""Test fixtures for the TeslaMate MQTT custom integration."""

import pytest


@pytest.fixture(autouse=True)
def _enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Enable custom integration loading for TeslaMate MQTT tests."""


@pytest.fixture
def expected_lingering_timers() -> bool:
    """Allow the MQTT test client periodic timer to be cleaned up by the harness."""
    return True
