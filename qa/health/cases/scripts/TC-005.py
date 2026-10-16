import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa  (shared points/accounts/helpers of this feature)
except ImportError:
    pass

META = {
 "title": "Pull to refresh refetches",
 "group": "Supplementary",
 "priority": "P2",
 "env": "Android · auto (adb) · resources: API-UP",
 "plan": "Test_health.md",
 "anchor": "tc-005--p2--pull-to-refresh-refetches",
 "source": "AC3",
 "expected": [
  "A new `health_checked` { status: \"ok\" } event after the swipe — event log",
  "The refresh indicator appears and then hides — screenrecord+frames"
 ],
 "caption": {
  "expected": "A new `health_checked` { status: \"ok\" } event after the swipe"
 },
 "plan_hash": "ceef57a784"
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
    ev = c.wait_event("health_checked", t0, 5)
    c.result(1, bool(ev and ev.get("status") == "ok"), f"event after swipe: {ev}")
    shot = c.shot("1_after_refresh")
    c.result(2, None, "refresh indicator: judge from video frames around the swipe", [shot])
