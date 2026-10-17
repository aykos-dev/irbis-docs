"""places feature: PLAN (rendered into Test_places.md), SCREENS (standards suite), shared helpers.

API/DB helpers reuse the auth ones (LOCAL dev DB through the db container; throwaway QA users).
Place rows are read-only for the app; cases that need season / hazards / region / a required level / a description
change ONE local row through `set_place()`, and `before_case()` puts every touched row back (backup in ~/.cache/irbis-qa)."""
import importlib.util
import json
import os
import re
import time
import urllib.parse

from drv import PKG, back, deep_link, find, has, mark, nodes, permission, point, relaunch, reset_permission, sh, tap, wait, wait_any, wait_event, wait_gone, no_event, events, distance_m, offset  # noqa: F401
from config import DOCS, QA_ROOT  # noqa: E402,F401

_p = os.path.join(QA_ROOT, "auth", "cases", "scripts", "_feature.py")
_spec = importlib.util.spec_from_file_location("auth_feature", _p)
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)
api, sql, make_user, ensure_guest = A.api, A.sql, A.make_user, A.ensure_guest

TASHKENT = (41.2995, 69.2401)
FINE = "android.permission.ACCESS_FINE_LOCATION"
COARSE = "android.permission.ACCESS_COARSE_LOCATION"
TYPES = ["peak", "lake", "cave", "camping", "trail", "waterfall", "canyon"]
SEED_COUNTS = {"peak": 34, "waterfall": 22, "lake": 11, "cave": 2, "canyon": 2}
LEVEL_NAMES = {1: "Wanderer", 2: "Burrower", 3: "Pathfinder", 4: "Ridge Walker", 5: "Mountain Guardian", 6: "Sky Watcher", 7: "Snow Legend"}
BACKUP = os.path.expanduser("~/.cache/irbis-qa/places_backup.json")
COLS = {"region": "region", "season": "season", "hazards": "hazards", "required_level": "required_level",
        "description_uz": "description_uz", "name_ru": "name_ru", "name_en": "name_en"}


# ---------------- API (Mac side, no token unless given) ----------------
def places(token=None, **q):
    """GET /v1/places → (status, json). List values repeat the key (types=peak&types=lake)."""
    qs = urllib.parse.urlencode({k: v for k, v in q.items() if v is not None}, doseq=True)
    st, d, _ = api("GET", "/v1/places" + ("?" + qs if qs else ""), token=token)
    return st, d


def place(pid, token=None, **q):
    qs = urllib.parse.urlencode({k: v for k, v in q.items() if v is not None})
    st, d, _ = api("GET", f"/v1/places/{pid}" + ("?" + qs if qs else ""), token=token)
    return st, d


def all_places(**q):
    st, d = places(limit=200, **q)
    assert st == 200, f"GET /v1/places → {st}"
    return d["items"]


def pid_of(slug):
    return sql(f"select id from places where slug='{slug}'")


def pick(where, order="elevation_m"):
    """slug of the first LOCAL row matching a SQL condition (e.g. "type='peak' and difficulty=1")."""
    return sql(f"select slug from places where {where} order by {order}, slug limit 1")


def count_where(where):
    return int(sql(f"select count(*) from places where {where}") or 0)


# ---------------- local-DB isolation ----------------
def set_place(slug, **cols):
    """Test isolation on the LOCAL dev DB: change columns of one place (keys of COLS); the original value is saved for
    before_case(). season/hazards take a list of enum names, others a str/int/None."""
    b = json.load(open(BACKUP)) if os.path.exists(BACKUP) else {}
    row = b.setdefault(slug, {})
    for k, v in cols.items():
        col = COLS[k]
        if k not in row:
            row[k] = sql(f"select coalesce({col}::text,'__NULL__') from places where slug='{slug}'")
        if v is None:
            lit = "null"
        elif isinstance(v, list):
            lit = "'{" + ",".join(v) + "}'"
        elif isinstance(v, int):
            lit = str(v)
        else:
            lit = "'" + v.replace("'", "''") + "'"
        sql(f"update places set {col}={lit} where slug='{slug}'")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    json.dump(b, open(BACKUP, "w"))


def restore_places():
    if not os.path.exists(BACKUP):
        return
    for slug, row in json.load(open(BACKUP)).items():
        for k, v in row.items():
            col = COLS[k]
            lit = "null" if v == "__NULL__" else "'" + v.replace("'", "''") + "'"
            sql(f"update places set {col}={lit} where slug='{slug}'")
    os.remove(BACKUP)


def before_case():
    A.before_case()
    restore_places()
    # device isolation: guest, tabs visible, no leftover filter sheet; location permission is set by each case
    deep_link("irbis://debug/onboarding/done")
    time.sleep(1)
    ensure_guest()


# ---------------- device helpers ----------------
def grant_location(on=True):
    for p in (FINE, COARSE):
        permission(p, on)


def mock_at(lat, lng):
    """Mock device position (session.py up --mock must be running)."""
    point(lat, lng)


def open_explore(wait_list=True):
    """Tap the Explore tab; True when the Explore screen (and, by default, the count header) shows."""
    if not wait("nav.tab-explore", 5, exact=True):
        relaunch()  # a permission revoke kills the app: start it again (the debug deep link lands on a screen without tabs)
        wait("nav.tab-explore", 25, exact=True)
    tap("nav.tab-explore", exact=True)
    return wait("explore.screen", 10, exact=True) and (not wait_list or wait("explore.count", 15, exact=True))


