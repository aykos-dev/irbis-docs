"""conditions feature: PLAN (rendered into Test_conditions.md), SCREENS (standards suite), shared helpers.

Everything runs against the LOCAL dev DB. Forecasts are fixtures: `seed()` writes one place_forecasts row (Open-Meteo
daily shape, dates relative to Tashkent today) and recomputes ONLY that place through the admin API (create + end a
throwaway override: AC3 "recomputes that place at once, no refetch"), so no case depends on the live Open-Meteo data.
Run the API with CONDITIONS_JOB_ENABLED=false (see PLAN) so the :05 cron never overwrites a fixture mid-case.
The admin is a throwaway QA user promoted to role admin in the LOCAL DB (no real admin credential is used or printed)."""
import calendar
import datetime as dt
import importlib.util
import json
import os
import time
from zoneinfo import ZoneInfo

from drv import relaunch, has, find, nodes, scroll_down, set_network, sh, wait, wait_any, wait_gone, mark, wait_event, no_event, tap, deep_link  # noqa: F401

from config import QA_ROOT  # noqa: E402

_p = os.path.join(QA_ROOT, "places", "cases", "scripts", "_feature.py")
_spec = importlib.util.spec_from_file_location("places_feature", _p)
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)
api, sql, make_user = P.api, P.sql, P.make_user
pick, pid_of, set_place, text_of, places, all_places = P.pick, P.pid_of, P.set_place, P.text_of, P.places, P.all_places
open_explore, open_place_link, explore_ready, card_text = P.open_explore, P.open_place_link, P.explore_ready, P.card_text

TASHKENT = P.TASHKENT
TZ = ZoneInfo("Asia/Tashkent")
MILD = {"weather_code": 1, "temperature_2m_max": 24, "temperature_2m_min": 12, "wind_speed_10m_max": 10,
        "wind_gusts_10m_max": 18, "precipitation_sum": 0, "precipitation_probability_max": 10, "snowfall_sum": 0}
FIELDS = list(MILD)
CARD_TIDS = ["place.condition", "place.condition-empty", "place.condition-error", "place.condition-offline", "place.condition-skeleton"]


def today():
    return dt.datetime.now(TZ).date()


def window():
    """{'sat': date, 'sun': date} for the coming weekend per AC2: Mon-Fri -> Sat+Sun, Sat -> Sat+Sun, Sun -> Sun only."""
    t = today()
    wd = t.weekday()  # Mon 0 .. Sun 6
    sat = t + dt.timedelta(days=(5 - wd) % 7) if wd != 6 else None
    sun = t + dt.timedelta(days=(6 - wd) % 7)
    return {k: v for k, v in (("sat", sat), ("sun", sun)) if v}


def month_name(m):
    return calendar.month_name[(m - 1) % 12 + 1]


# ---------------- admin API ----------------
_admin = {}


def admin():
    """Access token of a throwaway QA admin (role set in the LOCAL DB). Never printed."""
    if "t" not in _admin:
        u = make_user("cadm")
        sql(f"update users set role='admin' where id='{u['id']}'")
        st, d, _ = api("POST", "/v1/admin/auth/log-in", {"username": u["username"], "password": P.A.PW})
        assert st in (200, 201), f"admin log-in → {st}"
        _admin["t"] = d["accessToken"]
        _admin["id"] = u["id"]
    return _admin["t"]


def iso(delta_h=0):
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=delta_h)).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def closure(slug, text="QA closure uz", ru=None, en=None, source="official"):
    reason = {"uz": text}
    if ru: reason["ru"] = ru
    if en: reason["en"] = en
    st, d, _ = api("POST", f"/v1/admin/places/{pid_of(slug)}/closures", {"startsAt": iso(-1), "reason": reason, "source": source}, admin())
    assert st == 201, f"create closure → {st}"
    return d


def override(slug, status, text="QA override uz", ru=None, en=None, hours=24):
    reason = {"uz": text}
    if ru: reason["ru"] = ru
    if en: reason["en"] = en
    st, d, _ = api("POST", f"/v1/admin/places/{pid_of(slug)}/overrides", {"status": status, "reason": reason, "expiresAt": iso(hours)}, admin())
    assert st == 201, f"create override → {st}"
    return d


def recompute_place(slug):
    """Recompute one place now, no refetch: create + end a throwaway override."""
    o = override(slug, "go", text="QA refresh", hours=1)
    st, _, _ = api("POST", f"/v1/admin/overrides/{o['id']}/end", None, admin())
    assert st in (200, 201), f"end override → {st}"


def seed(slug, sat=None, sun=None, stale_h=0, clear=False, **by_date):
    """Write the forecast fixture for `slug` and recompute it. sat/sun = dict of Open-Meteo daily fields for those window
    dates (rest MILD); other days MILD. clear=True deletes the forecast (status null)."""
    pid = pid_of(slug)
    sql(f"delete from place_forecasts where place_id='{pid}'")
    if not clear:
        t = today()
        days = [t + dt.timedelta(days=i) for i in range(-3, 7)]
        w = window()
        over = {w[k]: v for k, v in (("sat", sat), ("sun", sun)) if k in w and v}
        daily = {"time": [d.isoformat() for d in days]}
        for f in FIELDS:
            daily[f] = [(over.get(d, {}) or {}).get(f, MILD[f]) for d in days]
        sql(f"insert into place_forecasts(place_id,daily,fetched_at) values('{pid}','{json.dumps(daily)}'::jsonb,now())")
    recompute_place(slug)
    if stale_h:
        sql(f"update place_conditions set computed_at=now()-interval '{stale_h} hours' where place_id='{pid}'")


def cond(slug):
    st, d, _ = api("GET", f"/v1/places/{pid_of(slug)}/condition")
    assert st == 200, f"GET condition → {st}"
    return d


