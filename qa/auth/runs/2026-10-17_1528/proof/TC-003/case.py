import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Guest Profile matches the A6 canvas content",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC2 — guest Profile content",
 "env": "Android · auto (adb)",
 "precondition": [
  "Signed out (guest)"
 ],
 "steps": [
  "Open the Profile tab as a guest → check: profile.guest within 15 s"
 ],
 "expected": [
  "Title 'You're exploring as a guest' and the guest body text — UI tree + screenshot",
  "Buttons profile.guest-signup 'Create free account' and profile.guest-login 'Log in' — UI tree",
  "Rows profile.language 'Language' and profile.safety 'Safety & SOS' — UI tree",
  "No account nodes (profile.username, profile.sign-out) — UI tree"
 ],
 "focus": "profile.guest",
 "caption": {
  "expected": "guest Profile"
 }
}


def run(c):
    c.pre("guest state (signed out through the app if needed)")
    c.step(1, "Cold start, open the Profile tab")
    c.checkpoint("guest Profile shown", ensure_guest(), "profile.guest not shown")
    shot = c.shot("1_guest")
    tx = texts()
    c.result(1, "You're exploring as a guest" in tx and any(t.startswith("Make a free account to keep your XP") for t in tx), f"texts: {tx[:6]}", [shot])
    s, l = find("profile.guest-signup", exact=True), find("profile.guest-login", exact=True)
    c.result(2, bool(s and l) and has("Create free account") and has("Log in"), f"signup {bool(s)}, login {bool(l)}", [shot])
    c.result(3, has("profile.language", exact=True) and has("Language") and has("profile.safety", exact=True) and has("Safety & SOS"),
             "Language and Safety rows", [shot])
    c.result(4, not has("profile.username", exact=True) and not has("profile.sign-out", exact=True), "no account nodes", [shot])
