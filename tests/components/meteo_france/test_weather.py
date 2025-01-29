"""Test Météo France weather entity."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from syrupy.assertion import SnapshotAssertion

from homeassistant.components.weather import (
    ATTR_CONDITION_PARTLYCLOUDY,
    ATTR_WEATHER_HUMIDITY,
    ATTR_WEATHER_PRESSURE,
    ATTR_WEATHER_TEMPERATURE,
    ATTR_WEATHER_WIND_BEARING,
    ATTR_WEATHER_WIND_GUST_SPEED,
    ATTR_WEATHER_WIND_SPEED,
)
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from tests.common import MockConfigEntry, snapshot_platform


@pytest.fixture(autouse=True)
def override_platforms() -> Generator[None]:
    """Override PLATFORMS."""
    with patch("homeassistant.components.meteo_france.PLATFORMS", [Platform.WEATHER]):
        yield


async def test_weather(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the weather entity."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)

    assert len(hass.states.async_entity_ids("weather")) == 1
    entity_id = hass.states.async_entity_ids("weather")[0]

    state = hass.states.get(entity_id)
    assert state
    assert state.state == ATTR_CONDITION_PARTLYCLOUDY
    assert state.attributes[ATTR_WEATHER_TEMPERATURE] == 9.1
    assert state.attributes[ATTR_WEATHER_PRESSURE] == 988.7
    assert state.attributes[ATTR_WEATHER_HUMIDITY] == 75
    assert state.attributes[ATTR_WEATHER_WIND_SPEED] == 28.8
    assert state.attributes[ATTR_WEATHER_WIND_BEARING] == 200
    assert state.attributes[ATTR_WEATHER_WIND_GUST_SPEED] == 64.8
