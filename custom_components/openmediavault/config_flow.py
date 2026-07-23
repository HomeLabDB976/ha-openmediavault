import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN
from .api import OpenMediaVaultAPI


class OpenMediaVaultConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input:
            api = OpenMediaVaultAPI(
                user_input["host"],
                user_input["username"],
                user_input["password"],
            )

            try:
                await api.connect()

            except Exception as err:
                print(f"OMV connection error: {err}")
                errors["base"] = "cannot_connect"

            else:
                return self.async_create_entry(
                    title="OpenMediaVault",
                    data=user_input,
                )

            finally:
                await api.close()

        schema = vol.Schema(
            {
                vol.Required("host"): str,
                vol.Required("username"): str,
                vol.Required("password"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
