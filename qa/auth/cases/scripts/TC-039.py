import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "VERIFY: after the access token expired the app refreshes silently and stays signed in",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC9 — refresh once on 401 and retry",
 "env": "Android · auto (adb)",
 "precondition": [
  "ARM case done ≥ 15.5 min ago; the device was not used for other sign-ins"
 ],
 "steps": [
  "Wait until 15.5 min after the arm (script waits ≤ 8 min, else Blocked)",
  "Cold start the app → open Profile"
 ],
 "expected": [
  "Still signed in as the armed user, no 'session has ended' toast — UI tree + screenshot",
  "DB: the user's refresh tokens grew past the arm count and one is marked replaced (rotated by the refresh) — DB"
 ],
 "focus": "profile.account",
 "caption": {
  "expected": "still signed in"
 }
}


def run(c):
    a = json.load(open(os.path.join(CACHE_DIR, "auth_arm.json")))
    c.pre(f"armed user {a['username']}")
    need = a["t0"] + 15.5 * 60 - time.time()
    c.checkpoint("≥ 15.5 min since the arm (else run again later)", need <= 480, f"{int(need)} s still to wait")
    if need > 0:
        time.sleep(need)
    c.step(1, "Cold start, open Profile")
    relaunch()
    saw_toast = False
    end = time.time() + 8
    while time.time() < end:
        saw_toast = saw_toast or has("Your session has ended")
        time.sleep(0.3)
    where = goto_profile()
    wait("profile.username", 8, exact=True)
    shot = c.shot("1_still_in", focus="profile.account")
    c.result(1, where == "profile.account" and field_text("profile.username") == a["username"] and not saw_toast, f"profile={where}, toast seen={saw_toast}", [shot])
    rows = int(sql(f"select count(*) from refresh_tokens where user_id='{a['id']}'") or 0)
    rep = int(sql(f"select count(*) from refresh_tokens where user_id='{a['id']}' and replaced_by_id is not null") or 0)
    c.result(2, rows > a["rows"] and rep >= 1, f"rows {a['rows']} → {rows}, rotated rows: {rep}")
