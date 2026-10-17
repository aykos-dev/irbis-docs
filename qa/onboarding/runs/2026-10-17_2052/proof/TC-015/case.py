import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Interests BVA: 1 and 5 selected, Continue disabled again at 0',
 'priority': 'P1',
 'group': 'Supplementary',
 'requirement': 'AC5 — boundaries 0 / 1 / 5',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['Reset → … → Interests',
           'Select all five (Peaks, Caves, Lakes, Camping, Trails)',
           'Deselect all five one by one'],
 'expected': ['With five selected the counter starts "5 selected" and Continue is enabled — UI tree + screenshot',
              'After deselecting down to 1 the counter starts "1 selected" and Continue is enabled — UI tree',
              'After the last deselect (0) Continue is disabled — UI tree + screenshot'],
 'focus': 'onboarding.interests',
 'caption': {'expected': '5 selected'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Interests shown", first_run_to("interests"), "no onboarding.interests")
    names = ["peaks", "caves", "lakes", "camping", "trails"]
    def cnt():
        n = find("onboarding.interests-count", exact=True); return (n["text"] or n["desc"]) if n else ""
    for n in names: tap(f"onboarding.interest-{n}", exact=True)
    c.result(1, cnt().startswith("5 selected") and enabled("onboarding.continue"), f"counter {cnt()!r}", [c.shot("1_five")])
    for n in names[:4]: tap(f"onboarding.interest-{n}", exact=True)
    c.result(2, cnt().startswith("1 selected") and enabled("onboarding.continue"), f"counter {cnt()!r}", [c.shot("2_one")])
    tap("onboarding.interest-trails", exact=True)
    c.result(3, not enabled("onboarding.continue"), f"continue enabled={enabled('onboarding.continue')}", [c.shot("3_zero")])
