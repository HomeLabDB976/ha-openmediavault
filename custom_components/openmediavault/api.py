import aiohttp


class OpenMediaVaultAPI:
    def __init__(self, host, username, password):
        self.host = host.rstrip("/")
        self.username = username
        self.password = password
        self.session = None
        self.session_id = None

    async def connect(self):
        self.session = aiohttp.ClientSession()

        payload = {
            "service": "Session",
            "method": "login",
            "params": {
                "username": self.username,
                "password": self.password
            }
        }

        async with self.session.post(
            f"{self.host}/rpc.php",
            json=payload
        ) as response:
            data = await response.json()

        if data.get("response"):
            self.session_id = data["response"]["sessionid"]
            return True

        raise Exception(f"Login failed: {data}")

    async def call(self, service, method, params=None):
        if not self.session_id:
            raise Exception("Not authenticated")

        payload = {
            "service": service,
            "method": method,
            "params": params or {}
        }

        headers = {
            "X-OPENMEDIAVAULT-SESSIONID": self.session_id
        }

        async with self.session.post(
            f"{self.host}/rpc.php",
            json=payload,
            headers=headers
        ) as response:
            return await response.json()

    async def close(self):
        if self.session:
            await self.session.close()
