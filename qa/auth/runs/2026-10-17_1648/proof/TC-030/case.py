import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Sign out returns to the guest Profile and stays signed out after restart",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC6 — sign out clears the Keychain, back to guest, no wall",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-USER signed in on the device"
 ],
 "steps": [
  "Tap Sign out → check: profile.guest",
  "Force-stop and cold start; open Profile"
 ],
 "expected": [
  "Guest Profile (profile.guest) shown, tab bar still present (no wall) — UI tree + screenshot",
  "Event signed_out — event log",
  "After restart the Profile is still the guest Profile (no stored session) — UI tree"
 ],
 "focus": "profile.guest",
 "caption": {
  "expected": "signed out, guest"
 }
}


def run(c):
    u = make_user("out")
    c.pre(f"QA-USER {u['username']} signed in")
    c.checkpoint("signed in", open_signed_in(u), "profile.account not shown")
    c.step(1, "Tap Sign out")
    t0 = c.mark()
    tap("profile.sign-out", exact=True)
    ok = wait("profile.guest", 10, exact=True)
    shot = c.shot("1_guest", focus="profile.guest")
    c.result(1, ok and has("nav.tab-profile", exact=True) and not has("auth.login", exact=True), f"guest profile={ok}", [shot])
    ev = c.wait_event("signed_out", t0, 5)
    c.result(2, ev is not None, f"signed_out event={ev is not None}")
    c.step(2, "Restart and open Profile")
    launch_app()
    where = goto_profile()
    c.result(3, where == "profile.guest", f"after restart: {where}", [c.shot("2_restart", focus="profile.guest")])
