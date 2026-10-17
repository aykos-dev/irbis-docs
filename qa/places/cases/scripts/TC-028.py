import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Level card: qualifies (required level 1)',
 'priority': 'P0',
 'group': 'Core',
 'requirement': "AC8 — 'Requires · Level 1 · Wanderer or higher' + green check 'You qualify'",
 'env': 'Android · auto (adb)',
 'precondition': ['Guest (viewer level 1)', 'A place with required_level 1 (difficulty 1)'],
 'steps': ['Open its Place via the link → check: place.level-card', 'Read the card'],
 'expected': ["Card text contains 'Requires', 'Level 1' and 'Wanderer or higher' — UI tree + screenshot",
              "place.level-qualify is shown with 'You qualify'; place.level-locked is absent — UI tree + screenshot",
              'QA event place_viewed {requiredLevel: 1, qualifies: true} — QA event'],
 'focus': 'place.level-card',
 'caption': {'expected': "Card text contains 'Requires', 'Level 1' and 'Wanderer or hi"}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = pick("required_level=1")
    t0 = mark()
    c.step(1, "open the place")
    c.checkpoint("Place opened", open_place_link(slug), "no place.screen")
    from drv import scroll_down
    for _ in range(3):
        if has("place.level-card", exact=True): break
        scroll_down()
    c.checkpoint("level card visible", has("place.level-card", exact=True), "no place.level-card")
    txt = screen_text()
    shot = c.shot("1_card", "place.level-card")
    c.result(1, "Requires" in txt and "Level 1" in txt and "Wanderer or higher" in txt, f"card text in screen: {'Requires' in txt}/{'Level 1' in txt}/{'Wanderer or higher' in txt}", [shot])
    c.result(2, has("place.level-qualify", exact=True) and "You qualify" in txt and not has("place.level-locked", exact=True), f"qualify {has('place.level-qualify', exact=True)}, locked {has('place.level-locked', exact=True)}", [shot])
    ev = wait_event("place_viewed", t0, 5)
    c.result(3, bool(ev) and ev.get("requiredLevel") == 1 and ev.get("qualifies") is True, f"event {ev}")
