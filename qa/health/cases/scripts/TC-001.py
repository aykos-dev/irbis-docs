import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Status screen shows API and database up",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC1 — API reachable and DB up shows ok (+AC7 event)",
 "env": "Android · auto (adb)",
 "precondition": [
  "API + DB running",
  "adb reverse tcp:3000"
 ],
 "steps": [
  "Cold start, open irbis://debug/status → check: health.status-card within 15 s"
 ],
 "expected": [
  "health.api-chip 'API is up' and health.db-chip 'Database is up', both Go — UI tree",
  "health.version 'v0.0.1' — UI tree",
  "Event health_checked {status: ok, db: up} — event log"
 ],
 "focus": "health.status-card",
 "caption": {
  "expected": "API is up, Database is up, v0.0.1"
 }
}


def run(c):
    c.pre('API-UP; `adb reverse tcp:3000 tcp:3000` active; phone online')
    reverse(True)
    st, body = api_health()
    c.checkpoint("API up from the Mac", st == 200 and body.get("db") == "up", (st, body))
    t0 = c.mark()
    c.step(1, "Cold start the app and open Status (irbis://debug/status)")
    open_status(c)
    c.checkpoint("status card shown", wait("health.status-card", 10, exact=True), "no health.status-card in 10 s")
    wait("API is up", 8)
    shot = c.shot("1_status")
    ok_chips = has("API is up") and has("Database is up")
    c.result(1, ok_chips, f"texts: {card_texts()[:8]}", [shot])
    c.result(2, has("v0.0.1"), "version v0.0.1 shown" if has("v0.0.1") else f"no v0.0.1 in {card_texts()[:8]}", [shot])
    ev = c.wait_event("health_checked", t0, 10)
    c.result(3, bool(ev and ev.get("status") == "ok" and ev.get("db") == "up"), f"event: {ev}")
