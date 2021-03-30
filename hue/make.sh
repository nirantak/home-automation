#!/bin/bash
set -euo pipefail

USER=$(whoami)
CURRDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# set -x

function install() {
  echo "Installing Hue Automation Scripts"
  sudo mkdir -p /var/log/com.nirantak
  sudo chown -R $USER:staff /var/log/com.nirantak
  touch /var/log/com.nirantak/signal_video.std{out,err}.log
  cd $CURRDIR && python3 -m venv .venv
  source $CURRDIR/.venv/bin/activate > /dev/null 2>&1
  $CURRDIR/.venv/bin/pip3 install -U pip wheel setuptools
  cd $CURRDIR && ./.venv/bin/pip3 install -U -r requirements.txt
  start
}

function start() {
  stop
  echo "Starting Hue Automation"
  cp -fv "$CURRDIR/com.nirantak.signal_video.plist" ~/Library/LaunchAgents/
  /usr/bin/sed -i "" "s+FULL_PATH_HERE+${CURRDIR}+g" ~/Library/LaunchAgents/com.nirantak.signal_video.plist
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
  cd "$(dirname $CURRDIR)" && ./.venv/bin/python3 -m hue.signal_on_video_call
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