# ---------------- isolation ----------------
def before_case():
    P.before_case()                       # login attempts, place rows restored (season/hazards), onboarding, guest
    sql("delete from condition_overrides where reason_uz like 'QA%'")
    sql("delete from closures where reason_uz like 'QA%'")
    set_network(True, True)
    sh("settings", "put", "global", "airplane_mode_on", "0")


# ---------------- device helpers ----------------
def reveal(tid, tries=8):
    """Scroll Place down until the testID is in the tree."""
    for _ in range(tries):
        if has(tid, exact=True):
            return True
        scroll_down()
    return has(tid, exact=True)


def show_place(slug, fresh=True):
    """(Cold-start the app so no cached condition from an earlier case is shown,) open Place by deep link and scroll to
    the condition card (any of its states). Returns the testID found."""
    if fresh:
        relaunch()
        wait("nav.tab-explore", 25, exact=True)
    assert open_place_link(slug), "place did not open"
    for _ in range(8):
        for t in CARD_TIDS:
            if has(t, exact=True):
                return t
        scroll_down()
    return None


def slug0():
    return pick("type='peak' and difficulty=2")


def view(c, slug, name, fresh=True):
    """Open Place for `slug`, return (t0, found card testID, screenshot name). t0 = event cursor taken before opening."""
    t0 = mark()
    tid = show_place(slug, fresh)
    return t0, tid, (c.shot(name, tid) if tid else c.shot(name))


def viewed(t0, slug, timeout=10):
    return wait_event("condition_viewed", t0, timeout, pred=lambda p: p.get("slug") == slug)


def text_in(tid):
    """All text inside the node `tid` (its own text/desc plus nodes within its bounds)."""
    ns = nodes()
    n = find(tid, exact=True, ns=ns)
    if not n:
        return None
    x1, y1, x2, y2 = n["b"]
    parts = [n["text"], n["desc"]] + [m["text"] or m["desc"] for m in ns if m is not n and x1 <= m["x"] <= x2 and y1 <= m["y"] <= y2]
    out = []
    for p in parts:
        if p and p not in out:
            out.append(p)
    return " | ".join(out)


def tidtext(tid):
    return text_of(tid) or text_in(tid)


PLAN = {
    "spec": "features/conditions.md",
    "resources": [("Android", "emulator pixel-8a (session.py up), devRelease APK uz.irbis.app.dev on irbis-app feat/conditions 92887f9, device UI English"),
                  ("Backend", "irbis-api feat/conditions 2e52ef3 on :3000 started with `CONDITIONS_JOB_ENABLED=false` (no :05 cron overwriting fixtures), "
                              "migration conditions_init applied, `npm run db:seed` (71 places), Postgres container `irbis-api-db-1`, `adb reverse tcp:3000 tcp:3000`"),
                  ("Forecast fixtures", "`seed(slug, sat=…, sun=…)` writes place_forecasts in the Open-Meteo daily shape with dates relative to Tashkent today "
                                        "and recomputes only that place (create + end throwaway override, no refetch). The live Open-Meteo feed is used only by TC-014."),
                  ("Admin", "throwaway QA user promoted to role admin on the LOCAL DB (`admin()`); no real admin account, no secret printed"),
                  ("Isolation", "`before_case()`: place rows restored (season/hazards via set_place backup), QA closures/overrides (reason 'QA…') deleted, "
                                "network back on, guest, onboarding done. Each case seeds its own forecast, so order never matters."),
                  ("Weekend window", "Mon-Fri → Sat+Sun, Sat → Sat+Sun, Sun → Sun only (AC2). Cases compute the window from the Tashkent date at run time and "
                                     "expect `place.weather-day.sat` only when it exists; run on Sunday proves the one-day variant.")],
    "test_data": [("PLACE", "peak, difficulty 2 (same as the places SCREENS place), picked by SQL", "LOCAL dev DB"),
                  ("FORECAST", "MILD = Sat/Sun 24°/12°, wind 10, gusts 18, rain 0 mm / 10 %, code 1; each case overrides single fields", "place_forecasts fixture"),
                  ("QA-ADMIN", "`qa_cadm_<n>`, role admin", "API sign-up + SQL on LOCAL DB")],
    "timers": "Hourly cron at :05 and the 10 s Open-Meteo timeout (AC1), override/closure expiry in the hourly job (AC3), 6 h stale rule (AC4) are NOT waited on the device: "
              "covered by irbis-api `conditions.job.spec.ts`, `open-meteo.client.spec.ts`, `conditions.service.spec.ts` / `condition.rules.spec.ts`. "
              "TC-012 only sets computed_at 7 h back in the DB and checks what the user sees. Expiry of an override by time has no device case; if "
              "`conditions.service.spec.ts` does not assert an expired override is ignored, that is an open question.",
    "manual": ["Worried Irbis art and weather glyphs: final/placeholder per Q8, visual sign-off by the owner (glyphs are placeholders)",
               "AC6 web admin (Conditions table, forms, confirm dialog): browser, not Android — irbis-web tests + owner walk-through",
               "Real-device pass on the Galaxy S25 Ultra before release (long ru/uz reason lines wrapping; STD-TEXT covers the layout)",
               "Live Open-Meteo data and its non-commercial licence before launch (ADR-004 open question)"],
}

def _open_place_condition(c=None):
    slug = pick("type='peak' and difficulty=2")
    seed(slug, sat={"precipitation_probability_max": 70}, sun={"wind_speed_10m_max": 40})
    return bool(show_place(slug))


SCREENS = {
    "place-condition": {"open": _open_place_condition, "root": "place.screen"},
    "explore": {"open": lambda c=None: explore_ready(), "root": "explore.screen"},
}
