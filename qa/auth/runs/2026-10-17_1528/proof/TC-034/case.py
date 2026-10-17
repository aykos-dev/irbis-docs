import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Signed-in user: the gated action runs immediately with no prompt",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC7 — signed in runs the action at once",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-USER signed in on the device"
 ],
 "steps": [
  "Open Debug → Open log-in prompt"
 ],
 "expected": [
  "No auth.gate within 3 s — UI tree",
  "debug.gate-ran increments to 1 straight away — UI tree",
  "No auth_gate_shown event — event log"
 ],
 "focus": "debug.gate-ran",
 "caption": {
  "expected": "ran immediately"
 }
}


def run(c):
    u = make_user("gi")
    c.pre(f"QA-USER {u['username']} signed in")
    c.checkpoint("signed in", open_signed_in(u), "profile.account not shown")
    c.checkpoint("Debug screen open", open_debug(), "no debug.screen")
    c.step(1, "Tap Open log-in prompt")
    t0 = c.mark()
    tap("debug.open-gate", exact=True)
    ran = wait("ran 1 time", 3)
    shot = c.shot("1_ran", focus="debug.gate-ran")
    c.result(1, not has("auth.gate", exact=True), "no gate sheet", [shot])
    c.result(2, ran, f"gate-ran text={field_text('debug.gate-ran')!r}", [shot])
    c.result(3, c.no_event("auth_gate_shown", t0, 2), "no auth_gate_shown")
