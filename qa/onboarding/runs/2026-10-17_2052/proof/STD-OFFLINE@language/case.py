import os, sys, time
from drv import *  # noqa
from _std import screen  # noqa

META = {"title": "Offline shows a persistent banner and keeps the screen", "priority": "P2", "group": "Standards",
        "requirement": "engineering-standards §11 — offline state", "env": "Android · auto (adb)",
        "precondition": ["screen loaded online"], "steps": ["Open the screen online", "Wi-Fi and mobile data off"],
        "expected": ["`app.offline-banner` visible at 5 s and still at 15 s (not a toast) — screenshot",
                     "The screen's content stays visible (cached, not blanked) — screenshot"],
        "caption": {"expected": "offline banner, content kept"}}


def run(c):
    open_screen, root = screen(c)
    c.step(1, "Open the screen online")
    c.checkpoint("screen opened", open_screen(c), root)
    c.step(2, "Wi-Fi and mobile data off")
    set_network(False, False)
    try:
        b1 = wait("app.offline-banner", 5, exact=True)
        time.sleep(10)
        b2 = has("app.offline-banner", exact=True)
        shot = c.shot("offline", focus=None)
        c.result(1, b1 and b2, f"banner at 5 s: {b1}, at 15 s: {b2}", [shot])
        c.result(2, has(root, exact=True), f"{root} visible: {has(root, exact=True)}", [shot])
    finally:
        set_network(True, True)
        wait_gone("app.offline-banner", 10)
