import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'List validation: 400 VALIDATION_FAILED matrix with boundary values',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC2 — lat/lng pair, ranges, difficulty order, unknown type; valid edges accepted',
 'env': 'API · auto (no device)',
 'precondition': ['API up, 71 places seeded'],
 'steps': ['GET with only lat=41.2995; only lng=69.2401',
           'GET lat=90.0001 and lat=-90.0001; lng=180.0001 and lng=-180.0001',
           'GET difficultyMin=4&difficultyMax=2; difficultyMin=0; difficultyMax=6; maxDistanceKm=0; '
           'maxDistanceKm=1001; limit=0; limit=201; types=hill',
           'GET the valid edges lat=90&lng=180, lat=-90&lng=-180, difficultyMin=3&difficultyMax=3, maxDistanceKm=1, '
           'maxDistanceKm=1000, limit=1, limit=200'],
 'expected': ['The 2 single-coordinate requests and the 4 out-of-range coordinates → 400, body code '
              'VALIDATION_FAILED — API response',
              'difficulty min>max, 0, 6, maxDistanceKm 0 and 1001, limit 0 and 201, unknown type → 400 '
              'VALIDATION_FAILED each — API response',
              'Every valid edge value → 200 (limit=1 returns exactly 1 item, total still counts all) — API response'],
 'caption': {'expected': 'The 2 single-coordinate requests and the 4 out-of-range coor'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    def code(**q):
        s, d = places(**q)
        return s, d.get("code")
    bad1 = [dict(lat=41.2995), dict(lng=69.2401), dict(lat=90.0001, lng=0), dict(lat=-90.0001, lng=0), dict(lat=0, lng=180.0001), dict(lat=0, lng=-180.0001)]
    bad2 = [dict(difficultyMin=4, difficultyMax=2), dict(difficultyMin=0), dict(difficultyMax=6), dict(maxDistanceKm=0), dict(maxDistanceKm=1001),
            dict(limit=0), dict(limit=201), dict(types=["hill"])]
    c.step(1, "coordinate errors")
    r1 = [code(**q) for q in bad1]
    c.result(1, all(x == (400, "VALIDATION_FAILED") for x in r1), f"{r1}")
    c.step(2, "range / type errors")
    r2 = [code(**q) for q in bad2]
    c.result(2, all(x == (400, "VALIDATION_FAILED") for x in r2), f"{r2}")
    c.step(3, "valid edges")
    good = [dict(lat=90, lng=180), dict(lat=-90, lng=-180), dict(difficultyMin=3, difficultyMax=3), dict(maxDistanceKm=1), dict(maxDistanceKm=1000), dict(limit=1), dict(limit=200)]
    r3 = [places(**q)[0] for q in good]
    s, d = places(limit=1)
    c.result(3, all(x == 200 for x in r3) and len(d["items"]) == 1 and d["total"] == 71, f"statuses {r3}; limit=1 → {len(d.get('items', []))} item, total {d.get('total')}")
