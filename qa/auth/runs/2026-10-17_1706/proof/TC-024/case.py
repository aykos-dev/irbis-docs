import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "An expired code is refused with a clear message",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC5 — code valid 5 minutes",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-VERIFIED user",
  "Reset code requested"
 ],
 "steps": [
  "Request the code, then age it on the local DB (expires_at one minute in the past)",
  "Type the right code and a valid new password, submit"
 ],
 "expected": [
  "Message 'The code expired. Send a new one.' — UI tree + screenshot",
  "No password_reset_done event; still signed out — event log + UI tree"
 ],
 "focus": "auth.reset",
 "caption": {
  "expected": "expired code"
 }
}


def run(c):
    u = make_user("exp", phone=phone(16), verified=True)
    before = len(sms_codes(u["id"]))
    c.pre(f"QA-VERIFIED {u['username']}")
    c.checkpoint("forgot screen open", open_forgot(), "no auth.forgot")
    fill("auth.username", u["username"]); tap_submit()
    c.checkpoint("code screen", wait("auth.reset", 10, exact=True), "no auth.reset")
    code = wait_new_code(u["id"], before, 10)
    c.checkpoint("code in API log", bool(code), "no new SMS line")
    c.step(1, "Age the code on the local DB")
    sql(f"update sms_codes set expires_at = now() - interval '1 minute' where user_id='{u['id']}' and purpose='password_reset' and used_at is null")
    c.step(2, "Submit the right code")
    t0 = c.mark()
    fill("auth.code", code); fill("auth.new-password", PW2); hide_kb(); tap_submit()
    time.sleep(2)
    m = field_text("auth.error") or field_text("auth.code-error") or ""
    c.result(1, "The code expired. Send a new one." in m, f"message={m!r}", [c.shot("2_expired", focus="auth.reset")])
    none = c.no_event("password_reset_done", t0, 3)
    c.result(2, none and has("auth.reset", exact=True), f"no event={none}")