def explore_ready(lat=TASHKENT[0], lng=TASHKENT[1], granted=True):
    """Standard start: location granted + mock fix at (lat, lng), then Explore open. Returns True when the list shows."""
    reset_permission(FINE)
    if granted:
        grant_location(True)
        mock_at(lat, lng)
    return open_explore()


def text_of(tid):
    n = find(tid, exact=True)
    return (n["text"] or n["desc"]) if n else None


def screen_text():
    return " | ".join(filter(None, ((n["text"] or n["desc"]) for n in nodes())))


def card_text(slug):
    """All text inside the card node of `slug` (text + desc of the node and of nodes within its bounds)."""
    ns = nodes()
    c = find(f"explore.card.{slug}", exact=True, ns=ns)
    if not c:
        return None
    x1, y1, x2, y2 = c["b"]
    parts = [c["text"], c["desc"]] + [n["text"] or n["desc"] for n in ns if n is not c and x1 <= n["x"] <= x2 and y1 <= n["y"] <= y2]
    return " | ".join(p for p in parts if p)


def count_in_header():
    m = re.search(r"\d+", text_of("explore.count") or "")
    return int(m.group()) if m else None


def apply_filters(types=None, dmin=None, dmax=None, km=None):
    """Open each filter sheet from its chip and apply. `km` None leaves Distance alone; 0 = Any."""
    if types is not None:
        tap("explore.filter.type", exact=True); wait("explore.filter-sheet.type", 5, exact=True)
        for t in types:
            tap(f"explore.filter-option.type-{t}", exact=True)
        tap("explore.filter.apply", exact=True)
    if dmin is not None:
        tap("explore.filter.difficulty", exact=True); wait("explore.filter-sheet.difficulty", 5, exact=True)
        tap(f"explore.filter-option.difficulty-min-{dmin}", exact=True)
        tap(f"explore.filter-option.difficulty-max-{dmax}", exact=True)
        tap("explore.filter.apply", exact=True)
    if km is not None:
        tap("explore.filter.distance", exact=True); wait("explore.filter-sheet.distance", 5, exact=True)
        tap(f"explore.filter-option.distance-{km or 'any'}", exact=True)
        tap("explore.filter.apply", exact=True)
    time.sleep(0.5)


def open_place(slug):
    """From a loaded Explore list: tap the card (scrolls down up to 12 times); True when Place shows."""
    from drv import scroll_down
    for _ in range(12):
        if has(f"explore.card.{slug}", exact=True):
            break
        scroll_down()
    tap(f"explore.card.{slug}", exact=True)
    return wait("place.screen", 10, exact=True)


def open_place_link(slug, extra=""):
    deep_link(f"irbis://place/{pid_of(slug)}{extra}")
    return wait("place.screen", 15, exact=True) and wait("place.name", 10, exact=True)


PLAN = {
    "spec": "features/places.md",
    "resources": [("Android", "emulator pixel-8a (session.py up --mock); devRelease APK uz.irbis.app.dev, device UI English; location via the mock loop"),
                  ("Backend", "irbis-api `npm run start:dev` on :3000, branch feat/places, migration places_init applied, `npm run db:seed` run once (71 places); "
                              "Postgres container `irbis-api-db-1`; `adb reverse tcp:3000 tcp:3000`"),
                  ("Isolation", "`before_case()`: clears login_attempts, restores every place row a case changed through `set_place()` "
                                "(region/season/hazards/required level/description, backup in ~/.cache/irbis-qa), ends onboarding, signs out to guest. "
                                "Each device case sets its own location permission + mock position. AC1 re-seeds the LOCAL dev DB only."),
                  ("Covered elsewhere", "Seed rule unit tests (name/slug/difficulty bands) and API validation matrix: irbis-api tests; "
                                        "TC-002/003/007 re-check them on the live API + DB")],
    "test_data": [("PLACES", "the 71 seeded rows (34 peaks, 22 waterfalls, 11 lakes, 2 caves, 2 canyons); slugs picked by SQL at run time", "LOCAL dev DB"),
                  ("TASHKENT", "41.2995, 69.2401 = API fallback origin and the mock device position unless the case says otherwise", "constant"),
                  ("QA-USER", "throwaway `qa_<case>_<n>` account for the signed-in checks", "API sign-up, LOCAL dev DB")],
    "timers": "The 10 s 'no location fix' fallback (AC6) is a UX timeout, not a security timer: TC-027 waits at most 12 s once. "
              "No lockout / rate-limit / token timers in this feature.",
    "manual": ["Map pins: type colours/icons, cluster counts and a single-pin tap are drawn by the GL canvas (not in the UI tree) — TC-013 is judged on the crop; "
               "pinch-zoom to split a cluster is a two-finger gesture (manual)",
               "Haptics on chip/filter toggles and press states",
               "Real GPS fix and the first-open OS prompt on the Galaxy S25 Ultra (RFCY616LFMX), before release",
               "Waterfall/canyon art and colours are placeholders (Q8) — visual sign-off by the owner when files arrive"],
}

SCREENS = {
    "explore": {"open": lambda c=None: explore_ready(), "root": "explore.screen"},
    "place": {"open": lambda c=None: open_place_link(pick("type='peak' and difficulty=2")), "root": "place.screen"},
}
