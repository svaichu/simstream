#!/usr/bin/env bash

# start_server.sh adjusted to work from the installed package location.
# It prefers the environment variable SIMSTREAM_ROOT to find `noVNC`.

set -euo pipefail

ROOT_DIR="${SIMSTREAM_ROOT:-}"
if [ -z "$ROOT_DIR" ]; then
  # If SIMSTREAM_ROOT is not set, try to derive from script location
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  ROOT_DIR="$SCRIPT_DIR"
fi

NOVNC_DIR="$ROOT_DIR/noVNC"

if [ ! -d "$NOVNC_DIR" ]; then
  echo "noVNC not found inside package at $NOVNC_DIR"
  echo "If you installed the package from PyPI the runner should have downloaded noVNC."
  echo "You can also place a copy of noVNC at: $NOVNC_DIR"
  exit 1
fi

# 1) start Xvfb in the background
Xvfb :1 -screen 0 1280x720x16 -ac 2>/dev/null &
export DISPLAY=:1
fluxbox 2>/dev/null &

echo -n "Waiting for Xvfb on ${DISPLAY}"
until xdpyinfo -display "${DISPLAY}" >/dev/null 2>&1; do
  sleep 0.1
  echo -n "."
done
echo " ready!"

# 2) now start the VNC server
x11vnc -display :1 -nopw -forever -shared -bg -rfbport 5901

echo -n "Waiting for VNC port 5901"
until ss -ltn | grep -q ":5901 "; do
  sleep 0.1
  echo -n "."
done
echo " ready!"

# 3) clean up any old websockify and start noVNC
pgrep -f "websockify .* 6080" | xargs -r kill -9 || true
pgrep -f "/bin/bash .* 6080"  | xargs -r kill -9 || true
sleep 0.5

cd "$NOVNC_DIR"
./utils/websockify/run 6080 --web "$NOVNC_DIR" localhost:5901 &
echo "✔ GUI ready → http://<server-ip>:6080/vnc.html"
echo "  DISPLAY=:1 exported."
