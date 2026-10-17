import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Four wrong passwords do not lock: the fifth attempt with the right password logs in",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC4 — lockout boundary 4 (not yet locked)",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-USER exists",
  "Guest, log-in screen open"
 ],
 "steps": [
  "Send 4 wrong passwords for the QA-USER through the API",
  "Log in through the app with the right password"
 ],
 "expected": [
  "API: four wrong attempts each 401 INVALID_CREDENTIALS — API response",
  "App log-in with the right password succeeds: event logged_in and profile.account — event log + UI tree"
 ],
 "focus": "profile.account",
 "caption": {
  "expected": "4 wrong then ok"
 }
}


def run(c):
    u = make_user("l4")
    c.pre(f"QA-USER {u['username']}")
    codes = []
    c.step(1, "Four wrong passwords via the API")
    for _ in range(4):
        st, d, _ = api("POST", "/v1/auth/log-in", {"username": u["username"], "password": PW2})
        codes.append((st, d.get("code")))
        time.sleep(0.3)
    c.result(1, all(x == (401, "INVALID_CREDENTIALS") for x in codes), f"{codes}")
    c.checkpoint("log-in screen open", open_login(), "no auth.login")
    c.step(2, "Log in with the right password")
    t0 = c.mark()
    ok = ui_login(u["username"], PW)
    ev = c.wait_event("logged_in", t0, 10)
    c.result(2, ok and bool(ev), f"profile.account={ok}, logged_in event={bool(ev)}", [c.shot("2_in", focus="profile.account")])
