import os

import httpx
from dotenv import load_dotenv

load_dotenv()

HUE_API = (
    f"http://{os.environ['HUE_BRIDGE_IP']}/api/{os.environ['HUE_BRIDGE_USER']}"
)


async def turn_on_light(light: int) -> bool:
    async with httpx.AsyncClient() as client:
        data = {"on": True}
        resp = await client.put(f"{HUE_API}/lights/{light}/state", json=data)
        print(f"Light {light} ON resp: {resp.text}")
        return resp.status_code == httpx.codes.OK


async def turn_off_light(light: int) -> bool:
    async with httpx.AsyncClient() as client:
        data = {"on": False}
        resp = await client.put(f"{HUE_API}/lights/{light}/state", json=data)
        print(f"Light {light} OFF resp: {resp.text}")
        return resp.status_code == httpx.codes.OK
