import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'List pagination by cursor covers every place once',
 'priority': 'P2',
 'group': 'Variants',
 'requirement': 'AC2 — cursor, limit default 50, limit 200 single page',
 'env': 'API · auto (no device)',
 'precondition': ['API up, 71 places seeded'],
 'steps': ['GET /v1/places (default limit)', 'Follow nextCursor with limit=50 until it is null', 'GET limit=200'],
 'expected': ['Default page has 50 items and a non-null nextCursor, total 71 — API response',
              'The pages concatenated give 71 distinct ids in the same order as the single limit=200 page — API '
              'response',
              'limit=200 returns 71 items and nextCursor null — API response'],
 'caption': {'expected': 'Default page has 50 items and a non-null nextCursor, total 7'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.step(1, "default page")
    s, d = places()
    c.result(1, s == 200 and len(d["items"]) == 50 and d["nextCursor"] and d["total"] == 71, f"status {s}, items {len(d.get('items', []))}, cursor set {bool(d.get('nextCursor'))}, total {d.get('total')}")
    c.step(2, "walk the cursor")
    ids, cur, n = [i["id"] for i in d["items"]], d["nextCursor"], 0
    while cur and n < 5:
        s, d2 = places(limit=50, cursor=cur)
        ids += [i["id"] for i in d2["items"]]
        cur, n = d2["nextCursor"], n + 1
    full = [i["id"] for i in all_places()]
    c.result(2, ids == full and len(set(ids)) == 71, f"collected {len(ids)}, distinct {len(set(ids))}, same order as limit=200: {ids == full}")
    s, d3 = places(limit=200)
    c.result(3, len(d3["items"]) == 71 and d3["nextCursor"] is None, f"items {len(d3['items'])}, nextCursor {d3['nextCursor']}")
