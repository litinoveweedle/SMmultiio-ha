"""Sequent Microsystems Multi-IO Integration."""

from sequent_ha_common import Card
from sequent_ha_common import setup as shared_setup
from sequent_ha_common.const import (
    COM_NOGET,
    CONF_CHAN,
    CONF_CHAN_RANGE,
    CONF_CHANNELS,
    CONF_NAME,
    CONF_STACK,
    CONF_TYPE,
    CONF_UPDATE_INTERVAL,
)

from . import data

DOMAIN = data.DOMAIN
LEGACY_DOMAIN = "SMmultiio"
NAME_PREFIX = data.NAME_PREFIX
SM_MAP = data.SM_MAP
SM_API = data.API
CARD = Card(DOMAIN, LEGACY_DOMAIN, NAME_PREFIX, data.FULL_NAME, SM_MAP, SM_API)
CONFIG_SCHEMA = shared_setup.config_schema(CARD)


async def async_setup(hass, config):
    return await shared_setup.async_setup(hass, config, CARD)


async def async_setup_entry(hass, entry):
    return await shared_setup.async_setup_entry(hass, entry, CARD)


async def async_unload_entry(hass, entry):
    return await shared_setup.async_unload_entry(hass, entry, CARD)
