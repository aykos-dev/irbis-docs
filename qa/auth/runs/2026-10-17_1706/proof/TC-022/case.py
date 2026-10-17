import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Three wrong codes void the code; the right code is then refused",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC5 — 3 wrong tries void the code",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-VERIFIED user",
  "Reset code screen open with a code requested"
 ],
 "steps": [
  "Enter a wrong 6-digit code with a valid new password, submit — three times",
  "Enter the RIGHT code and submit"
 ],
 "expected": [
  "Wrong tries 1 and 2: 'That code isn't right.' — UI tree",
  "After the third wrong try the message is 'Too many wrong tries. Send a new code.' (on the 3rd or on the next submit) — UI tree + screenshot",
  "The right code is refused: no password_reset_done event, still on auth.reset — event log + UI tree"
 ],
 "focus": "auth.reset",
 "caption": {
  "expected": "code voided"
 }
}


def run(c):
    u = make_user("w3", phone=phone(14), verified=True)
    before = len(sms_codes(u["id"]))
    c.pre(f"QA-VERIFIED {u['username']}")
    c.checkpoint("forgot screen open", open_forgot(), "no auth.forgot")
    fill("auth.username", u["username"]); tap_submit()
    c.checkpoint("code screen", wait("auth.reset", 10, exact=True), "no auth.reset")
    code = wait_new_code(u["id"], before, 10)
    c.checkpoint("code in API log", bool(code), "no new SMS line")
    wrong = "000000" if code != "000000" else "111111"
    msgs = []
    for i in range(3):
        c.step(i + 1, f"Wrong code try {i + 1}")
        fill("auth.code", wrong, clear=True)
        if i == 0:
            fill("auth.new-password", PW2); hide_kb()
        tap_submit()
        time.sleep(2)
        msgs.append(field_text("auth.error") or field_text("auth.code-error") or "")
    c.result(1, all("That code isn't right." in m for m in msgs[:2]), f"messages: {msgs}")
    c.step(4, "Right code")
    t0 = c.mark()
    fill("auth.code", code, clear=True); tap_submit(); time.sleep(2)
    m4 = field_text("auth.error") or field_text("auth.code-error") or ""
    void = "Too many wrong tries. Send a new code." in (msgs[2], m4)
    c.result(2, void, f"third: {msgs[2]!r}; after right code: {m4!r}", [c.shot("4_void", focus="auth.reset")])
    none = c.no_event("password_reset_done", t0, 3)
    c.result(3, none and has("auth.reset", exact=True), f"no reset event={none}")
