import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Signed in at launch skips onboarding and sets the flag',
 'priority': 'P1',
 'group': 'Supplementary',
 'requirement': 'AC1 — already signed in at launch',
 'env': 'Android · auto (adb)',
 'precondition': ['QA user signed in; onboarding flag cleared by the reset link'],
 'steps': ['QA user signed in on the tabs (onboarding done); open the reset link, then cold start → check: '
           'nav.tab-profile',
           'Sign out through Profile → cold start; watch 5 s'],
 'expected': ['Cold start while signed in lands on nav.tab-profile, no onboarding.splash within 5 s — UI tree (polled)',
              'After signing out (QA user) and a cold start: tabs again with no onboarding — the flag was set at the '
              'signed-in launch — UI tree (polled)'],
 'focus': 'nav.tab-profile',
 'caption': {'expected': 'tabs, no onboarding'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    u = make_user("onb12")
    c.checkpoint("signed in", start_onboarding() and to_language() and (tap("onboarding.close", exact=True) or True) and wait(TABS, 10, exact=True) and goto_profile() == "profile.guest" and (tap("profile.guest-login", exact=True) or True) and ui_login(u["username"], PW, expect="profile.account"), "not signed in")
    c.step(2, "Reset flag, cold start while signed in")
    deep_link("irbis://debug/onboarding/reset"); wait("onboarding.welcome", 10, exact=True)
    relaunch(); first = wait_any([TABS, "onboarding.splash", "onboarding.welcome"], 20)
    seen = False; end = time.time() + 5
    while time.time() < end:
        seen = seen or has("onboarding.splash", exact=True) or has("onboarding.welcome", exact=True); time.sleep(0.3)
    c.result(1, first == TABS and not seen, f"first {first}, onboarding seen={seen}", [c.shot("1_signed_in")])
    c.step(3, "Sign out, cold start")
    c.checkpoint("signed out", A.sign_out_ui() if goto_profile() else False, "sign-out failed")
    relaunch(); first = wait_any([TABS, "onboarding.splash", "onboarding.welcome"], 20)
    seen = False; end = time.time() + 5
    while time.time() < end:
        seen = seen or has("onboarding.splash", exact=True) or has("onboarding.welcome", exact=True); time.sleep(0.3)
    c.result(2, first == TABS and not seen, f"first {first}, onboarding seen={seen}", [c.shot("2_guest")])
