import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa  (shared points/accounts/helpers of this feature)
except ImportError:
    pass

META = {
 "title": "Largest font size does not clip the card",
 "group": "Supplementary",
 "priority": "P3",
 "env": "Android · auto (adb) · resources: API-UP",
 "plan": "Test_health.md",
 "anchor": "tc-009--p3--largest-font-size-does-not-clip-the-card",
 "source": "standards §12",
 "expected": [
  "All card texts fully visible (wrap or scroll, no clipped words), Retry/refresh still reachable — screenshot"
 ],
 "caption": {
  "expected": "All card texts fully visible (wrap or scroll, no clipped words), Retry/refresh s"
 },
 "plan_hash": "a9a3b2b7f0"
}


def run(c):
    prev_font = sh("settings", "get", "system", "font_scale").strip() or "1.0"
    c.pre('API-UP')
    reverse(True)
    c.step(1, "Font scale 2.0, cold start")
    font_scale(2.0)
    try:
        relaunch()
        c.checkpoint("status shown", wait("health.status-card", 15, exact=True), card_texts()[:6])
        wait("health.api-chip", 8, exact=True)
        shot = c.shot("1_font2")
        c.result(1, None, "clipping at 2.0: judge from the screenshot", [shot])
    finally:
        font_scale(prev_font)
