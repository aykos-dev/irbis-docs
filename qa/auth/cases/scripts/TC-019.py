import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Forgot password shows the same code screen for unknown, phoneless and verified accounts",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC5 — identical response; code only when a verified phone exists",
 "env": "Android · auto (adb)",
 "precondition": [
  "Unknown name; QA-USER without phone; QA-VERIFIED user"
 ],
 "steps": [
  "Forgot password → submit an unknown username → read the code screen",
  "Same for the no-phone QA-USER",
  "Same for the QA-VERIFIED user",
  "Compare screens and the API log's SMS lines"
 ],
 "expected": [
  "All three submissions land on auth.reset with identical texts (countdown digits ignored) — UI tree",
  "Event password_reset_requested for each submission — event log",
  "SMS log: no new line for the unknown and no-phone names; exactly one new 6-digit code for the verified user — API log"
 ],
 "focus": "auth.reset",
 "caption": {
  "expected": "same code screen"
 }
}


def run(c):
    nophone = make_user("fnp"); ver = make_user("fv", phone=phone(11), verified=True)
    total = lambda: sum(1 for _ in open(API_LOG, errors="replace") if "SMS code for user" in _)
    def submit(name):
        c.checkpoint("forgot screen open", open_forgot(), "no auth.forgot")
        t0 = c.mark()
        fill("auth.username", name); tap_submit()
        ok = wait("auth.reset", 10, exact=True)
        time.sleep(1)
        tx = [re.sub(r"\d+", "#", t) for t in texts() if name not in t]
        return ok, tx, c.wait_event("password_reset_requested", t0, 5), c.shot(f"s_{name[:8]}", focus="auth.reset")
    c.pre(f"unknown, no-phone {nophone['username']}, verified {ver['username']}")
    base_total, base_ver = total(), len(sms_codes(ver["id"]))
    c.step(1, "Unknown username")
    a = submit(uname("ghost"))
    c.step(2, "No-phone account")
    b = submit(nophone["username"])
    mid_total = total()
    c.step(3, "Verified-phone account")
    d = submit(ver["username"])
    code = wait_new_code(ver["id"], base_ver, 8)
    c.result(1, a[0] and b[0] and d[0] and a[1] == b[1] == d[1], f"on reset: {a[0]},{b[0]},{d[0]}; same texts: {a[1] == b[1] == d[1]}", [a[3], b[3], d[3]])
    c.result(2, bool(a[2] and b[2] and d[2]), f"events {bool(a[2])},{bool(b[2])},{bool(d[2])}")
    c.result(3, mid_total == base_total and bool(code) and re.fullmatch(r"\d{6}", code) is not None and len(sms_codes(ver["id"])) == base_ver + 1,
             f"codes after unknown+no-phone: {mid_total - base_total}; verified got a 6-digit code: {bool(code)}")
