import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Reveal animation and haptic on entering Companion',
 'priority': 'P2',
 'group': 'Supplementary',
 'requirement': 'AC6 — reveal animation + success haptic',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['Reset → … → Companion; capture screenshots right after entry (0.2 s, 0.6 s, 1.2 s)'],
 'expected': ['Backpack pop, panda scale-in and confetti are visible across the three frames and settle by 1.2 s — '
              'screenshots (needs eyes)',
              'Success haptic — manual on the phone (cannot be observed over adb)'],
 'focus': 'onboarding.companion',
 'caption': {'expected': 'reveal frames'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Interests shown", first_run_to("interests"), "no onboarding.interests")
    tap("onboarding.interest-peaks", exact=True); tap("onboarding.continue", exact=True)
    a = c.shot("1_t0"); time.sleep(0.4); b = c.shot("2_t06"); time.sleep(0.6); d = c.shot("3_t12")
    c.result(1, None, "compare the three crops: animation progresses, settles", [a, b, d])
    c.result(2, None, "manual: haptic on the phone", [])
