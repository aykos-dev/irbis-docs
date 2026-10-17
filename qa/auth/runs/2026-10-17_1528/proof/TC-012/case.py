import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Sign-up with a 6-char password and no phone logs in and returns to Profile",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC3 — success logs in and returns to where it started",
 "env": "Android · auto (adb)",
 "precondition": [
  "Guest; sign-up started from the Profile tab"
 ],
 "steps": [
  "Profile → Create free account → check: auth.signup",
  "Fill a free username, the 6-char password, no phone, tick terms, submit",
  "Log in again through the API with the same credentials"
 ],
 "expected": [
  "Event signed_up {has_phone: false} — event log",
  "Back on the Profile tab signed in: profile.account with profile.username = the new username — UI tree + screenshot",
  "API log-in with the same username in other case and the 6-char password → 200 — API response"
 ],
 "focus": "profile.account",
 "caption": {
  "expected": "signed in after sign-up"
 }
}


def run(c):
    import random
    name = f"qa_su6_{random.randint(1000, 9999)}"
    c.pre(f"free username {name}; password = 6-char run password")
    c.checkpoint("sign-up screen open", open_signup(), "no auth.signup")
    c.step(1, "Fill the form and submit")
    t0 = c.mark()
    ui_signup(name, PW6)
    ev = c.wait_event("signed_up", t0, 15)
    c.result(1, bool(ev) and ev.get("has_phone") in (False, "false"), f"event: {ev}")
    ok = wait("profile.account", 15, exact=True)
    wait("profile.username", 10, exact=True)
    shot = c.shot("2_profile", focus="profile.account")
    c.result(2, ok and field_text("profile.username") == name, f"on profile.account={ok}, username={field_text('profile.username')!r}", [shot])
    st, d, _ = api("POST", "/v1/auth/log-in", {"username": name.upper(), "password": PW6})
    c.result(3, st == 200, f"API log-in (upper-case name) → {st}")
