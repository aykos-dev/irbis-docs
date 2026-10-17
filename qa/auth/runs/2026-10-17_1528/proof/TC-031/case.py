import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Log-in prompt for a guest: shown with the reason, Not now closes with nothing lost",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC7 — gate for a guest; Not now",
 "env": "Android · auto (adb)",
 "precondition": [
  "Guest; Debug screen open (irbis://debug)"
 ],
 "steps": [
  "Open the Debug screen → check: debug.screen",
  "Tap Open log-in prompt → check: auth.gate",
  "Tap Not now"
 ],
 "expected": [
  "auth.gate sheet shows the title, Create free account (auth.gate-signup), I have an account (auth.gate-login), Not now (auth.gate-not-now) — UI tree + screenshot",
  "Events auth_gate_shown then auth_gate_dismissed — event log",
  "After Not now: gate closed, Debug screen still shown and debug.gate-ran count unchanged (0) over 3 s — UI tree"
 ],
 "focus": "auth.gate",
 "caption": {
  "expected": "log-in prompt"
 }
}


def run(c):
    c.pre("guest")
    c.checkpoint("guest state", ensure_guest(), "no guest Profile")
    c.checkpoint("Debug screen open", open_debug(), "no debug.screen")
    before = field_text("debug.gate-ran")
    c.step(1, "Tap Open log-in prompt")
    t0 = c.mark()
    tap("debug.open-gate", exact=True)
    shown = wait("auth.gate", 8, exact=True)
    shot = c.shot("1_gate", focus="auth.gate")
    parts = all(has(x, exact=True) for x in ("auth.gate-signup", "auth.gate-login", "auth.gate-not-now")) and has("Create free account") and has("I have an account") and has("Not now")
    c.result(1, shown and parts, f"gate shown={shown}, parts={parts}", [shot])
    c.step(2, "Tap Not now")
    tap("auth.gate-not-now", exact=True)
    gone = wait_gone("auth.gate", 6)
    e1 = c.wait_event("auth_gate_shown", t0, 3)
    e2 = c.wait_event("auth_gate_dismissed", t0, 5)
    c.result(2, bool(e1 and e2), f"shown={e1}, dismissed={e2}")
    time.sleep(3)
    after = field_text("debug.gate-ran")
    c.result(3, gone and has("debug.screen", exact=True) and before == after, f"gate gone={gone}, ran text before/after: {before!r} / {after!r}", [c.shot("2_closed", focus="debug.gate-ran")])
