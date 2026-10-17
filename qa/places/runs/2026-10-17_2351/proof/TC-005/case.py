import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'List filters combine with AND (types, difficulty, distance incl. boundaries)',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC2 — types any-of, difficulty inclusive, maxDistanceKm inclusive, total after filters',
 'env': 'API · auto (no device)',
 'precondition': ['API up, 71 places seeded', 'Origin = Tashkent fallback'],
 'steps': ['GET types=peak&types=lake → counts',
           'GET difficultyMin=2&difficultyMax=2 and difficultyMin=1&difficultyMax=1',
           'Pick the integer km k = ceil(distance of the 10th nearest place); GET maxDistanceKm=k and '
           'maxDistanceKm=k-1',
           'GET types=waterfall&difficultyMin=1&difficultyMax=2&maxDistanceKm=100'],
 'expected': ['types=peak&types=lake → total 45 (34+11), every item peak or lake, items = total — API response',
              'difficulty 2..2 → only difficulty 2 and total = local row count with difficulty 2; 1..1 likewise '
              '(inclusive ends) — API response',
              'maxDistanceKm=k includes every place with distanceM ≤ k×1000 (equals the unfiltered subset) and k−1 '
              'drops exactly the places with distanceM in (k−1)×1000 < d ≤ k×1000; `total` equals the returned count '
              '— API response',
              'Combined filters = intersection of the three single-filter result sets; total = its size — API '
              'response'],
 'caption': {'expected': 'types=peak&types=lake → total 45 (34+11), every item peak or'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    base = all_places()
    c.step(1, "types any-of")
    st, d = places(limit=200, types=["peak", "lake"])
    c.result(1, st == 200 and d["total"] == 45 and len(d["items"]) == 45 and {i["type"] for i in d["items"]} <= {"peak", "lake"},
             f"status {st}, total {d.get('total')}, types {sorted({i['type'] for i in d.get('items', [])})}")
    c.step(2, "difficulty inclusive")
    ok2, obs = True, []
    for dd in (1, 2):
        s, r = places(limit=200, difficultyMin=dd, difficultyMax=dd)
        exp = count_where(f"difficulty={dd}")
        ok2 &= s == 200 and r["total"] == exp and all(i["difficulty"] == dd for i in r["items"])
        obs.append(f"d{dd}: total {r.get('total')} / db {exp}")
    c.result(2, ok2, "; ".join(obs))
    c.step(3, "distance boundary")
    import math
    k = max(2, math.ceil(base[9]["distanceM"] / 1000))
    s1, r1 = places(limit=200, maxDistanceKm=k)
    s2, r2 = places(limit=200, maxDistanceKm=k - 1)
    e1 = [i["id"] for i in base if i["distanceM"] <= k * 1000]
    e2 = [i["id"] for i in base if i["distanceM"] <= (k - 1) * 1000]
    c.result(3, [i["id"] for i in r1["items"]] == e1 and [i["id"] for i in r2["items"]] == e2 and r1["total"] == len(e1) and r2["total"] == len(e2),
             f"k={k}: {len(r1['items'])}/{len(e1)} items, k-1: {len(r2['items'])}/{len(e2)}, totals {r1.get('total')}/{r2.get('total')}")
    c.step(4, "combined filters")
    s, r = places(limit=200, types=["waterfall"], difficultyMin=1, difficultyMax=2, maxDistanceKm=100)
    exp = [i["id"] for i in base if i["type"] == "waterfall" and 1 <= i["difficulty"] <= 2 and i["distanceM"] <= 100000]
    c.result(4, s == 200 and [i["id"] for i in r["items"]] == exp and r["total"] == len(exp), f"status {s}, got {len(r.get('items', []))}, expected {len(exp)}, total {r.get('total')}")
