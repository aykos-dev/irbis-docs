import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': "Offline: Place and Explore show the last cached condition with its 'Updated …' age",
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC8 — offline shows the cached condition + age (Place and Explore chip)',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done, location granted + mock Tashkent',
                  'Peak PLACE (API-nearest) with a Caution forecast',
                  'Explore and the place were opened online once in this session so both are cached'],
 'steps': ['Seed Caution, open Explore online, open the place online → check: card shown',
           'Wi-Fi and data off, cold-start the app, open the place → check: `place.screen`',
           'Read the card, go to Explore and read the card chip'],
 'expected': ["`place.condition` is shown with chip 'Caution' and `place.condition-updated` starts with 'Updated' "
              '(age) — UI tree + screenshot; `place.condition-offline` is not shown',
              "In Explore (offline) `explore.card.<slug>.status` reads 'Caution' — UI tree + screenshot"],
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
    c.step(2, "offline cold start")
    set_network(False, False)
    try:
        relaunch(); wait("nav.tab-explore", 25, exact=True)
        c.checkpoint("place opens offline", open_place_link(slug), "place.screen missing offline")
        for _ in range(8):
            if any(has(t, exact=True) for t in CARD_TIDS): break
            scroll_down()
        shot = c.shot("1_offline_place", "place.condition" if has("place.condition", exact=True) else None)
        c.step(3, "read card, then Explore")
        up = tidtext("place.condition-updated") or ""
        c.result(1, has("place.condition", exact=True) and text_in("place.condition-status") == "Caution" and up.startswith("Updated") and not has("place.condition-offline", exact=True), f"card {has('place.condition', exact=True)}, chip {text_in('place.condition-status')!r}, updated {up!r}", [shot])
        open_explore(wait_list=False); wait("explore.screen", 10, exact=True)
        for _ in range(3):
            if has(f"explore.card.{slug}.status", exact=True): break
            time.sleep(1)
        s2 = c.shot("2_offline_explore", "explore.sheet")
        chip = tidtext(f"explore.card.{slug}.status")
        c.result(2, chip is not None and "Caution" in chip, f"explore chip {chip!r}", [s2])
    finally:
        set_network(True, True)
