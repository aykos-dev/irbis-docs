import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Add a recovery phone and verify it with the SMS code",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC6 — add phone, code sent, verify marks verified",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-USER without phone, signed in on the device"
 ],
 "steps": [
  "Tap Recovery phone → check: auth.recovery-phone",
  "Type 9 digits (90 000 00 19), submit",
  "Type the code from the API log, submit"
 ],
 "expected": [
  "After submit the code step is shown (auth.code) and a code is in the API log — UI tree + API log",
  "Event recovery_phone_verified — event log",
  "Profile row shows 'Verified' with a check; API /v1/me hasRecoveryPhone true — UI tree + API response"
 ],
 "focus": "profile.recovery-phone",
 "caption": {
  "expected": "phone verified"
 }
}


def run(c):
    u = make_user("ph")
    c.pre(f"QA-USER {u['username']} signed in")
    c.checkpoint("signed in", open_signed_in(u), "profile.account not shown")
    before = len(sms_codes(u["id"]))
    c.step(1, "Open Recovery phone, add the number")
    tap("profile.recovery-phone", exact=True)
    c.checkpoint("phone screen", wait("auth.recovery-phone", 8, exact=True), "no auth.recovery-phone")
    fill("auth.phone", phone_digits(19)); tap_submit()
    shown = wait("auth.code", 8, exact=True)
    code = wait_new_code(u["id"], before, 8)
    c.result(1, shown and bool(code), f"code step={shown}, code logged={bool(code)}", [c.shot("1_code", focus="auth.recovery-phone")])
    c.step(2, "Type the code and verify")
    t0 = c.mark()
    fill("auth.code", code or "000000"); tap_submit()
    ev = c.wait_event("recovery_phone_verified", t0, 10)
    c.result(2, ev is not None, f"event={ev is not None}")
    wait("profile.account", 10, exact=True)
    shot = c.shot("3_verified", focus="profile.recovery-phone")
    st, d, _ = api("POST", "/v1/auth/log-in", {"username": u["username"], "password": PW})
    st2, me, _ = api("GET", "/v1/me", token=d.get("accessToken"))
    c.result(3, has("Verified") and me.get("hasRecoveryPhone") is True, f"row Verified={has('Verified')}, hasRecoveryPhone={me.get('hasRecoveryPhone')}", [shot])
