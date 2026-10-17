import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Forgot password screen shows the support path for accounts without a phone",
 "priority": "P2",
 "group": "Supplementary",
 "requirement": "AC5 — A4 support path",
 "env": "Android · auto (adb)",
 "precondition": [
  "Guest, Forgot password open"
 ],
 "steps": [
  "Log in screen → Forgot password? → check: auth.forgot"
 ],
 "expected": [
  "Title 'Forgot your password?' and the card 'No recovery phone on the account?' (auth.support-note) with the support text — UI tree + screenshot"
 ],
 "focus": "auth.support-note",
 "caption": {
  "expected": "support note"
 }
}


def run(c):
    c.pre("guest")
    c.checkpoint("forgot screen open", open_forgot(), "no auth.forgot")
    shot = c.shot("1_forgot", focus="auth.support-note")
    ok = has("Forgot your password?") and has("auth.support-note", exact=True) and has("No recovery phone on the account?")
    c.result(1, ok, f"title/note present: {ok}", [shot])
