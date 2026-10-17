import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Wrong password and unknown username give the same generic message",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC4 — one generic credential error",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-USER exists",
  "Guest, log-in screen open"
 ],
 "steps": [
  "Log in with the QA-USER name and a wrong password",
  "Log in with an unknown username and any password"
 ],
 "expected": [
  "Wrong password: auth.error 'Username or password is wrong' — UI tree + screenshot",
  "Unknown username: the identical text 'Username or password is wrong' — UI tree",
  "Event log_in_failed fired for both attempts — event log"
 ],
 "focus": "auth.error",
 "caption": {
  "expected": "generic credential error"
 }
}


def run(c):
    u = make_user("gen")
    c.pre(f"QA-USER {u['username']}")
    c.checkpoint("log-in screen open", open_login(), "no auth.login")
    msg = "Username or password is wrong"
    t0 = c.mark()
    c.step(1, "Wrong password")
    fill("auth.username", u["username"]); fill("auth.password", PW2); tap_submit()
    wait("auth.error", 8, exact=True)
    e1 = field_text("auth.error")
    s1 = c.shot("1_wrongpw", focus="auth.error")
    c.result(1, e1 == msg, f"auth.error={e1!r}", [s1])
    c.step(2, "Unknown username")
    fill("auth.username", uname("nobody"), clear=True); fill("auth.password", PW2, clear=True); tap_submit()
    time.sleep(2)
    wait("auth.error", 8, exact=True)
    e2 = field_text("auth.error")
    s2 = c.shot("2_unknown", focus="auth.error")
    c.result(2, e2 == msg and e1 == e2, f"auth.error={e2!r}", [s2])
    n = len(events().since(t0, "log_in_failed"))
    c.result(3, n >= 2, f"log_in_failed events: {n}")
