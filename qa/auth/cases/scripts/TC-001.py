import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Cold start lands on the five-tab bar with no log-in wall",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC1 — cold start → tab bar, no wall",
 "env": "Android · auto (adb)",
 "precondition": [
  "API up; any account state"
 ],
 "steps": [
  "Force-stop the app and cold start it → check: nav.tab-profile within 20 s"
 ],
 "expected": [
  "Tabs nav.tab-path, nav.tab-explore, nav.tab-lessons, nav.tab-community, nav.tab-profile exist left to right with labels Path · Explore · Lessons · Community · Profile — UI tree",
  "No auth.login, auth.signup or auth.gate node on screen 5 s after launch — UI tree",
  "The first tab (Path) shows empty.coming-soon — UI tree + screenshot"
 ],
 "focus": "nav.tab-profile",
 "caption": {
  "expected": "five tabs, Path empty state"
 }
}


def run(c):
    c.pre("emulator online, API up")
    c.step(1, "Force-stop and cold start the app")
    c.checkpoint("tab bar shown within 20 s", launch_app(), "no nav.tab-profile")
    time.sleep(5)
    keys = ["path", "explore", "lessons", "community", "profile"]
    labels = ["Path", "Explore", "Lessons", "Community", "Profile"]
    ns = [find(f"nav.tab-{k}", exact=True) for k in keys]
    xs = [n["x"] if n else None for n in ns]
    in_order = all(xs) and xs == sorted(xs)
    lab = all(n and n["desc"] == l for n, l in zip(ns, labels))
    shot = c.shot("1_start")
    c.result(1, in_order and lab, f"x order {xs}, labels {[n['desc'] if n else None for n in ns]}", [shot])
    wall = [t for t in ("auth.login", "auth.signup", "auth.gate") if has(t, exact=True)]
    c.result(2, not wall, f"wall nodes: {wall}", [shot])
    c.result(3, has("empty.coming-soon", exact=True) and has("Coming with the next update"),
             "empty state on first tab", [shot])
