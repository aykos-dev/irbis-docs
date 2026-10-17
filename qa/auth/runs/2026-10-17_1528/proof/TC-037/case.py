import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Refresh failure after a 401 returns the app to guest with a toast",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC9 — 401 → refresh fails → guest + toast",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-USER signed in on the device"
 ],
 "steps": [
  "Delete the signed-in QA user's tokens and row on the local DB (the access token stays cryptographically valid, the account is gone → 401, refresh refused)",
  "Cold start the app"
 ],
 "expected": [
  "Toast 'Your session has ended. You're browsing as a guest.' within 15 s of the start — UI tree + screenshot",
  "The Profile tab shows the guest Profile and no account nodes — UI tree"
 ],
 "focus": "profile.guest",
 "caption": {
  "expected": "guest after failed refresh"
 }
}


def run(c):
    u = make_user("rf")
    c.pre(f"QA-USER {u['username']} signed in")
    c.checkpoint("signed in", open_signed_in(u), "profile.account not shown")
    c.step(1, "Remove the account and its tokens on the local DB")
    for t in ("refresh_tokens", "sms_codes", "login_attempts"):
        col = "user_id" if t != "login_attempts" else None
        if col:
            sql(f"delete from {t} where user_id='{u['id']}'")
    sql(f"delete from users where id='{u['id']}'")
    c.checkpoint("user removed", sql(f"select count(*) from users where id='{u['id']}'") == "0", "row still present")
    c.step(2, "Cold start")
    relaunch()
    seen, end = False, time.time() + 20
    shot = None
    while time.time() < end and not seen:
        seen = has("Your session has ended")
        if seen:
            shot = c.shot("2_toast")
        time.sleep(0.2)
    c.result(1, seen, f"toast seen={seen}", [shot] if shot else [c.shot("2_no_toast")])
    goto_profile()
    c.result(2, has("profile.guest", exact=True) and not has("profile.username", exact=True), "guest Profile", [c.shot("3_guest", focus="profile.guest")])
