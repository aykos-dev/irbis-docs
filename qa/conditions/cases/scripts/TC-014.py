import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Recompute now (live Open-Meteo): 202, forecasts stored for every place, weekend matches the window',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC1 + AC5 — recompute fetches the Open-Meteo forecast, stores it, recomputes every place',
 'env': 'API · auto (no device)',
 'precondition': ['API up, 71 places, internet reachable (checkpoint: else Blocked)', 'QA admin token'],
 'steps': ['POST /v1/admin/conditions/recompute',
           'Poll the DB ≤ 10 s until place_forecasts holds a row for every place',
           'GET a place condition'],
 'expected': ['Response 202 with `startedAt` — API response',
              'place_forecasts rows = place count and place_conditions rows = place count within 10 s — LOCAL DB',
              'GET /v1/places/{id}/condition: `forecastAt` within the last 5 min and `weekend` has one entry per day '
              'of the window (Sun only → 1, otherwise 2) — API response'],
 'caption': {'expected': 'Response 202 with `startedAt` — API response'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = slug0(); n_places = int(sql("select count(*) from places"))
    sql("delete from place_forecasts")
    c.step(1, "recompute")
    st, d, _ = api("POST", "/v1/admin/conditions/recompute", None, admin())
    c.result(1, st == 202 and bool(d.get("startedAt")), f"status {st}")
    c.step(2, "poll DB")
    end = time.time() + 10; nf = nc = 0
    while time.time() < end:
        nf = int(sql("select count(*) from place_forecasts")); nc = int(sql("select count(*) from place_conditions"))
        if nf >= n_places and nc >= n_places: break
        time.sleep(1)
    c.checkpoint("Open-Meteo reachable (forecasts stored)", nf > 0, f"{nf} forecasts")
    c.result(2, nf == n_places and nc == n_places, f"forecasts {nf}/{n_places}, conditions {nc}/{n_places}")
    c.step(3, "read place")
    r = cond(slug)
    age = int(sql(f"select extract(epoch from now()-fetched_at)::int from place_forecasts where place_id='{pid_of(slug)}'") or 9999)
    c.result(3, age <= 300 and len(r["weekend"]) == len(window()) and bool(r.get("forecastAt")), f"forecast age {age}s, weekend days {len(r['weekend'])}, window {len(window())}")
