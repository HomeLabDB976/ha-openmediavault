import asyncio
from custom_components.openmediavault.api import OpenMediaVaultAPI


async def main():

    omv = OpenMediaVaultAPI(
        "http://100.68.121.109",
        "admin",
        "Awesome976.org"
    )

    print("Connecting...")
    await omv.connect()

    print("Login successful!")
    print("Session ID:", omv.session_id)

    print("Calling System.getInformation...")

    result = await omv.call(
        "System",
        "getInformation"
    )

    print("Response:")
    print(result)

    await omv.close()


asyncio.run(main())
