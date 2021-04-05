#!/usr/bin/env python3
import asyncio
import os

from . import hue_light as hue


async def trigger_hue_light(data: str, light: int = 1) -> bool:
    resp = None
    light = os.environ.get("HUE_ON_AIR_LIGHT", light)
    if "Post event kCameraStreamStart" in data:
        resp = await hue.turn_on_light(light)
    elif "Post event kCameraStreamStop" in data:
        resp = await hue.turn_off_light(light)
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

    async for line in process.stdout:
        data = line.decode()
        print(f"STDOUT: {data}")
        await trigger_hue_light(data)

    process.kill()
    return await process.wait()


asyncio.run(main())
