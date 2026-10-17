import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Reserved and taken usernames refused; live availability moves pristine → validating → success",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC3 — reserved, case-insensitive unique, live availability",
 "env": "Android · auto (adb)",
 "precondition": [
  "Sign-up screen open",
  "QA-USER exists (created by API, lowercase name)"
 ],
 "steps": [
  "Before typing, read the status line (pristine)",
  "Type a free name and read the status immediately and after 3 s",
  "Type 'admin', then 'Irbis', then 'OFFICIAL'",
  "Type the QA-USER's name in UPPER CASE"
 ],
 "expected": [
  "Pristine: hint text '3–20 letters, numbers, dot or underscore.' shown, no error — UI tree",
  "Free name: 'Checking if the name is free' while validating (seen within 1.5 s of typing, else needs eyes) then '<name> is free' — UI tree",
  "'admin', 'Irbis' and 'OFFICIAL' each: error 'That name is reserved. Pick another one.' — UI tree",
  "Upper-case copy of an existing name: error 'That username is taken.' (case-insensitive) — UI tree"
 ],
 "focus": "auth.username",
 "caption": {
  "expected": "reserved / taken / live states"
 }
}


def run(c):
    def feedback(text, wait_s=5):
        fill("auth.username", text, clear=True)
        tap("auth.password", exact=True)
        keys = [f"{text} is free", "Use 3–20 characters.", "Only letters, numbers, dot and underscore.", "A dot can't be first or last.",
                "That username is taken.", "That name is reserved. Pick another one.", "That username isn't allowed."]
        hit = wait_any(keys, wait_s)
        return hit, field_text("auth.username")

    import random
    u = make_user("tkn")
    c.pre(f"QA-USER {u['username']} exists")
    c.checkpoint("sign-up screen open", open_signup(), "no auth.signup")
    c.step(1, "Read the status line before typing")
    p = any(t.startswith("3–20 letters") for t in texts()) and not has("Use 3–20 characters.")
    c.result(1, p, f"pristine hint shown: {p}", [c.shot("1_pristine", focus="auth.username")])
    name = f"q{random.randint(100000, 999999)}"
    c.step(2, "Type a free name")
    tap("auth.username", exact=True); type_text(name)
    seen = wait("Checking if the name is free", 1.5)
    done = wait(f"{name} is free", 5)
    c.result(2, (True if seen and done else (None if done else False)), f"validating seen={seen}, success={done}", [c.shot("2_free", focus="auth.username")])
    res = []
    for i, nm in enumerate(["admin", "Irbis", "OFFICIAL"]):
        h, v = feedback(nm)
        res.append(h)
    c.step(3, "Type admin / Irbis / OFFICIAL")
    c.result(3, all(h == "That name is reserved. Pick another one." for h in res), f"statuses {res}", [c.shot("3_reserved", focus="auth.username")])
    c.step(4, "Type the existing name in upper case")
    h, v = feedback(u["username"].upper())
    c.result(4, h == "That username is taken.", f"status={h}", [c.shot("4_taken", focus="auth.username")])
