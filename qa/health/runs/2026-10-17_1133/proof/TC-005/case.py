import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Pull to refresh refetches",
 "priority": "P2",
 "group": "Core",
 "requirement": "AC3 — pull to refresh refetches",
 "env": "Android · auto (adb)",
 "precondition": [
  "Status screen showing ok, online"
 ],
 "steps": [
  "Swipe down on the Status screen"
 ],
 "expected": [
  "New health_checked {status: ok} after the swipe — event log",
  "Refresh spinner visible right after the swipe — screenshot (human)"
 ],
 "focus": None,
 "caption": {
  "expected": "spinner, refreshed"
 }
}


def run(c):
    c.pre('App open on the Status screen showing ok, online')
    reverse(True)
    relaunch()
    c.checkpoint("status ok first", wait("API is up", 15), card_texts()[:6])
    time.sleep(1)
    t0 = c.mark()
    c.step(1, "Pull to refresh")
    w, h = screen_size()
    swipe(w // 2, int(h * 0.3), w // 2, int(h * 0.75), 400)
    spin = c.shot("1_spinner")
    ev = c.wait_event("health_checked", t0, 5)
    c.result(1, bool(ev and ev.get("status") == "ok"), f"event after swipe: {ev}")
    c.result(2, None, "refresh indicator: judge from the screenshot taken right after the swipe", [spin])
