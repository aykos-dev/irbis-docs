import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': "Let's go ends onboarding; the next cold start goes straight to the tabs",
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC1 — flag saved, later cold start has no in-app splash',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['Walk Welcome → Language → Experience (Weekend hiker) → Interests (Peaks, Lakes) → Companion → check: '
           'onboarding.companion',
           "Tap Let's go! → check: nav.tab-profile",
           'Force-stop and cold start; watch 5 s'],
 'expected': ['Event onboarding_end {via: finish, experience: weekend, interestsCount: 2} — QA events',
              "Tab bar (nav.tab-profile) shown after Let's go! — UI tree + screenshot",
              'After the cold start nav.tab-profile shows and no onboarding.splash / onboarding.welcome node appears '
              'in 5 s — UI tree (polled)'],
 'focus': 'nav.tab-profile',
 'caption': {'expected': 'tabs, no onboarding'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("reached Companion", first_run_to("companion"), "no onboarding.companion")
    c.step(2, "Tap Let's go!"); t0 = mark()
    tap("onboarding.lets-go", exact=True)
    ok = wait(TABS, 10, exact=True)
    ev = wait_event("onboarding_end", t0, 5)
    shot = c.shot("2_tabs")
    c.result(1, bool(ev and ev.get("via") == "finish" and ev.get("experience") == "weekend" and ev.get("interestsCount") == 2), f"event {ev}")
    c.result(2, ok, "tabs shown" if ok else "no tab bar", [shot])
    c.step(3, "Cold start")
    relaunch(); first = wait_any([TABS, "onboarding.splash", "onboarding.welcome"], 20)
    bad = False
    end = time.time() + 5
    while time.time() < end:
        if has("onboarding.splash", exact=True) or has("onboarding.welcome", exact=True):
            bad = True
        time.sleep(0.3)
    c.result(3, first == TABS and not bad, f"first node {first}, onboarding seen={bad}", [c.shot("3_cold")])
