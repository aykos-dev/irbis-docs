import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': "Offline: Place shows the last cached condition with its 'Updated …' age",
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC8 — offline shows the cached condition + age (Place only; Explore needs no offline, owner 2026-10-18)',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done, location granted + mock Tashkent',
                  'Peak PLACE (API-nearest) with a Caution forecast',
                  'The place was opened online once in this session so it is cached'],
 'steps': ['Seed Caution, open Explore online, open the place online → check: card shown',
           'Wi-Fi and data off (app keeps running), reopen the place → check: `place.screen`',
           'Read the card'],
 'expected': ["`place.condition` is shown with chip 'Caution' and `place.condition-updated` starts with 'Updated' "
              '(age) — UI tree + screenshot; `place.condition-offline` is not shown'],
 'caption': {'expected': "`place.condition` is shown with chip 'Caution' and `place.condition-up"},
 'focus': 'place.condition'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    st, d = places(limit=200, lat=TASHKENT[0], lng=TASHKENT[1])
    slug = d["items"][0]["slug"]; set_place(slug, hazards=[], season=["possible"] * 12)
    c.step(1, "seed + online views"); seed(slug, sun={"wind_speed_10m_max": 40})
    c.checkpoint("Explore opened", explore_ready(), "no explore.count")
    c.checkpoint("card shown online", show_place(slug, fresh=False) == "place.condition", "no condition online")
    c.step(2, "go offline (app stays running), reopen Place")
    set_network(False, False)
    try:
        c.checkpoint("place opens offline", open_place_link(slug), "place.screen missing offline")
        for _ in range(8):
            if any(has(t, exact=True) for t in CARD_TIDS): break
            scroll_down()
        shot = c.shot("1_offline_place", "place.condition" if has("place.condition", exact=True) else None)
        c.step(3, "read card, then Explore")
        up = tidtext("place.condition-updated") or ""
        c.result(1, has("place.condition", exact=True) and text_in("place.condition-status") == "Caution" and up.startswith("Updated") and not has("place.condition-offline", exact=True), f"card {has('place.condition', exact=True)}, chip {text_in('place.condition-status')!r}, updated {up!r}", [shot])
    finally:
        set_network(True, True)
