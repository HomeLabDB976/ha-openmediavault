from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from homeassistant.core import HomeAssistant

from .api import OpenMediaVaultAPI
from .const import DOMAIN, SCAN_INTERVAL


class OpenMediaVaultCoordinator(DataUpdateCoordinator):

    def __init__(
        self,
        hass: HomeAssistant,
        api: OpenMediaVaultAPI,
    ):
        self.api = api

        super().__init__(
            hass,
            hass.helpers.event,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self):

        system = await self.api.call(
            "System",
            "getInformation"
        )

        return system["response"]
