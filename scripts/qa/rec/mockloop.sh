#!/bin/bash
# Re-sends the point from the point file ("LAT LNG ACC [AGE_SECONDS]") to the gps, network and fused
# test providers every second; re-adds a provider if Android removed it. Keep it running in a second terminal.
# usage: mockloop.sh [point file]   (default ~/.cache/irbis-qa/point.txt, the file drv.point() writes)
F="${1:-${QA_POINT:-$HOME/.cache/irbis-qa/point.txt}}"
mkdir -p "$(dirname "$F")"
[ -f "$F" ] || echo "41.3111 69.2797 10 0" > "$F"
while true; do
  read -r LAT LNG ACC AGE < "$F"
  t=$(( $(date +%s) * 1000 - ${AGE:-0} * 1000 ))
  for p in gps network fused; do
    if ! adb shell cmd location providers set-test-provider-location $p --location $LAT,$LNG --accuracy $ACC --time $t >/dev/null 2>&1; then
      adb shell cmd location providers add-test-provider $p >/dev/null 2>&1
      adb shell cmd location providers set-test-provider-enabled $p true >/dev/null 2>&1
      echo "$(date +%T) re-added $p"
    fi
  done
  sleep 1
done
