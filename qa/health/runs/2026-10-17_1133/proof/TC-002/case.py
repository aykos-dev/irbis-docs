import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Database down: DB chip Not-now, API chip stays up, no error",
 "priority": "P1",
 "group": "Core",
 "requirement": "AC2 + AC3 (Q4) — degraded is data, API chip stays Go",
 "env": "Android · auto (adb + docker)",
 "precondition": [
  "Status screen showing ok"
 ],
 "steps": [
  "docker compose stop db → check: /health says db down",
  "Pull to refresh"
 ],
 "expected": [
  "health.db-chip 'Database is down' (Not-now) and health.api-chip 'API is up' (Go) — UI tree",
  "No error state and no health.retry — UI tree",
  "Event health_checked {status: degraded, db: down} — event log"
 ],
 "postcondition": "docker compose start db",
 "focus": "health.status-card",
 "caption": {
  "expected": "API up, DB down, no error"
 }
}


def run(c):
    c.pre("App open on the Status screen showing ok (TC-001's postcondition)")
    reverse(True)
    relaunch()
    c.checkpoint("status ok first", wait("API is up", 15), card_texts()[:6])
    c.step(1, "Stop the database container")
    body = db(False)
    c.checkpoint("API reports db down", bool(body and body.get("db") == "down"), body)
    try:
        t0 = c.mark()
        c.step(2, "Pull to refresh")
        w, h = screen_size()
        swipe(w // 2, int(h * 0.3), w // 2, int(h * 0.75), 400)
        seen = wait("Database is down", 8)
        shot = c.shot("2_degraded")
        c.observe(f"db chip down: {seen}")
        c.result(1, seen and has("health.api-chip", exact=True),
                 f"db down shown: {seen}; texts: {card_texts()[:8]}", [shot])
        no_err = not has("health.retry", exact=True) and not has("Can't check the status")
        c.result(2, no_err, "no error state / Retry" if no_err else "error state or Retry shown", [shot])
        ev = c.wait_event("health_checked", t0, 8, pred=lambda p: p.get("db") == "down")
        c.result(3, bool(ev and ev.get("status") == "degraded"), f"event: {ev}")
    finally:
        c.setup("Restore: start the database container")
        db(True)
