import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': "Place distance label 'From you' with the device origin",
 'priority': 'P1',
 'group': 'Variants',
 'requirement': "AC7 — label 'From you' / 'From Tashkent'",
 'env': 'Android · auto (adb)',
 'precondition': ['Guest', 'Location granted, mock position 8,400 m north of a chosen peak'],
 'steps': ["Open the peak's Place from its Explore card", 'Read place.distance and the label'],
 'expected': ["place.distance shows '8.4 km' with the label 'From you' and not 'From Tashkent' — UI tree + "
              'screenshot'],
 'focus': 'place.distance',
 'caption': {'expected': "place.distance shows '8.4 km' with the label 'From you' and "}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = pick("type='peak' and difficulty=1")
    la0, ln0 = [float(x) for x in sql(f"select latitude || ' ' || longitude from places where slug='{slug}'").split()]
    la, ln = offset(la0, ln0, metres_north=8400)
    reset_permission(FINE); grant_location(True); mock_at(la, ln)
    relaunch(); wait("nav.tab-explore", 20, exact=True)
    c.checkpoint("Explore list loaded with the device origin", open_explore(), "no explore list")
    c.step(1, "open the place from its Explore card (a link carries no origin)")
    c.checkpoint("Place opened", open_place(slug), "no place.screen")
    time.sleep(1)
    txt = screen_text().lower()  # the label is rendered upper-case
    c.result(1, "from you" in txt and "from tashkent" not in txt and "8.4 km" in txt, f"labels you/Tashkent {'from you' in txt}/{'from tashkent' in txt}", [c.shot("1_dist", "place.distance")])
