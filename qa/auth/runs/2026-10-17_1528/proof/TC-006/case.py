import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Username characters and dot rules",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC3 — username allowed characters, dot at edges",
 "env": "Android · auto (adb)",
 "precondition": [
  "Sign-up screen open"
 ],
 "steps": [
  "Type '.abc' → blur",
  "Type 'abc.' → blur",
  "Type 'ab-cd' → blur",
  "Type 'ab cd' → blur",
  "Type a free name with dot and underscore in the middle → blur"
 ],
 "expected": [
  "'.abc': error 'A dot can't be first or last.' — UI tree",
  "'abc.': error 'A dot can't be first or last.' — UI tree",
  "'ab-cd': error 'Only letters, numbers, dot and underscore.' — UI tree",
  "'ab cd' (space): error 'Only letters, numbers, dot and underscore.' — UI tree",
  "Free name with an inner dot and underscore: '<name> is free', no error — UI tree"
 ],
 "focus": "auth.username",
 "caption": {
  "expected": "character rules"
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
    c.pre("sign-up screen")
    c.checkpoint("sign-up screen open", open_signup(), "no auth.signup")
    dot = "A dot can't be first or last."
    chars = "Only letters, numbers, dot and underscore."
    for i, (txt, want) in enumerate([(".abc", dot), ("abc.", dot), ("ab-cd", chars), ("ab cd", chars)], 1):
        c.step(i, f"Type {txt!r}")
        h, v = feedback(txt)
        c.result(i, h == want, f"status={h}, field={v!r}", [c.shot(f"{i}_rule", focus="auth.username")])
    ok_name = f"q.a_{random.randint(10000, 99999)}"
    c.step(5, f"Type {ok_name!r}")
    h, v = feedback(ok_name)
    c.result(5, h == f"{ok_name} is free", f"status={h}, field={v!r}", [c.shot("5_ok", focus="auth.username")])
