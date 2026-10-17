import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Close (✕) on a step ends onboarding on the tabs, keeps the language, saves no choices',
 'priority': 'P1',
 'group': 'Supplementary',
 'requirement': 'AC3 — ✕ ends onboarding',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['Reset → Language → pick Русский → Continue → Weekend hiker → Continue → Interests, Peaks → ✕ → check: '
           'nav.tab-profile',
           'Cold start',
           'Profile → Sign up as a new QA user',
           "Read the user's row"],
 'expected': ['Event onboarding_end {via: close, interestsCount: 0} with no experience prop — QA events',
              'Tabs are Russian (nav.tab-profile "Профиль") and stay Russian after the cold start; no onboarding node '
              'in 5 s — UI tree',
              'DB: experience null and interests empty for the new user — SQL on the LOCAL dev DB (no choices saved by '
              '✕)'],
 'focus': 'nav.tab-profile',
 'caption': {'expected': 'tabs in Russian'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Language shown", first_run_to("language"), "no onboarding.language")
    tap("onboarding.lang-ru", exact=True); time.sleep(0.5)
    to_experience(); to_interests(); tap("onboarding.interest-peaks", exact=True)
    c.step(2, "Tap ✕"); t0 = mark()
    tap("onboarding.close", exact=True)
    ok = wait(TABS, 10, exact=True); ev = wait_event("onboarding_end", t0, 5)
    c.result(1, bool(ev and ev.get("via") == "close" and ev.get("interestsCount") == 0 and not ev.get("experience")), f"event {ev}")
    relaunch(); first = wait_any([TABS, "onboarding.splash", "onboarding.welcome"], 20)
    tab = find(TABS, exact=True); seen = False; end = time.time() + 5
    while time.time() < end:
        seen = seen or has("onboarding.splash", exact=True); time.sleep(0.3)
    c.result(2, ok and first == TABS and not seen and bool(tab and "Профиль" in (tab["desc"] + tab["text"])), f"first {first}, tab {tab and (tab['desc'] or tab['text'])!r}", [c.shot("1_cold")])
    deep_link("irbis://debug/lang/en"); name = uname("onb13")
    c.checkpoint("sign-up open", goto_profile() == "profile.guest" and (tap("profile.guest-signup", exact=True) or True) and wait("auth.signup", 10, exact=True), "no auth.signup")
    ui_signup(name, PW); wait("profile.account", 20, exact=True); time.sleep(2)
    exp, ints = db_choices(name)
    c.result(3, exp == "null" and ints.strip("{}") == "", f"db experience={exp}, interests={ints!r}")
