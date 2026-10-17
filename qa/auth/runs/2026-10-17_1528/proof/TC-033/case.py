import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Create account from the prompt: sign-up returns to where it started and the action runs once",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC7 — prompt → sign-up → action once; AC3 returns to start",
 "env": "Android · auto (adb)",
 "precondition": [
  "Guest; Debug screen"
 ],
 "steps": [
  "Debug → Open log-in prompt → Create free account",
  "Fill a free username, the run password, tick terms, submit"
 ],
 "expected": [
  "Sign-up screen opens from the prompt (auth.signup) — UI tree",
  "After sign-up the app is back on the Debug screen (debug.screen), not Profile — UI tree + screenshot",
  "debug.gate-ran shows 1 and stays 1 after 4 s — UI tree"
 ],
 "focus": "debug.gate-ran",
 "caption": {
  "expected": "back on Debug, ran once"
 }
}


def run(c):
    import random
    name = f"qa_gs_{random.randint(1000, 9999)}"
    c.pre(f"guest; free username {name}")
    c.checkpoint("guest state", ensure_guest(), "no guest Profile")
    c.checkpoint("Debug screen open", open_debug(), "no debug.screen")
    tap("debug.open-gate", exact=True)
    c.checkpoint("gate shown", wait("auth.gate", 8, exact=True), "no auth.gate")
    c.step(1, "Tap Create free account")
    tap("auth.gate-signup", exact=True)
    c.result(1, wait("auth.signup", 8, exact=True), "sign-up screen from prompt")
    c.step(2, "Fill and submit")
    ui_signup(name, PW)
    back_on = wait("debug.screen", 15, exact=True)
    ran = wait("ran 1 time", 6)
    c.result(2, back_on and not has("profile.account", exact=True), f"back on Debug={back_on}", [c.shot("2_back", focus="debug.gate-ran")])
    time.sleep(4)
    c.result(3, ran and "ran 1 time" in (field_text("debug.gate-ran") or ""), f"after 4 s: {field_text('debug.gate-ran')!r}")
