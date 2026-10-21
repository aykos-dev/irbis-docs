import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Condition fetch error: the card shows error + retry, the rest of Place still renders, retry recovers',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC8 — error card + retry; rest of Place renders',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done, location granted + mock Tashkent',
                  'Peak PLACE with a Go forecast',
                  'Explore list loaded (place data cached), then the API is made unreachable with `adb reverse '
                  '--remove` (app still thinks it is online)'],
 'steps': ['Seed, open Explore → check: list loaded',
           'Remove the adb reverse, tap the place card → check: `place.screen` and `place.name` shown (else Blocked)',
           'Read the card',
           'Restore the reverse, tap `place.condition-retry`'],
 'expected': ["`place.condition-error` shows 'Couldn't load the condition' with `place.condition-retry` — UI tree + "
              'screenshot',
              '`place.name` and the level card (`place.screen`) are still rendered — UI tree',
              'After the reverse is back and Retry is tapped, `place.condition` shows within 10 s — UI tree'],
 'caption': {'expected': "`place.condition-error` shows 'Couldn't load the condition' with `plac"},
 'focus': 'place.condition-error'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    import subprocess
    ser = os.environ.get("QA_SERIAL", "emulator-5554")
    adb = lambda *a: subprocess.run(["adb", "-s", ser, *a], capture_output=True, text=True)
    slug = slug0(); set_place(slug, hazards=[], season=["possible"] * 12)
    c.step(1, "seed + Explore"); seed(slug)
    c.checkpoint("Explore opened", explore_ready(), "no explore.count")
    c.step(2, "API unreachable, open place")
    adb("reverse", "--remove", "tcp:3000")
    try:
        ok = P.open_place(slug)
        c.checkpoint("place opened with its name", ok and wait("place.name", 10, exact=True), "place.screen/name missing (place detail needs the API)")
        for _ in range(8):
            if has("place.condition-error", exact=True) or has("place.condition-offline", exact=True): break
            scroll_down()
        shot = c.shot("1_error", "place.condition-error" if has("place.condition-error", exact=True) else None)
        c.step(3, "read card")
        c.result(1, has("place.condition-error", exact=True) and has("place.condition-retry", exact=True) and has("Couldn't load the condition"), f"error {has('place.condition-error', exact=True)}, offline {has('place.condition-offline', exact=True)}", [shot])
        c.result(2, has("place.screen", exact=True) and has("place.name", exact=True), "place.screen + place.name present", [shot])
    finally:
        adb("reverse", "tcp:3000", "tcp:3000")
    c.step(4, "restore + retry")
    tap("place.condition-retry", exact=True)
    c.result(3, wait("place.condition", 10, exact=True), "place.condition after retry", [c.shot("2_after_retry", "place.condition")])
