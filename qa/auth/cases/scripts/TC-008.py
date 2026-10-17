import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Password rules in the form: 5 chars, 65 chars, equal to username, common password",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC3 — password 6–64, ≠ username, not common (UI)",
 "env": "Android · auto (adb)",
 "precondition": [
  "Sign-up screen open",
  "A free username typed"
 ],
 "steps": [
  "Type a free username",
  "Type a 5-char password → blur",
  "Type a 65-char password → blur",
  "Type the username as the password → blur",
  "Type 'password', tick terms, submit"
 ],
 "expected": [
  "5 chars: error 'Use 6–64 characters.' under the password — UI tree",
  "65 chars: error 'Use 6–64 characters.' or the field stops at 64 — UI tree",
  "Password equal to the username: error 'The password can't be your username.' — UI tree",
  "Common password 'password': 'That password is too easy to guess. Try another one.' after submit, no account created — UI tree + DB row count 0 + no signed_up event"
 ],
 "focus": "auth.password",
 "caption": {
  "expected": "password errors"
 }
}


def run(c):
    import random
    name = f"q{random.randint(100000, 999999)}"
    c.pre(f"free username {name}")
    c.checkpoint("sign-up screen open", open_signup(), "no auth.signup")
    fill("auth.username", name)
    time.sleep(1.5)
    def pw_status(pw, want_text):
        fill("auth.password", pw, clear=True)
        tap("auth.phone", exact=True)
        wait(want_text, 3)
        return has(want_text), field_text("auth.password")
    c.step(1, "5-char password")
    ok, v = pw_status("ab12c", "Use 6–64 characters.")
    c.result(1, ok, f"error shown={ok}", [c.shot("1_five", focus="auth.password")])
    c.step(2, "65-char password")
    ok, v = pw_status("A1" + "x" * 63, "Use 6–64 characters.")
    capped = v is not None and len(v) <= 64
    c.result(2, ok or capped, f"error={ok}, field length={len(v) if v else None}", [c.shot("2_sixtyfive", focus="auth.password")])
    c.step(3, "Password equals the username")
    ok, v = pw_status(name, "The password can't be your username.")
    c.result(3, ok, f"error shown={ok}", [c.shot("3_same", focus="auth.password")])
    c.step(4, "Common password 'password', terms ticked, submit")
    fill("auth.password", "password", clear=True)
    hide_kb()
    tap("auth.terms", exact=True)
    t0 = c.mark()
    tap_submit()
    weak = wait("That password is too easy to guess. Try another one.", 8)
    gone = sql(f"select count(*) from users where username='{name}'") == "0"
    ev = c.wait_event("signed_up", t0, 3)
    c.result(4, weak and gone and not ev, f"weak message={weak}, no account={gone}, signed_up event={bool(ev)}", [c.shot("4_weak", focus="auth.password")])
