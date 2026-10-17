import os
import sys

FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))           # the bug folder
DOCS = os.path.abspath(os.path.join(FOLDER, *[".."] * 4))                       # irbis-docs
sys.path.insert(0, os.path.join(DOCS, "scripts", "qa", "rec"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drv import *  # noqa: E402,F403
from _feature import api_health, app_locale, card_texts, db, reverse  # noqa: E402

VARIANT = sys.argv[1] if len(sys.argv) > 1 else None   # "retest-YYYY-MM-DD" for a retest
TITLE = "D1 · API chip turns red when only the database is down"

r = Rec(FOLDER, VARIANT)
r.start()
try:
    reverse(True)
    db(True)
    r.step("Setup: API and database running; app language English")
    r.step("Step 1: Open the app")
    relaunch()
    wait("API is up", 15)
    r.shot("01_all_up")
    r.step("Step 2: The database stops (API keeps running)")
    body = db(False)
    r.step(f"Setup: the API now reports status={body.get('status') if body else None}, db={body.get('db') if body else None}")
    r.step("Step 3: Pull down to refresh the Status screen")
    w, h = screen_size()
    swipe(w // 2, int(h * 0.3), w // 2, int(h * 0.75), 400)
    wait("health.db-chip", 8, exact=True)
    import time; time.sleep(2)
    r.shot("02_db_down")
    api = "API is up" if has("API is up") else ("API is degraded" if has("API is degraded") else "?")
    dbt = "Database is down" if has("Database is down") else "?"
    r.step(f"Observed: API chip '{api}', database chip '{dbt}'")
    time.sleep(2)
finally:
    r.stop(TITLE)
    db(True)
