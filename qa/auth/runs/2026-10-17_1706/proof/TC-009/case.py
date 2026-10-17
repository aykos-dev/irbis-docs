import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Password bounds through the API: 6 and 64 accepted, 5 and 65 refused",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC3 — password 6–64 BVA at the contract",
 "env": "API (HTTP)",
 "precondition": [
  "API up"
 ],
 "steps": [
  "POST /v1/auth/sign-up with 6-, 64-, 5-, 65-char passwords",
  "POST sign-up with password equal to username and with 'password'"
 ],
 "expected": [
  "6 chars → 201 and 64 chars → 201 — API response status",
  "5 chars and 65 chars → 4xx with code PASSWORD_WEAK or VALIDATION_FAILED — API response",
  "Password = username and 'password' → 4xx PASSWORD_WEAK — API response"
 ],
 "focus": "",
 "caption": {
  "expected": ""
 }
}


def run(c):
    c.pre("API up")
    base = lambda t, pw: {"username": uname(t), "password": pw, "locale": "en", "acceptTerms": True}
    res = {}
    c.step(1, "Sign up with 6- and 64-char passwords")
    for n in (6, 64):
        pw = ("Qz9" + "k" * 100)[:n]
        res[n] = api("POST", "/v1/auth/sign-up", base(f"pw{n}", pw))[0]
        time.sleep(0.5)
    c.result(1, res[6] == 201 and res[64] == 201, f"6→{res[6]}, 64→{res[64]}")
    c.step(2, "Sign up with 5- and 65-char passwords")
    bad = {}
    for n in (5, 65):
        st, d, _ = api("POST", "/v1/auth/sign-up", base(f"pw{n}", ("Qz9" + "k" * 100)[:n]))
        bad[n] = (st, d.get("code"))
        time.sleep(0.5)
    c.result(2, all(400 <= s < 500 and code in ("PASSWORD_WEAK", "VALIDATION_FAILED") for s, code in bad.values()), f"{bad}")
    c.step(3, "Sign up with password = username and 'password'")
    nm = uname("pwsame")
    s1, d1, _ = api("POST", "/v1/auth/sign-up", {"username": nm, "password": nm, "locale": "en", "acceptTerms": True})
    s2, d2, _ = api("POST", "/v1/auth/sign-up", base("pwcommon", "password"))
    c.result(3, s1 == 422 or (400 <= s1 < 500 and d1.get("code") == "PASSWORD_WEAK") and d2.get("code") == "PASSWORD_WEAK",
             f"same-as-username→{s1} {d1.get('code')}, common→{s2} {d2.get('code')}")
