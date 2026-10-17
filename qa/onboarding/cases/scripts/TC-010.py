import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Sign-up after onboarding: the choices land on the new account',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC7 — choices stored on the phone, merged on sign-up',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['Reset → complete onboarding with Weekend hiker + Peaks, Lakes → tabs',
           'Profile → Sign up as a new QA user (terms accepted) → check: signed-in Profile',
           "Read the user's row in the LOCAL dev DB"],
 'expected': ['Event guest_merge_result after sign-up whose merged includes onboarding — QA events',
              'DB: users.experience = weekend and interests = {peaks,lakes} for the new user — SQL on the LOCAL dev '
              'DB'],
 'focus': 'profile.account',
 'caption': {'expected': 'signed-in Profile'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("onboarding completed", first_run_to("companion") and lets_go(), "no tabs")
    name = uname("onb10")
    c.checkpoint("sign-up form open", goto_profile() == "profile.guest" and (tap("profile.guest-signup", exact=True) or True) and wait("auth.signup", 10, exact=True), "no auth.signup")
    c.step(3, "Sign up"); t0 = mark()
    ui_signup(name, PW)
    ok = wait("profile.account", 20, exact=True)
    ev = wait_event("guest_merge_result", t0, 10)
    c.result(1, bool(ev) and "onboarding" in (ev.get("merged") or ""), f"event {ev}", [c.shot("1_account")])
    exp, ints = db_choices(name)
    c.result(2, exp == "weekend" and set(ints.strip("{}").split(",")) == {"peaks", "lakes"}, f"db experience={exp}, interests={ints}")
