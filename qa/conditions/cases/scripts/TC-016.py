import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Admin API matrix: roles, reason and date boundaries, end twice = 409, one active override',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC5 — 401/403, reason.uz 1–280, endsAt > startsAt, expiresAt in (now, now+14 d], ended twice 409, '
                'at most one active override, createdById',
 'env': 'API · auto (no device)',
 'precondition': ['API up, QA admin and one QA user token', 'Peak PLACE'],
 'steps': ['Call create-closure without token (401) and with the user token (403)',
           'Create closures with reason.uz of 1, 280, 281 and 0 characters; endsAt equal to / after startsAt',
           'Create overrides with expiresAt now+14 d−1 min, +14 d+1 min, in the past; create a second override',
           'End a closure and an override twice',
           'Read condition-controls'],
 'expected': ['No token → 401 UNAUTHENTICATED; user token → 403 — API response',
              'reason.uz 1 and 280 chars → 201; 281 and 0 → 400; endsAt = startsAt → 400, endsAt > startsAt → 201 — '
              'API response',
              'expiresAt now+14 d−1 min → 201; +14 d+1 min → 400; past → 400 — API response',
              'Second end of a closure → 409 CLOSURE_ALREADY_ENDED; second end of an override → 409 '
              'OVERRIDE_ALREADY_ENDED — API response',
              'After creating two overrides condition-controls lists exactly one without endedAt (the newer); '
              'createdById of the closures = the admin — API response'],
 'caption': {'expected': 'No token → 401 UNAUTHENTICATED; user token → 403 — API response'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = slug0(); pid = pid_of(slug); tok = admin(); u = make_user("cusr")
    url = f"/v1/admin/places/{pid}/closures"
    body = lambda t, **k: {"startsAt": iso(-1), "reason": {"uz": t}, "source": "admin", **k}
    c.step(1, "roles")
    s_a, d_a, _ = api("POST", url, body("QA x"))
    s_b, _, _ = api("POST", url, body("QA x"), u["access"])
    c.result(1, s_a == 401 and d_a.get("code") == "UNAUTHENTICATED" and s_b == 403, f"{s_a} {d_a.get('code')}, {s_b}")
    c.step(2, "closure boundaries")
    r = {}
    r["1"] = api("POST", url, body("Q"), tok)[0]
    r["280"] = api("POST", url, body("QA" + "x" * 278), tok)[0]
    r["281"] = api("POST", url, body("QA" + "x" * 279), tok)[0]
    r["0"] = api("POST", url, body(""), tok)[0]
    r["ends_eq"] = api("POST", url, {**body("QA eq"), "endsAt": iso(-1)}, tok)[0]
    s_ok, closure_row, _ = api("POST", url, {**body("QA later"), "startsAt": iso(1), "endsAt": iso(2)}, tok)
    c.result(2, (r["1"], r["280"], r["281"], r["0"]) == (201, 201, 400, 400) and s_ok == 201, f"{r}, later {s_ok}")
    c.step(3, "override boundaries")
    ourl = f"/v1/admin/places/{pid}/overrides"
    ob = lambda h: {"status": "caution", "reason": {"uz": "QA ov"}, "expiresAt": iso(h)}
    sa, o1, _ = api("POST", ourl, ob(14 * 24 - 1 / 60), tok)
    sb = api("POST", ourl, ob(14 * 24 + 1 / 60), tok)[0]
    sc = api("POST", ourl, ob(-1), tok)[0]
    c.result(3, (sa, sb, sc) == (201, 400, 400), f"{sa}, {sb}, {sc}")
    c.step(4, "end twice")
    e1 = api("POST", f"/v1/admin/closures/{closure_row['id']}/end", None, tok)[0]
    e2s, e2d, _ = api("POST", f"/v1/admin/closures/{closure_row['id']}/end", None, tok)
    sx, o2, _ = api("POST", ourl, ob(5), tok)   # ends o1 first
    f1 = api("POST", f"/v1/admin/overrides/{o2['id']}/end", None, tok)[0]
    f2s, f2d, _ = api("POST", f"/v1/admin/overrides/{o2['id']}/end", None, tok)
    c.result(4, e1 == 200 and e2s == 409 and e2d.get("code") == "CLOSURE_ALREADY_ENDED" and f1 == 200 and f2s == 409 and f2d.get("code") == "OVERRIDE_ALREADY_ENDED", f"{e1} {e2s} {e2d.get('code')}, {f1} {f2s} {f2d.get('code')}")
    c.step(5, "controls")
    o3 = api("POST", ourl, ob(6), tok)[1]
    o4 = api("POST", ourl, ob(7), tok)[1]
    st, ctl, _ = api("GET", f"/v1/admin/places/{pid}/condition-controls", None, tok)
    act = [o for o in ctl.get("overrides", []) if not o.get("endedAt")]
    cl = ctl.get("closures", [])
    c.result(5, st == 200 and len(act) == 1 and act[0]["id"] == o4["id"] and cl and all(x.get("createdById") == _admin["id"] for x in cl), f"status {st}, active overrides {len(act)}, closures {len(cl)}")
