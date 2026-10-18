import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Offline with nothing cached: condition card shows the offline message + Try again, retry recovers',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC8 — nothing cached offline → offline message + retry',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done, location granted + mock Tashkent',
                  'A waterfall PLACE the app has not opened before (picked by time offset; a warm cache → Blocked)',
                  'Explore list loaded online (place list data cached)'],
 'steps': ['Open Explore online → check: list loaded',
           'Wi-Fi and data off, tap the place card → check: `place.screen`, `place.name`',
           'Read the card',
           'Network on, tap `place.condition-retry`'],
 'expected': ["`place.condition-offline` shows the text You're offline — condition not loaded with "
              '`place.condition-retry` — UI tree + screenshot',
              'After network on and Retry, `place.condition` or `place.condition-empty` shows within 10 s — UI tree'],
 'caption': {'expected': "`place.condition-offline` shows the text You're offline — condition no"},
 'focus': 'place.condition-offline'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = sql(f"select slug from places where type='waterfall' order by slug offset {int(time.time()) % 22} limit 1")
    set_place(slug, hazards=[], season=["possible"] * 12); seed(slug)
    c.step(1, "Explore online")
    c.checkpoint("Explore opened", explore_ready(), "no explore.count")
    c.step(2, "offline, open place")
    set_network(False, False)
    try:
        c.checkpoint("place opened offline", P.open_place(slug) and wait("place.name", 10, exact=True), "place data not available offline")
        for _ in range(8):
            if any(has(t, exact=True) for t in CARD_TIDS): break
            scroll_down()
        c.checkpoint("cache was cold (no cached card)", not has("place.condition", exact=True), "condition already cached for this place")
        shot = c.shot("1_offline", "place.condition-offline" if has("place.condition-offline", exact=True) else None)
        c.step(3, "read card")
        c.result(1, has("place.condition-offline", exact=True) and has("place.condition-retry", exact=True) and has("You're offline"), f"offline card {has('place.condition-offline', exact=True)}", [shot])
    finally:
        set_network(True, True)
    c.step(4, "retry online")
    wait_gone("app.offline-banner", 10)
    tap("place.condition-retry", exact=True)
    ok = wait_any(["place.condition", "place.condition-empty"], 10)
    c.result(2, bool(ok), f"after retry: {ok}", [c.shot("2_retry")])
