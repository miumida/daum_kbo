"""Config flow for daum_kbo"""
import logging
import json
from typing import Optional

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .const import DOMAIN, TITLE

_LOGGER = logging.getLogger(__name__)

class DaumKboConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for daum_kbo."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize flow."""
        self._id: Optional[str] = None

    async def async_step_user(self, user_input=None, error: Optional[str] = None):
        """Handle the initial step."""
        errors = {}

        if user_input is None:
            return self.async_show_form(step_id="user")
            
        await self.async_set_unique_id(f"{DOMAIN}")

        self._abort_if_unique_id_configured()
        
        return self.async_create_entry(title=f"{TITLE}", data=user_input)
