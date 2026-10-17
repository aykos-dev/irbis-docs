import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': "Level card: locked (required level 2 → 'Reach Level 2 to go here')",
 'priority': 'P0',
 'group': 'Core',
 'requirement': "AC8 — lock + 'Reach Level {n} to go here'",
 'env': 'Android · auto (adb)',
 'precondition': ['Guest (viewer level 1)', 'A place with required_level 2 (difficulty 2)'],
 'steps': ['Open its Place via the link → check: place.level-card', 'Read the card'],
 'expected': ["Card text contains 'Requires', 'Level 2' and 'Burrower or higher' — UI tree + screenshot",
              "place.level-locked is shown with 'Reach Level 2 to go here'; place.level-qualify and 'You qualify' "
              'are absent — UI tree + screenshot',
              'QA event place_viewed {requiredLevel: 2, qualifies: false} — QA event'],
 'focus': 'place.level-card',
 'caption': {'expected': "Card text contains 'Requires', 'Level 2' and 'Burrower or hi"}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = pick("required_level=2")
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
    c.result(1, "requires" in txt.lower() and "Level 2" in txt and "Burrower" in txt and "or higher" in txt, f"Requires/Level 2/Burrower: {'Requires' in txt}/{'Level 2' in txt}/{'Burrower or higher' in txt}", [shot])
    c.result(2, has("place.level-locked", exact=True) and "Reach Level 2 to go here" in txt and not has("place.level-qualify", exact=True) and "You qualify" not in txt, f"locked {has('place.level-locked', exact=True)}, qualify {has('place.level-qualify', exact=True)}", [shot])
    ev = wait_event("place_viewed", t0, 5)
    c.result(3, bool(ev) and ev.get("requiredLevel") == 2 and ev.get("qualifies") is False, f"event {ev}")
