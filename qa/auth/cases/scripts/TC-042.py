import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "A signed-in user who gets blocked is signed out on the next request with the same message",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC11 — blocked while signed in",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-USER signed in on the device"
 ],
 "steps": [
  "Block the user on the local DB (reason harassment)",
  "Cold start the app (next request) and wait up to 20 s"
 ],
 "expected": [
  "The blocked message 'Your account is blocked' with 'Reason: Harassment or hate' (auth.blocked) appears — UI tree + screenshot",
  "The user is signed out: the Profile tab shows the guest Profile — UI tree",
  "Event account_blocked_shown — event log"
 ],
 "focus": "auth.blocked",
 "caption": {
  "expected": "blocked while signed in"
 }
}


def run(c):
    u = make_user("blk2")
    c.pre(f"QA-USER {u['username']} signed in")
    c.checkpoint("signed in", open_signed_in(u), "profile.account not shown")
    c.step(1, "Block the user on the local DB")
    sql(f"update users set blocked_at=now(), block_reason_code='harassment' where id='{u['id']}'")
    c.checkpoint("blocked on the DB", sql(f"select block_reason_code from users where id='{u['id']}'") == "harassment", "block not set")
    c.step(2, "Cold start")
    t0 = c.mark()
    relaunch()
    shown = wait("auth.blocked", 20, exact=True)
    shot = c.shot("2_blocked", focus="auth.blocked") if shown else c.shot("2_none")
    c.result(1, shown and has("Your account is blocked") and has("Reason: Harassment or hate"), f"blocked card={shown}, texts={[t for t in texts() if 'block' in t.lower() or 'Reason' in t]}", [shot])
    if shown and has("auth.continue-guest", exact=True):
        tap("auth.continue-guest", exact=True)
    elif not shown:
        pass
    else:
        back()
    wait("nav.tab-profile", 10, exact=True)
    where = goto_profile()
    c.result(2, where == "profile.guest", f"profile after: {where}", [c.shot("3_profile", focus="profile.guest")])
    ev = c.wait_event("account_blocked_shown", t0, 3)
    c.result(3, bool(ev), f"event={bool(ev)}")
