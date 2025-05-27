from http import HTTPStatus
import requests
import logging
import asyncio
import aiohttp
import async_timeout

import json
import base64
import datetime

from typing import Any

import voluptuous as vol

import re
from bs4 import BeautifulSoup

import homeassistant.loader as loader
import homeassistant.helpers.config_validation as cv

from homeassistant.helpers.aiohttp_client import async_get_clientsession

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD
from homeassistant.core import (
    HomeAssistant,
    ServiceResponse,
    ServiceCall,
    SupportsResponse,
)

from homeassistant.helpers import discovery

from .const import DOMAIN,PLATFORMS, BSE_URL

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({DOMAIN: {}}, extra=vol.ALLOW_EXTRA)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})

    await _async_setup_service(hass, entry)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """설정 항목을 언로드합니다."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """업데이트 리스너"""
    await hass.config_entries.async_reload(entry.entry_id)


async def _async_setup_service( hass: HomeAssistant, entry: ConfigEntry ) -> None:
    """서비스를 설정합니다."""

    session = async_get_clientsession(hass)

    async def _async_rank(call: ServiceCall) -> None:

        param = call.data.get("team", None)

        header = { 
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "Content-Type": "application/json" }

        response = await session.get(BSE_URL, headers=header)
        
        rank = await response.json()

        rankarr = []
        rnk = {}

        for team in rank["list"]:
            rankdict = {}

            rankdict["id"]        = team["teamId"]
            rankdict["cpTeamId"]  = team["cpTeamId"]
            rankdict["name"]      = team["name"]
            rankdict["shortName"] = team["shortName"]
            rankdict["imageUrl"]  = team["imageUrl"]
            rankdict["rank"]      = team["rank"]
            
            rnk[team["shortName"]] = rankdict

            if param is None:
                return rankdict

            rankarr.append(rankdict)

        _LOGGER.error(f"[{DOMAIN}] _async_rank() -> {rankarr}")

        return rnk[param]

    hass.services.async_register(DOMAIN, "rank", _async_rank, supports_response=SupportsResponse.ONLY, )