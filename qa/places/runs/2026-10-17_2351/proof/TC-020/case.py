import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': "'Turn on' after one denial re-asks; after a second denial it opens app settings; granting there switches "
          'to device origin',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC6 — re-ask if the OS allows, else app settings; return with permission → device origin without '
                'restart',
 'env': 'Android · auto (adb)',
 'precondition': ["Guest, location permission reset to 'ask'",
                  'Mock device position = Tashkent centre',
                  'Explore opened once and denied (banner visible)'],
 'steps': ['Open Explore and deny once → check: banner shows',
           "Tap 'Turn on' → check: the system dialog appears again",
           "Deny again (now blocked); tap 'Turn on' → check: the app's settings screen opens",
           "Grant location (`pm grant`, the settings toggle's effect) and return to the app with Back"],
 'expected': ["After the first denial 'Turn on' shows the OS dialog again — UI tree + screenshot",
              "After the second denial 'Turn on' opens Android app settings for the Irbis package (not the dialog) — "
              'UI tree (settings screen text) + screenshot',
              "Back in the app without a restart: banner gone, header '… places near you', event explore_loaded "
              '{origin: device} after the return — UI tree + QA event'],
 'focus': 'explore.location-banner',
 'caption': {'expected': "After the first denial 'Turn on' shows the OS dialog again"}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    reset_permission(FINE); reset_permission(COARSE)
    mock_at(*TASHKENT)
    open_explore(wait_list=False)
    wait_any(["Don't allow", "Don’t allow"], 12)
    tap("Don't allow") if has("Don't allow") else tap("Don’t allow")
    c.checkpoint("Banner visible after denial", wait("explore.location-banner", 15, exact=True), "no banner")
    c.step(1, "Turn on (1st)")
    tap("explore.location-turn-on", exact=True)
    c.result(1, wait_any(["While using the app", "Don't allow", "Don’t allow"], 10) is not None, "OS dialog shown again", [c.shot("1_reask", None)])
    c.step(2, "deny again, Turn on")
    tap("Don't allow") if has("Don't allow") else tap("Don’t allow")
    wait("explore.location-banner", 10, exact=True)
    tap("explore.location-turn-on", exact=True)
    sets = wait_any(["App info", "Permissions", "Uninstall", "Force stop"], 10)
    c.result(2, sets is not None and not has("While using the app"), f"settings screen marker {sets!r}", [c.shot("2_settings", None)])
    c.step(3, "grant and return")
    grant_location(True)
    t0 = mark()
    launch()  # Back from app settings can land on a Google settings screen; resume the app
    wait("explore.screen", 10, exact=True)
    ev = wait_event("explore_loaded", t0, 15, lambda p: p.get("origin") == "device")
    c.result(3, bool(ev) and not has("explore.location-banner", exact=True) and "near you" in (text_of("explore.count") or ""), f"event {ev}, header {text_of('explore.count')!r}", [c.shot("3_back", "explore.count")])
