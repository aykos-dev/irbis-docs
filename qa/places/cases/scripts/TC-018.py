import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'First Explore open asks for location; Allow → device origin',
 'priority': 'P0',
 'group': 'Core',
 'requirement': "AC6 — OS prompt on first open, granted → 'near you', no banner",
 'env': 'Android · auto (adb)',
 'precondition': ["Guest, location permission reset to 'ask' (not granted, no user-set flag)",
                  'Mock device position = Tashkent centre'],
 'steps': ['Open the Explore tab → check: the system permission dialog is shown within 10 s',
           "Tap 'While using the app' (or 'Allow')",
           'Wait for the list'],
 'expected': ['The OS location prompt appears the first time Explore opens — screenshot of the dialog + UI tree '
              "(text 'Allow' / 'While using the app')",
              "QA event location_permission {result: granted}; header '71 places near you'; explore.location-banner "
              'absent — QA event + UI tree',
              'Event explore_loaded {origin: device}; the card distances come from the device point (first card '
              "equals the API's first item for the mock point) — QA event + UI tree"],
 'focus': 'explore.sheet',
 'caption': {'expected': 'The OS location prompt appears the first time Explore opens'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    reset_permission(FINE); reset_permission(COARSE)
    mock_at(*TASHKENT)
    t0 = mark()
    c.step(1, "open Explore")
    if not wait("nav.tab-explore", 5, exact=True):
        relaunch(); wait("nav.tab-explore", 25, exact=True)
    tap("nav.tab-explore", exact=True)
    c.checkpoint("OS permission dialog shown", wait_any(["While using the app", "Only this time", "Allow"], 12), "no dialog")
    c.result(1, True, "OS location dialog shown on first Explore open", [c.shot("1_prompt", None)])
    c.step(2, "tap Allow")
    tap("While using the app") if has("While using the app") else tap("Allow")
    ev = wait_event("location_permission", t0, 10)
    wait("explore.count", 15, exact=True)
    hdr = text_of("explore.count") or ""
    c.result(2, bool(ev) and ev.get("result") == "granted" and "near you" in hdr and not has("explore.location-banner", exact=True), f"event {ev}, header {hdr!r}, banner {has('explore.location-banner', exact=True)}", [c.shot("2_granted", "explore.count")])
    ev2 = wait_event("explore_loaded", t0, 10, lambda p: p.get("origin") == "device")
    st, d = places(limit=200, lat=TASHKENT[0], lng=TASHKENT[1])
    c.step(3, "check origin and first card")
    c.result(3, bool(ev2) and has("explore.card." + d["items"][0]["slug"], exact=True), f"explore_loaded {ev2}; first API slug {d['items'][0]['slug']}", [c.shot("3_list", "explore.sheet")])
