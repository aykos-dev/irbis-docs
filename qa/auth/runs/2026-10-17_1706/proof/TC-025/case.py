import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "At most 5 reset codes per account per day",
 "priority": "P2",
 "group": "Supplementary",
 "requirement": "AC5 — max 5 codes/day, identical response",
 "env": "API (HTTP)",
 "precondition": [
  "QA-VERIFIED user"
 ],
 "steps": [
  "POST /v1/auth/password/forgot six times, aging earlier codes by 2 minutes between calls so the 60 s resend gap is not the limit"
 ],
 "expected": [
  "Every call returns 202 {resendAfterSec: 60} — API response",
  "Exactly 5 new codes in the SMS log; the 6th call sends none — API log"
 ],
 "focus": "",
 "caption": {
  "expected": ""
 }
}


def run(c):
    u = make_user("cap", phone=phone(17), verified=True)
    c.pre(f"QA-VERIFIED {u['username']}")
    base = len(sms_codes(u["id"]))
    res = []
    c.step(1, "Six forgot calls")
    for i in range(6):
        st, d, _ = api("POST", "/v1/auth/password/forgot", {"username": u["username"]})
        res.append((st, d.get("resendAfterSec")))
        time.sleep(1.2)
        sql(f"update sms_codes set created_at = created_at - interval '2 minutes' where user_id='{u['id']}' and purpose='password_reset'")
    c.result(1, all(r == (202, 60) for r in res), f"{res}")
    got = len(sms_codes(u["id"])) - base
    c.result(2, got == 5, f"new codes after 6 requests: {got}")
