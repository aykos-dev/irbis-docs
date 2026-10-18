import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': "Status null: grey 'Condition not available yet', no chip",
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC7 — status null → grey empty card',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done',
                  'Peak PLACE with no forecast, no closure/override, season open (status null)'],
 'steps': ['set_place season open, delete the forecast and recompute',
           'Cold-start, open the place → check: a card testID shows'],
 'expected': ["`place.condition-empty` shows 'Condition not available yet'; `place.condition-status` is absent — UI "
              'tree + screenshot',
              'API `GET /v1/places/{id}/condition` status is null — API'],
 'caption': {'expected': "`place.condition-empty` shows 'Condition not available yet'; `place.co"},
 'focus': 'place.condition-empty'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = slug0(); set_place(slug, hazards=[], season=["possible"] * 12)
    c.step(1, "clear forecast"); seed(slug, clear=True)
    c.step(2, "open place")
    t0, tid, shot = view(c, slug, "1_empty")
    c.checkpoint("a condition card shown", tid is not None, tid)
    c.result(1, tid == "place.condition-empty" and has("Condition not available yet") and not has("place.condition-status", exact=True), f"card {tid}", [shot])
    c.result(2, cond(slug)["status"] is None, f"api status {cond(slug)['status']}")
