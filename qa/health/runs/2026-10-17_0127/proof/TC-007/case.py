import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa  (shared points/accounts/helpers of this feature)
except ImportError:
    pass

META = {
 "title": "Uzbek copy",
 "group": "Supplementary",
 "priority": "P2",
 "env": "Android · auto (adb) · resources: API-UP",
 "plan": "Test_health.md",
 "anchor": "tc-007--p2--uzbek-copy",
 "source": "AC4",
 "expected": [
  "Every text on the Status screen is Uzbek (Latin), matching `src/shared/i18n/uz` — screenshot"
 ],
 "caption": {
  "expected": "Every text on the Status screen is Uzbek (Latin), matching `src/shared/i18n/uz`"
 },
 "plan_hash": "7ed22be193"
}


def run(c):
    c.pre('API-UP')
    reverse(True)
    c.step(1, "Set the app language to Uzbek and cold start")
    app_locale("uz")
    try:
        relaunch()
        c.checkpoint("app relaunched", wait("health.status-card", 15, exact=True), card_texts()[:6])
        wait("health.api-chip", 8, exact=True)
        time.sleep(1)
        texts = card_texts()
        shot = c.shot("1_uz")
        english = [t for t in texts if t in ("Status", "API is up", "Database is up") or t.startswith("Checked at")]
        c.result(1, not english, f"English texts left: {english}; all: {texts[:10]}", [shot])
    finally:
        app_locale("en")
