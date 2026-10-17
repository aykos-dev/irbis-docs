import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Guest-merge rejects unknown or too many interests with 400',
 'priority': 'P1',
 'group': 'Supplementary',
 'requirement': 'AC7 — unknown values rejected (400)',
 'env': 'Android · auto (adb)',
 'precondition': ['Local API up; QA user via API (no device)'],
 'steps': ['POST /v1/me/guest-merge with experience "pro"',
           '… with interests ["peaks","peaks"]',
           '… with six interests',
           '… with five valid interests and experience weekend'],
 'expected': ['Status 400 and code VALIDATION_FAILED for the unknown experience — API response',
              'Status 400 for the duplicate interest — API response',
              'Status 400 for six interests — API response',
              'Status 200 and GET /v1/me returns experience weekend and the five interests — API response'],
 'focus': None,
 'caption': {'expected': 'API only'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    u = make_user("onb17"); tok = u["access"]
    def merge(ob): return api("POST", "/v1/me/guest-merge", {"onboarding": ob}, tok)
    st, d, _ = merge({"experience": "pro"}); c.result(1, st == 400 and d.get("code") == "VALIDATION_FAILED", f"status {st}, code {d.get('code')}")
    st, d, _ = merge({"interests": ["peaks", "peaks"]}); c.result(2, st == 400, f"status {st}")
    st, d, _ = merge({"interests": ["peaks", "caves", "lakes", "camping", "trails", "peaks"]}); c.result(3, st == 400, f"status {st}")
    st, d, _ = merge({"experience": "weekend", "interests": ["peaks", "caves", "lakes", "camping", "trails"]})
    st2, me, _ = api("GET", "/v1/me", None, tok)
    c.result(4, st == 200 and st2 == 200 and me.get("experience") == "weekend" and len(me.get("interests", [])) == 5, f"merge {st}, me {st2}, interests {len(me.get('interests', []))}")
