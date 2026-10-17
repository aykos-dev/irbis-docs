import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Per-IP limit stops trying many usernames",
 "priority": "P2",
 "group": "Supplementary",
 "requirement": "AC4 — per-IP limit across usernames",
 "env": "API (HTTP)",
 "precondition": [
  "API up"
 ],
 "steps": [
  "Send 30 log-in attempts for 30 different unknown usernames within a few seconds",
  "Wait 65 s for the window to clear"
 ],
 "expected": [
  "Early attempts return 401 INVALID_CREDENTIALS — API response",
  "Later attempts are refused with 429 RATE_LIMITED or 423 ACCOUNT_LOCKED before all 30 are tried — API response",
  "After 65 s an attempt returns 401 again (limit is a window, not permanent) — API response"
 ],
 "focus": "",
 "caption": {
  "expected": ""
 }
}


def run(c):
    c.pre("API up; QA IP window clean")
    time.sleep(3)
    seq = []
    c.step(1, "30 attempts, distinct usernames")
    for i in range(30):
        st, d, _ = api("POST", "/v1/auth/log-in", {"username": f"qa_ip_{int(time.time())%10**6}_{i}", "password": PW2})
        seq.append((st, d.get("code")))
    c.result(1, seq[0] == (401, "INVALID_CREDENTIALS") and seq[1] == (401, "INVALID_CREDENTIALS"), f"first: {seq[:2]}")
    limited = [x for x in seq if x[1] in ("RATE_LIMITED", "ACCOUNT_LOCKED") or x[0] in (423, 429)]
    c.result(2, bool(limited), f"{len(limited)} of 30 refused; first refusal at index {seq.index(limited[0]) if limited else None}")
    c.step(2, "Wait for the window to clear")
    time.sleep(65)
    st, d, _ = api("POST", "/v1/auth/log-in", {"username": uname("ipafter"), "password": PW2})
    c.result(3, st == 401, f"after 65 s → {st} {d.get('code')}")
