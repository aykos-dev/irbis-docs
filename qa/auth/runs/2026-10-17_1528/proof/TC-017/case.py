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
  "Wait the retryAfterSec the API reports, repeating while it still refuses (burst limit 60 s, then the 15-min failed-log-in window)"
 ],
 "expected": [
  "Early attempts return 401 INVALID_CREDENTIALS — API response",
  "Later attempts are refused with 429 RATE_LIMITED or 423 ACCOUNT_LOCKED before all 30 are tried — API response",
  "After retryAfterSec an attempt returns 401 again (limit is a window, not permanent) — API response"
 ],
 "focus": "",
 "caption": {
  "expected": ""
 }
}


def run(c):
    c.pre("API up; QA IP window clean (run this case LAST: it limits this IP for up to 15 min)")
    st0, d0, _ = api("POST", "/v1/auth/log-in", {"username": uname("ipprobe"), "password": PW2})
    while st0 == 429:
        time.sleep(min(int(d0.get("retryAfterSec") or 30), 960) + 3)
        st0, d0, _ = api("POST", "/v1/auth/log-in", {"username": uname("ipprobe"), "password": PW2})
    c.checkpoint("IP not already limited", st0 == 401, f"probe returned {st0}")
    seq = []
    last = {}
    c.step(1, "30 attempts, distinct usernames")
    for i in range(30):
        st, d, _ = api("POST", "/v1/auth/log-in", {"username": f"qa_ip_{int(time.time())%10**6}_{i}", "password": PW2})
        seq.append((st, d.get("code")))
        if st == 429:
            last = d
    c.result(1, seq[0] == (401, "INVALID_CREDENTIALS") and seq[1] == (401, "INVALID_CREDENTIALS"), f"first: {seq[:2]}")
    limited = [x for x in seq if x[1] in ("RATE_LIMITED", "ACCOUNT_LOCKED") or x[0] in (423, 429)]
    c.result(2, bool(limited), f"{len(limited)} of 30 refused; first refusal at index {seq.index(limited[0]) if limited else None}")
    c.step(2, "Wait for the window to clear")
    wait_s = 0
    for _ in range(3):
        step = int(last.get("retryAfterSec") or 60) + 5
        time.sleep(step)
        wait_s += step
        st, d, h = api("POST", "/v1/auth/log-in", {"username": uname("ipafter"), "password": PW2})
        if st != 429:
            break
        last = d
    c.result(3, st == 401, f"after {wait_s} s → {st} {d.get('code')}")
