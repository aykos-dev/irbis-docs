import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Offline shows a persistent banner and keeps the last result",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC3 — offline banner, cached result kept",
 "env": "Android · auto (adb)",
 "precondition": [
  "Status screen showing ok"
 ],
 "steps": [
  "Wi-Fi and mobile data off → check: both off"
 ],
 "expected": [
  "app.offline-banner at 5 s and still at 15 s — UI tree",
  "Last result still shown and marked stale ('Not updated…') — UI tree"
 ],
 "postcondition": "network back on",
 "focus": null,
 "caption": {
  "expected": "offline banner, result kept"
 }
}


def run(c):
    c.pre('App open on the Status screen showing ok')
    reverse(True)
    relaunch()
    c.checkpoint("status ok first", wait("API is up", 15), card_texts()[:6])
    c.step(1, "Turn Wi-Fi and mobile data off")
    set_network(False, False)
    try:
        wifi = sh("settings", "get", "global", "wifi_on").strip()
        data = sh("settings", "get", "global", "mobile_data").strip()
        c.checkpoint("Wi-Fi and mobile data off", wifi == "0" and data == "0", f"wifi_on={wifi} mobile_data={data}")
        b1 = wait("app.offline-banner", 5, exact=True)
        s1 = c.shot("1_offline_5s")
        time.sleep(10)
        b2 = has("app.offline-banner", exact=True)
        s2 = c.shot("1_offline_15s")
        c.result(1, b1 and b2, f"banner at 5 s: {b1}, at 15 s: {b2}", [s1, s2])
        kept = has("API is up")
        stale = has("Not updated") or has("last known result") or has("last saved data")
        c.result(2, kept and stale, f"result kept: {kept}, marked stale: {stale}; texts: {card_texts()[:10]}", [s2])
    finally:
        c.setup("Restore network")
        set_network(True, True)
        wait_gone("app.offline-banner", 10)
