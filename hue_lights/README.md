# Hue Lights

## Automation

### On Air signal for video calls

- This script [`hue_lights/signal_on_video_call.py`](https://github.com/nirantak/home-automation/blob/main/hue_lights/signal_on_video_call.py) can detect when the macOS camera is turned on/off, to trigger Hue lights.
- To use, clone this repo and create a `.env` file based on the sample, with the local IP address and username for the Hue bridge API.
  - Follow the [project readme](https://github.com/nirantak/home-automation#setting-up) to setup the required python environment.
  - Run `hue bridge discover` to get the Hue bridge IP address and set the env variable `HUE_BRIDGE_IP` (or go to [discovery.meethue.com](https://discovery.meethue.com/)).
  - Follow [this link](https://developers.meethue.com/develop/get-started-2/#so-lets-get-started) to create a Hue API user if not already known, and set the env variable `HUE_BRIDGE_USER` ([API reference](https://developers.meethue.com/develop/hue-api/7-configuration-api/#create-user)).
- Set the env variable `HUE_ON_AIR_LIGHT` to override the light number to be controlled.
- Once `./make.sh install` is run, a plist file is copied to the current user's LaunchAgents, so the script will restart on error and when the machine is rebooted.

```bash
cd home-automation        # project root dir
source .venv/bin/activate # activate virtual environment
cd hue_lights
./make.sh install         # to setup the environment for the script
./make.sh start           # to start if stopped, or to reload the plist
./make.sh logs            # to view logs generated
./make.sh stop            # to turn off the automation
./make.sh uninstall       # to remove the plist
```

## References

- https://github.com/nirantak/hue-api
