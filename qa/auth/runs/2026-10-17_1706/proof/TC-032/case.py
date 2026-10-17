import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Log in from the prompt: the gated action continues exactly once",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC7 — after log-in the gated action continues once",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-USER; guest; Debug screen"
 ],
 "steps": [
  "Debug → Open log-in prompt → I have an account",
  "Log in with the QA-USER",
  "Wait 4 s on the Debug screen"
 ],
 "expected": [
  "Log-in screen opens from the prompt (auth.login) — UI tree",
  "After log-in the Debug screen shows 'The gated action ran 1 time(s).' — UI tree + screenshot",
  "Still 1 after 4 s (it did not run twice) — UI tree"
 ],
 "focus": "debug.gate-ran",
 "caption": {
  "expected": "gated action ran once"
 }
}


def run(c):
    u = make_user("gl")
    c.pre(f"QA-USER {u['username']}; guest")
    c.checkpoint("guest state", ensure_guest(), "no guest Profile")
    c.checkpoint("Debug screen open", open_debug(), "no debug.screen")
    tap("debug.open-gate", exact=True)
    c.checkpoint("gate shown", wait("auth.gate", 8, exact=True), "no auth.gate")
    c.step(1, "Tap I have an account")
    tap("auth.gate-login", exact=True)
    ok1 = wait("auth.login", 8, exact=True)
    c.result(1, ok1, f"login screen={ok1}", [c.shot("1_login")])
    c.step(2, "Log in")
    fill("auth.username", u["username"]); fill("auth.password", PW); tap_submit()
    back_on = wait("debug.screen", 15, exact=True)
    ran = wait("ran 1 time", 6)
    shot = c.shot("2_ran", focus="debug.gate-ran")
    c.result(2, back_on and ran, f"back on Debug={back_on}, text={field_text('debug.gate-ran')!r}", [shot])
    time.sleep(4)
    c.result(3, "ran 1 time" in (field_text("debug.gate-ran") or ""), f"after 4 s: {field_text('debug.gate-ran')!r}", [c.shot("3_still", focus="debug.gate-ran")])
