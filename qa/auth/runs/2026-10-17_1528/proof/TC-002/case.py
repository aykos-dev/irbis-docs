import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Path, Explore, Lessons, Community show the coming-soon empty state",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC1 — four tabs empty state",
 "env": "Android · auto (adb)",
 "precondition": [
  "App on the tab bar"
 ],
 "steps": [
  "Tap each of Explore, Lessons, Community, Path in turn → check: empty.coming-soon within 5 s each"
 ],
 "expected": [
  "Each of the four tabs shows 'Coming with the next update', 'Irbis is still packing for this one.' and the sleepy Irbis ('Irbis, sleepy') — screenshot per tab",
  "Event tab_opened {tab} with the tapped tab's key for each of the four taps — event log"
 ],
 "focus": "empty.coming-soon",
 "caption": {
  "expected": "coming soon + sleepy Irbis"
 }
}


def run(c):
    c.pre("app launched")
    checkpoint_ok = launch_app()
    c.checkpoint("tab bar shown", checkpoint_ok, "no tab bar")
    shots, good, evs = [], [], []
    for i, k in enumerate(["explore", "lessons", "community", "path"], 1):
        c.step(i, f"Tap tab {k}")
        t0 = c.mark()
        tap(f"nav.tab-{k}", exact=True)
        shown = wait("empty.coming-soon", 5, exact=True)
        ok = shown and has("Coming with the next update") and has("Irbis is still packing for this one.") and has("Irbis, sleepy")
        shots.append(c.shot(f"{i}_{k}", focus="empty.coming-soon"))
        good.append((k, bool(ok)))
        ev = c.wait_event("tab_opened", t0, 5, lambda p, k=k: p.get("tab") == k)
        evs.append((k, bool(ev)))
    c.result(1, all(o for _, o in good), f"per tab: {good}", shots)
    c.result(2, all(o for _, o in evs), f"tab_opened per tab: {evs}")
