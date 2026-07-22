from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [
            OMVCPUSensor(coordinator),
            OMVMemorySensor(coordinator),
            OMVUptimeSensor(coordinator),
            OMVUpdatesSensor(coordinator),
        ]
    )


class OMVBaseSensor(SensorEntity):

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_has_entity_name = True

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.data["hostname"])},
            name=self.coordinator.data["hostname"],
            manufacturer="OpenMediaVault",
            model=self.coordinator.data["version"],
        )

    async def async_update(self):
        await self.coordinator.async_request_refresh()


class OMVCPUSensor(OMVBaseSensor):

    _attr_name = "CPU Usage"
    _attr_native_unit_of_measurement = "%"

    @property
    def native_value(self):
        return round(
            self.coordinator.data["cpuUtilization"] * 100,
            1
        )


class OMVMemorySensor(OMVBaseSensor):

    _attr_name = "Memory Usage"
    _attr_native_unit_of_measurement = "%"

    @property
    def native_value(self):
        return round(
            float(self.coordinator.data["memUtilization"]) * 100,
            1
        )


class OMVUptimeSensor(OMVBaseSensor):

    _attr_name = "Uptime"
    _attr_native_unit_of_measurement = "s"

    @property
    def native_value(self):
        return round(
            self.coordinator.data["uptime"]
        )


class OMVUpdatesSensor(OMVBaseSensor):

    _attr_name = "Available Updates"

    @property
    def native_value(self):
        return self.coordinator.data["availablePkgUpdates"]
