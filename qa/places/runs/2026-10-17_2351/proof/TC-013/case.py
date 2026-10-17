import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Distance format: one decimal under 10 km, whole km from 10 km',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': "AC4 — '8.4 km' / '112 km'",
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, location granted',
                  'Mock position 8.4 km north of one seed place and a second run 112 km away (both computed from the '
                  "place's coordinates)"],
 'steps': ['Pick a peak by SQL; mock the device 8,400 m north of it; open Explore; read its card',
           'Mock the device 112,000 m north; reopen Explore; read the same card',
           'Mock 9,900 m, 9,960 m and 10,100 m north; read the card each time'],
 'expected': ["Card text contains '8.4 km' — UI tree + screenshot",
              "Card text contains '112 km' (no decimal) — UI tree + screenshot",
              "9.9 km distance → '9.9 km'; 10.1 km → '10 km' — UI tree + screenshot (the 9.95–9.99 rounding edge is "
              'an open question)'],
 'caption': {'expected': "Card text contains '8.4 km'"}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = pick("type='peak' and difficulty=1")
    lat0, lng0 = [float(x) for x in sql(f"select latitude || ' ' || longitude from places where slug='{slug}'").split()]
    def read(m):
        la, ln = offset(lat0, lng0, metres_north=m)
        reset_permission(FINE); grant_location(True); mock_at(la, ln)
        relaunch(); wait("nav.tab-explore", 20, exact=True)
        ok = open_explore()
        for _ in range(12):
            if has(f"explore.card.{slug}", exact=True): break
            from drv import scroll_down; scroll_down()
        return ok, card_text(slug), c.shot(f"d{m}", f"explore.card.{slug}") if has(f"explore.card.{slug}", exact=True) else None
    cases = [(8400, r"\b8\.4 km"), (112000, r"\b112 km"), (9900, r"\b9\.9 km"), (9960, r"\b10\.0 km"), (10100, r"(?<![\d.])10 km")]
    for i, (m, rx) in enumerate(cases):
        c.step(i + 1, f"mock {m} m from the place")
        ok, t, shot = read(m)
        c.checkpoint(f"Explore + card visible at {m} m", ok and t, t)
        c.result(min(i + 1, 3), re.search(rx, t or "") is not None, f"{m} m: card text {t!r}", [shot])
