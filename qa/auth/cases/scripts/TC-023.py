import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Send again is locked with a countdown when the code screen opens",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC5 — resend locked for 60 s (unlock after 60 s + new code: irbis-app reset.test.tsx, irbis-api auth.rules.spec.ts)",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-VERIFIED user",
  "Reset code screen just opened"
 ],
 "steps": [
  "Open the reset code screen and read the resend row"
 ],
 "expected": [
  "auth.resend-countdown 'Send again in …' shown, no auth.resend — UI tree + screenshot"
 ],
 "focus": "auth.resend-row",
 "caption": {
  "expected": "resend lock"
 }
}


def run(c):
    u = make_user("rsd", phone=phone(15), verified=True)
    c.pre(f"QA-VERIFIED {u['username']}")
    c.checkpoint("forgot screen open", open_forgot(), "no auth.forgot")
    fill("auth.username", u["username"]); tap_submit()
    c.checkpoint("code screen", wait("auth.reset", 10, exact=True), "no auth.reset")
    c.step(1, "Read the resend row")
    locked = has("auth.resend-countdown", exact=True) and not has("auth.resend", exact=True)
    c.result(1, locked, f"locked with countdown: {locked}", [c.shot("1_start", focus="auth.resend-row")])
