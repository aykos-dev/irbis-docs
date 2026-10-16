import os
import sys

FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))           # the bug folder
DOCS = os.path.abspath(os.path.join(FOLDER, *[".."] * 4))                       # irbis-docs
sys.path.insert(0, os.path.join(DOCS, "scripts", "qa", "rec"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drv import *  # noqa: E402,F403
from _feature import api_health, app_locale, card_texts, db, reverse  # noqa: E402

VARIANT = sys.argv[1] if len(sys.argv) > 1 else None   # "retest-YYYY-MM-DD" for a retest
TITLE = "D2 · Status chip runs past the card when its label wraps"

r = Rec(FOLDER, VARIANT)
r.start()
try:
    reverse(True)
    r.step("Setup: API and database running; phone font size 1.15 (this phone's normal setting)")
    font_scale(1.15)
    r.step("Step 1: Set the app language to Russian")
    app_locale("ru")
    r.step("Step 2: Open the app")
    relaunch()
    wait("health.db-chip", 15, exact=True)
    import time; time.sleep(2)
    r.shot("01_ru_status")
    lines = [t for t in card_texts() if t.startswith("База")]
    r.step(f"Observed: the database chip label '{lines[0] if lines else '?'}' wraps to two lines; look at the chip's right end against the card's right border")
    time.sleep(3)
finally:
    r.stop(TITLE)
    app_locale("en")
    font_scale(1.15)
