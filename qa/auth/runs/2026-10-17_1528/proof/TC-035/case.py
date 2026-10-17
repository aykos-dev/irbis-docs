import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Guest language moves into the account once, after the first sign-up on the device",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC8 — guest-merge sent once after first sign-up/log-in",
 "env": "Android · auto (adb)",
 "precondition": [
  "Guest; app language English"
 ],
 "steps": [
  "Profile → Language → Uzbek",
  "Sign up a free username",
  "Sign out and log in again with the same account",
  "Restore English while a guest"
 ],
 "expected": [
  "Event guest_merged {items ≥ 1} after sign-up — event log",
  "API /v1/me locale is 'uz' for the new account — API response",
  "No second guest_merged event within 6 s of the next log-in — event log"
 ],
 "focus": "profile.account",
 "caption": {
  "expected": "merged once"
 }
}


def run(c):
    import random
    name = f"qa_gm_{random.randint(1000, 9999)}"
    c.pre(f"guest; free username {name}")
    c.checkpoint("guest state", ensure_guest(), "no guest Profile")
    c.step(1, "Choose Uzbek")
    tap("profile.language", exact=True)
    c.checkpoint("language sheet", wait("profile.language-sheet", 6, exact=True), "no sheet")
    tap("profile.language-uz", exact=True)
    time.sleep(1.5)
    tap("profile.guest-signup", exact=True)
    c.checkpoint("sign-up screen", wait("auth.signup", 8, exact=True), "no auth.signup")
    c.step(2, "Sign up")
    t0 = c.mark()
    ui_signup(name, PW)
    ev = c.wait_event("guest_merged", t0, 15)
    c.result(1, ev is not None and int(ev.get("items", 0)) >= 1, f"event: {ev}")
    st, d, _ = api("POST", "/v1/auth/log-in", {"username": name, "password": PW})
    _, me, _ = api("GET", "/v1/me", token=d.get("accessToken"))
    c.result(2, me.get("locale") == "uz", f"locale={me.get('locale')}")
    c.step(3, "Sign out, log in again")
    wait("profile.account", 10, exact=True)
    tap("profile.sign-out", exact=True)
    c.checkpoint("guest again", wait("profile.guest", 10, exact=True), "no guest")
    tap("profile.guest-login", exact=True)
    c.checkpoint("login screen", wait("auth.login", 8, exact=True), "no auth.login")
    t1 = c.mark()
    ui_login(name, PW)
    c.result(3, c.no_event("guest_merged", t1, 6), "no second guest_merged")
    c.step(4, "Restore English")
    tap("profile.sign-out", exact=True); wait("profile.guest", 10, exact=True)
    tap("profile.language", exact=True); wait("profile.language-sheet", 6, exact=True); tap("profile.language-en", exact=True)
