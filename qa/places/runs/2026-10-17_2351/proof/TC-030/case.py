import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Level names 1–7 and the qualify boundary (level 1 vs 2)',
 'priority': 'P2',
 'group': 'Variants',
 'requirement': 'AC8 — names Wanderer … Snow Legend; boundary requiredLevel 1 qualifies, 2 does not',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest (viewer level 1)',
                  'One local place whose required_level is changed 1 → 7 through set_place() (restored after the '
                  'run)'],
 'steps': ["For n in 1..7 set the place's required_level to n, reopen Place, read the card"],
 'expected': ['Names shown: 1 Wanderer, 2 Burrower, 3 Pathfinder, 4 Ridge Walker, 5 Mountain Guardian, 6 Sky '
              "Watcher, 7 Snow Legend, each as 'Level n · <name> or higher' — UI tree",
              "Only n = 1 shows 'You qualify' (place.level-qualify); n = 2…7 show the lock and 'Reach Level n to go "
              "here' — UI tree + screenshots"],
 'focus': 'place.level-card',
 'caption': {'expected': 'Names shown: 1 Wanderer, 2 Burrower, 3 Pathfinder, 4 Ridge W'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    from drv import scroll_down
    slug = pick("required_level=1")
    names, flags = [], []
    for n in range(1, 8):
        c.step(n, f"required level {n}")
        set_place(slug, required_level=n)
        c.checkpoint(f"Place opened (level {n})", open_place_link(slug), "no place.screen")
        for _ in range(3):
            if has("place.level-card", exact=True): break
            scroll_down()
        txt = screen_text()
        names.append(f"Level {n} · {LEVEL_NAMES[n]}" in txt and "or higher" in txt)
        flags.append((has("place.level-qualify", exact=True), has("place.level-locked", exact=True) and f"Reach Level {n} to go here" in txt))
        c.shot(f"lvl{n}", "place.level-card")
        sh("am", "force-stop", PKG); time.sleep(0.5)
    c.result(1, all(names), f"names ok per level: {names}")
    ok = flags[0] == (True, False) or flags[0][0]
    c.result(2, flags[0][0] and not flags[0][1] and all((not q) and l for q, l in flags[1:]), f"(qualify, locked) per level: {flags}")
