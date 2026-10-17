import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Denying location falls back to Tashkent with a banner',
 'priority': 'P0',
 'group': 'Core',
 'requirement': "AC6 — denied → 'from Tashkent', banner 'Turn on location to see distances from you'",
 'env': 'Android · auto (adb)',
 'precondition': ["Guest, location permission reset to 'ask'",
                  'Mock device position far from Tashkent (so a wrong origin would show)'],
 'steps': ['Open Explore → check: system dialog', "Tap 'Don't allow'", 'Wait for the list'],
 'expected': ['QA event location_permission {result: denied} — QA event',
              "Header '71 places from Tashkent'; explore_loaded {origin: tashkent}; first card = API's first item "
              'for the Tashkent origin — UI tree + QA event + API response',
              "explore.location-banner shows 'Turn on location to see distances from you' and "
              "explore.location-turn-on shows 'Turn on' — UI tree + screenshot"],
 'focus': 'explore.location-banner',
 'caption': {'expected': 'QA event location_permission {result: denied}'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    reset_permission(FINE); reset_permission(COARSE)
    mock_at(*offset(41.0, 71.0))
    t0 = mark()
    open_explore(wait_list=False)
    c.checkpoint("OS permission dialog shown", wait_any(["Don't allow", "Don’t allow", "Deny"], 12), "no dialog")
    c.step(1, "Don't allow")
    tap("Don't allow") if has("Don't allow") else (tap("Don’t allow") if has("Don’t allow") else tap("Deny"))
    ev = wait_event("location_permission", t0, 10)
    c.result(1, bool(ev) and ev.get("result") in ("denied", "blocked"), f"event {ev}")
    wait("explore.count", 15, exact=True)
    st, d = places(limit=200)
    ev2 = wait_event("explore_loaded", t0, 10, lambda p: p.get("origin") == "tashkent")
    hdr = text_of("explore.count") or ""
    c.step(2, "read header")
    c.result(2, "71 places from Tashkent" in hdr and bool(ev2) and has("explore.card." + d["items"][0]["slug"], exact=True), f"header {hdr!r}, event {ev2}", [c.shot("2_list", "explore.count")])
    c.step(3, "read banner")
    c.result(3, has("Turn on location to see distances from you") and (text_of("explore.location-turn-on") or "").strip() == "Turn on", f"banner {text_of('explore.location-banner')!r}, button {text_of('explore.location-turn-on')!r}", [c.shot("3_banner", "explore.location-banner")])
