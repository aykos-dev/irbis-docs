import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': "Companion: Bao reveal, Let's go goes to the tabs, Android back returns to Interests",
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC6 — Onb5',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['Reset → … → Companion (Weekend hiker, Peaks + Lakes) → check: onboarding.companion',
           'Read texts, header',
           'Press Android back → Interests',
           "Continue again → Companion → Let's go!"],
 'expected': ['"Meet Bao, your panda cub!" and "Wanderer" with "clumsy & cozy" are on screen; no onboarding.back / '
              'onboarding.close / onboarding.progress node — UI tree + screenshot',
              'Event onboarding_step {step: companion} on entry — QA events',
              'Android back → onboarding.interests with Peaks and Lakes still selected — UI tree',
              "Let's go! → nav.tab-profile — UI tree"],
 'focus': 'onboarding.companion',
 'caption': {'expected': 'Bao reveal'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    t0 = mark()
    c.checkpoint("Companion shown", first_run_to("companion"), "no onboarding.companion")
    ev = wait_event("onboarding_step", t0, 3, lambda p: p.get("step") == "companion")
    texts_ = " | ".join(n["text"] for n in nodes() if n["text"])
    nohdr = not any(has(t, exact=True) for t in ("onboarding.back", "onboarding.close", "onboarding.progress"))
    c.result(1, "Meet Bao, your panda cub!" in texts_ and "Wanderer" in texts_ and "clumsy & cozy" in texts_ and nohdr, f"header absent={nohdr}", [c.shot("1_companion")])
    c.result(2, bool(ev), f"event {ev}")
    c.step(3, "Android back"); back()
    ok = wait("onboarding.interests", 5, exact=True)
    c.result(3, ok and selected("onboarding.interest-peaks") and selected("onboarding.interest-lakes"), f"interests={ok}", [c.shot("2_back")])
    c.step(4, "Continue, Let's go!")
    tap("onboarding.continue", exact=True); wait("onboarding.companion", 10, exact=True)
    c.result(4, lets_go(), "tabs", [c.shot("3_tabs")])
