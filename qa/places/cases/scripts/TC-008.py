import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Place detail without a token: shape, empty season/hazards, viewer',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC3 — PlaceDetail, public, viewer {level 1, qualifies}',
 'env': 'API · auto (no device)',
 'precondition': ['API up, 71 places seeded', 'No Authorization header'],
 'steps': ['Pick one level-1 place and one level-3 place by SQL',
           'GET /v1/places/{id} for each (no token, no lat/lng)',
           'GET the level-1 place with lat=41.2995&lng=69.2401'],
 'expected': ['Level-1 place → 200 with id, slug, name.uz set, name.ru and name.en null, type, latitude, longitude, '
              'elevationM, difficulty, requiredLevel 1, distanceM, region null, description {uz, ru, en}, season [], '
              'hazards [], origin `tashkent` — API response',
              'Level-1 place viewer = {level: 1, qualifies: true}; level-3 place viewer = {level: 1, qualifies: '
              'false} — API response',
              'With lat/lng: origin `device` and distanceM = haversine of the request point (±1 m) — API response'],
 'caption': {'expected': 'Level-1 place → 200 with id, slug, name.uz set, name.ru and '}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    s1, s3 = pick("required_level=1"), pick("required_level=3")
    c.step(1, "GET detail level-1 place")
    st, d = place(pid_of(s1))
    need = {"id", "slug", "name", "type", "latitude", "longitude", "elevationM", "difficulty", "requiredLevel", "distanceM", "region", "description", "season", "hazards", "origin", "viewer"}
    c.result(1, st == 200 and need <= set(d) and d["name"]["uz"] and d["name"]["ru"] is None and d["name"]["en"] is None and d["requiredLevel"] == 1
             and d["season"] == [] and d["hazards"] == [] and d["region"] is None and d["origin"] == "tashkent",
             f"status {st}, missing {sorted(need - set(d))}, name ru/en {d.get('name', {}).get('ru')}/{d.get('name', {}).get('en')}, season {d.get('season')}, hazards {d.get('hazards')}, origin {d.get('origin')}")
    c.step(2, "GET detail level-3 place")
    st3, d3 = place(pid_of(s3))
    c.result(2, d.get("viewer") == {"level": 1, "qualifies": True} and d3.get("viewer") == {"level": 1, "qualifies": False},
             f"level-1 viewer {d.get('viewer')}, level-3 (requiredLevel {d3.get('requiredLevel')}) viewer {d3.get('viewer')}")
    c.step(3, "GET with lat/lng")
    st4, d4 = place(pid_of(s1), lat=TASHKENT[0], lng=TASHKENT[1])
    hav = distance_m(TASHKENT[0], TASHKENT[1], d4["latitude"], d4["longitude"])
    c.result(3, st4 == 200 and d4["origin"] == "device" and abs(d4["distanceM"] - hav) <= 1, f"status {st4}, origin {d4.get('origin')}, distanceM {d4.get('distanceM')} vs {round(hav, 1)}")
