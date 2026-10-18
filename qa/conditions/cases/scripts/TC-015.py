import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Public condition endpoint and list field: no token, 404 / 400, conditionStatus on list items',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC4 — GET /v1/places/{id}/condition public; 404 PLACE_NOT_FOUND; 400 non-uuid; list items carry '
                'conditionStatus',
 'env': 'API · auto (no device)',
 'precondition': ['API up, 71 places',
                  'Peak PLACE with a Go forecast fixture (seeded), another with the forecast cleared'],
 'steps': ['GET the condition without a token',
           "GET with an unknown uuid and with 'not-a-uuid'",
           "GET /v1/places and read both places' items"],
 'expected': ["200 and the body has placeId, status 'go', source 'forecast', reasons, hazards, weekend, forecastAt, "
              'computedAt — API response',
              "Unknown uuid → 404 code PLACE_NOT_FOUND; 'not-a-uuid' → 400 code VALIDATION_FAILED — API response",
              "List item of the Go place has conditionStatus 'go'; item of the cleared place has it null or absent — "
              'API response'],
 'caption': {'expected': "200 and the body has placeId, status 'go', source 'forecast', reasons,"}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    items = all_places()
    A = slug0(); B = next(i["slug"] for i in items if i["slug"] != A)
    seed(A); seed(B, clear=True)
    c.step(1, "no token")
    st, d, _ = api("GET", f"/v1/places/{pid_of(A)}/condition")
    keys = {"placeId", "status", "source", "reasons", "hazards", "weekend", "forecastAt", "computedAt"}
    c.result(1, st == 200 and keys <= set(d) and d["status"] == "go" and d["source"] == "forecast", f"status {st}, keys missing {sorted(keys - set(d))}")
    c.step(2, "404 / 400")
    s1, d1, _ = api("GET", "/v1/places/00000000-0000-4000-8000-000000000000/condition")
    s2, d2, _ = api("GET", "/v1/places/not-a-uuid/condition")
    c.result(2, s1 == 404 and d1.get("code") == "PLACE_NOT_FOUND" and s2 == 400 and d2.get("code") == "VALIDATION_FAILED", f"{s1} {d1.get('code')}, {s2} {d2.get('code')}")
    c.step(3, "list")
    it = {i["slug"]: i for i in all_places()}
    c.result(3, it[A].get("conditionStatus") == "go" and it[B].get("conditionStatus") in (None,), f"A {it[A].get('conditionStatus')}, B {it[B].get('conditionStatus')}")
