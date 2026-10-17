import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Place detail errors and signed-in viewer',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC3 — unknown uuid 404 PLACE_NOT_FOUND, non-uuid 400, signed-in = guest viewer',
 'env': 'API · auto (no device)',
 'precondition': ['API up', 'A throwaway QA user signed up through the API (token kept in memory only)'],
 'steps': ['GET /v1/places/00000000-0000-4000-8000-000000000000',
           'GET /v1/places/not-a-uuid and /v1/places/123',
           "GET a level-2 place with the QA user's token and without"],
 'expected': ['Unknown uuid → 404, code PLACE_NOT_FOUND — API response',
              '`not-a-uuid` and `123` → 400 VALIDATION_FAILED — API response',
              'Signed-in and guest responses carry the same viewer {level: 1, qualifies: false} for a level-2 place '
              '— API response'],
 'caption': {'expected': 'Unknown uuid → 404, code PLACE_NOT_FOUND'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.step(1, "unknown uuid")
    s, d, _ = api("GET", "/v1/places/00000000-0000-4000-8000-000000000000")
    c.result(1, s == 404 and d.get("code") == "PLACE_NOT_FOUND", f"status {s}, code {d.get('code')}")
    c.step(2, "non-uuid")
    r = [api("GET", f"/v1/places/{x}")[:2] for x in ("not-a-uuid", "123")]
    c.result(2, all(s == 400 and d.get("code") == "VALIDATION_FAILED" for s, d in r), f"{[(s, d.get('code')) for s, d in r]}")
    c.step(3, "signed-in vs guest viewer")
    u = make_user("pl_viewer")
    pid = pid_of(pick("required_level=2"))
    sg, dg = place(pid)
    ss, ds = place(pid, token=u["access"])
    c.result(3, sg == 200 and ss == 200 and dg["viewer"] == ds["viewer"] == {"level": 1, "qualifies": False}, f"guest {dg.get('viewer')}, signed-in {ds.get('viewer')}")
