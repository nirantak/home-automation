#!/bin/bash
set -euo pipefail

USER=$(whoami)
HUE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
BASE_DIR="$( dirname "${HUE_DIR}" )"
# set -x

function install() {
  echo "Installing Hue Automation Scripts"
  sudo mkdir -p /var/log/com.nirantak
  sudo chown -R $USER:staff /var/log/com.nirantak
  touch /var/log/com.nirantak/signal_video.std{out,err}.log
  clear_logs
  start
}

function start() {
  stop
  echo "Starting Hue Automation"
  cp -fv "$HUE_DIR/com.nirantak.signal_video.plist" ~/Library/LaunchAgents/
  /usr/bin/sed -i "" "s+FULL_PATH_HERE+${HUE_DIR}+g" ~/Library/LaunchAgents/com.nirantak.signal_video.plist
  launchctl load -w ~/Library/LaunchAgents/com.nirantak.signal_video.plist
}

function clear_logs() {
  echo "Clearing Old Logs"
  echo '' > /var/log/com.nirantak/signal_video.stdout.log
  echo '' > /var/log/com.nirantak/signal_video.stderr.log
}

function logs() {
  echo "Getting Logs"
  tail -f /var/log/com.nirantak/signal_video.*.log
}

function stop() {
  echo "Stopping Hue Automation"
  launchctl unload -w ~/Library/LaunchAgents/com.nirantak.signal_video.plist
}

function uninstall() {
  stop
  rm -f ~/Library/LaunchAgents/com.nirantak.signal_video.plist
  rm -f /var/log/com.nirantak/signal_video.*.log
  echo "Uninstalling Hue Automation Scripts"
}

function run() {
  echo "Running Hue Automation at $(date)"
  cd $BASE_DIR && ./.venv/bin/python3 hue_lights/signal_on_video_call.py
}

function help() {
  declare -F | awk '{print $NF}' | sort | egrep -v "^_"
}

if [ $# -eq 0 ]; then
  echo "Please provide one of the following arguments:"
  help
  exit 1
else
  "$@"
fi
