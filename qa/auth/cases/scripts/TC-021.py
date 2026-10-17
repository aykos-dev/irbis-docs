import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Correct code and a new password log the user in and end the other sessions",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC5 — reset with code logs in, signs out other sessions",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-VERIFIED user with a second (API) session",
  "Guest, Forgot password open"
 ],
 "steps": [
  "Submit the username → check: auth.reset",
  "Read the code from the API log, type it, new password, submit",
  "API: log in with the old, then the new password",
  "API: refresh with the second session's refresh token"
 ],
 "expected": [
  "Event password_reset_done and the app lands on Profile signed in as the user — event log + UI tree",
  "Old password → 401, new password → 200 — API response",
  "The other session's refresh token is refused (401) — API response"
 ],
 "focus": "profile.account",
 "caption": {
  "expected": "logged in after reset"
 }
}


def run(c):
    u = make_user("rst", phone=phone(13), verified=True)
    c.pre(f"QA-VERIFIED {u['username']}, other session open")
    before = len(sms_codes(u["id"]))
    c.checkpoint("forgot screen open", open_forgot(), "no auth.forgot")
    c.step(1, "Submit the username")
    fill("auth.username", u["username"]); tap_submit()
    c.checkpoint("code screen", wait("auth.reset", 10, exact=True), "no auth.reset")
    code = wait_new_code(u["id"], before, 10)
    c.checkpoint("code in API log", bool(code), "no new SMS line")
    c.step(2, "Type the code and the new password")
    fill("auth.code", code); fill("auth.new-password", PW2); hide_kb()
    t0 = c.mark()
    tap_submit()
    ev = c.wait_event("password_reset_done", t0, 15)
    ok = wait("profile.account", 15, exact=True)
    wait("profile.username", 8, exact=True)
    c.result(1, bool(ev) and ok and field_text("profile.username") == u["username"], f"event={bool(ev)}, profile.account={ok}", [c.shot("2_done", focus="profile.account")])
    s_old, _, _ = api("POST", "/v1/auth/log-in", {"username": u["username"], "password": PW})
    s_new, _, _ = api("POST", "/v1/auth/log-in", {"username": u["username"], "password": PW2})
    c.result(2, s_old == 401 and s_new == 200, f"old→{s_old}, new→{s_new}")
    s_ref, d_ref, _ = api("POST", "/v1/auth/refresh", {"refreshToken": u["refresh"]})
    c.result(3, s_ref == 401, f"old session refresh → {s_ref} {d_ref.get('code')}")
