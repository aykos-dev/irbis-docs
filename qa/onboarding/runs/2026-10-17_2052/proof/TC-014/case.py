import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Closing Log in returns to Meet Irbis',
 'priority': 'P1',
 'group': 'Supplementary',
 'requirement': 'AC2 — closing Log in returns to Onb1',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['Reset → Meet Irbis → I already have an account → check: auth.login',
           'Close the log-in screen (Continue as guest, else Android back)'],
 'expected': ['onboarding.welcome is shown again and auth.login is gone; no onboarding_end event — UI tree + QA '
              'events'],
 'focus': 'onboarding.welcome',
 'caption': {'expected': 'back on Meet Irbis'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Meet Irbis shown", first_run_to("welcome"), "no onboarding.welcome")
    tap("onboarding.have-account", exact=True)
    c.checkpoint("log-in open", wait("auth.login", 10, exact=True), "no auth.login")
    t0 = mark()
    if has("auth.continue-guest", exact=True): tap("auth.continue-guest", exact=True)
    else: back()
    ok = wait("onboarding.welcome", 5, exact=True)
    c.result(1, ok and not has("auth.login", exact=True) and not events().since(t0, "onboarding_end"), f"welcome={ok}", [c.shot("1_back")])
