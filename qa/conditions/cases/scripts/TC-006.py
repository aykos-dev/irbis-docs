import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Explore cards show the status chip next to the type line; none when the status is null',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC8 — chip (colour + icon + label) on cards, none when null, explore_loaded.withStatus',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done, location granted, mock position Tashkent',
                  'API-nearest place A has a Go forecast, the second-nearest place B has no forecast (status null)'],
 'steps': ['Seed A (MILD) and clear B', 'Open Explore → check: list loaded', 'Read cards A and B'],
 'expected': ["`explore.card.<A>.status` exists and reads 'Go'; it sits on the same card as the type line — UI tree "
              '+ screenshot',
              'Card B has no `explore.card.<B>.status` node — UI tree',
              'QA event `explore_loaded` {withStatus = number of items with conditionStatus in GET /v1/places} — '
              'event log + API',
              "The chip is drawn beside the '{Type} · {distance}' line with its icon — crop (person judges)"],
 'caption': {'expected': "`explore.card.<A>.status` exists and reads 'Go'; it sits on the same c"},
 'focus': 'explore.sheet'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    st, d = places(limit=200, lat=TASHKENT[0], lng=TASHKENT[1])
    A, B = d["items"][0]["slug"], d["items"][1]["slug"]
    c.step(1, "seed A, clear B"); seed(A); seed(B, clear=True)
    n_api = sum(1 for i in all_places(lat=TASHKENT[0], lng=TASHKENT[1]) if i.get("conditionStatus"))
    c.step(2, "open Explore")
    t0 = mark()
    c.checkpoint("Explore opened", explore_ready(), "no explore.count")
    shot = c.shot("1_explore", "explore.sheet")
    c.step(3, "read cards")
    a = tidtext(f"explore.card.{A}.status")
    c.result(1, a is not None and "Go" in a, f"A status {a!r}", [shot])
    c.result(2, not has(f"explore.card.{B}.status", exact=True), f"B status node present: {has(f'explore.card.{B}.status', exact=True)}", [shot])
    ev = wait_event("explore_loaded", t0, 15)
    c.result(3, bool(ev) and ev.get("withStatus") == n_api, f"event {ev}, api count {n_api}")
    c.result(4, None, "judge on the crop: chip beside the type line", [shot])
