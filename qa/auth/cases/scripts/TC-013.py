import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Sign-up with a recovery phone reports has_phone and stores the phone",
 "priority": "P2",
 "group": "Supplementary",
 "requirement": "AC3 — optional recovery phone accepted at sign-up",
 "env": "Android · auto (adb)",
 "precondition": [
  "Guest; sign-up started from the Profile tab"
 ],
 "steps": [
  "Create account with a free username, the run password, phone +998 90 000 00 12, terms ticked"
 ],
 "expected": [
  "Event signed_up {has_phone: true} — event log",
  "Signed in on Profile with the Recovery phone row present (profile.recovery-phone) — UI tree",
  "DB: the user's recovery_phone column is set (stored, not shown) — DB"
 ],
 "focus": "profile.account",
 "caption": {
  "expected": "signed up with phone"
 }
}


def run(c):
    import random
    name = f"qa_sup_{random.randint(1000, 9999)}"
    c.pre(f"free username {name}")
    c.checkpoint("sign-up screen open", open_signup(), "no auth.signup")
    c.step(1, "Fill the form with phone and submit")
    t0 = c.mark()
    ui_signup(name, PW, phone_d=phone_digits(12))
    ev = c.wait_event("signed_up", t0, 15)
    c.result(1, bool(ev) and ev.get("has_phone") in (True, "true"), f"event: {ev}")
    ok = wait("profile.account", 15, exact=True)
    shot = c.shot("2_profile", focus="profile.account")
    c.result(2, ok and has("profile.recovery-phone", exact=True), f"profile.account={ok}", [shot])
    stored = sql(f"select recovery_phone is not null from users where username='{name}'")
    c.result(3, stored == "t", f"recovery_phone set: {stored}")
