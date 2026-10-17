import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Experience tiles show their art and 1 / 2 / 4 boots',
 'priority': 'P2',
 'group': 'Supplementary',
 'requirement': 'AC4 — art and boots per tile',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['Reset → … → Experience'],
 'expected': ['Beginner (trail art, 1 boot), Weekend hiker (lake art, 2 boots), Experienced (peak art, 4 boots) match '
              'the canvas — screenshot (needs eyes)'],
 'focus': 'onboarding.experience',
 'caption': {'expected': 'tiles with boots'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Experience shown", first_run_to("experience"), "no onboarding.experience")
    c.result(1, None, "judge the crop against design/canvas Onb3Experience", [c.shot("1_tiles")])
