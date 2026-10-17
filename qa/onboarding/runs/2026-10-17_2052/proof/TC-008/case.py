import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Interests: nothing preselected, counter and Continue follow the selection',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC5 — Onb4 toggles, counter, Continue',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['Reset → … → Interests (Weekend hiker chosen) → check: onboarding.interests',
           'Read counter and Continue',
           'Tap Peaks',
           'Tap Caves, Lakes',
           'Tap Peaks again'],
 'expected': ['No onboarding.interest-* is selected; Continue disabled — UI tree + screenshot',
              'After Peaks: counter starts "1 selected" and contains "Your weekly path mixes these with safe options '
              'for the season."; Continue enabled — UI tree',
              'After Caves + Lakes: counter starts "3 selected" — UI tree',
              'Peaks tapped again toggles off: peaks unselected, counter "2 selected" — UI tree'],
 'focus': 'onboarding.interests',
 'caption': {'expected': 'interest tiles + counter'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Interests shown", first_run_to("interests"), "no onboarding.interests")
    names = ["peaks", "caves", "lakes", "camping", "trails"]
    def cnt():
        n = find("onboarding.interests-count", exact=True); return (n["text"] or n["desc"]) if n else ""
    c.result(1, not any(selected(f"onboarding.interest-{n}") for n in names) and not enabled("onboarding.continue"), f"counter {cnt()!r}", [c.shot("1_initial")])
    c.step(3, "Peaks"); tap("onboarding.interest-peaks", exact=True)
    c.result(2, cnt().startswith("1 selected") and "Your weekly path mixes these with safe options for the season." in (cnt() + " " + " ".join(t["text"] for t in nodes())) and enabled("onboarding.continue"), f"counter {cnt()!r}", [c.shot("2_one")])
    c.step(4, "Caves, Lakes"); tap("onboarding.interest-caves", exact=True); tap("onboarding.interest-lakes", exact=True)
    c.result(3, cnt().startswith("3 selected"), f"counter {cnt()!r}", [c.shot("3_three")])
    c.step(5, "Peaks again"); tap("onboarding.interest-peaks", exact=True)
    c.result(4, not selected("onboarding.interest-peaks") and cnt().startswith("2 selected"), f"counter {cnt()!r}", [c.shot("4_two")])
