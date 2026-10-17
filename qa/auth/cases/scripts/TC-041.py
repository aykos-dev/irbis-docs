import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "A blocked user cannot log in and sees the block reason",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC11 — blocked account at log-in",
 "env": "Android · auto (adb)",
 "precondition": [
  "QA-BLOCKED user (blocked on the local DB with reason spam)",
  "Guest, log-in screen open"
 ],
 "steps": [
  "Log in with the blocked QA user's correct credentials"
 ],
 "expected": [
  "auth.blocked shows 'Your account is blocked' and 'Reason: Spam or advertising' — UI tree + screenshot",
  "Event account_blocked_shown — event log",
  "No session: after closing the screen the Profile tab is the guest Profile — UI tree"
 ],
 "focus": "auth.blocked",
 "caption": {
  "expected": "blocked message"
 }
}


def run(c):
    u = make_user("blk")
    sql(f"update users set blocked_at=now(), block_reason_code='spam' where id='{u['id']}'")
    c.pre(f"QA-BLOCKED {u['username']} (spam)")
    c.checkpoint("blocked on the DB", sql(f"select block_reason_code from users where id='{u['id']}'") == "spam", "block not set")
    c.checkpoint("log-in screen open", open_login(), "no auth.login")
    c.step(1, "Log in")
    t0 = c.mark()
    fill("auth.username", u["username"]); fill("auth.password", PW); tap_submit()
    shown = wait("auth.blocked", 10, exact=True)
    shot = c.shot("1_blocked", focus="auth.blocked")
    c.result(1, shown and has("Your account is blocked") and has("Reason: Spam or advertising"), f"blocked card={shown}, texts={[t for t in texts() if 'block' in t.lower() or 'Reason' in t]}", [shot])
    ev = c.wait_event("account_blocked_shown", t0, 5)
    c.result(2, bool(ev), f"event={bool(ev)}")
    c.step(2, "Close the log-in screen")
    tap("auth.continue-guest", exact=True)
    c.result(3, wait("profile.guest", 8, exact=True), "guest Profile after closing", [c.shot("2_guest", focus="profile.guest")])
