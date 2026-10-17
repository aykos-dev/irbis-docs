import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa  (shared points/accounts/helpers of this feature)
except ImportError:
    pass

META = {
 "title": "API unreachable shows an error with Retry, and Retry recovers",
 "group": "Core",
 "priority": "P1",
 "env": "Android · auto (adb) · resources: API-GONE, API-UP",
 "plan": "Test_health.md",
 "anchor": "tc-003--p1--api-unreachable-shows-an-error-with-retry-and-retry-recovers",
 "source": "AC3",
 "expected": [
  "After step 2: plain-language error message and `health.retry` visible; no raw status code or stack — screenshot",
  "After step 3: the card shows \"API is up\" again — screenshot",
  "Event `health_checked` { status: \"ok\" } after the Retry tap — event log"
 ],
 "caption": {
  "expected": "After step 2: plain-language error message and `health.retry` visible; no raw st"
 },
 "plan_hash": "6e3bd62452"
}


def run(c):
    c.pre('API-UP; app open on the Status screen')
    c.step(1, "Remove the port forward and cold start")
    reverse(False)
    try:
        t0 = c.mark()
        relaunch()
        c.checkpoint("API unreachable from the phone", c.no_event("health_checked", t0, 15), "health_checked arrived")
        c.step(2, "Wait for the error state")
        err = wait("health.retry", 30, exact=True)
        shot = c.shot("2_error")
        raw = any(re.search(r"\b(5\d\d|4\d\d)\b|Error:|Exception", t) for t in card_texts())
        c.result(1, err and not raw, f"retry shown: {err}; texts: {card_texts()[:8]}", [shot])
        c.step(3, "Restore the forward and tap Retry")
        reverse(True)
        t1 = c.mark()
        tap("health.retry", exact=True)
        up = wait("API is up", 10)
        shot2 = c.shot("3_recovered")
        c.result(2, up, "API is up after Retry" if up else f"texts: {card_texts()[:8]}", [shot2])
        ev = c.wait_event("health_checked", t1, 10)
        c.result(3, bool(ev and ev.get("status") == "ok"), f"event: {ev}")
    finally:
        reverse(True)
