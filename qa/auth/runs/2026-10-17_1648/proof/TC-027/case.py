import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Signed-in Profile shows username, Recovery phone row and Sign out",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC6 — signed-in Profile content",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-USER without phone, signed in on the device"
 ],
 "steps": [
  "Log in through the app → check: profile.account"
 ],
 "expected": [
  "profile.username shows the username — UI tree + screenshot",
  "Row profile.recovery-phone 'Recovery phone' with value 'Add' — UI tree",
  "Button profile.sign-out 'Sign out'; no guest buttons — UI tree"
 ],
 "focus": "profile.account",
 "caption": {
  "expected": "signed-in Profile"
 }
}


def run(c):
    u = make_user("pro")
    c.pre(f"QA-USER {u['username']} without phone")
    c.step(1, "Log in through the app")
    c.checkpoint("signed in", open_signed_in(u), "profile.account not shown")
    wait("profile.username", 8, exact=True)
    shot = c.shot("1_account", focus="profile.account")
    c.result(1, field_text("profile.username") == u["username"], f"username={field_text('profile.username')!r}", [shot])
    row = find("profile.recovery-phone", exact=True)
    c.result(2, bool(row) and has("Recovery phone") and has("Add"), f"row present={bool(row)}", [shot])
    c.result(3, has("profile.sign-out", exact=True) and has("Sign out") and not has("profile.guest-signup", exact=True), "sign-out present, no guest buttons", [shot])
