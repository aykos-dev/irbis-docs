import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Terms must be accepted to create an account",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC3 — terms checkbox required",
 "env": "Android · auto (adb)",
 "precondition": [
  "Sign-up screen open",
  "Valid free username and password typed"
 ],
 "steps": [
  "Fill username and password, leave terms unticked, submit"
 ],
 "expected": [
  "Error 'Please accept the Terms and Privacy Policy.' — UI tree + screenshot",
  "No account created: DB count 0 and no signed_up event in 4 s — DB + event log"
 ],
 "focus": "auth.terms",
 "caption": {
  "expected": "terms error"
 }
}


def run(c):
    import random
    name = f"q{random.randint(100000, 999999)}"
    c.pre(f"free username {name}")
    c.checkpoint("sign-up screen open", open_signup(), "no auth.signup")
    c.step(1, "Fill username and password, no terms, submit")
    fill("auth.username", name); time.sleep(1.5)
    fill("auth.password", PW)
    t0 = c.mark()
    tap_submit()
    ok = wait("Please accept the Terms and Privacy Policy.", 6)
    shot = c.shot("1_terms", focus="auth.terms")
    c.result(1, ok, f"error shown={ok}", [shot])
    none = c.no_event("signed_up", t0, 4)
    c.result(2, none and sql(f"select count(*) from users where username='{name}'") == "0", f"no event={none}", [shot])
