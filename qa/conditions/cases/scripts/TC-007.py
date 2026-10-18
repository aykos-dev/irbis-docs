import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': "Place without hazards keeps 'Hazards not set yet'",
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC7 — places without hazards keep the empty line',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done', 'Peak PLACE with hazards = [] and a MILD forecast'],
 'steps': ['set_place hazards [], seed', 'Cold-start, open the place, scroll to the hazards section'],
 'expected': ["Text 'Hazards not set yet' is shown and no `place.hazard.<h>` row exists — UI tree + screenshot"],
 'caption': {'expected': "Text 'Hazards not set yet' is shown and no `place.hazard.<h>` row exis"},
 'focus': 'place.screen'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = slug0(); set_place(slug, hazards=[], season=["possible"] * 12)
    c.step(1, "seed"); seed(slug)
    c.step(2, "open place")
    view(c, slug, "0_open")
    ok = False
    for _ in range(8):
        if has("Hazards not set yet"):
            ok = True; break
        scroll_down()
    shot = c.shot("1_hazards")
    rows = [h for h in ("avalanche", "flood", "mudslide", "heat", "road") if has(f"place.hazard.{h}", exact=True)]
    c.result(1, ok and not rows, f"empty line {ok}, rows {rows}", [shot])
