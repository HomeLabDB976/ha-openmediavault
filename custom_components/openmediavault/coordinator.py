import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class OpenMediaVaultCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, api):
        self.api = api

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),
        )

    async def _async_update_data(self):
        try:
            response = await self.api.call(
                "System",
                "getInformation",
            )

            if response.get("error"):
                raise Exception(response["error"])

            return response["response"]

        except Exception as err:
            raise UpdateFailed(
                f"Error communicating with OpenMediaVault: {err}"
            ) from err
