from .api import OpenMediaVaultAPI
from .coordinator import OpenMediaVaultCoordinator
from .const import DOMAIN


async def async_setup_entry(hass, entry):

    api = OpenMediaVaultAPI(
        entry.data["host"],
        entry.data["username"],
        entry.data["password"],
    )

    await api.connect()

    coordinator = OpenMediaVaultCoordinator(
        hass,
        api
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        ["sensor"]
    )

    return True
