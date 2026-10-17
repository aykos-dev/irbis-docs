import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Fifth wrong password locks the username for 15 minutes and says how long",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC4 — 5 wrong → 15-min lock with minutes",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-USER exists",
  "Guest, log-in screen open"
 ],
 "steps": [
  "Submit the QA-USER with 5 wrong passwords in the app",
  "Submit again with the RIGHT password",
  "Call the API log-in with the right password",
  "Log in as a different QA user through the API"
 ],
 "expected": [
  "Attempts 1–4 show 'Username or password is wrong' — UI tree",
  "After the 5th wrong password the next attempt (right password) shows 'Too many tries. Try again in 15 minutes.' (14 or 15 minutes) — UI tree + screenshot",
  "API log-in for the locked name → 423 ACCOUNT_LOCKED with retryAfterSec between 840 and 900 — API response",
  "A different username is not locked (API 200) — API response"
 ],
 "focus": "auth.error",
 "caption": {
  "expected": "lock message with minutes"
 }
}


def run(c):
    u = make_user("l5"); other = make_user("l5o")
    c.pre(f"QA-USER {u['username']} (+ {other['username']})")
    c.checkpoint("log-in screen open", open_login(), "no auth.login")
    msgs = []
    c.step(1, "Five wrong passwords")
    for i in range(5):
        fill("auth.username", u["username"], clear=True); fill("auth.password", PW2, clear=True); tap_submit()
        time.sleep(2)
        msgs.append(field_text("auth.error"))
    generic = "Username or password is wrong"
    c.result(1, all(m == generic for m in msgs[:4]), f"first four messages: {msgs[:4]}; fifth: {msgs[4]!r}", [c.shot("1_fifth", focus="auth.error")])
    c.step(2, "Right password after the lock")
    fill("auth.password", PW, clear=True); tap_submit()
    time.sleep(2)
    m = field_text("auth.error") or ""
    mm = re.search(r"Try again in (\d+) minutes?", m)
    mins = int(mm.group(1)) if mm else None
    c.result(2, m.startswith("Too many tries.") and mins in (14, 15), f"message={m!r}", [c.shot("2_locked", focus="auth.error")])
    st, d, _ = api("POST", "/v1/auth/log-in", {"username": u["username"], "password": PW})
    ra = d.get("retryAfterSec")
    c.result(3, st == 423 and d.get("code") == "ACCOUNT_LOCKED" and isinstance(ra, int) and 840 <= ra <= 900, f"status={st}, code={d.get('code')}, retryAfterSec={ra}")
    st2, _, _ = api("POST", "/v1/auth/log-in", {"username": other["username"], "password": PW})
    c.result(4, st2 == 200, f"other user → {st2}")
