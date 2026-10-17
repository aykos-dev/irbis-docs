import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Recovery phone validation: 8 digits refused, 9 accepted, letters not typable",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC3 — optional recovery phone +998 + 9 digits",
 "env": "Android · auto (adb)",
 "precondition": [
  "Sign-up screen open"
 ],
 "steps": [
  "Type 8 digits in the phone field → blur",
  "Replace with 9 digits → blur",
  "Type '9a0b' into the empty field"
 ],
 "expected": [
  "8 digits: error 'Enter 9 digits after +998.' — UI tree",
  "9 digits: no phone error — UI tree",
  "Letters are not accepted: the field keeps digits only — UI tree"
 ],
 "focus": "auth.phone",
 "caption": {
  "expected": "phone field"
 }
}


def run(c):
    c.pre("sign-up screen")
    c.checkpoint("sign-up screen open", open_signup(), "no auth.signup")
    err = "Enter 9 digits after +998."
    c.step(1, "8 digits")
    fill("auth.phone", "90000001")
    tap("auth.username", exact=True)
    ok = wait(err, 3)
    c.result(1, ok, f"error shown={ok}", [c.shot("1_eight", focus="auth.phone")])
    c.step(2, "9 digits")
    fill("auth.phone", "900000011", clear=True)
    tap("auth.username", exact=True)
    time.sleep(1)
    c.result(2, not has(err), f"error shown={has(err)}", [c.shot("2_nine", focus="auth.phone")])
    c.step(3, "Type letters")
    fill("auth.phone", "9a0b", clear=True)
    v = field_text("auth.phone") or ""
    digits_only = re.sub(r"[\s+]", "", v).isdigit() or v == ""
    c.result(3, digits_only and "a" not in v and "b" not in v, f"field now {v!r}", [c.shot("3_letters", focus="auth.phone")])
