#!/usr/bin/env python3
import asyncio
import os

from . import hue_light as hue

ALERT_STATE = {
    "on": True,
    "bri": 200,
    "xy": [0.704, 0.296],  # red
}


async def trigger_hue_light(data: str, light: int) -> bool:
    resp = None
    if "Post event kCameraStreamStart" in data:
        resp = await hue.set_state(light, ALERT_STATE)
    elif "Post event kCameraStreamStop" in data:
        resp = await hue.restore_state(light)
    return resp


async def main():
    light = os.environ.get("HUE_ON_AIR_LIGHT", 1)
    await hue.save_state(light)

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

    async for line in process.stdout:
        data = line.decode()
        print(f"STDOUT: {data}")
        await trigger_hue_light(data, light)

    process.kill()
    return await process.wait()


asyncio.run(main())
