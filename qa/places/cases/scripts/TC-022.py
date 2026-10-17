import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Permission granted but no fix: Tashkent fallback within 10 s',
 'priority': 'P2',
 'group': 'Variants',
 'requirement': 'AC6 — no fix in 10 s → Tashkent + banner',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, permission granted',
                  'No mock position published (mock loop stopped / point cleared) so the device has no fix',
                  'UX timeout, not a security timer: wait at most 12 s once'],
 'steps': ['Open Explore with no available fix', 'Watch for explore_loaded for at most 12 s'],
 'expected': ['explore_loaded {origin: tashkent} arrives between 8 and 12 s after Explore opened — QA event '
              'timestamps',
              "Header '71 places from Tashkent' and the banner are shown — UI tree + screenshot"],
 'focus': 'explore.location-banner',
 'caption': {'expected': 'explore_loaded {origin: tashkent} arrives between 8 and 12 s'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    grant_location(True)
    sh("cmd", "location", "providers", "send-extra-command", "gps", "delete_aiding_data")
    from drv import POINT_FILE
    try:
        os.remove(POINT_FILE)
    except OSError:
        pass
    sh("cmd", "location", "set-location-enabled", "true")
    t0 = mark()
    c.step(1, "open Explore")
    tap("nav.tab-explore", exact=True)
    c.checkpoint("Explore screen", wait("explore.screen", 10, exact=True), "no explore.screen")
    c.step(2, "wait for fallback")
    ev = wait_event("explore_loaded", t0, 12, lambda p: p.get("origin") == "tashkent")
    c.checkpoint("device really had no fix (no location_received)", not events().since(t0, "location_received"), "a fix arrived — setup failed")
    from drv import events as _e
    ts = [t for t, n, p in _e().since(t0, "explore_loaded") if p.get("origin") == "tashkent"]
    dt = round(ts[0] - t0, 1) if ts else None
    c.result(1, dt is not None and 8 <= dt <= 12.5, f"fallback after {dt} s, event {ev}")
    c.result(2, "from Tashkent" in (text_of("explore.count") or "") and has("explore.location-banner", exact=True), f"header {text_of('explore.count')!r}", [c.shot("2_fallback", "explore.location-banner")])
