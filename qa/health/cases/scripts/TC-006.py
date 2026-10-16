import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa  (shared points/accounts/helpers of this feature)
except ImportError:
    pass

META = {
 "title": "Russian copy",
 "group": "Supplementary",
 "priority": "P2",
 "env": "Android · auto (adb) · resources: API-UP",
 "plan": "Test_health.md",
 "anchor": "tc-006--p2--russian-copy",
 "source": "AC4",
 "expected": [
  "Every text on the Status screen is Russian, matching `src/shared/i18n/ru` — no English left — screenshot",
  "Layout does not clip or truncate any Russian label — screenshot"
 ],
 "caption": {
  "expected": "Every text on the Status screen is Russian, matching `src/shared/i18n/ru`"
 },
 "plan_hash": "b763662730"
}


def run(c):
    c.pre('API-UP')
    reverse(True)
    c.step(1, "Set the app language to Russian and cold start")
    app_locale("ru")
    try:
        relaunch()
        c.checkpoint("app relaunched", wait("health.status-card", 15, exact=True), card_texts()[:6])
        wait("health.api-chip", 8, exact=True)
        time.sleep(1)
        texts = card_texts()
        shot = c.shot("1_ru")
        latin = [t for t in texts if re.search(r"[A-Za-z]{3,}", t) and not re.fullmatch(r"v[\d.]+|IRBIS|Irbis|dev|API.*", t)]
        c.result(1, not latin, f"English-looking texts left: {latin}; all: {texts[:10]}", [shot])
        c.result(2, None, "clipping: judge from the screenshot", [shot])
    finally:
        app_locale("en")
