import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Username length boundaries: 2 refused, 3 and 20 accepted, 21 refused",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC3 — username 3–20 BVA",
 "env": "Android · auto (adb)",
 "precondition": [
  "Sign-up screen open",
  "Names qa… are free (checked via username-available)"
 ],
 "steps": [
  "Open Create free account → check: auth.signup",
  "Type a 2-char name, blur → read the field status",
  "Type a 3-char free name",
  "Type a 20-char free name",
  "Type a 21-char name"
 ],
 "expected": [
  "2 chars ('qa'): error 'Use 3–20 characters.' under the field — UI tree + screenshot",
  "3 chars (free): status '<name> is free', no error — UI tree",
  "20 chars (free): status '<name> is free', no error — UI tree",
  "21 chars: error 'Use 3–20 characters.' or the field stops at 20 characters (cannot exceed) — UI tree"
 ],
 "focus": "auth.username",
 "caption": {
  "expected": "username length statuses"
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
        def free_name(n, prefix="q"):
            for _ in range(20):
                s = (prefix + "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(n)))[:n]
                st, d, _ = api("GET", f"/v1/auth/username-available?u={s}")
                if st == 200 and d.get("available"):
                    return s
            raise RuntimeError("no free name found")
        c.step(1, "Type 'qa' (2 chars)")
        h, v = feedback("qa")
        c.result(1, h == "Use 3–20 characters.", f"status={h}, field={v!r}", [c.shot("1_two", focus="auth.username")])
        n3 = free_name(3)
        c.step(2, f"Type a free 3-char name")
        h, v = feedback(n3)
        c.result(2, h == f"{n3} is free", f"status={h}, field={v!r}", [c.shot("2_three", focus="auth.username")])
        n20 = free_name(20)
        c.step(3, "Type a free 20-char name")
        h, v = feedback(n20)
        c.result(3, h == f"{n20} is free", f"status={h}, field={v!r}", [c.shot("3_twenty", focus="auth.username")])
        c.step(4, "Type the 20-char name plus one more character (21)")
        h, v = feedback(n20 + "z")
        capped = v is not None and len(v) == 20
        c.result(4, h == "Use 3–20 characters." or capped, f"status={h}, field length={len(v) if v else None}", [c.shot("4_twentyone", focus="auth.username")])
