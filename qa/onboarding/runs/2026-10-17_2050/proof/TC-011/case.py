import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': "Log-in: the account's values win, the account language is applied",
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC8 — account wins on log-in',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['QA user with experience beginner, interests {caves}, locale ru (SQL)',
           'Reset (app English) → complete onboarding with Experienced + Peaks, Lakes, Trails → tabs',
           'Profile → Log in as the QA user → check: signed-in',
           "Read the user's row"],
 'expected': ['Event guest_merge_result whose skipped names onboarding / locale (nothing overwritten) — QA events',
              'Event locale_applied {locale: ru} and the tab labels turn Russian (nav.tab-profile content-desc '
              '"Профиль") — QA events + UI tree',
              'DB: experience still beginner, interests still {caves}, locale still ru — SQL on the LOCAL dev DB'],
 'focus': 'nav.tab-profile',
 'caption': {'expected': 'tabs in Russian'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    ensure_guest()
    u = make_user("onb11"); set_account(u["username"], "beginner", ["caves"], "ru")
    c.checkpoint("onboarding completed", first_run_to("companion", exp="experienced", interests=("peaks", "lakes", "trails")) and lets_go(), "no tabs")
    c.checkpoint("log-in form open", goto_profile() == "profile.guest" and (tap("profile.guest-login", exact=True) or True) and wait("auth.login", 10, exact=True), "no auth.login")
    c.step(3, "Log in"); t0 = mark()
    fill_ok = ui_login(u["username"], PW, expect="profile.account")
    ev = wait_event("guest_merge_result", t0, 10); loc = wait_event("locale_applied", t0, 10)
    skipped = (ev or {}).get("skipped") or ""
    m = (ev or {}).get("merged") or ""
    c.result(1, bool(ev) and "experience" not in m and "locale" not in m and "interests" not in m, f"event {ev}")
    tab = find("nav.tab-profile", exact=True)
    c.result(2, bool(loc and loc.get("locale") == "ru") and bool(tab and "Профиль" in (tab["desc"] + tab["text"])), f"locale_applied {loc}, tab {tab and (tab['desc'] or tab['text'])!r}", [c.shot("1_tabs_ru")])
    exp, ints = db_choices(u["username"])
    loc_db = sql(f"select locale from users where username='{u['username']}'")
    c.result(3, exp == "beginner" and ints.strip("{}") == "caves" and loc_db == "ru", f"db {exp}, {ints}, {loc_db}")
    deep_link("irbis://debug/lang/en")
