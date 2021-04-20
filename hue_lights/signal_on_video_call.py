#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv
from hue import Color, Light

load_dotenv()


ALERT_STATE = {
    "on": True,
    "bri": 200,
    "xy": Color().rgb_to_xy(255, 0, 0),
}
LIGHT_ID = os.environ.get("HUE_ON_AIR_LIGHT", 1)
HUE_BRIDGE_IP = os.environ["HUE_BRIDGE_IP"]
HUE_BRIDGE_USER = os.environ["HUE_BRIDGE_USER"]


async def trigger_hue_light(light: Light, data: str):
    resp = None
    if "Post event kCameraStreamStart" in data:
        await light.save_state()
        resp = await light.set_state(ALERT_STATE)
    elif "Post event kCameraStreamStop" in data:
        resp = await light.restore_state()
    return resp


async def main():
    process = await asyncio.create_subprocess_exec(
        "log",
        "stream",
        "--type",
        "log",
        "--style",
        "compact",
        "--predicate",
        '(category == "device") && (eventMessage contains "Camera")',
        stdout=asyncio.subprocess.PIPE,
    )
    light = Light(LIGHT_ID, ip=HUE_BRIDGE_IP, user=HUE_BRIDGE_USER)

    async for line in process.stdout:
        data = line.decode()
        print(f"STDOUT: {data}")
        await trigger_hue_light(light, data)

    process.kill()
    return await process.wait()


asyncio.run(main())
