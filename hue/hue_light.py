import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

HUE_API: str = (
    f"http://{os.environ['HUE_BRIDGE_IP']}/api/{os.environ['HUE_BRIDGE_USER']}"
)
ORIGINAL_STATE: dict[Any] = {}


async def switch_on(light: int) -> bool:
    async with httpx.AsyncClient() as client:
        data = {"on": True}
        resp = await client.put(f"{HUE_API}/lights/{light}/state", json=data)
        print(f"Light {light} ON resp: {resp.text}")
        return resp.status_code == httpx.codes.OK


async def switch_off(light: int) -> bool:
    async with httpx.AsyncClient() as client:
        data = {"on": False}
        resp = await client.put(f"{HUE_API}/lights/{light}/state", json=data)
        print(f"Light {light} OFF resp: {resp.text}")
        return resp.status_code == httpx.codes.OK


async def get_state(light: int) -> bool:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{HUE_API}/lights/{light}")
        resp = resp.json()["state"]
        print(f"Light {light} resp: {resp}")
        return resp


async def set_state(light: int, state: dict[Any]) -> bool:
    async with httpx.AsyncClient() as client:
        data = {"on": bool(state.get("on"))}
        for i in ["bri", "hue", "sat", "xy", "ct"]:
            if s := state.get(i):
                data[i] = s

        resp = await client.put(f"{HUE_API}/lights/{light}/state", json=data)
        print(f"Light {light} resp: {resp.text}")
        return (resp.status_code == httpx.codes.OK, resp.json())


async def save_state(light: int) -> dict[Any]:
    ORIGINAL_STATE = await get_state(light)
    return ORIGINAL_STATE


async def restore_state(light: int) -> dict[Any]:
    return await set_state(light, ORIGINAL_STATE)
