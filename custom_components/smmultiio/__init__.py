"""Sequent Microsystems Home Automation Integration"""

import logging

import voluptuous as vol
from homeassistant.const import CONF_NAME
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.discovery import load_platform

from . import data

DOMAIN = data.DOMAIN
LEGACY_DOMAIN = "SMmultiio"
NAME_PREFIX = data.NAME_PREFIX
SM_MAP = data.SM_MAP
SM_API = data.API

CONF_STACK = "stack"
CONF_TYPE = "type"
CONF_CHAN = "chan"
CONF_CHAN_RANGE = "chan_range"
CONF_CHANNELS = "channels"
CONF_UPDATE_INTERVAL = "update_interval" # In seconds
COM_NOGET = "__NOGET__"



CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema(vol.Any([vol.Schema({
        vol.Optional(CONF_STACK, default="0"): cv.string,
    }, extra=vol.ALLOW_EXTRA)], {}))
}, extra=vol.ALLOW_EXTRA)

_LOGGER = logging.getLogger(__name__)

async def SM_load_platform(hass, entity_config):
        for platform_type, attr in SM_MAP.items():
            if entity_config[CONF_TYPE] in attr:
                load_platform(
                        hass, platform_type, DOMAIN, entity_config, {}
                )

async def SM_load_all_platforms(hass, stack=0):
    for platform_type, platform in SM_MAP.items():
        for type, attr in platform.items():
            if attr.get("optional", False):
                continue
            for chan in range(int(attr["chan_no"])):
                entity_config = {
                        CONF_NAME: NAME_PREFIX+str(stack)+"_"+type+"_"+str(chan+1),
                        CONF_STACK: stack,
                        CONF_TYPE: type,
                        CONF_CHAN: chan+1
                }
                load_platform(
                        hass, platform_type, DOMAIN, entity_config, {}
                )


def create_entity_config(config, name, stack, type, chan, update_interval):
    entity_config = {
            **config,
            CONF_NAME: NAME_PREFIX + str(stack) + "_" + name,
            CONF_STACK: stack,
            CONF_TYPE: type,
            CONF_CHAN: chan,
            CONF_UPDATE_INTERVAL: update_interval,
    }
    return entity_config

async def async_setup(hass, config):
    registry = er.async_get(hass)
    legacy_entities = [
        entry for entry in registry.entities.values()
        if entry.platform == LEGACY_DOMAIN
    ]
    for entry in legacy_entities:
        if registry.async_get_entity_id(entry.domain, DOMAIN, entry.unique_id):
            raise RuntimeError(
                f"Cannot migrate {entry.entity_id}: its unique ID already exists "
                f"under {DOMAIN}"
            )
    for entry in legacy_entities:
        registry.async_update_entity_platform(entry.entity_id, DOMAIN)

    hass.data[DOMAIN] = []
    card_configs = config.get(DOMAIN)
    if not card_configs:
        await SM_load_all_platforms(hass, stack=0)
        return True
    for card_config in card_configs:
        stack = int(card_config.pop(CONF_STACK, 0))
        if not card_config:
            await SM_load_all_platforms(hass, stack=stack)
            continue
        for entity in card_config:
            card_config[entity] = card_config[entity] or {}
            channels = card_config[entity].get(CONF_CHANNELS)
            chan_range = card_config[entity].get(CONF_CHAN_RANGE)
            update_interval = card_config[entity].get(CONF_UPDATE_INTERVAL)
            single_channel = channels is None and chan_range is None
            if channels is not None:
                try:
                    if not isinstance(channels, str):
                        raise ValueError("expected a comma-separated string")
                    channel_numbers = [int(chan) for chan in channels.split(",")]
                    if len(channel_numbers) != len(set(channel_numbers)):
                        raise ValueError("duplicate channels")
                except ValueError as ex:
                    _LOGGER.error("Invalid channels for %s: %s", entity, ex)
                    continue
                type = entity
            elif chan_range is not None:
                try:
                    if not isinstance(chan_range, str):
                        raise ValueError("expected a start..end string")
                    chan_start, chan_end = (int(chan) for chan in chan_range.split(".."))
                    if chan_end < chan_start:
                        raise ValueError("end must not be less than start")
                except ValueError as ex:
                    _LOGGER.error("Invalid chan_range for %s: %s", entity, ex)
                    continue
                type = entity
                channel_numbers = range(chan_start, chan_end + 1)
            else:
                try:
                    type, chan = entity.rsplit("_", 1)
                    channel_numbers = [int(chan)]
                except ValueError:
                    _LOGGER.error("%s doesn't respect type_channel format", entity)
                    continue
            for chan in channel_numbers:
                name = entity if single_channel else f"{entity}_{chan}"
                entity_config = create_entity_config(
                        card_config[entity], name,
                        stack, type, chan, update_interval
                )
                await SM_load_platform(hass, entity_config)
    return True
