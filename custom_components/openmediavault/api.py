import aiohttp


class OpenMediaVaultAPI:

    def __init__(self, host, username, password):
        self.host = host.rstrip("/")
        self.username = username
        self.password = password
        self.session_id = None
        self.session = aiohttp.ClientSession()

    async def close(self):
        if self.session:
            await self.session.close()

    async def connect(self):

        payload = {
            "service": "Session",
            "method": "login",
            "params": {
                "username": self.username,
                "password": self.password,
            },
        }

        async with self.session.post(
            f"{self.host}/rpc.php",
            json=payload,
        ) as response:

            data = await response.json()

            if data.get("error"):
                await self.close()
                raise Exception(
                    f"Login failed: {data}"
                )

            self.session_id = data["response"]["sessionid"]

            return True


    async def call(self, service, method, params=None):

        payload = {
            "service": service,
            "method": method,
            "params": params or {},
        }

        headers = {
            "X-OPENMEDIAVAULT-SESSIONID": self.session_id
        }

        async with self.session.post(
            f"{self.host}/rpc.php",
            json=payload,
            headers=headers,
        ) as response:

            return await response.json()
