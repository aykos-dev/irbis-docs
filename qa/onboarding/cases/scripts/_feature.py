"""onboarding feature: PLAN (rendered into Test_onboarding.md), SCREENS (standards suite), shared helpers.

Reuses the auth helpers (API/SQL on the LOCAL dev DB, throwaway `qa_<case>_<n>` users, log-in/sign-up UI helpers).
Onboarding state is driven only through the QA deep links:
  irbis://debug/onboarding/reset  forget the done flag + saved choices, restart at Splash
  irbis://debug/onboarding/done   mark done (opens Debug)
  irbis://debug/lang/<uz|ru|en>   persisted app language (opens Debug)"""
import importlib.util
import os
import time

from drv import PKG, back, deep_link, find, has, mark, nodes, relaunch, sh, tap, wait, wait_any, wait_event, wait_gone  # noqa: F401
from config import QA_ROOT  # noqa: E402

_p = os.path.join(QA_ROOT, "auth", "cases", "scripts", "_feature.py")
_spec = importlib.util.spec_from_file_location("auth_feature", _p)
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)
api, sql, make_user, PW = A.api, A.sql, A.make_user, A.PW
ensure_guest, goto_profile, open_login, open_signup, ui_login, ui_signup, uname = (
    A.ensure_guest, A.goto_profile, A.open_login, A.open_signup, A.ui_login, A.ui_signup, A.uname)

TABS = "nav.tab-profile"
STEP_ROOT = {"welcome": "onboarding.welcome", "language": "onboarding.language", "experience": "onboarding.experience",
             "interests": "onboarding.interests", "companion": "onboarding.companion"}


def before_case():
    A.before_case()   # clears login_attempts on the LOCAL dev DB


def start_onboarding(lang="en"):
    """Reset to a first run with app language `lang`; returns True when Meet Irbis (Onb1) shows."""
    deep_link(f"irbis://debug/lang/{lang}")
    time.sleep(1)
    deep_link("irbis://debug/onboarding/reset")
    return wait("onboarding.welcome", 10, exact=True)


def cold_start():
    """Force-stop + launch; returns the first of tabs / splash / welcome that shows."""
    relaunch()
    return wait_any([TABS, "onboarding.splash", "onboarding.welcome"], 20)


def to_language():
    tap("onboarding.get-started", exact=True)
    return wait("onboarding.language", 10, exact=True)


def to_experience():
    tap("onboarding.continue", exact=True)
    return wait("onboarding.experience", 10, exact=True)


def to_interests(exp="weekend"):
    tap(f"onboarding.exp-{exp}", exact=True)
    tap("onboarding.continue", exact=True)
    return wait("onboarding.interests", 10, exact=True)


def to_companion(interests=("peaks", "lakes")):
    for i in interests:
        tap(f"onboarding.interest-{i}", exact=True)
    tap("onboarding.continue", exact=True)
    return wait("onboarding.companion", 10, exact=True)


def walk_to(step, exp="weekend", interests=("peaks", "lakes")):
    """From a first run at Onb1 walk forward to `step` (language|experience|interests|companion) with the choices."""
    steps = [("language", to_language), ("experience", to_experience),
             ("interests", lambda: to_interests(exp)), ("companion", lambda: to_companion(interests))]
    for name, fn in steps:
        if not fn():
            return False
        if name == step:
            return True
    return False


def first_run_to(step, **kw):
    return start_onboarding() and (step == "welcome" or walk_to(step, **kw))


def lets_go():
    tap("onboarding.lets-go", exact=True)
    return wait(TABS, 10, exact=True)


def selected(tid):
    n = find(tid, exact=True)
    return bool(n and (n["selected"] == "true" or n["checked"] == "true"))


def enabled(tid):
    n = find(tid, exact=True)
    return bool(n and n["enabled"] == "true")


def progress_text():
    import re
    for n in nodes():
        if re.fullmatch(r"step \d of 4", n["text"].strip(), re.I):
            return n["text"].strip()
    return None


def db_choices(username):
    """(experience, interests) of a QA user from the LOCAL dev DB."""
    r = sql(f"select coalesce(experience::text,'null') || '|' || coalesce(interests::text,'') from users where username='{username}'")
    exp, _, ints = r.partition("|")
    return exp, ints


def set_account(username, experience=None, interests=None, locale=None):
    """QA-only test isolation on the LOCAL dev DB: give a QA user pre-set profile values."""
    sets = []
    if experience:
        sets.append(f"experience='{experience}'")
    if interests is not None:
        sets.append("interests='{" + ",".join(interests) + "}'")
    if locale:
        sets.append(f"locale='{locale}'")
    if sets:
        sql(f"update users set {', '.join(sets)} where username='{username}'")


def login_ui(username):
    """On a log-in screen: fill and submit; True once a signed-in tab bar shows."""
    return ui_login(username, PW, expect=TABS)


def to_guest_profile():
    """Onboarding already ended (tabs), guest: open Profile and make sure it is the guest one."""
    return goto_profile() == "profile.guest"


PLAN = {
    "spec": "features/onboarding.md",
    "resources": [("Android", "emulator pixel-8a emulating the S25 Ultra (session.py up); devRelease APK uz.irbis.app.dev, device UI English"),
                  ("Backend", "irbis-api `npm run start:dev` on :3000 (branch feat/onboarding, migration onboarding_profile applied); "
                              "Postgres container `irbis-api-db-1`; `adb reverse tcp:3000 tcp:3000`"),
                  ("Isolation", "every case starts with `irbis://debug/lang/en` + `irbis://debug/onboarding/reset` (clears the done flag AND saved "
                                "choices on the phone); `before_case()` clears `login_attempts`; each case makes its own `qa_<case>_<n>` user; "
                                "account values for AC8 are set with SQL on the LOCAL dev DB"),
                  ("Shared reset note", "A fresh install or cleared app data now opens onboarding, not the tabs. Auth cases that clear data or "
                                        "reinstall must call `irbis://debug/onboarding/done` first (auth `launch_app` waits for nav.tab-profile). "
                                        "Existing auth cases that only force-stop are unaffected once the done flag is set."),
                  ("Covered elsewhere", "AC7 API validation matrix and migration/merge rule (Q8): irbis-api tests; TC-017 re-checks 400 on the live API")],
    "test_data": [("QA-USER", "throwaway account `qa_<case>_<n>`, per-machine password (auth cache, not committed)", "API sign-up, LOCAL dev DB"),
                  ("QA-PROFILED", "QA-USER with experience/interests/locale preset", "`update users set experience=…, interests=…, locale=…` on LOCAL dev DB"),
                  ("CHOICES", "experience weekend, interests peaks + lakes (unless the case says otherwise)", "tapped in the app")],
    "timers": "Splash 1.5 s is checked from QA-event timestamps (onboarding_step splash → welcome), not by waiting; no security timers in this feature.",
    "manual": ["Success haptic on Onb5 and selection haptics (TC-019)",
               "First-run language preselect for device locale uz / ru / other (emulator UI is English): set device language, reinstall, check Onb2",
               "Final Lottie / confetti look (placeholders until the owner delivers the files)"],
}

SCREENS = {
    "welcome": {"open": lambda c=None: first_run_to("welcome"), "root": "onboarding.welcome"},
    "language": {"open": lambda c=None: first_run_to("language"), "root": "onboarding.language"},
    "experience": {"open": lambda c=None: first_run_to("experience"), "root": "onboarding.experience"},
    "interests": {"open": lambda c=None: first_run_to("interests"), "root": "onboarding.interests"},
    "companion": {"open": lambda c=None: first_run_to("companion"), "root": "onboarding.companion"},
}
