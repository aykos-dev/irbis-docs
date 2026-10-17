import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'I already have an account: log-in from Meet Irbis ends onboarding on the tabs',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC2 — Onb1 → Log in → tabs, flag saved',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['QA user created via API',
           'Reset → Meet Irbis → tap I already have an account → check: auth.login',
           'Log in as the QA user → check: nav.tab-profile',
           'Cold start'],
 'expected': ['auth.login opens over onboarding — UI tree + screenshot',
              'Event onboarding_end {via: login} and the tab bar shows — QA events + UI tree',
              'Cold start goes to the tabs, no onboarding.splash within 5 s — UI tree (polled)'],
 'focus': 'auth.login',
 'caption': {'expected': 'log-in from Onb1'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    u = make_user("onb4")
    c.checkpoint("Meet Irbis shown", first_run_to("welcome"), "no onboarding.welcome")
    c.step(2, "I already have an account")
    tap("onboarding.have-account", exact=True)
    ok = wait("auth.login", 10, exact=True)
    c.result(1, ok, "log-in screen" if ok else "no auth.login", [c.shot("1_login")])
    c.checkpoint("log-in screen open", ok, "no auth.login")
    c.step(3, "Log in"); t0 = mark()
    logged = login_ui(u["username"])
    ev = wait_event("onboarding_end", t0, 8)
    c.result(2, logged and bool(ev and ev.get("via") == "login"), f"tabs={logged}, event={ev}", [c.shot("2_tabs")])
    c.step(4, "Cold start")
    relaunch(); first = wait_any([TABS, "onboarding.splash", "onboarding.welcome"], 20)
    seen = False
    end = time.time() + 5
    while time.time() < end:
        seen = seen or has("onboarding.splash", exact=True)
        time.sleep(0.3)
    c.result(3, first == TABS and not seen, f"first {first}, splash seen={seen}", [c.shot("3_cold")])
