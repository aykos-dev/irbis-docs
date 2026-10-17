import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Tapping a card opens Place and Back returns to Explore',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC4 + AC7 — card → Place; Back keeps Explore',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, location granted + mock at Tashkent centre', 'Explore list loaded'],
 'steps': ['Tap the first card (slug from the API for the same point)',
           '→ check: place.screen within 10 s',
           'Tap place.back'],
 'expected': ["place.screen shows with place.name equal to the card's name; QA event place_viewed {slug: <card "
              'slug>, requiredLevel, qualifies} — UI tree + QA event',
              'After Back explore.screen and explore.count are shown again — UI tree + screenshot'],
 'focus': 'place.name',
 'caption': {'expected': "place.screen shows with place.name equal to the card's name;"}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Explore loaded", explore_ready(), "no list")
    st, d = places(limit=200, lat=TASHKENT[0], lng=TASHKENT[1])
    it = d["items"][0]
    t0 = mark()
    c.step(1, "tap the first card")
    tap("explore.card." + it["slug"], exact=True)
    c.checkpoint("Place opened", wait("place.screen", 10, exact=True), "no place.screen")
    ev = wait_event("place_viewed", t0, 10)
    nm = text_of("place.name")
    c.result(1, nm == it["name"]["uz"] and bool(ev) and ev.get("slug") == it["slug"] and ev.get("requiredLevel") == it["requiredLevel"],
             f"name {nm!r} vs {it['name']['uz']!r}; event {ev}", [c.shot("1_place")])
    c.step(2, "tap Back")
    tap("place.back", exact=True)
    c.result(2, wait("explore.count", 10, exact=True) and has("explore.screen", exact=True), "Explore shown after Back", [c.shot("2_back", "explore.sheet")])
