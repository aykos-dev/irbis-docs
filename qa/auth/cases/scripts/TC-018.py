import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Continue as guest closes the log-in screen",
 "priority": "P2",
 "group": "Supplementary",
 "requirement": "AC4 — 'Continue as guest' closes the screen",
 "env": "Android · auto (adb)",
 "precondition": [
  "Guest; log-in opened from Profile"
 ],
 "steps": [
  "Profile → Log in → check: auth.login",
  "Tap Continue as guest"
 ],
 "expected": [
  "auth.login is gone and the guest Profile (profile.guest) is shown — UI tree + screenshot",
  "Still a guest: no profile.username — UI tree"
 ],
 "focus": "profile.guest",
 "caption": {
  "expected": "back on guest Profile"
 }
}


def run(c):
    c.pre("guest")
    c.checkpoint("log-in screen open", open_login(), "no auth.login")
    c.step(1, "Tap Continue as guest")
    tap("auth.continue-guest", exact=True)
    gone = wait_gone("auth.login", 5)
    on = wait("profile.guest", 5, exact=True)
    shot = c.shot("1_closed", focus="profile.guest")
    c.result(1, gone and on, f"login gone={gone}, guest profile={on}", [shot])
    c.result(2, not has("profile.username", exact=True), "no account node", [shot])
