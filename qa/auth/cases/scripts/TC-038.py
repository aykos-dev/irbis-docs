import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "ARM: sign in on the device and record the time (silent-refresh check)",
 "priority": "P2",
 "group": "Supplementary",
 "requirement": "AC9 — setup for 'refresh once on 401 and retry'",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-USER; guest"
 ],
 "steps": [
  "Log in with a QA-USER through the app and note the time; leave the app signed in"
 ],
 "expected": [
  "Signed in (profile.account) and the arm time + refresh-token row count saved — UI tree + DB"
 ],
 "focus": "profile.account",
 "caption": {
  "expected": "armed"
 }
}


def run(c):
    u = make_user("arm")
    c.pre(f"QA-USER {u['username']}")
    c.checkpoint("signed in", open_signed_in(u), "profile.account not shown")
    n = sql(f"select count(*) from refresh_tokens where user_id='{u['id']}'")
    json.dump({"username": u["username"], "id": u["id"], "t0": time.time(), "rows": int(n)}, open(os.path.join(CACHE_DIR, "auth_arm.json"), "w"))
    c.result(1, has("profile.account", exact=True), f"armed; refresh rows at arm: {n}", [c.shot("1_armed", focus="profile.account")])
