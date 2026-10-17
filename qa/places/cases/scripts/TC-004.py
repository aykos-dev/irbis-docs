import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'List without a token: sorted by distance, integer metres, total',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC2 — public, sorted asc (ties by id), distanceM int, total, limit 200',
 'env': 'API · auto (no device)',
 'precondition': ['API up, 71 places seeded', 'No Authorization header'],
 'steps': ['GET /v1/places?limit=200 (no token, no lat/lng)', 'GET /v1/places?limit=200&lat=41.2995&lng=69.2401'],
 'expected': ['Status 200 without a token; items 71, total 71, nextCursor null, origin `tashkent` — API response',
              'distanceM is an integer on every item; (distanceM, id) is non-decreasing across the page — API '
              'response',
              "With lat/lng given: origin `device`, same 71 items, first item's distanceM within 1 m of the "
              'haversine from the request point to its latitude/longitude — API response'],
 'caption': {'expected': 'Status 200 without a token; items 71, total 71, nextCursor n'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.step(1, "GET /v1/places?limit=200 without a token")
    st, d = places(limit=200)
    it = d.get("items", [])
    c.result(1, st == 200 and len(it) == 71 and d.get("total") == 71 and d.get("nextCursor") is None and d.get("origin") == "tashkent",
             f"status {st}, items {len(it)}, total {d.get('total')}, nextCursor {d.get('nextCursor')}, origin {d.get('origin')}")
    ints = all(isinstance(i["distanceM"], int) for i in it)
    keys = [(i["distanceM"], i["id"]) for i in it]
    c.result(2, ints and keys == sorted(keys), f"all distanceM ints: {ints}; sorted by (distanceM,id): {keys == sorted(keys)}")
    c.step(2, "GET with lat/lng")
    st2, d2 = places(limit=200, lat=TASHKENT[0], lng=TASHKENT[1])
    i0 = d2["items"][0] if st2 == 200 and d2.get("items") else None
    hav = distance_m(TASHKENT[0], TASHKENT[1], i0["latitude"], i0["longitude"]) if i0 else None
    c.result(3, bool(i0) and d2["origin"] == "device" and len(d2["items"]) == 71 and abs(i0["distanceM"] - hav) <= 1,
             f"status {st2}, origin {d2.get('origin')}, items {len(d2.get('items', []))}, first distanceM {i0 and i0['distanceM']} vs haversine {hav and round(hav, 1)}")
