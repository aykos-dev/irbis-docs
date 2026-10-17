import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Location switched off on the device falls back to Tashkent',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC6 — location off → origin Tashkent + banner',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, location permission granted',
                  'Device location switched OFF (`cmd location set-location-enabled false`), switched back ON in '
                  'cleanup'],
 'steps': ['Open Explore → check: explore.screen', 'Wait for the list (at most 12 s)'],
 'expected': ['QA event location_permission {result: unavailable} or explore_loaded {origin: tashkent} — QA event',
              "Header '71 places from Tashkent' and the banner 'Turn on location to see distances from you' — UI "
              'tree + screenshot'],
 'focus': 'explore.location-banner',
 'caption': {'expected': 'QA event location_permission {result: unavailable} or explor'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    grant_location(True)
    sh("cmd", "location", "set-location-enabled", "false")
    try:
        t0 = mark()
        c.step(1, "open Explore")
        c.checkpoint("Explore screen", wait("nav.tab-explore", 10, exact=True) and (tap("nav.tab-explore", exact=True) or True) and wait("explore.screen", 10, exact=True), "no explore.screen")
        ev = wait_event("explore_loaded", t0, 12, lambda p: p.get("origin") == "tashkent")
        wait("explore.count", 5, exact=True)
        c.step(2, "read header and banner")
        c.result(1, bool(ev), f"explore_loaded {ev}; location_permission {[p for _, _, p in events().since(t0, 'location_permission')]}")
        c.result(2, "from Tashkent" in (text_of("explore.count") or "") and has("Turn on location to see distances from you"), f"header {text_of('explore.count')!r}", [c.shot("2_off", "explore.location-banner")])
    finally:
        sh("cmd", "location", "set-location-enabled", "true")
