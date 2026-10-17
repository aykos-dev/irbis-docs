import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Status is not the first screen; reachable from Debug and by deep link",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC10 — Status behind the Debug screen and irbis://debug/status",
 "env": "Android · auto (adb)",
 "precondition": [
  "Dev build"
 ],
 "steps": [
  "Cold start → check: tab bar, no health.status-card",
  "Profile → Debug tools → API status",
  "Cold start and open irbis://debug/status"
 ],
 "expected": [
  "First screen is the tab bar, health.status-card absent — UI tree",
  "Profile → Debug tools (profile.debug) → debug.screen → API status (debug.api-status) opens health.status-card — UI tree",
  "irbis://debug/status opens health.status-card — UI tree + screenshot"
 ],
 "focus": "health.status-card",
 "caption": {
  "expected": "Status via Debug"
 }
}


def run(c):
    c.pre("dev build")
    c.checkpoint("tab bar shown", launch_app(), "no nav.tab-profile")
    time.sleep(2)
    c.result(1, not has("health.status-card", exact=True), "no status card on start", [c.shot("1_start")])
    c.step(2, "Profile → Debug tools → API status")
    goto_profile()
    tap("profile.debug", exact=True)
    ok = wait("debug.screen", 6, exact=True)
    tap("debug.api-status", exact=True)
    ok2 = wait("health.status-card", 10, exact=True)
    c.result(2, ok and ok2, f"debug={ok}, status={ok2}", [c.shot("2_status", focus="health.status-card")])
    c.step(3, "Deep link")
    launch_app()
    deep_link("irbis://debug/status")
    ok3 = wait("health.status-card", 15, exact=True)
    c.result(3, ok3, f"status via deep link={ok3}", [c.shot("3_link", focus="health.status-card")])
