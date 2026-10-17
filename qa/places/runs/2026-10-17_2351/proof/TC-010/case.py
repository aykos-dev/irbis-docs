import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Explore tab opens for a guest: map, sheet, count header, sorted cards',
 'priority': 'P0',
 'group': 'Core',
 'requirement': "AC4 — Explore replaces Coming soon; header, 'Sorted by distance', cards",
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done',
                  'Location granted, mock device position = Tashkent centre (41.2995, 69.2401)'],
 'steps': ['Tap the Explore tab → check: explore.screen within 10 s',
           'Wait for the list header',
           'Read the first card and compare with the API order for the same point'],
 'expected': ["explore.screen, explore.map and explore.sheet are shown, no 'Coming soon' text — UI tree + screenshot",
              "Header explore.count reads '71 places near you' and the text 'Sorted by distance' is shown; QA event "
              'explore_loaded {count: 71, origin: device} — UI tree + QA event',
              "The first card is the API's first item (slug) and shows name, '{Type} · {distance}' and difficulty "
              'boots — UI tree + screenshot'],
 'focus': 'explore.sheet',
 'caption': {'expected': 'explore.screen, explore.map and explore.sheet are shown, no '}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    t0 = mark()
    c.step(1, "open Explore")
    c.checkpoint("Explore opened", explore_ready(), "no explore.count")
    shot = c.shot("1_explore")
    c.result(1, all(has(t, exact=True) for t in ("explore.screen", "explore.map", "explore.sheet")) and not has("Coming soon"), "screen, map, sheet present; no Coming soon", [shot])
    ev = wait_event("explore_loaded", t0, 15)
    hdr = text_of("explore.count") or ""
    c.step(2, "read header")
    c.result(2, "71 places near you" in hdr and has("Sorted by distance") and bool(ev) and ev.get("count") == 71 and ev.get("origin") == "device",
             f"header {hdr!r}, event {ev}", [shot])
    st, d = places(limit=200, lat=TASHKENT[0], lng=TASHKENT[1])
    slug = d["items"][0]["slug"]
    ct = card_text(slug)
    c.step(3, "first card")
    c.result(3, bool(ct) and re.search(r"\d+(\.\d)? km", ct or "") is not None and has("explore.card." + slug, exact=True),
             f"first API slug {slug}; card text {ct!r}", [c.shot("3_first_card", "explore.card." + slug)])
