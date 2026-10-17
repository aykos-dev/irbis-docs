import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Steps 2–4 header: progress, back chevron, Android back',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC3 — header on steps 2–4',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['Reset → Meet Irbis',
           'Get started → read progress (Language)',
           'Continue → read progress (Experience); pick Weekend hiker; Continue → read progress (Interests)',
           'Tap the back chevron → Experience',
           'Press Android back → Language',
           'Press Android back → Meet Irbis'],
 'expected': ['Progress text is "Step 1 of 4" on Language, "Step 2 of 4" on Experience, "Step 3 of 4" on Interests — '
              'UI tree (onboarding.progress)',
              'Chevron on Interests lands on onboarding.experience — UI tree',
              'Android back on Experience lands on onboarding.language; on Language lands on onboarding.welcome — UI '
              'tree'],
 'focus': 'onboarding.progress',
 'caption': {'expected': 'Step N of 4'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Meet Irbis shown", first_run_to("welcome"), "no onboarding.welcome")
    c.step(2, "Language"); tap("onboarding.get-started", exact=True); wait("onboarding.language", 10, exact=True)
    p1 = progress_text(); s1 = c.shot("1_language")
    c.step(3, "Experience, Interests")
    to_experience(); p2 = progress_text(); s2 = c.shot("2_experience")
    to_interests(); p3 = progress_text(); s3 = c.shot("3_interests")
    c.result(1, (p1, p2, p3) == ("Step 1 of 4", "Step 2 of 4", "Step 3 of 4"), f"progress {p1!r} {p2!r} {p3!r}", [s1, s2, s3])
    c.step(4, "Back chevron"); tap("onboarding.back", exact=True)
    a = wait("onboarding.experience", 5, exact=True)
    c.result(2, a, "experience" if a else "not on experience", [c.shot("4_back")])
    c.step(5, "Android back"); back()
    b = wait("onboarding.language", 5, exact=True)
    c.step(6, "Android back"); back()
    d = wait("onboarding.welcome", 5, exact=True)
    c.result(3, b and d, f"language={b}, welcome={d}", [c.shot("5_welcome")])
