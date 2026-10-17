import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Reset refuses a 5-char new password and leaves the old one valid",
 "priority": "P2",
 "group": "Supplementary",
 "requirement": "AC5 — new password 6–64 on reset",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-VERIFIED user",
  "Reset code screen with the right code"
 ],
 "steps": [
  "Type the right code and a 5-char new password, submit"
 ],
 "expected": [
  "Error 'Use 6–64 characters.' on auth.new-password — UI tree + screenshot",
  "No password_reset_done event and the old password still works through the API (200) — event log + API response"
 ],
 "focus": "auth.new-password",
 "caption": {
  "expected": "short new password"
 }
}


def run(c):
    u = make_user("npw", phone=phone(18), verified=True)
    before = len(sms_codes(u["id"]))
    c.pre(f"QA-VERIFIED {u['username']}")
    c.checkpoint("forgot screen open", open_forgot(), "no auth.forgot")
    fill("auth.username", u["username"]); tap_submit()
    c.checkpoint("code screen", wait("auth.reset", 10, exact=True), "no auth.reset")
    code = wait_new_code(u["id"], before, 10)
    c.checkpoint("code in API log", bool(code), "no new SMS line")
    c.step(1, "Right code, 5-char new password")
    t0 = c.mark()
    fill("auth.code", code); fill("auth.new-password", "ab12c"); hide_kb(); tap_submit()
    ok = wait("Use 6–64 characters.", 6)
    c.result(1, ok, f"error shown={ok}", [c.shot("1_short", focus="auth.new-password")])
    none = c.no_event("password_reset_done", t0, 3)
    st, _, _ = api("POST", "/v1/auth/log-in", {"username": u["username"], "password": PW})
    c.result(2, none and st == 200, f"no event={none}, old password → {st}")
