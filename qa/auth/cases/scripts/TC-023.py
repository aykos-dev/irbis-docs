import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Send again is locked for 60 seconds, then sends a new code",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC5 — resend unlocks after 60 s",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-VERIFIED user",
  "Reset code screen just opened"
 ],
 "steps": [
  "Open the reset code screen → read countdown at 0 s",
  "At 50 s read again",
  "At 65 s read and tap Send again"
 ],
 "expected": [
  "At 0 s and 50 s: auth.resend-countdown 'Send again in …' shown, no auth.resend — UI tree",
  "At 65 s: auth.resend 'Send again' shown, countdown gone — UI tree + screenshot",
  "Tapping Send again: a new code line in the API log and the note 'A new code is on its way.' — API log + UI tree"
 ],
 "focus": "auth.resend-row",
 "caption": {
  "expected": "resend lock"
 }
}


def run(c):
    u = make_user("rsd", phone=phone(15), verified=True)
    before = len(sms_codes(u["id"]))
    c.pre(f"QA-VERIFIED {u['username']}")
    c.checkpoint("forgot screen open", open_forgot(), "no auth.forgot")
    fill("auth.username", u["username"]); tap_submit()
    t_start = time.time()
    c.checkpoint("code screen", wait("auth.reset", 10, exact=True), "no auth.reset")
    c.step(1, "Read the countdown at ~0 s")
    a = has("auth.resend-countdown", exact=True) and not has("auth.resend", exact=True)
    s0 = c.shot("1_start", focus="auth.resend-row")
    time.sleep(max(0, 50 - (time.time() - t_start)))
    b = has("auth.resend-countdown", exact=True) and not has("auth.resend", exact=True)
    c.step(2, "Read at ~50 s")
    c.result(1, a and b, f"locked at 0 s: {a}, at 50 s: {b}", [s0])
    c.step(3, "Wait to 65 s")
    time.sleep(max(0, 65 - (time.time() - t_start)))
    unlocked = has("auth.resend", exact=True) and not has("auth.resend-countdown", exact=True)
    s1 = c.shot("3_unlocked", focus="auth.resend-row")
    c.result(2, unlocked, f"unlocked at 65 s: {unlocked}", [s1])
    c.step(4, "Tap Send again")
    n_before = len(sms_codes(u["id"]))
    tap("auth.resend", exact=True)
    new = wait_new_code(u["id"], n_before, 8)
    note = wait("A new code is on its way.", 4)
    c.result(3, bool(new) and note, f"new code logged={bool(new)}, note shown={note}", [c.shot("4_resent", focus="auth.reset")])
