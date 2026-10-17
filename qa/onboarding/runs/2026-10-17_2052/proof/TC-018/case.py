import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': "Log-in fills only the account's empty fields",
 'priority': 'P1',
 'group': 'Supplementary',
 'requirement': 'AC8 — empty account fields are filled, locale untouched',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['QA user with experience null, interests empty, locale uz (SQL)',
           'Reset → complete onboarding with Beginner + Trails → tabs → Profile → Log in as the QA user',
           "Read the user's row"],
 'expected': ['Event guest_merge_result whose merged names the onboarding choices — QA events',
              'DB: experience beginner, interests {trails}, locale still uz — SQL on the LOCAL dev DB',
              'Event locale_applied {locale: uz} — QA events'],
 'focus': 'nav.tab-profile',
 'caption': {'expected': 'account filled'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    u = make_user("onb18"); set_account(u["username"], locale="uz")
    c.checkpoint("onboarding completed", first_run_to("companion", exp="beginner", interests=("trails",)) and lets_go(), "no tabs")
    c.checkpoint("log-in open", goto_profile() == "profile.guest" and (tap("profile.guest-login", exact=True) or True) and wait("auth.login", 10, exact=True), "no auth.login")
    t0 = mark(); ui_login(u["username"], PW, expect="profile.account")
    ev = wait_event("guest_merge_result", t0, 10); loc = wait_event("locale_applied", t0, 10)
    c.result(1, bool(ev) and "onboarding" in (ev.get("merged") or ""), f"event {ev}")
    exp, ints = db_choices(u["username"]); loc_db = sql(f"select locale from users where username='{u['username']}'")
    c.result(2, exp == "beginner" and ints.strip("{}") == "trails" and loc_db == "uz", f"db {exp}, {ints}, {loc_db}")
    c.result(3, bool(loc and loc.get("locale") == "uz"), f"locale_applied {loc}")
    deep_link("irbis://debug/lang/en")
