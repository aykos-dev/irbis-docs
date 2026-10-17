import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "A wrong verification code is refused and the phone stays unverified",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC6 — wrong code does not verify",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-USER without phone, signed in, code requested for the phone"
 ],
 "steps": [
  "Add the phone, then type a wrong 6-digit code, submit"
 ],
 "expected": [
  "Error 'That code isn't right.' — UI tree + screenshot",
  "No recovery_phone_verified event; API /v1/me hasRecoveryPhone stays false — event log + API response"
 ],
 "focus": "auth.recovery-phone",
 "caption": {
  "expected": "wrong verify code"
 }
}


def run(c):
    u = make_user("phw")
    c.pre(f"QA-USER {u['username']} signed in")
    c.checkpoint("signed in", open_signed_in(u), "profile.account not shown")
    before = len(sms_codes(u["id"]))
    tap("profile.recovery-phone", exact=True)
    c.checkpoint("phone screen", wait("auth.recovery-phone", 8, exact=True), "no auth.recovery-phone")
    fill("auth.phone", phone_digits(20)); tap_submit()
    code = wait_new_code(u["id"], before, 8)
    c.checkpoint("code step", wait("auth.code", 8, exact=True) and bool(code), "no code step")
    c.step(1, "Wrong code")
    t0 = c.mark()
    fill("auth.code", "000000" if code != "000000" else "111111"); tap_submit()
    time.sleep(2)
    m = field_text("auth.error") or field_text("auth.code-error") or ""
    c.result(1, "That code isn't right." in m, f"message={m!r}", [c.shot("1_wrong", focus="auth.recovery-phone")])
    none = c.no_event("recovery_phone_verified", t0, 3)
    st, d, _ = api("POST", "/v1/auth/log-in", {"username": u["username"], "password": PW})
    _, me, _ = api("GET", "/v1/me", token=d.get("accessToken"))
    c.result(2, none and me.get("hasRecoveryPhone") is False, f"no event={none}, hasRecoveryPhone={me.get('hasRecoveryPhone')}")
